# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

TOPICS_CHOICES = [('General', 'General'), ('Sport', 'Sport')]
DIFFICULTY_LEVELS = [(1, 1), (2, 2), (3, 3), (4, 4)]
GAME_MODES = [('General', 'General')]


"""
    this class represents a question object 
"""


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    topic = models.CharField(choices=TOPICS_CHOICES, default='General', max_length=100)
    question = models.TextField()
    extensions = models.TextField(default = 'null')
    difficulty = models.IntegerField(choices=DIFFICULTY_LEVELS, default = 1)
    hint = models.TextField(default = 'null')
    game_mode = models.CharField(choices=GAME_MODES, default='General', max_length=100)
    owner = models.ForeignKey('auth.User', related_name='app_server', on_delete=models.CASCADE,
                              default=1)

    def __str__(self):
        return 'Question ID: ' + str(self.id) + '\nThe Question is: ' + self.question

    class Meta:
        ordering = ('created',)


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    answer = models.TextField()
    question_id = models.IntegerField()
    positive_count = models.IntegerField(default=0)
    negative_count = models.IntegerField(default=0)
    # owner = models.ForeignKey('auth.User', related_name='app_server', on_delete=models.CASCADE,
    #                           default=1)

    def __str__(self):
        return 'Answer to question with id : ' + str(self.question_id) + ' is :\n' + self.answer

    class Meta:
        ordering = ('created',)