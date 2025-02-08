import os
from datetime import datetime, date
from pybars import Compiler
from weasyprint import HTML
from pathlib import Path
from PIL import Image
import io
import json
from models import CV, CoverLetter

def load_cv_data(file_path: str) -> CV:
    """Load CV data from JSON file"""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return CV(**data)

def load_cover_letter_data(file_path: str, job_details: dict = None) -> CoverLetter:
    """Load cover letter data from JSON file"""
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    if job_details:
        # Replace placeholders in paragraphs
        data['paragraphs'] = [
            p.replace('[Position]', job_details.get('position', '[Position]'))
             .replace('[Company Name]', job_details.get('company_name', '[Company Name]'))
             .replace('[specific aspect of the company\'s work or culture]', 
                     job_details.get('company_culture', '[specific aspect of the company\'s work or culture]'))
            for p in data['paragraphs']
        ]
        data['closing_paragraph'] = data['closing_paragraph'].replace(
            '[Company Name]', job_details.get('company_name', '[Company Name]')
        )
        
        # Update job-specific fields
        if 'position' in job_details:
            data['job_title'] = job_details['position']
        if 'company_name' in job_details:
            data['company_name'] = job_details['company_name']
        if 'hiring_manager_name' in job_details:
            data['hiring_manager_name'] = job_details['hiring_manager_name']
    
    return CoverLetter(**data)

def render_template(template_path, data):
    """Render HTML template with given data"""
    with open(template_path, 'r') as file:
        template_content = file.read()
    
    compiler = Compiler()
    template = compiler.compile(template_content)
    return template(data.model_dump())

def html_to_jpeg(html_content, output_path):
    """Convert HTML content to JPEG using WeasyPrint and PIL"""
    # Create PDF in memory
    pdf = HTML(string=html_content).write_pdf()
    
    # Convert PDF to PIL Image
    from pdf2image import convert_from_bytes
    images = convert_from_bytes(pdf)
    
    # Save first page as JPEG
    if images:
        images[0].save(output_path, 'JPEG', quality=95)

def html_to_pdf(html_content, output_path):
    """Convert HTML content to PDF using WeasyPrint"""
    HTML(string=html_content).write_pdf(output_path)

def main():
    # Sample job details (you can modify these or load from a file)
    job_details = {
        'position': 'Senior Front End Developer',
        'company_name': 'TechCorp Solutions',
        'hiring_manager_name': 'Sarah Johnson',
        'company_culture': 'innovative approach to cloud-based solutions'
    }
    
    # Create test output directory
    output_dir = Path("templates/test_output")
    output_dir.mkdir(exist_ok=True)
    
    # Load and process CV
    cv_data = load_cv_data("CV.txt")
    cv_template_path = "templates/cv_template.html"
    cv_html = render_template(cv_template_path, cv_data)
    
    # Save CV as JPEG
    cv_jpg_path = output_dir / "test_cv.jpg"
    html_to_jpeg(cv_html, str(cv_jpg_path))
    print(f"CV saved to: {cv_jpg_path}")
    
    # Save CV as PDF
    cv_pdf_path = output_dir / "test_cv.pdf"
    html_to_pdf(cv_html, str(cv_pdf_path))
    print(f"CV PDF saved to: {cv_pdf_path}")
    
    # Load and process Cover Letter
    cover_letter_data = load_cover_letter_data("Cover_Letter.txt", job_details)
    cl_template_path = "templates/cover_letter_template.html"
    cl_html = render_template(cl_template_path, cover_letter_data)
    
    # Save Cover Letter as JPEG
    cl_jpg_path = output_dir / "test_cover_letter.jpg"
    html_to_jpeg(cl_html, str(cl_jpg_path))
    print(f"Cover Letter saved to: {cl_jpg_path}")
    
    # Save Cover Letter as PDF
    cl_pdf_path = output_dir / "test_cover_letter.pdf"
    html_to_pdf(cl_html, str(cl_pdf_path))
    print(f"Cover Letter PDF saved to: {cl_pdf_path}")

if __name__ == "__main__":
    main() 