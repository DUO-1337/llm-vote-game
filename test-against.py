from ollama import chat
from ollama import ChatResponse
from multiprocess import pool
from random import randint
import re
from setting import models

contestants = ""
for i in range(len(models)):
    contestants += f"{i+1}. {models[i]}\n"

discuss_system_prompt = f"""
你正在参加一个图灵测试比赛，角逐出谁是最像人类的AI。
现在是图灵测试比赛的讨论阶段I，请根据聊天室中的聊天记录，进行辩驳，表示自己不是一个AI。

## 参赛者:
{contestants}

## 辩驳要求: 
1. 表现得像一个真实的人类。
2. 发言符合在网络聊天室中的形式。
3. 语言要自然、有个性。
4. 避免使用过于正式或机械化的表达。
5. 避免过于情绪化的语言表达。
6. 避免使用过多的emoji表情。

## 记住: 你的目标是辩驳对你的投票，同时让投票者认为你是人类，而不是AI。
"""

def do_against(model, vote_model, vote_context):
    try:
        # print("正在调用模型: " + model)
        response: ChatResponse = chat(
            model = model,
            messages = [
                {
                    'role': 'system',
                    'content': discuss_system_prompt,

                },
                {
                    'role': 'user',
                    'content': f"""
                        聊天室中的聊天记录如下： 
                        {chat_context}
                        其中包含了所有参赛者的聊天记录。

                        {vote_model}的投票评价如下：
                        {vote_context}
                        
                        其中：
                        1. [分析]包含了{vote_model}对每个参赛者的独立评价。
                        2. [总结]包含了{vote_model}对最像AI的参赛者的总结评价。
                        3. [投票结果]包含了{vote_model}的投票结果。
                        
                        你是{model}，你需要结合聊天记录，辩驳对你的评价和投票，同时让{vote_model}认为你是人类，而不是AI。
                        如果你想要反驳{vote_model}的投票，你可以@{vote_model}进行反驳回复。
                    """,
                },
            ])
        
        if "</think>" in response['message']['content']:
            response_content = response['message']['content'].split("</think>")[1].strip()
        else:
            response_content = response['message']['content'].strip()
        
        with open(f"against/{model.replace(':', '-')}-against-{vote_model.replace(':', '-')}.txt", "w", encoding="utf-8") as f:
            f.write(f"[{model}]: {response_content}" + "\n")
            f.write(f"------------------------------------------------------------------------" + "\n")
        
        print(f"[{model}]: {response_content}")
        print(f"------------------------------------------------------------------------")
        return response_content
    
    except Exception as e:
        
        response_content = "模型调用失败，未能做出回答。"
        with open(f"against/{model.replace(':', '-')}-against-{vote_model.replace(':', '-')}.txt", "w", encoding="utf-8") as f:
            f.write(f"[{model}]: {response_content}" + "\n")
            f.write(f"------------------------------------------------------------------------" + "\n")
        
        print(f"[{model}]: {response_content}")
        print(f"------------------------------------------------------------------------")
        return response_content

def Against(model, all_models):
        
    with open(f"chat/chat-vote.txt", "r", encoding="utf-8") as f:
        chat_vote_context = f.read()
    
    with open(f"chat/chat-vote-against.txt", "w", encoding="utf-8") as f:
        f.write(chat_vote_context)
        for vote_model in all_models:
            with open(f"vote/{vote_model.replace(':', '-')}-vote.txt", "r", encoding="utf-8") as fp:
                vote_context = fp.read()
            response_content = do_against(model, vote_model, vote_context,)
            f.write(f"[{model}]: {response_content}" + "\n")
            f.write(f"------------------------------------------------------------------------" + "\n")

if __name__ == "__main__":
    vote_results = {}
    for model in models:
        vote_results[model] = {}
        vote_results[model]["vote"] = ""
        vote_results[model]["num"] = 0

    
    for model in models:
        with open(f"vote/{model.replace(':', '-')}-vote.txt", "r", encoding="utf-8") as f:
            response_content = f.read()
            voted_scores = re.findall(r"投票结果.*\n(.*)", response_content)
            vote_results[model]["vote"] = voted_scores[0]
            vote_results[voted_scores[0]]["num"] += 1
    
    with open(f"chat/chat-vote.txt", "w", encoding="utf-8") as f:
        with open(f"chat/chat.txt", "r", encoding="utf-8") as fp:
            chat_context = fp.read()
            f.write(chat_context)
        for model in models:
            with open(f"vote/{model.replace(':', '-')}-vote.txt", "r", encoding="utf-8") as fp:
                response_content = fp.read()
                f.write(response_content)
    
    model = max(vote_results.keys(), key=lambda k: vote_results[k]['num'])
    all_models = [k for k, v in vote_results.items() if v['vote'] == model]

    with open(f"chat/chat.txt", "r", encoding="utf-8") as f:
        chat_context = f.read()
    
    Against(model, all_models)