def build_resume_analysis_prompt(resume_text: str, job_description: str) -> str:
    return f"""
Analyze the resume against the job description.

Return concise, practical results.

Rules:
- match_score must be an integer from 0 to 100.
- strengths should contain 6 to 10 concise skills, technologies, or qualifications.
- Strengths should be short labels or keywords, usually 1 to 4 words.
- Prefer specific technologies and technical skills over explanations.
- Do not write full sentences in strengths.
- Do not combine multiple unrelated skills into one item.
- Example strengths: "Java", "AWS Lambda", "REST APIs", "SQL Server", "CI/CD", "Git", "Backend Development".
- Do not include location, work authorization, graduation status, or other logistical information as a strength.
- skill_gaps should contain 3 to 6 concise skills, technologies, or areas where the job description expects more evidence than the resume currently provides.
- A skill gap does not necessarily mean the candidate has no experience with the skill.
- Only identify a gap when the job description clearly emphasizes it and the resume does not provide strong evidence of it.
- Do not treat a skill as a gap simply because the resume does not use the exact same wording as the job description.
- Skill gaps should usually be 1 to 5 words.
- Do not write full sentences in skill_gaps.
- relevant_experience should contain 4 to 6 short items describing experience from the resume that directly relates to the job.
- Keep relevant_experience concise and specific.
- recommendations should contain 3 to 5 short, actionable suggestions.
- Keep recommendations concise and practical.
- Do not repeat the same information across multiple sections.
- Use the resume as the source of truth for the candidate's education and experience.
- Do not claim that a degree is still in progress if the resume indicates that it has already been completed.
- Do not invent experience, skills, technologies, or qualifications that are not supported by the resume.
- Recognize technologies and frameworks that are commonly used to satisfy the same requirement.
- Do not identify a skill as a gap when the resume demonstrates equivalent or directly related experience.
- For example, AWS SAM, AWS CDK, and CloudFormation should be recognized as Infrastructure as Code experience.
- Consider the candidate's actual work and project descriptions, not only exact keyword matches.

Resume:
{resume_text}

Job Description:
{job_description}
"""

def build_job_description_check_prompt(text: str) -> str:
    return f"""
Determine whether the following scraped webpage text contains an actual job posting.

Return true if the text contains substantive job-specific information such as:
- Job title
- Job description
- Responsibilities
- Qualifications
- Requirements
- Required skills or experience
- Employment details

Return false if the text is primarily:
- Website navigation
- Login/signup information
- Headers or footers
- Generic company information
- Cookie notices
- Search results
- Other webpage content without an actual job posting

Do not require every category above to be present.
The text only needs to contain enough substantive information to clearly represent a job posting.

Return only the structured result.

Scraped webpage text:
{text}
"""