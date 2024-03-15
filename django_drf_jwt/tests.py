from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient


class JWTTests(TestCase):
    def setUp(self):
        self.username = "test"
        self.password = "test124356"
        self.user = User.objects.create(username=self.username)
        self.user.set_password(self.password)
        self.user.save()
        self.client = APIClient()

        self.url = reverse("django_drf_jwt:get_token")

    def test_jwt_auth_init(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get("password")[0], "This field is required.")
        self.assertEqual(response.json().get("username")[0], "This field is required.")

    def test_jwt_auth_wrong_cred(self):
        response = self.client.post(self.url, {"username": "test", "password": "testing123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get("non_field_errors")[0], "Unable to authenticate with provided credentials")

    def test_jwt_auth(self):
        response = self.client.post(self.url, {"username": self.username, "password": self.password})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.json().get("token").split(".")), 3, "Expect JWT Token created")
        self.assertIn("created", response.json().keys(), "Expect created in response body")
