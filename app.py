import os
import shutil
from flask import Flask, request, render_template, send_file, flash, Response
from pathlib import Path
from pydub import AudioSegment
from openai import OpenAI
from tqdm import tqdm
from datetime import datetime

if not os.path.exists('files'):
    os.makedirs('files')

app = Flask(__name__)
app.secret_key = '0ebe33610f95d4a34c64cf66de33c9026c8a5f71bed4774f2d10ececaf83a2f3'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        api_key = request.form.get('api_key')
        text = request.form.get('text')
        voice = request.form.get('voice')
        model = request.form.get('model')
        client = OpenAI(api_key=api_key)

        # Save the text to 'input_text.txt'
        with open('files/input_text.txt', 'w') as f:
            f.write(text)
            
        # Path to the text file
        text_file_path = Path(__file__).parent / "files/input_text.txt"

        # Path for the output audio file
        speech_file_path = Path(__file__).parent / "files/output.mp3"

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
        with open(speech_file_path, "wb") as f:
            combined_audio.export(f, format="mp3")

        return """
        <head>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/kognise/water.css@latest/dist/dark.min.css">
        </head>
        <body>
            <h2>Conversion Completed!</h2><br>
            <a href="/download" download>
                <button>Download Output File</button>
            </a><br>
            <a href="/">
                <button>Go Back</button>
            </a>
        </body>
        """
    return render_template('index.html')  # A simple form for API key input

@app.route('/download')
def download_file():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f'output_{timestamp}.mp3'
    with open('output.mp3', 'rb') as f:
        data = f.read()
    response = Response(data, mimetype="audio/mpeg")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3210, debug=True)



