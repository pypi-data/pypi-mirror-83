"""This file contains all the test for the models file.

Classes:
    TestGetCurrentDomain: Test get_current_site function.
    TestGetCurrentUser: Test get_current_user function.
    TestAuditModel: Test AuditModel.
"""
import logging
import traceback

from django.test import TestCase
from mock import Mock, patch
from testfixtures import LogCapture

from eox_audit_model.constants import LOG_FORMAT, Status
from eox_audit_model.exceptions import EoxAuditModelInvalidMethod, EoxAuditModelInvalidParameters
from eox_audit_model.models import AuditModel, AuditNote, get_current_ip, get_current_performer, get_current_site

LOG = logging.getLogger(__name__)


class TestGetCurrentSite(TestCase):
    """Test cases for get_current_site."""

    @patch('eox_audit_model.models.get_current_request')
    def test_valid_request(self, get_current_request_mock):
        """This method tests when the request is valid and has the value
        'HTTP_HOST' in the META field.

        Expected behavior:
            - Return expected value.
            - get_current_request is called once.
        """
        request = Mock()
        expected_value = 'https://howgarts.com'
        request.META = {
            'HTTP_HOST': expected_value,
        }
        get_current_request_mock.return_value = request

        result = get_current_site()

        self.assertEqual(expected_value, result.domain)
        get_current_request_mock.assert_called_once()

    @patch('eox_audit_model.models.get_current_request')
    def test_invalid_request(self, get_current_request_mock):
        """This method tests when the request is None.

        Expected behavior:
            - Return expected value.
            - get_current_request is called once.
        """
        get_current_request_mock.return_value = None
        expected_value = 'Missing domain.'

        result = get_current_site()

        self.assertEqual(expected_value, result.domain)
        get_current_request_mock.assert_called_once()


class TestGetCurrentIp(TestCase):
    """Test cases for get_current_site."""

    @patch('eox_audit_model.models.get_ip')
    @patch('eox_audit_model.models.get_current_request')
    def test_valid_request(self, get_current_request_mock, get_ip_mock):
        """This method tests when the request is not None.

        Expected behavior:
            - Return expected value.
            - get_current_request is called once.
            - get_ip is called once.
        """
        request = Mock()
        expected_value = '192.163.45.67'
        get_ip_mock.return_value = expected_value
        get_current_request_mock.return_value = request

        result = get_current_ip()

        self.assertEqual(expected_value, result)
        get_current_request_mock.assert_called_once()
        get_ip_mock.assert_called_once_with(request)

    @patch('eox_audit_model.models.get_ip')
    @patch('eox_audit_model.models.get_current_request')
    def test_invalid_request(self, get_current_request_mock, get_ip_mock):
        """This method tests when the request is None.

        Expected behavior:
            - Return expected value.
            - get_current_request is called once.
            - get_ip is not called.
        """
        get_current_request_mock.return_value = None
        expected_value = 'Missing ip.'

        result = get_current_ip()

        self.assertEqual(expected_value, result)
        get_current_request_mock.assert_called_once()
        get_ip_mock.assert_not_called()


class TestGetCurrentPerformer(TestCase):
    """Test cases for get_current_performer."""

    @patch('eox_audit_model.models.get_current_user')
    def test_valid_user(self, get_current_user_mock):
        """This method tests when the user is valid.

        Expected behavior:
            - Return expected value.
            - get_current_user is called once.
        """
        user = Mock()
        expected_value = 'HarryPotter'
        user.username = expected_value
        get_current_user_mock.return_value = user

        result = get_current_performer()

        self.assertEqual(expected_value, result)
        get_current_user_mock.assert_called_once()

    @patch('eox_audit_model.models.get_current_user')
    def test_invalid_user(self, get_current_user_mock):
        """This method tests when the request is None.

        Expected behavior:
            - Return expected value.
            - get_current_user is called once.
        """
        get_current_user_mock.return_value = None
        expected_value = 'Missing user.'

        result = get_current_performer()

        self.assertEqual(expected_value, result)
        get_current_user_mock.assert_called_once()


class TestAuditModel(TestCase):
    """Test cases for the model AuditModel."""

    def setUp(self):
        """Setup common conditions for every test case"""
        def valid_method(a, b, c, d):
            """Execute a mathematic operation."""
            LOG.info('This is an info message')
            return (a + b + c) / d

        self.valid_method = valid_method

    def test_invalid_method(self):
        """Test for execute_action class method, when the given method is invalid.

        Expected behavior:
            - Raise EoxAuditModelInvalidMethod exception.
        """
        action = 'Test action.'
        method = 'Invalid method.'
        parameters = {}

        with self.assertRaises(EoxAuditModelInvalidMethod):
            AuditModel.execute_action(action, method, parameters)

    def test_invalid_parameters(self):
        """Test for execute_action class method, when the parameter are invalid.

        Expected behavior:
            - Raise EoxAuditModelInvalidMethod exception.
        """
        action = 'Test action.'
        method = self.valid_method
        parameters = 'This should be a dict.'

        with self.assertRaises(EoxAuditModelInvalidParameters):
            AuditModel.execute_action(action, method, parameters)

    @patch.object(AuditModel.objects, 'create')
    def test_valid_method(self, create_mock):
        """Test for execute_action class method, when the method is executed successfully.

        Expected behavior:
            - Return expected value.
            - cls.objects.create is called with the right parameters.
        """
        action = 'Test action.'
        method = self.valid_method
        expected_value = 6
        parameters = {
            'args': (1, 2),
            'kwargs': {'c': 3, 'd': 1},
        }

        with LogCapture() as test_logs:
            result = AuditModel.execute_action(action, method, parameters)

        test_logs.setFormatter(logging.Formatter(LOG_FORMAT))
        logs = [test_logs.format(record) for record in test_logs.records]
        self.assertEqual(expected_value, result)
        create_mock.assert_called_once_with(
            action=action,
            status=Status.SUCCESS,
            method_name=method.__name__,
            captured_logs='\n'.join(logs),
            traceback_log=traceback.format_exc(),
            input_parameters=parameters,
            output_parameters=str(method(1, 2, 3, 1)),
        )

    @patch('eox_audit_model.models.traceback')
    @patch.object(AuditModel.objects, 'create')
    def test_method_raise_exception(self, create_mock, traceback_mock):
        """Test for execute_action class method, when the method raises an exception.

        Expected behavior:
            - Return expected value.
            - cls.objects.create is called with the right parameters.
            - traceback.format_exc() is called.
        """
        action = 'Test action.'
        method = self.valid_method
        traceback_mock.format_exc.return_value = 'Test traceback.'
        parameters = {
            'args': (1, 2),
            'kwargs': {'c': 3, 'd': 0},
        }

        with LogCapture() as test_logs:
            with self.assertRaises(Exception):
                AuditModel.execute_action(action, method, parameters)

        test_logs.setFormatter(logging.Formatter(LOG_FORMAT))
        logs = [test_logs.format(record) for record in test_logs.records]
        traceback_mock.format_exc.assert_called_once()
        create_mock.assert_called_once_with(
            action=action,
            status=Status.FAIL,
            method_name=method.__name__,
            captured_logs='\n'.join(logs),
            traceback_log=traceback_mock.format_exc(),
            input_parameters=parameters,
            output_parameters={}.__repr__(),
        )

    @patch.object(AuditNote.objects, 'create')
    @patch.object(AuditModel.objects, 'create')
    def test_notes(self, create_audit_mock, create_note_mock):
        """Test for execute_action class method, when notes parameter is not None.

        Expected behavior:
            - AuditNote.objects.create is called with the right parameters.
        """
        action = 'Test action.'
        method = self.valid_method
        parameters = {
            'args': (1, 2),
            'kwargs': {'c': 3, 'd': 1},
        }
        notes = [
            {
                'title': 'AuditNote',
                'description': 'this description is store in the audit note model.',
            },
        ]

        AuditModel.execute_action(action, method, parameters, notes)

        create_note_mock.assert_called_once_with(
            audit_register=create_audit_mock(),
            title='AuditNote',
            description='this description is store in the audit note model.',
        )
