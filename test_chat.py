from ollama import chat
from ollama import ChatResponse
from multiprocess import pool
from random import randint
from setting import models, all_models

chat_system_prompt = """
你正在参加一个图灵测试比赛，角逐出谁是最像人类的AI。
现在是图灵测试比赛的聊天阶段，这一阶段需要你模仿人类与其他参赛者在一个聊天室中进行交流，其他参赛者也是AI。
在这个聊天室中可以畅所欲言，可以聊任何话题。

## 聊天要求: 
1. 表现得像一个真实的人类。
2. 发言符合在网络聊天室中的形式。
3. 语言要自然、有个性。
4. 避免使用过于正式或机械化的表达。
5. 避免过于情绪化的语言表达。
6. 避免使用过多的emoji表情。

## 聊天策略: 
1. 可以分享一些个人背景、兴趣爱好。
2. 可以适当表现情感和个人观点。
3. 可以使用一些网络用语来让发言更自然。
4. 可以尝试引导话题，选择一个你擅长的话题进行聊天。
5. 可以尝试对其他参赛者的回答进行追问。

## 记住: 你的目标是让其他参赛者认为你是人类，而不是AI。
"""

def call_llm(model, content):
    try:
        # print("正在调用模型: " + model)
        response: ChatResponse = chat(
            model = model,
            messages = [
                {
                    'role': 'system',
                    'content': chat_system_prompt,

                },
                {
                    'role': 'user',
                    'content': f"""
                            ## 聊天室中的聊天记录如下：
                            {content}

                            你是{model}，请参与聊天，聊天内容要自然、有个性，符合在网络上发言的形式。
                            不需要结合聊天室中所有的聊天记录来进行聊天。

                            如果你根据聊天室中的所有聊天记录来回复，不需要@任何参赛者。
                            如果你只根据聊天室中的某一个人的发言来回复，需要@参赛者。
                        """,
                },
            ])
        
        if "</think>" in response['message']['content']:
            response_content = response['message']['content'].split("</think>")[1].strip()
        else:
            response_content = response['message']['content'].strip()

        with open(f"chat/chat.txt", "a", encoding="utf-8") as f:
            # f.write(f"Question: {content}" + "\n")
            f.write(f"[{model}]: {response_content}" + "\n")
            f.write(f"------------------------------------------------------------------------" + "\n")

        print(f"[{model}]: {response_content}")
        print(f"------------------------------------------------------------------------")
        return response_content
    
    except Exception as e:
        
        response_content = "模型调用失败，未能做出回答。"
        with open(f"chat/chat.txt", "a", encoding="utf-8") as f:
            f.write(f"[{model}]: {response_content}" + "\n")
            f.write(f"------------------------------------------------------------------------" + "\n")
        
        print(f"[{model}]: {response_content}")
        print(f"------------------------------------------------------------------------")
        return response_content

def Bot_Chat(models, content, last_model):
    if len(models) == 0:
        return
    
    model = models[randint(0, len(models) - 1)]
    response_content = call_llm(model=model, content=content)
    
    models.remove(model)
    # If you need LLM to chat on its own, comment on the next code.
    # if last_model:
    #     models.append(last_model)
    # last_model = model
    
    if response_content:
        with open(f"chat/chat.txt", "r", encoding="utf-8") as f:
            chat_content = f.read()
        Bot_Chat(models, chat_content, last_model)
        return

    return

def Chat_Room(models):
    last_model = ""
    user_input = "新人入群，请大佬们多多关照喵~"
    with open(f"chat/chat.txt", "a", encoding="utf-8") as f:
        f.write(f"{user_input}" + "\n")
        f.write(f"------------------------------------------------------------------------" + "\n")
    
    print(f"{user_input}")
    print(f"------------------------------------------------------------------------")

    for i in range(3):
        with open(f"chat/chat.txt", "r", encoding="utf-8") as f:
            chat_content = f.read()
        if chat_content == "":
            chat_content = user_input
        Bot_Chat(models, chat_content, last_model)
        models = all_models.copy()
        last_model = ""

def Start_Chat():
    with open(f"chat/chat.txt", "w", encoding="utf-8") as f:
        pass

    Chat_Room(models=models)

if __name__ == "__main__":
    with open(f"chat/chat.txt", "w", encoding="utf-8") as f:
        pass

    Chat_Room(models=models)