from http import HTTPStatus

from django.conf import settings
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from users.forms import UserCreateForm
from users.models import EmailVerification, User


class TestRegistrationPage(TestCase):

    def setUp(self):
        self.data = {
            'username': 'username',
            'password1': 'worstshoppassword',
            'password2': 'worstshoppassword',
            'email': 'email@gmail.com'
        }

    def test_registration_form(self):
        form = UserCreateForm(self.data)
        self.assertTrue(form.is_valid())

    def test_registration_user_post_success(self):
        url = reverse('users:registration')
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertEqual(User.objects.count(), 1)
        self.assertFalse(User.objects.first().is_active)
        # self.assertEqual(EmailVerification.objects.count(), 1)

    def test_registration_user_post_error(self):
        self.user = User.objects.create_user(
            username='username',
            email='email@mail.com',
            password='testpasswordtest22'
        )
        url = reverse('users:registration')
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует')

    def test_verification_email_sent(self):
        form = UserCreateForm(self.data)
        form.save()
        verification = EmailVerification.objects.first()
        verification.send_verification_code()
        self.assertEqual(mail.outbox[0].body,
                         f'Для завершения регистрации, перейдите по ссылке:'
                         f' {settings.DOMAIN_NAME}/user/verify/{verification.code}')

    def test_verification_user(self):
        form = UserCreateForm(self.data)
        form.save()
        verification = EmailVerification.objects.first()
        url = reverse('users:email_verification', kwargs={'code': verification.code})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.first().is_active)


class TestLoginPage(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='username',
            email='email@mail.com',
            password='testpasswordtest22'
        )

    def test_login_user_success(self):
        response = self.client.post(reverse('users:login'), {'username': 'username', 'password': 'testpasswordtest22'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('catalog:category_list'))
