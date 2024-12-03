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
    prompt_question = '''You are the resume expert. Please Analyse the resume text'''
    model_response_format = '''The Response format should be of json with the key "body".
                            The body should be as a plain text.'''
    example_output = '''{"body": ""  }'''
    response_language = 'The response should be in %s Language.' % (selected_language)

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
      