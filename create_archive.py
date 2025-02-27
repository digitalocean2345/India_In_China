import os 
from datetime import datetime, timedelta
import calendar # import calendar

def create_archive_index(docs_dir):
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
