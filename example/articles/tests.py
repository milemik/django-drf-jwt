from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from articles.models import Article


class ArticleTest(TestCase):
    def setUp(self):
        self.username = "test"
        self.password = "testpass123"
        user = User.objects.create(username=self.username)
        user.set_password(self.password)
        user.save()
        self.article = Article.objects.create(posted_by=user, title="Test", body="Hello there")
        self.url = reverse("articles:article_list")
        self.client = APIClient()

        self.get_token_url = reverse("django_drf_jwt:get_token")

    def test_article_list_api_init(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_article_detail_api(self):
        # Get token
        response = self.client.post(self.get_token_url, {"username": self.username, "password": self.password})
        token = response.json().get("token")
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Clean credentials
        self.client.credentials()

