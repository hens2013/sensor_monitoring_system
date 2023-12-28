import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from http import HTTPStatus
from smtplib import SMTPException, SMTPAuthenticationError, SMTPServerDisconnected
from config.environment_vars import SERVER_HOST, EMAIL_RECEIVER


class EmailSender:
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, receiver_email, subject, body):
        try:
            # Set up the SMTP server for Outlook
            smtp_server = SERVER_HOST

            # Outlook works with port 587
            PORT = 587

            smtp = smtplib.SMTP(smtp_server, PORT)

            # Encrypt the connection
            smtp.starttls()

            # Login to the sender's email account
            smtp.login(self.sender_email, self.sender_password)

            # Create the email
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject

            # Attach the email body
            msg.attach(MIMEText(body, 'plain'))

            # Send the email
            smtp.send_message(msg)

            # Close the SMTP server
            smtp.quit()

            print("Email sent successfully")
            return HTTPStatus.OK  # Success status code

        except SMTPAuthenticationError:
            print("Authentication error. Please check your username and password.")
            return HTTPStatus.UNAUTHORIZED  # Unauthorized status code
        except SMTPServerDisconnected:
            print("Server unexpectedly disconnected")
            return HTTPStatus.SERVICE_UNAVAILABLE  # Service not available status code
        except SMTPException as e:
            print(f"SMTP error occurred: {str(e)}")
            return HTTPStatus.BAD_REQUEST  # SMTP error status code
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return HTTPStatus.INTERNAL_SERVER_ERROR  # Internal server
