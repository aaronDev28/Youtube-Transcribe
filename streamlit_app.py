import streamlit as st
from langchain.document_loaders import YoutubeLoader
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(page_title="YouTube Transcription App")

st.title('📽️ YouTube Transcriber')

#Getting the YT video's URL
youtube_url = st.text_input('Enter YouTube Video URL', '')

# Getting the YT video's ID
def extract_youtubeID(inputURL):
  processedURL = []
  if inputURL.startswith('https://www.youtube.com') or inputURL.startswith('https://youtube.com'):
    inputURL_split = inputURL.split('=')[-1]
    processedURL.append(inputURL_split)
  if inputURL.startswith('https://youtu.be/'):
    inputURL_split = inputURL.split('/')[-1]
    processedURL.append(inputURL_split)
  return processedURL

# Getting the YT video's Thumbnail Picture
def get_thumbnail(input_id):
  return st.image(f'http://i.ytimg.com/vi/{input_id[0]}/maxresdefault.jpg', width=350)

# Retrieve the YT video's transcription
def getTranscription(input_id):
  inputURL = f'https://www.youtube.com/watch?v={input_id[0]}'
  loaderObj = YoutubeLoader.from_youtube_url(inputURL , add_video_info=False)
  loadResult = loaderObj.load()
  ytText = loadResult[0].page_content
  return st.write(ytText)
  
# Interface
if youtube_url == '':
  st.warning('👆 Please enter a YouTube video URL to get started!')
  with st.expander('See example URL'):
    st.code('https://www.youtube.com/watch?v=TX9qSaGXFyg')
    st.code('https://www.youtube.com/watch?v=I3cjbB38Z4A')
else: 
  ## Display YouTube thumbnail image
  youtubeID = extract_youtubeID(youtube_url)
  get_thumbnail(youtubeID)
  
  ## Display transcription
  with st.expander('See Video Transcript'):
    getTranscription(youtubeID)
