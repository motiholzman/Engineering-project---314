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
    created = models.DateTimeField(auto_now_add=True)
    topic = models.CharField(choices=TOPICS_CHOICES, default='General', max_length=100)
    question = models.TextField()
    extensions = models.TextField()
    difficulty = models.IntegerField(choices=DIFFICULTY_LEVELS, default = 1)
    hint = models.TextField()
    game_mode = models.CharField(choices=GAME_MODES, default='General', max_length=100)

    def __str__(self):
        return 'Question ID: ' + str(self.id) + ' The Question is: ' + self.question

    class Meta:
        ordering = ('created',)


