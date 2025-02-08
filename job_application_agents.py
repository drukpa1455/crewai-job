from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain.tools import tool
import requests
import os
from bs4 import BeautifulSoup
import json
import re
from pathlib import Path
from datetime import date
from models import CV, CoverLetter
from weasyprint import HTML
from PIL import Image
from pdf2image import convert_from_bytes
from pybars import Compiler

# Load environment variables
load_dotenv()

# Initialize the LLM
model = ChatOpenAI(model_name="gpt-4-turbo-preview", temperature=0.7)

# Tools
@tool
def read_text_file(file_path: str):
    """
    Reads a text file and returns the content 
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@tool
def write_text_file(file_path: str, content: str):
    """
    Writes content to a text file
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

@tool
def get_webpage_contents(url: str):
    """
    Reads the webpage with a given URL and returns the page content
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try multiple common selectors for job details
        title = ''
        company = ''
        location = ''
        description = ''

        # Title selectors
        title_selectors = ['h1', '.job-title', '.position-title', '[data-testid="job-title"]']
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                title = element.text.strip()
                break

        # Company selectors
        company_selectors = ['.company-name', '.employer', '[data-testid="company-name"]']
        for selector in company_selectors:
            element = soup.select_one(selector)
            if element:
                company = element.text.strip()
                break

        # Location selectors
        location_selectors = ['.location', '.job-location', '[data-testid="location"]']
        for selector in location_selectors:
            element = soup.select_one(selector)
            if element:
                location = element.text.strip()
                break

        # Description selectors
        description_selectors = ['.job-description', '.description', '#job-description', '[data-testid="job-description"]']
        for selector in description_selectors:
            element = soup.select_one(selector)
            if element:
                description = element.text.strip()
                break

        # If we couldn't find the description with specific selectors, try to get the main content
        if not description:
            # Try to get the largest text content block
            content_blocks = soup.find_all(['div', 'section', 'article'])
            if content_blocks:
                # Sort by content length and get the largest
                description = max(content_blocks, key=lambda x: len(x.text.strip())).text.strip()

        job_content = {
            'title': title or 'Position Title Not Found',
            'company': company or 'Company Name Not Found',
            'location': location or 'Location Not Found',
            'description': description or 'Job Description Not Found'
        }
        
        return json.dumps(job_content, indent=2)
    except Exception as e:
        return f"Error fetching webpage: {str(e)}"

@tool
def render_and_save_documents(cv_data: dict, cover_letter_data: dict, output_dir: str):
    """Renders and saves CV and Cover Letter as PDF and JPEG"""
    try:
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Validate data using Pydantic models
        cv = CV(**cv_data)
        cover_letter = CoverLetter(**cover_letter_data)
        
        def render_template(template_path, data):
            with open(template_path, 'r') as file:
                template_content = file.read()
            compiler = Compiler()
            template = compiler.compile(template_content)
            return template(data.model_dump())
        
        def html_to_jpeg(html_content, output_path):
            pdf = HTML(string=html_content).write_pdf()
            images = convert_from_bytes(pdf)
            if images:
                images[0].save(output_path, 'JPEG', quality=95)
        
        def html_to_pdf(html_content, output_path):
            HTML(string=html_content).write_pdf(output_path)
        
        # Process CV
        cv_template_path = "templates/cv_template.html"
        cv_html = render_template(cv_template_path, cv)
        
        cv_jpg_path = os.path.join(output_dir, "cv.jpg")
        cv_pdf_path = os.path.join(output_dir, "cv.pdf")
        
        html_to_jpeg(cv_html, cv_jpg_path)
        html_to_pdf(cv_html, cv_pdf_path)
        
        # Process Cover Letter
        cl_template_path = "templates/cover_letter_template.html"
        cl_html = render_template(cl_template_path, cover_letter)
        
        cl_jpg_path = os.path.join(output_dir, "cover_letter.jpg")
        cl_pdf_path = os.path.join(output_dir, "cover_letter.pdf")
        
        html_to_jpeg(cl_html, cl_jpg_path)
        html_to_pdf(cl_html, cl_pdf_path)
        
        return json.dumps({
            "success": True,
            "files": {
                "cv_jpg": cv_jpg_path,
                "cv_pdf": cv_pdf_path,
                "cover_letter_jpg": cl_jpg_path,
                "cover_letter_pdf": cl_pdf_path
            }
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })

class JobApplicationCrew:
    def __init__(self):
        self.model = ChatOpenAI(model_name="gpt-4-turbo-preview", temperature=0.7)
        
    def job_crawler(self) -> Agent:
        return Agent(
            role='Job Description Crawler',
            goal='Extract and analyze job posting information',
            backstory="""You are an expert at analyzing job postings and extracting key information.
            You focus on identifying essential requirements, qualifications, responsibilities, and company details.
            You also ensure proper formatting of company and job information for file organization.""",
            verbose=True,
            tools=[get_webpage_contents, read_text_file],
            allow_delegation=False,
            llm=self.model
        )

    def cv_writer(self) -> Agent:
        return Agent(
            role='CV Writer',
            goal='Create a professional CV that matches job requirements while maintaining authenticity',
            backstory="""You are an experienced CV writer who specializes in creating compelling CVs that match job requirements.
            You understand the Pydantic model requirements and ensure all data fits within specified constraints.
            
            Key guidelines:
            1. NEVER make up or fabricate specific metrics or statistics
            2. Focus on describing actual responsibilities and achievements without quantification
            3. Use clear, professional language to describe experience
            4. Maintain consistent formatting and style
            5. Ensure content is authentic and verifiable
            
            You understand the following constraints:
            - full_name: 1-50 characters (use full capacity)
            - job_title: 1-50 characters (use full capacity)
            - location: 1-50 characters (use full capacity)
            - email: valid email format
            - phone: 10-20 characters
            - linkedin: 1-100 characters (use full capacity)
            - professional_summary: 50-300 characters (aim for 250-300)
            - technical_skills: 1-5 items, each with:
              - category: 1-30 characters (use 20-30)
              - skills: 1-150 characters (aim for 100-150)
            - experience: 1-3 items, each with:
              - job_title: 1-50 characters (use full capacity)
              - company: 1-50 characters (use full capacity)
              - date_range: 1-30 characters (use full capacity)
              - responsibilities: 1-3 items, each 1-120 characters (aim for 100-120)
            - education: 1-2 items, each with:
              - degree: 1-50 characters (use full capacity)
              - institution: 1-50 characters (use full capacity)
              - year: 4 characters
              - achievements: 0-2 items, each 1-100 characters (aim for 80-100)
            - certifications: 0-5 items, each 1-40 characters (use 30-40)""",
            verbose=True,
            tools=[read_text_file],
            allow_delegation=False,
            llm=self.model
        )

    def cover_letter_writer(self) -> Agent:
        return Agent(
            role='Cover Letter Writer',
            goal='Create authentic and compelling cover letters that highlight relevant qualifications',
            backstory="""You are a professional cover letter writer who creates engaging and relevant cover letters.
            You understand the importance of authenticity and avoid making unsubstantiated claims.
            
            Key guidelines:
            1. NEVER include fabricated metrics or statistics
            2. Focus on actual experience and skills
            3. Use specific examples without quantification
            4. Maintain professional and genuine tone
            5. Highlight relevant experience without exaggeration
            
            You understand the following constraints:
            - full_name: 1-50 characters
            - address: 1-100 characters
            - city: 1-50 characters
            - state: 2 characters
            - zip: 5-10 characters
            - email: valid email format
            - phone: 10-20 characters
            - date: valid date format
            - hiring_manager_name: 1-50 characters
            - job_title: 1-50 characters
            - company_name: 1-50 characters
            - company_address: 1-100 characters
            - company_city: 1-50 characters
            - company_state: 2 characters
            - company_zip: 5-10 characters
            - paragraphs: 3 items, each 50-800 characters
            - closing_paragraph: 20-300 characters""",
            verbose=True,
            tools=[read_text_file],
            allow_delegation=False,
            llm=self.model
        )

    def document_processor(self) -> Agent:
        return Agent(
            role='Document Processor',
            goal='Generate professionally formatted PDF and JPEG versions of the CV and cover letter',
            backstory="""You are an expert at processing and formatting documents.
            You ensure all documents are properly formatted and validate against the Pydantic models.
            You focus on creating clean, professional layouts with consistent styling.
            
            Key responsibilities:
            1. Ensure proper spacing and alignment
            2. Maintain consistent font usage
            3. Create clear visual hierarchy
            4. Optimize readability
            5. Generate high-quality output files""",
            verbose=True,
            tools=[render_and_save_documents],
            allow_delegation=False,
            llm=self.model
        )

    def create_tasks(self, job_url: str, output_dir: str) -> list:
        task_extract_job = Task(
            description=f"""Extract key information from the job posting at {job_url}.
            Focus on required skills, qualifications, responsibilities, and company culture.
            Return the information in a structured format including:
            1. Job requirements and qualifications
            2. Company details and culture
            3. Role responsibilities
            Format the output in JSON format for other agents to use.""",
            expected_output="A JSON string containing structured job posting information",
            agent=self.job_crawler()
        )

        task_create_cv = Task(
            description="""Create a CV that matches the job requirements.
            First, read the base CV from CV.txt using the read_text_file tool.
            Then, modify the content to match the job requirements while following the Pydantic model structure.
            Ensure all content fits within the specified length constraints.
            Return the CV data in valid JSON format that matches the CV model.""",
            expected_output="A JSON string containing CV data that matches the CV Pydantic model",
            agent=self.cv_writer(),
            context=[task_extract_job]
        )

        task_create_cover_letter = Task(
            description="""Create a cover letter that highlights relevant qualifications.
            First, read the base cover letter from Cover_Letter.txt using the read_text_file tool.
            Then, modify the content to match the job requirements while following the Pydantic model structure.
            Ensure all content fits within the specified length constraints.
            Return the cover letter data in valid JSON format that matches the CoverLetter model.""",
            expected_output="A JSON string containing cover letter data that matches the CoverLetter Pydantic model",
            agent=self.cover_letter_writer(),
            context=[task_extract_job]
        )

        task_process_documents = Task(
            description=f"""Generate PDF and JPEG versions of the CV and cover letter.
            Use the provided templates and save to the output directory: {output_dir}
            Validate all data against the Pydantic models before processing.
            Ensure professional formatting and appearance.""",
            expected_output="A JSON string containing the paths to the generated PDF and JPEG files",
            agent=self.document_processor(),
            context=[task_extract_job, task_create_cv, task_create_cover_letter]
        )

        return [task_extract_job, task_create_cv, task_create_cover_letter, task_process_documents]

def main():
    # Get job URL from user
    job_url = input("\nPlease enter the job posting URL: ").strip()
    
    # Set up output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    print("\nStarting job application process...")
    print(f"Job URL: {job_url}")
    print(f"Output Directory: {output_dir}")
    
    # Initialize the crew
    application_crew = JobApplicationCrew()
    
    # Create initial tasks
    initial_tasks = application_crew.create_tasks(job_url, output_dir)

    # Create and run the crew
    crew = Crew(
        agents=[
            application_crew.job_crawler(),
            application_crew.cv_writer(),
            application_crew.cover_letter_writer(),
            application_crew.document_processor()
        ],
        tasks=initial_tasks,
        verbose=True
    )

    try:
        # Run document creation
        result = crew.kickoff()
        print("\nFinal Result:")
        print(result)
        
    except Exception as e:
        print(f"\nError during execution: {str(e)}")

if __name__ == "__main__":
    main() 