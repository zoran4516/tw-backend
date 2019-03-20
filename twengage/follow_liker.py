from Particle.requests_manager import RequestsManager
from Particle.session import Session
from Particle.actions import Actions
from Particle.Extractors import hashtags

from db_handler import get_account
from collections import OrderedDict

import random
import time
import os
import traceback

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="Twitter Username")
# parser.add_argument("-p", "--password", help="Twitter Password")
# parser.add_argument("-t", "--hashtag", help="Twitter Hashtag")

args = parser.parse_args()


# python follow_liker.py -u @GentillMayCry -p Endy0507 -t #soundcloud
# python follow_liker.py -u @LtStevenLRogers -p Beardog227 -t #MAGA
# python follow_liker.py -u @Xavgar2967 -p Home2!!! -t #gaysofinstagram
# python follow_liker.py -u @Russelltbrazil -p boston99 -t #realestate
# python follow_liker.py -u @luxpros -p anthony2012 -t #realestateagent
# python follow_liker.py -u @ExposeTheMedia -p 39ETM! -t #MAGA
# python follow_liker.py -u @H_weav96 -p Honeybee1996 -t #momlife
# python follow_liker.py -u @ApprovedThanks -p Kvonne93 -t #musicstudio
# python follow_liker.py -u @Bipolar_Jesus -p Pbowers0311 -t #twitch
# python follow_liker.py -u @moonshothost -p M00nsh0t -t #cryptocurrency 
# python follow_liker.py -u @iamfabrizio -p 10andoverLN -t #life 
# python follow_liker.py -u @argtumco -p argentum13 -t #streetwear 


class FollowLiker(object):
    def __init__(self, account_obj):
        self.account_obj = account_obj
        os.system("title " + "Working on {} : {}".format(self.account_obj.username, self.account_obj.password))
        self.initialize()
        return None
    #
    def initialize(self):
        requests_manager = RequestsManager()
        self.session = Session(requests_manager, self.account_obj)
        self.hashtags_extractor = hashtags.Hashtags(requests_manager)
        if self.session.login():
            self.actions = Actions(requests_manager, self.session.bearer_token)
        return None
    #
    def follow_like_tweets_hashtag(self, hashtag, min_position=None):
        tweets_data = self.hashtags_extractor.get_hashtags(hashtag, min_position)
        if tweets_data["tweets"]:
            if tweets_data:
                min_position = tweets_data.get("min_position")
                # tweets_to_like = OrderedDict((follower["user_id"], tweet["username"]) for tweet in tweets_data["tweets"] if not tweet["you_follow"])
                # users_to_follow = OrderedDict((follower["user_id"], tweet["username"]) for tweet in tweets_data["tweets"] if not tweet["you_follow"])
                print(str(tweets_data).encode())
                for tweet in tweets_data["tweets"]:
                    user_id = tweet["user_id"]
                    username = tweet["username"]
                    if username == self.account_obj.username:
                        print("Skipping liking/following my tweet.")
                        continue
                    tweet_id = tweet["tweet_id"]
                    tweet_likes = tweet["likes"]
                    print("-------------------------------------------------------\n")
                    if self.account_obj.follow:
                        if not tweet["you_follow"]:
                            follow_resp = self.actions.follow(user_id)
                            if follow_resp:
                                if follow_resp.status_code == 200:
                                    print("Successfully followed username: {} with user_id: {}".format(username, user_id))
                                    pause_time = random.choice(range(10, 20))
                                    print("Pausing for {}s".format(pause_time))
                                    time.sleep(pause_time)
                            else:
                                print("Failed to follow tweet's user: {}".format(user_id))
                                print("Stopping App")
                                return None
                        else:
                            print("Already following username: {} with user_id: {}".format(username, user_id))
                    else:
                        print("{} does not want to follow people".format(self.account_obj.username))
                    #
                    if self.account_obj.like:
                        if not tweet["you_liked"]:
                            like_resp = self.actions.like(tweet_id, tweet_likes)
                            if like_resp:
                                if like_resp.status_code == 200:
                                    print("Successfully liked tweet: {}".format(tweet_id))
                                    pause_time = random.choice(range(10, 20))
                                    print("Pausing for {}s".format(pause_time))
                                    time.sleep(pause_time)
                            else:
                                print("Failed to like tweet: {}".format(tweet_id))
                                print("Stopping App")
                                return None
                        else:
                            print("Already liked  tweet: {} with likes: {}".format(tweet_id, tweet_likes))
                    else:
                        print("{} does not want to like tweets".format(self.account_obj.username))
                    print("\n-------------------------------------------------------")
            if min_position:
                print("Getting new tweets from hashtags")
                return self.follow_like_tweets_hashtag(hashtag, min_position)
        print("All Done")
        return None



print(args)
tw_username = args.username
# tw_password = str(args.password)
# tw_hashtag = str(args.hashtag).lstrip("#")

print(tw_username)

account_obj = get_account(tw_username)
if account_obj:
    alpha = FollowLiker(account_obj)
    tags = account_obj.hashtags.split(" ")
    random.shuffle(tags)
    for each_tag in tags:
        while True:
            try:
                # alpha.follow_like_tweets_hashtag(account_obj.current_hashtag.lstrip("#"))
                print("Current Hashtag: {}".format(each_tag))
                alpha.follow_like_tweets_hashtag(each_tag.lstrip("#"))
                break
            except Exception as e:
                print(e)
                traceback.print_exc()