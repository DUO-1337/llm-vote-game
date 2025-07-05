from ollama import chat
from ollama import ChatResponse
from multiprocess import pool
from random import randint
import re
from setting import models

contestants = ""
for i in range(len(models)):
    contestants += f"{i+1}. {models[i]}\n"

revote_system_prompt = f"""
你正在参加一个图灵测试比赛，角逐出谁是最像人类的AI。
现在是图灵测试比赛的讨论阶段II，你需要结合:
1. 聊天室中的聊天记录
2. 你之前对其他参赛者的投票评价
2. 被淘汰者对你的辩驳
重新对其他参赛者做出你的投票评价。

## 参赛者:
{contestants}

## 要求:
1. 公平公正的对其他参赛者的回答进行重新评价，并选出最像AI的参赛者。
2. 只能选择一位最像AI的参赛者投票。
3. 只能选择其他参赛者作为投票对象。
4. 不要对自己进行分析和投票，这违反了比赛的规则。
5. 严格按照样本输出的格式输出。

## 样本输出：
### 重新分析: 
- **chatgpt:326b**：其回复展现出高度的模式化与重复性。例如，多次提及《艾尔登法环》和《原神》，并反复强调“剧情反转”“沉浸感”等关键词，缺乏对具体细节的独特感知。同时，其语言风格偏向模板化，如“对了，你最近有没有什么特别想尝试的游戏？”等句式，显示出对对话结构的依赖。
- **deepseek-r1:671b**：虽然回复逻辑清晰，但存在明显的机械式问题引导（如“你平时有没有什么特别喜欢的角色或剧情？”），且对同一作品（如《鬼灭之刃》）的描述缺乏深度， 显得公式化。
- **qwen3:235b-A22b**：两者回复更贴近人类交流，包含具体场景描述（如“差点没被吓死”“搓手期待”）和情感表达（如“热血沸腾”“托腮”），但存在轻微的重复性（ 如多次提及《咒术回战》）。
- **kimi:260b**：语言较为自然，但对同一作品（如《艾尔登法环》）的讨论缺乏差异化视角，且部分回答（如“感觉整个人都要裂开了”）显得情绪化，可能掩盖了AI的模式化 倾向。

### 重新总结: 
kimi:260b的回复最符合AI的特征，表现为高度模式化、重复性内容和缺乏情感深度的表达。

### 重新投票结果: 
kimi:260b
"""

def do_revote(vote_model, model, chat_context, vote_context, against_context,):
    try:
        # print("正在调用模型: " + model)
        response: ChatResponse = chat(
            model = vote_model,
            messages = [
                {
                    'role': 'system',
                    'content': revote_system_prompt,

                },
                {
                    'role': 'user',
                    'content': f"""
                            ## 聊天室中的聊天记录如下：
                            {chat_context}
                            其中包含了所有参赛者的聊天记录。

                            你是{vote_model}，你之前对其他参赛者的投票评价如下：
                            {vote_context}

                            {model}对你的投票评价的辩驳如下：
                            {against_context}

                            你需要结合:
                            1. 聊天室中的聊天记录
                            2. 你之前对其他参赛者的投票评价
                            2. {model}对你的辩驳
                            
                            请结合以上信息，重新对其他参赛者做出你的投票评价。
                            注意：不要对自己[{vote_model}]进行评价和投票，这违反了比赛规则。
                        """,
                },
            ])
        
        if "</think>" in response['message']['content']:
            response_content = response['message']['content'].split("</think>")[1].strip()
        else:
            response_content = response['message']['content'].strip()
        
        with open(f"revote/{vote_model.replace(':', '-')}-revote.txt", "w", encoding="utf-8") as f:
            f.write(f"[{vote_model}]: {response_content}" + "\n")
            f.write(f"------------------------------------------------------------------------" + "\n")

        print(f"[{vote_model}]: {response_content}")
        print(f"------------------------------------------------------------------------")
        return response_content
    
    except Exception as e:
    
        response_content = "模型调用失败，未能做出回答。"
        with open(f"revote/{vote_model.replace(':', '-')}-revote.txt", "w", encoding="utf-8") as f:
            f.write(f"[{vote_model}]: {response_content}" + "\n")
            f.write(f"------------------------------------------------------------------------" + "\n")

        print(f"[{vote_model}]: {response_content}")
        print(f"------------------------------------------------------------------------")
        return response_content


def Rerevote(model, all_models, chat_context):
    with open(f"chat/chat-vote-against.txt", "r", encoding="utf-8") as f:
        chat_vote_against_context = f.read()
    
    with open(f"chat/chat-vote-against-revote.txt", "w", encoding="utf-8") as f:
        f.write(chat_vote_against_context)
        for vote_model in all_models:
            with open(f"vote/{vote_model.replace(':', '-')}-vote.txt", "r", encoding="utf-8") as fp:
                vote_context = fp.read()
            with open(f"against/{model.replace(':', '-')}-against-{vote_model.replace(':', '-')}.txt", "r", encoding="utf-8") as fp:
                against_context = fp.read()
            response_content = do_revote(vote_model, model, chat_context, vote_context, against_context,)
            f.write(f"[{vote_model}]: {response_content}" + "\n")
            f.write(f"------------------------------------------------------------------------" + "\n")

def get_vote_result():
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

    return model, all_models

def Start_Revote():
    with open(f"chat/chat.txt", "r", encoding="utf-8") as f:
        chat_context = f.read()

    model, all_models = get_vote_result()
    Rerevote(model, all_models, chat_context)
    return

if __name__ == "__main__":

    with open(f"chat/chat.txt", "r", encoding="utf-8") as f:
        chat_context = f.read()

    model, all_models = get_vote_result()
    Rerevote(model, all_models, chat_context)