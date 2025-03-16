import requests
import time
from datetime import datetime, timedelta

# Function to fetch results from CSE API
def fetch_articles(query, start_date, end_date, num_results, key, cse_id):
    url = "https://www.googleapis.com/customsearch/v1"
    results = []
    start_index = 1


    # Format the date range
    date_range = f"{start_date}..{end_date}"  # Date format is YYYY-MM-DD..YYYY-MM-DD
    print(date_range)
    while len(results) < num_results:
        params = {
                'key': key,
                'cx': cse_id,
                'q': query,
                'start': start_index, # start with the first result,
                'dateRestrict': date_range,  # Date range
                'sort':'date', # Use 'sort' with 'date:r' and formatted range
                'num': 10, # Number of results per page
            }

        # Print the full URL for debugging
        full_url = f"{url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
        print("Full URL:", full_url)


        response = requests.get(url, params=params)
        print("Response Status Code:", response.status_code)
        #print("Response Content:", response.text)
        print(response)

        if response.status_code != 200:
            print("Error in API request. Check the parameters and try again.")
            break

        # Check for 429 error
        if response.status_code == 429:
            print("Rate limit exceeded. Waiting for 60 seconds...")
            time.sleep(120)  # Wait for 60 seconds before retrying
            continue  # Retry the same request

        data = response.json()
        #print(data)

        if 'items' in data:
            results.extend(data['items'])
        
        # Check if there are more results or if we've reached the desired number
        if "queries" in data and "nextPage" in data["queries"]:
            # Continue to the next page if available
            start_index += 10  # Move to the next page
            #pass
        else:
            # Stop if there are no more pages or we have enough results
            break

        # Add a delay between requests to avoid hitting the rate limit
        time.sleep(30)  # Wait for 2 seconds before the next request


    print (f"length of results: {len(results)}")
    return results
