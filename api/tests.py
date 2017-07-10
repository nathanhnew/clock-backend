# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse
from api.models import UserSettings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework.authtoken.models import Token
# Create your tests here.


class SettingsTestCase(TestCase):
    '''Test settings model itself'''
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.userOne = User.objects.create_user(username="one",
                                                password="onepass",
                                                email="one@test.com")
        self.userOne.save()
        token = self.client.login(username='one', password='onepass')
        print(token)
        self.userTwo = User.objects.create_user(username="two",
                                                password="twopass",
                                                email="two@test.com")
        self.data1 = {'owner': self.userOne, 'theme': 'standard',
                      'alerts': False, 'fullDay': False, 'metric': False}
        self.data2 = {'owner': self.userTwo, 'theme': 'standard',
                      'alerts': True, 'fullDay': False, 'metric': True}

        UserSettings.objects.create(owner=self.userOne, theme='standard',
                                    alerts=False, fullDay=False, metric=False)
        UserSettings.objects.create(owner=self.userTwo, theme='standard',
                                    alerts=True, fullDay=True, metric=True)

    def test_settings_create(self):
        ownerOne = User.objects.get(username='one')
        ownerTwo = User.objects.get(username="two")
        user_one = UserSettings.objects.get(owner=ownerOne)
        user_two = UserSettings.objects.get(owner=ownerTwo)

        self.assertEqual(user_one.alerts, False)
        self.assertEqual(user_two.metric, True)


# class SettingsAPITestCase(APITestCase):
#     '''Defines the test suite for the User Settings Model'''
#     def setUp(self):
#         self.user = User.objects.create_user('john',
#                                              'john@snow.com',
#                                              'johnpassword')
#         self.client = APIClient()
#         self.client.credentials(username='john', password='johnpassword')
#         self.data = {'theme': 'standard', 'alerts': False,
#                      'fullDay': False, 'metric': False}
#         # self.theme = "standard"
#         # self.alerts = False
#         # self.fullDay = False
#         # self.metric = False
#         # self.owner = User.objects.create_user(username='test',
#         #                                       password='secret',
#         #                                       email="test@test.gov")
#         # self.Settings = UserSettings(owner=self.owner,
#         #                              theme=self.theme,
#         #                              alerts=self.alerts,
#         #                              fullDay=self.fullDay,
#         #                              metric=self.metric)
#
#     def test_can_create_settings(self):
#         response = self.client.post('/api/settings', self.data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
