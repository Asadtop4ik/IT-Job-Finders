# import openai
# from django.conf import settings
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from answers.models import UserResponse
#
# openai.api_key = "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"
#
# class ResultView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         responses = UserResponse.objects.filter(user=request.user)
#         answers = {response.question.text: response.answer for response in responses}
#
#         # Send responses to GPT API
#         gpt_prompt = f"Analyze the following answers and determine the user's proficiency in backend and frontend development:\n{answers}"
#         gpt_response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": "You are an IT job profiler."},
#                 {"role": "user", "content": gpt_prompt},
#             ]
#         )
#         result = gpt_response['choices'][0]['message']['content']
#         return Response({"result": result})



