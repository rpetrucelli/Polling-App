import datetime
from django.contrib import admin
from django.db import models
from django.utils import timezone

#define a many to one relationship from choices to questions
class Question(models.Model):
    """
    Here we define the question model of our Application. I have kept it simple with just text and publish date,
    but adding fields is as simple as typing in additional attributes
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    @admin.display(                     #this block customizes the question display in our admin site
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )

    def was_published_recently(self):   #method to display if the question was published in the last day
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    """
    Here I implement the choice model, each of which belongs to one and only one question
    the foreign key field is used to assign the choice to a question
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
