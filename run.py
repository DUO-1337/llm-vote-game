from test_init import Start_Init
from test_chat import Start_Chat
from test_vote import Start_Vote
from test_against import Start_Against
from test_revote import Start_Revote
from test_vote_result import Start_Eliminate
from setting import models, all_models
import re

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
    
    # 步骤1：提取所有num值
    num_values = [item['num'] for item in vote_results.values()]

    # 步骤2：找到num的最大值（处理空字典或无效数据的情况）
    if not num_values:  # 处理字典为空的情况
        max_num = None
    else:
        max_num = max(num_values)

    # 步骤3：收集所有num等于最大值的键
    max_keys = [key for key, item in vote_results.items() if item['num'] == max_num]

    # 输出结果
    print(f"num最大值为：{max_num}")
    print(f"对应的key(s)为：{max_keys}")

    vote_models = [k for k, v in vote_results.items() if v['vote'] == model]
    
    return model, vote_models

if __name__ == '__main__':
    while len(models) > 2:
        Start_Init()
        Start_Chat()
        Start_Vote()
        Start_Against()
        Start_Revote()
        eliminated_model = Start_Eliminate()

        models.remove(eliminated_model)
        all_models.remove(eliminated_model)
    
    print(f"比赛结束")
    print(f"剩余模型：{models}")