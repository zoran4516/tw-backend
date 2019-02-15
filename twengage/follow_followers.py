from Particle.requests_manager import RequestsManager
from Particle.session import Session
from Particle.actions import Actions
from Particle.Extractors import followers
# from Particle.configuration import Configuration

from collections import OrderedDict

import random
import time
import argparse
import os
import traceback
from db_handler import get_account

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="Twitter Username")
# parser.add_argument("-p", "--password", help="Twitter Password")
# parser.add_argument("-t", "--hashtag", help="Twitter Hashtag")

args = parser.parse_args()



class FollowFollowers(object):
    def __init__(self, account_obj):
        self.account_obj = account_obj
        os.system("title " + "Working on {} : {}".format(self.account_obj.username, self.account_obj.password))
        self.initialize()
        return None
    #
    def initialize(self):
        requests_manager = RequestsManager()
        self.session = Session(requests_manager, self.account_obj)
        self.followers_extractor = followers.Followers(requests_manager)
        if self.session.login():
            self.actions = Actions(requests_manager, self.session.bearer_token)
        return None
    #
    def follow_followers_of_username(self, username, min_position=None):
        followers_data = self.followers_extractor.get_followers(username, min_position)
        if followers_data:
            min_position = followers_data.get("min_position")
            followers = OrderedDict((follower["user_id"], follower["username"]) for follower in followers_data["followers"] if not follower["you_follow"])
            print(followers)
            for user_id, username in followers.items():
                # user_id = follower["user_id"]
                # username = follower["username"]
                print("-------------------------------------------------------\n")
                follow_resp = self.actions.follow(user_id)
                if follow_resp:
                    if follow_resp.status_code == 200:
                        print("Successfully followed username: {} with user_id: {}".format(username, user_id))
                        pause_time = random.choice(range(10,15))
                        print("Pausing for {}s".format(pause_time))
                        time.sleep(pause_time)
                else:
                    print("Failed to follow tweet: {}".format(user_id))
                    print("Stopping App")
                    break
                print("\n-------------------------------------------------------")
        if min_position:
            print("Getting new tweets")
            return self.follow_followers_of_username(username, min_position)
        print("All Done")
        return None




print(args)
tw_username = args.username
# tw_password = str(args.password)
# tw_hashtag = str(args.hashtag).lstrip("#")

print(tw_username)

account_obj = get_account(tw_username)
if account_obj:
    alpha = FollowFollowers(account_obj)
    users = account_obj.follow_accounts.split(" ")
    print(users)
    random.shuffle(users)
    for each_user in users:
        try:
            # alpha.follow_like_tweets_hashtag(account_obj.current_hashtag.lstrip("#"))
            print("Current User: {}".format(each_user))
            alpha.follow_followers_of_username(each_user.lstrip("@"))
            break
        except Exception as e:
            print(e)
            traceback.print_exc()


# alpha = FollowFollowers("unfollowpro@gmail.com", "123321aa")
# alpha = FollowFollowers("constant_likes", "123321aa")
# alpha.follow_followers_of_username("SrBachchan")

# Xpath to Check tweets order in browser
# //div[contains(@class, "original-tweet") and @data-tweet-id="1012307188596006912"]