import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote
from resources import save_to_csv_file
from newspaper import Article


def get_crawled_text(input_text):
    urls_list = get_google_search_urls(input_text)
    total_text = get_content_from_all_urls(urls_list)
    save_to_csv_file(total_text, "text_files/"+input_text+".txt")
    return total_text


def get_google_search_urls(input_text):
    response =  get_google_search_page_response(input_text)
    soup = BeautifulSoup(response.content, features="html.parser")
    urls_list = []

    # Find all "a" tags with href attributes starting with "/url?q="
    for url in soup.find_all("a", href=re.compile(r"^/url\?q=(htt.*://.*)")):
        raw_url = url["href"]
        parsed_url = parse_qs(urlparse(raw_url).query).get("q")
        if parsed_url:
            decoded_url = unquote(parsed_url[0])  # Decode the URL
            urls_list.append(decoded_url)

    filtered_urls = filter_unwanted_urls(urls_list)
    if len(filtered_urls) > 3:
        filtered_urls = filtered_urls[:3]
    return filtered_urls

def get_content_from_all_urls(urls_list):
    total_text = ""
    source_count = 1
    for url in urls_list:
        source = "Source " + str(source_count) + " : "
        text = get_url_content_using_newspaper(url)
        if text is not None:
            total_text += source + text + "\n"
            source_count += 1
    return total_text




def filter_unwanted_urls(urls_list):
    unwanted_patterns = [
        "google.com/maps", "maps.google.com", "facebook.com", "twitter.com",
        "/login", "/logout", "/admin", "utm_", "session_id", "#",
        ".pdf", ".docx", ".xlsx", ".png", ".jpg", ".zip", ".json", ".xml","instagram", "pinterest"
    ]
    filtered_urls = []
    for url in urls_list:
        contains_unwanted = any(pattern in url for pattern in unwanted_patterns)
        if not contains_unwanted:
            filtered_urls.append(url)
    return filtered_urls

def get_google_search_page_response(input_text):
    google_base_url = "https://www.google.com/search"
    params = {"q": input_text}
    response = requests.get(google_base_url, params=params)
    if response.status_code != 200:
        print(f"Failed to fetch Google search results: {response.status_code}")
        return []
    return response

def get_url_content_using_newspaper(url):
        try:
            article = Article(url)
            article.download()  # Fetch the webpage content
            article.parse()  # Parse the main content
            return article.text  # Return the main content
        except Exception as e:
            return None




# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# import time, random
# def get_url_data_using_selenium(link):
#
#     # Set up Chrome options (optional: headless mode)
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--disable-gpu")  # Disable GPU rendering (for compatibility)
#     chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
#
#     # Automatically download and use the appropriate ChromeDriver
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#     try:
#         driver.get(link)
#         time.sleep(random.uniform(1, 3))
#         # print(driver.page_source)
#         if "Page Not Found" not in driver.page_source:
#              text = driver.find_element(By.TAG_NAME, "body").text
#              return text
#
#     except Exception as error:
#         print(f"Issue with this link: {error}")
#
#     finally:
#         driver.quit()
#
#     return None