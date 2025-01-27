# ATS Resume Analyzer

## Overview
The **ATS Resume Analyzer** is an AI-powered tool designed to help job seekers optimize their resumes for compatibility with Applicant Tracking Systems (ATS). By leveraging cutting-edge language models, the system evaluates resumes, provides a compatibility score, and offers actionable suggestions for improvement.

## Features
- 📂 **Resume Upload**: Analyze resume files in PDF format by placing them in a predefined directory.
- 📊 **ATS Compatibility Scoring**: Generates an average ATS score based on multiple analysis runs (ensuring consistency and reliability).
- 💡 **Actionable Suggestions**: Offers up to 3 specific, structured recommendations to improve your resume's ATS compatibility and overall quality.
- 🌟 **Customizable**: Built with modular components, ready for future expansion into web interfaces.

## Tech Stack
- **LLM Integration**: LLaMA 3.2 (via Ollama CLI) for processing resumes and generating insights.
- **Backend**: Python for processing and orchestration.
- **Libraries Used**:
  - `PyPDF2` for extracting text from PDF resumes.
  - `subprocess` for seamless integration with the Ollama CLI.
  - `transformers` for language model processing.
  - `pathlib` for streamlined file management.

## Current Workflow
1. Place your resume files in the `/Resume` directory.
2. Run the program, which:
   - Lists available resume files.
   - Allows selection of a specific resume for analysis.
   - Extracts and processes text using LLaMA 3.2 (via Ollama CLI).
   - Runs the analysis three times to ensure accuracy and averages the ATS score.
3. If desired, generates actionable improvement suggestions with clear formatting.
4. Displays results in the console for further review.

## Future Enhancements
- 🌍 **User-Friendly Web Interface**: Development of a web-based platform for seamless interaction, including drag-and-drop resume upload.
- 🤖 **Advanced LLM Support**: Incorporate fine-tuned models for domain-specific analysis.
- 📈 **Analytics Dashboard**: Generate detailed visual reports with ATS analysis trends.
- 🌟 **Multi-Format Support**: Extend compatibility to DOCX and other file types.

## Getting Started

### Prerequisites
- Python 3.12 or above.
- Install **Ollama CLI** and set up the **LLaMA 3.2** model:
  ```bash
  ollama pull llama3.2:latest
  ```
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/PouyaPourfarrokh/ATS-Resume-Analyzer.git
   cd ATS-Resume-Analyzer
   ```
2. Place your resume files in the `Resume` folder.
3. Run the analyzer:
   ```bash
   python3 resume_analyzer.py
   ```
4. Follow the prompts to:
   - Select a resume file for analysis.
   - View the average ATS score and insights.
   - Generate improvement suggestions (optional).

### Example Output
- **ATS Score**: 85.0%
- **Strengths**:
  - Comprehensive technical skills.
  - Relevant certifications.
- **Weaknesses**:
  - Lack of measurable achievements.
  - Formatting issues.
- **Suggestions**:
  1. Add measurable achievements to showcase impact.
  2. Improve section formatting for better ATS parsing.
  3. Highlight leadership experience, if applicable.

## Contributing
Feel free to fork this repository and contribute enhancements or bug fixes. Pull requests are welcome!

---
