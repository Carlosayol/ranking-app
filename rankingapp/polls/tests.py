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
        """"If no question exist, an appropiate message is displayed"""

        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question(self):
        """"Question created in the future arent displayed on the index page"""

        create_question("test 1", 10)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """"Question created in the past are displayed on the index page"""

        question = create_question("test 1", -10)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [question]
        )
