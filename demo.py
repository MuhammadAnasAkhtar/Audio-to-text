import openai
import os
from dotenv import load_dotenv


load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
audio_file=open("Recordings.mp3","rb")
#output= openai.Audio.translate("whisper-1", audio_file)
#output = openai.Audio.translations.create(model="whisper-1", file=audio_file)
output = openai.audio.transcriptions.create(model="whisper-1", file=audio_file)

print(output)