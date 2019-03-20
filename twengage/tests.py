from django.test import TestCase
from db_handler import get_account

# Test for getting followings
from Particle.requests_manager import RequestsManager
from Particle.session import Session
from Particle.actions import Actions
from Particle.Extractors import following

account_obj = get_account("@objectcart1")
rm = RequestsManager()
session = Session(rm, account_obj)
session.login()
fwings = following.Following(rm)
test = fwings.get_following("objectcart1")
