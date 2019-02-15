from django.db import models


class Account(models.Model):
    def __str__(self):
        return self.username + " : " + self.password

    user_active = models.BooleanField("Twitter User Active", default=False)
    user_verified = models.BooleanField("Twitter User Verified", default=False)
    username = models.CharField("Twitter Username", max_length = 200, default=None, blank=True, null=True)
    name = models.CharField("Twitter Name", max_length = 200, default=None, blank=True, null=True)
    user_id = models.CharField("Twitter User Id", max_length = 200, default=None, blank=True, null=True)
    password = models.CharField("Twitter Password", max_length = 200, default=None, blank=True, null=True)
    email = models.CharField("Twitter Email", max_length = 2000, default=None, blank=True, null=True)
    phone_number = models.CharField("Twitter Phone Number", max_length = 2000, default=None, blank=True, null=True)
    current_hashtag = models.TextField("Working on this tag", max_length = 200, default=None, blank=True, null=True)
    current_following_account = models.TextField("Working on this user", max_length = 200, default=None, blank=True, null=True)
    hashtags = models.TextField("Twitter Hashtags", max_length = 3000, default=None, blank=True, null=True)
    follow_accounts = models.TextField("Twitter Accounts to Follow", max_length = 3000, default=None, blank=True, null=True)
    cookies = models.CharField("Twitter Account Cookies", max_length = 2000, default=None, blank=True, null=True)
    like = models.BooleanField("Like ?", default=True)
    follow = models.BooleanField("Follow ?", default=True)
    notes = models.TextField("Notes", max_length = 3000, default=None, blank=True, null=True)



class Stat(models.Model):
    def __str__(self):
        return self.account.username + " : " + str(self.followers) + " : " + str(self.updated_timestamp)

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    followers = models.BigIntegerField("Twitter User Followers", default=0)
    followings = models.BigIntegerField("Twitter User Followings", default=0)
    likes = models.BigIntegerField("Twitter User Likes", default=0)
    tweets = models.BigIntegerField("Twitter User Tweets", default=0)
    date = models.CharField("Stats scraped on", default=None, max_length=200, blank=True, null=True)
    updated_timestamp = models.DateTimeField("Stat Last Updated On", auto_now=True, null=True)
    created_timestamp = models.DateTimeField("Stat Saved On", auto_now_add=True, null=True) 




