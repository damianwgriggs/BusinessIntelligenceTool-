# AI Business Intelligence Tool

This is a multi-functional web application that combines two powerful AI-driven tools into a single, streamlined interface. This project serves as a portfolio piece demonstrating the ability to build and deploy sophisticated, practical AI applications using the "Architect & AI Co-Pilot" development framework.

The application is built with Python and Streamlit and is deployed on Hugging Face Spaces.

---

## Features

This tool provides two distinct modules accessible through a clean, tabbed interface:

### 1. Business Sentiment Analyzer
* **Function**: Users can paste a block of unstructured text, such as customer reviews or survey responses.
* **Output**: The AI analyzes the text and provides a high-level summary, classifying the overall sentiment as **Positive, Negative, or Neutral**, and extracts a bulleted list of the key recurring themes.

### 2. AI Webpage Summarizer
* **Function**: Users can provide a URL to an article, blog post, or news story.
* **Output**: The application scrapes the text content from the webpage, sends it to the AI, and returns a concise, bullet-pointed summary of the key information.

---

## Key Technologies
* **Python**: The core programming language.
* **Streamlit**: For building the interactive, multi-tab web interface.
* **Google Gemini API**: For all natural language processing tasks (sentiment analysis and summarization).
* **BeautifulSoup & Requests**: For the web scraping module.
* **Streamlit Session State**: For implementing a robust, server-side rate limit per user session.
* **Hugging Face Spaces**: For hosting the live application.
* **Docker**: For containerizing the application to ensure a stable and reproducible deployment environment.

---

## Setup and Configuration

To run this project, you will need a secret API key from Google.

### 1. Clone and Install
First, clone the repository from GitHub and install the necessary libraries from the `requirements.txt` file.

```bash
# Clone the repository
git clone [URL_OF_YOUR_GITHUB_REPO]

# Navigate into the project directory
cd Business-Intelligence-Tool

# Install all required libraries
pip install -r requirements.txt
