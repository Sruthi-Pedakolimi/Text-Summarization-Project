import requests
import re
import os
import time, random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, parse_qs, unquote
from resources import save_to_csv_file, read_text_file
from newspaper import Article


def filter_urls(urls_list, input_text):
    unwanted_patterns = [
        "google.com/maps", "maps.google.com", "facebook.com", "twitter.com",
        "/login", "/logout", "/admin", "utm_", "session_id", "#",
        ".pdf", ".docx", ".xlsx", ".png", ".jpg", ".zip", ".json", ".xml"
    ]
    # must_have_patterns = input_text.split()
    filtered_urls = []
    for url in urls_list:
        # contains_must_have = any(pattern in url for pattern in must_have_patterns)
        contains_unwanted = any(pattern in url for pattern in unwanted_patterns)
        if not contains_unwanted:
            filtered_urls.append(url)

    return filtered_urls

def get_all_page_links(input_text):
    """
    Fetch and clean working URLs from Google search results.

    Args:
        input_text (str): The search query.

    Returns:
        list: A list of clean, working URLs.
    """
    base_url = "https://www.google.com/search"
    params = {"q": input_text}
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print(f"Failed to fetch Google search results: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, features="html.parser")
    links = []

    # Find all "a" tags with href attributes starting with "/url?q="
    for link in soup.find_all("a", href=re.compile(r"^/url\?q=(htt.*://.*)")):
        raw_url = link["href"]
        parsed_url = parse_qs(urlparse(raw_url).query).get("q")
        if parsed_url:
            decoded_url = unquote(parsed_url[0])  # Decode the URL
            links.append(decoded_url)

    # search_term = input_text.lower()
    # relevant_links = [link for link in links if search_term in link.lower()]
    filtered_urls = filter_urls(links, input_text)
    if len(filtered_urls) > 3:
        filtered_urls = filtered_urls[:3]

    return filtered_urls


def get_url_data_using_selenium(link):
                                                                                                                                                       
    # Set up Chrome options (optional: headless mode)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  # Disable GPU rendering (for compatibility)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    # Automatically download and use the appropriate ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.get(link)
        time.sleep(random.uniform(1, 3))
        # print(driver.page_source)
        if "Page Not Found" not in driver.page_source:
             text = driver.find_element(By.TAG_NAME, "body").text
             return text

    except Exception as error:
        print(f"Issue with this link: {error}")

    finally:
        driver.quit()

    return None

def get_urls_data_using_newspaper(url):
        try:
            article = Article(url)
            article.download()  # Fetch the webpage content
            article.parse()  # Parse the main content

            return article.text  # Return the main content
        except Exception as e:
            return None

def get_text_from_all_sources(urls_list):
    total_text = ""
    source_count = 1
    for url in urls_list:
        print("URL: ", url)
        source = "Source " + str(source_count) + " : "
        # text = get_url_data_using_selenium(url)
        text = get_urls_data_using_newspaper(url)
        if text is not None:
            total_text += source + text + "\n"
            source_count += 1

    return total_text


def get_crawled_text(input_text):
    urls_list = get_all_page_links(input_text)
    #
    # print("Input text: ", input_text)
    # print("urls_list: ", urls_list)
    total_text = get_text_from_all_sources(urls_list)
    save_to_csv_file(total_text, "text_files/"+input_text+".txt")
    # print(total_text)
    return total_text

# if __name__ == "__main__":
#     get_crawled_text("How Corona Effects the World")