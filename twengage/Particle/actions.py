from .configuration import Configuration

class Actions(object):
    def __init__(self, requests_manager, bearer_token):
        self.requests_manager = requests_manager
        self.bearer_token = bearer_token
        self.initialize()
        return None
    #
    def initialize(self):
        print("Initializing Actions")
        self.home_url = Configuration.home_url
        self.follow_url = Configuration.follow_url
        self.like_url = Configuration.like_url
        self.unfollow_url = Configuration.unfollow_url
        return None
    #
    def fu_data(self, user_id):
        #user_id = "50393960"
        data = {}
        # latest_resp = self.requests_manager.make_request(self.home_url)
        x_csrf_token = self.requests_manager.session.cookies.get("ct0")
        print("X-CSRF-TOKEN : {}".format(x_csrf_token))
        data["headers"] = {
                                    "Host": "api.twitter.com",
                                    "x-csrf-token": x_csrf_token,
                                    "authorization": "Bearer {}".format(self.bearer_token),
                                    "x-twitter-auth-type": "OAuth2Session",
                                    "X-Twitter-Active-User": "yes",
                                }
        data["data"] = {
                                    "challenges_passed": "false",
                                    "handles_challenges": "1",
                                    "include_blocked_by": "true",
                                    "include_blocking": "true",
                                    "include_can_dm": "true",
                                    "include_followed_by": "true",
                                    "include_mute_edge": "true",
                                    "skip_status": "true",
                                    "user_id": str(user_id),
                            }
        return data
    #
    def like_data(self, tweet_id, tweet_likes):
        data = self.fu_data(None)
        data["data"] = {
                            "id": str(tweet_id),
                            "lang": "en",
                            "tweet_stat_count": tweet_likes,
                        }
        return data
    #
    def get_options_data(self):
        #user_id = "50393960"
        data = {}
        # self.requests_manager.make_request(self.home_url)
        # x_csrf_token = self.requests_manager.session.cookies.get("ct0")
        # print("X-CSRF-TOKEN : {}".format(x_csrf_token))
        data["headers"] = {
                            "Host": "api.twitter.com",
                            "Access-Control-Request-Method": "POST",
                            "Access-Control-Request-Headers": "authorization,x-csrf-token,x-twitter-active-user,x-twitter-auth-type",
                       }
        return data
    #
    def follow(self, user_id):
        data = self.fu_data(user_id)
        options_data = self.get_options_data()
        options_response = self.requests_manager.make_request(self.follow_url, headers=options_data["headers"], method="OPTIONS")
        if options_response.status_code == 200:
            follow_response = self.requests_manager.make_request(self.follow_url, data=data["data"], headers=data["headers"], method="POST")
            print("Follow Respnse: {}".format(follow_response))
            return follow_response
        return None
    #
    def unfollow(self, user_id):
        data = self.fu_data(user_id)
        options_data = self.get_options_data()
        options_response = self.requests_manager.make_request(self.unfollow_url, headers=options_data["headers"], method="OPTIONS")
        if options_response.status_code == 200:
            unfollow_response = self.requests_manager.make_request(self.unfollow_url, data=data["data"], headers=data["headers"], method="POST")
            return unfollow_response
        return None
    #
    def like(self, tweet_id, tweet_likes):
        data = self.like_data(tweet_id, tweet_likes)
        options_data = self.get_options_data()
        options_response = self.requests_manager.make_request(self.like_url, headers=options_data["headers"], method="OPTIONS")
        if options_response.status_code == 200:
            like_response = self.requests_manager.make_request(self.like_url, data=data["data"], headers=data["headers"], method="POST")
            print("Like Respnse: {}".format(like_response))
            return like_response
        return False


# twin = Actions(rm, bt)
# e = twin.like("1035732297318842368")