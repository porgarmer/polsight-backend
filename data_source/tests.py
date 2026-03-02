from django.test import TestCase
from pathlib import Path
import os
from dotenv import load_dotenv


# Create your tests here.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR/".env")

PRODUCTION = os.getenv(key="PRODUCTION", default="")

print(PRODUCTION)