from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from answers.serializers import GeminiChatbotSerializer
import google.generativeai as genai

# Configure the API key for Google Generative AI
genai.configure(api_key='AIzaSyA7Uu3ZXbBPbzM1eDUmoGx0-ek14xsllAc')


class GeminiChatbotView(APIView):
    @extend_schema(
        summary="Generate a response using Google's Gemini API",
        description="This endpoint takes a user prompt and generates a response using the Google Generative AI Gemini model.",
        request=GeminiChatbotSerializer,  # Use the serializer for the request schema
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
        # Validate the request body using the serializer
        serializer = GeminiChatbotSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract the validated prompt
        user_prompt = serializer.validated_data['prompt']

        try:
            # Initialize the Gemini model
            model = genai.GenerativeModel("gemini-1.5-flash")

            # Generate content using the Gemini model
            response = model.generate_content(user_prompt)

            # Return the generated response
            return Response({"prompt": user_prompt, "response": response.text}, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any errors (e.g., invalid API key, network issues, etc.)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
