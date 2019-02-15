from django.shortcuts import render, redirect
from twengage import db_handler

import os
import threading
import datetime
import random
import time


# def start_bots(self):
#     accounts = db_handler.active_accounts()
#     for acc in accounts:
#         os.start("start cmd /K & cd Scripts & activate & cd .. & cd {} & python manage.py migrate")
#         start cmd /K ".\Scripts\activate & cd .\Matter\ & cd .\twengage\"
#     return None


def homepage(request):
    return render(request, "home.html")

def accounts(request):
    context = {
        "accounts": db_handler.all_accounts(),
    }
    return render(request, "accounts.html", context=context)

def stats(request):
    date = datetime.datetime.now().strftime ("%m-%d-%Y")
    context = {
        "stats": db_handler.get_stats_by_date(date)
    }
    return render(request, "stats.html", context=context)

def specific_stats(request, account):
    context = {
        "stats": db_handler.get_stats_by_account(account)
    }
    return render(request, "stats.html", context=context)
#    
def start(request, account):
 #   print(account)
    if account == "all":
        print("Starting all accounts")
        accounts = db_handler.all_accounts()
    elif account == "active":
        print("Starting all active accounts")
        accounts = db_handler.active_accounts()
    elif account == "inactive":
        print("Starting all inactive accounts")
        accounts = db_handler.inactive_accounts()
    elif account:
        print("Starting single account : {}".format(account))
        accounts = [db_handler.get_account(account)]
    #
    th = threading.Thread(target=lambda: start_bot(accounts))
    th.start()
    return redirect("/accounts/")

def start_bot(accounts):
    # for each_acc in db_handler.all_accounts():
    for each_acc in accounts:
        pause_time = random.choice(range(2,3))
        print("Starting account: {}".format(each_acc.username))
        time.sleep(1)
        os.system('start cmd /K "TITLE {0} & cd twengage & resize_cmd 80 25 80 9999 & python follow_liker.py -u{0}"'.format(each_acc.username))
        # os.system('start cmd /K "TITLE {0} & cd twengage & resize_cmd 80 25 80 9999 & python unfollower.py -u{0}"'.format(each_acc.username))
    return None