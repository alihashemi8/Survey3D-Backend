import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key is not set in environment variables")
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.avalai.ir/v1"  # آدرس آوالای
    )
    return client
