from langchain.document_loaders import RSSFeedLoader
import streamlit as st
from langchain.llms import VertexAI
import google.auth

credentials, project_id = google.auth.default()

llm = VertexAI(model_name='text-bison@001', credentials=credentials)

user_input_url = st.text_input("Enter the RSS feed URL:", "https://www.bleepingcomputer.com/feed/")
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
