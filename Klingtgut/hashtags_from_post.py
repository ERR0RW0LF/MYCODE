import pandas as pd
import os.path
import random
from pandas import *
import sys
import logging

logging.basicConfig(level=logging.DEBUG)
n = len(sys.argv)



if len(sys.argv[1]) == 30:
    user = str(sys.argv[1]) #User ID TODO: must be changed when I add the apis to the code 
    logging.info('information')

userFile =  "hashtags-" + user + "-.csv"
if os.path.isfile(userFile):
    pass
else:
    f = open(userFile, "w")
    f.write("hashtag,viewed,time,liked,disliked,comments,posted,score")
    f.write("\ntest,0,0,0,0,0,0,0")
    f.close()

df = pd.read_csv(userFile, index_col=0, sep=",")

hashtags1 = [] #definiert die Liste hashtag1
hashtags2 = []
check = "#" #da durch wir jeder hastag erkannt
splitPostSubSentinses = []
post = "Dies ist ein #Test Post für #Python. So das ist, der zweite, Satz ich nutze #VS-Code um zu #programmieren." #Post von dem man den Hastag haben will TODO: must be changed when I add the apis to the code 
print(post) #druckt Post in Terminal nur zum debuggen

like = False
dislik = False
time = 10
comment = False

postdot = post.rfind(".") #Findet vom hintersten Punkt im Post die Position
post = post[:postdot] #Löscht den hintersten Punkt im Post
print(post) #druckt Post in Terminal nur zum debuggen

splitPostSentinses = post.split(". ") #trent den Post an jebem Punkt mit Lehrzeichen danach und schreibt in Liste ohne Punkte
print(splitPostSentinses) #druckt List von forheriger Line in Terminal nur zum debuggen

for satz in splitPostSentinses:
    if ', ' in satz:
        splitPostSubSentinses.extend(satz.split(", "))
    else:
        splitPostSubSentinses.append(satz)

print(splitPostSubSentinses)

for subSatz in splitPostSubSentinses:                                                       # TODO: for ö, ü, ä implement recognition and then replace with oe, ue, ae
    hashtags = [idx for idx in subSatz.split() if idx[0].lower() == check.lower()]          # sucht alle hashtags aus den Sätzen und fügt sie alle als einzelne Items in die Liste hashtags1
    hashtags1.extend(hashtags)                                                              #)

print(hashtags1) #druckt List hashtags1 in Terminal nur zum debuggen

print(df)

for hashtag in hashtags1:
    print(hashtag.lower())
    hashtags2.append(hashtag.lower())

print(df)

for hashtag in hashtags2:
    time = random.randrange(4,120) #TODO: must be changed when I add the apis to the code 
    if hashtag in df.index.to_list():
        print(hashtag, " is in csv")
        df.at[hashtag,"viewed"] = df.at[hashtag,"viewed"] + 1
        print(df.at[hashtag,"viewed"])
        df.at[hashtag,"time"] = df.at[hashtag,"time"] + time
        like = random.randrange(0,2)    #TODO: must be changed when I add the apis to the code 
        print(like)
        if like == 1:
            df.at[hashtag,"liked"] = df.at[hashtag,"liked"] + 1
        else:
            df.at[hashtag,"disliked"] = df.at[hashtag,"disliked"] + 1

        if random.randrange(0,4) == 3:
            df.at[hashtag,"comments"] = df.at[hashtag,"comments"] + 1
        elif random.randrange(0,3) == 2:
            df.at[hashtag,"posted"] = df.at[hashtag,"posted"] + 1
            
        df.at[hashtag,"score"] = df.at[hashtag,"time"] / df.at[hashtag,"viewed"] + 10 * (df.at[hashtag,"liked"] - df.at[hashtag,"disliked"]) + 5 * df.at[hashtag,"comments"] + 10 * df.at[hashtag,"posted"]
        #TODO: Add sorting for the hashtags based on ther scores
    else:
        print(hashtag, " is not in csv")

        new_row = {hashtag:[1,0,0,0,0,0,0/1+10*(1-0)+5*1+10*0]} #TODO: must be changed when I add the apis to the code 
        df_new_row = pd.DataFrame.from_dict(data=new_row,
                                            orient='index',
                                            columns=[
                                                "viewed",
                                                "time",
                                                "liked",
                                                "disliked",
                                                "comments",
                                                "posted",
                                                "score"
                                            ])
        print(new_row)
        print(df_new_row)
        df = pd.concat([df, df_new_row])

print(df)
print(hashtag in df.index.to_list())
if hashtag in df.index.to_list():
    print('yes')
else:
    print('no')

df.reset_index
print(df)

df.to_csv(userFile)