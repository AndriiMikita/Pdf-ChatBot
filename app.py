import streamlit
import os
from templates import CSS_T, USER_T, BOT_T
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from openai import RateLimitError
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

def get_text_from_PDF(pdf_list: list) -> str:
    """
    Extracts text from a list of PDF files.

    Args:
        pdf_list (list): A list of paths to PDF files.

    Returns:
        str: The extracted text from all PDF files.
    """
    
    text = ""
    
    for pdf in pdf_list:
        pdf_reader = PdfReader(pdf)
        
        for page in pdf_reader.pages:
            text += page.extract_text()
            
    return text

def text_to_chunks(text: str) -> list[str]:
    """
    Splits text into chunks.

    Args:
        text (str): The input text to be split.

    Returns:
        list[str]: A list of text chunks.
    """
    
    text_splitter = RecursiveCharacterTextSplitter(
                                                    chunk_size = 1000,
                                                    chunk_overlap = 200,
                                                    length_function = len,
                                                    separators="\n",)
    chunks = text_splitter.split_text(text)
    
    return chunks

def create_vectorstore(data: list[str]) -> FAISS:
    """
    Creates a FAISS vector store from a list of text data.

    Args:
        data (list[str]): A list of text data.

    Returns:
        FAISS: The created FAISS vector store.
    """
    
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(data, embedding=embeddings)
    
    return vectorstore
                
def process_userinput(query: str) -> None:
    """
    Processes user input and generates a response.

    Args:
        query (str): The user's input question.
    """
    
    if streamlit.session_state.conversation is None:
        streamlit.write(BOT_T.replace("{{MSG}}", 
                                      "Please upload the files so I can answer your questions."), 
                        unsafe_allow_html=True)
        
        return
    
    try:
        response = streamlit.session_state.conversation({'question': query})
    except RateLimitError as e:
        streamlit.write(BOT_T.replace("{{MSG}}", 
                                      "Sorry, you've reached the limit for requests. Please try again later."), 
                        unsafe_allow_html=True)
        return

    streamlit.session_state.chat_history = response['chat_history']

    for i in range(len(streamlit.session_state.chat_history) - 2, -1, -2):
        messageHuman = streamlit.session_state.chat_history[i]
        messageAI = streamlit.session_state.chat_history[i + 1]
        
        streamlit.write(USER_T.replace("{{MSG}}", 
                                       messageHuman.content), 
                        unsafe_allow_html=True)
        streamlit.write(BOT_T.replace("{{MSG}}", 
                                      messageAI.content), 
                        unsafe_allow_html=True)
        
    if len(streamlit.session_state.chat_history) > 100:
        streamlit.session_state.chat_history = None
        
def get_llm_chain(vectorstore: FAISS):
    """
    Creates a conversational retrieval chain using an LLM and a vector store.

    Args:
        vectorstore (FAISS): The vector store to use for retrieval.

    Returns:
        ConversationalRetrievalChain: The created retrieval chain.
    """
    
    llm = OpenAI(temperature=0)
    memory = ConversationBufferMemory(memory_key='chat_history', 
                                      return_messages=True, 
                                      human_prefix="You", 
                                      ai_prefix="AI",)
    chain = ConversationalRetrievalChain.from_llm(llm=llm,
                                                  retriever=vectorstore.as_retriever(),
                                                  memory=memory,)
    
    return chain

def process_data(pdf_list: list) -> None:
    """
    Processes PDF files and creates a conversational retrieval chain.

    Args:
        pdf_list (list): A list of paths to PDF files.
    """
    
    user_text = get_text_from_PDF(pdf_list)
                    
    chunked_data = text_to_chunks(user_text)
    
    vectorstore = create_vectorstore(chunked_data)
    
    streamlit.session_state.conversation = get_llm_chain(vectorstore)
    
def process_test_data() -> None:
    """
    Processes test data for running predefined test questions.
    """
    
    pdf_files = []
    test_data_path = "./test_data"
    if os.path.exists(test_data_path) and os.path.isdir(test_data_path):
        for file_name in os.listdir(test_data_path):
            if file_name.endswith(".pdf"):
                pdf_files.append(os.path.join(test_data_path, file_name))
        
        if pdf_files:
            process_data(pdf_files)
        else:
            streamlit.write("No PDF files found in the 'test_data' folder.")
    else:
        streamlit.write("The 'test_data' folder does not exist.")
        
def process_test_questions() -> bool:
    """
    Processes predefined test questions.

    Returns:
        bool: False to end the test run.
    """
    
    test_questions = ["Who is Andrii Mikita?", 
                      "Why should I hire Andrii Mikita?",
                      "Where are the top startups located?", 
                      "What does Stripe company do?", 
                      "How can I resolve the issue of my coffee being trapped in the machine?", 
                      "What do the colors in the 'CONTAINER' panel mean?",]
    
    placeholder = streamlit.empty()
    
    for question in test_questions:
        with placeholder.container():
            process_userinput(question)
            
        placeholder.empty()

    return False

def main() -> None:
    """
    Main function for running the Streamlit application.
    """
    
    load_dotenv()
    streamlit.set_page_config(page_title="Python Developer with AI Experience Test Task",
                       page_icon="💬")
    streamlit.write(CSS_T, unsafe_allow_html=True)

    if "conversation" not in streamlit.session_state:
        streamlit.session_state.conversation = None
    if "chat_history" not in streamlit.session_state:
        streamlit.session_state.chat_history = None
        
    streamlit.header("Chat with PDF")
    
    query = streamlit.text_input("Ask questions about your PDFs:")
    
    if query:
        with streamlit.spinner("Looking for answers..."):
            process_userinput(query)

    run_tests = False 
     
    with streamlit.sidebar:
        user_pdf_list = streamlit.file_uploader(
                                                "Upload your PDFs!", type='pdf', 
                                                accept_multiple_files=True,)
        if user_pdf_list:
            if streamlit.button("Process"):
                with streamlit.spinner("In progress..."):
                    process_data(user_pdf_list)
                    
        if streamlit.button("Run Tests"):
            with streamlit.spinner("Runnig tests..."):
                process_test_data()
                
                run_tests = True
                
    if run_tests:
        with streamlit.spinner("Looking for answers..."):
            run_tests = process_test_questions()

                    
if __name__ == '__main__':
    main()
