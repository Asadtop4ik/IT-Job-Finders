from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from answers.models import Question, Answer
from answers.serializers import QuestionSerializer, AnswerSerializer


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

    def create(self, request, *args, **kwargs):
        """
        Save the user's answer to a question.
        Prevent duplicate answers for the same question.
        """
        question_id = request.data.get('question')
        selected_option = request.data.get('selected_option')

        # Check if the user has already answered this question
        if Answer.objects.filter(user=request.user, question_id=question_id).exists():
            return Response(
                {"error": "You have already answered this question."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate and save the answer
        data = request.data.copy()
        data['user'] = request.user.id  # Set the authenticated user

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
