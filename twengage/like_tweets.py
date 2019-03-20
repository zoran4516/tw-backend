from Particle.requests_manager import RequestsManager
from Particle.session import Session
from Particle.actions import Actions
from Particle.Extractors import tweets

from collections import OrderedDict

import random
import time


class LikeTweets(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.initialize()
        return None
    #
    def initialize(self):
        requests_manager = RequestsManager()
        self.session = Session(requests_manager, self.username, self.password)
        self.tweets_extractor = tweets.Tweets(requests_manager)
        if self.session.login():
            self.actions = Actions(requests_manager, self.session.bearer_token)
        return None
    #
    def like_tweets_of_username(self, username, last_tweet_id=None):
        tweets_data = self.tweets_extractor.get_tweets(username, last_tweet_id)
        if tweets_data:
            last_tweet_id = tweets_data[-1].get("tweet_id")
            # id_and_likes = {tweet["tweet_id"] : tweet["likes"] for tweet in tweets_data if not tweet["you_liked"]}
            id_and_likes = OrderedDict((tweet["tweet_id"], tweet["likes"]) for tweet in tweets_data if not tweet["you_liked"])
            print(id_and_likes)
            print(len(id_and_likes))
            for tweet_id, tweet_likes in id_and_likes.items():
                print("-------------------------------------------------------\n")
                like_resp = self.actions.like(tweet_id, tweet_likes)
                if like_resp:
                    if like_resp.status_code == 200:
                        print("Successfully liked tweet: {}".format(tweet_id))
                        pause_time = random.choice(range(10,15))
                        print("Pausing for {}s".format(pause_time))
                        time.sleep(2)
                else:
                    print("Failed to like tweet: {}".format(tweet_id))
                    print("Stopping App")
                    break
                print("\n-------------------------------------------------------")
        if last_tweet_id:
            print("Getting new tweets")
            return self.like_tweets_of_username(username, last_tweet_id)
        print("All Done")
        return None



# alpha = LikeTweets("unfollowpro@gmail.com", "123321aa")
alpha = LikeTweets("likesstack", "123321aa")
alpha.like_tweets_of_username("TEDTalks")

# Xpath to Check tweets order in browser
# //div[contains(@class, "original-tweet") and @data-tweet-id="1012307188596006912"]