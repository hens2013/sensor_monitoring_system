from pydantic import BaseModel
from http import HTTPStatus
from config.environment_vars import SLACK_TOKEN, EMAIL, PASSWORD, EMAIL_RECEIVER
from email_intergration.email_sender import EmailSender
from slack_integration.slack import SlackAlerter
from .logger_config import setup_logger
from fastapi import FastAPI, HTTPException

"""
The following code is an alert service, that receives message from the main
service and pass the message via slack or email
"""

local_logger = setup_logger(__name__)
app = FastAPI(debug=True)


class MessagePayload(BaseModel):
    message: str


@app.post("/message")
def read_message(request: MessagePayload):
    """
    Endpoint to read a message and send it via Slack or Email.
    """
    message = request.message
    if not message:
        # Raising an exception if the message is empty or invalid
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid message.")

    local_logger.info('-' * 100)
    local_logger.info(message)

    # Attempt to send the message through Slack, and if it fails, try email
    if send_message_slack(message) or send_message_email(message):
        return {"status": "success", "message": "Message sent"}, HTTPStatus.OK

    # If both Slack and Email sending fail, raise an exception
    raise HTTPException(status_code=HTTPStatus.EXPECTATION_FAILED, detail="Failed to send message")


def send_message_slack(message: str) -> bool:
    """
    Function to send a message via Slack.
    Returns True if successful, False otherwise.
    """
    try:
        slack = SlackAlerter('test', SLACK_TOKEN)
        return slack.post_message(message)
    except Exception as e:
        local_logger.error(f"Slack sending error: {e}")
        return False


def send_message_email(message: str) -> bool:
    """
    Function to send a message via Email.
    Returns True if successful, False otherwise.
    """
    try:
        email_obj = EmailSender(EMAIL, PASSWORD)
        subject = 'Sensor Notification'
        email_response = email_obj.send_email(receiver_email=EMAIL_RECEIVER, subject=subject, body=message)
        return email_response == HTTPStatus.OK
    except Exception as e:
        local_logger.error(f"Email sending error: {e}")
        return False
