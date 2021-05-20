# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

import os
import re
import json

import hashlib
import markdown
import yaml


def read_json(path):
    with open(path) as file:
        data = json.load(file)
    return data


def read_markdown(path):
    with open(path, 'r', encoding='utf-8') as file:
        data = file.read()
        output = markdown.markdown(data)
    return output


def read_html(path):
    with open(path) as f:
        newdom = f.read()
        soup = BeautifulSoup(newdom, 'html.parser')
    return soup


def read_xml(path):
    with open(path) as f:
        newdom = f.read()
        soup = BeautifulSoup(newdom, 'lxml-xml')
    return soup


def read_yaml(path):
    with open(path) as f:
        data = yaml.safe_load(f)
    return data


def check_file_extension(path, extension):
    fname, fextension = os.path.splitext(path)
    return fextension == extension


def get_filename(path):
    filename = os.path.split(path)[-1]
    filename = os.path.splitext(filename)[0]
    return filename


def save_html(soup, filename):
    with open(filename, "w") as file:
        file.write(str(soup))


def generate_id(string):
    return hashlib.sha1(str.encode(string)).hexdigest()


def prepare_options(results):
    line = '<option value="{}">{}</option>'
    options = []
    for index, result in enumerate(results):
        if isinstance(result, (int, str)):
            result = (result,)
        option = line.format(*result, *result)
        options.append(option)
    return options


def preprocess_string(line, sep=','):
    line = line[0].split(sep)
    return [
        re.sub(r'[^\w\s_]+', '', word).strip()
        for word in line
    ]


def include_page_content(current_dir):
    os.system("cd ../../static/img")
    os.system("ln -s ../../../page_content/img/* .")
    os.chdir(current_dir)

