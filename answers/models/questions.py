from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Question(models.Model):
    text = models.TextField()  # The question text
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the authenticated user
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Link to the question
    selected_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])  # User's selected answer
    timestamp = models.DateTimeField(auto_now_add=True)  # When the answer was submitted
    gemini_response = models.TextField(null=True, blank=True)  # Store the Gemini API response

    def __str__(self):
        return f"User: {self.user}, Question: {self.question}, Answer: {self.selected_option}"

class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.name
