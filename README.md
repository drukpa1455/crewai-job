# 🚀 Job Application Automation with CrewAI

An intelligent job application automation system that uses CrewAI and LangChain to customize CVs and cover letters based on job descriptions. The system employs multiple AI agents working together to analyze job postings, tailor application materials, and provide professional feedback.

## ✨ Features

- 🔍 **Intelligent Job Analysis**: Automatically extracts key information from job postings including requirements, qualifications, and company culture
- 📝 **CV Customization**: Tailors your CV to highlight relevant skills and experiences for each job
- ✉️ **Cover Letter Generation**: Creates personalized cover letters that connect your experience with job requirements
- 🎯 **Professional Evaluation**: Provides detailed feedback and scoring of your application materials
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

The system uses four specialized AI agents:

1. **Job Description Crawler** 🕷️
   - Analyzes job postings
   - Extracts key requirements and company information
   - Structures data for other agents

2. **CV Modifier** 📄
   - Tailors CV content to match job requirements
   - Emphasizes relevant skills and experiences
   - Maintains professional formatting

3. **Cover Letter Writer** ✉️
   - Creates personalized cover letters
   - Connects experience with job requirements
   - Incorporates company culture and values

4. **Recruiter** 👔
   - Evaluates modified documents
   - Provides detailed feedback
   - Suggests improvements

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
- [ ] Additional document formats (PDF, DOCX)
- [ ] Integration with job application APIs
- [ ] Enhanced evaluation metrics
- [ ] Custom agent creation interface
- [ ] Batch processing capabilities

## 📞 Support

- Create an issue for bugs or feature requests
- Join our [Discord community](your-discord-link)
- Check out our [Wiki](your-wiki-link) for detailed documentation

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/crewai-job&type=Date)](https://star-history.com/#yourusername/crewai-job&Date)

---

Made with ❤️ by the CrewAI Job community
