import os
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

import streamlit as st
import openai
from streamlit_webrtc import webrtc_streamer
import numpy as np
import tempfile
from pydub import AudioSegment
from gtts import gTTS

# Setting up the OpenAI API client
def setup_openai_client(api_key):
    openai.api_key = api_key

# Transcribing the audio file using OpenAI Whisper model
def transcribe_audio(audio_file):
    with open(audio_file, "rb") as file:
        transcript = openai.Audio.transcribe("whisper-1", file)
    return transcript['text']

# Generating a response using GPT-3.5-turbo model
def fetch_ai_response(input_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": input_text}]
    )
    return response['choices'][0]['message']['content']

# Converting text to audio file using gTTS
def text_to_audio(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

def main():
    st.set_page_config(page_title="Audio Recorder and Transcription App", page_icon="🎙️")

    # Sidebar for OpenAI API key input
    st.sidebar.title("API Key Configuration")
    api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

    if api_key:
        setup_openai_client(api_key)

        st.title("Audio Recorder and Transcription App")

        # Audio recorder component
        webrtc_ctx = webrtc_streamer(
            key="speech-to-text",
            audio_receiver_size=1024,
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={"video": False, "audio": True},
        )

        if webrtc_ctx.audio_receiver:
            if st.button("Stop Recording and Transcribe"):
                st.info("Processing audio...")
                sound_chunk = []
                try:
                    while True:
                        audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
                        for audio_frame in audio_frames:
                            sound = audio_frame.to_ndarray()
                            sound_chunk.extend(sound.flatten())
                except:
                    pass

                if len(sound_chunk) > 0:
                    audio_segment = AudioSegment(
                        np.array(sound_chunk).tobytes(),
                        frame_rate=48000,
                        sample_width=2,
                        channels=1
                    )

                    # Create a temporary audio file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
                        audio_segment.export(fp.name, format="wav")
                        audio_file = fp.name

                    # Transcribe the audio file
                    transcript = transcribe_audio(audio_file)
                    st.write("Transcript:")
                    st.write(transcript)

                    # Generate AI response
                    ai_response = fetch_ai_response(transcript)
                    st.write("AI Response:")
                    st.write(ai_response)

                    # Convert AI response to audio
                    response_audio_file = text_to_audio(ai_response)
                    st.audio(response_audio_file, format='audio/mp3')

                    # Clean up temporary files
                    os.unlink(audio_file)
                    os.unlink(response_audio_file)
                else:
                    st.error("No audio recorded. Please check your microphone and try again.")

    else:
        st.warning("Please enter your OpenAI API key.")

if __name__ == "__main__":
    main()
