import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from answers.serializers import GPTRequestSerializer

class GPTAPIView(APIView):
    def post(self, request):
        serializer = GPTRequestSerializer(data=request.data)
        if serializer.is_valid():
            prompt = serializer.validated_data['prompt']
            response = self.get_gpt_response(prompt)
            return Response({'response': response}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_gpt_response(self, prompt):
        api_key = os.getenv('OPENAI_API_KEY')
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }
        data = {
            'model': 'text-davinci-003',
            'prompt': prompt,
            'max_tokens': 500,
        }
        response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
        if response.status_code == 200:
            return response.json().get('choices', [{}])[0].get('text', '')
        return 'Error: Unable to get response from GPT API'
