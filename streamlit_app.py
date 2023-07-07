import streamlit as st
from langchain.document_loaders import YoutubeLoader
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(page_title="YouTube Transcription App")

st.title('📺 YouTube Transcription App')

# YouTube URL
yt_url = st.text_input('Enter YouTube video URL', '')

# Get YouTube video ID
def extract_yt_id(input_url):
  processed_url = []
  if input_url.startswith('https://www.youtube.com') or input_url.startswith('https://youtube.com'):
    input_url_split = input_url.split('=')[-1]
    processed_url.append(input_url_split)
  if input_url.startswith('https://youtu.be/'):
    input_url_split = input_url.split('/')[-1]
    processed_url.append(input_url_split)
  return processed_url

# Get YouTube thumbnail image
def get_yt_img(input_id):
  return st.image(f'http://i.ytimg.com/vi/{input_id[0]}/maxresdefault.jpg', width=350)

# Retrieve transcript from YouTube video
def get_transcript(input_id):
  input_url = f'https://www.youtube.com/watch?v={input_id[0]}'
  loader = YoutubeLoader.from_youtube_url(input_url , add_video_info=False)
  results = loader.load()
  yt_text = results[0].page_content
  return st.write(yt_text)
  
# Conditional display of content
if yt_url == '':
  st.warning('👆 Please enter a YouTube video URL to get started!')
  with st.expander('See example URL'):
    st.code('https://www.youtube.com/watch?v=TX9qSaGXFyg')
    st.code('https://www.youtube.com/watch?v=I3cjbB38Z4A')
else: 
  ## Display YouTube thumbnail image
  yt_id = extract_yt_id(yt_url)
  get_yt_img(yt_id)
  
  ## Display transcription
  with st.expander('See video transcript'):
    get_transcript(yt_id)
