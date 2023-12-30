import requests
from bs4 import BeautifulSoup

def extract_pub_date(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    date_tag = soup.find('div', {'class': '_3Mkg- byline'})
    if date_tag:
        return date_tag.text
    else:
        return "Publication date not found"

# Test the function with a URL
url = "https://timesofindia.indiatimes.com/world/pakistan/change-in-tactics-2023-saw-terrorist-groups-place-pakistan-army-in-crosshairs/articleshow/106327512.cms"
print(extract_pub_date(url))