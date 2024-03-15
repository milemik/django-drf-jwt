from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient


class JWTTests(TestCase):
    def setUp(self):
        self.username = "test@test.com"
        self.password = "test124356"
        self.user = get_user_model().objects.create(email=self.username)
        self.user.set_password(self.password)
        self.user.save()
        self.client = APIClient()

        self.url = reverse("django_drf_jwt:get_token")
        self.revoke_url = reverse("django_drf_jwt:revoke_token")

    def test_jwt_auth_init(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get("password")[0], "This field is required.")
        self.assertEqual(response.json().get("email")[0], "This field is required.")

    def test_jwt_auth_wrong_cred(self):
        response = self.client.post(self.url, {"email": "test@test.com", "password": "testing123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get("non_field_errors")[0], "Unable to authenticate with provided credentials")

    def test_jwt_auth(self):
        response = self.client.post(self.url, {"email": self.username, "password": self.password})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.json().get("token").split(".")), 3, "Expect JWT Token created")
        self.assertIn("created", response.json().keys(), "Expect created in response body")

    def test_revoke_token_init(self):
        response = self.client.post(self.revoke_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_revoke_token(self):
        response = self.client.post(self.url, {"email": self.username, "password": self.password})
        token = response.json().get("token")
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

        response = self.client.post(self.revoke_url, {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials()
