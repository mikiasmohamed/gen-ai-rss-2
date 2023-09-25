from langchain.document_loaders import RSSFeedLoader
import streamlit as st
from langchain.llms import VertexAI
from google.oauth2.service_account import Credentials
import validators
import logging

st.write(st.config.get_option("server.enableCORS"))

def load_credentials():
    try:
        google_secrets = st.secrets["google"]
        credentials = Credentials.from_service_account_info(google_secrets)
        return credentials
    except Exception as e:
        logging.error(f"Error loading credentials, exception: {e}")
        st.error(f"Error loading credentials, exception: {e}")
        st.stop()
        
def load_and_process_data(url, llm, params):
    content = ""
    with st.spinner("Loading content..."):
    
        try:
            loader = RSSFeedLoader(urls=[url], continue_on_failure=True)
            data = loader.load()
            counter = 0
            for item in data:
                if counter >= 10:
                    break
                content += f"### {item.metadata['title']}\n"
                prompt = f"Summarize the following article in about 3 to 4 lines:\n{item.page_content}"
                content += f" {llm(prompt, **params)}\n"
                counter += 1
        except Exception as e:                
                st.error(f"Error fetching {url}, Pleae try again later.")        
        return content


def main():
    logging.basicConfig(level=logging.INFO)
    credentials = load_credentials()
    
    llm = VertexAI(model_name='text-bison@001', credentials=credentials)
    params = { 'temperature': 0.7, 'top_p': 0.9 }

    st.header("Gen AI RSS Feed Summaries App")

    user_input_url = st.text_input("Enter the RSS feed URL to get summaries of articles:", "https://www.bleepingcomputer.com/feed/")
    st.markdown('')
    
    if validators.url(user_input_url):
        content = load_and_process_data(user_input_url, llm, params)
        st.markdown(content)
    else:
        st.error(f"Invalid entry. Please enter a valid RSS feed URL.")
if __name__ == "__main__":
    main()