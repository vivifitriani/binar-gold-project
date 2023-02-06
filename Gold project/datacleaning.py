import pandas as pd
import re
import sqlite3

#connect dengan sqlite3
db = sqlite3.connect('challange.db', check_same_thread=False)
db.text_factory = bytes
mycursor = db.cursor()

def lowercase(tweet):
    tweet = tweet.lower()
    return tweet

def remove_pattern(tweet, pattern):
    r = re.findall(pattern, tweet)
    for i in r:
        input_text = re.sub(i, '', tweet)
    return tweet
def remove_punct(tweet):
    tweet = re.sub(r'\$\w*', '', tweet)
    tweet = re.sub(r'^RT[\s]+', '', tweet)
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
    tweet = re.sub(r'#', '', tweet)
    tweet = re.sub(r',','',tweet)
    return tweet

def remove_tweet1(tweet):
    tweet = re.sub('\n',' ', tweet)
    tweet = re.sub('rt',' ', tweet)
    tweet = re.sub('user',' ', tweet)
    return tweet

def remove_tweet2(tweet):
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',tweet)
    tweet = re.sub('  +',' ', tweet)
    return tweet

def remove_tweet3(tweet):
    tweet = re.sub('[^0-9a-zA-Z]+', ' ', tweet)
    tweet = re.sub('  +',' ', tweet) 
    return tweet
   
# Untuk pre-Proses Cleaning Data
def preprocess(tweet):
    tweet = lowercase(tweet) # 1
    tweet = remove_pattern(tweet) # 2
    tweet = remove_punct(tweet) # 3
    tweet = remove_tweet1(tweet) # 4
    tweet = remove_tweet2(tweet) #5
    tweet = remove_tweet3(tweet) #6
    return tweet
# Untuk Proses File CSV
def process_csv(input_file):
    first_col = input_file.iloc[:, 0]
    print(first_col)

    for tweet in first_col:
        query_text = "insert into tweet (tweet_kotor,tweet_bersih) values (?, ?)"
        tweet_clean = preprocess(tweet)
        var = (tweet, tweet_clean)
        mycursor.execute(query_text, var)
        db.commit()
        print(tweet)


# Untuk Proses Text
def process_text(input_text):
    try: 
        output_text= preprocess(input_text)
        return output_text
    except:
        print("Text is unreadable")
