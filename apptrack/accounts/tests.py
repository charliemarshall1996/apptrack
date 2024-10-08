import datetime

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Profile

# Create your tests here.


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@user.com", password="foo")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False)


class TestProfileModel(TestCase):

    def test_profile_model(self):
        user = get_user_model().objects.create_user(
            email="JpjHt@example.com",
            password="testpass123"
        )
        first_name = "Test"
        second_name = "User"
        gender = "M"
        birth_date = datetime.date(2000, 1, 1)
        profile = Profile.objects.create(user=user,
                                         gender=gender,
                                         birth_date=birth_date)
        profile.save()
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.gender, gender)
        self.assertEqual(profile.birth_date, birth_date)
