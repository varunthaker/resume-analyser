import os
from dotenv import load_dotenv
from rest_framework import status
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from rest_framework.response import Response
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import OpenAI


def load_api_key(model_name):
    load_dotenv()
    api_key = os.getenv(model_name)
    if not api_key:
        raise ValueError(f"API key for {model_name} not found in environment variables")
    return api_key
    
     

def get_pdf_text(uploaded_file): 
    temp_file_path = f"/tmp/{uploaded_file}"

    # save temp file at location in chunks
    with open(temp_file_path, 'wb') as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)
    try:
        # get pdf and split the text in chunks
        loader = PyPDFLoader(temp_file_path)
        document= loader.load()
        raw_text= "\n".join([doc.page_content for doc in document])

        text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,  
        chunk_overlap=100  
                )
    except Exception as e:
                os.remove(temp_file_path)   
                return Response({'message': f"Error extracting text: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    pdf_text = text_splitter.split_text(raw_text)

    os.remove(temp_file_path)


    return pdf_text

def get_prompt(selected_language):
    prompt_question = '''You are a professional resume expert. Your task is to analyze the provided resume text and provide specific, actionable feedback to improve it based on standard best practices.'''
    model_response_format = '''Analyze the resume based on the following criteria:  

1. **Contact Details**:  
   - Ensure the contact details include only the essential information: name, email, phone number, and a partial address (e.g., 13353 Berlin, Germany).  
   - Check for relevant social media links, such as LinkedIn, Xing, personal website, or GitHub.  
   - Summarize who the person is (e.g., software developer, data analyst).  

2. **Education**:  
   - Verify that degrees (Bachelor’s, Master’s, or special training) are included.  
   - Check if the university name, grades, durations, and important subjects are mentioned.  
   - Suggest adding missing details, such as grades or incomplete degree descriptions.  

3. **Experience**:  
   - Ensure each job entry includes the job title, company name, location, duration, and responsibilities.  
   - Verify that descriptions use bullet points, action verbs (e.g., “led,” “developed,” “managed”), and quantify achievements where possible.  

4. **Projects**:  
   - Assess whether project descriptions follow the STAR method (Situation, Task, Action, Result).  
   - Check for bullet points and action verbs.  
   - Verify the inclusion of project links (e.g., GitHub, portfolio) if needed.  

5. **Skills**:  
   - Ensure both technical and soft skills are mentioned.  
   - Check if the skills are organized in a list format.  

6. **Languages**:  
   - Ensure international languages such as English and German are mentioned.  
   - Verify the proficiency level is specified (e.g., B1, fluent).  

7. **Certificates**:  
   - Check that all relevant certificates are listed clearly. 

**General Instructions**:
    - Ensure proper formatting throughout the resume.  
    - If any information is missing or incomplete in a section, include it as a feedback suggestion.  
    - Feedback should be actionable and concise, focusing on improvements and filling gaps.  
'''
    example_output = '''Return the feedback in JSON format as follows:  

{
    "body": {
        "contact_details": [
            "Feedback point 1 for contact details",
            "Feedback point 2 for contact details"
        ],
        "education": [
            "Feedback point 1 for education",
            "Feedback point 2 for education"
        ],
        "experience": [
            "Feedback point 1 for experience",
            "Feedback point 2 for experience"
        ],
        "projects": [
            "Feedback point 1 for projects",
            "Feedback point 2 for projects"
        ],
        "skills": [
            "Feedback point 1 for skills",
            "Feedback point 2 for skills"
        ],
        "languages": [
            "Feedback point 1 for languages",
            "Feedback point 2 for languages"
        ],
        "certificates": [
            "Feedback point 1 for certificates",
            "Feedback point 2 for certificates"
        ]
    }
}
'''
    response_language = f'The response should be in {selected_language} Language.'

    prompt_sentense = f"""
        {prompt_question}

        {model_response_format}

        {response_language}

        Return only the JSON object in the following format:

        # Example Output template:
        {example_output}
        """
    return prompt_sentense

def get_response_from_Gemini(resume_text, selected_language):
        
    GOOGLE_API_KEY = load_api_key('GOOGLE_API_KEY')
    model_name = "gemini-pro"

    prompt = get_prompt(selected_language) + f"\nResume Text:\n{resume_text}"

    llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=GOOGLE_API_KEY)

    response = llm.invoke(prompt)
    return response

def get_response_from_chatGPT(resume_text, selected_language):
    load_dotenv()
    OPENAI_API_KEY = load_api_key("OPENAI_API_KEY")
    model_name = "gpt-3.5-turbo"

    prompt = get_prompt(selected_language) + f"\nResume Text:\n{resume_text}"

    llm = OpenAI(temperature= 0.7, model=model_name, openai_api_key=OPENAI_API_KEY, max_tokens=500)
    response = llm.invoke(prompt)

    print("response", response)
    return response
      