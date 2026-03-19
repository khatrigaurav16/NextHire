
import os
from dotenv import load_dotenv

# Load your .env file
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# List available models
print("📋 Available Gemini models for your API key:\n")
for model in genai.list_models():
    # Filter only models that support text generation
    if "generateContent" in model.supported_generation_methods:
        print("✅", model.name)
