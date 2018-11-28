import os, sys, inspect

currentdir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import src.datastructures.database as db


def create_empty():
    """
    compare db.database() with empty dict
    """
    return {} == db.database()


def data_comparison():
    """
    compare db.database() with dict
    """
    data = db.database()
    data['a'] = 1
    data['b'] = 2
    data['c'] = 3
    return data == {'a': 1, 'b': 2, 'c': 3}


def data_assignment(**kwargs):
    """
    init db.database() given input dict as
    {'a':1, 'b':2, 'c':3}
    """
    data = db.database()
    for key in kwargs:
        print(key)
        print(kwargs[key])
        data[key] = kwargs[key]
    return data


def data_length():
    data = db.database()
    data['a'] = 1
    data['b'] = 2
    data['c'] = 3
    return len(data)


def data_list():
    data = db.database()
    data['a'] = 1
    data['b'] = 2
    data['c'] = 3
    return list(data)


def data_access():
    data = db.database()
    data['a'] = 1
    data['b'] = 2
    data['c'] = 3
    return data['a']


def test_create_empty():
    assert create_empty() == True


def test_data_assignment():
    assert data_assignment(a=1, b=2, c=3) == {'a': 1, 'b': 2, 'c': 3}


def test_data_comparison():
    assert data_comparison() == True


def test_data_length():
    assert data_length() == 3


def test_data_list():
    assert data_list() == list({'a': 1, 'b': 2, 'c': 3})


def test_data_access():
    assert data_access() == 1
