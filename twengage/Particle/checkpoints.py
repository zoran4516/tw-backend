import urllib.parse
import lxml.html
import re
import time

from .configuration import Configuration

#####################################################################################
# Custom method to get first element or empty element by xpath
def xpath_first(self, elm_xpath):
    elements = self.xpath(elm_xpath)
    return next(iter(elements), lxml.html.HtmlElement())

lxml.html.HtmlElement.xpath_first = xpath_first
#####################################################################################

class Checkpoints(object):
    def __init__(self, requests_manager):
        self.requests_manager = requests_manager
        self.initialize()
        return None
    #
    def initialize(self):
        self.checkpoint_solution_url = Configuration.checkpoint_solution_url
        self.twitter_captcha_url     = Configuration.twitter_captcha_url
        self.twitter_site_key        = Configuration.twitter_site_key
        self.two_captcha_api_key     = Configuration.two_captcha_api_key
        self.two_captcha_submit_url  = Configuration.two_captcha_submit_url
        self.two_captcha_result_url  = Configuration.two_captcha_result_url
        return None
    #
    def get_checkpoint_details(self, response):
        checkpoint_xml = lxml.html.fromstring(response.content)
        checkpoint_details = {}
        checkpoint_details["checkpoint_url"]        = response.url
        checkpoint_details["checkpoint_message"]    = re.sub(r'\n+', '\n', re.sub(r'\n +', '\n', checkpoint_xml.xpath_first('//div[@class="Section"]').text_content()))
        checkpoint_details["authenticity_token"]    = checkpoint_xml.xpath_first('//input[@name="authenticity_token"]/@value')
        checkpoint_details["challenge_id"]          = checkpoint_xml.xpath_first('//input[@name="challenge_id"]/@value')
        checkpoint_details["user_id"]               = checkpoint_xml.xpath_first('//input[@name="user_id"]/@value')
        checkpoint_details["challenge_type"]        = checkpoint_xml.xpath_first('//input[@name="challenge_type"]/@value')
        checkpoint_details["platform"]              = checkpoint_xml.xpath_first('//input[@name="platform"]/@value')
        checkpoint_details["redirect_after_login"]  = checkpoint_xml.xpath_first('//input[@name="redirect_after_login"]/@value')
        checkpoint_details["remember_me"]           = checkpoint_xml.xpath_first('//input[@name="remember_me"]/@value')
        #
        # if checkpoint_details["challenge_type"] == "RetypeScreenName":
        return checkpoint_details
    #
    def prepare_challenge_data(self, checkpoint_details):
        challenge_data = {}
        checkpoint_url              = checkpoint_details["checkpoint_url"]
        checkpoint_message          = checkpoint_details["checkpoint_message"]
        authenticity_token          = checkpoint_details["authenticity_token"]
        challenge_id                = checkpoint_details["challenge_id"]
        user_id                     = checkpoint_details["user_id"]
        challenge_type              = checkpoint_details["challenge_type"]
        platform                    = checkpoint_details["platform"]
        redirect_after_login        = checkpoint_details["redirect_after_login"]
        remember_me                 = checkpoint_details["remember_me"]
        #
        print(checkpoint_message)
        challenge_response = str(input("Please enter a response to the {} challenge: ".format(challenge_type)))
        #
        challenge_data["data"] = {
                            "authenticity_token": authenticity_token,
                            "challenge_id": challenge_id,
                            "user_id": user_id,
                            "challenge_type": challenge_type,
                            "platform": platform,
                            "redirect_after_login": redirect_after_login,
                            "remember_me": remember_me,
                            "challenge_response": challenge_response,
        }
        challenge_data["headers"] = {
            "Referer": checkpoint_url
        }
        return challenge_data
    #
    def solve_challenge(self, response): 
        checkpoint_details = self.get_checkpoint_details(response)
        challenge_data = self.prepare_challenge_data(checkpoint_details)
        solved_response = self.requests_manager.make_request(self.checkpoint_solution_url, data=challenge_data["data"], headers=challenge_data["headers"], method="POST")
        if "/login_challenge" not in solved_response.url:
            print("Checkpoint Solved Successfully")
            return True
        else:
            print("Checkpoint could not be solved, try again.")
        return self.solve_challenge(response)
    #
    def get_captcha_solution(self, captcha_id):
        url = self.two_captcha_result_url.format(self.two_captcha_api_key, captcha_id)
        captcha_response = self.requests_manager.make_request(url)
        if captcha_response.status_code == 200:
            captcha_json = captcha_response.json()
            print(captcha_json)
            if not captcha_json["status"]:
                print("Sleeping for 5 seconds, captcha not ready!")
                time.sleep(5)
                return self.get_captcha_solution(captcha_id)
            return captcha_json["request"]
        return None
    #
    def submit_captcha(self):
        url = self.two_captcha_submit_url.format(self.two_captcha_api_key, self.twitter_site_key, self.twitter_captcha_url)
        print(url)
        captcha_response = self.requests_manager.make_request(url)
        if captcha_response.status_code == 200:
            captcha_json = captcha_response.json()
            print(captcha_json)
            return captcha_json["request"]
        return []
    #
    def prepare_captcha_data(self, response, captcha_solution):
        data = {}
        data["data"] = {}
        data["headers"] = {}
        xml = lxml.html.fromstring(response.content)
        data["headers"]["Referer"] = "https://twitter.com/account/access"
        #
        data["data"]["authenticity_token"] = xml.xpath_first('//input[@name="authenticity_token"]/@value')
        data["data"]["assignment_token"] = xml.xpath_first('//input[@name="assignment_token"]/@value')
        data["data"]["lang"] = "en"
        data["data"]["flow"] = ""
        if captcha_solution:
            data["data"]["g-recaptcha-response"] = captcha_solution
            data["data"]["verification_string"] = captcha_solution
        return data
    #
    def pre_captcha_requests(self):
        print("Solving Captcha")
        # Load the page before captcha
        sc_resp_1 = self.requests_manager.make_request(self.twitter_captcha_url)
        # print("\n\n\n")
        # print(sc_resp_1.content)
        # print("\n\n\n")
        print("Status Code of first GET request to get captcha is {}".format(sc_resp_1.status_code))
        data = self.prepare_captcha_data(sc_resp_1, None)
        print("Data of second POST request is {}".format(data))
        # This request is to tell twitter we are ready to solve captcha
        sc_resp_2 = self.requests_manager.make_request(self.twitter_captcha_url, headers=data["headers"], data=data["data"], method="POST")
        print("Status Code of second POST request to get captcha is {}".format(sc_resp_2.status_code))        
        return sc_resp_1
    #
    def solve_captcha(self):
        sc_resp_1 = self.pre_captcha_requests()
        # 2Captcha from here
        captcha_id = self.submit_captcha()
        print("Captcha Id for submitted captcha is {}".format(captcha_id))
        if captcha_id:
            captcha_solution = self.get_captcha_solution(captcha_id)
            print("Captcha Solution of the captcha is {}".format(captcha_solution))
            # Submit to twitter
            if captcha_solution:
                data = self.prepare_captcha_data(sc_resp_1, captcha_solution)
                print(data)
                captcha_solved_response = self.requests_manager.make_request(self.twitter_captcha_url, headers=data["headers"], data=data["data"], method="POST")
                print("Response Code of solved captcha submitted to twitter is {}".format(captcha_solved_response.status_code))
                # Calling same function to tell twitter we have solved Captcha, now send us back to twitter
                self.pre_captcha_requests()
            return captcha_solved_response
        return None






# import requests

# TWO_CAPTCHA_API_KEY = "ad17fcd59a1eb8d3fbfd96f1c50eb1a7"


# https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lc5hC4UAAAAAEx-pIfqjpmg-_-1dLnDwIZ8RToe&co=aHR0cHM6Ly90d2l0dGVyLmNvbTo0NDM.&hl=en&v=v1536705955372&theme=light&size=normal&cb=6dn7l6m1kjni


# http://2captcha.com/in.php?key=ad17fcd59a1eb8d3fbfd96f1c50eb1a7&method=userrecaptcha&googlekey=6Lc5hC4UAAAAAEx-pIfqjpmg-_-1dLnDwIZ8RToe&pageurl=https://twitter.com/account/access


# http://2captcha.com/res.php?key=ad17fcd59a1eb8d3fbfd96f1c50eb1a7&action=get&id=60492048686

# OK|03AL4dnxrR2bCv49Sr4Rc0zMAUbNjBLpOoHohNbJJJ2-kAvVWQCouJKxOHN5uC5-Re1CqAY4bOn8q_fwYWRmJu_3s0_tATLegmtwAuejtnzi0r-Dv_MdrRJHCceyaEwSR8UM6BBMAD0LQe6BrzyOfq0F-j9_4ZrjwdeV6EDole6ZXAEXxgh4f7CRl6V-xwHJjIKUOKYbx2NYBZCR9Ao2jkazQssbmb7D9A1HsjhvlOCddyfFKjmK1oSYdmFw8dQvqn3-S-k4iVTrmpGuxa-ffrp8YGonahMFOULceCwcyrgUwmCjoBTm2Em59R-JwZH8OI74UtzDTb9GpPvyvEXYOdrKva8vVPQ9Ygow



# POST https://twitter.com/account/access HTTP/1.1

# Referer: https://twitter.com/account/access

# authenticity_token=659ac8e0cc8be0fb8d9e87d235bbdf587324b7dc&assignment_token=201839685&lang=en&flow=&g-recaptcha-response=03AL4dnxrBKf1eZQYl4pk_M1DjHjadTrVBgea_evoZDxDi9HWD61N79S3n31bRv40kw-r3T3rXWGHKaVofrgQz9cSWVS-dm-oDoMUD-Hf-wd8Ae_3IDuc3Tv3OY_Su7wKRoIrcKv5pzqml0kCPaEfh9gRZgx9YpTyzGWoC8jOlo0pUapjQkBimzjRclHH4VuI3PbKpToiH98dDmsffZNwqfyo1ZQ0EvWi1ypRZg65UOoRyWbQYQ9vnH8W3yBz4XqBrlZ2DMrGn8BCgAT3dqiCtqC4DqKDnmRowQw&verification_string=03AL4dnxrBKf1eZQYl4pk_M1DjHjadTrVBgea_evoZDxDi9HWD61N79S3n31bRv40kw-r3T3rXWGHKaVofrgQz9cSWVS-dm-oDoMUD-Hf-wd8Ae_3IDuc3Tv3OY_Su7wKRoIrcKv5pzqml0kCPaEfh9gRZgx9YpTyzGWoC8jOlo0pUapjQkBimzjRclHH4VuI3PbKpToiH98dDmsffZNwqfyo1ZQ0EvWi1ypRZg65UOoRyWbQYQ9vnH8W3yBz4XqBrlZ2DMrGn8BCgAT3dqiCtqC4DqKDnmRowQw