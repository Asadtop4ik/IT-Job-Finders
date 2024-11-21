import openai
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from answers.serializers import GPTRequestSerializer

class GPTView(APIView):
    def post(self, request):
        serializer = GPTRequestSerializer(data=request.data)
        if serializer.is_valid():
            prompt = serializer.validated_data['prompt']
            try:
                openai.api_key = settings.OPENAI_API_KEY
                response = openai.Completion.create(
                    engine="text-davinci-003",  # or another engine
                    prompt=prompt,
                    max_tokens=150
                )
                return Response(response.choices[0].text.strip(), status=status.HTTP_200_OK)
            except Exception as e:
                return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
