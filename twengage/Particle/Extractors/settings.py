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

class Settings(object):
    def __init__(self, requests_manager):
        self.requests_manager = requests_manager
        self.initialize()
        return None
    #
    def initialize(self):
        self.account_settings_url = "https://twitter.com/settings"
        self.device_settings_url = "https://twitter.com/settings/add_phone"
        return None
    #
    def prepare_data(self):
        settings_data = {}
        settings_data["headers"] = {
                                        "Accept": "application/json, text/javascript, */*; q=0.01",
                                        "X-Push-State-Request": "true",
                                        "X-Requested-With": "XMLHttpRequest",
                                        "X-Twitter-Active-User": "yes",
                                    }
        return settings_data
    #
    def extract_settings(self, json1, json2):
        settings = {}
        html = json1["page"] + json2["page"]
        settings_xml = lxml.html.fromstring(html)
        settings["name"] = settings_xml.xpath_first('//div[contains(@class, "DashboardProfileCard-name")]//a/text()')
        settings["email"] = settings_xml.xpath_first('//input[@type="hidden" and @id="orig_email"]/@value')
        settings["phone_number"] = settings_xml.xpath_first('//span[@class="device_number_with_country_code"]').text_content().encode().decode('ascii', 'ignore')
        settings["username"] = settings_xml.xpath_first('//input[@type="hidden" and @id="orig_uname"]/@value')
        #
        settings["user_id"] = json1["init_data"]["userId"]
        settings["user_verified"] = json1["init_data"]["userVerified"]
        return settings
    #
    def get_settings(self):
        settings_data = self.prepare_data()
        account_settings_resp = self.requests_manager.make_request(self.account_settings_url, headers=settings_data["headers"])
        settings_data["headers"]["Referer"] = "https://twitter.com/settings/account"
        device_settings_resp = self.requests_manager.make_request(self.device_settings_url, headers=settings_data["headers"])
        if (account_settings_resp.status_code == 200) and (device_settings_resp.status_code == 200):
            account_settings_json = account_settings_resp.json()
            device_settings_json = device_settings_resp.json()
            settings = self.extract_settings(account_settings_json, device_settings_json)
            return settings
        return {}


# a = Settings(rm)
# s = a.get_settings()