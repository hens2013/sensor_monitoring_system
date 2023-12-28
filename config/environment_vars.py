from dotenv import find_dotenv, load_dotenv
import os

# find .env path file in the project
env_path_file = find_dotenv()

load_dotenv(env_path_file)

SLACK_TOKEN = os.getenv("SLACK_TOEKN")
SERVER_HOST = os.getenv("SERVER_HOST")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
URL = os.getenv("URL")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
