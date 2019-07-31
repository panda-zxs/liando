#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string
import time

from django.conf import settings


def convert_to_string(data):
    """
    Convert dict/list to string by:
        geting the firt item of firt value
    """
    if isinstance(data, dict):
        return convert_to_string(list(data.values())[0])
    elif isinstance(data, list):
        return convert_to_string(data[0])
    elif not isinstance(data, str):
        return str(data)
    return data


def is_simple_string_list(data):
    """
    Check if data is a string list.
    """
    if not isinstance(data, list):
        return False

    for ret in data:
        if not isinstance(ret, str):
            return False

    return True


def name_maker(prefix, num=settings.NAME_ID_LENGTH):
    words = string.digits + string.ascii_lowercase
    exclude_words = ['0', 'o', 'l', '1']
    words = ''.join(set(words) - set(exclude_words))
    random.seed(time.time())
    return prefix + '-' + ''.join(random.sample(words, num))
