from test_init import Start_Init
from test_chat import Start_Chat
from test_vote import Start_Vote
from test_against import Start_Against
from test_revote import Start_Revote
from test_vote_result import Start_Eliminate
from setting import models, all_models

if __name__ == '__main__':
    
    Start_Init()
    Start_Chat()
    Start_Vote()
    Start_Against()
    Start_Revote()
    eliminated_model = Start_Eliminate()

    models.remove(eliminated_model)
    all_models.remove(eliminated_model)