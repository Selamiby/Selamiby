import tweepy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import defaultdict
import json
import time

class TrendingTopicExtractor:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(self.auth)

    def get_trending_topics(self):
        trends = self.api.trends_place(1)  # 1 is the WOEID for worldwide
        trending_topics = []
        for trend in trends[0]['trends']:
            trending_topics.append(trend['name'])
        return trending_topics

    def get_related_tweets(self, topic):
        tweets = tweepy.Cursor(self.api.search_tweets, q=topic, lang='en').items(100)
        related_tweets = []
        for tweet in tweets:
            related_tweets.append(tweet.text)
        return related_tweets

    def extract_keywords(self, tweets):
        stop_words = set(stopwords.words('english'))
        keywords = defaultdict(int)
        for tweet in tweets:
            words = word_tokenize(tweet)
            for word in words:
                if word.lower() not in stop_words:
                    keywords[word] += 1
        return keywords

def main():
    consumer_key = 'your_consumer_key'
    consumer_secret = 'your_consumer_secret'
    access_token = 'your_access_token'
    access_token_secret = 'your_access_token_secret'

    extractor = TrendingTopicExtractor(consumer_key, consumer_secret, access_token, access_token_secret)
    trending_topics = extractor.get_trending_topics()
    for topic in trending_topics:
        related_tweets = extractor.get_related_tweets(topic)
        keywords = extractor.extract_keywords(related_tweets)
        print(f'Topic: {topic}')
        print(f'Keywords: {keywords}')
        print('')

if __name__ == '__main__':
    main()

# NEXUS-ONE CORE MODULE