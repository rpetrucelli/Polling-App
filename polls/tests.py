from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse
import datetime
"""
In this file I have created the basics of an automated test suite in order to test the many functionalities of
the polling application quickly, and from the command line.

It is worth noting that I have used the reverse() method to find the urls for each http response, in order to maintain
the DRY principal 
"""


def create_question(question_text, days):
    """
    this method is used to quickly and easily create a question for testing purposes.
    timedelta is used to create questions in the future or past_question
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        future_question = create_question("", -30)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionResultsViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionChoicesTests(TestCase):       #test class dealing with number of choices for each question

    def test_no_choices(self):
        no_choices = create_question(question_text="I have no choices",days=0)  #create a question
        self.assertIs(no_choices.choice_set.exists(), False)                    #assert that its choic set is empty

    def test_has_choices(self):
        has_choice = create_question(question_text="I have one choice", days=0) #create the question
        c = has_choice.choice_set.create(choice_text="I am a choice!", votes=0) #create a choice for that question
        self.assertIs(has_choice.choice_set.exists(), True)                     #assert that the choice set exists

    def test_has_choices(self):
        has_choice = create_question(question_text="I have choices!", days=0) #create the question
        c = has_choice.choice_set.create(choice_text="I am a choice!", votes=0)
        d = has_choice.choice_set.create(choice_text="and another choice!", votes=0) #create 2 choices
        self.assertIs(has_choice.choice_set.exists(), True)                     #assert that the choice set exists

    def test_choice_size(self):
        has_choice = create_question(question_text="I have several choice", days=0) #create the question
        c = has_choice.choice_set.create(choice_text="I am a choice!", votes=0)
        d = has_choice.choice_set.create(choice_text="and another choice!", votes=0)
        e = has_choice.choice_set.create(choice_text="and a final choice!", votes=0) #create 3 choices
        self.assertEqual(has_choice.choice_set.count(), 3)      #assert that the number of choices is 3
