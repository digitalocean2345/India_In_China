#!pip install googletrans==3.1.0a0
#!pip install requests beautifulsoup4

import subprocess
subprocess.run(["pip", "install", "googletrans==3.1.0a0"])
import subprocess
subprocess.run(["pip", "install", "requests", "beautifulsoup4"])

from translation_utils import translate_article  # Import from translation_utils.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import os # Import the os module
import calendar # import calendar


# Replace with your own credentials
API_KEY = os.getenv('API_KEY')
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

def publish_articles(articles):
    # Get current date
    today = datetime.today().strftime('%Y-%m-%d')
    
    # Use f-string to properly embed the variable in the HTML content
    html_content = f"<html><head><title>India News {today}</title></head><body><h1>India-related Articles {today}</h1></body></html>"
    
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

def create_archive_index(docs_dir="docs"):
    """Creates an index.html file with a clickable calendar archive."""

    # Get a list of all HTML files in the docs directory
    html_files = [f for f in os.listdir(docs_dir) if f.startswith("india_news_") and f.endswith(".html")]
    
    # Create a dictionary to store the dates and their corresponding HTML files
    date_links = {}
    for file in html_files:
        # Extract the date from the filename
        date_str = file.split("_")[2].split(".")[0]
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            date_links[date_obj] = file
        except ValueError:
            print(f"Skipping file with invalid date format: {file}")

    # Create HTML content for the calendar
    calendar_html = "<h1>Daily Archive</h1>"
    # Create a calendar for the current month, and link the files to their respective days.
    current_date = datetime.today()
    current_month = current_date.month
    current_year = current_date.year
    cal = calendar.Calendar()
    calendar_html+= f"<h2>{calendar.month_name[current_month]} {current_year}</h2>"
    calendar_html += "<table style='border-collapse: collapse; width: 50%;'>"
    calendar_html += "<tr style='border: 1px solid black;'><th style='border: 1px solid black;'>Sun</th><th style='border: 1px solid black;'>Mon</th><th style='border: 1px solid black;'>Tue</th><th style='border: 1px solid black;'>Wed</th><th style='border: 1px solid black;'>Thu</th><th style='border: 1px solid black;'>Fri</th><th style='border: 1px solid black;'>Sat</th></tr>"
    
    for week in cal.monthdayscalendar(current_year, current_month):
        calendar_html += "<tr style='border: 1px solid black;'>"
        for day in week:
            if day == 0:
                calendar_html += "<td style='border: 1px solid black;'></td>"
            else:
                current_day = datetime(current_year, current_month, day)
                if current_day in date_links:
                    calendar_html += f"<td style='border: 1px solid black;'><a href='{date_links[current_day]}'>{day}</a></td>"
                else:
                    calendar_html += f"<td style='border: 1px solid black;'>{day}</td>"
        calendar_html += "</tr>"
    calendar_html += "</table>"
    

    # Create the index.html content
    index_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Daily News Archive</title>
        <style>
            table {{
                border-collapse: collapse;
                width: 50%;
            }}
            th, td {{
                border: 1px solid black;
                padding: 8px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        {calendar_html}
    </body>
    </html>
    """
    # Save the index.html file
    index_path = os.path.join(docs_dir, "index.html")
    with open(index_path, "w") as file:
        file.write(index_content)

    print(f"Archive index created: {index_path}")

# Date range: past 24 hours
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

# Search query to find India-related articles
query = "印度"

# Fetch articles
articles = fetch_articles(query, start_date, end_date, num_results=90)
print(len(articles))

# Publish to a webpage
publish_articles(articles)

#Create the daily archive index
create_archive_index()
