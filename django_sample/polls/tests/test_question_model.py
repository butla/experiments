import datetime

from django.utils import timezone

from polls.models import Question


def test_was_published_recently_true_for_less_than_one_day():
    recent_date = timezone.now() - datetime.timedelta(hours=5)
    question = Question(pub_date=recent_date)
    assert question.was_published_recently()


def test_was_published_recently_false_for_less_than_one_day():
    old_date = timezone.now() - datetime.timedelta(days=2)
    question = Question(pub_date=old_date)
    assert not question.was_published_recently()


def test_was_published_recently_false_for_future_date():
    future_date = timezone.now() + datetime.timedelta(days=30)
    future_question = Question(pub_date=future_date)
    assert not future_question.was_published_recently()


# TODO this will be used below
# TODO enable database access everywhere. Is db_fixture_maker needed?
def create_question(text: str, days_old: int):
    creation_date = timezone.now() + datetime.timedelta(days=days_old)
    return Question.objects.create(text=text, pub_date=creation_date)


# TODO
#class Questionview
