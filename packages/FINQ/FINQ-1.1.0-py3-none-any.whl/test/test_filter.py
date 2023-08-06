from finq import FINQ


def odd(a):
    return a % 2 == 1


def test_filters_odd():
    a = [1, 2, 5, 7, 12, 15, 22, 26]
    expected = [1, 5, 7, 15]

    a_f = FINQ(a)

    assert a_f.filter(odd).to_list() == expected


def test_filters_none():
    a = [1, 2, 5, 7, 12, 15, 22, 26]
    expected = []

    a_f = FINQ(a)

    assert a_f.filter(lambda a: False).to_list() == expected


def test_filters_nonbool():
    a = [1, 2, 5, 7, 12, 15, 22, 26]
    expected = [1, 2, 5, 7, 15, 22, 26]

    a_f = FINQ(a)
    assert a_f.filter(lambda a: a - 12).to_list() == expected
