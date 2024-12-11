import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from resume_analyser.enums import LANGUAGE, AIMODEL
from resume_analyser.utils import get_pdf_text, get_response_from_Gemini, get_response_from_chatGPT
import os

class upload_resume(APIView):

    def post(self, request, *args, **kwargs):

        try: 

            data_received = request.data


            if 'resumeFile' not in data_received:
                return JsonResponse({'message': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
            
            uploaded_file = data_received['resumeFile']
            selected_language = data_received['language' ]
            selected_AI_Model = data_received['aiModel']



            # extract text from pdf
            resume_text = get_pdf_text(uploaded_file)
            if not resume_text:
                return JsonResponse({'message': 'Failed to extract text from the uploaded file.'}, status=status.HTTP_400_BAD_REQUEST)

            # get response from AI model
            if selected_AI_Model == AIMODEL.OPENAI_GPT:
                response = get_response_from_chatGPT(resume_text, selected_language)
            elif selected_AI_Model == AIMODEL.GOOGLE_GEMINI:
                response = get_response_from_Gemini( resume_text, selected_language)
            else:
                return JsonResponse({'message': f'Unsupported AI model: {selected_AI_Model}'}, status=status.HTTP_400_BAD_REQUEST)

            response_json = json.loads(response.content)

            return JsonResponse(response_json.get("body", "No body found"), status=200, safe=False)
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'message': 'Internal server error.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        return JsonResponse({'message': 'Get request Sucess'}, status=status.HTTP_200_OK)
    



