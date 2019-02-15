from Particle.requests_manager import RequestsManager
from Particle.session import Session
from Particle.actions import Actions
from Particle.Extractors import following

from .db_handler import get_account

from collections import OrderedDict

import random
import time
import os
import traceback
import threading


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="Twitter Username")
# parser.add_argument("-p", "--password", help="Twitter Password")
# parser.add_argument("-t", "--hashtag", help="Twitter Hashtag")

args = parser.parse_args()

class Unfollower(object):
    def __init__(self, account_obj):
        self.account_obj = account_obj
        os.system("title " + "Working on {} : {}".format(self.account_obj.username, self.account_obj.password))
        self.initialize()
        return None
    #
    def initialize(self):
        requests_manager = RequestsManager()
        self.session = Session(requests_manager, self.account_obj)
        self.following_extractor = following.Following(requests_manager)
        if self.session.login():
            self.actions = Actions(requests_manager, self.session.bearer_token)
        return None
    #
    def unfollow_following(self, min_position=None):
        following_data = self.following_extractor.get_following(self.account_obj.username, min_position)
        if following_data["following"]:
            min_position = following_data.get("min_position")
            print(str(following_data).encode())
            for user in following_data["following"]:
                user_id = user["user_id"]
                username = user["username"]
                if username == self.account_obj.username:
                    print("Skipping unfollowing, self user.")
                    continue
                user_id = user["user_id"]
                print("-------------------------------------------------------\n")
                if user["you_follow"]:
                    unfollow_resp = self.actions.unfollow(user_id)
                    if unfollow_resp:
                        if unfollow_resp.status_code == 200:
                            print("{} successfully unfollowed username: {} with user_id: {}".format(self.account_obj.username, username, user_id))
                            pause_time = random.choice(range(10, 15))
                            print("Pausing for {}s".format(pause_time))
                            time.sleep(pause_time)
                    else:
                        print("Failed to unfollow user: {}".format(username))
                        print("Stopping App")
                        return None
                else:
                    print("{} already unfollowing username: {} with user_id: {}".format(self.account_obj.username, username, user_id))
                #
        if min_position:
            print("Getting new users from following")
            return self.unfollow_following(min_position)
        print("All Done")
        return None


print(args)
tw_username = args.username
# tw_password = str(args.password)
# tw_hashtag = str(args.hashtag).lstrip("#")

print(tw_username)

account_obj = get_account(tw_username)
if account_obj:
    alpha = Unfollower(account_obj)
    while True:
        try:
            alpha.unfollow_following()
            break
        except Exception as e:
            print(e)
            traceback.print_exc()


