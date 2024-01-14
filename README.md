# OpenSpeech Text to Speech
### A Text to Speech (TTS) web application using openai api that you can self host.
OpenSpeech is a self-hostable Python-based web application that uses OpenAI's text-to-speech capabilities to convert text into speech. The application is built with Flask, a lightweight web framework for Python.
Use your own openai api key and convert your text content to awesome spoken mp3 files.

#### Key Features
- Open Source
- Docker Compatible
- Supports light/dark themes
- Filter different voices and quality levels supported by openai
- Displays estimated cost to convert the text to speech
- Overcomes openai 4096 character limit by splitting the text to chunks, generating separate audio files for each chunks and combining the final output into a single file.

#### Installation and Usage
##### Docker
- The easiest way to run the application is using docker. Refer to the `docker-compose.yaml` file. Create a copy of the file in your system.
	- update the port on the left-hand side if you would like to run the application over a different port other than the default one: 3210
	- update the path to files directory. this is where the input text and output mp3 will be stored.
	Run the compose file by:
	```
	docker-compose up -d
	```
- The application will start a local server and will be accessible on `http://127.0.0.1:3210/` or `http://localhost:3210/`
	- update the ip to the ip of the server where the container is running
	- update the port if you changed the value in the docker-compose file.
- Open this URL in your web browser to use the application.
##### Clone the repo and execute the Python app
1. Clone the repo
```
git clone https://github.com/binuengoor/OpenSpeech.git
```
2. Navigate to the main directory
```
cd OpenSpeech
```
3. install python dependencies
```
pip install -r requirements.txt
```
4. To run the application, run the `app.py` file:
```
python app.py
```
The application will start a local server and will be accessible on `http://127.0.0.1:3210/` or `http://localhost:3210/`
Open this URL in your web browser to use the application.

#### Attributions
- Python script I came across while browsing reddit
- water.css
- fontawesome
- Github Copilot
- Chatgpt

<a href="https://www.buymeacoffee.com/binuengoor" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

---
#### Contributing
- Contributions are welcome! I am not a trained programmer. I put this together with the help of ai. So any help to make the application better or cleaner is welcome.

#### License
This project is licensed under the terms of the MIT license.

(c) Binu Pradeep 2024
