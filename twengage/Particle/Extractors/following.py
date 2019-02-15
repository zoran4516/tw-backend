from ..configuration import Configuration

import lxml.html

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

class Following(object):
    def __init__(self, requests_manager):
        self.requests_manager = requests_manager
        self.initialize()
        return None
    #
    def initialize(self):
        self.home_url = Configuration.home_url
        self.get_following_url = Configuration.get_following_url
        return None
    #
    def parse_following(self, following_json):
        following = {}
        following["following"] = []
        following_html = following_json.get("items_html")
        following_xml  = lxml.html.fromstring(following_html  + "<p></p>")
        following_elms = following_xml.xpath('//div[contains(@class, "ProfileCard") and @data-user-id]')
        following["min_position"] = following_json["min_position"]
        for follower in following_elms:
            you_follow = True
            if follower.xpath('.//div[contains(@class, "not-following")]'):
                you_follow = False
            else:
                print("Already following this user")
            following["following"].append({
                "user_id" : follower.attrib.get("data-user-id"),
                "username" : follower.attrib.get("data-screen-name"),
                "you_follow" : you_follow,
            })
        return following    
    #
    def get_min_position(self, username):
        headers = {
                    "X-Push-State-Request": "true",
                    # "X-Twitter-Active-User": "yes",
                    "Referer": "https://twitter.com/{}".format(username),
                    }
        url = self.home_url + "/" + str(username) + "/following"
        min_position_resp = self.requests_manager.make_request(url, headers=headers)
        print(min_position_resp)
        print(min_position_resp.url)
        import pprint
        pprint.pprint(dict(min_position_resp.request.headers))
        min_position_json = min_position_resp.json()
        min_position_xml = lxml.html.fromstring(min_position_json["page"])
        min_position = min_position_xml.xpath_first('//div/@data-min-position')
        print("Min Position for pagination of Following of {} is {}".format(username, min_position))
        return min_position
    #
    def prepare_data(self, username):
        data = {}
        data["headers"] = {
                            "Accept": "application/json, text/javascript, */*; q=0.01",
                            "X-Twitter-Active-User": "yes",
                            "Referer": "https://twitter.com/{}/following".format(username),
                            }
        return data
    #
    def get_following(self, username, min_position=None):
        if not min_position:
            min_position = self.get_min_position(username)
        data = self.prepare_data(username)     
        url = self.get_following_url.format(username, min_position)
        following_resp = self.requests_manager.make_request(url, headers=data["headers"])
        print(following_resp)
        if following_resp.status_code == 200:
            following_json = following_resp.json()
            following = self.parse_following(following_json)
            return following
        return []


# fl = Following(rm)
# test = fl.get_following("unfollowpro1")