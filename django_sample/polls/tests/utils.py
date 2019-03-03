import datetime

from django.utils import timezone

from polls.models import Question


def create_question(text: str, days_old: int = 0):
    creation_date = timezone.now() - datetime.timedelta(days=days_old)
    return Question.objects.create(text=text, pub_date=creation_date)
