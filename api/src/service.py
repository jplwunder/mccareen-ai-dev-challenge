import requests
import re

from api.src.utils.logger import get_logger, LogLevel
from api.src.utils.document_converter import convert_document_to_markdown

logger = get_logger("service", level=LogLevel.DEBUG)


def analyze_website(website_url):
    """Mock function to analyze a website and generate a business profile."""
    all_domain_urls = [
        url
        for url in fetch_html_urls(website_url)
        if not re.search(
            r"\.(pdf|jpg|jpeg|png|gif|bmp|svg|docx?|xlsx?|pptx?|zip|rar|tar\.gz|mp3|mp4|avi|mov|wmv|flv|mkv|css)(\?|$)",
            str(url),
            re.IGNORECASE,
        )
    ]

    # Fetch and store the HTML content of each domain URL in memory
    converted_html_contents_to_markdown = {}
    for url in all_domain_urls:
        try:
            converted_html_contents_to_markdown[url] = convert_document_to_markdown(
                str(url)
            )
        except Exception as e:
            logger.error(f"Failed to fetch content from {url}: {e}")

    all_markdown_content = "\n\n".join(converted_html_contents_to_markdown.values())

    # Mock response for demonstration
    mock_profile = {
        "company_name": "Example Company",
        "service_lines": [
            "Web Development",
            "Mobile App Development",
            "Cloud Services",
        ],
        "company_description": "A leading technology company providing innovative solutions for businesses worldwide.",
        "tier1_keywords": [
            "technology",
            "innovation",
            "solutions",
            "business",
            "software",
        ],
        "tier2_keywords": [
            "AI",
            "machine learning",
            "automation",
        ],
        "emails": ["contact@example.com"],
        "point_of_contact": "John Doe",
    }

    return mock_profile


def fetch_html_urls(url, max_depth=2, _visited=None, _depth=0, _html_contents=None):
    if _visited is None:
        _visited = set()
    if _html_contents is None:
        _html_contents = {}
    if url in _visited or _depth >= max_depth:
        return [], _html_contents

    _visited.add(url)
    try:
        response = requests.get(url)
        if _depth == 0:
            response.raise_for_status()
        html_content = response.text
        _html_contents[url] = html_content
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return [], _html_contents

    main_domain_match = re.search(r"http[s]?://(?:www\.)?([^./]+)", str(url))
    main_domain = main_domain_match.group(1) if main_domain_match else ""

    pattern = r"http[s]?://(?:www\.)?" + re.escape(main_domain) + r"[^ \t\n\r\"'>]*"
    http_urls = re.findall(
        pattern,
        html_content,
    )
    domain_urls = [u for u in http_urls if main_domain in u]

    # Recursively search for domain_urls inside each found domain_url
    all_urls = set(domain_urls)
    for next_url in domain_urls:
        nested_urls, _html_contents = fetch_html_urls(
            next_url,
            max_depth=max_depth,
            _visited=_visited,
            _depth=_depth + 1,
            _html_contents=_html_contents,
        )
        all_urls.update(nested_urls)

    return list(all_urls) + [str(url)], _html_contents
