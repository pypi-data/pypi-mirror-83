from os.path import abspath, join, dirname

import RandomHelper

full_path = lambda filename: abspath(join(dirname(__file__), filename))

FILE = {
    'alphanum:pass': full_path('dist.pass.alphanum'),
    'alpha:pass': full_path('dist.pass.alpha')

}


def get_email_unit(filename):
    """Select a random pass unit"""
    selected = RandomHelper.singelton_float_bit() * 120
    with open(filename) as name_file:
        for line in name_file:
            pass_value, cummulative = line.split()
            if float(cummulative) > selected:
                return pass_value
    return ""


def get_email(emaillength=10, serviceprovider='xyz', isalphanum=False):
    """Generates a random email with the specified length and service provider"""
    email_values = []
    count = 0
    while count < emaillength:
        if isalphanum:
            instant_value = get_email_unit(FILE['alphanum:pass'])

        else:
            instant_value = get_email_unit(FILE['alpha:pass'])

        email_values.append(instant_value)
        count = count + 1

    generated_email = ''.join([str(value) for value in email_values]) + '@' + serviceprovider + '.com'

    return generated_email
