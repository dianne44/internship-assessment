import os
import requests


ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwYXRyaWNrY21kIiwiYWNjb3VudF90eXBlIjoiRnJlZSIsImV4cCI6NDg2OTE4NjUzOX0.wcFG_GjBSNVZCpP4NPC2xk6Dio8Jdd8vMb8e_rzXOFc"

# List of supported languages and their codes
language_codes = {
    "English": "eng",
    "Luganda": "lug",
    "Runyankole": "nyn",
    "Acholi": "ach",
    "Ateso": "teo",
    "Lugbara": "lgg"
}

# Prompt user for input
print("Please choose the source language:", ", ".join(language_codes.keys()))
source_lang = input().strip()

print("Please choose the target language (cannot be the same as source):", ", ".join(language_codes.keys()))
target_lang = input().strip()

if source_lang == target_lang:
    print("Source and target languages must be different.")
    exit()

if source_lang not in language_codes or target_lang not in language_codes:
    print("Unsupported language selected.")
    exit()

print("Enter the text to translate:")
text = input().strip()

# Prepare the API request
url = "https://api.sunbird.ai/tasks/nllb_translate"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
}
data = {
    "source_language": language_codes[source_lang],
    "target_language": language_codes[target_lang],
    "text": text
}

# Send the request
response = requests.post(url, headers=headers, json=data)

# Display the result
if response.status_code == 200:
    translated = response.json()["output"]["translated_text"]
    #print("Raw response JSON:", response.json())

    print("Translation:", translated)
else:
    print("Translation failed. Status code:", response.status_code)
    print("Details:", response.text)
