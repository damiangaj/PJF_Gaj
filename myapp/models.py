import random

from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    name = models.CharField(max_length=120,blank=True,null=True)
    topic = models.CharField(max_length=120,blank=True,null=True)
    number_of_question = models.IntegerField(default=0)
    time = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes_user2', blank=True, null=True)


    def __str__(self):
        return f"{self.name}-{self.pk}-{self.time}"

    def get_questions(self):
        question = list(self.question_set.all())
        random.shuffle(question)
        return question


class Question(models.Model):
    text = models.CharField(max_length=300,blank=True,null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text}"

    def get_answer(self):
        return self.answer_set.all()

class Answer(models.Model):
    text = models.CharField(max_length=300,blank=True,null=True)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return f"{self.text}"


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2', blank=True, null=True)
    score = models.FloatField()
    def __str__(self):
        return str(self.pk)



