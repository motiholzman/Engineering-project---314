from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Question, Answer


class QuestionSerializer(serializers.ModelSerializer):
    """
    serializer class for Question object
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Question
        fields = ('id', 'created', 'topic', 'question',
                  'extensions', 'difficulty', 'hint', 'game_mode', 'owner')


class AnswerSerializer(serializers.ModelSerializer):
    """
    serializer class for Answer object
    """
    # owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Answer
        fields = ('id', 'created', 'answer', 'question_id')#, 'owner'



class UserSerializer(serializers.ModelSerializer):
    """
    serializer class for User object
    """
    #questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username')