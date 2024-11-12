import openai 
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import time  # To generate unique filenames


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static"


@app.route('/', methods=['GET', 'POST'])
def main():
    translated_text = ""  # Initialize translated_text with an empty string
    if request.method == "POST":
        language = request.form["language"]
        file = request.files.get("file")
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            
            
  # Transcription with Whisper
            try:
                with open(file_path, "rb") as audio_file:
                    transcript = openai.Audio.transcribe(model="whisper-1", file=audio_file)
                print("Transcription Result:", transcript["text"])  # Print for debugging
            except Exception as e:
                print(f"Error during transcription: {str(e)}")
                transcript = {"text": "Error during transcription."}  # Handle any transcription errors
            
            # Translate the transcribed text with GPT-4
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{
                    "role": "system", 
                    "content": f"You are a professional translator. Translate the following English text into {language} exactly, word-for-word. Do not summarize, paraphrase, or alter the structure. The goal is to keep the meaning and context of the text exactly the same."
                }, 
                {
                    "role": "user", 
                    "content": transcript["text"]
                }],
                temperature=0,
                max_tokens=256
            )
            
            translated_text = response["choices"][0]["message"]["content"]
            print("GPT-4 Output:", translated_text)  # Print for debugging

    return render_template("index.html", translated_text=translated_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)