import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import google.generativeai as palm

def get_text_from_pdf(pdf_file) -> str:
    """
    Extracts text from a PDF file.
    """
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def run_comparison(cv_text: str, job_text: str, model):
    """
    Runs prepared prompts against the CV and job description to generate a chat-like comparison
    using Google's PaLM API (via google-generativeai).
    """
    prompts = [
        "How suitable is this CV for the given job position?",
        "What should the candidate learn or change in their CV to better match the job requirements?",
        "What are the pros and cons of this CV in relation to the job position?",
        "Based on the job description, what are the key requirements of the position?"
    ]

    context = f"CV:\n{cv_text}\n\nJob Description:\n{job_text}\n\n"

    conversation = []

    for prompt in prompts:
        full_prompt = context + f"Question: {prompt}\nAnswer:"

        response = model.generate_content(full_prompt,)

        conversation.append((prompt, response.text))

    return conversation

def main():
    load_dotenv()
    palm.configure(api_key=os.environ.get("PALM_API_KEY"))

    st.set_page_config(page_title="CV Comparison Chat", page_icon="💬")
    st.title("CV Comparison Chat")

    st.sidebar.header("Input Data")
    cv_file = st.sidebar.file_uploader("Upload your CV (PDF)", type="pdf")
    job_description = st.sidebar.text_area("Paste the Job Description")

    if st.sidebar.button("Compare CV and Job"):
        if not cv_file or not job_description.strip():
            st.sidebar.error("Please upload a CV and enter a job description.")
        else:
            cv_text = get_text_from_pdf(cv_file)
            model = palm.GenerativeModel('gemini-1.5-flash')
            conversation = run_comparison(cv_text, job_description, model)

            st.subheader("Comparison Results")
            for question, answer in conversation:
                st.markdown(f"**Q: {question}**")
                st.markdown(f"**A:** {answer}")

if __name__ == '__main__':
    main()
