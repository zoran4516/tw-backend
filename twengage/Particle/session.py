from slimit.lexer import Lexer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import lxml.html
import pprint
import re
import json
import requests
import time
import random
import ctypes
import os
import signal



#
from .configuration import Configuration
from .checkpoints import Checkpoints
from .requests_manager import RequestsManager
from .Extractors.settings import Settings



#####################################################################################
# Custom method to get first element or empty element by xpath
def xpath_first(self, elm_xpath):
    elements = self.xpath(elm_xpath)
    return next(iter(elements), lxml.html.HtmlElement())

lxml.html.HtmlElement.xpath_first = xpath_first
#####################################################################################


class Session(object):
    def __init__(self, requests_manager, account_obj):
        '''
        requests_manager: requests manager instance
        '''
        self.requests_manager = requests_manager
        self.account_obj = account_obj
        self.cookies = account_obj.cookies
        self.initialize()
        return None
    #
    def initialize(self):
        print("Initializing Session")
        time.sleep(random.choice(range(4,10)))
        self.sw_url = Configuration.sw_url
        self.home_url = Configuration.home_url
        self.login_url = Configuration.login_url
        self.logout_url = Configuration.logout_url
        self.settings_url = Configuration.settings_url
        self.ui_metrics_url = Configuration.ui_metrics_url
        self.checkpoints_obj = Checkpoints(self.requests_manager)
        self.settings_obj = Settings(self.requests_manager)
        self.load_cookies()
        return None
    #
    def save_settings(self):
        print("Saving User Settings")
        if not all([
                    self.account_obj.name, 
                    self.account_obj.email, 
                    # self.account_obj.phone_number, 
                    self.account_obj.user_verified, 
                    self.account_obj.user_id,
                ]):
            settings = self.settings_obj.get_settings()
            try:
                print(settings)
            except:
                print("Encoding error while printing settings")
                print(str(settings).encode())
            if settings:
                name = settings.get("name")
                email = settings.get("email")
                phone_number = settings.get("phone_number")
                user_verified = settings.get("user_verified")
                user_id = settings.get("user_id")
                self.account_obj.refresh_from_db()
                if name:
                    self.account_obj.name = name
                if email:
                    self.account_obj.email = email
                if phone_number:
                    self.account_obj.phone_number = phone_number
                if user_verified:
                    self.account_obj.user_verified = user_verified
                if user_id:
                    self.account_obj.user_id = user_id
                self.account_obj.save()
        return None
    #
    def save_cookies(self):
        cookies_dict = requests.utils.dict_from_cookiejar(self.requests_manager.session.cookies)
        print(cookies_dict)
        cookies_json = json.dumps(cookies_dict)
        self.account_obj.refresh_from_db()
        self.account_obj.cookies = cookies_json
        self.account_obj.save()
        return None
    #
    def load_cookies(self):
        cookies = self.account_obj.cookies
        if cookies:
            cookie_jar = requests.cookies.cookiejar_from_dict(json.loads(cookies))
            self.requests_manager.session.cookies.update(cookie_jar)
        return None
    #
    def get_ui_metrics(self):
        init_js = '''
                        ui_metrics_elm = document.createElement("input")
                        ui_metrics_elm.setAttribute("type", "hidden")
                        ui_metrics_elm.setAttribute("name", "ui_metrics")
                        ui_metrics_elm.setAttribute("autocomplete", "off")
                        ui_metrics_elm.setAttribute("value", "")
                        document.body.appendChild(ui_metrics_elm);
                '''
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--log-level=3')
        driver = webdriver.Chrome(chrome_options=options)
        ui_metrics_js = self.requests_manager.make_request(self.ui_metrics_url).text
        driver.execute_script(init_js)
        driver.execute_script(ui_metrics_js)
        ui_metrics = driver.find_element_by_name("ui_metrics").get_attribute("value")
        driver.quit()
        return ui_metrics
    #
    def get_bearer_token(self):
        print("Getting Bearer Token")
        bt_headers = {"Host": "abs.twimg.com",}
        sw_resp = self.requests_manager.make_request(self.home_url)
        sw_xml  = lxml.html.fromstring(sw_resp.content)
        bt_url = sw_xml.xpath_first('//script[contains(@src, "/init")]//@src')
        print(bt_url)
        bt_resp = self.requests_manager.make_request(bt_url, headers=bt_headers)
        bt_resp_str = bt_resp.text
        print(bt_resp)
        # bearer_token = re.search(r'"([^"]|"")*"', bt_resp_str[bt_resp_str.index("BEARER_TOKEN") + len("BEARER_TOKEN"):-1])
        token_index = bt_resp_str.index('.a="') + len('.a=')
        # bearer_token = re.search(r"'([^']|'')*'", bt_resp_str[token_index: token_index+250])
        bearer_token = re.search(r'"([^"]|"")*"', bt_resp_str[token_index: token_index+250])
        print(bearer_token)
        if bearer_token:
            bearer_token = bearer_token.group(0).strip('"')
        else:
            print("Bearer Token is empty, quitting and restarting program")
            ppid = os.getppid()
            os.kill(ppid, signal.SIGTERM)
            print("Sleeping for 5s and restarting bot.")
            time.sleep(5)
            os.system('start cmd /K "TITLE {0} & resize_cmd 80 25 80 9999 & python follow_liker.py -u{0}"'.format(self.account_obj.username))
            time.sleep(2)
            raise SystemExit
        return bearer_token
    # #
    # def get_bearer_token(self):
    #     print("Getting Bearer Token")
    #     bt_headers = {"Host": "abs.twimg.com",}
    #     sw_resp = self.requests_manager.make_request(self.sw_url)
    #     lexer = Lexer()
    #     lexer.input(sw_resp.text)
    #     bt_url = [token.value for token in lexer if (token.type == "STRING" and "serviceworker" in token.value)][0].strip('"')
    #     print(bt_url)
    #     bt_resp = self.requests_manager.make_request(bt_url, headers=bt_headers)
    #     bt_resp_str = bt_resp.text
    #     print(bt_resp)
    #     # bearer_token = re.search(r'"([^"]|"")*"', bt_resp_str[bt_resp_str.index("BEARER_TOKEN") + len("BEARER_TOKEN"):-1])
    #     token_index = bt_resp_str.index("BEARER_TOKEN") + len("BEARER_TOKEN")
    #     # bearer_token = re.search(r"'([^']|'')*'", bt_resp_str[token_index: token_index+250])
    #     bearer_token = re.search(r'"([^"]|"")*"', bt_resp_str[token_index: token_index+250])
    #     print(bearer_token)
    #     if bearer_token:
    #         bearer_token = bearer_token.group(0).strip("'")
    #     else:
    #         print("Bearer Token is empty, quitting and restarting program")
    #         ppid = os.getppid()
    #         os.kill(ppid, signal.SIGTERM)
    #         print("Sleeping for 5s and restarting bot.")
    #         time.sleep(5)
    #         os.system('start cmd /K "TITLE {0} & resize_cmd 80 25 80 9999 & python follow_liker.py -u{0}"'.format(self.account_obj.username))
    #         time.sleep(2)
    #         raise SystemExit
    #     return bearer_token
    #
    def get_authenticity_token(self):
        # Get authenticity_token from home page
        token_resp = self.requests_manager.make_request(self.home_url)
        token_xml = lxml.html.fromstring(token_resp.content)
        authenticity_token = token_xml.xpath_first('//input[@name="authenticity_token"]/@value')        
        return authenticity_token
    #
    def prepare_login(self):
        login_data = {}
        authenticity_token = self.get_authenticity_token()
        ui_metrics = self.get_ui_metrics()
        login_data["headers"]  = {
                                    "Referer": "https://twitter.com/login",
                                    "Content-Type": "application/x-www-form-urlencoded",
                                    }
        login_data["data"] = {
                                    "session[username_or_email]": self.account_obj.username,
                                    "session[password]": self.account_obj.password,
                                    "authenticity_token": authenticity_token,
                                    "ui_metrics": ui_metrics,
                                    "scribe_log": "",
                                    "redirect_after_login": "",
                                    "remember_me": "1",
                                }                  
        return login_data
    #
    def prepare_logout(self):        
        self.d = {}
        logout_data = self.d
        authenticity_token = self.get_authenticity_token()
        logout_data["headers"] = {
                                    "X-Requested-With": "XMLHttpRequest",
                                    "X-Twitter-Active-User": "yes",
                                    "Referer": "https://twitter.com/settings/account",
                                    }
        logout_data["data"] = {
                                    "authenticity_token": authenticity_token,
                                    "nonPermanent": "true",
                                    }
        return logout_data
    #
    def is_logged_in(self):
        # Try loading the accounts page in settings, if the url matches, then return True
        settings_page = self.requests_manager.session.get(self.settings_url)
        #print(settings_page)
        print(settings_page.url)
        if settings_page.url == self.settings_url:
            print("{} is logged in".format(self.account_obj.username))
            self.save_cookies()
            self.save_settings()
            self.bearer_token = self.get_bearer_token()
            self.account_obj.refresh_from_db()
            self.account_obj.user_active = True
            self.account_obj.save()    
            print("Minimizing window in 2s")
            time.sleep(2)
            #ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
            # Setting Bearer Token
            return True
        return False
    #
    def login(self):
        # Check if user is already logged in
        if not self.is_logged_in():
            print("Logging In!")
            login_data = self.prepare_login()
            print("1 function")
            pprint.pprint(login_data, indent=4)
            print("2 function")
            login_response = self.requests_manager.make_request(self.login_url, data=login_data["data"], headers=login_data["headers"], method="POST")
            print(login_response)
            print(login_response.url)
            # Check if any checkpoints are present
            if "/login_challenge" in login_response.url:
                self.checkpoints_obj.solve_challenge(login_response)
            # Solve Captcha
            if "/account/access" in login_response.url:
                print("Captcha detected, trying to solve it.")
                self.checkpoints_obj.solve_captcha()
                input("Captcha Solved, please check the results above.")
            # Check if login was successful
            if not self.is_logged_in():
                print("{} logged in failed".format(self.account_obj.username))
                print("Quitting Program because logged in failed!")
                self.account_obj.refresh_from_db()
                self.account_obj.user_active = False
                self.account_obj.save()               
                raise SystemExit(0)
                # return False
        return True
    #
    def logout(self):
        print("Logging Out!")
        logout_data = self.prepare_logout()
        pprint.pprint(logout_data, indent=4)
        logout_response = self.requests_manager.make_request(self.logout_url, data=logout_data["data"], headers=logout_data["headers"], method="POST")
        print(logout_response)
        return logout_response



# rm = RequestsManager()
# alpha = Session(rm, "unfollowpro@gmail.com", "123321aa")
# alpha.login()


# omega = alpha.logout()
# print(omega)
# print(omega.url)

#Save And Load Cookies


