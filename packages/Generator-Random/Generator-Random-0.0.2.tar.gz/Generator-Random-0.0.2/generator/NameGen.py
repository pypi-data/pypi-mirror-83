from __future__ import unicode_literals

import random
from os.path import abspath, join, dirname

import RandomHelper

full_path = lambda filename: abspath(join(dirname(__file__), filename))

FILES = {
    'first:male': full_path('dist.male.first'),
    'first:female': full_path('dist.female.first'),
    'last': full_path('dist.all.last')
}


def get_name(filename):
    """Generate random name from dataset"""
    selected = RandomHelper.singelton_float_bit() * 90
    with open(filename) as name_file:
        for line in name_file:
            name, _, cummulative, _ = line.split()
            print(cummulative)
            if float(cummulative) > selected:
                return name
    return ""


def get_first_name_western(gender=None):
    """Selects random Western First name from dataset"""
    if gender not in ('male', 'female'):
        gender = random.choice(('male', 'female'))
    return get_name(FILES['first:%s' % gender]).capitalize()


def get_last_name_western():
    """Selects random Western Last name from dataset"""
    return get_name(FILES['last']).capitalize()


def get_full_name_western(gender=None):
    """Selects random Western Full name from dataset"""
    return "{0}{1}{2}".format(get_first_name_western(gender).capitalize(), ' ', get_last_name_western().capitalize())
