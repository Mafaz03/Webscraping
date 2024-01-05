import requests
import re
from bs4 import BeautifulSoup
import ssl
from tqdm import tqdm



class WebScraper1:
    """
    Class WebScraper

    Args:
    sub_url_size: Number of self iteration/ tree branches.
    """
    def __init__(self, sub_url_size):
        self.inside_urls = dict()  # Storing inside URLs as a dict for uniqueness
        self.failed_fetch = 0
        self.sub_url_size = sub_url_size

    def get_suburls1(self, urls_list):
        """
        Gets as many urls as mentioned by the sub_url_size.

        Args:
        urls_list: Top urls.

        Returns:
        inside_urls: [list] All available urls.
        failed_fetch: amount of urls that couldnt be fetched due to some error.
        sub_url_size: tree split.
        total_size: amount of urls present in inside_urls.
        """
        
        urls_list = urls_list.split(',')
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
    

class WebScraper2:
    """
    Class WebScraper

    Args:
    sub_url_size: Number of self iteration/ tree branches.
    """
    def __init__(self, sub_url_size, keywords):
        self.inside_urls = dict()  # Storing inside URLs as a dict for uniqueness
        self.failed_fetch = 0
        self.sub_url_size = sub_url_size
        self.keywords = keywords.split(",")

    def get_suburls2(self, urls_list):
        """
        Gets as many urls as mentioned by the sub_url_size.

        Args:
        urls_list: Top urls.

        Returns:
        inside_urls: [list] All available urls.
        failed_fetch: amount of urls that couldnt be fetched due to some error.
        sub_url_size: tree split.
        total_size: amount of urls present in inside_urls.
        """
        
        urls_list = urls_list.split(',')
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
            
            temp_inside_urls = [url for url in temp_inside_urls if any(keyword in url for keyword in self.keywords)]
            self.inside_urls[i + 1] = temp_inside_urls
            
        total_size = 0
        for i in self.inside_urls:
            total_size += len(self.inside_urls[i])
        return self.inside_urls, self.failed_fetch, self.sub_url_size, total_size
"""
# Example Usage:
urls_list = ["https://www.khaleejtimes.com"] # Can add as many urls as needed, keep it below 5 for faster executing
scraper = WebScraper1(1) # KEEP IT 1, 2 or more will result in 1000's of urls.
                        # Integration with DB will make it faster in future, as fetching is much faster than scrapping.
inside_urls, failed_fetch, sub_url_size, total_size = scraper1.get_suburls(urls_list)

print("Inside URLs:", inside_urls)
print("Failed Fetch:", failed_fetch)
print("Splits:", len(inside_urls))
print("Tree size:", total_size)

"""
