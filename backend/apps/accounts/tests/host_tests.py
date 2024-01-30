from unittest.mock import patch
from backend.components.CORS.hosts import Hosts
from rest_framework.test import APITestCase


class TestHosts(APITestCase):

    @patch('backend.components.CORS.hosts.config')
    def test_debug_configuration(self, mock_config):
        mock_config.side_effect = lambda key, **kwargs: {
            'DEBUG_BACKEND_HOST': 'api.localhost',
            'DEBUG_FRONTEND_HOST': 'localhost'
        }.get(key, None)

        hosts = Hosts(debug=True)

        self.assertEqual(hosts.backend, 'api.localhost')
        self.assertEqual(hosts.frontend, 'localhost')

    @patch('backend.components.CORS.hosts.config')
    def test_production_configuration(self, mock_config):
        mock_config.side_effect = lambda key, **kwargs: {
            'BACKEND_HOST': 'api.example.com',
            'FRONTEND_HOST': 'www.example.com'
        }.get(key, None)

        hosts = Hosts(debug=False)

        self.assertEqual(hosts.backend, 'api.example.com')
        self.assertEqual(hosts.frontend, 'www.example.com')

    def test_origin_domain_for_localhost(self):
        hosts = Hosts(debug=True)
        self.assertEqual(hosts.origin_domain, 'localhost')

    @patch('backend.components.CORS.hosts.config')
    def test_origin_domain_for_production(self, mock_config):
        mock_config.side_effect = lambda key, **kwargs: {
            'BACKEND_HOST': 'api.example.com',
            'FRONTEND_HOST': 'www.example.com'
        }.get(key, None)
        hosts = Hosts(debug=False)
        self.assertEqual(hosts.origin_domain, 'example.com')
