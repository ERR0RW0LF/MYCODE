import os.path


user = "113231132311323113231132311323" #User ID
userFile = "hashtags " + user + ".csv"
if os.path.isfile(userFile):
    f =     f = open(userFile, "w+")
    print(f.read())
    f.write("hashtag")
    print(f.readlines())
    f.close
else:
    f = open(userFile, "w")
    f.write("hashtag,viewed,time,liked,disliked,comments,posted,score")
    f.write("\ntest,1,10,5,3,2,1,77")
    print(f.read())
    f.close()