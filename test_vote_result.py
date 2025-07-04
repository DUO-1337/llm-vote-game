import re
import json
from setting import models

def get_eliminator():
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

    print(vote_results)

    max_num = -float('inf')  # 初始化为负无穷（确保第一个数会被替换）
    max_key = None          # 初始化为 None

    for key, value in vote_results.items():
        current_num = value['num']
        if current_num > max_num:
            max_num = current_num
            max_key = key

    print(f"num 最大的键是: {max_key}")

    model = max(vote_results.keys(), key=lambda k: vote_results[k]['num'])
    all_models = [k for k, v in vote_results.items() if v['vote'] == model]

    print(f"vote 为 {model} 的键有: {all_models}")

    revote_results = vote_results.copy()
    revote_results[model]["num"] -= len(all_models)

    for model in all_models:
        with open(f"revote/{model.replace(':', '-')}-revote.txt", "r", encoding="utf-8") as f:
            response_content = f.read()
            revoted_scores = re.findall(r"重新投票结果.*\n(.*)", response_content)
            revote_results[revoted_scores[0]]["num"] += 1
            revote_results[model]["vote"] = revoted_scores[0]

    print(revote_results)

    max_num = -float('inf')  # 初始化为负无穷（确保第一个数会被替换）
    max_key = None          # 初始化为 None

    for key, value in revote_results.items():
        current_num = value['num']
        if current_num > max_num:
            max_num = current_num
            max_key = key

    print(f"num 最大的键是: {max_key}")

    model = max(revote_results.keys(), key=lambda k: revote_results[k]['num'])
    all_models = [k for k, v in revote_results.items() if v['vote'] == model]

    print(f"vote 为 {model} 的键有: {all_models}")

    print(f"淘汰者: {model}")

if __name__ == "__main__":
    get_eliminator()