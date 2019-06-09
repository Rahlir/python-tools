"""Utilities functions for jupyter notebook"""

import shelve
from os.path import join


__all__ = ['save_to_shelve', 'save_dict_to_shelve', 'retrieve_from_shelve', 'retrieve_dict_from_shelve',
           'print_content_of_shelve']


def save_to_shelve(file_name, key, value):
    with shelve.open(join('shelve', file_name), protocol=4) as database:
        database[key] = value


def save_dict_to_shelve(file_name, dictionary):
    with shelve.open(join('shelve', file_name), protocol=4) as database:
        database.update(dictionary)


def retrieve_from_shelve(file_name, key):
    with shelve.open(join('shelve', file_name)) as database:
        return database[key]


def retrieve_dict_from_shelve(file_name):
    with shelve.open(join('shelve', file_name)) as database:
        result_dict = {}
        for key, value in database.items():
            result_dict[key] = value
        return result_dict


def print_content_of_shelve(filename):
    print("Keys in file `{:s}`:".format(filename))
    with shelve.open("shelve/{:s}".format(filename), protocol=4) as database:
        name_list = list(database.keys())
        sorted_name_list = sorted(name_list)
        for name in sorted_name_list:
            print(name)
