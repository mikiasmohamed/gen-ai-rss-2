from langchain.document_loaders import RSSFeedLoader
import streamlit as st
from langchain.llms import VertexAI
from google.oauth2.service_account import Credentials

# Load the credentials from Streamlit secrets
google_secrets = st.secrets["google"]
credentials = Credentials.from_service_account_info(google_secrets)

llm = VertexAI(model_name='text-bison@001', credentials=credentials)

st.header("RSS Feed Summaries")

user_input_url = st.text_input("Enter the RSS feed URL to get summaries of articles:", "https://www.bleepingcomputer.com/feed/")
st.markdown('')

params = {
    'temperature': 0.7,
    'top_p': 0.9,
}

if user_input_url:
    urls = [user_input_url]
    
    with st.spinner("Loading content..."):
        try:
        
            loader = RSSFeedLoader(urls=urls)
            data = loader.load()

            content = ""

            for item in data:
                content += f"### {item.metadata['title']}\n"
                prompt = f"Summarize the following article in about 3 to 4 lines:\n{item.page_content}"
                content += f" {llm(prompt, **params)}\n"                                    
            
            st.markdown(content)
        
        
        except Exception as e:
            st.error(f"Error fetching {user_input_url}, exception: {e}")
