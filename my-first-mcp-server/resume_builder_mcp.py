"""
Resume Builder MCP Server

A comprehensive MCP server for resume management, job matching, and mentor finding.
Features:
- Resume upload and parsing
- Job description analysis
- Resume optimization based on JD
- Mentor matching system
- Resume export in JSON format
"""

import json
import sqlite3
import re
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from mcp.server.fastmcp import FastMCP, Context
from api_requester import APIRequester



API_BASE_URL = "http://localhost:8000/api/v1"  # Update as needed
api = APIRequester(API_BASE_URL)

class ResumeParser:
    @staticmethod
    def extract_skills_from_text(text: str) -> List[str]:
        """Extract technical skills from resume text"""
        # Common technical skills patterns
        skill_patterns = [
            r'\b(?:Python|Java|JavaScript|TypeScript|C\+\+|C#|PHP|Ruby|Go|Rust|Swift|Kotlin)\b',
            r'\b(?:React|Angular|Vue|Node\.js|Express|Django|Flask|Spring|Laravel)\b',
            r'\b(?:MySQL|PostgreSQL|MongoDB|Redis|Elasticsearch|Cassandra)\b',
            r'\b(?:AWS|Azure|GCP|Docker|Kubernetes|Jenkins|Git|GitHub|GitLab)\b',
            r'\b(?:Machine Learning|Deep Learning|AI|Data Science|Analytics)\b',
            r'\b(?:HTML|CSS|SASS|SCSS|Bootstrap|Tailwind)\b',
            r'\b(?:REST|GraphQL|API|Microservices|DevOps|Agile|Scrum)\b'
        ]
        
        skills = set()
        for pattern in skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.update(match.strip() for match in matches)
        
        return list(skills)
    
    @staticmethod
    def parse_resume_text(resume_text: str) -> Dict[str, Any]:
        """Parse resume text and extract structured information"""
        lines = resume_text.split('\n')
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, resume_text)
        email = email_match.group() if email_match else ""
        
        # Extract phone
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phone_match = re.search(phone_pattern, resume_text)
        phone = phone_match.group() if phone_match else ""
        
        # Extract name (assume first line or line with name pattern)
        name = lines[0].strip() if lines else ""
        
        # Extract skills
        skills = ResumeParser.extract_skills_from_text(resume_text)
        
        return {
            'name': name,
            'email': email,
            'phone': phone,
            'skills': skills,
            'raw_text': resume_text
        }


class JobDescriptionAnalyzer:
    @staticmethod
    def extract_required_skills(jd_text: str) -> List[str]:
        """Extract required skills from job description"""
        return ResumeParser.extract_skills_from_text(jd_text)
    
    @staticmethod
    def analyze_job_description(jd_text: str) -> Dict[str, Any]:
        """Analyze job description and extract key information"""
        skills = JobDescriptionAnalyzer.extract_required_skills(jd_text)
        
        # Extract experience requirements
        exp_pattern = r'(\d+)[\+\-\s]*(?:years?|yrs?).*?(?:experience|exp)'
        exp_match = re.search(exp_pattern, jd_text, re.IGNORECASE)
        required_experience = exp_match.group(1) if exp_match else "0"
        
        # Extract key responsibilities
        responsibility_keywords = ['responsible', 'duties', 'requirements', 'qualifications']
        responsibilities = []
        
        for line in jd_text.split('\n'):
            if any(keyword in line.lower() for keyword in responsibility_keywords):
                responsibilities.append(line.strip())
        
        return {
            'required_skills': skills,
            'required_experience': required_experience,
            'responsibilities': responsibilities,
            'raw_text': jd_text
        }


# Initialize FastMCP server with database context
@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Manage application lifecycle with database"""
    try:
        yield {"test": 'test'}
    finally:
        # Cleanup if needed
        pass


mcp = FastMCP("Resume Builder", lifespan=app_lifespan)




@mcp.prompt(name="JD Analyis Prompt")
def Analyse_JD(JD: str) -> str:
    return f"Please analyse below JD and share the skills, experience, roles and responsiblities in a josn"




# @mcp.tool()
# def upload_resume(resume_text: str, ctx: Context) -> str:
#     # extracts a json of user    
#     parsed_data = ResumeParser.parse_resume_text(resume_text)
#     if not parsed_data['email']:
#         return json.dumps({"error": "Could not extract email from resume"})

#     # 1. Create user
#     user_payload = {
#         "email": parsed_data['email'],
#         "name": parsed_data['name'],
#         "password": "TempPassword123!"  # Or generate securely
#     }
#     user_resp = api.request("POST", "/auth/signup", json=user_payload)
#     if "id" not in user_resp:
#         return json.dumps({"error": "User creation failed", "details": user_resp})

#     user_id = user_resp["id"]

#     # 2. Add skills
#     for skill in parsed_data['skills']:
#         skill_payload = {
#             "skill_id": None,  # If you have skill IDs, use them; else, create skill first
#             "proficiency_level": 8.0,
#             "years_experience": 1,
#             "description": "",
#         }
#         api.request("POST", f"/skills/add-skill", json=skill_payload)

#     return json.dumps({
#         "user_id": user_id,
#         "message": "Resume uploaded successfully",
#         "extracted_data": parsed_data
#     })


# @mcp.tool()
# def add_experience(user_id: str, experiences_json: str, ctx: Context) -> str:
#     try:
#         experiences_data = json.loads(experiences_json)
#         for exp_data in experiences_data:
#             exp_resp = api.request("POST", "/experience", json={**exp_data, "user_id": user_id})
#             if "error" in exp_resp:
#                 return json.dumps({"error": "Failed to add experience", "details": exp_resp})
#         return json.dumps({"message": "Experience added successfully"})
#     except Exception as e:
#         return json.dumps({"error": f"Failed to add experience: {str(e)}"})


# @mcp.tool()
# def add_education(user_id: str, education_json: str, ctx: Context) -> str:
#     try:
#         education_data = json.loads(education_json)
#         for edu_data in education_data:
#             edu_resp = api.request("POST", "/education", json={**edu_data, "user_id": user_id})
#             if "error" in edu_resp:
#                 return json.dumps({"error": "Failed to add education", "details": edu_resp})
#         return json.dumps({"message": "Education added successfully"})
#     except Exception as e:
#         return json.dumps({"error": f"Failed to add education: {str(e)}"})
    

# @mcp.tool()
# def get_resume_json(user_id: str, ctx: Context) -> str:
#     resp = api.request("GET", f"/mcp/resume/{user_id}")
#     return json.dumps(resp, indent=2)

# @mcp.tool()
# def analyse_jd(jd: str):
#     """
#     This tool  analyse the JD shared by the user and share the analysis

#     Args: 
#         jd (str): The job descripion of the job user wants to pursue.

#     Returns: 
#         str: A JSON string representing the analysis of the jd (consisting experience required, skills required, roles and responsibilities)
#     """

#     return {'Analysis': 'Analysed JD'}


@mcp.prompt(name='Resume Updte prompt')
def resume_update_prompt(resume , jd_analysis):
    return f"Can you please update {resume} to make it suitable for below {jd_analysis}"

@mcp.tool()
def update_resume_according_to_jd(resume: str, jd: str, ) -> str:
    """
    Updates a user's resume to better match a given job description (JD) without changing the core content.

    This tool analyzes the provided resume and job description, then reorders, highlights, or emphasizes relevant sections
    and skills in the resume to better align with the requirements of the JD. The core information of the resume is preserved.

    Args:
        resume (str): The user's resume in JSON string format.
        jd (str): The job description text.

    Returns:
        str: A JSON string representing the updated resume, optimized for the provided JD.
    """
    # Example placeholder logic (replace with LLM or rule-based logic as needed)
    import json

    try:
        resume_data = json.loads(resume)
    except Exception as e:
        return json.dumps({"error": f"Invalid resume JSON: {str(e)}"})

    # --- Placeholder: Add your JD matching logic here ---
    # For demonstration, we'll just add a field indicating the resume was "optimized" for the JD.
    resume_data["optimized_for_jd"] = jd[:100]  # Store first 100 chars of JD for traceability

    # You can implement keyword matching, skill highlighting, or section reordering here.

    return json.dumps(resume_data, indent=2)