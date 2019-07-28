from .models import *
from .views import *
from nltk.corpus import wordnet as wn
from django.http import HttpResponse, HttpResponseServerError
import csv

# topics for the database. you can change al except the first two.
topics = ['SAT vocabulary', 'GRE vocabulary', 'sport', 'Law', 'Food', 'Computers', 'Music',
          'Science', 'Religion', 'Tools', 'Movies', 'Animals', 'Clothing', 'Holidays']

# the files that contain the GRE and SAT definitions and words
paths_to_files =\
    ['/cs/engproj/314/proj2/app_backend/list of words for gre and gmat/sat_words.csv',
     '/cs/engproj/314/proj2/app_backend/list of words for gre and gmat/gre_words.csv']


def init_database(request):
    """
    this function initializes the the database
    :param request: a required parameter in Django
    :return: http response
    """
    Question.objects.all().delete()
    for topic in topics:
        print("\n ************************ "
              "******************************************************************************************\n")
        print(topic)
        if topic == 'SAT vocabulary':
            insert_to_db_from_list(csv_2_words_and_defs(paths_to_files[0]), topic)
        elif topic == 'GRE vocabulary':
            insert_to_db_from_list(csv_2_words_and_defs(paths_to_files[1]), topic)
        elif topic == 'Movies':
            #  to avoid nonsense
            helper(topic, topic, 2)
            print(x)
        else:
            helper(topic, topic, 3)
            print(x)
    return HttpResponse([], content_type='application/json')


x = 0


def helper(word, topic, n):
    """
    modifies the database so that the questions are divided into categories
    :param word: current word we iterate over in the topic
    :param topic: current topic
    :param n: recursion depth
    :return: nothing, modifies the database
    """
    if n == 0:
        return
    topics_synsets_list = wn.synsets(word)
    if topics_synsets_list:
        relevant_sysnet = topics_synsets_list[0].lemma_names()
        # here we add the first synonym's definition
        if not Question.objects.filter(word=word):
            Question.objects.create(topic=topic, question=topics_synsets_list[0].definition(), word=word)
        global x
        x += 1
        for lemma in relevant_sysnet:
            hypo_synset = wn.synsets(lemma)[0].hyponyms()
            for hypo in hypo_synset:
                helper(hypo.lemma_names()[0], topic, n-1)


def file_to_csv(file_path, csv_path):
    """
    converts file of definitions into csv - feel free to modify this to your use :)
    :param file_path: the file we want to convert
    :param csv_path: the csv file's path
    :return: nothing.
    """
    word = []
    definition = []
    with open(file_path) as fp:
        line = fp.readline()
        while line:
            line = line.split('-')
            word.append(line[0][:-1])
            definition.append(line[1][1:].split('\n')[0])
            line = fp.readline()
    with open(csv_path, mode='w') as csv_path:
        csv_writer = csv.writer(csv_path, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['number', 'word', 'definition'])
        cnt = 1
        for (x, y) in zip(word, definition):
            csv_writer.writerow([str(cnt), x, y])
            cnt += 1


def csv_2_words_and_defs(path):
    """
    converts csv into words and definitions lists
    :param path: the path of the csv file
    :return: two lists: words and definitions, containing the words nad definitions in the file
    """
    with open(path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        words = []
        definition = []
        next(readCSV)
        for row in readCSV:
            words.append(row[1])
            definition.append(row[2])
        return words, definition


def insert_to_db_from_list(set, topic):
    """
    this function inserts questions to the database when they come in as tuple of two lists
    :param set: tuple of words and definition
    :param topic: the topic of the words in the set
    :return: nothing. it modifies the Question table
    """
    for (word, defe) in zip(set[0], set[1]):
        syns = wn.synsets(word)
        definition = defe
        if syns:
            definition = syns[0].definition()
        Question.objects.create(topic=topic, question=definition, word=word)
