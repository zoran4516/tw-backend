from Particle.requests_manager import RequestsManager
from Particle.session import Session
from Particle.actions import Actions
from Particle.Extractors import following

from db_handler import get_account
from db_handler import save_followings

from collections import OrderedDict



import random
import time
import os
import traceback
import threading


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="Twitter Username")

parser.add_argument("-m", "--mode", help="Running Mode")
#Running Mode
#       0 : Normal
#       1 : Store followings to DB

# parser.add_argument("-p", "--password", help="Twitter Password")
# parser.add_argument("-t", "--hashtag", help="Twitter Hashtag")

args = parser.parse_args()

class Unfollower(object):
    def __init__(self, account_obj):
        self.account_obj = account_obj
        self.following_store = []
        self.count = 0
        os.system("title " + "Working on {} : {}".format(self.account_obj.username, self.account_obj.password))
        self.initialize()
        return None
    #
    def initialize(self):
        requests_manager = RequestsManager()
        self.session = Session(requests_manager, self.account_obj)
        #print to find the bug
        self.following_extractor = following.Following(requests_manager)
        #print("{}" .format(self.following_extractor))
        if self.session.login():
            self.actions = Actions(requests_manager, self.session.bearer_token)
        return None
    #

    def unfollow_following(self, minPositionInput=None, mode=0, funcMode=0):

        following_data = self.following_extractor.get_following(account_obj.username, minPositionInput, mode)
        if following_data == [] :
            print("Get No Data")
            exit(0)

        min_position = following_data.get("min_position")

        if len(following_data["following"]) == 0:
            print("All Done", self.count)
            self.count = 0
            return None

        for user in following_data["following"]:
            user_id = user["user_id"]
            username = user["username"]
            if username == self.account_obj.username:
                print("Skipping unfollowing, self user.")
                continue
            if funcMode == 1:
                self.following_store.append(username)
                self.count += 1
            else:
                if user["you_follow"] == True and account_obj.org_following_users.find(username) == -1 and account_obj.follower_users.find(username) == -1 :
                    print("unfollow start")
                    unfollow_resp = self.actions.unfollow(user_id)

                    if unfollow_resp:
                        if unfollow_resp.status_code == 200:
                            self.count += 1
                            print("{} successfully unfollowed username: {} with user_id: {}".format(self.account_obj.username, username, user_id))
                            pause_time = random.choice(range(10, 20))
                            print("Pausing for {}s".format(pause_time))
                            time.sleep(pause_time)
                    else:
                        print("Failed to unfollow user: {}".format(username))
                        print("Stopping App")
                        self.count = 0
                        return None
                else:
                    print("{} already unfollowing username: {} with user_id: {} or unfollowing condition not matched".format(self.account_obj.username, username, user_id))
                #
        print(self.following_store)
        pause_time = random.choice(range(2, 4))
        time.sleep(pause_time)
        save_followings(tw_username, self.following_store)
        return self.unfollow_following(min_position, 1, funcMode)


#print(args)
tw_username = args.username
tw_mode = args.mode
# tw_password = str(args.password)
# tw_hashtag = str(args.hashtag).lstrip("#")
account_obj = get_account(tw_username)

if account_obj:
    alpha = Unfollower(account_obj)

    if tw_mode == "0":
        print("unfollow mode")
        alpha.unfollow_following()
    else:
        print("get following mode")
        alpha.unfollow_following(None, 0, 1)
        print(alpha.following_store)
        print(len(alpha.following_store))
        save_followings(tw_username, alpha.following_store)
    # while True:
    #     try:
    #         if tw_mode == 0:
    #             alpha.unfollow_following()
    #             break
    #         else:
    #             alpha.unfollow_following(None, 0, 1)
    #             print(alpha.following_store)
    #             print(len(alpha.following_store))
    #             #save_followings(tw_username, alpha.followers_store)
    #             break
    #     except Exception as e:
    #         print(e)
    #         traceback.print_exc()


