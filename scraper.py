import requests
from bs4 import BeautifulSoup
import time

# 🔁 Replace this with your actual Make.com webhook URL
WEBHOOK_URL = 'https://hook.us2.make.com/4gsv4eug8wfap33lifa8svkhi4cui59g'

# Get sitemap and extract event URLs
sitemap_url = "https://www.visitmilwaukee.org/sitemap.xml"
headers = {'User-Agent': 'Mozilla/5.0'}

sitemap_res = requests.get(sitemap_url, headers=headers)
soup = BeautifulSoup(sitemap_res.content, 'lxml-xml')
event_urls = [loc.text for loc in soup.find_all('loc') if '/event/' in loc.text]

for url in event_urls[:5]:  # Limit to 5 for testing
    res = requests.get(url, headers=headers)
    page = BeautifulSoup(res.text, 'html.parser')

    title = page.find('h1').text.strip() if page.find('h1') else 'N/A'
    date = page.find('span', class_='event-detail-date')
    location = page.find('div', class_='event-detail-location')

    payload = {
        "title": title,
        "date": date.text.strip() if date else "N/A",
        "location": location.text.strip() if location else "Milwaukee",
        "link": url
    }

    response = requests.post(WEBHOOK_URL, json=payload)
    print(f"{'✅' if response.status_code == 200 else '❌'} Sent: {title}")
    time.sleep(2)  # Respect crawl-delay
