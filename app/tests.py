from django.test import TestCase
from app.constants import SUCCESSFUL,FAILED
from rest_framework.test import APIClient
from rest_framework import status
from app.models import Service, Transaction
from app.utility import  sign_request
from django.urls import reverse
from datetime import date
from django.core.cache import cache
import json

class NationalIDAPITest(TestCase):
    """Unit tests for the NationalIDAPI endpoint."""

    def setUp(self):
        self.service = Service.objects.create(
            service_name="Test Service",
            is_active=True,
        )
        self.client = APIClient()
        self.url = reverse('nationalid-data')
        self.payload = {
            "country_code": "EG",
            "national_id": "29802090101517"
        }
    
    def tearDown(self):
        cache.clear()

    def test_post_success(self):
        """Test the API with a valid request."""
        
        signature = sign_request(self.service.private_key)


        response = self.client.post(
            self.url,
            data=self.payload,
            headers={
                "X-PUBLIC-KEY": self.service.public_key,
                "X-SIGNATURE": signature,
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("birth_date"), date(1998, 2, 9))
        self.assertEqual(response.data.get("gender"), "Male")

        transaction = Transaction.objects.last()
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.status, SUCCESSFUL)
        

    def test_post_failure_invalid_national_id(self):
        """Test the API with an invalid national ID."""

        signature = sign_request(self.service.private_key)
        self.payload['national_id'] = "99000000101517"

        response = self.client.post(
            self.url,
            data=self.payload,
            headers={
                "X-PUBLIC-KEY": self.service.public_key,
                "X-SIGNATURE": signature,
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Invalid date in National ID.")

        transaction = Transaction.objects.last()
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.status, FAILED)
    
    def test_post_failure_invalid_signature(self):
        """Test the API with an invalid signature."""
        invalid_signature = "invalid_signature"

        response = self.client.post(
            self.url,
            data=self.payload,
            headers={
                "X-PUBLIC-KEY": self.service.public_key,
                "X-SIGNATURE": invalid_signature,
            }
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Invalid signature")


    def test_post_failure_rate_limit_exceeded(self):
        """Test the API when the rate limit is exceeded."""

        signature = sign_request(self.service.private_key)
        for _ in range(5):
            response = self.client.post(
                self.url,
                data=self.payload,
                headers={
                    "X-PUBLIC-KEY": self.service.public_key,
                    "X-SIGNATURE": signature,
                }
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
    
        response = self.client.post(
            self.url,
            data=self.payload,
            headers={
                "X-PUBLIC-KEY": self.service.public_key,
                "X-SIGNATURE": signature,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertEqual(
            response.data["detail"],
            "Too many attempts. Please try again later after 5 minutes.",
        )
    
    def test_post_failure_missing_auth_headers(self):
        """Test the API with missing authentication headers."""
        signature = sign_request(self.service.private_key)
        response = self.client.post(
            self.url,
            data=self.payload,
            headers={
                "X-PUBLIC-KEY": "public key",
                "X-SIGNATURE": signature,
            }
        )
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.content.decode('utf-8'))
        
        self.assertIn('detail', response_data)
        self.assertEqual(response_data['detail'], 'Invalid API Key.')


