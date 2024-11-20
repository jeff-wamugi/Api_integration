from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

class SendSMSTestCase(APITestCase):
    def test_send_sms_success(self):
        # Define the endpoint URL
        url = "/api/send-sms/"
        
        # Mock input data
        data = {
            "message": "Hello, this is a test message!",
            "recipients": ["+254745544814"],
        }
        
        # Send a POST request
        response = self.client.post(url, data, format='json')
        
        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("success", response.data)

    def test_send_sms_missing_fields(self):
        # Define the endpoint URL
        url = "/api/send-sms/"
        
        # Missing recipients
        data = {
            "message": "Hello, this is a test message!"
        }
        
        # Send a POST request
        response = self.client.post(url, data, format='json')
        
        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
