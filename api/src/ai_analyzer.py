import os
import asyncio

from google import genai
from google.genai import types as genai_types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


# Helper function to run the async get_company_profile in sync contexts
def get_company_profile_sync(website_content) -> dict:
    """
    Synchronous wrapper for the async get_company_profile function.
    Use this when calling from synchronous code.
    """
    return asyncio.run(get_company_profile(website_content))


async def get_company_profile(website_content) -> dict:
    try:
        markdown_content = await convert_html_to_markdown(website_content)

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

        tasks = [
            extract_company_name_from_markdown(markdown_content),
            extract_service_lines_from_markdown(markdown_content),
            extract_company_description_from_markdown(markdown_content),
            extract_tier1_keywords_from_markdown(markdown_content),
            extract_emails_from_markdown(markdown_content),
            extract_point_of_contact_from_markdown(markdown_content),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                print(f"Error in extraction: {result}")
                processed_results.append("Unknown")
            else:
                processed_results.append(result)

        (
            company_name,
            service_lines,
            company_description,
            tier_1_keywords,
            emails,
            point_of_contact,
        ) = processed_results

        try:
            tier_2_keywords = (
                await extract_tier2_keywords_from_markdown_and_previous_tier_1_keywords(
                    markdown_content, tier_1_keywords
                )
            )
        except Exception as e:
            print(f"Error extracting tier 2 keywords: {e}")
            tier_2_keywords = "Unknown"

        return {
            "company_name": company_name,
            "service_lines": service_lines.split(",")
            if service_lines and service_lines != "Unknown"
            else ["Unknown"],
            "company_description": company_description,
            "tier1_keywords": tier_1_keywords.split(",")
            if tier_1_keywords and tier_1_keywords != "Unknown"
            else ["Unknown"],
            "tier2_keywords": tier_2_keywords.split(",")
            if tier_2_keywords and tier_2_keywords != "Unknown"
            else ["Unknown"],
            "emails": emails.split(",")
            if emails and emails != "Unknown"
            else ["Unknown"],
            "point_of_contact": point_of_contact,
        }

    except Exception as e:
        print(f"Error in get_company_profile: {e}")
        return {
            "company_name": "Unknown",
            "service_lines": ["Unknown"],
            "company_description": "Unknown",
            "tier1_keywords": ["Unknown"],
            "tier2_keywords": ["Unknown"],
            "emails": ["Unknown"],
            "point_of_contact": "Unknown",
        }


async def convert_html_to_markdown(html_content: str) -> str | None:
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        config=genai_types.GenerateContentConfig(
            system_instruction="You are a HTML to Markdown converter. Convert the input HTML to markdown format."
        ),
        contents=html_content,
    )
    return response.text


async def extract_company_name_from_markdown(markdown_content: str) -> str:
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        config=genai_types.GenerateContentConfig(
            system_instruction="You are a company name extractor. Extract a SINGLE company name from the provided markdown content. There should be no other text in the response. Do not include any additional information or context."
        ),
        contents=markdown_content,
    )
    return response.text if response.text else "Unknown"


async def extract_service_lines_from_markdown(markdown_content: str) -> str:
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        config=genai_types.GenerateContentConfig(
            system_instruction="You are a service line extractor. Extract service lines for the company being described in the markdown content input. Return a list of service lines separated by comma. There should be no other text in the response."
        ),
        contents=markdown_content,
    )
    return response.text if response.text else "Unknown"


async def extract_company_description_from_markdown(markdown_content: str) -> str:
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        config=genai_types.GenerateContentConfig(
            system_instruction="You are a company description extractor. Extract the company description from the input markdown content. There should be no other text in the response."
        ),
        contents=markdown_content,
    )
    return response.text if response.text else "Unknown"


async def extract_tier1_keywords_from_markdown(markdown_content: str) -> str:
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        config=genai_types.GenerateContentConfig(
            system_instruction="You are a company keyword extractor. Extract keywords that this company would DEFINITELY use to search for public government opportunities (e.g., 'solar' would be a good keyword for a company that sells solar panels). Return a list of keywords separated by comma. There should be no other text in the response."
        ),
        contents=markdown_content,
    )
    return response.text if response.text else "Unknown"


async def extract_tier2_keywords_from_markdown_and_previous_tier_1_keywords(
    markdown_content: str, tier_1_keywords: str
) -> str:
    response = await client.aio.models.generate_content(
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
    return response.text if response.text else "Unknown"


async def extract_emails_from_markdown(markdown_content: str) -> str:
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        config=genai_types.GenerateContentConfig(
            system_instruction="You are an email extractor. Extract all emails from the input markdown content. Return a list of emails separated by comma. There should be no other text in the response. If no emails are found, return an empty list."
        ),
        contents=markdown_content,
    )
    return response.text if response.text else "Unknown"


async def extract_point_of_contact_from_markdown(markdown_content: str) -> str:
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        config=genai_types.GenerateContentConfig(
            system_instruction="You are a point of contact extractor. Extract the point of contact from the input markdown content. There should be no other text in the response. If uncertain, return 'Unknown'."
        ),
        contents=markdown_content,
    )
    return response.text if response.text else "Unknown"
