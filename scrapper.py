import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import yaml

def scrape_url(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        response = requests.get(url, headers=headers, timeout=8)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')  # use lxml for speed
        domain = urlparse(url).netloc
        title = soup.title.string.strip() if soup.title and soup.title.string else "No title found"

        meta_tag = soup.select_one("meta[name='description']")
        meta_desc = meta_tag['content'].strip() if meta_tag and 'content' in meta_tag.attrs else ""

        # Extract main content quickly
        main_content = ""
        content_blocks = soup.select("main, article, div[class*='main'], div[class*='content']")[:2]

        for block in content_blocks:
            text = block.get_text(separator=' ', strip=True)
            if text and len(main_content) < 5000:
                main_content += text + "\n\n"
        
        # Fallback to body if nothing found
        if not main_content:
            for tag in soup.select("body p, body h1, body h2, body h3, body li")[:50]:
                main_content += tag.get_text(strip=True) + "\n"
        
        return {
            "url": url,
            "main_content": main_content[:5000],
        }

    except Exception as e:
        return {
            "url": url,
            "error": str(e),
            "main_content": "Failed to scrape content"
        }

def html_to_yaml(scraped_data):
    try:
        yaml_data = {
            "website": {
                "url": scraped_data.get("url", ""),
            },
            "content": {
                "main_text": scraped_data.get("main_content", "")
            }
        }

        return yaml.dump(yaml_data, sort_keys=False, default_flow_style=False)

    except Exception as e:
        return f"Error converting to YAML: {str(e)}\n\nRaw data: {str(scraped_data)}"
