!pip install googletrans==3.1.0a0
!pip install requests beautifulsoup4

from translation_utils import translate_article  # Import from translation_utils.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import os # Import the os module



# Replace with your own credentials
API_KEY = os.environ.get('API_KEY')
CSE_ID = os.environ.get('CSE_ID')

# Function to fetch results from CSE API
def fetch_articles(query, start_date, end_date, num_results):
    url = "https://www.googleapis.com/customsearch/v1"
    results = []
    start_index = 1


    # Format the date range
    date_range = f"{start_date}..{end_date}"  # Date format is YYYY-MM-DD..YYYY-MM-DD

    while len(results) < num_results:
        params = {
                'key': API_KEY,
                'cx': CSE_ID,
                'q': query,
                'start': start_index, # start with the first result,
                'dateRestrict': date_range,  # Date range
                'sort':'date', # Use 'sort' with 'date:r' and formatted range
                'num': 10, # Number of results per page
            }


        response = requests.get(url, params=params)
            #print(response)
        data = response.json()
        #print(data)

        if 'items' in data:
            results.extend(data['items'])

        start_index += 10  # Increment start index for next page

        # Check if there are more results or if we've reached the desired number
        if "queries" in data and "nextPage" in data["queries"]:
            # Continue to the next page if available
            pass
        else:
            # Stop if there are no more pages or we have enough results
            break


    print (len(results))
    return results

# Function to extract summary from a webpage
def extract_summary(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Assuming the article summary is in <meta name="description">
    meta_description = soup.find('meta', attrs={'name': 'description'})
    if meta_description:
        return meta_description.get('content')

    # Fallback to the first paragraph text
    paragraph = soup.find('p')
    return paragraph.text if paragraph else "No summary available."

# Function to publish articles on a webpage
def publish_articles(articles):
    html_content = "<html><head><title>India News</title></head><body><h1>India-related Articles</h1>"

    for article in articles:
        title = article['title']
        link = article['link']
        summary = extract_summary(link)

        # Translate title and summary
        translated_title = translate_article(title)
        translated_summary = translate_article(summary)

        html_content += f"<h2><a href='{link}'>{translated_title}</a></h2>"
        html_content += f"<p>{translated_summary}</p>"

    html_content += "</body></html>"

    # Get current date
    today = datetime.today().strftime('%Y-%m-%d')

    # Create filename with date
    filename = f"india_news_{today}.html"

    # Save the HTML file with the date in the filename
    with open(filename, "w") as file:
        file.write(html_content)

    print("File location:", os.path.abspath(filename))

# Date range: past 24 hours
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

# Search query to find India-related articles
query = "印度"

# Fetch articles
articles = fetch_articles(query, start_date, end_date, num_results=30)
print(len(articles))

# Publish to a webpage
publish_articles(articles)
