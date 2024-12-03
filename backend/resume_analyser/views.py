import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from resume_analyser.utils import get_pdf_text, get_prompt, get_response_from_Gemini, get_response_from_chatGPT
from .models import UploadedCvData
from .serializers import UploadedCvDataSerializer
import os
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import io




class upload_resume(APIView):



    def post(self, request, *args, **kwargs):

        data_received = request.data

        print("data received", data_received)

        if 'resumeFile' not in data_received:
            return Response({'message': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_file = data_received['resumeFile']
        selected_language = data_received['language']
        selected_AI_Model = data_received['aiModel']

        print("selected_language",selected_language)
        print("selected_AI_Model", selected_AI_Model)


        resume_text = get_pdf_text(uploaded_file)

        if selected_AI_Model == 'OPENAI_GPT':
            response = get_response_from_chatGPT(resume_text, selected_language)
        elif selected_AI_Model == 'GOOGLE_GEMINI':
            response = get_response_from_Gemini( resume_text, selected_language)

        
        response_json = json.loads(response.content)

        return Response({'message': 'File uploaded successfully', 'data':response_json.get("body", "No body found") }, status=status.HTTP_201_CREATED)

    def get(self, request):
        return Response({'message': 'Get request Sucess'}, status=status.HTTP_200_OK)
    



