from rest_framework.test import APITestCase
from rest_framework import status


class SignUpViewTest(APITestCase):
    URL = '/api/account/sign_up/'

    def test_correct_data(self):
        response = self.client.post(
            self.URL,
            {
                'username': 'username',
                'password': 'password',
                'password2': 'password',
                'role': 'developer'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
