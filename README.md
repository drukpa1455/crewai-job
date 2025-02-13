# 🚀 Job Application Automation with CrewAI

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.11.0-orange.svg)](https://github.com/joaomdmoura/crewAI)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<p align="center">
  <strong>🤖 Automate Your Job Applications with AI Agents 📝</strong>
  <br>
  <em>Transform your job search with intelligent CV and cover letter customization</em>
</p>

[Features](#-features) •
[Installation](#️-installation) •
[Quick Start](#-quick-start) •
[Contributing](#-contributing) •
[Support](#-support)

</div>

An intelligent job application automation system that uses CrewAI and LangChain to customize CVs and cover letters based on job descriptions. The system employs specialized AI agents working together to analyze job postings and create tailored application materials that maintain authenticity and professionalism.

> 🌟 Perfect for job seekers who want to create tailored applications efficiently while maintaining authenticity and professionalism.

## ✨ Features

- 🔍 **Intelligent Job Analysis**: Automatically extracts key information from job postings including requirements, qualifications, and company culture
- 📝 **CV Customization**: Tailors your CV to highlight relevant skills and experiences for each job
- ✉️ **Cover Letter Generation**: Creates personalized cover letters that connect your experience with job requirements
- 🎨 **Professional Formatting**: Generates beautifully formatted PDF and JPEG versions of your documents
- 🤖 **Multi-Agent System**: Utilizes specialized AI agents for different aspects of the application process
- 💾 **Organized Output**: Saves modified documents with clear, job-specific naming conventions

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/crewai-job.git
cd crewai-job
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- Basic text files for your CV and cover letter

## 🚀 Quick Start

1. Prepare your base CV and cover letter:
```bash
# Save your CV as CV.txt
# Save your cover letter as Cover_Letter.txt
```

2. Run the script:
```bash
python job_application_agents.py
```

3. Enter the job posting URL when prompted

4. Find your customized documents in the `output` directory

## 🤖 How It Works

The system uses three specialized AI agents working in harmony:

1. **Job Description Crawler** 🕷️
   - Analyzes job postings
   - Extracts key requirements and company information
   - Structures data for other agents

2. **CV Writer** 📄
   - Tailors CV content to match job requirements
   - Emphasizes relevant skills and experiences
   - Ensures content authenticity and professionalism
   - Maintains proper formatting and structure

3. **Cover Letter Writer** ✉️
   - Creates personalized cover letters
   - Connects experience with job requirements
   - Incorporates company culture and values
   - Maintains professional tone and formatting

Each agent is designed to focus on its specific task while maintaining data consistency and professional standards throughout the process.

## 🎯 Use Cases

- Job seekers applying to multiple positions
- Career counselors helping clients
- HR professionals processing applications
- Recruitment agencies handling multiple candidates

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch:
```bash
git checkout -b feature/amazing-feature
```
3. Commit your changes:
```bash
git commit -m 'Add amazing feature'
```
4. Push to the branch:
```bash
git push origin feature/amazing-feature
```
5. Open a Pull Request

### 📝 Contribution Guidelines

- Follow PEP 8 style guide for Python code
- Add comments for complex logic
- Update documentation for new features
- Include tests for new functionality
- Ensure all tests pass before submitting PR

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the multi-agent framework
- [LangChain](https://github.com/hwchase17/langchain) for the LLM tools
- OpenAI for the language models
- All our contributors and supporters

## 🔮 Future Improvements

- [ ] Support for more job board platforms
- [ ] Additional document formats (DOCX, RTF)
- [ ] Integration with job application APIs
- [ ] Batch processing capabilities
- [ ] Template customization options
- [ ] Additional styling themes

## 📞 Support

- Create an issue for bugs or feature requests
- Join our [Discord community](your-discord-link)
- Check out our [Wiki](your-wiki-link) for detailed documentation

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/crewai-job&type=Date)](https://star-history.com/#yourusername/crewai-job&Date)

---

Made with ❤️ by the CrewAI Job community
