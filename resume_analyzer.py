import os
from transformers import LlamaTokenizer, LlamaForCausalLM
from PyPDF2 import PdfReader
from docx import Document

# Load LLaMA model and tokenizer
model_name = "meta-llama/Llama-2-7b-hf"
tokenizer = LlamaTokenizer.from_pretrained(model_name)
model = LlamaForCausalLM.from_pretrained(model_name, device_map="auto")

def extract_text(file_path):
    """Extract text from PDF or DOCX files."""
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = " ".join(page.extract_text() for page in reader.pages)
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        text = " ".join(paragraph.text for paragraph in doc.paragraphs)
    else:
        raise ValueError("Unsupported file format")
    return text

def analyze_resume(text):
    """Analyze the resume text using LLaMA."""
    prompt = f"Analyze this resume text for ATS compatibility and provide a score from 0 to 100. Text: {text}"
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(
        inputs.input_ids, max_length=200, temperature=0.7, top_p=0.9
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

if __name__ == '__main__':
    # Test the processing system with a local file
    test_file = "Resume/POUYA POURFARROKH_ML_Resume2025 (1).pdf"  # Replace with your test file path
    if os.path.exists(test_file):
        try:
            resume_text = extract_text(test_file)
            analysis_result = analyze_resume(resume_text)
            print("Analysis Result:", analysis_result)
        except Exception as e:
            print("Error:", str(e))
    else:
        print("Test file does not exist. Please provide a valid path.")
