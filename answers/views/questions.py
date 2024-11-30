# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from answers.models import Question, UserResponse
# from answers.serializers import QuestionSerializer, UserResponseSerializer
#
# class QuestionListView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         questions = Question.objects.all()[:20]
#         serializer = QuestionSerializer(questions, many=True)
#         return Response(serializer.data)
#
# class UserResponseView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         data = request.data
#         data['user'] = request.user.id
#         serializer = UserResponseSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)
