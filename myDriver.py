from glob import glob
import csv
import datetime as dt
import os
import pdb

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
        #print "In " + csvfile.name
        #print row
        #raise
        pass
    return [csvfile.name[2:-4], newlines]
        

userfile = glob('u_*.csv')
userdata = read_and_parse(userfile[0])
#print userdata

followerfiles = glob('f_*.csv')
followerdata_temp = []
follower_tweet_map = {}
for filename in followerfiles:
    followerdata_temp.append(read_and_parse(filename))
for follower in followerdata_temp:
    follower_tweet_map[follower[0]] = follower[1]
count = 0
for follower in follower_tweet_map:
    tweet_list = follower_tweet_map[follower]
    count +=1
    #print follower
    #print follower_tweet_map
    train_tweet_list = []
    test_tweet_list = []
    for tweet in tweet_list:
        tmstmp = tweet[0]
        twttxt = tweet[1]
        dt_tmstmp = dt.datetime.strptime(tmstmp, '%I:%M %p - %d %b %Y')
        if ((dt.datetime.now() - dt_tmstmp).total_seconds()/86400) <= 28.0:
            if ((dt.datetime.now() - dt_tmstmp).total_seconds()/86400) <= 7.0:
                test_tweet_list.append(twttxt)
            else:
                train_tweet_list.append(twttxt)
        else:
            continue
    follower_tweet_map[follower] = [train_tweet_list, test_tweet_list]

for follower in follower_tweet_map:
    print follower
    print 'Train set = ' + str(len(follower_tweet_map[follower][0]))
    print 'Test set = ' + str(len(follower_tweet_map[follower][1]))

[os.remove(f) for f in glob('*.jpg')]
