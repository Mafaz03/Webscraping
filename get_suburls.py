import requests
import re
from bs4 import BeautifulSoup
import ssl
from tqdm import tqdm



class WebScraper:
    def __init__(self, sub_url_size):
        ssl._create_default_https_context = ssl._create_unverified_context
        self.inside_urls = dict()  # Storing inside URLs as a dict for uniqueness
        self.failed_fetch = 0
        self.sub_url_size = sub_url_size

    def get_suburls(self, urls_list):
        self.inside_urls[0] = urls_list
        for i in range(self.sub_url_size):
            temp_inside_urls = [] 
            for url_ in tqdm(self.inside_urls[i]):
                try:
                    response = requests.get(url_)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        all_links = soup.find_all('a', href=True)
                        excluded_domains = r'(magicbricks|play\.google|facebook\.com|twitter\.com|instagram\.com|linkedin\.com|youtube\.com|\.gov|\.org|policy|terms|buy|horoscope)'
                        # excluded_domains will not take urls into account with these domains
                        for link in all_links:
                            href = link['href']
                            if re.match(r'https?://', href) and not re.search(excluded_domains, href):
                                # print(href)
                                temp_inside_urls.append(href)
                    else:
                        self.failed_fetch += 1
                except Exception as e:
                    print(f"Error fetching {url_}: {e}")
                    self.failed_fetch += 1
            self.inside_urls[i + 1] = temp_inside_urls
        total_size = 0
        for i in self.inside_urls:
            total_size += len(self.inside_urls[i])
        return self.inside_urls, self.failed_fetch, self.sub_url_size, total_size

# Example Usage:
urls_list = ["https://www.khaleejtimes.com"] 
scraper = WebScraper(1)
inside_urls, failed_fetch, sub_url_size, total_size = scraper.get_suburls(urls_list)

print("Inside URLs:", inside_urls)
print("Failed Fetch:", failed_fetch)
print("Splits:", len(inside_urls))
print("Tree size:", total_size)
