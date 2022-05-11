from django.urls import reverse
import pytest

from .utils import create_question


@pytest.mark.django_db
def test_no_questions_gives_a_message_in_the_index(client):
    response = client.get(reverse('polls:index'))

    assert response.status_code == 200
    assert b"No polls are available." in response.content


@pytest.mark.django_db
def test_past_questions_get_displayed(client):
    question_1 = create_question('Do you even lift?', 3)
    question_2 = create_question('What is love?', 12)

    response = client.get(reverse('polls:index'))

    assert response.status_code == 200
    # This actually doesn't check if anything is displayed, it relies on the template
    # to be correct, which is uncomfortable for me, so I'll add a better assertion next.
    # This is just so that I remember about that you introspect contexts in Django.
    assert list(response.context['latest_questions']) == [question_1, question_2]

    # This is something that doesn't depend on the template necessary being correct, but at the
    # same it it doesn't assert anything about the layout of the page (template's responsibility)
    # as well.
    assert question_1.text.encode() in response.content
    assert question_2.text.encode() in response.content


@pytest.mark.django_db
def test_future_questions_dont_get_displayed(client):
    visible_question_text = 'see me'
    invisible_question_text = "you don't know me"
    create_question(visible_question_text)
    create_question(invisible_question_text, days_old=-4)

    response = client.get(reverse('polls:index'))

    assert visible_question_text.encode() in response.content
    assert invisible_question_text.encode() not in response.content
