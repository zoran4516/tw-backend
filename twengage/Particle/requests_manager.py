from .configuration import Configuration

import requests
import time
import random




proxies = [
    "twengage108:123321aa@198.144.187.73:80",
"twengage108:123321aa@200.10.37.234:80",
"twengage108:123321aa@206.41.178.38:80",
"twengage108:123321aa@200.10.37.216",
"twengage108:123321aa@154.16.87.11:80",
"twengage108:123321aa@191.96.240.55:80",
"twengage108:123321aa@173.44.164.148:80",
"twengage108:123321aa@154.16.87.65:80",
"twengage108:123321aa@207.244.117.38:80",
"twengage108:123321aa@196.196.86.194:80",
"twengage108:123321aa@173.44.164.183:80",
"twengage108:123321aa@185.143.242.149:80",
"twengage108:123321aa@173.44.164.106:80",
"twengage108:123321aa@185.143.242.22:80",
"twengage108:123321aa@200.10.37.8:80",
"twengage108:123321aa@209.242.221.164:80",
"twengage108:123321aa@209.242.221.134:80",
"twengage108:123321aa@207.244.117.125:80",
"twengage108:123321aa@206.41.178.212:80",
"twengage108:123321aa@198.144.182.168:80",
"twengage108:123321aa@209.242.221.168:80",
"twengage108:123321aa@107.175.141.180:80",
"twengage108:123321aa@185.143.242.31:80",
"twengage108:123321aa@196.196.86.130:80",
"twengage108:123321aa@154.16.87.76:80",
"twengage108:123321aa@192.210.147.53:80",
"twengage108:123321aa@196.196.86.169:80",
"twengage108:123321aa@107.173.92.179:80",
"twengage108:123321aa@191.96.240.46:80",
"twengage108:123321aa@185.143.242.18:80",
"twengage108:123321aa@191.96.241.48:80",
"twengage108:123321aa@154.16.87.56:80",
"twengage108:123321aa@107.172.181.180:80",
"twengage108:123321aa@207.244.117.89:80",
"twengage108:123321aa@173.44.164.254:80",
"twengage108:123321aa@207.244.117.201:80",
"twengage108:123321aa@200.10.37.140:80",
"twengage108:123321aa@104.160.1.206:80",
"twengage108:123321aa@172.245.119.11:80",
"twengage108:123321aa@23.94.185.184:80",
"twengage108:123321aa@196.196.86.13:80",
"twengage108:123321aa@191.96.241.121:80",
"twengage108:123321aa@200.10.37.138:80",
"twengage108:123321aa@173.44.164.118:80",
"twengage108:123321aa@206.41.178.236:80",
"twengage108:123321aa@207.244.117.235:80",
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
        current_proxy = random.choice(proxies)
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