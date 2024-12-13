from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SmallWin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    duration = models.CharField(max_length=100, blank=True, null=True)  # Masalan, 30 minut uchun
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.description}"
