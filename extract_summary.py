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
