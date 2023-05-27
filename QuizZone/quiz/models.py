from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Quizmaker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    id = models.CharField(max_length=5, unique=True)
    email_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    STATUS_CHOICES = [
        ('inactive', 'Inactive'),
        ('active', 'Active'),
        ('finished', 'Finished'),
    ]

    question = models.TextField()
    options = models.JSONField()
    right_answer = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive')
    creator = models.ForeignKey(Quizmaker, on_delete=models.CASCADE, related_name='created_quizzes')

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def is_finished(self):
        now = timezone.now()
        return now > self.end_date + timezone.timedelta(minutes=5)
