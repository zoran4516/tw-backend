# unfollowpro@gmail.com pass: 123321aa 


class Configuration(object):
    # Captcha
    twitter_captcha_url = "https://twitter.com/account/access"
    twitter_site_key = "6Lc5hC4UAAAAAEx-pIfqjpmg-_-1dLnDwIZ8RToe"
    two_captcha_api_key = "ad17fcd59a1eb8d3fbfd96f1c50eb1a7"
    two_captcha_submit_url = "http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}&json=1"
    two_captcha_result_url = "http://2captcha.com/res.php?key={}&action=get&id={}&json=1"
    #
    home_url = "https://twitter.com"
    login_url = "https://twitter.com/sessions"
    logout_url = "https://twitter.com/logout"
    settings_url = "https://twitter.com/settings/account"
    ui_metrics_url = "https://twitter.com/i/js_inst?c_name=ui_metrics"
    checkpoint_solution_url = "https://twitter.com/account/login_challenge"
    # Actions Url
    follow_url = "https://api.twitter.com/1.1/friendships/create.json"
    unfollow_url = "https://api.twitter.com/1.1/friendships/destroy.json"
    like_url = "https://api.twitter.com/1.1/favorites/create.json"
    # Service Worker Url
    sw_url = "https://twitter.com/sw.js"
    # Data Url
    get_tweets_url = "https://twitter.com/i/profiles/show/{}/timeline/tweets?include_available_features=1&include_entities=1&max_position={}&reset_error_state=false"
    get_followers_url = "https://twitter.com/{}/followers/users?include_available_features=1&include_entities=1&lang=en&max_position={}&reset_error_state=false"
    get_following_url = "https://twitter.com/{}/following/users?include_available_features=1&include_entities=1&lang=en&max_position={}&reset_error_state=false"
    get_hashtags_url = "https://twitter.com/i/search/timeline?vertical=news&q=%23{}&src=hash&include_available_features=1&include_entities=1&max_position={}&reset_error_state=false"
    get_user_data_url = "https://twitter.com/i/profiles/popup?user_id={}&wants_hovercard=true&_={}"
    #
    headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Host": "twitter.com",
                "Origin": "https://twitter.com",
                "Referer": "https://twitter.com/",
                "Upgrade-Insecure-Requests": "1",
            }