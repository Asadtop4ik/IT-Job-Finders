from rest_framework import serializers
from answers.models import SmallWin

class SmallWinSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmallWin
        fields = ['id', 'user', 'description', 'duration', 'date_created']
