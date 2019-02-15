from ..configuration import Configuration
import lxml.html
import datetime


class User(object):
    def __init__(self, requests_manager):
        self.requests_manager = requests_manager
        self.initialize()
        return None
    #
    def initialize(self):
        self.home_url = Configuration.home_url
        self.get_user_data_url = Configuration.get_user_data_url
        return None
    #
    def get_user_id(self, username):
        user_profile_resp = self.requests_manager.make_request(self.home_url + "/" + str(username))
        user_profile_xml = lxml.html.fromstring(user_profile_resp.content)
        user_id = user_profile_xml.xpath_first('//div[@class="ProfileNav"]/@data-user-id')
        print("{} id is {}".format(username, user_id))
        return user_id
    #
    def prepare_data(self):
        data = {}
        data["headers"] = {
                            "Accept": "application/json, text/javascript, */*; q=0.01",
                            "X-Twitter-Active-User": "yes",
                            "X-Requested-With": "XMLHttpRequest",
                            }
        return data
    #
    def parse_user_data_from_id(self, user_data_json):
        user_data_xml = lxml.html.fromstring(user_data_json["html"])
        you_follow = True
        if user_data_xml.xpath('//div[contains(@class, "not-following")]'):
            you_follow = False
        user_data = {
            "user_id" : user_data_json["user_id"],
            "username" : user_data_json["screen_name"],
            "you_follow" : you_follow,
        }  
        return user_data
    #
    def get_user_data_from_id(self, user_id):
        data = self.prepare_data()
        url = self.get_user_data_url.format(user_id, int(datetime.datetime.timestamp(datetime.datetime.now())*1000))
        print(url)
        user_data_resp = self.requests_manager.make_request(url, headers=data["headers"])
        print(user_data_resp)
        if user_data_resp.status_code == 200:
            user_data_json = user_data_resp.json()
            user_data = self.parse_user_data_from_id(user_data_json)
            return user_data
        return []


# k = User(rm)
# user_id = k.get_user_id("iamsrk")
# k.get_user_data_from_id(user_id)
