from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

def thereIsUser(email: str, password: str) -> User:
    return User.objects.create_user(email=email, password=password)

class UserSelfViewTests(APITestCase):
    def test_get_me(self):
        email, password = 'robson@firma.pl', '12345678'

        thereIsUser(email, password)
        self.client.login(email=email, password=password)

        res = self.client.get('/api/users/me/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        self.assertEqual(data['email'], email)

    def test_get_me_unauthenticated(self):
        res = self.client.get('/api/users/me/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    
class UserViewTests(APITestCase):
    def test_get_by_id(self):
        user = thereIsUser('robson@firma.pl', '12345678')
        res = self.client.get(f'/api/users/{user.id}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        self.assertEqual(data['id'], user.id)
        self.assertEqual(data['email'], user.email)

class UserUsernameChangeView(APITestCase):
    def test_proper(self):
        user = thereIsUser('robson@firma.pl', '12345678')
        self.client.force_login(user)

        res = self.client.patch('/api/users/me/username/', {'username': 'marcinek'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()

        self.assertEqual(data['username'], 'marcinek')
    def test_bad_request(self):
        user = thereIsUser('robson@firma.pl', '12345678')
        self.client.force_login(user)

        res = self.client.patch('/api/users/me/username/', {'usrnm': 'marcinek'})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    def test_unauthenticated(self):
        res = self.client.get('/api/users/me/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)