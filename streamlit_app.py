import streamlit as st
import requests

# Set up Streamlit page
st.set_page_config(page_title="YouTube Transcriber and Summarizer")
st.title('📽️ YouTube Transcriber and Summarizer')

# YouTube video transcription functions
from langchain.document_loaders import YoutubeLoader
from streamlit_extras.add_vertical_space import add_vertical_space

def extract_youtubeID(inputURL):
    processedURL = []
    if inputURL.startswith('https://www.youtube.com') or inputURL.startswith('https://youtube.com'):
        inputURL_split = inputURL.split('=')[-1]
        processedURL.append(inputURL_split)
    if inputURL.startswith('https://youtu.be/'):
        inputURL_split = inputURL.split('/')[-1]
        processedURL.append(inputURL_split)
    return processedURL

def get_thumbnail(input_id):
    return st.image(f'http://i.ytimg.com/vi/{input_id[0]}/maxresdefault.jpg', width=350)

def getTranscription(input_id):
    inputURL = f'https://www.youtube.com/watch?v={input_id[0]}'
    loaderObj = YoutubeLoader.from_youtube_url(inputURL , add_video_info=False)
    loadResult = loaderObj.load()
    ytText = loadResult[0].page_content
    return ytText

# Hugging Face API functions
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": st.secrets["bearer"]}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Streamlit app interface
youtube_url = st.text_input('Enter YouTube Video URL', '')

if youtube_url == '':
    st.warning('👆 Please enter a YouTube video URL to get started!')
    with st.expander('See example URL'):
        st.code('https://www.youtube.com/watch?v=TX9qSaGXFyg')
        st.code('https://www.youtube.com/watch?v=I3cjbB38Z4A')
else:
    # Display YouTube thumbnail image
    youtubeID = extract_youtubeID(youtube_url)
    get_thumbnail(youtubeID)

    # Display transcription
    with st.expander('See Video Transcript'):
        ytText = getTranscription(youtubeID)
        st.write(ytText)

    # Summarize transcription
    summarized_output = query({"inputs": ytText})
    summary_text = summarized_output[0]['summary_text']
    
    with st.expander('See Summarized Transcript'):
        st.write(summary_text)
