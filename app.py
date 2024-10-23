import streamlit as st
import os
from audio_recorder_streamlit import audio_recorder
import base64
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from api import transcribe_audio, text_to_speech
from pdf_processor import get_pdf_text, get_text_chunks, get_vectorstore
from htmlTemplates import css, bot_template, user_template

# Path to the folder containing PDF files
PDF_FOLDER = "pdf"

# Function to retrieve PDF files from the folder
def get_pdf_files():
    pdf_files = []
    for file in os.listdir(PDF_FOLDER):
        if file.endswith(".pdf"):
            pdf_files.append(os.path.join(PDF_FOLDER, file))
    return pdf_files

# Function to create a conversation chain with a vectorstore
def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()  # Using the OpenAI chat model
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

# Function to automatically play audio in the browser
def auto_play_audio(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)

# Main function to run the Streamlit app
def main():
    st.set_page_config(page_title="Multi-PDF Chat with Voice", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    
    st.title("Multi-PDF Chat with Voice Interaction")

    # Automatic PDF processing
    if "conversation" not in st.session_state:
        with st.spinner("Processing PDFs..."):
            pdf_files = get_pdf_files()
            if pdf_files:
                raw_text = get_pdf_text(pdf_files)  # Extract text from the PDFs
                text_chunks = get_text_chunks(raw_text)  # Break the text into chunks
                vectorstore = get_vectorstore(text_chunks)  # Create a vectorstore
                st.session_state.conversation = get_conversation_chain(vectorstore)
                st.success(f"Processed {len(pdf_files)} PDF files successfully!")
            else:
                st.error(f"No PDF files found in the {PDF_FOLDER} folder.")
                return

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Voice input section
    st.subheader("Ask a question (Voice or Text)")
    audio_bytes = audio_recorder()  # Record audio input
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_bytes)  # Save the recorded audio to a file
        user_question = transcribe_audio("temp_audio.wav")  # Transcribe the audio to text
        st.text(f"You asked: {user_question}")
    else:
        user_question = st.text_input("Or type your question here:")  # Allow user to input text

    if user_question:
        handle_user_input(user_question)  # Handle the user's question input

# Function to handle user input and AI response
def handle_user_input(user_question):
    if st.session_state.conversation is not None:
        response = st.session_state.conversation({'question': user_question})  # Get AI response
        st.session_state.chat_history = response['chat_history']

        # Display conversation history
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)  # Display user message
            else:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)  # Display bot response
                # Convert AI response to speech
                text_to_speech(message.content, "ai_response.mp3")
                st.audio("ai_response.mp3")
                auto_play_audio("ai_response.mp3")  # Automatically play the AI response as audio
    else:
        st.warning("Conversation not initialized. Please try refreshing the page.")

if __name__ == "__main__":
    main()
