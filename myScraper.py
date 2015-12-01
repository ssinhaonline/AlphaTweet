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



def getTweets(usrNm, flag):
    """Collects the tweets of passed @username and returns a list of tweets"""
    usrUrl = 'https://twitter.com/' + usrNm.lower()
    src = sourceExtractor(usrUrl)
    soup = BeautifulSoup(src)
    tweetStream = soup.find('ol', {'id': 'stream-items-id'}).find_all('li', {'data-item-type': 'tweet'})
    #pdb.set_trace()
    tweetdivs = []
    for tweetTree in tweetStream:
        tweetdivs.append(tweetTree.find('div', {'class': 'tweet'}))
    tweetlist = []
    data = open(flag + '_' + usrNm + '.csv', 'w')

    for item in tweetdivs:
        try:
            content = item.find('div', {'class': 'content'}).find('p', {'class': 'tweet-text', 'lang': 'en'}).text.replace('\n', ' ').replace('"', '')
            if '\n' in content:
                newcontent = content.replace('\n', ' ')
                content = newcontent
            timestamp = item.find('a', {'class': 'tweet-timestamp'})['title']
            try:
                data.write(timestamp + '|' + content + '\n')
            except:
                pass
        except:
            pass
    data.close()
    print 'File wriiten: ' + data.name
    #return tweets

def sourceExtractor(url):
    """Get the source code of the passed url"""
    from selenium import webdriver
    from time import sleep
    driver = webdriver.Firefox()
    driver.get(url)
    lensrc1 = driver.execute_script("return document.body.scrollHeight")
    while(True):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        sleep(2)
        lensrc2 = driver.execute_script("return document.body.scrollHeight")
        if(lensrc2 == lensrc1):
            break
        lensrc1 = lensrc2
    src2 = driver.page_source
    driver.close()
    return src2

def id_to_username(ID): 
    import urllib2
    usock = urllib2.urlopen('http://twitter.com/intent/user?user_id=' + str(ID))
    src = usock.read()
    usock.close()
    soup = BeautifulSoup(src)
    return soup.find('span', {'class': 'nickname'}).text[1:]


usrNm = raw_input('Provide your username: @')
followers_ids = []
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
    followers_unames.append(str(id_to_username(ID)))
#print followers_unames
#print followers
import threading
for follower in followers_unames:
    try:
        getTweets(follower, 'f')
    except:
        print follower
        pass
