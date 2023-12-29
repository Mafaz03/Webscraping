from tkinter import *
import requests
from bs4 import BeautifulSoup
import re
import requests
import ssl
import openai
from tqdm import tqdm

import csv
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By


# Set your OpenAI API key
api_key = "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"
openai.api_key = api_key

# GUI
root = Tk()
root.title("Petra Oil Bot")

# Set the size of the root window to 1080x1920
root.geometry("650x600")

BG_GRAY = "#ABB2B9"
BG_COLOR = "#383836"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

urls_list = []
keyword_list = []

def add_to_list_url():
    # Get the text from the Entry widget
    url = e_urls.get()

    # Append the URL to the list
    urls_list.append(url)

    # Clear the Entry widget
    e_urls.delete(0, 'end')

    print(urls_list)

    website_str = "\n".join(urls_list)
    txt.insert(END, "\n\nWEBSITES TO BE LOOKED INTO:\n" + website_str)

def add_to_list_keyword():
    # Get the text from the Entry widget
    key = e_keywords.get()

    # Append the URL to the list
    keyword_list.append(key)

    # Clear the Entry widget
    e_keywords.delete(0, 'end')

    print(keyword_list)

    keyword_str = "\n".join(keyword_list)
    txt.insert(END, "\n\nKEYWORDS TO BE LOOKED INTO:\n" + keyword_str)

def perform_url_scrapping():

    data    = []
    header  = ['title', 'link', 'date']

    def sort_csv_by_date(csv_file_path):
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            data = list(reader)

        # Sort the data based on the 'date' field
        data.sort(key=lambda x: datetime.strptime(x['date'], '%d/%m/%Y'), reverse=True)

        # Write the sorted data back to the CSV file
        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'link', 'date'])
            writer.writeheader()
            writer.writerows(data)


    def convert(date_str):
        if isinstance(date_str, (int, float)):
            date_pattern = r'\b\d{2}/\d{2}/\d{4}\b'
            dates = re.findall(date_pattern, str(date_str))

            # Assuming that there can be multiple matches, convert each one
            converted_dates = [datetime.strptime(date, "%m/%d/%Y").strftime("%d/%m/%Y") for date in dates]
            return converted_dates

        # Try to extract the date part using a specific pattern
        date_match = re.search(r'(\d{2}/\d{2}/\d{4})', date_str)
        if date_match:
            date_str = date_match.group(1)

            # Try to parse the date with the specific format
            try:
                date_obj = datetime.strptime(date_str, "%m/%d/%Y")
                return date_obj.strftime("%d/%m/%Y")
            except ValueError:
                pass
        
        # Try to parse the date with multiple formats
        formats_to_try = ["%B %d, %Y", "%m/%d/%Y - %H:%M", "%A, %B %d, %Y - %H:%M", "%B %d, %Y - %H:%M"]
        for format_str in formats_to_try:
            try:
                date_obj = datetime.strptime(date_str, format_str)
                return date_obj.strftime("%d/%m/%Y")
            except ValueError:
                pass
        # If none of the formats match, return the original string
        return date_str

    def write_csv():

        for row in data:
            row['date'] = convert(row['date'])


        
        with open('link.csv', mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(data)

    def prepare_source(urls : list) -> pd.DataFrame:
        df = pd.DataFrame(columns=["home_page" , "base_url" , "title" , "date"])
        source  = pd.read_csv('master_source.csv')

        for url in urls:
            if source[source["home_page"] == url].empty == True:
                print(f"The URL {url} is not present in master source file")
            else:
                exist = source[source["home_page"] == url]
                df = pd.concat([df , exist] , axis=0)

        df.to_csv("source.csv" , index=False)
        return df
        

    urls = urls_list
    prepare_source(urls)

    def scrape():
        # prompt  = input("Prompt: ")fgfds
        prompt = ",".join(keyword_list)
        key     = prompt.replace(" ", "%20")
        driver  = webdriver.Chrome()

        source  = pd.read_csv('source.csv')
        rows    = source.shape[0]
        
        processed_urls = set()  
        
        for i in range(rows):
            base_url = source.base_url[i]
            xpath    = source.title[i]
            basedate = source.date[i]

            for i in range(1,5):
                try:
                    url = f"{base_url.format(key= key, page=i)}"
                    driver.get(url)

                    for j in range(1, 11):
                        try:
                            xp      = xpath.format(j)
                            date_xp = basedate.format(j)

                            date    = driver.find_element(By.XPATH, date_xp).text
                            link    = driver.find_element(By.XPATH, xp)
                            url     = link.get_attribute("href")
                            title   = link.text

                            if url not in processed_urls:

                                entry = {
                                    "title" : title,
                                    "link"  : url,
                                    "date"  : date
                                }
                                
                                data.append(entry)
                                processed_urls.add(url)

                        except:
                            pass


                except:
                    pass

        driver.quit() 

        
    if __name__ == '__main__':
        scrape()
        write_csv()
        sort_csv_by_date('link.csv')







def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "system", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

# Send function
def send():
    ssl._create_default_https_context = ssl._create_unverified_context
    website_content = {}
    

    top_urls = urls_list
    
    website_str = "\n".join(top_urls)
    txt.insert(END, "\n\nWEBSITES TO BE LOOKED INTO:\n" + website_str)

    txt.insert(END, "\n\nAnalyzing Sub URLs.....")
    inside_urls = []
    failed_fetch = 0

    for url_ in top_urls:
        response = requests.get(url_)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            all_links = soup.find_all('a', href=True)
            excluded_domains = r'(facebook\.com|twitter\.com|instagram\.com|linkedin\.com|youtube\.com|\.gov|\.org|policy|terms)'

            for link in all_links:
                href = link['href']
                if re.match(r'https?://', href) and not re.search(excluded_domains, href):
                    inside_urls.append(href)
        else:
            failed_fetch += 1

    txt.insert(END, f"\n\n{failed_fetch} URLS Failed to fetch content from {len(inside_urls)} sub URL")

    website_sub_str = "\n".join(inside_urls)
    text_file = open("Metadata 1.txt", "w")
    text_file.write(website_sub_str)

    root.after(2000, lambda:txt.insert(END, f"\n{len(inside_urls)} sub URLs have been saved in 'Metadata 1.txt'"))

    root.after(2000, lambda:txt.insert(END, f"\nPlease wait as {len(inside_urls)} sub URLs are getting scraped"))

    for url_index in tqdm(range(len(inside_urls))):
        website = inside_urls[url_index]
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

    print("\n\n\n")

    # Get keywords from the entry widget

    # keywords = e_keywords.get().split(";")
    keywords = keyword_list
    keywords_str = "\n".join(keywords)
    txt.insert(END, f"\n\nKEYWORDS:\n{keywords_str}")

    website_content_relevant = {}

    for url, text in website_content.items():
        paragraphs = text.split('\n')
        keyword_paragraphs = [paragraph for paragraph in paragraphs if any(keyword in paragraph.lower() for keyword in keywords)]
        for paragraph in keyword_paragraphs:
            if len(paragraph) >= 10:
                website_content_relevant[url] = paragraph.strip()

    keys_str = pd.DataFrame(website_content_relevant , index=[0])
    keys_str.to_csv("metadata 2.csv" , index=False)
    # text_file = open("Metadata 2.txt", "w")
    # text_file.write(keys_str)
    root.after(2000, lambda:txt.insert(END, "\n\nRelevant URLs : Description have been saved in 'Metadata 2.csv'"))

    # Get question/topic from the entry widget
    question = e_question.get()
    txt.insert(END, f"\n\nQuestion/Topic: {question}\n")

    root.after(2000, lambda:txt.insert(END, "\n\nGenerating Response.......\n"))

    prompt = f""" 
    Data is in the form of dictionary: {website_content_relevant} \n\n\n 
    Question: {question} \n\n\n
    Method of reply: 100 - 200 word sentences, clear reply,
    """

    response = get_completion(prompt)
    root.after(2000, lambda:txt.insert(END, "\n\nResponse: " + response))

    prompt = f"""Data: {website_content_relevant} \n\n\n 
    Question: Only mention URLs from data for {question} \n\n\n
    Method of reply: 2-5 URLs, separate each point with a 2-line gap, format it properly
    """
    response1 = get_completion(prompt)
    root.after(2000, lambda:txt.insert(END, "\n\nFor more information:\n\n" + response1))
    # txt.insert(END, f"\n\nFrom {len(inside_urls)}, {len(website_content_relevant.keys())} have been found useful\n\n{(len(inside_urls) * (len(website_content_relevant.keys())/100))}% Coverage")

    text_file = open("Result.txt", "w")
    text_file.write(response + "\n\n\n\n" + response1)

# Entry widgets for URLs, keywords, and question/topic
e_urls = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=100)
e_urls.grid(row=2, column=0 , columnspan=4)


e_keywords = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=100)
e_keywords.grid(row=3, column=0 , columnspan=4)

e_question = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=100)
e_question.grid(row=4, column=0 , columnspan=4)

send_button = Button(root, text="Prompt Scraping", font=FONT_BOLD, bg=BG_GRAY, command=send)
send_button.grid(row=5, column=0 , columnspan=2)

btn_add_url = Button(root, text="Add url to stack", command=add_to_list_url , font=FONT_BOLD, bg=BG_GRAY)
btn_add_url.grid(row=5, column=1 , columnspan=2)

btn_add_key = Button(root, text="Add keyword to stack", command=add_to_list_keyword , font=FONT_BOLD, bg=BG_GRAY)
btn_add_key.grid(row=5, column=2 , columnspan=2)

perform_url_scrape = Button(root, text="URL scrapping", command=perform_url_scrapping , font=FONT_BOLD, bg=BG_GRAY)
perform_url_scrape.grid(row=6, column=0 , columnspan=2)


txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=100, height=50)
txt.grid(row=1, column=0, columnspan=4)

# scrollbar = Scrollbar(txt)
# scrollbar.place(relheight=1, relx=0.974)

root.mainloop()
