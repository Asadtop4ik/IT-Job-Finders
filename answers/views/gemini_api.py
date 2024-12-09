from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from answers.serializers import GeminiChatbotSerializer
import google.generativeai as genai


genai.configure(api_key='AIzaSyA7Uu3ZXbBPbzM1eDUmoGx0-ek14xsllAc')


class GeminiChatbotView(APIView):
    @extend_schema(
        summary="Generate a response using Google's Gemini API",
        description="This endpoint takes a user prompt and generates a response using the Google Generative AI Gemini model.",
        request=GeminiChatbotSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "example": "Explain how AI works."},
                    "response": {"type": "string", "example": "AI works by using machine learning algorithms..."},
                },
            },
            400: {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Prompt is required."},
                },
            },
            500: {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "An unexpected error occurred."},
                },
            },
        },
    )
    def post(self, request):
        serializer = GeminiChatbotSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        user_prompt = serializer.validated_data['prompt']

        try:

            model = genai.GenerativeModel("gemini-1.5-flash")


            response = model.generate_content(user_prompt)


            return Response({"prompt": user_prompt, "response": response.text}, status=status.HTTP_200_OK)

        except Exception as e:

            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
