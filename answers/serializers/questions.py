from rest_framework import serializers
from answers.models import Question, Answer


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'option_a', 'option_b', 'option_c', 'option_d']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'user', 'question', 'selected_option', 'timestamp']
        read_only_fields = ['user', 'timestamp']  # User will be set automatically from the request
