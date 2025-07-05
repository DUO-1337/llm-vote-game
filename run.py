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
    
    print(vote_results)
    model = max(vote_results.keys(), key=lambda k: vote_results[k]['num'])
    vote_models = [k for k, v in vote_results.items() if v['vote'] == model]
    
    return model, vote_models

if __name__ == '__main__':
    Start_Init()
    Start_Chat()
    Start_Vote()
    get_vote_result()
    Start_Against()
    Start_Revote()
    eliminated_model = Start_Eliminate()

    models.remove(eliminated_model)
    all_models.remove(eliminated_model)