# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv, io
import re
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

from itertools import chain

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseServerError
from django.core import serializers

from .models import Question, Answer, Score
from .serializers import QuestionSerializer, UserSerializer, AnswerSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics, permissions, renderers
import json
from django.db.models import F, Func
from django.db.models import Q
from .tokenIDHelper import *
from wordfreq import top_n_list
from .sentencesVerif import calc_distance


freq_list = top_n_list('en', 10000, wordlist='best')
THRESHOLD = 3.6  # threshold for the GateKeeper classifier - important!


@api_view(['GET'])
def api_root(request, format=None):
    """
    this function defines the root API of the project
    """
    return Response({
        'users': reverse('Users-list', request=request, format=format),
        'Questions': reverse('Questions-list', request=request, format=format)
    })


class EstablishSession(generics.GenericAPIView):
    """
    Authentication Unit:
    this class is in charge of the session establishing with the frontend.
    all is done with the post function
    """
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def post(self, request, *args, **kwargs):
        """
        the post request receives the data in Json format. the data should contain the token id of the user.
        the function will then authenticate the session with Google API.
        :return the function returns in the Json object the current score of the user
        """
        json_data = json.loads(request.body)  # request.raw_post_data w/ Django < 1.4
        try:
            token = json_data['token']
            user_id, user_name = tokenIDHlpeer.tokenParser(token)
            HttpResponse("Got json data")
            if not Score.objects.filter(user_id=user_id):
                Score.objects.create(user_id=user_id, user_name=user_name, score=0)
            score_obj = Score.objects.filter(user_id=user_id).first()
            response_json = serializers.serialize('json', [score_obj])
            request.session['user_id'] = user_id
            return HttpResponse(response_json, content_type='application/json')
        except KeyError:
            HttpResponseServerError("Malformed data!")
            return HttpResponse("Error parsing JSON")


class AddAnswerToDB(generics.GenericAPIView):
    """
    this class is the interface for adding answers to the database
    """
    queryset = Answer.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    @staticmethod
    def calculateScoreForString(sentence):
        """
        this functionality is not in use in the current version of the game.
        the function receives a sentence and returns a real number indicating
        how complex the sentence is. the idea is to give high score to words that have
        low usage frequency in the English language
        :param sentence: the sentence to score
        :return: a real number indicating how complex the sentence is
        """
        words = re.split('\W+', sentence)
        sum = 0
        for word in words:
            if word in freq_list:
                sum += freq_list.index(word)
                continue
            sum += 10000
        return sum

    @staticmethod
    def calculateWMD(s1, s2):
        """
        the function receives two sentences and returns the WMD distance between them.
        (not exactly the WMD, but the modification we made to the algorithm)
        :param s1: first sentence
        :param s2: second sentence
        :return: real number indicating the logical distance between the sentences.
        the higher the number, the further apart the sentences
        """
        WMD = calc_distance(s1, s2)
        print(WMD)
        return WMD

    def post(self, request, *args, **kwargs):
        """
        this POST request function receives in Json format an answer to a question from the front-end,
        and adds it to the Answer table. the function will also increase the users's current score by a fixed
        amount. The function will NOT add the answer to the DB if the answer is spam with respect to the
        question sentence - this is done using WMD based algorithm
        :return: top trending answers to the same question (for front-end purposes)
        """
        json_data = json.loads(request.body)  # request.raw_post_data w/ Django < 1.4
        try:
            answer = json_data['answer']
            grade = self.calculateScoreForString(answer)
            question_id = json_data['id']
            cur_question = Question.objects.filter(id=question_id).first().question
            trending_answers = Answer.objects.filter(question_id=question_id).order_by('positive_count')
            score_obj = Score.objects.filter(user_id=request.session['user_id']).first()
            # GateKeeper classifier
            if self.calculateWMD(answer, cur_question) <= THRESHOLD:
                print('good try')
                Answer.objects.create(answer=answer, question_id=Question(id=question_id),
                                      user_id=score_obj)
            # GateKeeper classifier - done
            x = min(5, trending_answers.count())
            trending_answers = trending_answers[0:x]
            HttpResponse("Got json data")
            response_json = serializers.serialize('json', list(trending_answers))
            # adding score to the user
            Score.add_points(request.session['user_id'], 10)
            return HttpResponse(response_json, content_type='application/json')
        except KeyError:
            HttpResponseServerError("Malformed data!")
            return HttpResponse("Error parsing JSON")


class UpdateAnswerCount(generics.GenericAPIView):
    """
    this class is a get interface for grading user's answers
    """
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        """
        this GET request function will update the positive or negative count score
        for a certain answer, according to the last char of the URL used. (+ or -).
        the function will also add fixed amount of points to the user
        :return: the answer object of the rated answer (for front-end purposes)
        """
        url = request.build_absolute_uri()
        url_data = url.rsplit('/', 2)
        ans_id = url_data[-2]
        sign = url_data[-1]
        if sign == '+':
            Answer.objects.filter(id=ans_id).update(positive_count=F('positive_count') + 1)
        else:
            Answer.objects.filter(id=ans_id).update(negative_count=F('negative_count') + 1)
        Score.add_points(request.session['user_id'], 1)
        ans_to_return = Answer.objects.filter(id=ans_id).first()
        as_json = serializers.serialize('json', [ans_to_return])
        return HttpResponse(as_json, content_type='application/json')


class GetReviewByTopic(generics.GenericAPIView):
    """
    this class if the interface for getting an answer by topic, for review in the review path of the game.
    """
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        """
        this GET request function receives the requested topic of the user from the last part
        of the URL and returns an answer from that category.
        :return: 5 answers in the requested topic
        """
        url = request.build_absolute_uri()
        topic = url.rsplit('/', 1)[-1].replace('%20', ' ')
        if topic == 'GRE' or topic == 'SAT':
            topic = topic + ' vocabulary'
        answers_per_topic = Answer.objects.filter(question_id__topic=topic)\
            .annotate(sum_of=F('positive_count') + F('negative_count'),
                                  diff_of=Func(F('positive_count') - F('negative_count'),
                                               function='ABS')).order_by('?')
        res = {}
        n_plus_p_trh = 20
        n_minus_p_trh = 5
        while not res:
            res = answers_per_topic.filter(Q(sum_of__lt=n_plus_p_trh) | Q(diff_of__lt=n_minus_p_trh))
            n_minus_p_trh *= 2
            n_plus_p_trh *= 2
        q_to_ret = res.first()
        selected_q_id = q_to_ret.question_id.id
        a_to_ret = res.filter(question_id__id=selected_q_id)
        q_to_ret = Question.objects.filter(id=selected_q_id).first()
        x = min(5, a_to_ret.count())
        a_to_ret = a_to_ret[0:x]
        HttpResponse("Got json data")
        both = list(chain([q_to_ret], a_to_ret))
        ret = serializers.serialize('json', both)
        return HttpResponse(ret, content_type='application/json')


class GetQuestionsByTopic(generics.GenericAPIView):
    """
    this class is the interface for getting question in a given topic
    """
    queryset = Question.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        """
        this GET request function gets a topic from the front-end via the last
        part of the URL, and returns a question from that topic
        :return:a question from the requested topic. in JSON format
        """
        url = request.build_absolute_uri()
        topic = url.rsplit('/', 1)[-1].replace('%20', ' ')
        if topic == 'GRE' or topic == 'SAT':
            topic = topic + ' vocabulary'
        print(topic)
        HttpResponse("Got json data")
        # note that the user might get back questions that he had already answered
        question_to_send_back = Question.objects.filter(topic=topic).order_by('?').first()
        qs_json = serializers.serialize('json', [question_to_send_back])
        return HttpResponse(qs_json, content_type='application/json')


class GetScore(generics.GenericAPIView):
    """
    this class is the interface for getting the current score for a user
    """
    queryset = Question.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        """
        this GET request function returns the current score of the user (identified with session id)
        :return: score object of the user
        """
        score_obj = Score.objects.filter(user_id=request.session['user_id']).first()
        response_json = serializers.serialize('json', [score_obj])
        return HttpResponse(response_json, content_type='application/json')


class GetTopScore(generics.GenericAPIView):
    """
    this class is the interface for getting the top scored users
    """
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        """
        this GET request function returns the current top 10 scored users in the game.
        :return: JSON containing the 10 highest scored users and their scores
        """
        res = Score.objects.all().order_by('-score')
        x = min(10, res.count())
        res = res[0:x]
        response_json = serializers.serialize('json', res)
        return HttpResponse(response_json, content_type='application/json')


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
    """
    this view returns the questions
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class UserList(generics.ListAPIView):
    """
    this view returns the users list.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    this view returns the users list.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


@permission_required('admin.can_add_log_entry')
def question_upload(request):
    """
    this function allows to import data from csv file in a certain format.
    :param request: must-have parameter in Django
    :return: nothing
    """
    template = "question_upload.html"
    prompt = {
        'order': 'order of CSV should be topic, question'
    }
    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file!')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)  # because of the header
    reader = csv.reader(io_string)
    # this will not work in the current format of the DB
    for row in reader:
        _, created = Question.objects.update_or_create(
            topic=row[0],
            question=row[1].rsplit('-', 1)[-2]
        )
    context = {}
    return render(request, template, context)
