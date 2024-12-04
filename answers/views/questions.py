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

    def perform_create(self, serializer):
        """
        Automatically associate the logged-in user with the answer
        """
        serializer.save(user=self.request.user)  # Assign the authenticated user to the answer
