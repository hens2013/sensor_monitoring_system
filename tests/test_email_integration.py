import pytest
from unittest.mock import patch
from http import HTTPStatus
from smtplib import SMTPAuthenticationError, SMTPServerDisconnected, SMTPException

from email_intergration.email_sender import EmailSender
from config.environment_vars import EMAIL, PASSWORD


class TestEmailSender:

    @pytest.fixture
    def email_sender(self):
        # This fixture creates an instance of EmailSender with the given EMAIL and PASSWORD.
        return EmailSender(EMAIL, PASSWORD)

    def test_send_email_success(self, email_sender):
        # This test simulates successful email sending.
        with patch('smtplib.SMTP') as mock_smtp:
            smtp_instance = mock_smtp.return_value
            smtp_instance.send_message.return_value = None

            # Calling send_email and expecting HTTPStatus.OK as the response for successful sending.
            response = email_sender.send_email("receiver@example.com", "Test Subject", "Test Body")
            assert response == HTTPStatus.OK

    def test_send_email_auth_error(self, email_sender):
        # This test checks the handling of an authentication error during email sending.
        with patch('smtplib.SMTP') as mock_smtp:
            smtp_instance = mock_smtp.return_value
            smtp_instance.login.side_effect = SMTPAuthenticationError(535, 'Authentication failed')

            # Expecting HTTPStatus.UNAUTHORIZED when there's an authentication error.
            response = email_sender.send_email("receiver@example.com", "Test Subject", "Test Body")
            assert response == HTTPStatus.UNAUTHORIZED

    def test_send_email_server_disconnected(self, email_sender):
        # This test simulates a scenario where the SMTP server is disconnected.
        with patch('smtplib.SMTP') as mock_smtp:
            smtp_instance = mock_smtp.return_value
            smtp_instance.login.side_effect = SMTPServerDisconnected()

            # Expecting HTTPStatus.SERVICE_UNAVAILABLE on server disconnection.
            response = email_sender.send_email("receiver@example.com", "Test Subject", "Test Body")
            assert response == HTTPStatus.SERVICE_UNAVAILABLE

    def test_send_email_smtp_exception(self, email_sender):
        # This test handles general SMTP exceptions during email sending.
        with patch('smtplib.SMTP') as mock_smtp:
            smtp_instance = mock_smtp.return_value
            smtp_instance.send_message.side_effect = SMTPException()

            # Expecting HTTPStatus.BAD_REQUEST on SMTP exceptions.
            response = email_sender.send_email("receiver@example.com", "Test Subject", "Test Body")
            assert response == HTTPStatus.BAD_REQUEST
