from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User

def thereIsUser(email: str, password: str) -> User:
    return User.objects.create_user(email=email, password=password)

class LoginViewTests(APITestCase):
    def test_login(self):
        email, password = 'robson@firma.pl', '12345678'
        thereIsUser(email, password)

        res = self.client.post('/api/auth/login/', {'email': email, 'password': password})

        self.assertEqual(res.status_code, status.HTTP_202_ACCEPTED)
        self.assertIsNotNone(self.client.cookies.get('sessionid'))

class LogoutViewTests(APITestCase):
    def test_logout(self):
        email, password = 'robson@firma.pl', '12345678'
        thereIsUser(email, password)
        self.client.login(email=email, password=password)

        res = self.client.post('/api/auth/logout/')

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

class RegisterViewTests(APITestCase):
    def test_register(self):
        email, password = 'robson@firma.pl', '12345678'
        res = self.client.post('/api/auth/register/', {'email': email, 'password': password})

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email=email)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, email)