# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import F
topics = ['SAT vocabulary', 'GRE vocabulary', 'sport', 'Law', 'Food', 'Computers', 'Music',
          'Science', 'Religion', 'Tools', 'Movies', 'Animals', 'Clothing', 'Holidays']
TOPICS_CHOICES = [(x, x) for x in topics]
# TOPICS_CHOICES = [('General', 'General'), ('Sport', 'Sport')]
DIFFICULTY_LEVELS = [(1, 1), (2, 2), (3, 3), (4, 4)]
GAME_MODES = [('General', 'General')]


class Question(models.Model):
    """
    this class represents a question object
    """
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    topic = models.CharField(choices=TOPICS_CHOICES, default='General', max_length=100)
    word = models.TextField()
    question = models.TextField()
    extensions = models.TextField(default='null')
    difficulty = models.IntegerField(choices=DIFFICULTY_LEVELS, default=1)
    # score = models.IntegerField()
    hint = models.TextField(default='null')
    game_mode = models.CharField(choices=GAME_MODES, default='General', max_length=100)
    owner = models.ForeignKey('auth.User', related_name='app_server', on_delete=models.CASCADE,
                              default=1)

    def __str__(self):
        return 'Question ID: ' + str(self.id) + ' word is :' + self.word + ' The definition is: ' + \
               self.question

    class Meta:
        ordering = ('created',)


class Score(models.Model):
    """
    this class represents a score object
    """
    user_id = models.TextField(primary_key=True)
    user_name = models.TextField(default='no_name')
    score = models.IntegerField(default=0)

    def __str__(self):
        return 'User id ' + str(self.user_id) +' User name is: ' + str(self.user_name) + ' The score is : ' + str(self.score)

    @staticmethod
    def add_points(user_id, points):
        Score.objects.filter(user_id=user_id).update(score=F('score') + points)

    class Meta:
        ordering = ('user_id',)


class Answer(models.Model):
    """
    this class represents an answer object
    """
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    answer = models.TextField()
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    positive_count = models.IntegerField(default=0)
    negative_count = models.IntegerField(default=0)
    user_id = models.ForeignKey(Score, on_delete=models.SET_NULL, null=True)
    # score = models.IntegerField()

    def __str__(self):
        return 'Answer id ' + str(self.id) + ' to question with id : ' + str(self.question_id) + ' is :\n' + self.answer

    class Meta:
        ordering = ('created',)