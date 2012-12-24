"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django_webtest import WebTest

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
import drest
from backend.models import Genre
from django.utils import unittest
from django.test.client import Client
from django.test import LiveServerTestCase
#from tastypie.test import ResourceTestCase
from backend.models import Article

#class ArticleResourceTest(ResourceTestCase):


class MyTest(LiveServerTestCase):
    fixtures=['users.json']

    def test_api_articles_get(self):
        api = drest.api.TastyPieAPI(self.live_server_url + '/api/v1/', auth_mech='basic')
        api.auth('admin', 'admin')
        genre_data = dict(title='SF', id=1)
        api.genre.post(genre_data)
        genre = Genre.objects.all()[0]
        assert 'SF' in genre.title





