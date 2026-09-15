import os
from dotenv import load_dotenv

load_dotenv()

print("API environment loaded.")

if os.getenv("FEATHERLESS_API_KEY"):
    print("Featherless API key detected.")
else:
    print("Featherless API key not configured yet.")