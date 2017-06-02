#! /usr/bin/env python

from os.path import dirname, join
from bs4 import BeautifulSoup
import bs4
import re

PATH = 'langen.conf'


def read_conf(name):
    dictionary = { }

    with open(join(dirname(__file__), name ) , 'r') as f:
        string = f.read()
        string.replace('\n', '')
        b = BeautifulSoup(string, 'xml')
        for child in b.children:
            if isinstance(child, bs4.element.Tag):
                dictionary[child.name.strip()] = child.get_text().strip()
        return dictionary


def translate(s, dictionary):
    #regular_exp = re.compile('|'.join('&\?{};'.format(key) for key in dictionary.keys()))
    #result = regular_exp.sub(lambda m: dictionary[m.group(0)[2:-1]], s)
    for k, v in dictionary.items():
        s = s.replace('&?{};'.format(k), v)
    return s


def translate_file(path, dictionary):
    with open(path, 'br+') as f:
        content = f.read().decode('utf-8', 'replace')
        content_t = translate(content, dictionary)

        f.seek(0) #rewind
        f.write(content_t.encode('utf-8'))
        f.truncate()


dictionary = read_conf(PATH)
translate_file('template.gch', dictionary)