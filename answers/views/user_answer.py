from django.http import JsonResponse
from answers.models import Answer
from answers.serializers import AnswerSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_answers_by_user(request, user_id):
    """
    Custom view to fetch answers for a specific user with pagination.
    """
    answers = Answer.objects.filter(user_id=user_id)

    if not answers.exists():
        return JsonResponse({"message": "No answers found for this user."}, status=404)

    # Apply pagination
    paginator = PageNumberPagination()
    paginator.page_size = 10  # Number of items per page
    paginated_answers = paginator.paginate_queryset(answers, request)

    # Serialize the paginated data
    serializer = AnswerSerializer(paginated_answers, many=True)

    # Return paginated response
    return paginator.get_paginated_response(serializer.data)
