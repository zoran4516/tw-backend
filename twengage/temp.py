import csv
import datetime
import lxml.html
import os
import requests
import random
import time

from db_handler import Account, get_stats_by_account_date, all_accounts

#####################################################################################
# Custom method to get first element or empty element by xpath
def xpath_first(self, elm_xpath):
    elements = self.xpath(elm_xpath)
    return next(iter(elements), 0)

lxml.html.HtmlElement.xpath_first = xpath_first
#####################################################################################

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3197.0 Safari/537.36"
}

def get_stats(username):
    print("Getting stats of user {}".format(username))
    url = "https://twitter.com/{}".format(username)
    while True:
        try:
            resp = requests.get(url, headers=headers, timeout=5)
            break
        except:
            print("Error occured while getting stats")
            time.sleep(2)
    xml = lxml.html.fromstring(resp.content)

    followers = xml.xpath_first('//a[@data-nav="followers"]//span/@data-count')
    followings = xml.xpath_first('//a[@data-nav="following"]//span/@data-count')
    likes = xml.xpath_first('//a[@data-nav="favorites"]//span/@data-count')
    tweets = xml.xpath_first('//a[@data-nav="tweets"]//span/@data-count')
    stats = "{}, {}, {}, {}".format(followers, followings, likes, tweets)
    print("Stats of {} are {}".format(username, stats))
    return [followers, followings, likes, tweets]


accounts = Account.objects.all()

for each_acc in accounts:
    account_stats = get_stats(each_acc.username)
    followers, followings, likes, tweets = account_stats
    current_date = datetime.datetime.now().strftime ("%m-%d-%Y")
    print("Current Date: {}".format(current_date))
    stat_obj =  get_stats_by_account_date(each_acc, current_date)
    if any(account_stats):
        stat_obj.followers = followers
        stat_obj.followings = followings
        stat_obj.likes = likes
        stat_obj.tweets = tweets
    else:
        print("Skipping {} cause stats are all 0, account might be temporarily disabled.".format(each_acc.username))
    stat_obj.save()

input("Press enter to start engagement of active accounts")

# for each_acc in db_handler.active_accounts():
for each_acc in all_accounts():
    pause_time = random.choice(range(1,5))
    time.sleep(pause_time)
    os.system('start cmd /K "TITLE {0} & resize_cmd 80 25 80 9999 & python follow_liker.py -u{0}"'.format(each_acc.username))
    # os.system('start cmd /K "TITLE {0} & resize_cmd 80 25 80 9999 & python follow_followers.py -u{0}"'.format(each_acc.username))

# with open("accounts.txt", "rb") as rr:
#     a = rr.read()

# data = a.decode('ascii', 'ignore').rstrip('\r\n').lstrip('\r\n').split("\r\n")
# for i in data :
#     m = i.split("\t")
#     username = m[0]
#     password = m[1]
#     tags = "#" + " #".join(m[2].replace("," , " ").replace('"', '').replace('#', '').split())
#     accs = "@" + " @".join(m[3].replace("," , " ").replace('"', '').replace('@', '').split())
#     acc_obj = Account()
#     acc_obj.username = username
#     acc_obj.password = password
#     acc_obj.hashtags = tags
#     acc_obj.follow_accounts = accs
#     acc_obj.save()

