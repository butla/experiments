import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now())

    def was_published_recently(self):
        now = timezone.now()
        if now - self.pub_date < datetime.timedelta(days=1) and self.pub_date < now:
            return True
        return False


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
