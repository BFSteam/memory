import os, sys, inspect

currentdir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import src.datastructures.news as nw

empty_news = {
    'id-n': None,
    'new': None,
    'id-source': None,
    'date-creation': None,
    'relevance': None
}


def news_empty():
    return nw.news()


def news_set():
    n = nw.news()
    n['relevance'] = 1
    return n


def news_get():
    n = nw.news()
    n['relevance'] = 1
    return n['relevance']


def news_length():
    return len(nw.news())


def news_delete():
    n = nw.news()
    n['relevance'] = 1
    del n['relevance']
    return n


def news_delete_non_existent():
    n = nw.news()
    n['relevance'] = 1
    try:
        del n['ciao']
        return True
    except:
        return n


def news_equal():
    return nw.news()


def news_clear():
    n = nw.news()
    n['relevance'] = 1
    n.clear()
    return n


def test_news_empty():
    assert news_empty() == empty_news


def test_news_set():
    assert news_set()['relevance'] == 1


def test_news_length():
    assert news_length() == len(nw.news._news_parameters)


def test_news_get():
    assert news_get() == 1


def test_news_delete():
    assert news_delete()['relevance'] == None


def test_news_delete_non_existent():
    assert news_delete_non_existent()['relevance'] == 1


def test_news_clear():
    assert news_clear() == empty_news


def test_news_equal():
    assert news_equal() == empty_news
    assert (news_equal() == 1) is False
