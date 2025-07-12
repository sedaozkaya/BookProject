
from django.db import models
from django.contrib.auth.models import User
import random
import string

def generate_code():
    return ''.join(random.choices(string.digits, k=6))

class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, default=generate_code)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.code}"
