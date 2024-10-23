from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to transcribe audio file using OpenAI's Whisper model
def transcribe_audio(audio_file):
    with open(audio_file, "rb") as file:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=file)
    return transcript.text  # Return the transcribed text

# Function to convert text to speech using OpenAI's TTS model
def text_to_speech(text, output_file):
    response = client.audio.speech.create(
        model="tts-1",
        voice="echo",  # Specify the voice model
        input=text  # Text input to be converted to speech
    )
    # Save the speech output to a file
    response.stream_to_file(output_file)
