from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class HouseholdModelTests(TestCase):
    def test_creating_a_household_generates_a_unique_invite_code(self):
        from src.households.models import Household

        first = Household.objects.create(name="The Oaks")
        second = Household.objects.create(name="The Pines")

        self.assertTrue(first.invite_code)
        self.assertTrue(second.invite_code)
        self.assertNotEqual(first.invite_code, second.invite_code)

    def test_a_user_belongs_to_at_most_one_household(self):
        from django.db import IntegrityError

        from src.households.models import Household, Membership

        user = User.objects.create_user(username="member", password="unused")
        first_home = Household.objects.create(name="First")
        second_home = Household.objects.create(name="Second")
        Membership.objects.create(user=user, household=first_home)

        with self.assertRaises(IntegrityError):
            Membership.objects.create(user=user, household=second_home)


class LoginRequiredHouseholdTests(TestCase):
    def test_anonymous_visitor_cannot_open_create_and_is_sent_to_login(self):
        response = self.client.get(reverse("household_create"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["Location"],
            f"{reverse('login')}?next={reverse('household_create')}",
        )

    def test_anonymous_visitor_cannot_open_household_home_and_is_sent_to_login(self):
        response = self.client.get(reverse("household_home"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["Location"],
            f"{reverse('login')}?next={reverse('household_home')}",
        )


class CreateHouseholdTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alex",
            password="unused",
            first_name="Alex",
        )

    def test_logged_in_user_with_no_household_sees_create_and_not_a_member_list(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("home"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="name"')
        self.assertNotContains(response, "Members")
        self.assertNotContains(response, "You are signed in.")

    def test_creating_a_household_adds_member_generates_code_and_opens_home(self):
        from src.households.models import Household, Membership

        self.client.force_login(self.user)

        response = self.client.post(
            reverse("household_create"),
            {"name": "The Oaks"},
        )

        self.assertRedirects(response, reverse("household_home"))
        self.assertEqual(Household.objects.count(), 1)
        household = Household.objects.get()
        self.assertEqual(household.name, "The Oaks")
        self.assertTrue(household.invite_code)
        self.assertTrue(
            Membership.objects.filter(user=self.user, household=household).exists()
        )

        home = self.client.get(reverse("household_home"))
        self.assertContains(home, "The Oaks")
        self.assertContains(home, household.invite_code)
        self.assertContains(home, "Alex")
        self.assertContains(home, "Members")
        self.assertNotContains(home, "You are signed in.")
        self.assertNotContains(home, "Switch person")

    def test_empty_name_does_not_create_a_household_and_shows_an_error(self):
        from src.households.models import Household, Membership

        self.client.force_login(self.user)

        response = self.client.post(reverse("household_create"), {"name": ""})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Household.objects.count(), 0)
        self.assertEqual(Membership.objects.count(), 0)
        self.assertContains(response, "This field is required.")
        self.assertFalse(Membership.objects.filter(user=self.user).exists())

    def test_user_who_already_belongs_sees_household_home_not_create(self):
        from src.households.models import Household, Membership

        household = Household.objects.create(name="The Oaks")
        Membership.objects.create(user=self.user, household=household)
        self.client.force_login(self.user)

        home_response = self.client.get(reverse("home"), follow=True)
        self.assertContains(home_response, "The Oaks")
        self.assertContains(home_response, household.invite_code)
        self.assertContains(home_response, "Members")
        self.assertNotContains(home_response, "Create household")

        create_response = self.client.get(reverse("household_create"))
        self.assertRedirects(create_response, reverse("household_home"))

    def test_user_who_already_belongs_cannot_create_a_second_household(self):
        from src.households.models import Household, Membership

        original = Household.objects.create(name="The Oaks")
        Membership.objects.create(user=self.user, household=original)
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("household_create"),
            {"name": "Another Place"},
        )

        self.assertRedirects(response, reverse("household_home"))
        self.assertEqual(Household.objects.count(), 1)
        self.assertEqual(Household.objects.get().name, "The Oaks")
        self.assertEqual(self.user.membership.household_id, original.id)
