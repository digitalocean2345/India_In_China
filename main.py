#!pip install googletrans==3.1.0a0
#!pip install requests beautifulsoup4

import subprocess
subprocess.run(["pip", "install", "googletrans==3.1.0a0"])
import subprocess
subprocess.run(["pip", "install", "requests", "beautifulsoup4"])

from translation_utils import translate_article  # Import from translation_utils.py
from fetch_utils import fetch_articles
from create_archive import create_archive_index

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import os # Import the os module
import calendar # import calendar
import time

# Replace with your own credentials
API_KEY = os.getenv('API_KEY')
CSE_ID_Chinese = os.getenv('CSE_ID_C')
CSE_ID_English = os.getenv('CSE_ID_E')

print("API_KEY:", API_KEY)
print("CSE_ID_Chinese:", CSE_ID_Chinese)
print("CSE_ID_English:", CSE_ID_English)

def publish_articles(articles):
    # Get current date
    today = datetime.today().strftime('%Y-%m-%d')
    
    # Use f-string to properly embed the variable in the HTML content
    html_content = f"<html><head><title>India News {today}</title></head><body><h1>India-related Articles {today}</h1></body></html>"
    
    for article in articles:
        title = article['title']
        link = article['link']
        #summary = extract_summary(link)

        # Translate title and summary
        translated_title = translate_article(title)
        #translated_summary = translate_article(summary)

        html_content += f"<h2><a href='{link}'>{translated_title}</a></h2>"
        #html_content += f"<p>{translated_summary}</p>"
        html_content += "<p>----------------------</p>"


    html_content += "</body></html>"
   

    # Create filename with date
    filename = f"india_news_{today}.html"

    # Define the path to the docs directory
    docs_dir = os.path.join(os.getcwd(), "docs")  # Ensure full path

    
    # Ensure the 'docs' directory exists
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir, exist_ok=True) #Ensure directory creation
    
    # Define the full file path within the docs directory
    file_path = os.path.join(docs_dir, filename)
    
    # Save the HTML file with the date in the filename
    with open(file_path, "w") as file:
        file.write(html_content)

    print(f"File location: {file_path}")



# Date range: past 24 hours
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

# Search query to find India-related articles
query_c = "印度"
query_e = "india"
# Fetch articles from Chinese sources
articles_chinese = fetch_articles(query_c, start_date, end_date, num_results=90, key=API_KEY, cse_id=CSE_ID_Chinese)
print(f"number of articles fetched from Chinese sources: {len(articles_chinese)}")

# Fetch articles from English sources
articles_english = fetch_articles(query_e, start_date, end_date, num_results=30, key=API_KEY, cse_id=CSE_ID_English)
print(f"number of articles fetched from English sources: {len(articles_english)}")

# Combine the results
combined_articles = articles_chinese + articles_english
print(f"total number of articles: {len(combined_articles)}")

# Publish to a webpage
publish_articles(combined_articles)

#Create the daily archive index

create_archive_index(docs_dir="docs")
