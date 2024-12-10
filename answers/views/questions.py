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
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access
    pagination_class = CustomPagination  # Add pagination


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can answer questions
    pagination_class = CustomPagination  # Add pagination

    def get_queryset(self):
        return Answer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='bulk', serializer_class=BulkAnswerSerializer)
    def bulk_create(self, request):
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

            # Use update_or_create to prevent duplicates
            answer, created = Answer.objects.update_or_create(
                user=request.user,
                question=question,
                defaults={'selected_option': selected_option}
            )
            saved_answers.append(answer)

        # Build the prompt for the Gemini API
        prompt = "Here are the user's answers:\n"
        for answer in saved_answers:
            prompt += f"Question: {answer.question.text}\n"
            prompt += f"Options: A) {answer.question.option_a}, B) {answer.question.option_b}, C) {answer.question.option_c}, D) {answer.question.option_d}\n"
            prompt += f"Answer: {answer.selected_option}\n"

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
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Gemini API error: {str(e)}")

        created_count = len(
            [answer for answer in saved_answers if answer.timestamp == answer.timestamp])  # Count new answers
        updated_count = len(saved_answers) - created_count

        return Response(
            {
                "created_answers": created_count,
                "updated_answers": updated_count,
                "saved_answers": AnswerSerializer(saved_answers, many=True).data
            },
            status=status.HTTP_201_CREATED
        )


