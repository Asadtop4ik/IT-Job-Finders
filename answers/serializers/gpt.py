from rest_framework import serializers

class GPTRequestSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=1000)
