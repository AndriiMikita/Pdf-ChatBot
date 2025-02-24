# CV Comparison Chat

An interactive web application that compares CVs against job descriptions using Google's Gemini AI model. The app provides automated analysis and allows users to ask follow-up questions about the comparison.

## Features

- **CV Upload**: Support for PDF format CVs
- **Job Description Analysis**: Paste any job description for comparison
- **Automated Comparison**: 
  - Identifies key job requirements
  - Calculates CV-job position match percentage
  - Suggests improvements for the CV
  - Provides pros and cons analysis
- **Interactive Chat**: Ask follow-up questions about the comparison
- **Markdown Support**: AI responses are formatted with markdown for better readability
- **Real-time Updates**: New messages appear at the top of the conversation

## Setup

1. Clone the repository
2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory of your project and add your Google API key:

   ```
   PALM_API_KEY=your_api_key_here
   ```

4. Run the application:

   ```
   streamlit run app.py
   ```

## Usage

1. Upload your CV (PDF format) using the sidebar
2. Paste the job description in the provided text area
3. Click "Compare CV and Job" to get the initial analysis
4. Use the chat input field to ask specific questions about the comparison

## Dependencies

- streamlit
- python-dotenv
- PyPDF2
- google-generativeai
- python 3.8+

## Notes

- Remember to replace `your_api_key_here` with your actual Google API key in the `.env` file.
- This application relies on external services (Streamlit, Google Generative AI) and may incur costs or be subject to rate limits.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
