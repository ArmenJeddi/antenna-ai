import streamlit as st
import requests
import time
import os
# from dotenv import load_dotenv

# Load AssemblyAI API key from .env file
# load_dotenv()
ASSEMBLYAI_API_KEY = 'db5168b8919646a4b2e130f2eee1e7a5'

# Function to upload audio file to AssemblyAI and get transcription
def transcribe_audio(file):
    base_url = "https://api.assemblyai.com/v2"

    headers = {
        "authorization": ASSEMBLYAI_API_KEY 
    }

    # with open(file , "rb") as f:
    response = requests.post(base_url + "/upload",
        headers=headers,
        data=file
    )

    upload_url = response.json()["upload_url"]

    data = {
        "audio_url": upload_url # You can also use a URL to an audio or video file on the web
    }

    url = base_url + "/transcript"
    response = requests.post(url, json=data, headers=headers)

    transcript_id = response.json()['id']
    polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

    while True:
        transcription_result = requests.get(polling_endpoint, headers=headers).json()

        if transcription_result['status'] == 'completed':
            return transcription_result['text']

        elif transcription_result['status'] == 'error':
            raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

        else:
            time.sleep(3)
    


# Streamlit app layout
st.title("Audio to Text Transcription App")
st.write("Upload an audio file, and we'll transcribe it for you using AssemblyAI.")

# File uploader
uploaded_file = st.file_uploader("Choose an audio file...", type=["wav", "mp3", "m4a"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')
    if st.button("Transcribe"):
        with st.spinner("Transcribing..."):
            transcription = transcribe_audio(uploaded_file)
            st.write("Transcription:")
            st.write(transcription)
