import streamlit as st
import os
import google.generativeai as genai
from docx import Document
from dotenv import load_dotenv
from io import BytesIO

# Load environment variables from .env file
load_dotenv()

# Try to use the API key from Streamlit secrets (for deployment on Streamlit Cloud)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    # If not found, fall back to the environment variable (for local development)
    api_key = os.environ.get("GEMINI_API_KEY")

# Configure the Gemini API with the chosen API key
genai.configure(api_key=api_key)

# Define model and system behavior
MODEL_NAME = "gemini-2.0 flash"
SYSTEM_INSTRUCTIONS = "You are a professional resume and cover letter writer specializing in ATS-optimized documents."

# Template for prompting Gemini API
PROMPT_TEMPLATE = """
{system_instructions}
Generate a detailed and well-structured {doc_type} tailored to the job description below.
Ensure the {doc_type} includes all essential sections and follows professional formatting.

**Important Instructions:**
1. Only provide the {doc_type} content. Do NOT include any additional notes, explanations, or disclaimers.
2. Do NOT include phrases like "Note:", "Remember to", "Best of luck", or "For demonstration purposes".
3. Be specific and direct. Only provide the {doc_type} content.

Job Title: {job_title}
Company: {company_name}
Job Description: {job_description}

### {doc_type} ###
"""

def generate_document(doc_type, job_description, company_name, job_title):
    """
    Generates a resume or cover letter using the Gemini API based on user-provided details.
    
    Parameters:
        doc_type (str): The type of document to generate ("Resume" or "Cover Letter").
        job_description (str): The job description provided by the user.
        company_name (str): The name of the company.
        job_title (str): The title of the job.
    
    Returns:
        str: The generated resume or cover letter text or an error message.
    """
    if not job_description or not company_name or not job_title:
        return "Please provide all details."
    
    # Format the prompt with user-provided details
    prompt = PROMPT_TEMPLATE.format(
        system_instructions=SYSTEM_INSTRUCTIONS, 
        doc_type=doc_type, 
        job_title=job_title, 
        company_name=company_name, 
        job_description=job_description
    )
    
    # Call Gemini API to generate content
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "Error: No response generated."
    except Exception as e:
        return f"Error: {str(e)}"

def save_as_docx(text, filename):
    """
    Creates a Word document (.docx) in memory and returns a BytesIO stream.
    
    Parameters:
        text (str): The generated resume or cover letter content.
        filename (str): The desired filename for the saved document (used for download).
    
    Returns:
        BytesIO: A stream containing the Word document data.
    """
    doc = Document()
    doc.add_paragraph(text)
    doc_io = BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    return doc_io

# Streamlit UI Header with Template Notice
st.header("ATS Resume & Cover Letter Generator Template ✍️")
st.write("This template can be downloaded as a Word file and modified as needed. Enter the job details below to generate a professional ATS-optimized document.")

# Expander to explain ATS (Applicant Tracking System)
with st.expander("What is ATS?"):
    st.write("""
    **ATS (Applicant Tracking System)** is software used by companies to manage the recruitment process. 
    It helps in sorting, ranking, and filtering resumes to find the best candidates efficiently.
    """)

# User Inputs for Job Details
job_title = st.text_input("Job Title", placeholder="Enter job title")
company_name = st.text_input("Company Name", placeholder="Enter company name")
job_description = st.text_area("Job Description", placeholder="Paste the job description here")
doc_type = st.selectbox("Select Document Type", ["Resume", "Cover Letter"], index=0)

# Generate Document Button
if st.button("Generate"):
    # Generate the resume or cover letter based on user inputs
    generated_text = generate_document(doc_type, job_description, company_name, job_title)
    
    # Display generated content in a text area
    st.text_area("Generated Document", generated_text, height=300)
    
    if generated_text:
        # Set appropriate filename based on document type
        filename = "resume.docx" if doc_type == "Resume" else "cover_letter.docx"
        
        # Create the Word document in memory
        doc_file = save_as_docx(generated_text, filename)
        
        # Provide a download button so the user can choose to download the document
        st.download_button(
            label="Download as Word Document",
            data=doc_file,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
