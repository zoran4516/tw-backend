from ..configuration import Configuration

import lxml.html
import json
from urllib.parse import quote


#####################################################################################
# Custom method to get first element or empty element by xpath
def xpath_first(self, elm_xpath):
    elements = self.xpath(elm_xpath)
    return next(iter(elements), lxml.html.HtmlElement())

def xpath_get_text(self, elm_xpath):
    # gets the first element and trims the text
    element = self.xpath_first(elm_xpath)
    return " ".join(element.text_content().split())

lxml.html.HtmlElement.xpath_first = xpath_first
lxml.html.HtmlElement.xpath_get_text = xpath_get_text

#####################################################################################

class Hashtags(object):
    def __init__(self, requests_manager):
        self.requests_manager = requests_manager
        self.initialize()
        return None
    #
    def initialize(self):
        self.home_url = Configuration.home_url
        self.get_hashtags_url = Configuration.get_hashtags_url
        return None
    #
    def parse_hashtags(self, tweets_json):
        tweets = {}
        tweets["tweets"] = []
        tweets_html = tweets_json['inner']['items_html']
        tweets_xml  = lxml.html.fromstring(tweets_html + "<p></p>")
        tweets_elms = tweets_xml.xpath('//div[contains(@class, "original-tweet")]')
        for tweet in tweets_elms:
            liked = False
            if "favorited" in tweet.attrib.get("class"):
                print("You have already liked this tweet")
                liked = True
            tweet_data = {
                "user_id" : tweet.attrib.get("data-user-id"),
                "username" : tweet.attrib.get("data-screen-name"),
                "tweet_id" : tweet.attrib.get("data-tweet-id"),
                "url" : tweet.attrib.get("data-permalink-path"),
                "name" : tweet.attrib.get("data-name"),
                "you_liked" : liked,
                "you_follow" : json.loads(tweet.attrib.get("data-you-follow")),
                "follows_you" : json.loads(tweet.attrib.get("data-follows-you")),
                "you_block" : json.loads(tweet.attrib.get("data-you-block")),
                # From Xpath
                # "verified_account" : tweet.xpath_first(),
                "text" : tweet.xpath_first('.//p[contains(@class, "tweet-text")]/text()'),
                "replies" : tweet.xpath_first('.//span[contains(@class,"ProfileTweet-action--reply")]//span/@data-tweet-stat-count'),
                "retweets" : tweet.xpath_first('.//span[contains(@class,"ProfileTweet-action--retweet")]//span/@data-tweet-stat-count'),
                "likes" : tweet.xpath_first('.//span[contains(@class,"ProfileTweet-action--favorite")]//span/@data-tweet-stat-count'),
                "timestamp_ms" : tweet.xpath_first('.//span[contains(@class, "_timestamp ")]/@data-time'),
            }
            tweets["tweets"].append(tweet_data)
        tweets["min_position"] = tweets_json['inner']["min_position"]
        return tweets    
    #
    def get_max_data_position(self, hashtag):
        url = "https://twitter.com/hashtag/{}?src=tren".format(hashtag)
        data_position_resp = self.requests_manager.make_request(url)
        data_position_xml = lxml.html.fromstring(data_position_resp.content)
        data_position_id = data_position_xml.xpath('//@data-max-position')
        if data_position_id:
            data_position_id = data_position_id[0]
            print("Max data position of hashtag {} is {}".format(hashtag, data_position_id))
            return quote(data_position_id)
        return ""
    #
    def prepare_data(self, hashtag):
        data = {}
        data["headers"] = {
                            "Accept": "application/json, text/javascript, */*; q=0.01",
                            "X-Twitter-Active-User": "yes",
                            "X-Requested-With": "XMLHttpRequest",
                            "Origin": None,
                            "Referer": "https://twitter.com/hashtag/{}?src=tren".format(hashtag),
                            }
        return data
    #
    def get_hashtags(self, hashtag, max_position=None):
        if not max_position:
            max_position = self.get_max_data_position(hashtag)
        data = self.prepare_data(hashtag)     
        url = self.get_hashtags_url.format(hashtag, max_position)
        # print(max_position)
        print(url)
        hashtags_resp = self.requests_manager.make_request(url, headers=data["headers"])
        print(hashtags_resp)
        # print(str(hashtags_resp.json()).encode())
        if hashtags_resp.status_code == 200:
            hashtags_json = hashtags_resp.json()
            hashtags = self.parse_hashtags(hashtags_json)
            return hashtags
        return []   

    
# alpha = Hashtags(rm)
# # w = alpha.get_max_data_position("CongressKeGunde")
# w = alpha.get_hashtags("CongressKeGunde")

