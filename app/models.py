from django.db import models
from django.contrib.auth.models import User

class SavedCompany(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    challenge_type = models.CharField(max_length=100, default='All')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'company_name', 'challenge_type')

    def __str__(self):
        return f"{self.user.username} - {self.company_name} ({self.challenge_type})"

class SolvedQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    question_name = models.CharField(max_length=500)
    solved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'company_name', 'question_name')

    def __str__(self):
        return f"{self.user.username} solved {self.question_name} in {self.company_name}"
