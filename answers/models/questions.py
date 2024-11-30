# from django.db import models
# from django.conf import settings
#
#
# class Question(models.Model):
#     text = models.TextField()  # The question text
#     option_a = models.CharField(max_length=255)
#     option_b = models.CharField(max_length=255)
#     option_c = models.CharField(max_length=255)
#     option_d = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.text
#
#
# class Answer(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to the authenticated user
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Link to the question
#     selected_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])  # User's selected answer
#     timestamp = models.DateTimeField(auto_now_add=True)  # When the answer was submitted
#
#     def __str__(self):
#         return f"User: {self.user}, Question: {self.question}, Answer: {self.selected_option}"
