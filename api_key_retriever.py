import dotenv
import os


def get_api_key(api_key_name):
    dotenv.load_dotenv()
    api_key = os.getenv(api_key_name)
    return api_key

 