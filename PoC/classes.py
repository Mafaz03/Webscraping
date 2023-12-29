import requests
import re
from bs4 import BeautifulSoup
import ssl

class WebScraper:
    def __init__(self, sub_url_size):
        ssl._create_default_https_context = ssl._create_unverified_context
        self.inside_urls = set()  # Storing inside URLs as a set for uniqueness
        self.failed_fetch = 0
        self.sub_url_size = sub_url_size

    def get_suburls(self, urls_list):
        for _ in range(self.sub_url_size):
            temp_inside_urls = set()  # Temporary set to avoid duplication per iteration
            for url_ in urls_list:
                try:
                    response = requests.get(url_)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        all_links = soup.find_all('a', href=True)
                        excluded_domains = r'(magicbricks|play\.google|facebook\.com|twitter\.com|instagram\.com|linkedin\.com|youtube\.com|\.gov|\.org|policy|terms|buy|horoscope)'

                        for link in all_links:
                            href = link['href']
                            if re.match(r'https?://', href) and not re.search(excluded_domains, href):
                                print(href)
                                temp_inside_urls.add(href)
                    else:
                        self.failed_fetch += 1
                except Exception as e:
                    print(f"Error fetching {url_}: {e}")
                    self.failed_fetch += 1
                
            self.inside_urls.update(temp_inside_urls)  # Update the main set with unique URLs found in this iteration
            urls_list = list(temp_inside_urls)  # Update the URLs for the next iteration

        return self.inside_urls, self.failed_fetch, self.sub_url_size

# Example Usage:
# urls_list = ["https://timesofindia.indiatimes.com"]
# scraper = WebScraper(2)
# inside_urls, failed_fetch, sub_url_size = scraper.get_suburls(urls_list)

# print("Inside URLs:", inside_urls)
# print("Failed Fetch:", failed_fetch)
# print("Size:", len(inside_urls))
# print("Tree size:", sub_url_size)
