import os

from google import genai
from google.genai import types as genai_types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def get_company_profile(website_content) -> dict:
    markdown_content = convert_html_to_markdown(website_content)

    if markdown_content is None:
        return {
            "company_name": "Unknown",
            "service_lines": "Unknown",
            "company_description": "Unknown",
            "tier1_keywords": "Unknown",
            "tier2_keywords": "Unknown",
            "emails": "Unknown",
            "point_of_contact": "Unknown",
        }

    company_name = extract_company_name_from_markdown(markdown_content)
    service_lines = extract_service_lines_from_markdown(markdown_content)
    company_description = extract_company_description_from_markdown(markdown_content)
    tier_1_keywords = extract_tier1_keywords_from_markdown(markdown_content)
    tier_2_keywords = extract_tier2_keywords_from_markdown_and_previous_tier_1_keywords(
        markdown_content, tier_1_keywords
    )
    emails = extract_emails_from_markdown(markdown_content)
    point_of_contact = extract_point_of_contact_from_markdown(markdown_content)

    return {
        "company_name": company_name,
        "service_lines": service_lines.split(",") if service_lines else [],
        "company_description": company_description,
        "tier1_keywords": tier_1_keywords.split(",") if tier_1_keywords else [],
        "tier2_keywords": tier_2_keywords.split(",") if tier_2_keywords else [],
        "emails": emails.split(",") if emails else [],
        "point_of_contact": point_of_contact,
    }


def convert_html_to_markdown(html_content: str) -> str | None:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=genai_types.GenerateContentConfig(
            system_instruction="You are a HTML to Markdown converter. Convert the input HTML to markdown format."
        ),
        contents=html_content,
    )

    return response.text


def extract_company_name_from_markdown(markdown_content: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=genai_types.GenerateContentConfig(
            system_instruction="You are a company name extractor. Extract ONLY company name from the input markdown content. There should be no other text in the response."
        ),
        contents=markdown_content,
    )

    if not response.text:
        return "Unknown"

    return response.text


def extract_service_lines_from_markdown(markdown_content: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=genai_types.GenerateContentConfig(
            system_instruction="You are a service line extractor. Extract service lines for the company being described in the markdown content input. Return a list of service lines separated by comma. There should be no other text in the response."
        ),
        contents=markdown_content,
    )

    if not response.text:
        return "Unknown"

    return response.text


def extract_company_description_from_markdown(markdown_content: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=genai_types.GenerateContentConfig(
            system_instruction="You are a company description extractor. Extract the company description from the input markdown content. There should be no other text in the response."
        ),
        contents=markdown_content,
    )

    if not response.text:
        return "Unknown"

    return response.text


def extract_tier1_keywords_from_markdown(markdown_content: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=genai_types.GenerateContentConfig(
            system_instruction="You are a company keyword extractor. Extract keywords that this company would DEFINITELY use to search for public government opportunities (e.g., 'solar' would be a good keyword for a company that sells solar panels). Return a list of keywords separated by comma. There should be no other text in the response."
        ),
        contents=markdown_content,
    )

    if not response.text:
        return "Unknown"

    return response.text


def extract_tier2_keywords_from_markdown_and_previous_tier_1_keywords(
    markdown_content: str, tier_1_keywords: str
) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=genai_types.GenerateContentConfig(
            system_instruction=f"""You are a company keyword extractor. 
            Extract keywords that this company MIGHT use to search for public government opportunities, 
            but these keywords should be different than the tier 1 keywords provided: tier 1 keywords: {tier_1_keywords}. 
            Return a list of keywords separated by comma. 
            There should be no other text in the response."""
        ),
        contents=markdown_content,
    )

    if not response.text:
        return "Unknown"

    return response.text


def extract_emails_from_markdown(markdown_content: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=genai_types.GenerateContentConfig(
            system_instruction="You are an email extractor. Extract all emails from the input markdown content. Return a list of emails separated by comma. There should be no other text in the response. If no emails are found, return an empty list."
        ),
        contents=markdown_content,
    )

    if not response.text:
        return "Unknown"

    return response.text


def extract_point_of_contact_from_markdown(markdown_content: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=genai_types.GenerateContentConfig(
            system_instruction="You are a point of contact extractor. Extract the point of contact from the input markdown content. There should be no other text in the response. If uncertain, return 'Unknown'."
        ),
        contents=markdown_content,
    )

    if not response.text:
        return "Unknown"

    return response.text
