from slack_integration.slack import SlackAlerter
from config.environment_vars import SLACK_TOKEN


class TestSlackAlerter:
    """
    test for slack integration, includes two tests, one of sending message success
    two sending message to invalid token
    """

    # Test for successful message posting
    def test_post_message_success(self):
        slack_alerter = SlackAlerter('test', SLACK_TOKEN)
        response = slack_alerter.post_message('Test message')
        assert response['ok'] == True

    # Test for message posting message failure
    def test_post_message_failure(self):
        slack_alerter = SlackAlerter('test', 'fake_token')
        response = slack_alerter.post_message('Fake message')
        assert response is None
