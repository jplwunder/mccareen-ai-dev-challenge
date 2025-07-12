import requests

from api.src.ai_analyzer import get_company_profile


async def analyze_website(website_url):
    html_content = await fetch_html_content(str(website_url))
    company_profile = await get_company_profile(html_content)
    return company_profile


async def fetch_html_content(url):
    response = requests.get(url)
    response.raise_for_status()
    html_content = response.text
    return html_content
