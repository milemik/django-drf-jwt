from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    posted_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(max_length=100)
    body = models.TextField()
    published = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
