# summarize.py

import os
import sys
import requests
import re
from transformers import pipeline
from dotenv import load_dotenv

# --- 1. Load Secrets and Model ---

# Load the GITHUB_TOKEN from our .env file
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    print("Error: GITHUB_TOKEN not found in .env file.")
    sys.exit(1)

# Load the summarization model (this will download it the first time)
print("Loading NLP model... (this may take a minute)")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
print("Model loaded.")


# --- 2. Helper Functions ---

def parse_github_url(url: str):
    """Pulls 'owner', 'repo', and 'number' from a URL."""
    match = re.search(r"github\.com/([\w-]+)/([\w-]+)/(issues|pull)/(\d+)", url)
    if match:
        owner, repo, _, number = match.groups()
        return owner, repo, number
    return None, None, None

def get_thread_text(owner, repo, number):
    """Fetches all text from a GitHub issue."""
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    full_text = ""

    # 1. Get the main issue body
    issue_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{number}"
    issue_resp = requests.get(issue_url, headers=headers)
    if issue_resp.status_code != 200:
        return f"Error: Could not fetch issue. Status code: {issue_resp.status_code}"
    
    issue_data = issue_resp.json()
    full_text += f"Title: {issue_data.get('title', '')}\nBody: {issue_data.get('body', '')}\n\n"
    
    # 2. Get the comments
    comments_url = issue_data.get('comments_url')
    comments_resp = requests.get(comments_url, headers=headers)
    comments_data = comments_resp.json()
    
    full_text += "--- COMMENTS ---\n"
    for comment in comments_data:
        full_text += f"Comment by {comment['user']['login']}:\n{comment['body']}\n---\n"
        
    return full_text

# --- 3. Main Application Logic ---

def main():
    # Get the URL from the command line argument
    if len(sys.argv) < 2:
        print("Error: Please provide a GitHub URL as an argument.")
        print("Usage: python summarize.py <url>")
        sys.exit(1)
        
    url = sys.argv[1]
    print(f"Fetching thread from: {url}")
    
    owner, repo, number = parse_github_url(url)
    if not owner:
        print("Error: Invalid GitHub URL. Must be an issue or pull request.")
        sys.exit(1)
        
    # 1. Fetch
    try:
        text = get_thread_text(owner, repo, number)
    except Exception as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)

    # 2. Summarize
    # Truncate text to avoid model errors (models have a max input size)
    max_length = 1024
    truncated_text = text[:max_length]
    
    print("Generating summary...")
    summary = summarizer(truncated_text, max_length=150, min_length=30, do_sample=False)
    
    # 3. Print
    print("\n--- SUMMARY ---")
    print(summary[0]['summary_text'])

if __name__ == "__main__":
    main()