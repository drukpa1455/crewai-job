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
        
        # Extract job details
        job_content = {
            'title': soup.find('h1', class_='app-title').text.strip() if soup.find('h1', class_='app-title') else '',
            'company': soup.find('span', class_='company-name').text.strip() if soup.find('span', class_='company-name') else '',
            'location': soup.find('div', class_='location').text.strip() if soup.find('div', class_='location') else '',
            'description': soup.find('div', id='content').text.strip() if soup.find('div', id='content') else ''
        }
        
        return json.dumps(job_content, indent=2)
    except Exception as e:
        return f"Error fetching webpage: {str(e)}"

def sanitize_filename(filename):
    """
    Convert a string into a safe filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Remove any non-ASCII characters
    filename = ''.join(char for char in filename if ord(char) < 128)
    return filename

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
            tools=[get_webpage_contents],
            allow_delegation=False,
            llm=self.model
        )

    def cv_modifier(self) -> Agent:
        return Agent(
            role='CV/Resume Writer',
            goal='Modify CV to align with job requirements while maintaining authenticity',
            backstory="""You are an experienced CV writer who specializes in tailoring CVs to specific job requirements.
            You maintain honesty and authenticity while reorganizing and emphasizing relevant skills and experiences.""",
            verbose=True,
            tools=[read_text_file, write_text_file],
            allow_delegation=False,
            llm=self.model
        )

    def cover_letter_modifier(self) -> Agent:
        return Agent(
            role='Cover Letter Writer',
            goal='Create compelling cover letters that highlight relevant qualifications',
            backstory="""You are a professional cover letter writer with expertise in crafting engaging and relevant cover letters.
            You focus on connecting candidate experiences with job requirements while maintaining a genuine tone.
            You are skilled at using company research to personalize each letter.""",
            verbose=True,
            tools=[read_text_file, write_text_file],
            allow_delegation=False,
            llm=self.model
        )

    def recruiter(self) -> Agent:
        return Agent(
            role='Hiring Manager',
            goal='Evaluate application materials and provide constructive feedback',
            backstory="""You are an experienced hiring manager who has reviewed thousands of applications.
            You provide detailed feedback and scoring based on how well the application matches job requirements.""",
            verbose=True,
            allow_delegation=False,
            llm=self.model
        )

    def create_tasks(self, job_url: str, cv_path: str, cover_letter_path: str, output_dir: str) -> list:
        task_extract_job = Task(
            description=f"""Extract key information from the job posting at {job_url}.
            Focus on required skills, qualifications, responsibilities, and company culture.
            Also extract and format the company name and job title for file organization.
            Return the information in a structured format including:
            1. Job analysis (requirements, qualifications, etc.)
            2. File organization info (company_name and job_title as clean, filename-safe strings)
            3. Company details (full company name, location, etc.)
            Format the output in JSON format for easy parsing by other agents.
            
            The output should be a valid JSON string with this structure:
            {{
                "job_analysis": {{
                    "responsibilities": [],
                    "qualifications": [],
                    "other_details": []
                }},
                "file_organization_info": {{
                    "company_name": "company_name_in_snake_case",
                    "job_title": "job_title_in_snake_case"
                }},
                "company_details": {{
                    "full_company_name": "",
                    "location": "",
                    "company_culture": ""
                }}
            }}""",
            agent=self.job_crawler(),
            expected_output="A structured JSON containing job analysis, file organization information, and company details"
        )

        task_modify_cv = Task(
            description=f"""Using the job details provided, modify the CV at {cv_path}.
            First, read the original CV content using the read_text_file tool.
            Then, modify the content to align with the job requirements from the previous task's JSON output.
            Finally, save the modified content to: {output_dir}/CV_{{company_name}}_{{job_title}}.txt
            
            Use the company_name and job_title from the file_organization_info in the previous task's output.
            
            Steps:
            1. Read CV using read_text_file from {cv_path}
            2. Modify content based on job requirements
            3. Format properly maintaining plain text format
            4. Save using write_text_file to the output path
            5. Verify the file was saved successfully
            
            Emphasize relevant skills and experiences.
            Do not fabricate or add new information.
            Maintain professional tone and formatting.""",
            agent=self.cv_modifier(),
            expected_output="A confirmation that the tailored CV has been saved to the output directory",
            context=[task_extract_job]
        )

        task_modify_cover_letter = Task(
            description=f"""Using the job details provided, modify the cover letter at {cover_letter_path}.
            First, read the original cover letter content using the read_text_file tool.
            Then, modify the content using the job details from the previous task's JSON output.
            Finally, save the modified content to: {output_dir}/Cover_Letter_{{company_name}}_{{job_title}}.txt
            
            Use the company_name and job_title from the file_organization_info in the previous task's output.
            Use the company details for proper addressing and company-specific content.
            
            Steps:
            1. Read cover letter using read_text_file from {cover_letter_path}
            2. Modify content based on job requirements and company details:
               - Update the company name and job title
               - Customize the introduction to mention G-P's mission
               - Highlight relevant experience with modern frameworks and cloud technologies
               - Emphasize experience with agile methodologies and team collaboration
               - Connect your experience to G-P's remote-first, innovative culture
            3. Format properly maintaining plain text format
            4. Save using write_text_file to the output path
            5. Verify the file was saved successfully
            
            Focus on connecting candidate's experience with job requirements.
            Maintain authenticity and enthusiasm.
            Ensure proper addressing using the company details from the job posting.""",
            agent=self.cover_letter_modifier(),
            expected_output="A confirmation that the tailored cover letter has been saved to the output directory with proper formatting and content",
            context=[task_extract_job]
        )

        task_evaluate = Task(
            description=f"""Review the modified CV and cover letter against the job requirements.
            The CV and cover letter should be in the output directory with names based on the company_name and job_title
            from the job crawler's output.
            
            Steps:
            1. Use the job analysis from the first task
            2. Read and evaluate both modified files
            3. Provide a detailed evaluation and score from 0-100
            4. Include specific feedback and suggestions for improvement
            5. Verify both files exist and contain appropriate content
            
            Ensure both documents maintain professional formatting and contain accurate information.""",
            agent=self.recruiter(),
            expected_output="A detailed evaluation report with score and specific feedback",
            context=[task_extract_job, task_modify_cv, task_modify_cover_letter]
        )

        return [task_extract_job, task_modify_cv, task_modify_cover_letter, task_evaluate]

def main():
    # Get job URL from user
    job_url = input("\nPlease enter the job posting URL: ").strip()
    
    # Set up paths with .txt extension
    cv_path = "CV.txt"
    cover_letter_path = "Cover_Letter.txt"
    output_dir = "output"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print("\nStarting job application process...")
    print(f"Job URL: {job_url}")
    print(f"Input CV Path: {cv_path}")
    print(f"Input Cover Letter Path: {cover_letter_path}")
    print(f"Output Directory: {output_dir}")
    print("Note: Modified files will be saved as .txt files in the output directory\n")
    
    # Initialize the crew
    application_crew = JobApplicationCrew()
    
    # Create tasks
    tasks = application_crew.create_tasks(job_url, cv_path, cover_letter_path, output_dir)

    # Create and run the crew
    crew = Crew(
        agents=[
            application_crew.job_crawler(),
            application_crew.cv_modifier(),
            application_crew.cover_letter_modifier(),
            application_crew.recruiter()
        ],
        tasks=tasks,
        verbose=True
    )

    try:
        result = crew.kickoff()
        print("\nFinal Result:")
        print(result)
        
    except Exception as e:
        print(f"\nError during execution: {str(e)}")

if __name__ == "__main__":
    main() 