from finq import FINQ
from test.test_foreach import collector


def test_any():
    a = [1, 2, 5, 7]
    expected = [5, 7]

    a_f = FINQ(a)
    func = lambda i: i > 4

    assert a_f.any(func)
    assert a_f.filter(func).to_list() == expected


def test_any_false():
    a = [1, 2, 5, 7]
    expected = []

    a_f = FINQ(a)
    func = lambda i: i > 40

    assert not a_f.any(func)
    assert a_f.filter(func).to_list() == expected

def test_none_false():
    a = [1, 2, 5, 7]
    expected = [5, 7]

    a_f = FINQ(a)
    func = lambda i: i > 4

    assert not a_f.none(func)
    assert a_f.filter(func).to_list() == expected


def test_none():
    a = [1, 2, 5, 7]
    expected = []

    a_f = FINQ(a)
    func = lambda i: i > 40

    assert a_f.none(func)
    assert a_f.filter(func).to_list() == expected
