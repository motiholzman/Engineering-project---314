# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseServerError
from django.core import serializers

from .models import Question, Answer
from .serializers import QuestionSerializer, UserSerializer, AnswerSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics, permissions, renderers
import json

"""
this function defines the root API of the project 
"""
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('Users-list', request=request, format=format),
        'Questions': reverse('Questions-list', request=request, format=format)
    })


#TODO complete this code
class AddAnswerToDB(generics.GenericAPIView):
    queryset = Answer.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4
        try:
            answer = json_data['answer']
            question_id = json_data['id']
            Answer.objects.create(answer=answer, question_id=question_id)
            trending_answers = Answer.object.filter(question_id=question_id).order_by('positive_count')
            x = min(5, trending_answers.count())
            trending_answers = trending_answers[0:x]
            HttpResponse("Got json data")
            # question_to_send_back = Question.objects.filter(topic=topicJSN).order_by('?').first()
            response_json = serializers.serialize('json', [trending_answers])
            return HttpResponse(response_json, content_type='application/json')
        except KeyError:
            HttpResponseServerError("Malformed data!")
            return HttpResponse("Error parsing JSON")




class GetQuestionsByTopic(generics.GenericAPIView):
    queryset = Question.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        url = request.build_absolute_uri()
        topic = url.rsplit('/', 1)[-1]
        print(topic)
        HttpResponse("Got json data")#TODO - is this needed?
        question_to_send_back = Question.objects.filter(topic=topic).order_by('?').first()
        qs_json = serializers.serialize('json', [question_to_send_back])
        return HttpResponse(qs_json, content_type='application/json')


class AnswersList(generics.ListCreateAPIView):
    """
    this view returns the answers

    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class QuestionsList(generics.ListCreateAPIView):
    """
    this view returns the questions

    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class QuestionsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


"""
this view returns the users list.
"""
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


"""
this view returns the users list.
"""
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
