"""
This module uses BeautifulSoup 4 and Requests package to scrape Twitter for data, and can be used to bypass the REST API request ceiling set by Twitter

@author ssinhaonline <homepage = "www.datanoobjournals.com/ssinhaonline" email = "ssinhaonline@gmail.com">
@date Nov 6, 2015
"""

import re
from bs4 import BeautifulSoup
import webbrowser
import pdb
import tweepy
import os
import datetime as dt
from nltk.corpus import stopwords


def getTweets(usrNm, flag):
    """Collects the tweets of passed @username and returns a list of tweets"""
    usrUrl = 'https://twitter.com/' + usrNm.lower()
    src = sourceExtractor(usrUrl)
    soup = BeautifulSoup(src, 'html.parser')
    tweetStream = soup.find('ol', {'id': 'stream-items-id'}).find_all('li', {'data-item-type': 'tweet'})
    if len(tweetStream) < 1:
        pass
    else:
        tweetdivs = []
        for tweetTree in tweetStream:
            tweetdivs.append(tweetTree.find('div', {'class': 'tweet'}))
        tweetlist = []
        anothertemplist = []
        #pdb.set_trace()
        for item in tweetdivs:
            try:
                context = item.find('div', {'class': 'context'}).text
                if flag == 'u':
                    #if user, collect only tweets
                    if 'Retweeted' in context:
                        continue
                    else:
                        content = item.find('div', {'class': 'content'}).find('p', {'class': 'tweet-text', 'lang': 'en'}).text.replace('\n', ' ').replace('"', '')
                        words = re.findall("[-'#@\w]+", content)
                        cachedStops = stopwords.words("english")
                        content = ' '.join([word for word in words if word not in cachedStops])
                        timestamp = item.find('a', {'class': 'tweet-timestamp'})['title']
                        footer = item.find('div', {'class': 'stream-item-footer'})
                        retweet = footer.find('div', {'class': 'ProfileTweet-action--retweet'}).find('div', {'class': 'IconTextContainer'}).find('span', {'class': 'ProfileTweet-actionCountForPresentation'}).text
                        if retweet == '':
                            retweet = '0'
                        favorite = footer.find('div', {'class': 'ProfileTweet-action--favorite'}).find('div', {'class': 'IconTextContainer'}).find('span', {'class': 'ProfileTweet-actionCountForPresentation'}).text
                        if favorite == '':
                            favorite = '0'
                        tweet_tmstmp = dt.datetime.strptime(timestamp, '%I:%M %p - %d %b %Y')
                        if ((dt.datetime.now() - tweet_tmstmp).total_seconds()/86400.0 > 28.0):
                            continue
                        else:
                            anothertemplist.append([timestamp, content, retweet, favorite])
                else:
                    #if followers, collect only retweets
                    if 'Retweeted' in context:
                        content = item.find('div', {'class': 'content'}).find('p', {'class': 'tweet-text', 'lang': 'en'}).text.replace('\n', ' ').replace('"', '')
                        words = re.findall("[-'#@\w]+", content)
                        cachedStops = stopwords.words("english")
                        content = ' '.join([word for word in words if word not in cachedStops])
                        timestamp = item.find('a', {'class': 'tweet-timestamp'})['title']
                        footer = item.find('div', {'class': 'stream-item-footer'})
                        retweet = footer.find('div', {'class': 'ProfileTweet-action--retweet'}).find('div', {'class': 'IconTextContainer'}).find('span', {'class': 'ProfileTweet-actionCountForPresentation'}).text
                        if retweet == '':
                            retweet = '0'
                        favorite = footer.find('div', {'class': 'ProfileTweet-action--favorite'}).find('div', {'class': 'IconTextContainer'}).find('span', {'class': 'ProfileTweet-actionCountForPresentation'}).text
                        if favorite == '':
                            favorite = '0'
                        tweet_tmstmp = dt.datetime.strptime(timestamp, '%I:%M %p - %d %b %Y')
                        if ((dt.datetime.now() - tweet_tmstmp).total_seconds()/86400.0 > 28.0):
                            continue
                        else:
                            anothertemplist.append([timestamp, content, retweet, favorite])
                    else:
                        continue
            except:
                pass
        if len(anothertemplist) != 0:
            data = open(flag + '_' + usrNm + '.csv', 'w')
            for row in anothertemplist:
                timestamp, content, retweet, favorite = row
                try:
                    data.write(timestamp + '|' + content + '|' + retweet + '|' + favorite + '\n')
                except:
                    pass
            data.close()
            print 'File written: ' + data.name
        #return tweets

def sourceExtractor(url):
    """Get the source code of the passed url"""
    from selenium import webdriver
    from time import sleep
    driver = webdriver.Firefox()
    driver.get(url)
    lensrc1 = driver.execute_script("return document.body.scrollHeight")
    #pdb.set_trace()
    while(True):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        sleep(2)
        lensrc2 = driver.execute_script("return document.body.scrollHeight")
        
        if (lensrc2 == lensrc1):
            break
        else:
            try:
                page_last_timestamp = BeautifulSoup(driver.page_source, 'html.parser').find('ol', {'id': 'stream-items-id'}).find_all('li', {'data-item-type': 'tweet'})[-1].find('div', {'class': 'tweet'}).find('a', {'class': 'tweet-timestamp'})['title']
                pg_last_tmstmp = dt.datetime.strptime(page_last_timestamp, '%I:%M %p - %d %b %Y')
                if ((dt.datetime.now() - pg_last_tmstmp).total_seconds()/86400) >= 28.0:
                    break
                else:
                    pass
            except:
                pass
        lensrc1 = lensrc2
    src2 = driver.page_source
    driver.close()
    return src2

def id_to_username(ID): 
    import urllib2
    usock = urllib2.urlopen('http://twitter.com/intent/user?user_id=' + str(ID))
    src = usock.read()
    usock.close()
    soup = BeautifulSoup(src, 'html.parser')
    return soup.find('span', {'class': 'nickname'}).text[1:]


usrNm = raw_input('Provide your username: @')
followers_ids = []
os.mkdir(usrNm)
os.chdir('./' + usrNm)
getTweets(usrNm, 'u')
consumer_key = "uyLBbpnlVe5KiBy9oU1Zz5C2F" 
consumer_secret = "S9qN3td9JbCaM6SMEHDjjZlu8FOeyWucGHOye2RhtJdO4YEeNx"
access_token = "40179822-lzdJzzaaPTes19EV8co6zsQNOrjUmy2ONK1SGnBHj"
access_token_secret = "auq6rLf0Wxbm0ulkMNJvlGpC7FsjQEYNJcbCIdkgbgGjV"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
tweepyUsr = api.get_user(usrNm)

followers_ids = api.followers_ids(usrNm)
followers_unames = [] 
for ID in followers_ids:
    try:
        followers_unames.append(str(id_to_username(ID)))
    except:
        pass
#print followers_unames
#print followers
for follower in followers_unames:
    try:
        getTweets(follower, 'f')
    except:
        pass
os.chdir('../')
infodata = open(usrNm + '.info', 'w')
infodata.write(usrNm)
infodata.close()

