from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from answers.models import Question, Answer
from answers.serializers import AnswerSerializer, BulkAnswerSerializer, QuestionSerializer
import google.generativeai as genai
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from config.settings import GEMINI_API_KEY


genai.configure(api_key=GEMINI_API_KEY)


class CustomPagination(PageNumberPagination):
    """
    Custom pagination for large datasets
    """
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100


class QuestionViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for Questions
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access
    pagination_class = CustomPagination  # Add pagination


class AnswerViewSet(viewsets.ModelViewSet):
    """
    Handles saving user answers to questions
    """
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can answer questions
    pagination_class = CustomPagination  # Add pagination

    def get_queryset(self):
        """
        Filter answers so that users only see their own answers
        """
        return Answer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically associate the logged-in user with the answer
        """
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='bulk', serializer_class=BulkAnswerSerializer)
    def bulk_create(self, request):
        """
        Handle bulk answer submission and generate a single response from the Gemini API
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        answers_data = serializer.validated_data['answers']


        saved_answers = []
        for answer_data in answers_data:
            question_id = answer_data['question']
            selected_option = answer_data['selected_option']


            try:
                question = Question.objects.get(id=question_id)
            except Question.DoesNotExist:
                return Response(
                    {"error": f"Question with ID {question_id} does not exist."},
                    status=status.HTTP_400_BAD_REQUEST
                )


            answer = Answer.objects.create(
                user=request.user,
                question=question,
                selected_option=selected_option
            )
            saved_answers.append(answer)


        prompt = "Here are the user's answers:\n"
        for answer in saved_answers:
            prompt += f"Question: {answer.question.text}\nAnswer: {answer.selected_option}\n"

        prompt += "\nBased on these answers, what profession or career path would you recommend for the user?"

        try:

            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            chatbot_response = response.text


            for answer in saved_answers:
                answer.gemini_response = chatbot_response
                answer.save()
        except Exception as e:
            chatbot_response = f"Error generating chatbot response: {str(e)}"


        return Response(
            {
                "saved_answers": AnswerSerializer(saved_answers, many=True).data,
                "chatbot_response": chatbot_response
            },
            status=status.HTTP_201_CREATED
        )
