import os
import shutil
from flask import Flask, request, render_template, send_file, flash, Response
from pathlib import Path
from pydub import AudioSegment
from openai import OpenAI
from tqdm import tqdm
from datetime import datetime

# Sicherstellen, dass der Ordner existiert
files_dir = Path(__file__).parent / "files"
if not files_dir.exists():
    os.makedirs(files_dir)

app = Flask(__name__)
app.secret_key = '0ebe33610f95d4a34c64cf66de33c9026c8a5f71bed4774f2d10ececaf83a2f3'

@app.route('/', methods=['GET', 'POST'])
def home():
    api_key = os.getenv('OPENAI_API_KEY', '')  # Hole den API-Schlüssel aus der Umgebungsvariablen
    if request.method == 'POST':
        api_key = request.form.get('api_key') or api_key
        text = request.form.get('text')
        voice = request.form.get('voice')
        model = request.form.get('model')
        client = OpenAI(api_key=api_key)

        # Save the text to 'input_text.txt'
        with open(files_dir / 'input_text.txt', 'w') as f:
            f.write(text)
            
        # Path to the text file
        text_file_path = files_dir / "input_text.txt"

        # Path for the output audio file
        speech_file_path = files_dir / "output.mp3"

        # Function to split text into chunks of max_size characters
        def split_text(text, max_size):
            for i in range(0, len(text), max_size):
                yield text[i:i + max_size]

        # Read the contents of the text file
        with open(text_file_path, "r") as file:
            text_content = file.read()

        # Split text into chunks
        chunks = list(split_text(text_content, 4096))

        # Temporary folder for intermediate audio files
        temp_folder = Path(__file__).parent / "temp_audio"
        temp_folder.mkdir(exist_ok=True)

        # Process each chunk
        combined_audio = None
        for i in tqdm(range(len(chunks)), desc="Processing Chunks"): # Use tqdm for the loading bar
            chunk = chunks[i]

            # Create speech audio from the text chunk
            response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=chunk)

            # Temporary file for this chunk
            temp_file = temp_folder / f"chunk_{i}.mp3"
            with open(temp_file, "wb") as f:
                f.write(response.content)

            # Read the audio file
            audio = AudioSegment.from_file(temp_file)

            # Combine audio
            combined_audio = audio if combined_audio is None else combined_audio + audio
        
        # Remove temporary files and folder
        for temp_file in tqdm(temp_folder.iterdir(), desc="Cleaning up"): # Also add tqdm here
            temp_file.unlink()
        temp_folder.rmdir()

        # Write the combined audio content to a file
        combined_audio.export(speech_file_path, format="mp3")

        return """
        <head>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/kognise/water.css@latest/dist/dark.min.css">
        </head>
