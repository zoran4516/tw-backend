import django
import os
import sys
# rootDir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..'))

sys.path.append('../')
# sys.path.append(rootDir)
# print(rootDir)

# print(os.getcwd())
# print(sys.path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Matter.settings'
django.setup()

from twengage.models import Account, Stat

def save_followings(userNameInput, followings):
    record = Account.objects.get(username=userNameInput)
    record.org_following_users = ""
    for following in followings :
        if record.org_following_users.find(following) == -1:
            record.org_following_users += (following + ' ')

    record.following_cnt=len(followings)
    record.save()

def save_followers(userNameInput, followers):
    record = Account.objects.get(username=userNameInput)
    record.follower_users = ""
    for follower in followers :
        if record.follower_users.find(follower) == -1:
            record.follower_users += (follower + ' ')
    record.follower_cnt=len(followers)
    record.save()

def set_userActive(userNameInput, value):
    record = Account.objects.get(username=userNameInput)
    record.user_active = value
    record.save()

def all_accounts():
    return Account.objects.all()

def active_accounts():
    return Account.objects.filter(user_active=True)

def inactive_accounts():
    return Account.objects.filter(user_active=False)

def get_account(username):
    accounts = list(Account.objects.filter(username=username))
    if accounts:
        return accounts[0]
    return []

def get_stats_by_account_date(account, date):
    stat_objs = list(Stat.objects.filter(account=account, date=date))
    if stat_objs:
        return stat_objs[0]
    else:
        stat_obj = Stat(account=account, date=date)
        return stat_obj

def get_stats_by_account(account):
    account_obj = get_account(account)
    if account_obj:
        stat_objs = list(Stat.objects.filter(account=account_obj))
        return stat_objs
    return []

def get_stats_by_date(date):
    stat_objs = list(Stat.objects.filter(date=date))
    return stat_objs