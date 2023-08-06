import pandas as pd
import numpy as np
import re
import time
import contractions
from tqdm import tqdm
import unicodedata
import tensorflow as tf

def make_train_dataset(lines, conv_lines):
    """
    takes input of lines and conversations, returns a list of questions and answers

    :type lines: string
    :param lines: path were text file of lines is present

    :type conv_lines: string
    :param conv_lines: path were text file of conversations is present
    """
    lines = open(lines, encoding='iso-8859-1', errors='ignore').read().split('\n')
    conv_lines = open(conv_lines, encoding='iso-8859-1', errors='ignore').read().split('\n')
    id2line = {_line.split(' +++$+++ ')[0]:_line.split(' +++$+++ ')[4] for _line in lines if len(_line.split(' +++$+++ '))==5}
    convs = [_line.split(' +++$+++ ')[-1][1:-1].replace("'","").replace(" ","").split(',') for _line in conv_lines[:-1]]
    qa = [[id2line[conv[i]], id2line[conv[i+1]]] for conv in convs for i in range(len(conv)-1)]
    return map(list, zip(*qa))

def map_contraction(text):

    ntext = [contractions.fix(i) for i in text]
    return ntext

def unicodeToAscii(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

def normalizeString(text):

    text = unicodeToAscii(text.lower().strip())
    
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"n't", " not", text)
    text = re.sub(r"n'", "ng", text)
    text = re.sub(r"'bout", "about", text)
    text = re.sub(r"'til", "until", text)
    text = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
    
    # Removing any character that is not a sequence of lower or upper case letters
    # + means one or more
    text = re.sub(r"[^a-zA-Z.!?]+", r" ", text)
    
    # Removing a sequence of whitespace characters
    text = re.sub(r"\s+", r" ", text).strip()
    
    return text

def clean_train_dataset(text):
    """
    takes input list of questiond or answers, returns clean list of strings

    :type text: text
    :param text: list of strings
    """
    text = map_contraction(text)
    text = [normalizeString(text[i]) for i in range(len(text))]
    return text

def trim_train_dataset(q, a, minlen, maxlen):
    """
    trims questions and answers list (strings)

    :type q: list
    :param q: list of questions

    :type a: list
    :param a: list of answers

    :type minlen: int
    :param minlen: minimum length of a question

    :type maxlen: int
    :param maxlen: maximum length of a question
    """
    qn, an = [], []
    for i in tqdm(range(len(q))):
        if (len(q[i].split()) in range(minlen,maxlen+1)) and (len(a[i].split()) in range(minlen,maxlen+1)):
            print
            qn.append(q[i])
            an.append(a[i])
    return qn, an

def make_count_dict(q, a):
    """
    makes a dictionary of words

    :type q: list
    :param q: list of questions

    :type a: list
    :param a: list of answers
    """

    count_dict = {}
    for _text in (q+a):
        for _w in _text.split():
            if _w not in count_dict: count_dict[_w] = 1
            else: count_dict[_w] += 1
    return count_dict

def count_rare_words(cd, mincount):
    """
    counts the number of rare words

    :type cd: dictionary
    :param cd: count dictionary {word:key}

    :type mincount: int
    :param mincount: minimum length of a question
    """

    count = 0
    for k, v in cd.items():
        if v >= mincount: count += 1

    return count

def make_word_dict(cd, mincount, tokens={'<PAD>':0, '<SOS>':1, '<EOS>':2, '<UNK>':3}):
    """
    makes dictionary, returns mapping of word to key and key to word

    :type cd: dictionary
    :param cd: count dictionary {word:key}

    :type mincount: int
    :param mincount: min frequency of word such that it makes it into the word_dict

    :type tokens: dictionary
    :param tokens: default - {'<PAD>':0, '<SOS>':1, '<EOS>':2, '<UNK>':3}
    """

    word_dict, id = tokens, len(tokens)
    for _w, _c in cd.items():
        if _c > mincount:
            word_dict[_w] = id
            id += 1
    id_dict = {id: w for w, id in word_dict.items()}

    return word_dict, id_dict

def add_word_tags(q, a, wd):
    """
    takes input of {word:key} and adds tags to those words

    :type q: list
    :param q: list of questions

    :type a: list
    :param a: list of answers

    :type wd: dict
    :param wd: mapping of word to key
    """

    nq, na = [], []
    for _q in q:
        qw = []
        for _w in _q.split():
            if _w not in wd:
                qw.append('<UNK>')
            else:
                qw.append(_w)
        nq.append(' '.join(qw))
    
    for _a in a:
        aw = []
        for _w in _a.split():
            if _w not in wd:
                aw.append('<UNK>')
            else:
                aw.append(_w)
        aw.append('<EOS>')
        na.append(' '.join(aw))
    
    return nq, na 

def make_line_id(q, a, wd):
    """
    takes input list of questions or answers and word_dict and returns text converted to id

    :type q: list
    :param q: list of questions

    :type a: list
    :param a: list of answers

    :type wd: dict
    :param wd: mapping of word to key
    """

    idq, ida = [], []
    for _q in q:
        qw = []
        for _w in _q.split():
            qw.append(wd[_w])
        idq.append(qw)

    for _a in a:
        aw = []
        for _w in _a.split():
            aw.append(wd[_w])
        ida.append(aw)
    
    return idq, ida

def sort_line_pad(q, a, max_line_length):
    """
    sorts questions and answers based on their length, returns sorted list of question or answer

    :type q: list
    :param q: list of questions

    :type a: list
    :param a: list of answers

    :type max_line_length: int
    :param max_line_length: maximum length of question or answer
    """

    sortq, sorta = [], []
    for length in range(1, max_line_length+1):
        for i in enumerate(q):
            if len(i[1]) == length:
                sortq.append(q[i[0]])
                sorta.append(a[i[0]])
    return sortq, sorta

