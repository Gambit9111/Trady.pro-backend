# test users/views.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status
from .serializers import UserSerializer


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        print('test_create_valid_user_success')
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'user1@mail.com',
            'password': 'testpass123',
        }
        res = self.client.post(reverse('authentication:register'), payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        print('test_user_exists')
        """Test creating a user that already exists fails"""
        payload = {
            'email': 'user1@mail.com',
            'password': 'testpass123',
        }
        get_user_model().objects.create_user(**payload)

        res = self.client.post(reverse('authentication:register'), payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_password_too_short(self):
        print('test_password_too_short')
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'user1@mail.com',
            'password': 'pw',
        }
        res = self.client.post(reverse('authentication:register'), payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
        
    def test_create_token_for_user(self):
        print('test_create_token_for_user')
        """Test that a token is created for the user"""
        payload = {
            'email': 'user1@mail.com',
            'password': 'testpass123',
        }
        get_user_model().objects.create_user(**payload)
        res = self.client.post(reverse('authentication:login'), payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        print('test_create_token_invalid_credentials')
        """Test that token is not created if invalid credentials are given"""
        get_user_model().objects.create_user(email='user1@mail.com', password='testpass123')
        payload = {
            'email': 'user1@mail.com',
            'password': 'wrong',
        }
        res = self.client.post(reverse('authentication:login'), payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_token_no_user(self):
        print('test_create_token_no_user')
        """Test that token is not created if user doesn't exist"""
        payload = {
            'email': 'user1@mail.com',
            'password': 'testpass123',
        }
        res = self.client.post(reverse('authentication:login'), payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

# class PrivateUserTests(APITestCase):
#     """Test API requests that require authentication"""

#     def setUp(self):
#         self.admin = get_user_model().objects.create_superuser('admin@mail.com', 'testpass123')
#         # get the bearer token
#         url = reverse('authentication:login')
#         data = {
#             'email': 'admin@mail.com',
#             'password': 'testpass123',
#         }
#         response = self.client.post(url, data, format='json')
#         self.token = response.data['token']
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

#         # create 3 users
#         self.user1 = get_user_model().objects.create_user('user1@mail.com', 'testpass123')
#         self.user2 = get_user_model().objects.create_user('user2@mail.com', 'testpass123')
#         self.user3 = get_user_model().objects.create_user('user3@mail.com', 'testpass123')
    
#     # retrieve user list
#     def test_retrieve_user_list(self):
#         res = self.client.get(reverse('authentication:user-list'))

#         users = get_user_model().objects.all()
#         serializer = UserSerializer(users, many=True)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)
    
#     # # retrieve user list unauthorized
#     # def test_users_list_unauthorized(self):
#     #     """Test that authentication is required for users"""
#     #     client = APIClient()
#     #     res = client.get(reverse('users:user-list'))

#     #     self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



































# class UserTestCase(TestCase):
#     def setUp(self):
#         User = get_user_model()
#         User.objects.create_user(email='testuser1@mail.com', password='Turtuolis123456')
#         User.objects.create_user(email='testuser2@mail.com', password='Turtuolis123456')
#         User.objects.create_user(email='testuser3@mail.com', password='Turtuolis123456')
#         #--
#         User.objects.create_superuser(email='admin@mail.com', password='Admin123456')
    
#     def test_user_list(self):
#         data = {'email': 'admin@mail.com', 'password': 'Admin123456'}
#         response = self.client.post(reverse('users:login'), data)
#         # pass in jwt token
#         self.client.authenticate(HTTP_AUTHORIZATION='JWT ' + response.data['token'])
#         response = self.client.get(reverse('users:users'))
#         self.assertEqual(response.status_code, 200)
#         response = self.client.get(reverse('users:users'))
#         self.assertEqual(response.status_code, 200)

#     def test_user_list_invalid(self):
#         data = {'email': 'testuser1@mail.com', 'password': 'Turtuolis123456'}
#         response = self.client.post(reverse('users:login'), data)
#         self.assertEqual(response.status_code, 200)
#         response = self.client.get(reverse('users:users'))
#         self.assertEqual(response.status_code, 401)

#     def test_user_login(self):
#         data = {'email': 'testuser1@mail.com', 'password': 'Turtuolis123456'}
#         response = self.client.post(reverse('users:login'), data)
#         self.assertEqual(response.status_code, 200)
    
#     def test_user_login_invalid(self):
#         data = {'email': 'testuserinvalid@mail.com', 'password': 'Turtuocw2c2'}
#         response = self.client.post(reverse('users:login'), data)
#         self.assertEqual(response.status_code, 401)

#     # def test_user_logout(self):
#     #     self.client.login(username='testuser', password='12345')
#     #     response = self.client.get(reverse('users:logout'))
#     #     self.assertEqual(response.status_code, 302)

#     def test_user_register(self):
#         data = {'email': 'testuserregister@mail.com', 'password': '12345Turtuolis'}
#         response = self.client.post(reverse('users:register'), data)
#         self.assertEqual(response.status_code, 201)
    
#     def test_user_register_invalid(self):
#         data = {'email': 'testuser1@mail.com', 'password': '12345Turtuolis'}
#         response = self.client.post(reverse('users:register'), data)
#         self.assertEqual(response.status_code, 400)