import pytest
from django.urls import reverse

from .utils import create_question


@pytest.mark.django_db
def test_question_details_returned_if_its_from_the_past(client):
    question_text = "Do you like bread?"
    past_question = create_question(question_text)

    response = client.get(
        reverse('polls:detail', args=(past_question.id,))
    )

    assert response.status_code == 200
    assert question_text.encode() in response.content


@pytest.mark.django_db
def test_question_details_not_returned_if_its_from_the_future(client):
    past_question = create_question('whatever', days_old=-3)

    response = client.get(
        reverse('polls:detail', args=(past_question.id,))
    )

    assert response.status_code == 404
