from test_init import Start_Init
from test_chat import Start_Chat
from test_vote import Start_Vote
from test_against import Start_Against
from test_revote import Start_Revote
from test_vote_result import Start_Eliminate
from setting import models, all_models
import re
import json

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
    # print(f"num最大值为：{max_num}")
    # print(f"对应的key(s)为：{max_keys}")

    # vote_models = [k for k, v in vote_results.items() if v['vote'] == model]
    
    print("投票结果: ")
    print(json.dumps(vote_results, indent=4, ensure_ascii=False))
    print(f"------------------------------------------------------------------------")

    return max_keys

def get_revote_result():
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

    # print(vote_results)

    max_num = -float('inf')  # 初始化为负无穷（确保第一个数会被替换）
    max_key = None          # 初始化为 None

    for key, value in vote_results.items():
        current_num = value['num']
        if current_num > max_num:
            max_num = current_num
            max_key = key

    # print(f"num 最大的键是: {max_key}")

    model = max(vote_results.keys(), key=lambda k: vote_results[k]['num'])
    all_models = [k for k, v in vote_results.items() if v['vote'] == model]

    # print(f"vote 为 {model} 的键有: {all_models}")

    revote_results = vote_results.copy()
    revote_results[model]["num"] -= len(all_models)

    for model in all_models:
        with open(f"revote/{model.replace(':', '-')}-revote.txt", "r", encoding="utf-8") as f:
            response_content = f.read()
            revoted_scores = re.findall(r"重新投票结果.*\n(.*)", response_content)
            revote_results[revoted_scores[0]]["num"] += 1
            revote_results[model]["vote"] = revoted_scores[0]
    
    # 步骤1：提取所有num值
    num_values = [item['num'] for item in revote_results.values()]

    # 步骤2：找到num的最大值（处理空字典或无效数据的情况）
    if not num_values:  # 处理字典为空的情况
        max_num = None
    else:
        max_num = max(num_values)

    # 步骤3：收集所有num等于最大值的键
    max_keys = [key for key, item in revote_results.items() if item['num'] == max_num]
    # print(revote_results)

    print("重新投票结果: ")
    print(json.dumps(vote_results, indent=4, ensure_ascii=False))
    print(f"------------------------------------------------------------------------")
    
    return max_keys

if __name__ == '__main__':
    while len(models) > 2:
        Start_Init()
        Start_Chat()
        Start_Vote()
        
        max_keys = get_vote_result()
        if len(max_keys) > 1:
            print(f"投票结果有同票: {max_keys}，重新讨论")
            print(f"------------------------------------------------------------------------")
            continue

        Start_Against()
        Start_Revote()
        max_keys = get_revote_result()
        if len(max_keys) > 1:
            print(f"重新投票结果有同票: {max_keys}，重新讨论")
            print(f"------------------------------------------------------------------------")
            continue
        
        eliminated_model = Start_Eliminate()
        models.remove(eliminated_model)
        all_models.remove(eliminated_model)
    
    print(f"比赛结束")
    print(f"剩余模型：{models}")