import requests
from bs4 import BeautifulSoup

def get_html(urls : list[str]):
    """
    Function that takes in urls and returns the html content within it

    Args:
    urls = List of all urls

    Return:
    Dictionary: {urls : html content}
    failed_fetch: websites that it coudl'nt access during fetching html
    """
    website_content = {}
    failed_fetch = 0

    for website_idx in range(len(urls)):
        website = urls[website_idx]
        response = requests.get(website)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()
        else:
            failed_fetch += 1

        lines = text.splitlines()
        non_empty_lines = [line for line in lines if line.strip()]
        result = '\n'.join(non_empty_lines)
        website_content[website] = result

    return website_content, failed_fetch

## Usecase:
"""
text2, failed_fetch_html = get_html(["https://timesofindia.indiatimes.com/india/whole-world-waiting-for-22nd-january-pm-modi-in-ayodhya/articleshow/106388185.cms"])
print(text2)
"""