import datetime

from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from .models import Question

# Models
# Views


class QuestionModelTests(TestCase):
    def test_was_created_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose created_at is in the future"""

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="Test", created_at=time)
        self.assertIs(future_question.was_created_recently(), False)

    def test_was_created_recently_with_past_questions(self):
        """was_published_recently returns False for questions whose created_at is in the past"""

        time = timezone.now() - datetime.timedelta(days=30)
        future_question = Question(question_text="Test", created_at=time)
        self.assertIs(future_question.was_created_recently(), False)

    def test_was_created_recently_with_valid_questions(self):
        """was_published_recently returns True for questions whose created_at is in the valid timerange"""

        time = timezone.now() - datetime.timedelta(hours=16)
        future_question = Question(question_text="Test", created_at=time)
        self.assertIs(future_question.was_created_recently(), True)


def create_question(question_text, days):
    """Create a question with the given question_text and days for testing purposes"""

    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, created_at=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """If no question exist, an appropiate message is displayed"""

        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question(self):
        """Question created in the future arent displayed on the index page"""

        create_question("test 1", 10)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """Question created in the past are displayed on the index page"""

        question = create_question("test 1", -10)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_past_and_future_questions(self):
        """Question created in the past are displayed and future questions arent displayed"""

        past_question = create_question("test 1", -10)
        future_question = create_question("test 2", 10)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [past_question]
        )

    def test_two_past_questions(self):
        """Question created in the past are displayed on the index page"""

        past_question = create_question("test 1", -10)
        past_2_question = create_question("test 2", -10)

        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [past_question, past_2_question]
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """The detail view of a question with a created_at in the future returns a 404 error"""
        future_question = create_question("test 2", 10)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """The detail view of a question with a created_at in the past is displayed"""
        past_question = create_question("test 2", -10)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
