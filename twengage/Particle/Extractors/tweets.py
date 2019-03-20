from ..configuration import Configuration

import lxml.html
import json

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

class Tweets(object):
    def __init__(self, requests_manager):
        self.requests_manager = requests_manager
        self.initialize()
        return None
    #
    def initialize(self):
        self.home_url = Configuration.home_url
        self.get_tweets_url = Configuration.get_tweets_url
        return None
    #
    def parse_tweets(self, tweets_json):
        tweets = []
        tweets_html = tweets_json.get("items_html")
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
                "timestamp_ms" : tweet.xpath_first('.//span[contains(@class, "_timestamp ")]/@data-time-ms'),
            }
            tweets.append(tweet_data)
        return tweets
    #
    def get_latest_tweet_id(self, username):
        last_tweet_resp = self.requests_manager.make_request(self.home_url + "/" + str(username))
        last_tweet_xml = lxml.html.fromstring(last_tweet_resp.content)
        last_tweet_id = last_tweet_xml.xpath_first('//div[contains(@class, "original-tweet")]/@data-tweet-id')
        print("Latest Tweet id of {} is {}".format(username, last_tweet_id))
        return last_tweet_id
    #
    def prepare_data(self, username):
        data = {}
        data["headers"] = {
                            "X-Twitter-Active-User": "yes",
                            "Referer": "https://twitter.com/{}".format(username),
                            }
        return data
    #
    def get_tweets(self, username, last_tweet_id=None):
        if not last_tweet_id:
            last_tweet_id = self.get_latest_tweet_id(username)
        data = self.prepare_data(username)     
        url = self.get_tweets_url.format(username, last_tweet_id)
        tweets_resp = self.requests_manager.make_request(url, headers=data["headers"])
        if tweets_resp.status_code == 200:
            tweets_json = tweets_resp.json()
            tweets = self.parse_tweets(tweets_json)
            return tweets
        return []



# tw = Tweets(rm)
# y = tw.get_tweets("iamsrk")

# import json
# print(json.dumps(tweets, sort_keys=True, indent=4))


