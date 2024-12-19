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
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

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


            answer, created = Answer.objects.update_or_create(
                user=request.user,
                question=question,
                defaults={'selected_option': selected_option}
            )
            saved_answers.append(answer)


        prompt = (
            "Based on the user's responses to a career questionnaire, analyze and determine the 5 most suitable professions "
            "for the user. Include the professions with their suitability percentages and provide a concise explanation for each profession. "
            "The responses are summarized internally and do not need to be shown explicitly in the output."
        )

        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            gemini_response = response.text


            for answer in saved_answers:
                answer.gemini_response = gemini_response
                answer.save()
        except Exception as e:
            gemini_response = f"Error generating chatbot response: {str(e)}"
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Gemini API error: {str(e)}")


        return Response(
            {
                "user_id": request.user.id,
                "gemini_response": gemini_response
            },
            status=status.HTTP_201_CREATED
        )

