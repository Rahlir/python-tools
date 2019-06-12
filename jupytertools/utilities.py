"""Utilities functions for jupyter notebook"""

import shelve
from os.path import join


__all__ = ['save_to_shelve', 'save_dict_to_shelve', 'retrieve_from_shelve', 'retrieve_dict_from_shelve',
           'print_content_of_shelve']


def save_to_shelve(filename, key, value, foldername='shelve'):
    """Save the key and value pair into shelve file with
    given name. This function assumes that the working directory
    contains folder `shelve` where the shelve files are stored.

    Parameters
    ----------
    filename : name of the shelve file to be updated or created
    key : key of the value used when retrieving the value from shelve
    value : the object to be stored to the shelve file
    """
    with shelve.open(join(foldername, filename), protocol=4) as database:
        database[key] = value


def save_dict_to_shelve(filename, dictionary, foldername='shelve'):
    """Save the entire dictionary to disk as a shelve file.
    This function assumes that the working directory
    contains folder `shelve` where the shelve files are stored.

    Parameters
    ----------
    filename : name of the shelve file to be updated or created
    dictionary : dictionary to be stored to the file with given name
    """
    with shelve.open(join(foldername, filename), protocol=4) as database:
        database.update(dictionary)


def retrieve_from_shelve(filename, key, foldername='shelve'):
    """Retrieve the object stored in the file with given key.
    This function assumes that the working directory
    contains folder `shelve` where the shelve files are stored.

    Parameters
    ----------
    filename : name of the shelve file where the object is stored
    key : key of the object stored in the shelve file

    Returns
    -------
    stored_object: python object stored in the given file under the
        specified key
    """
    with shelve.open(join(foldername, filename)) as database:
        return database[key]


def retrieve_dict_from_shelve(filename, foldername='shelve'):
    """Retrieve an entire dictionary saved as a shelve file.
    This function assumes that the working directory
    contains folder `shelve` where the shelve files are stored.

    Parameters
    ----------
    filename : name of the shelve file

    Returns
    -------
    result_dict: dictionary of key value pairs saved on the disk
        as a shelve file
    """
    with shelve.open(join(foldername, filename)) as database:
        result_dict = {}
        for key, value in database.items():
            result_dict[key] = value
        return result_dict


def print_content_of_shelve(filename, foldername='shelve'):
    """Print all keys of a given shelve file.
    This function assumes that the working directory
    contains folder `shelve` where the shelve files are stored.

    Parameters
    ----------
    filename : name of the shelve file
    """
    print("Keys in file `{:s}`:".format(filename))
    with shelve.open("{:s}/{:s}".format(foldername, filename), protocol=4) as database:
        name_list = list(database.keys())
        sorted_name_list = sorted(name_list)
        for name in sorted_name_list:
            print(name)
