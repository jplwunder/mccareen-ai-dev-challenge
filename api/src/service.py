import requests

from api.src.logger import get_logger, LogLevel
from api.src.ai_analyzer import get_company_profile

logger = get_logger("service", level=LogLevel.DEBUG)


def analyze_website(website_url):
    html_content = fetch_html_content(str(website_url))
    company_profile = get_company_profile(html_content)
    return company_profile


def fetch_html_content(url):
    response = requests.get(url)
    response.raise_for_status()
    html_content = response.text
    return html_content
