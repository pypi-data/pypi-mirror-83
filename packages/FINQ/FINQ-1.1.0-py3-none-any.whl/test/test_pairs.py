from finq import FINQ


def test_pairs():
    a = [1, 2, 5, 7]
    expected = [(1, 1), (1, 2), (1, 5), (1, 7),
                (2, 1), (2, 2), (2, 5), (2, 7),
                (5, 1), (5, 2), (5, 5), (5, 7),
                (7, 1), (7, 2), (7, 5), (7, 7)]

    a_f = FINQ(a)

    assert a_f.pairs().to_list() == expected


def test_pairs_of_empty():
    a = []
    expected = []

    a_f = FINQ(a)

    assert a_f.pairs().to_list() == expected
