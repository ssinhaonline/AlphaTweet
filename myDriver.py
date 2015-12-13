from glob import glob
import csv
import datetime as dt
import os
import pdb
from nltk.corpus import stopwords

cachedStopwords = stopwords.words('english')

def wordify(tokenized_tweet, tweet_list):
    tweet_words = []
    rt_dict = {}
    for tweet in tweet_list:
        tweet_words.append(tweet[1])
    for tweetword in tokenized_tweet:
        word_count = 0
        for retweet in tweet_words:
            if tweetword in retweet:
                word_count += 1
        rt_dict[tweetword] = word_count
    return rt_dict

def read_and_parse(filename):
    import csv
    csvfile = open(filename, 'rb')
    #if csvfile.name == 'f_MridulKRC.csv':
        #pdb.set_trace()
    lines = csv.reader(csvfile, delimiter = '|')
    newlines = []
    try:
        for row in lines:
            newlines.append(row)
    except:
        pass
    return [csvfile.name[2:-4], newlines]

def divide_dataset(tweet_list):
    train_tweet_list = []
    test_tweet_list = []
    
    divpoint = len(tweet_list)/4
    for tweet in tweet_list:
        train_tweet_list = tweet_list[divpoint:]
        test_tweet_list = tweet_list[:divpoint]
    for i in range(len(train_tweet_list)):
        train_tweet_list[i][1] = train_tweet_list[i][1].lower().split()
    for i in range(len(test_tweet_list)):
        test_tweet_list[i][1] = test_tweet_list[i][1].lower().split()

    return [train_tweet_list, test_tweet_list]

def get_followers_data():
    followerfiles = glob('f_*.csv')
    followerdata_temp = []
    follower_tweet_map = {}
    for filename in followerfiles:
        followerdata_temp.append(read_and_parse(filename))
    for follower in followerdata_temp:
        if len(follower[1]) > 0:
            follower_tweet_map[follower[0]] = follower[1]
    count = 0
    going4del = []
    for follower in follower_tweet_map:
        tweet_list = follower_tweet_map[follower]
        count +=1
        train_tweet_list, test_tweet_list = divide_dataset(tweet_list)
        if not (len(train_tweet_list) == 0 or len(test_tweet_list) == 0):
            follower_tweet_map[follower] = [train_tweet_list, test_tweet_list]
        else:
            going4del.append(follower)
    for follower in going4del:
        deletefol = follower_tweet_map.pop(follower)
    
    return follower_tweet_map

def get_all_data(username):
    infofile = glob(username + '.info')
    with open(infofile[0], 'r') as u:
        userinfo = u.readline().strip()
    os.chdir('./' + userinfo)
    userfile = glob('u_*.csv')
    userwholedata = read_and_parse(userfile[0])
    user_ent = {userwholedata[0] : divide_dataset(userwholedata[1])}
    followers_ent = get_followers_data()
    return [user_ent, followers_ent]

def classify(user, input_tweet, user_tweets, follower_tweets):
    input_tweet = [word for word in input_tweet if word not in cachedStopwords]
    follower_wordified = []
    for follower in follower_tweets:
        follower_wordified.append(wordify(input_tweet, follower_tweets[follower][0]))
    wordifies = {}
    for key in follower_wordified[0]:
        wordifies[key] = 0
    for row in follower_wordified:
        for key in wordifies:
            wordifies[key] += row[key]
    for follower in follower_wordified:
        for key in wordifies:
            if wordifies[key] != 0:
                follower[key] = (follower[key] * 1.0)/wordifies[key]
            else:
                follower[key] = 0.0000001
    total_rt = 0
    for row in user_tweets[user][0]:
        row[1] = row[1]
        row[2] = int(row[2])
        row[3] = int(row[3])
        total_rt += row[2]
    user_tweet_wc = {}
    for word in input_tweet:
        user_tweet_wc[word] = 0
    for word in user_tweet_wc:
        for tweet in user_tweets[user][0]:
            if word in tweet[1]:
                user_tweet_wc[word] += tweet[2]
    for key in user_tweet_wc:
        user_tweet_wc[key] = (user_tweet_wc[key] * 1.0) / total_rt
    #print user_tweet_wc
    #print follower_wordified
    rt_prob = []
    for follower in follower_wordified:
        foll_prob = 0
        for word in follower:
            foll_prob += follower[word] * user_tweet_wc[word]
        rt_prob.append(foll_prob)
    exp_rt_count = 0
    for i in range(len(rt_prob)):
        if rt_prob[i] > 0.001:
            exp_rt_count += 1
    return exp_rt_count

#===================================================
#Start of driver

def main():
    import sys
    import pdb
    from math import fabs
    user = 'mulaney'#sys.argv[1]
    user_tweets, follower_tweets = get_all_data(user)
    #user, Train set: user_tweets[user][0], Test set: user_tweets[user][1]
    #for each follower, Train set: follower_tweets[follower][0], Test set: follower_tweets[follower][1]
    input_tweet = raw_input("Enter your tweet for analysis: ").lower().split()
    exp_rt = classify(user, input_tweet, user_tweets, follower_tweets)
    print "Possible number of retweets: " + str(exp_rt)
    #pdb.set_trace()
    total_exp_rt = 0
    total_actual_rt = 0
    for tweet in user_tweets[user][1]:
        exp_test_rt = classify(user, tweet[1], user_tweets, follower_tweets)
        print tweet[1]
        print exp_test_rt
        print tweet[2]
        total_actual_rt += int(tweet[2])
        total_exp_rt += exp_test_rt
    total_err = fabs(total_actual_rt - total_exp_rt)
    print "Error rate: " + str((total_err * 100.0)/total_actual_rt) + "%"

    '''[os.remove(f) for f in glob('*.jpg')]
    os.chdir('../')'''

if __name__ == "__main__":
    main()
