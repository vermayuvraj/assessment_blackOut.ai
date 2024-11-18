from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

SERP_API_KEY = os.getenv("SERP_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LLM_API_KEY = os.getenv("LLM_API_KEY")
