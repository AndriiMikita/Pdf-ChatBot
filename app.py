import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import google.genai as palm
from google.genai import types
from templates import CSS_T, USER_T, BOT_T

def get_text_from_pdf(pdf_file) -> str:
    """
    Extracts text from a PDF file.
    """
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def run_comparison(cv_text: str, job_text: str, client):
    """
    Runs prepared prompts against the CV and job description to generate a chat-like comparison
    using Google's PaLM API (via google-generativeai).
    """
    prompts = [
        "Based on the job description, what are the key requirements of the position?",
        "How suitable is this CV for the given job position in percentage?",
        "What should the candidate learn or change in their CV to better match the job requirements?",
        "What are the pros and cons of this CV in relation to the job position?",
    ]

    context = f"CV:\n{cv_text}\n\nJob Description:\n{job_text}\n\n"
    conversation = []

    for prompt in prompts:
        full_prompt = context + f"Question: {prompt}\nAnswer:"
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=full_prompt,
            config=types.GenerateContentConfig(temperature=0.1,),
        )
        conversation.append((prompt, response.text))
    return conversation

def run_chat(user_message: str, conversation_history: list, client, cv_text: str, job_description: str):
    """
    Handles a single turn in the chat conversation by appending the user message,
    constructing the conversation prompt, and retrieving a response from the model.
    """
    prompt = f"CV:\n{cv_text}\n\nJob Description:\n{job_description}\n\nChat History:\n{conversation_history}\n\nUser: {user_message}\nAssistant:"
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.1,),
    )
    bot_message = response.text.strip()
    conversation_history.append(f"User: {user_message}")
    conversation_history.append(f"Assistant: {bot_message}")
    return bot_message

def main():
    load_dotenv()
    client = palm.Client(api_key=os.environ.get("PALM_API_KEY"))

    st.set_page_config(page_title="CV Comparison Chat", page_icon="💬")
    st.title("CV Comparison Chat")
    st.write(CSS_T, unsafe_allow_html=True)

    st.sidebar.header("Input Data")
    cv_file = st.sidebar.file_uploader("Upload your CV (PDF)", type="pdf")
    cv_text = get_text_from_pdf(cv_file)
    job_description = st.sidebar.text_area("Paste the Job Description")
    
    st.subheader("Chat with the Model")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


    if st.sidebar.button("Compare CV and Job"):
        if not cv_file or not job_description.strip():
            st.sidebar.error("Please upload a CV and enter a job description.")
        else:
            conversation = run_comparison(cv_text, job_description, client)
            st.subheader("Comparison Results")
            for question, answer in conversation:
                st.session_state.chat_history.append(f"User: {question}")
                st.session_state.chat_history.append(f"Assistant: {answer}")


    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Enter your message:")
        submitted = st.form_submit_button("Send")
        if submitted and user_input:
            run_chat(user_input, st.session_state.chat_history, client, cv_text, job_description)
            
    num_pairs = len(st.session_state.chat_history) // 2

    for i in range(num_pairs - 1, -1, -1):
        user_msg = st.session_state.chat_history[2 * i]
        bot_msg = st.session_state.chat_history[2 * i + 1]
        st.write(USER_T.replace("{{MSG}}", user_msg[len("User: "):]), unsafe_allow_html=True)
        st.write(BOT_T.replace("{{MSG}}", bot_msg[len("Assistant: "):]), unsafe_allow_html=True)

if __name__ == '__main__':
    main()
