import requests
from bs4 import BeautifulSoup

def extract_pub_date_from_metadata(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    meta_tag = soup.find('meta', {'property': 'article:published_time'})
    if meta_tag:
        return meta_tag['content']
    else:
        return "Publication date not found in metadata"

# Test the function with a URL
url = "https://timesofindia.indiatimes.com/world/pakistan/change-in-tactics-2023-saw-terrorist-groups-place-pakistan-army-in-crosshairs/articleshow/106327512.cms"
print(extract_pub_date_from_metadata(url))