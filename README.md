### Chat with PDF Documentation

This application allows users to upload PDF files and ask questions about the content of those files. The application uses Streamlit for the user interface, PyPDF2 for PDF text extraction, and OpenAI for question-answering capabilities.

#### Installation
1. Clone the repository from GitHub:

   ```
   git clone https://github.com/AndriiMikita/Pdf-ChatBot
   cd Pdf-ChatBot
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory of your project and add your OpenAI API key:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

#### Usage
1. Run the application:

   ```
   streamlit run app.py
   ```

2. Upload one or more PDF files using the file uploader.

3. Ask questions about the content of the uploaded PDF files in the text input box.

4. Click the "Process" button to analyze the PDF files and find answers to your questions.

5. View the answers provided by the application in the main panel.

6. You can also click the "Run Tests" button to run predefined test questions against the prepared PDF files.

#### Components
- **templates.py:** Contains HTML templates for styling the chat interface.
- **app.py:** The main application script that defines the Streamlit UI and handles user interactions.

#### Dependencies
- Streamlit
- PyPDF2
- Langchain
- OpenAI
- dotenv

#### Notes
- Remember to replace `your_openai_api_key_here` with your actual OpenAI API key in the `.env` file.
- This application relies on external services (Streamlit, OpenAI) and may incur costs or be subject to rate limits.
