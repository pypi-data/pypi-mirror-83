from finq import FINQ


def test_pairs():
    a = [1, 2, 5, 7]
    expected = [(0, 1), (1, 2), (2, 5), (3, 7)]

    a_f = FINQ(a)

    assert a_f.enumerate().to_list() == expected


def test_pairs_from_1():
    a = [1, 2, 5, 7]
    expected = [(1, 1), (2, 2), (3, 5), (4, 7)]

    a_f = FINQ(a)

    assert a_f.enumerate(1).to_list() == expected
