from app.models import Quote
from app.serializers import QuoteSerializer
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse


class RandomViewTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:

        call_command("fill_db", limit=1000)
        cls.username = "test_user"
        cls.user_password = "test_password"
        User.objects.create_user(
            username=cls.username, password=cls.user_password
        )
        return super().setUpClass()

    def setUp(self) -> None:
        self.assertTrue(
            self.client.login(
                username=self.username, password=self.user_password
            )
        )
        return super().setUp()

    def test_get_random_quote(self):
        response = self.client.get(reverse("random-quote"))
        self.assertEqual(response.status_code, 200)

        response_quote = response.json()
        quote = Quote.objects.filter(id=response_quote["id"])
        self.assertTrue(quote.exists())

        serializer = QuoteSerializer(quote.get())
        self.assertEqual(response_quote, serializer.data)

    def test_get_random_quote_with_category_filter(self):
        for _ in range(100):
            response = self.client.get(
                reverse("random-quote"), {"category": "age"}
            )
            self.assertEqual(response.status_code, 200)
            response_quote = response.json()

            self.assertEqual(response_quote["category"], "age")

    def test_get_random_quote_with_author_filter(self):
        for _ in range(100):
            response = self.client.get(
                reverse("random-quote"),
                {"author": "Aung San Suu Kyi"},
            )
            self.assertEqual(response.status_code, 200)
            response_quote = response.json()

            self.assertEqual(
                response_quote["author"], "Aung San Suu Kyi"
            )

    def test_get_empty_quote(self):
        response = self.client.get(
            reverse("random-quote"), {"author": "Nikita Zigman"}
        )
        self.assertEqual(response.status_code, 404)
