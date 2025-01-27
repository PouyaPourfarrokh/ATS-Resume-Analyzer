import os
import subprocess
import sys
from pathlib import Path
from PyPDF2 import PdfReader
from visualizer import generate_visualizations  # Correct function name


def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        sys.exit(1)


def analyze_resume_with_llama(resume_text, runs=3):
    """Analyze the resume using LLaMA 3.2 via Ollama CLI."""
    prompt = f"""
    You are an expert in ATS-friendly resumes. Analyze the following resume text and provide:
    - An ATS compliance score (0-100%).
    - A list of strengths.
    - A list of weaknesses.

    Format the response as:
    ATS Score: [score]%
    Strengths:
    - [Strength 1]
    - [Strength 2]
    ...
    Weaknesses:
    - [Weakness 1]
    - [Weakness 2]
    ...
    Resume:
    {resume_text}
    """
    scores = []
    strengths, weaknesses = [], []
    try:
        for _ in range(runs):
            # Run the Ollama CLI with LLaMA 3.2
            process = subprocess.run(
                ["ollama", "run", "llama3.2:latest"],
                input=prompt,
                text=True,
                capture_output=True,
                check=True
            )
            output = process.stdout.strip()

            # Parse ATS Score
            score_line = next((line for line in output.splitlines() if line.startswith("ATS Score:")), None)
            if score_line:
                score = float(score_line.split(":")[1].strip().replace("%", ""))
                scores.append(score)

            # Parse Strengths
            strength_lines = [
                line.strip("- ") for line in output.splitlines() if line.startswith("-") and "Strength" in output
            ]
            if strength_lines:
                strengths.extend(strength_lines)

            # Parse Weaknesses
            weakness_lines = [
                line.strip("- ") for line in output.splitlines() if line.startswith("-") and "Weakness" in output
            ]
            if weakness_lines:
                weaknesses.extend(weakness_lines)

        # Compute the average score
        avg_score = sum(scores) / len(scores) if scores else 0
        return avg_score, strengths, weaknesses
    except subprocess.CalledProcessError as e:
        print(f"Error running Ollama CLI: {e.stderr}")
        sys.exit(1)


def generate_improvement_suggestions(avg_score, detailed_output):
    """Generate structured improvement suggestions."""
    prompt = f"""
    Based on the following ATS analysis, provide exactly three actionable improvement suggestions:
    Average ATS Score: {avg_score:.2f}%
    Analysis Details:
    {detailed_output}
    Format the response as:
    Suggestions:
    1. [Suggestion 1]
    2. [Suggestion 2]
    3. [Suggestion 3]
    """
    try:
        # Run Ollama CLI for improvement suggestions
        process = subprocess.run(
            ["ollama", "run", "llama3.2:latest"],
            input=prompt,
            text=True,
            capture_output=True,
            check=True
        )
        return process.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running Ollama CLI: {e.stderr}")
        sys.exit(1)


def ask_user_for_improvements():
    """Prompt the user to ask if they want improvement suggestions."""
    while True:
        response = input("\nDo you want to generate improvement suggestions? (yes/no): ").strip().lower()
        if response in ["yes", "no"]:
            return response == "yes"
        print("Invalid input. Please enter 'yes' or 'no'.")


def list_resume_files(resume_dir):
    """List all resume files in the given directory."""
    try:
        files = [f for f in os.listdir(resume_dir) if f.endswith(".pdf")]
        if not files:
            print("No resume files found in the directory. Please add files and try again.")
            sys.exit(1)
        return files
    except Exception as e:
        print(f"Error accessing the directory: {e}")
        sys.exit(1)


def select_resume_file(resume_dir, files):
    """Ask the user to select a resume file from the list."""
    print("\nAvailable resume files:")
    for i, file_name in enumerate(files, 1):
        print(f"{i}. {file_name}")

    while True:
        try:
            choice = int(input("\nEnter the number of the resume file to analyze: "))
            if 1 <= choice <= len(files):
                return Path(resume_dir) / files[choice - 1]
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    """Main function for analyzing resumes."""
    # Define the directory where resumes are stored
    resume_dir = "/Users/pouyapourfarrokh/Desktop/AI&Data science Projects/ATS-Resume-Analyzer/Resume"

    # List and select a resume file
    resume_files = list_resume_files(resume_dir)
    selected_file = select_resume_file(resume_dir, resume_files)
    print(f"\nSelected file: {selected_file}")

    # Extract text from the selected resume
    print("Extracting text from the resume...")
    resume_text = extract_text_from_pdf(selected_file)
    print("Resume text extracted successfully.")

    # Analyze the resume with LLaMA 3.2 (3 runs for averaging)
    print("Analyzing the resume with LLaMA 3.2...")
    avg_score, strengths, weaknesses = analyze_resume_with_llama(resume_text, runs=3)

    # Ask if the user wants improvement suggestions
    suggestions = []
    if ask_user_for_improvements():
        print("\nGenerating improvement suggestions...")
        suggestions = generate_improvement_suggestions(avg_score, "\n".join(strengths + weaknesses))

    # Visualize results
    print("\nVisualizing results...")
    generate_visualizations(avg_score, strengths, weaknesses, suggestions)


if __name__ == "__main__":
    main()
