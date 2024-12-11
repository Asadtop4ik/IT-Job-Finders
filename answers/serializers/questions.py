from rest_framework import serializers
from answers.models import Question, Answer, Contact


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'option_a', 'option_b', 'option_c', 'option_d']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'user', 'question', 'selected_option', 'timestamp', 'gemini_response']
        read_only_fields = ['user', 'timestamp', 'gemini_response']



class SingleAnswerSerializer(serializers.Serializer):
    question = serializers.IntegerField()
    selected_option = serializers.CharField(max_length=1)

class BulkAnswerSerializer(serializers.Serializer):
    answers = serializers.ListField(
        child=SingleAnswerSerializer(),
        help_text="A list of answers with question IDs and selected options."
    )




class GeminiChatbotSerializer(serializers.Serializer):
    prompt = serializers.CharField(
        required=True,
        max_length=500,
        help_text="The user prompt for the chatbot."
    )

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

