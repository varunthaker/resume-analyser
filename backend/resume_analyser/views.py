from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UploadedCvData
from .serializers import UploadedCvDataSerializer
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv


import io


class upload_resume(APIView):

    def post(self, request, *args, **kwargs):

        def get_response_from_chatGPT(text):
            load_dotenv()
            OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
            model_name = "gpt-3.5-turbo"

            # initiate model
            llm = OpenAI(temperature= 0.7, model = model_name, openai_api_key=OPENAI_API_KEY, max_tokens=500)
            
    
            # question to ask
            prompt = PromptTemplate(input_variables=["text"], template="You are a helpful assistant. Respond to the following text:\n\n{text}")
            formated_prompt = prompt.format(text=text)

            #answer to get
            result = llm(formated_prompt)
            return result

        print("data received", request.data)

        data_received = request.data

        if 'resumeFile' not in data_received:
            return Response({'message': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UploadedCvDataSerializer(data=request.data)


        if serializer.is_valid():
            serializer.save()  

            uploaded_file = data_received['resumeFile']
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
                
                pdf_text = text_splitter.split_text(raw_text)
                print("extracted_text", pdf_text)

                os.remove(temp_file_path)

                text = "Please tell me capital of Mumbai"
                response = get_response_from_chatGPT(text)
                print("response", response)


            except Exception as e:
                os.remove(temp_file_path)   
                return Response({'message': f"Error extracting text: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'File uploaded successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)

    def get(self, request):
        return Response({'message': 'Get request Sucess'}, status=status.HTTP_200_OK)
    



