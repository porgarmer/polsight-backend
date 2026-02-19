from google import genai
from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR/".env")

#token = os.getenv(key="GITHUB_TOKEN", default="")
api_key = os.getenv(key="GEMINI_API_KEY", default="")


client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Explain how AI works in a few words",
)

print(response.text)