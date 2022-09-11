from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .apps import PollsConfig
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        return (
            Question.objects
            .filter(pub_date__lte=timezone.now())
            .order_by('-pub_date')[:5]
        )


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # TODO why does this not work?
    # app: PollsConfig = request.current_app
    # app.app_object_bla += ' | one more vote cast'
    # print("========== XXXXX srakator", app.app_object_bla, '===========================')

    try:
        chosen_answer_id = request.POST['choice']
        selected_choice = question.choice_set.get(pk=chosen_answer_id)
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        redirect_url = reverse('polls:results', args=(question.id,))
        return HttpResponseRedirect(redirect_url)
