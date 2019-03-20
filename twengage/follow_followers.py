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
from db_handler import save_followers

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="Twitter Username")
# parser.add_argument("-p", "--password", help="Twitter Password")
# parser.add_argument("-t", "--hashtag", help="Twitter Hashtag")


parser.add_argument("-m", "--mode", help="Running Mode")
#Running Mode
#       0 : Normal
#       1 : Store followers to DB


args = parser.parse_args()
class FollowFollowers(object):
    def __init__(self, account_obj):
        self.account_obj = account_obj

        #states variables
        self.count = 0
        self.isStopped = False

        os.system("title " + "Working on {} : {}".format(self.account_obj.username, self.account_obj.password))
        self.initialize()
        return None
    #
    def initialize(self):
        requests_manager = RequestsManager()
        self.session = Session(requests_manager, self.account_obj)
        self.followers_extractor = followers.Followers(requests_manager)
        self.followers_store = []
        if self.session.login():
            self.actions = Actions(requests_manager, self.session.bearer_token)
        return None
    #
    def follow_followers_of_username(self, userNameInput, minPositionInput=None, mode=0, funcMode=0):
        followers_data = self.followers_extractor.get_followers(userNameInput, minPositionInput, mode)
        if followers_data == [] :
            print("Get No Data")
            exit(0)
        min_position = 0
        #if followers_data:
        if mode == 1:
        	min_position = followers_data.get("min_position")
        print("min_position in follow_followers.py", min_position)
        

        followers = OrderedDict((follower["user_id"], (follower["username"], follower["you_follow"])) for follower in followers_data["followers"])# if not follower["you_follow"])
        print(followers)
        if len(followers) == 0:
            print("All Done", self.count)
            self.count = 0
            return None
        for user_id, (username, isFollow) in followers.items():
            # user_id = follower["user_id"]
            # username = follower["username"]
            if funcMode == 1:
                self.followers_store.append(username)
            else:
                if isFollow == False:
                    print("-------------------------------------------------------\n")
                    follow_resp = self.actions.follow(user_id)
                    if follow_resp:
                        if follow_resp.status_code == 200:
                            print("Successfully followed username: {} with user_id: {}".format(username, user_id))
                            pause_time = random.choice(range(10,20))
                            print("Pausing for {}s".format(pause_time))
                            self.count += 1
                            time.sleep(pause_time)
                    else:
                        print("Failed to follow tweet: {}".format(user_id))
                        print("Stopping App")
                        self.isStopped = True
                        break
                    print("\n-------------------------------------------------------")
        #if min_position:
        #print("Getting new tweets", min_position)
        if self.isStopped == True :
            self.count = 0
            self.isStopped = False
            return None
        return self.follow_followers_of_username(userNameInput, min_position, 1, funcMode)
        print("All Done")
        return None




print(args)
tw_username = args.username
tw_mode = args.mode
# tw_password = str(args.password)
# tw_hashtag = str(args.hashtag).lstrip("#")

print(tw_username)

account_obj = get_account(tw_username)
if account_obj:
    alpha = FollowFollowers(account_obj)

    if account_obj.follow_accounts.strip(' \t\n\r') == "":
        print("No accounts to follow")
        exit(0)
    if tw_mode == "0":
        users = account_obj.follow_accounts.split(" ")
        print(users)
        random.shuffle(users)
        for each_user in users:
            try:
                # alpha.follow_like_tweets_hashtag(account_obj.current_hashtag.lstrip("#"))
                print("Current User: {}".format(each_user))
                alpha.follow_followers_of_username(each_user.replace(',','').replace(' ','').lstrip("@"))
                break
            except Exception as e:
                print(e)
                traceback.print_exc()
    else:
        print("mode1")
        alpha.follow_followers_of_username(tw_username.lstrip("@"), None, 0, 1)
        print("Current User: ",tw_username)
        print(alpha.followers_store)
        print(len(alpha.followers_store))
        save_followers(tw_username, alpha.followers_store)


# alpha = FollowFollowers("unfollowpro@gmail.com", "123321aa")
# alpha = FollowFollowers("constant_likes", "123321aa")
# alpha.follow_followers_of_username("SrBachchan")

# Xpath to Check tweets order in browser
# //div[contains(@class, "original-tweet") and @data-tweet-id="1012307188596006912"]