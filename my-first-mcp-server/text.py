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


@dataclass
class PersonalInfo:
    name: str
    email: str
    phone: str
    address: str
    linkedin: str = ""
    github: str = ""


@dataclass
class Experience:
    company: str
    position: str
    start_date: str
    end_date: str
    description: str
    skills_used: List[str]


@dataclass
class Education:
    institution: str
    degree: str
    field: str
    graduation_date: str
    gpa: str = ""


@dataclass
class UserProfile:
    user_id: str
    personal_info: PersonalInfo
    skills: List[str]
    experiences: List[Experience]
    education: List[Education]
    certifications: List[str]


class DatabaseManager:
    def __init__(self, db_path: str = "resume_builder.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                address TEXT,
                linkedin TEXT,
                github TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Skills table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                skill_name TEXT NOT NULL,
                proficiency_level TEXT DEFAULT 'intermediate',
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        
        # Experience table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS experience (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                company TEXT NOT NULL,
                position TEXT NOT NULL,
                start_date TEXT,
                end_date TEXT,
                description TEXT,
                skills_used TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        
        # Education table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS education (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                institution TEXT NOT NULL,
                degree TEXT NOT NULL,
                field TEXT,
                graduation_date TEXT,
                gpa TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        
        # Certifications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS certifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                certification_name TEXT NOT NULL,
                issuing_organization TEXT,
                issue_date TEXT,
                expiry_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        
        # Job descriptions table for analysis
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_descriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                company TEXT,
                position TEXT,
                description TEXT,
                required_skills TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_user(self, user_data: PersonalInfo) -> str:
        """Create a new user and return user_id"""
        user_id = hashlib.md5(f"{user_data.email}{datetime.now()}".encode()).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO users 
            (user_id, name, email, phone, address, linkedin, github)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, user_data.name, user_data.email, user_data.phone, 
              user_data.address, user_data.linkedin, user_data.github))
        
        conn.commit()
        conn.close()
        return user_id
    
    def add_skills(self, user_id: str, skills: List[str]):
        """Add skills for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clear existing skills
        cursor.execute("DELETE FROM skills WHERE user_id = ?", (user_id,))
        
        for skill in skills:
            cursor.execute("""
                INSERT INTO skills (user_id, skill_name)
                VALUES (?, ?)
            """, (user_id, skill.strip()))
        
        conn.commit()
        conn.close()
    
    def add_experience(self, user_id: str, experiences: List[Experience]):
        """Add work experiences for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clear existing experience
        cursor.execute("DELETE FROM experience WHERE user_id = ?", (user_id,))
        
        for exp in experiences:
            cursor.execute("""
                INSERT INTO experience 
                (user_id, company, position, start_date, end_date, description, skills_used)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, exp.company, exp.position, exp.start_date, 
                  exp.end_date, exp.description, json.dumps(exp.skills_used)))
        
        conn.commit()
        conn.close()
    
    def add_education(self, user_id: str, education: List[Education]):
        """Add education records for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clear existing education
        cursor.execute("DELETE FROM education WHERE user_id = ?", (user_id,))
        
        for edu in education:
            cursor.execute("""
                INSERT INTO education 
                (user_id, institution, degree, field, graduation_date, gpa)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, edu.institution, edu.degree, edu.field, 
                  edu.graduation_date, edu.gpa))
        
        conn.commit()
        conn.close()
    
    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get complete user profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get user info
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user_row = cursor.fetchone()
        if not user_row:
            conn.close()
            return None
        
        personal_info = PersonalInfo(
            name=user_row[1], email=user_row[2], phone=user_row[3],
            address=user_row[4], linkedin=user_row[5], github=user_row[6]
        )
        
        # Get skills
        cursor.execute("SELECT skill_name FROM skills WHERE user_id = ?", (user_id,))
        skills = [row[0] for row in cursor.fetchall()]
        
        # Get experience
        cursor.execute("SELECT * FROM experience WHERE user_id = ?", (user_id,))
        experiences = []
        for row in cursor.fetchall():
            exp = Experience(
                company=row[2], position=row[3], start_date=row[4],
                end_date=row[5], description=row[6],
                skills_used=json.loads(row[7]) if row[7] else []
            )
            experiences.append(exp)
        
        # Get education
        cursor.execute("SELECT * FROM education WHERE user_id = ?", (user_id,))
        education = []
        for row in cursor.fetchall():
            edu = Education(
                institution=row[2], degree=row[3], field=row[4],
                graduation_date=row[5], gpa=row[6]
            )
            education.append(edu)
        
        # Get certifications
        cursor.execute("SELECT certification_name FROM certifications WHERE user_id = ?", (user_id,))
        certifications = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        
        return UserProfile(
            user_id=user_id, personal_info=personal_info, skills=skills,
            experiences=experiences, education=education, certifications=certifications
        )
    
    def find_mentors_by_skills(self, required_skills: List[str]) -> List[Dict]:
        """Find users who have the required skills"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Find users with matching skills
        skills_placeholder = ','.join(['?' for _ in required_skills])
        query = f"""
            SELECT DISTINCT u.user_id, u.name, u.email, u.linkedin, u.github,
                   GROUP_CONCAT(s.skill_name) as matching_skills
            FROM users u
            JOIN skills s ON u.user_id = s.user_id
            WHERE s.skill_name IN ({skills_placeholder})
            GROUP BY u.user_id, u.name, u.email, u.linkedin, u.github
            ORDER BY COUNT(s.skill_name) DESC
        """
        
        cursor.execute(query, required_skills)
        mentors = []
        for row in cursor.fetchall():
            mentors.append({
                'user_id': row[0],
                'name': row[1],
                'email': row[2],
                'linkedin': row[3],
                'github': row[4],
                'matching_skills': row[5].split(',') if row[5] else []
            })
        
        conn.close()
        return mentors


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
    db_manager = DatabaseManager()
    try:
        yield {"db": db_manager}
    finally:
        # Cleanup if needed
        pass


mcp = FastMCP("Resume Builder", lifespan=app_lifespan)


@mcp.tool()
def upload_resume(resume_text: str, ctx: Context) -> str:
    """
    Upload and parse a resume to extract user information.
    
    Args:
        resume_text: The complete text content of the resume
    
    Returns:
        JSON string containing user_id and extracted information
    """
    db: DatabaseManager = ctx.lifespan_context["db"]
    
    # Parse resume
    parsed_data = ResumeParser.parse_resume_text(resume_text)
    
    if not parsed_data['email']:
        return json.dumps({"error": "Could not extract email from resume"})
    
    # Create user profile
    personal_info = PersonalInfo(
        name=parsed_data['name'],
        email=parsed_data['email'],
        phone=parsed_data['phone'],
        address="",  # Would need more sophisticated parsing
        linkedin="",
        github=""
    )
    
    # Create user
    user_id = db.create_user(personal_info)
    
    # Add skills
    if parsed_data['skills']:
        db.add_skills(user_id, parsed_data['skills'])
    
    return json.dumps({
        "user_id": user_id,
        "message": "Resume uploaded successfully",
        "extracted_data": {
            "name": parsed_data['name'],
            "email": parsed_data['email'],
            "phone": parsed_data['phone'],
            "skills": parsed_data['skills']
        }
    })


@mcp.tool()
def add_experience(user_id: str, experiences_json: str, ctx: Context) -> str:
    """
    Add work experience to user profile.
    
    Args:
        user_id: User identifier
        experiences_json: JSON string containing list of experience objects
    
    Returns:
        Success/error message
    """
    db: DatabaseManager = ctx.lifespan_context["db"]
    
    try:
        experiences_data = json.loads(experiences_json)
        experiences = []
        
        for exp_data in experiences_data:
            exp = Experience(
                company=exp_data['company'],
                position=exp_data['position'],
                start_date=exp_data['start_date'],
                end_date=exp_data['end_date'],
                description=exp_data['description'],
                skills_used=exp_data.get('skills_used', [])
            )
            experiences.append(exp)
        
        db.add_experience(user_id, experiences)
        return json.dumps({"message": "Experience added successfully"})
    
    except Exception as e:
        return json.dumps({"error": f"Failed to add experience: {str(e)}"})


@mcp.tool()
def add_education(user_id: str, education_json: str, ctx: Context) -> str:
    """
    Add education information to user profile.
    
    Args:
        user_id: User identifier
        education_json: JSON string containing list of education objects
    
    Returns:
        Success/error message
    """
    db: DatabaseManager = ctx.lifespan_context["db"]
    
    try:
        education_data = json.loads(education_json)
        education_list = []
        
        for edu_data in education_data:
            edu = Education(
                institution=edu_data['institution'],
                degree=edu_data['degree'],
                field=edu_data['field'],
                graduation_date=edu_data['graduation_date'],
                gpa=edu_data.get('gpa', '')
            )
            education_list.append(edu)
        
        db.add_education(user_id, education_list)
        return json.dumps({"message": "Education added successfully"})
    
    except Exception as e:
        return json.dumps({"error": f"Failed to add education: {str(e)}"})


@mcp.tool()
def optimize_resume_for_jd(user_id: str, job_description: str, ctx: Context) -> str:
    """
    Optimize user's resume based on job description requirements.
    
    Args:
        user_id: User identifier
        job_description: The job description text to match against
    
    Returns:
        JSON string with optimization suggestions and updated resume
    """
    db: DatabaseManager = ctx.lifespan_context["db"]
    
    # Get user profile
    user_profile = db.get_user_profile(user_id)
    if not user_profile:
        return json.dumps({"error": "User not found"})
    
    # Analyze job description
    jd_analysis = JobDescriptionAnalyzer.analyze_job_description(job_description)
    required_skills = jd_analysis['required_skills']
    
    # Find skill gaps
    user_skills = set(skill.lower() for skill in user_profile.skills)
    required_skills_lower = set(skill.lower() for skill in required_skills)
    
    matching_skills = user_skills.intersection(required_skills_lower)
    missing_skills = required_skills_lower - user_skills
    
    # Generate optimization suggestions
    suggestions = {
        "matching_skills": list(matching_skills),
        "missing_skills": list(missing_skills),
        "skill_match_percentage": len(matching_skills) / len(required_skills_lower) * 100 if required_skills_lower else 0,
        "recommendations": []
    }
    
    # Add recommendations
    if missing_skills:
        suggestions["recommendations"].append(
            f"Consider adding these skills to your profile: {', '.join(missing_skills)}"
        )
    
    if suggestions["skill_match_percentage"] < 70:
        suggestions["recommendations"].append(
            "Your skill match is below 70%. Consider highlighting relevant experience or acquiring missing skills."
        )
    
    # Create optimized resume
    optimized_resume = {
        "personal_info": asdict(user_profile.personal_info),
        "skills": user_profile.skills,
        "experiences": [asdict(exp) for exp in user_profile.experiences],
        "education": [asdict(edu) for edu in user_profile.education],
        "certifications": user_profile.certifications,
        "optimization_analysis": suggestions
    }
    
    return json.dumps(optimized_resume, indent=2)


@mcp.tool()
def find_mentors(required_skills_json: str, ctx: Context) -> str:
    """
    Find mentors with specific skills from the user database.
    
    Args:
        required_skills_json: JSON array of required skills to search for
    
    Returns:
        JSON string containing mentor information and contact details
    """
    db: DatabaseManager = ctx.lifespan_context["db"]
    
    try:
        required_skills = json.loads(required_skills_json)
        mentors = db.find_mentors_by_skills(required_skills)
        
        result = {
            "mentors_found": len(mentors),
            "mentors": mentors,
            "search_criteria": required_skills
        }
        
        return json.dumps(result, indent=2)
    
    except Exception as e:
        return json.dumps({"error": f"Failed to find mentors: {str(e)}"})


@mcp.tool()
def update_resume_with_prompt(user_id: str, update_prompt: str, ctx: Context) -> str:
    """
    Update resume based on user's specific instructions/prompts.
    
    Args:
        user_id: User identifier
        update_prompt: User's instructions for updating the resume
    
    Returns:
        JSON string with updated resume structure
    """
    db: DatabaseManager = ctx.lifespan_context["db"]
    
    user_profile = db.get_user_profile(user_id)
    if not user_profile:
        return json.dumps({"error": "User not found"})
    
    # Parse update prompt for common update patterns
    prompt_lower = update_prompt.lower()
    
    updates_applied = []
    
    # Skill updates
    if 'add skill' in prompt_lower or 'new skill' in prompt_lower:
        # Extract skills from prompt
        new_skills = ResumeParser.extract_skills_from_text(update_prompt)
        if new_skills:
            existing_skills = set(skill.lower() for skill in user_profile.skills)
            unique_new_skills = [skill for skill in new_skills if skill.lower() not in existing_skills]
            
            if unique_new_skills:
                user_profile.skills.extend(unique_new_skills)
                db.add_skills(user_id, user_profile.skills)
                updates_applied.append(f"Added skills: {', '.join(unique_new_skills)}")
    
    # Generate updated resume
    updated_resume = {
        "user_id": user_id,
        "personal_info": asdict(user_profile.personal_info),
        "skills": user_profile.skills,
        "experiences": [asdict(exp) for exp in user_profile.experiences],
        "education": [asdict(edu) for edu in user_profile.education],
        "certifications": user_profile.certifications,
        "updates_applied": updates_applied,
        "original_prompt": update_prompt
    }
    
    return json.dumps(updated_resume, indent=2)


@mcp.tool()
def get_resume_json(user_id: str, ctx: Context) -> str:
    """
    Get complete resume in JSON format.
    
    Args:
        user_id: User identifier
    
    Returns:
        Complete resume in JSON structure
    """
    db: DatabaseManager = ctx.lifespan_context["db"]
    
    user_profile = db.get_user_profile(user_id)
    if not user_profile:
        return json.dumps({"error": "User not found"})
    
    resume_json = {
        "user_id": user_id,
        "personal_info": asdict(user_profile.personal_info),
        "skills": user_profile.skills,
        "experiences": [asdict(exp) for exp in user_profile.experiences],
        "education": [asdict(edu) for edu in user_profile.education],
        "certifications": user_profile.certifications,
        "generated_at": datetime.now().isoformat()
    }
    
    return json.dumps(resume_json, indent=2)


@mcp.resource("user://{user_id}/profile")
def get_user_profile_resource(user_id: str, ctx: Context) -> str:
    """Get user profile as a resource"""
    db: DatabaseManager = ctx.lifespan_context["db"]
    
    user_profile = db.get_user_profile(user_id)
    if not user_profile:
        return "User not found"
    
    return f"""
User Profile: {user_profile.personal_info.name}
Email: {user_profile.personal_info.email}
Skills: {', '.join(user_profile.skills)}
Experience: {len(user_profile.experiences)} positions
Education: {len(user_profile.education)} degrees
"""


@mcp.prompt()
def resume_optimization_prompt(user_skills: str, job_requirements: str) -> str:
    """Generate a prompt for resume optimization"""
    return f"""
Based on the following information, provide detailed suggestions for optimizing a resume:

Current Skills: {user_skills}
Job Requirements: {job_requirements}

Please analyze:
1. Skill gaps and recommendations
2. Experience highlighting strategies
3. Keywords to include
4. Sections to emphasize
5. Overall resume structure improvements
"""


if __name__ == "__main__":
    mcp.run()