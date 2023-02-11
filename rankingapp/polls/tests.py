import datetime

from django.test import TestCase
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
