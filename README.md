# Virtual_Assistant

This project enables a multi-PDF chat experience with voice interaction, allowing users to ask questions about the contents of multiple PDFs either via voice or text. The application uses OpenAI’s Whisper model to transcribe voice input and GPT-3.5-turbo to generate answers. Additionally, it features the ability to convert the AI’s response back to audio for a complete voice-driven interaction experience.

## Description

Virtual_Assistant allows users to interact with the content of multiple PDF documents using voice or text-based input. The application processes PDF files and lets users ask questions about their contents. Voice input is transcribed using OpenAI Whisper, and the answers are generated using GPT-3.5-turbo. The responses can also be converted back into audio, providing a fully interactive voice assistant experience.

## Features

- Voice-based or text-based question input.
- Transcription of voice input using OpenAI Whisper.
- AI-powered chat using OpenAI GPT-3.5-turbo.
- PDF document parsing and semantic search.
- Text-to-speech conversion for AI-generated responses.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/Virtual_Assistant.git
    cd Virtual_Assistant
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the project root and add your OpenAI API key:

    ```bash
    OPENAI_API_KEY=your_openai_api_key_here
    ```

5. **Run the application:**

    ```bash
    streamlit run app.py
    ```

## Usage

- The application automatically processes PDF files located in the `pdf` folder.
- You can ask questions about the PDFs using your voice or by typing text.
- The AI will generate responses, and the answers can be played as audio.

## Requirements

- Python 3.10+
- OpenAI API Key
- Streamlit
- `pydub`, `audio_recorder_streamlit`, `openai`, and other dependencies specified in the `requirements.txt`.

## Contributing

Feel free to fork the repository and submit pull requests for improvements or new features.


