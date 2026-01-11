import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

models = genai.list_models()
print("Modelos disponibles en esta cuenta:")
for m in models:
    print("-", m.name)