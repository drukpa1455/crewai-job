from pydantic import BaseModel, EmailStr, constr, conlist, Field
from typing import List, Optional
from datetime import date

class TechnicalSkill(BaseModel):
    category: constr(min_length=1, max_length=30)
    skills: constr(min_length=1, max_length=150)

class Experience(BaseModel):
    job_title: constr(min_length=1, max_length=50)
    company: constr(min_length=1, max_length=50)
    date_range: constr(min_length=1, max_length=30)
    responsibilities: conlist(constr(min_length=1, max_length=120), min_length=1, max_length=3)

class Education(BaseModel):
    degree: constr(min_length=1, max_length=50)
    institution: constr(min_length=1, max_length=50)
    year: constr(min_length=4, max_length=4)
    achievements: conlist(constr(min_length=1, max_length=100), min_length=0, max_length=2)

class CV(BaseModel):
    full_name: constr(min_length=1, max_length=50)
    job_title: constr(min_length=1, max_length=50)
    location: constr(min_length=1, max_length=50)
    email: EmailStr
    phone: constr(min_length=10, max_length=20)
    linkedin: constr(min_length=1, max_length=100)
    professional_summary: constr(min_length=50, max_length=300)
    technical_skills: conlist(TechnicalSkill, min_length=1, max_length=5)
    experience: conlist(Experience, min_length=1, max_length=3)
    education: conlist(Education, min_length=1, max_length=2)
    certifications: conlist(constr(min_length=1, max_length=40), min_length=0, max_length=5)

class CoverLetter(BaseModel):
    full_name: constr(min_length=1, max_length=50)
    address: constr(min_length=1, max_length=100)
    city: constr(min_length=1, max_length=50)
    state: constr(min_length=2, max_length=2)
    zip: constr(min_length=5, max_length=10)
    email: EmailStr
    phone: constr(min_length=10, max_length=20)
    date: date
    hiring_manager_name: constr(min_length=1, max_length=50)
    job_title: constr(min_length=1, max_length=50)
    company_name: constr(min_length=1, max_length=50)
    company_address: constr(min_length=1, max_length=100)
    company_city: constr(min_length=1, max_length=50)
    company_state: constr(min_length=2, max_length=2)
    company_zip: constr(min_length=5, max_length=10)
    paragraphs: conlist(constr(min_length=50, max_length=800), min_length=3, max_length=3)
    closing_paragraph: constr(min_length=20, max_length=300)

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "John Doe",
                "address": "123 Main St",
                "city": "Miami",
                "state": "FL",
                "zip": "33101",
                "email": "john.doe@email.com",
                "phone": "(305) 555-0123",
                "date": "2024-02-07",
                "hiring_manager_name": "Jane Smith",
                "job_title": "Hiring Manager",
                "company_name": "Tech Solutions Inc",
                "company_address": "456 Business Ave",
                "company_city": "San Francisco",
                "company_state": "CA",
                "company_zip": "94105",
                "paragraphs": [
                    "Introduction paragraph (100-150 words)",
                    "Experience and qualifications paragraph (100-150 words)",
                    "Company specific interest paragraph (100-150 words)"
                ],
                "closing_paragraph": "Thank you for considering my application."
            }
        } 