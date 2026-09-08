from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class LoginRequiredTests(TestCase):
    def test_anonymous_user_is_redirected_from_home_to_login(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], f"{reverse('login')}?next=/")


class LogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="member", password="unused")

    def test_logged_in_user_can_log_out_and_cannot_open_home(self):
        self.client.force_login(self.user)
        logout_response = self.client.post(reverse("logout"))
        self.assertEqual(logout_response.status_code, 302)
        self.assertEqual(logout_response["Location"], reverse("login"))

        home_response = self.client.get(reverse("home"))
        self.assertEqual(home_response.status_code, 302)
        self.assertEqual(home_response["Location"], f"{reverse('login')}?next=/")


class LoginPageTests(TestCase):
    def test_login_page_offers_sign_in_with_google(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign in with Google")
