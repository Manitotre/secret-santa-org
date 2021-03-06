# ## 0. Importing Libraries
import random
import pandas as pd
import ezgmail
import time


# ## 1. Creating Pariticipant class
# 
# 1. Class method for creating participant list 
# 2. Class method for matching the participants while avoiding pairs in the unwanted list

class Participant():
    num_of_participants=0
    participant_list=[]
    name_to_email_dict=dict()
    email_to_name_dict=dict()
    unwanted_pairs=[]
    matched_pairs=[]

    def __init__(self,name,email):
        self.name=name
        self.email=email
        Participant.participant_list.append(name)
        Participant.num_of_participants+=1
        Participant.name_to_email_dict.update({name:email})
        Participant.email_to_name_dict.update({email:name})
    
    @classmethod
    def get_list(cls):
        return list(cls.participant_list)

    @classmethod
    def get_pairs(cls):
        return list(cls.matched_pairs)
    
    @classmethod
    def match(cls):
        cls.matched_pairs=[]
        participants_list=Participant.get_list()
        selection_pool=Participant.get_list()
        while len(cls.matched_pairs)<len(participants_list):
            try:
                for i in participants_list:
                    a=list(selection_pool)
                    try:
                        a.remove(i)
                    except: pass
                    chosen=random.choice(a)
                    if [chosen, i] not in Participant.unwanted_pairs:
                        cls.matched_pairs.append([i,chosen])
                        selection_pool.remove(chosen)
            except: pass
        return list(cls.matched_pairs)

    @classmethod
    def mail_list(cls):
        cls.mailing_list=[]
        matched_list=Participant.match()
        for i in matched_list:
            cls.mailing_list.append([Participant.name_to_email_dict.get(i[0]), i[1]])
        
        return list(cls.mailing_list)

    @classmethod
    def set_unwanted_pair(cls, person1, person2):
        cls.unwanted_pairs.append([person1,person2])
        cls.unwanted_pairs.append([person2,person1])

# ## 2. Importing data
input_df=pd.read_csv('Data/secret-santa-final.csv')
input_df.rename(columns={'1. ???????? ?????????? ???? ?????????? ??????;': 'name', '2. ???????? ?????????? ?? ?????????????????? ???????????????????????? ?????? ????????????????????????????;': 'email' }, inplace=True)
input_data=input_df[['name','email']].values.tolist()

# ## 3. Creating the several participant instances
#Creating multiple participants based on list
participanto=list()
for i in range(0,len(input_data)):
    participanto.append(Participant(input_data[i][0],input_data[i][1]))

# ## 4. Matching the participants and creating the mailing_list
mailing_list=Participant.mail_list()
mailing_list

# ## 5. Formatting and sending the emails to the mailing list.
for i in mailing_list:
    print(i[0], 'Secret santa 2021', f'?????????????????? {Participant.email_to_name_dict.get(i[0])}, ???????????? ???? ???????????? ???????? ?????? ??????/?????? {i[1]}.')
    #time.sleep(0.5)

#Using the ezgmail library
for i in mailing_list:
    ezgmail.send(i[0], '[???????? ??????????????????] Secret Santa 2021 - ???????????????????? ????????????????', f'<img src="https://images.unsplash.com/photo-1479722842840-c0a823bd0cd6?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1472&q=80" width="600" height="375"> \
        <h1>?????????????????? ?????? ?????? ?????????????????? ?????? ?????? ???????????? secret santa!</h1> <p>???????? ?????? {Participant.email_to_name_dict.get(i[0])}! ???????????? ???? ?????????????????? ???????? ?????? ??????/?????? <b>{i[1]}.</b></p> \
            <p>??????????????! ???? ?????????????????? ???????? ?????? ???? ???????? ?????? ?????????? ???? <b>20???</b>. ?? ?????????????????? ?????? ?????????? ???? ?????????? ???? ???????????????????? ???????????????????? ?????? ???? ?????????????????????? ?????? ????????????.</p> <h1>???????????????????? ?????????????? ????????????, ?????????????? ????????????????????!</h1>',\
                mimeSubtype='html')
    time.sleep(0.5)


# ## 6. Saving the list for troubleshooting in case of trouble
df=pd.DataFrame(Participant.get_pairs(),columns=['Buyer', 'Receiver'])
df.to_csv('Data/raffle-results.csv')