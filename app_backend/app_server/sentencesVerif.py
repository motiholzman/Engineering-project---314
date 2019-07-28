
from time import time
from gensim.corpora.dictionary import Dictionary
from numpy import dot, float32 as REAL, memmap as np_memmap, \
    double, array, zeros, vstack, sqrt, newaxis, integer, \
    ndarray, sum as np_sum, prod, argmax
import numpy as np
import os
from gensim.models import Word2Vec, KeyedVectors
from nltk.corpus import stopwords

stop_words = stopwords.words('english')
trained_model = []


def wordMoversDistance(model, document1, document2):
    """
    this function implements the WMD algorithm with some modifications for the game's specific use.
    :param model: trained word embedding model
    :param document1: first sentence
    :param document2: second sentence
    :return: the WMD distance for the sentences
    """
    # If pyemd C extension is available, import it.
    # If pyemd is attempted to be used, but isn't installed, ImportError will be raised in wmdistance
    from pyemd import emd
    # Remove out-of-vocabulary words.
    len_pre_oov1 = len(document1)
    len_pre_oov2 = len(document2)
    document1 = [token for token in document1 if token in model]
    document2 = [token for token in document2 if token in model]
    diff1 = len_pre_oov1 - len(document1)
    diff2 = len_pre_oov2 - len(document2)
    if diff1 > 0 or diff2 > 0:
        print('Remove ' + str(diff1) + ' and ' + str(diff2) + ' OOV words from document 1 and 2 ('
                                                             'respectively).')
        return float('inf')

    if not document1 or not document2:
        print("At least one of the documents had no words that were in the vocabulary. Aborting (returning "
              "inf).")
        return float('inf')

    dictionary = Dictionary(documents=[document1, document2])
    vocab_len = len(dictionary)

    if vocab_len == 1:
        # Both documents are composed by a single unique token
        return 0.0

    # Sets for faster look-up.
    docset1 = set(document1)
    docset2 = set(document2)

    # Compute distance matrix.
    distance_matrix = zeros((vocab_len, vocab_len), dtype=double)
    for i, t1 in dictionary.items():
        if t1 not in docset1:
            continue

        for j, t2 in dictionary.items():
            if t2 not in docset2 or distance_matrix[i, j] != 0.0:
                continue

            # Compute Euclidean distance between word vectors.
            distance_matrix[i, j] = distance_matrix[j, i] = sqrt(np_sum((model[t1] - model[t2]) ** 2))

    if np_sum(distance_matrix) == 0.0:
        # `emd` gets stuck if the distance matrix contains only zeros.
        print('The distance matrix is all zeros. Aborting (returning inf).')
        return float('inf')

    def nbow(document):
        d = zeros(vocab_len, dtype=double)
        nbow = dictionary.doc2bow(document)  # Word frequencies.
        doc_len = len(document)
        for idx, freq in nbow:
            d[idx] = freq / float(doc_len)  # Normalized word frequencies.
        return d

    # Compute nBOW representation of documents.
    d1 = nbow(document1)
    d2 = nbow(document2)

    # Compute WMD.
    return emd(d1, d2, distance_matrix)


def init_word2vec():
    """
    this function initializes the entire word embedding model
    :return: nothing.
    """
    start = time()
    if not os.path.exists('/cs/engproj/314/proj2/trained_model/GoogleNews-vectors-negative300.bin.gz'):
        raise ValueError("SKIP: You need to download the google news model")
    model = KeyedVectors.load_word2vec_format('/cs/engproj/314/proj2/trained_model/GoogleNews-vectors-negative300.bin.gz', binary=True)
    print('Cell took %.2f seconds to run.' % (time() - start))
    # model.init_sims(replace=True)
    global trained_model
    trained_model = model
    return


def calc_distance(sentence_1, sentence_2):
    """
    this function computes the modified WMD distance for two sentences
    :param sentence_1: first sentence
    :param sentence_2: second sentence
    :return: real number representing the WMD distance between the words
    """
    print(sentence_1)
    print(sentence_2)
    # sentence_1 = sentence_1.replace("'", "")
    # sentence_2 = sentence_2.replace("'", "")
    sentence_1 = sentence_1.replace(",", "")
    sentence_2 = sentence_2.replace(",", "")
    sentence_1 = sentence_1.replace(";", "")
    sentence_2 = sentence_2.replace(";", "")
    print(sentence_1)
    print(sentence_2)
    sentence_1 = sentence_1.lower().split()
    sentence_2 = sentence_2.lower().split()
    sentence_1 = [w for w in sentence_1 if w not in stop_words]
    sentence_2 = [w for w in sentence_2 if w not in stop_words]
    return wordMoversDistance(trained_model, sentence_1, sentence_2)
