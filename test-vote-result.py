import re
import json
from setting import models

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

    revote_results = {}
    for model in all_models:
        revote_results[model] = {}
        revote_results[model]["vote"] = ""
        revote_results[model]["num"] = 0

    for model in models:
        with open(f"vote/{model.replace(':', '-')}-vote.txt", "r", encoding="utf-8") as f:
            response_content = f.read()
            voted_scores = re.findall(r"重新投票结果.*\n(.*)", response_content)
            revote_results[model]["vote"] = voted_scores[0]
            revote_results[voted_scores[0]]["num"] += 1
    print(revote_results)