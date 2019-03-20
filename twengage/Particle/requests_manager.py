from .configuration import Configuration

import requests
import time
import random



index = 0

proxies = [
    "twengage64:123321aa@185.217.170.58:80",
    "twengage64:123321aa@170.130.37.51:80",
    "twengage64:123321aa@185.217.170.134:80",
    "twengage64:123321aa@23.95.81.180:80",
    "twengage64:123321aa@155.94.221.41:80",
    "twengage64:123321aa@185.217.170.70:80",
    "twengage64:123321aa@170.130.98.234:80",
    "twengage64:123321aa@23.95.204.140:80",
    "twengage64:123321aa@23.83.87.42:80",
    "twengage64:123321aa@23.83.87.98:80",
    "twengage64:123321aa@170.130.98.149:80",
    "twengage64:123321aa@23.95.204.224:80",
    "twengage64:123321aa@23.95.204.227:80",
    "twengage64:123321aa@155.94.221.71:80",
    "twengage64:123321aa@170.130.98.230:80",
    "twengage64:123321aa@23.95.224.103:80",
    "twengage64:123321aa@155.94.221.136:80",
    "twengage64:123321aa@23.83.87.247:80",
    "twengage64:123321aa@185.217.170.165:80",
    "twengage64:123321aa@23.95.224.108:80"
]


# 107.175.88.217:80:twengage:123321aa
    
# set HTTPS_PROXY=https://twengage:123321aa@107.175.88.217:80
# set HTTP_PROXY=http://twengage:123321aa@107.175.88.217:80

class RequestsManager(object):
    def __init__(self):
        self.initialize()
        return None
    #
    def initialize(self):
        print("Initializing RequestsManager")
        #current_proxy = random.choice(proxies)
        current_proxy = proxies[index]
        proxy = {
            "http"  : "http://{}".format(current_proxy), 
            "https" : "https://{}".format(current_proxy)
        }
        _session = requests.Session()
        _session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3205.0 Safari/537.36"
        _session.proxies = proxy
        self.session = _session
        return None 
    #
    def parse_response(self, response):
        if response.status_code == 200:
            pass
        else:
            pass
        parsed_response = None
        return parsed_response
    #
    def make_request(self, url, data={}, headers={}, method="GET", ERROR=False):
        final_headers = Configuration.headers.copy()
        final_headers.update(headers)
        final_headers = {k: v for k, v in final_headers.items() if v is not None}
        response = False
        try:
            if method == "GET":
                response = self.session.get(url, headers=final_headers, timeout=3)
            elif method == "POST":
                response = self.session.post(url, headers=final_headers, data=data, timeout=3)
            elif method == "OPTIONS":
                response = self.session.options(url, headers=final_headers, timeout=3)
        #
        except requests.exceptions.Timeout:
                print("Request timeout occured, retrying now.")
                time.sleep(2)
                return self.make_request(url, data, headers, method, ERROR=False)
        #
        except Exception as request_error:
            print(request_error)
            if not ERROR:
                print("Error occured, retrying request")
                time.sleep(2)
                return self.make_request(url, data, headers, method, ERROR=True)
        #
        if response.status_code == 429:
            print(response.text)
            print("Quiting program due to Too many requests")
            raise SystemExit
        elif response.status_code == 404:
            print("Url not found: {}".format(url))
        elif response.status_code == 401:
            print("Unauthorized get new bearer token")
            print(response.text)
            raise SystemExit
        elif response.status_code == 403:
            print("Unauthorized")
            print(response.text)
        return response