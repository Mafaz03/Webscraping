from newspaper import Article

def extract_pub_date_newspaper(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.publish_date

# Test the function with a URL
url = "https://timesofindia.indiatimes.com/world/pakistan/change-in-tactics-2023-saw-terrorist-groups-place-pakistan-army-in-crosshairs/articleshow/106327512.cms"
print(extract_pub_date_newspaper(url))