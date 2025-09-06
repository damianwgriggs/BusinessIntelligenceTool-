import streamlit as st
import google.generativeai as genai
import os
import time
import requests
from bs4 import BeautifulSoup

# --- Helper Functions for Session State Rate Limiting ---
def check_rate_limit(limit=5, period_seconds=3600):
    """Checks the usage limit based on Streamlit's Session State."""
    # Initialize the usage log in the session state if it doesn't exist
    if 'usage_log' not in st.session_state:
        st.session_state.usage_log = []
    
    current_time = time.time()
    cutoff_time = current_time - period_seconds

    # Filter out old timestamps from the log
    st.session_state.usage_log = [ts for ts in st.session_state.usage_log if ts > cutoff_time]
    
    # Check if the user is under the limit
    return len(st.session_state.usage_log) < limit

def add_usage_record():
    """Adds a new usage timestamp to the session state."""
    st.session_state.usage_log.append(time.time())

# --- Scraper Module ---
def scrape_text_from_url(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = '\n'.join(chunk for chunk in chunks if chunk)
        return clean_text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the URL: {e}")
        return None

# --- Configuration (Shared) ---
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# --- Main App Interface ---
st.set_page_config(page_title="AI Business Intelligence Tool", layout="wide")
st.title("📈 AI Business Intelligence Tool")

# --- UI Tabs ---
tab1, tab2 = st.tabs(["Business Sentiment Analyzer", "Webpage Summarizer"])

# --- Tab 1: Sentiment Analyzer ---
with tab1:
    st.header("Analyze Customer Sentiment")
    customer_reviews = st.text_area("Paste Customer Reviews Here:", height=250, key="sentiment_reviews")

    if st.button("Analyze Sentiment", key="sentiment_button"):
        if not check_rate_limit():
            st.error("Rate limit exceeded. Please try again later. (Limit is per session)")
        elif not customer_reviews.strip():
            st.warning("Please paste some customer reviews first.")
        else:
            with st.spinner("Analyzing sentiment..."):
                prompt = f"""
                Analyze the following block of customer reviews and perform two tasks:
                1. **Overall Sentiment:** Classify the overall sentiment into one of three categories: Positive, Negative, or Neutral.
                2. **Key Themes:** Provide a bulleted list of the top 3-5 recurring themes, complaints, or praises mentioned in the reviews.
                Customer Reviews: --- {customer_reviews}
                """
                try:
                    response = model.generate_content(prompt)
                    st.success("Analysis Complete!")
                    st.markdown(response.text)
                    add_usage_record()
                except Exception as e:
                    st.error(f"An error occurred: {e}")

# --- Tab 2: Webpage Summarizer ---
with tab2:
    st.header("Summarize a Webpage")
    url_input = st.text_input("Paste URL Here:", key="url_input")

    if st.button("Generate Summary", key="summary_button"):
        if not check_rate_limit():
            st.error("Rate limit exceeded. Please try again later. (Limit is per session)")
        elif not url_input.strip():
            st.warning("Please paste a URL first.")
        else:
            with st.spinner("Scraping and summarizing..."):
                scraped_text = scrape_text_from_url(url_input)
                if scraped_text:
                    prompt = f"""
                    Please act as an expert analyst. Read the following text scraped from a webpage and provide a concise, easy-to-read summary of its key points in a few bullet points.
                    Scraped Text: --- {scraped_text}
                    """
                    try:
                        response = model.generate_content(prompt)
                        st.success("Summary Complete!")
                        st.markdown(response.text)
                        add_usage_record()
                    except Exception as e:
                        st.error(f"An error occurred during AI analysis: {e}")