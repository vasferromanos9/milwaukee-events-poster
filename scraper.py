import requests
from bs4 import BeautifulSoup
import time

# Your Make.com webhook URL
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

    # Title
    title_tag = page.find('h1', {'role': 'heading'})
    title = title_tag.text.strip() if title_tag else 'N/A'

    # Date
    date_tag = page.find('span', class_='event-detail-date')
    date = date_tag.text.strip() if date_tag else 'N/A'

    # Location
    location_div = page.find('div', class_='event-detail-location')
    location = location_div.text.strip() if location_div else 'Milwaukee'

    # Address (venue + full address)
    address_wrap = page.find('div', class_='two-line-wrap')
    if address_wrap:
        venue = address_wrap.find('a').text.strip() if address_wrap.find('a') else ''
        address = address_wrap.find('span', class_='address-cont').text.strip() if address_wrap.find('span', class_='address-cont') else ''
        full_address = f"{venue}, {address}".strip(', ')
    else:
        full_address = 'N/A'

    # Image
    image_tag = page.find('img', class_='slide-img')
    image_url = image_tag['src'] if image_tag and 'src' in image_tag.attrs else 'N/A'

    # Content / Description
    content_div = page.find('div', class_='core-styles')
    if content_div:
        paragraphs = content_div.find_all('p')
        content = '\n\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
    else:
        content = 'N/A'

    # Send to webhook
    payload = {
        "title": title,
        "date": date,
        "location": location,
        "address": full_address,
        "image": image_url,
        "content": content,
        "link": url
    }

    response = requests.post(WEBHOOK_URL, json=payload)
    print(f"{'✅' if response.status_code == 200 else '❌'} Sent: {title}")
    time.sleep(2)  # Be polite to the server
