# coding=utf-8
from .. import context_menu

import mock
import unittest


class context_menu_tests(unittest.TestCase):

    def context_menu(self, *a, **kw):
        return context_menu(*a, **kw)

    def test_empty_menu(self):
        with mock.patch(
            'euphorie.client.api.getTreeData', return_value={
                'children': []
            }
        ):
            self.assertEqual(
                self.context_menu(mock.Mock(), 'context', 'phase', None), []
            )

    def test_risk_status_no_class_set(self):
        menu = {
            'children': [{
                'id': 15,
                'type': 'risk',
                'class': None,
                'leaf_module': True,
                'path': '/1',
                'current_parent': False,
                'url': '/1',
                'children': [],
            }]
        }
        request = mock.Mock()
        request.survey_session.absolute_url.return_value = 'http://localhost'
        with mock.patch('euphorie.client.api.getTreeData', return_value=menu):
            context_menu = self.context_menu(request, 'context', 'phase', None)
            self.assertEqual(context_menu[0]['status'], None)

    def test_risk_status_postponed(self):
        menu = {
            'children': [{
                'id': 15,
                'type': 'risk',
                'class': 'postponed',
                'leaf_module': True,
                'path': '/1',
                'current_parent': False,
                'url': '/1',
                'children': [],
            }]
        }
        request = mock.Mock()
        request.survey_session.absolute_url.return_value = 'http://localhost'
        with mock.patch('euphorie.client.api.getTreeData', return_value=menu):
            context_menu = self.context_menu(request, 'context', 'phase', None)
            self.assertEqual(context_menu[0]['status'], 'postponed')

    def test_risk_status_risk_present(self):
        menu = {
            'children': [{
                'id': 15,
                'type': 'risk',
                'class': 'answered risk',
                'leaf_module': True,
                'path': '/1',
                'current_parent': False,
                'url': '/1',
                'children': [],
            }]
        }
        request = mock.Mock()
        request.survey_session.absolute_url.return_value = 'http://localhost'
        with mock.patch('euphorie.client.api.getTreeData', return_value=menu):
            context_menu = self.context_menu(request, 'context', 'phase', None)
            self.assertEqual(context_menu[0]['status'], 'present')

    def test_risk_status_risk_not_present(self):
        menu = {
            'children': [{
                'id': 15,
                'type': 'risk',
                'class': 'current answered',
                'leaf_module': True,
                'path': '/1',
                'current_parent': False,
                'url': '/1',
                'children': [],
            }]
        }
        request = mock.Mock()
        request.survey_session.absolute_url.return_value = 'http://localhost'
        with mock.patch('euphorie.client.api.getTreeData', return_value=menu):
            context_menu = self.context_menu(request, 'context', 'phase', None)
            self.assertEqual(context_menu[0]['status'], 'not-present')

    def test_risk_status_risk_seen(self):
        menu = {
            'children': [{
                'id': 15,
                'type': 'risk',
                'class': 'current',
                'leaf_module': True,
                'path': '/1',
                'current_parent': False,
                'url': '/1',
                'children': [],
            }]
        }
        request = mock.Mock()
        request.survey_session.absolute_url.return_value = 'http://localhost'
        with mock.patch('euphorie.client.api.getTreeData', return_value=menu):
            context_menu = self.context_menu(request, 'context', 'phase', None)
            self.assertEqual(context_menu[0]['status'], None)
