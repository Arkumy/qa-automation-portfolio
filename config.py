import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL")
USERNAME = os.getenv("API_LOGIN")
PASSWORD = os.getenv("API_PASSWORD")