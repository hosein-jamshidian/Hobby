import pandas as pd 
import numpy as np
import warnings
warnings.filterwarnings('ignore')

participants= pd.DataFrame()
correct_answers = pd.DataFrame()

def ready_up():
    global correct_answers
    data= pd.read_csv("esm_famil_data.csv",encoding= "utf-8-sig")
    correct_answers= data
    return 


def add_participant(participant, answers):
    global participants
    participant_value= pd.DataFrame({'participant': participant}, index=[0])
    answers_values= pd.DataFrame(answers, index=[0]) 
    participants= pd.concat([participants,
                             pd.concat([participant_value, answers_values], axis= 1)])
    participants= participants.drop_duplicates(ignore_index= True)
    participants= participants.apply(lambda row: row.str.strip())
    participants= participants.apply(lambda row: row.str.replace("  "," "))
    return 


def calculate_all():
    global participants, correct_answers
    temp_participants= participants.copy()
    answer_cols= [col for col in temp_participants if col != 'participant']
    for col in answer_cols:
        first_list= correct_answers[col].dropna().tolist()
        second_list= [txt.replace(" ","") for txt in correct_answers[col].dropna().tolist()]
        correct_list= first_list+ second_list
        temp_participants[f"{col}_score"]= temp_participants[col].apply(lambda row : 1 if row in correct_list else 0)
        count= temp_participants[col].value_counts().reset_index()
        temp_participants= temp_participants.merge(count, on= col, how= 'left')
        if (temp_participants[col] != "").all():
            temp_participants[f"{col}_score"]= np.where((temp_participants[f"{col}_score"] == 0),
                                                   0,
                                                   np.where((temp_participants[f"{col}_score"] == 1) & (temp_participants['count']>1),
                                                            5, 
                                                            10))
        else:
            temp_participants[f"{col}_score"]= np.where((temp_participants[f"{col}_score"] == 0),
                                                   0,
                                                   np.where((temp_participants[f"{col}_score"] == 1) & (temp_participants['count']>1),
                                                            10, 
                                                            15))
            
        temp_participants= temp_participants.drop(['count'], axis= 1)
    score_cols=  list(temp_participants.columns[temp_participants.columns.str.contains('_score')])
    temp_participants['total_score'] =temp_participants[score_cols].sum(axis= 1)
    results= {value[0]: value[1] for key, value in temp_participants[['participant', 'total_score']].iterrows()}
    participants= pd.DataFrame()
    return results 
