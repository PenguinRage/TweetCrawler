import iso8601 as iso8601
from bs4 import BeautifulSoup
import requests
from time import sleep
from dateutil.parser import *
import sys
import flask
from flask import jsonify
from flask import request
import threading
import logging
import datetime
import pytz

tz = pytz.UTC


class Tweet:

    def __init__(self, text, timestamp):
        self.text = str(text).rstrip()
        self.timestamp = timestamp

    def print_tweet(self):
        print(self.text)

    def serialize(self):
        return {
            'tweet': self.text,
            'timestamp': self.timestamp
        }


class tweetCrawler:

    def __init__(self, handle):
        self.handle = handle
        self.tweets = self.get_tweets()[:5]

    def monitor(self):
        while True:
            # Wait 10 secs
            sleep(300)
            tweets_list = self.get_tweets()
            last_tweet = self.tweets[0]

            new_tweets = []

            for tweet in tweets_list:
                if last_tweet.timestamp == tweet.timestamp:
                    break
                else:
                    new_tweets.append(tweet)

            self.print_tweets(new_tweets)
            self.tweets = new_tweets + self.tweets

    def get_tweets(self):
        url = 'https://syndication.twitter.com/timeline/profile?screen_name=' + self.handle
        r = requests.get(url)
        bs = BeautifulSoup(r.json()['body'], 'html.parser')
        tl = bs.find_all('p', {'class': 'timeline-Tweet-text'})
        timestamps = bs.find_all('time', {'class': 'dt-updated'})
        tweet_list = []
        for count, item in enumerate(tl):
            tweet_list.append(Tweet(item.get_text(), iso8601.parse_date(timestamps[count]['datetime'])))

        return tweet_list

    @staticmethod
    def print_tweets(tweet_list):
        for tweet in reversed(tweet_list):
            tweet.print_tweet()

    def print_intro(self):
        print("_____________________________________________________________________")
        print("""
     _____                _    ___                 _         
    |_   _|_ __ _____ ___| |_ / __|_ _ __ ___ __ _| |___ _ _ 
      | | \ V  V / -_) -_)  _| (__| '_/ _` \ V  V / / -_) '_|
      |_|  \_/\_/\___\___|\__|\___|_| \__,_|\_/\_/|_\___|_|  
      Usage: ./tweetcrawler (username)
      Api can be found on 0.0.0.0/5000""")

        print("_____________________________________________________________________")
        self.print_tweets(self.tweets)

    @staticmethod
    def get_date_from_string(s):
        d = parse(s)
        return d

    def get_tweets_after_date(self, ts):
        return [tweet for tweet in self.tweets if tweet.timestamp >= pytz.utc.localize(ts)]


class processThread:

    def __init__(self, bot):
        p = threading.Thread(target=self.run, args=(bot,))
        p.daemon = True
        p.start()

    @staticmethod
    def run(bot):
        sleep(0.5)
        bot.print_intro()
        bot.monitor()


tweetCrawler = tweetCrawler(sys.argv[1])

# Flask API Setup
app = flask.Flask(__name__)
# Disable logging so not to spam  Console log
log = logging.getLogger('werkzeug')
log.disabled = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Tweet Crawler API</h1><p>This is Tweet Crawler API, tweets can be found in /tweets.</p>"


@app.route('/tweets', methods=['GET'])
def tweets():
    timestamp = request.args.get('timestamp')

    if timestamp is None:
        return jsonify(tweets=[tweet.serialize() for tweet in tweetCrawler.tweets])
    else:
        ts = datetime.datetime.strptime(timestamp, '%a, %d %b %Y %H:%M:%S GMT')
        return jsonify(tweets=[tweet.serialize() for tweet in tweetCrawler.get_tweets_after_date(ts)])


if __name__ == "__main__":
    processThread(tweetCrawler)
    app.run(host='0.0.0.0', threaded=True)
