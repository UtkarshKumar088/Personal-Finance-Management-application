from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Health', 'Health'),
        ('Electronics', 'Electronics'),
        ('Travel', 'Travel'),
        ('Education', 'Education'),
        ('Books', 'Books'),
        ('Others', 'Others'),
    ]

   
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    name = models.CharField(max_length=140)
    date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    amount = models.PositiveIntegerField()

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_expenses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
