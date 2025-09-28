import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load the API key from your .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("--- Available Models for 'generateContent' ---")

# List all models and check if they support the 'generateContent' method
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

print("---------------------------------------------")