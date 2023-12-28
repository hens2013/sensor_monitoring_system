from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackAlerter:
    """
    this class responsible for sending a message to a slack channel
    """

    def __init__(self, channel_id: str, token: str):
        self.channel_id = channel_id
        self.token = token

    def post_message(self, message: str):
        client = WebClient(self.token)
        response = None
        try:
            # Call the chat.postMessage method using the WebClient
            response = client.chat_postMessage(
                channel=self.channel_id,
                text=message
            )
            return response

        except SlackApiError as e:
            print(f"failed to deliver alert to slack channel: {e}")
            return response
