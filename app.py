import feedparser
import streamlit as st
from langchain.llms import VertexAI
import validators
import logging

def load_and_process_data(url, llm, params):
    content = ""
    with st.spinner("Loading content..."):
        try:
            feed = feedparser.parse(url)
            for counter, entry in enumerate(feed.entries):
                if counter >= 10:
                    break
                content += f"### {entry.title}\n"
                prompt = f"Summarize the following article in about 3 to 4 lines:\n{entry.summary}"
                content += f" {llm(prompt, **params)}\n"
        except Exception as e:
            st.error(f"Error fetching {url}, Please try again later.")
            st.error(e)
        return content

def main():
    logging.basicConfig(level=logging.INFO)

    llm = VertexAI(model_name='text-bison@001')
    params = {'temperature': 0.7, 'top_p': 0.9}

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
