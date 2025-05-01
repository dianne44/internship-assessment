import os
from pydub import AudioSegment
import requests

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwYXRyaWNrY21kIiwiYWNjb3VudF90eXBlIjoiRnJlZSIsImV4cCI6NDg2OTE4NjUzOX0.wcFG_GjBSNVZCpP4NPC2xk6Dio8Jdd8vMb8e_rzXOFc"

# Supported languages and their codes
language_codes = {
    "English": "eng",
    "Luganda": "lug",
    "Runyankole": "nyn",
    "Acholi": "ach",
    "Ateso": "teo",
    "Lugbara": "lgg"
}

# Get audio file path from user
audio_path = input("Please enter audio file path").strip()

# Check if file exists
if not os.path.isfile(audio_path):
    print("Invalid file path.")
    exit()

# Load audio and check duration
try:
    audio = AudioSegment.from_file(audio_path)
except Exception as e:
    print("Failed to load audio:", e)
    exit()

duration_seconds = len(audio) / 1000
if duration_seconds > 300:
    print("Audio is longer than 5 minutes. Please provide a shorter file.")
    exit()

# Ask for target language
print("Please choose the target language:", ", ".join(language_codes.keys()))
target_lang = input().strip()

if target_lang not in language_codes:
    print("Unsupported language selected.")
    exit()

# Prepare the API request
url = "https://api.sunbird.ai/tasks/stt"  
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}
files = {
   
    "audio": ("sample.mp3", open(audio_path, "rb"), "audio/mpeg")

}
data = {
    "language": language_codes[target_lang]
}

# Send the transcription request
print(f"Transcribing audio in {target_lang.lower()}... Please wait.")

response = requests.post(url, headers=headers, files=files, data=data)


if response.status_code == 200:
    result = response.json()
    #print("Raw response:", result)

    transcription = result.get("audio_transcription", "")
    if transcription:
        print(f"Audio transcription text in {target_lang.lower()}:")
        print(transcription)
    else:
        print("No transcription text was returned.")
else:
    print("Transcription failed. Status code:", response.status_code)
    print("Details:", response.text)
