import os
import unittest
from typing import Dict

import django
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.urls.resolvers import ResolverMatch
from django_extensions import middlewares

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()


class GetClientIpTests(unittest.TestCase):

    def test_simple(self):
        params: Dict[str, str] = {
            'REQUEST_METHOD': 'GET',
            'wsgi.input': '',
            'REMOTE_ADDR': '127.0.0.0'
        }
        request = WSGIRequest(params)
        ip = middlewares._get_client_ip(request)

        self.assertEqual(ip, params['REMOTE_ADDR'])


class AdminIPRestrictionMiddlewareTests(unittest.TestCase):

    def setUp(self):
        self.middleware: object = middlewares.AdminIPRestrictionMiddleware(
            get_response='a'
        )
        params: Dict[str, str] = {
            'REQUEST_METHOD': 'GET',
            'wsgi.input': '',
            'REMOTE_ADDR': 'xxx.xxx.xxx.xxx'
        }
        self.request: object = WSGIRequest(params)
        self.request.resolver_match = ResolverMatch(
            '', {}, {}, app_names=['admin']
        )

    def test_allowed_ip(self):
        r = self.middleware.process_view(self.request, None, None, None)
        self.assertIsNone(r)

    def test_restricted_ip(self):
        params: Dict[str, str] = {
            'REQUEST_METHOD': 'GET',
            'wsgi.input': '',
            'REMOTE_ADDR': '0.0.0.0'
        }
        self.request: object = WSGIRequest(params)
        self.request.resolver_match = ResolverMatch(
            '', {}, {}, app_names=['admin']
        )

        with self.assertRaises(Http404):
            self.middleware.process_view(self.request, None, None, None)
