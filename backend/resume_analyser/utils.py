import json
import os
from venv import logger
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.response import Response
from langchain_google_genai import ChatGoogleGenerativeAI
import openai
from PyPDF2 import PdfReader

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
        reader = PdfReader(temp_file_path)
        raw_text = ""
        for page in reader.pages:
            raw_text += page.extract_text() + "\n"


        chunk_size=1000 
        chunk_overlap=100  
        pdf_text = []
        start = 0
                
        while start < len(raw_text):
            end = min(start + chunk_size, len(raw_text))
            pdf_text.append(raw_text[start:end])
            start += chunk_size - chunk_overlap
    except Exception as e:
        os.remove(temp_file_path)   
        return {'message': f"Error extracting text: {str(e)}"}
        
    
    os.remove(temp_file_path)
    return pdf_text

def get_prompt(selected_language):
    prompt_question = '''You are a professional resume expert. Your task is to analyze the provided resume text and provide specific, actionable feedback to improve it based on standard best practices.'''
    model_response_format = '''Analyze the resume based on the following criteria:  

1. **Contact Details**:  
   - Ensure the contact details include only the essential information: name, email, phone number, and partial address (e.g., 13353 Berlin, Germany).  
   - Ensure that the resume includes a relevant social media profile (LinkedIn, GitHub, etc.).  
   - Consider if the profile section provides a strong overview of who the person is (e.g., software developer, data analyst). If not, add a brief personal summary.

2. **Education**:  
   - Verify that degrees (Bachelor’s, Master’s, or special training) are included.  
   - Include university names, graduation years, and major subjects.  
   - Suggest adding grades (if impressive) or relevant coursework. If not complete, clarify the degree status. 
   - If available, list academic projects that demonstrate the candidate's skills.

3. **Experience**:  
   - Verify that each job includes job title, company name, location, duration, and responsibilities. 
   - Ensure that job descriptions use action verbs and are achievement-oriented (e.g., “led,” “improved,” “optimized”).
   - Quantify achievements where possible (e.g., “Reduced system errors by 30% through bug fixes”).

4. **Projects**:  
   - Ensure that project descriptions use the STAR method (Situation, Task, Action, Result). 
   - Check for bullet points and action verbs.  
   - If available, add project links (e.g., GitHub, portfolio) to show real-world examples of work.
 
5. **Skills**:  
   - Ensure both technical and soft skills are included. 
   - Organize the skills in categories (e.g., technical, soft skills).
   - Ensure bullet points are concise and action-oriented.
   - Suggest providing examples from experience where those skills were applied.

6. **Languages**:  
   - Ensure international languages (English, German) are mentioned. 
   - Specify proficiency level (e.g., B1, fluent) and consider adding certifications or tests, if applicable.

7. **Certificates**:  
   - Ensure that all relevant certifications are listed clearly. If missing, suggest including any certifications that demonstrate relevant expertise.

**General Instructions**:
    - Focus on proper formatting throughout the resume (e.g., consistency in bullet points, headers).  
    - Offer suggestions on improving structure and visual appeal.  
    - Suggest adding missing information or improving incomplete sections.
'''
    example_output = '''Return the feedback in JSON format as follows:  

{
    "body": {
        "contactDetails": [
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
    response_language = f'Please provide the feedback in {selected_language}. Do not translate the example output, but ensure the feedback is in {selected_language}. If the resume is in a different language, analyze it in its original form, but provide all feedback in {selected_language}.'

    prompt_sentense = f"""
        {prompt_question}

        {model_response_format}

        {response_language}

        Return only the JSON object below, with no additional commentary or explanation:

        # Example Output template:
        {example_output}

        (Ensure the JSON object is not wrapped in any code block and contains only the feedback, no text before or after it.)
        """
    return prompt_sentense

def get_response_from_Gemini(resume_text, selected_language):
        
    GOOGLE_API_KEY = load_api_key('GOOGLE_API_KEY')
    model_name = "gemini-pro"

    prompt = get_prompt(selected_language) + f"\nResume Text:\n{resume_text}"

    llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=GOOGLE_API_KEY)

    try:

        response = llm.invoke(prompt)
        if hasattr(response, "content"):
            content = response.content

        if isinstance(response, str):
            response_json = json.loads(response) 
        else:
            response_json = response
        return response_json

    except Exception as e:
        return f"An error occurred while processing the gemini request: {str(e)}"

def get_response_from_chatGPT(resume_text, selected_language):
    load_dotenv()
    OPENAI_API_KEY = load_api_key("OPENAI_API_KEY")
    openai.api_key = OPENAI_API_KEY
    
    model_name = "gpt-3.5-turbo"

    prompt = get_prompt(selected_language) + f"\nResume Text:\n{resume_text}"

    try:
        response = openai.chat.completions.create(
            model =model_name,
            messages = [{"role": "system", "content": "You are a professional resume expert. Provide feedback in a structured, actionable manner, formatted strictly as JSON."},{"role": "user", "content": prompt},], 
            temperature=0.7, 
            max_tokens=500, 
        )
        if response:
            content =  response.choices[0].message.content
            if content:
                response_content = content.strip('```json\n').strip('```')
                response_json = json.loads(response_content)
                return response_json
            else:
                raise ValueError("AI model returned an empty response.")
        else:
            raise ValueError("No valid response from AI model.")
    except Exception as e:
        logger.error(f"Error while communicating with ChatGPT: {e}", exc_info=True)
        return "An error occurred while processing the request."

    
      