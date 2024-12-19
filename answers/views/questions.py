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
    permission_classes = [IsAuthenticated]  # Only authenticated users can access
    pagination_class = CustomPagination  # Add pagination



PROFESSION_SCORES = {
    # Example structure: {question_id: {option: {profession: score}}}
    1: {"A": {"Frontend": 2}, "B": {"Backend": 2}, "C": {"Q/A": 1}, "D": {"DevOps": 3}},
    2: {"A": {"PM": 3}, "B": {"Q/A": 1}, "C": {"Frontend": 1}, "D": {"Backend": 1}},
    # Add mappings for all your questions
}

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
        profession_scores = {"Frontend": 0, "Backend": 0, "Q/A": 0, "DevOps": 0, "PM": 0}  # Initialize scores

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


            if question_id in PROFESSION_SCORES and selected_option in PROFESSION_SCORES[question_id]:
                for profession, score in PROFESSION_SCORES[question_id][selected_option].items():
                    profession_scores[profession] += score


        best_profession = max(profession_scores, key=profession_scores.get)


        prompt = f"The user aligns well with a career in {best_profession}. Could you share tailored advice, \
        growth opportunities, or skills to focus on for excelling in this field? and make a short summary."

        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            gemini_response = response.text

            # Save the gemini_response to each answer
            for answer in saved_answers:
                answer.gemini_response = gemini_response
                answer.save()
        except Exception as e:
            gemini_response = f"Error generating chatbot response: {str(e)}"
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Gemini API error: {str(e)}")


        if saved_answers:
            timestamp = saved_answers[0].timestamp
        else:
            timestamp = None

        return Response(
            {
                "saved_answer": {
                    "id": saved_answers[0].id if saved_answers else None,
                    "user": request.user.id,
                    "timestamp": timestamp,
                    "gemini_response": gemini_response,
                    "best_profession": best_profession
                }
            },
            status=status.HTTP_201_CREATED
        )
