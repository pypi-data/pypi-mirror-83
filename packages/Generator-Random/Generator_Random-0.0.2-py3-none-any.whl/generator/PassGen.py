from __future__ import unicode_literals

from os.path import abspath, join, dirname

import RandomHelper

full_path = lambda filename: abspath(join(dirname(__file__), filename))

FILES = {
    'num:pass': full_path('dist.pass.num'),
    'alpha:pass': full_path('dist.pass.alpha'),
    'alphanum:pass': full_path('dist.pass.alphanum'),
    'alphanumspecial:pass': full_path('dist.pass.alphanumspecial')

}


def get_pass_unit(filename):
    """Select a random pass unit"""
    selected = RandomHelper.singelton_float_bit() * 120
    with open(filename) as name_file:
        for line in name_file:
            pass_value, cummulative = line.split()
            if float(cummulative) > selected:
                return pass_value

    return ""


def pass_maker(filename, passlength=8):
    """Generates a random pass with the specified length"""
    pass_values = []
    count = 0
    while count < passlength:
        instant_value = get_pass_unit(filename)
        pass_values.append(instant_value)
        count = count + 1

    generated_pass = ''.join([str(value) for value in pass_values])

    return generated_pass


def get_pass_num(passlength):
    """Generates a random numeric password with specified length"""
    return pass_maker(FILES['num:pass'], passlength)


def get_pass_alpha(passlength):
    """Generates a random alphabetic password with specified length"""
    return pass_maker(FILES['alpha:pass'], passlength)


def get_pass_alphanum(passlength):
    """Generates a random alpha numeric password with specified length"""
    return pass_maker(FILES['alphanum:pass'], passlength)


def get_pass_aplhanumspecial(passlength):
    """Generates a random alpha numeric special charachter password with specified length"""
    return pass_maker(FILES['alphanumspecial:pass'], passlength)


if __name__ == '__main__':
    get_pass_unit(FILES['num:pass'])
