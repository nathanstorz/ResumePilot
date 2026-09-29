import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ResumeAnalysis(BaseModel):
    match_score: int
    strengths: list[str]
    skill_gaps: list[str]
    relevant_experience: list[str]
    recommendations: list[str]

def analyze_resume(prompt: str):
    response = client.responses.parse(
        model="gpt-5.6-luna",
        input=prompt,
        text_format=ResumeAnalysis
    )

    return response.output_parsed

def extract_job_description(page_text: str):
    prompt = f"""
You are cleaning text scraped from a company's career webpage.

The webpage may contain navigation menus, buttons, headers, footers,
cookie notices, legal text, privacy policies, and other unrelated content.

Your job is to extract ONLY the information that belongs to the actual
job posting.

Keep:
- Job title
- Company name
- Location
- Job summary or description
- Responsibilities
- Required qualifications
- Preferred qualifications
- Required/preferred skills
- Technologies
- Education requirements
- Experience requirements
- Salary or compensation information if present
- Other information useful for evaluating a candidate for the position

Remove:
- Navigation menus
- Buttons
- Cookie notices
- Privacy policies
- Terms of use
- Equal opportunity/legal boilerplate
- Unrelated company website content
- Repeated text
- Footer content
- "Apply now" or similar interface text

Return the cleaned job posting as plain text.
Do not analyze the candidate.
Do not score the job.
Do not add information that is not present in the scraped text.

If the content does not contain a job description, you must return "No job posting content found."

Scraped webpage text:
{page_text}
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    return response.output_text

class JobDescriptionCheck(BaseModel):
    contains_job_description: bool


def contains_job_description(text: str):
    prompt = f"""
Determine whether the following scraped webpage text contains an actual job posting.

Return true if the text contains substantive job-specific information such as:
- Job title
- Job description
- Responsibilities
- Qualifications
- Requirements
- Required skills or experience
- Employment details

Return false if the text does not contain a job role description

Do not require every category above to be present. The text only needs to contain enough substantive information to clearly represent a job posting.

Return only the structured result.

Scraped webpage text:
{text}
"""

    response = client.responses.parse(
        model="gpt-5.6-luna",
        input=prompt,
        text_format=JobDescriptionCheck
    )

    return response.output_parsed.contains_job_description
