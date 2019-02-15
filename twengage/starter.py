import csv
import datetime
import lxml.html
import os
import requests



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

# updated_accs = []

def get_stats(username):
    print("Getting stats of user {}".format(username))
    url = "https://twitter.com/{}".format(username)
    resp = requests.get(url, headers=headers)
    xml = lxml.html.fromstring(resp.content)
    current_date = datetime.datetime.now().strftime ("%m-%d-%Y")
    followers = xml.xpath_first('//a[@data-nav="followers"]//span/@data-count')
    followings = xml.xpath_first('//a[@data-nav="following"]//span/@data-count')
    likes = xml.xpath_first('//a[@data-nav="favorites"]//span/@data-count')
    stats = "{}: {}, {}, {}".format(current_date, followers, followings, likes)
    print("Stats of {} are {}".format(username, stats))
    return stats

# with open("accounts.csv", "r", encoding="utf-8") as read_file:
#     accounts = [acc.split("\t") for acc in read_file.read().rstrip("\n").lstrip("\n").split("\n")]



for each_acc in accounts:
    username = each_acc[0]
    password = each_acc[1]
    stats = get_stats(username)
    each_acc.append(stats)
    updated_accs.append(each_acc)


# with open("accounts1.csv", "w", encoding="utf-8", newline="") as write_file:
#     writer = csv.writer(write_file)
#     for acc in updated_accs:
#         writer.writerow(acc)






k = get_stats("unfollowpro1")

