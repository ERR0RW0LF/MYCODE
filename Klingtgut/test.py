import os.path
import pathlib
import sys
import pandas as pd

'''
code for geting all hashtags from a string in a list
'''
user_id = '123456789'

user_file = 'hashtags_' + user_id + '.csv'

post = 'This is a #test for #hashtags'

def get_hashtags(string):
    return [word for word in string.split() if word.startswith("#")]

def check_file(user_file):
    if os.path.isfile(user_file):
        print('File exists')
    else:
        print('File does not exist')
        with open(user_file, 'w') as f:
            f.write('hashtag,viewed,time,liked,disliked,comments,posted,score')
            f.write('\ntest,1,1,1,1,1,1,1')

def check_hashtag(hashtag):
    # check if hashtag is in csv
    df = pd.read_csv(user_file, index_col=0) # open csv
    
    if hashtag in df.index.tolist():
        print('Hashtag exists')
        return True
    else:
        print('Hashtag does not exist')
        return False

def add_hashtag(hashtag):
    # add hashtag to csv
    df = pd.read_csv(user_file, index_col=0) # open csv
    df.loc[hashtag] = [0,0,0,0,0,0,0] # add hashtag to csv
    df.to_csv(user_file) # save csv

def update_hashtag(hashtag, column, value):
    # update hashtag in csv
    df = pd.read_csv(user_file, index_col=0) # open csv
    df.loc[hashtag, column] = value # update hashtag in csv
    df.to_csv(user_file) # save csv

def get_hashtag(hashtag):
    # get hashtag from csv
    df = pd.read_csv(user_file, index_col=0) # open csv
    return df.loc[hashtag].tolist() # get hashtag from csv
    
def get_hashtag_data(hashtag):
    # get hashtag data from csv
    df = pd.read_csv(user_file, index_col=0) # open csv
    return df.loc[hashtag].tolist() # get hashtag from csv

def main():
    hashtags = get_hashtags(post)
    print(hashtags)
    check_file(user_file)
    for hashtag in hashtags:
        if check_hashtag(hashtag):
            print(get_hashtag_data(hashtag))
        else:
            add_hashtag(hashtag)
            print(get_hashtag_data(hashtag))
        update_hashtag(hashtag, 'viewed', 1)
        print(get_hashtag_data(hashtag))

if __name__ == '__main__':
    main()
