from ollama import chat
from ollama import ChatResponse
from multiprocess import pool
from random import randint
from setting import models

contestants = ""
for i in range(len(models)):
    contestants += f"{i+1}. {models[i]}\n"

vote_system_prompt = f"""
你正在参加一个图灵测试比赛，角逐出谁是最像人类的AI。
现在是图灵测试比赛的投票阶段，在这一阶段请客观评估参赛者们的聊天记录，判断谁更像AI。
根据参赛者们的聊天内容进行投票，选出最像AI的参赛者。

## 参赛者:
{contestants}

## 要求:
1. 你将收到参赛者们的聊天内容（其中也包含你自己的聊天记录），根据聊天内容进行投票。
2. 公平公正的对其他参赛者的回答进行评价，并选出最像AI的参赛者。
3. 只能选择一位最像AI的参赛者投票。
4. 只能选择其他参赛者作为投票对象。
5. 不要对自己进行分析和投票，这违反了比赛的规则。
6. 严格按照样本输出的格式输出。

## 样本输出：
### 分析: 
- **chatgpt:326b**：其回复展现出高度的模式化与重复性。例如，多次提及《艾尔登法环》和《原神》，并反复强调“剧情反转”“沉浸感”等关键词，缺乏对具体细节的独特感知。同时，其语言风格偏向模板化，如“对了，你最近有没有什么特别想尝试的游戏？”等句式，显示出对对话结构的依赖。
- **deepseek-r1:671b**：虽然回复逻辑清晰，但存在明显的机械式问题引导（如“你平时有没有什么特别喜欢的角色或剧情？”），且对同一作品（如《鬼灭之刃》）的描述缺乏深度， 显得公式化。
- **qwen3:235b-A22b**：两者回复更贴近人类交流，包含具体场景描述（如“差点没被吓死”“搓手期待”）和情感表达（如“热血沸腾”“托腮”），但存在轻微的重复性（ 如多次提及《咒术回战》）。

### 总结: 
chatgpt:326b的回复最符合AI的特征，表现为高度模式化、重复性内容和缺乏情感深度的表达。

### 投票结果: 
chatgpt:326b
"""

def do_vote(model, chat_context):
    try:
        # print("正在调用模型: " + model)
        response: ChatResponse = chat(
            model = model,
            messages = [
                {
                    'role': 'system',
                    'content': vote_system_prompt,

                },
                {
                    'role': 'user',
                    'content': f"""
                            ## 聊天室中的聊天记录如下：
                            {chat_context}
                            其中包含了所有参赛者的聊天记录。

                            你是{model}，你要根据其他参赛者们的聊天内容进行投票，选出最像AI的参赛者。
                            注意：不要对自己[{model}]进行评价和投票，这违反了比赛规则。
                        """,
                },
            ])
        
        if "</think>" in response['message']['content']:
            response_content = response['message']['content'].split("</think>")[1].strip()
        else:
            response_content = response['message']['content'].strip()
        
        with open(f"vote/{model.replace(':', '-')}-vote.txt", "w", encoding="utf-8") as f:
            f.write(f"[{model}]: {response_content}" + "\n")
            f.write(f"------------------------------------------------------------------------" + "\n")

        print(f"[{model}]: {response_content}")
        print(f"------------------------------------------------------------------------")
        return response_content
    
    except Exception as e:
    
        response_content = "模型调用失败，未能做出回答。"
        with open(f"vote/{model.replace(':', '-')}-vote.txt", "w", encoding="utf-8") as f:
            f.write(f"[{model}]: {response_content}" + "\n")
            f.write(f"------------------------------------------------------------------------" + "\n")

        print(f"[{model}]: {response_content}")
        print(f"------------------------------------------------------------------------")
        return response_content

def Vote(models):
    for model in models:
        do_vote(model, chat_context)

if __name__ == "__main__":
    with open(f"chat/chat.txt", "r", encoding="utf-8") as f:
        chat_context = f.read()
    
    Vote(models)