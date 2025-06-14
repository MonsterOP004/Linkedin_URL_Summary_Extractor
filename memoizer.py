# memoizer.py
from cachetools import TTLCache
from scrapper import scrape_url
from llm import get_response

scrape_cache = TTLCache(maxsize=100, ttl=3600)
llm_cache = TTLCache(maxsize=100, ttl=3600)

def memoized_scrape(url: str):
    if url in scrape_cache:
        return scrape_cache[url]
    result = scrape_url(url)
    scrape_cache[url] = result
    return result

def memoized_llm_response(yaml_text: str):
    if yaml_text in llm_cache:
        return llm_cache[yaml_text]
    result = get_response(yaml_text)
    llm_cache[yaml_text] = result
    return result
