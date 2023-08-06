from finq import FINQ


def test_reduce():
    a = [1, 2, 5, 7, 12, 15, 22, 26]
    expected = 90

    a_f = FINQ(a)

    assert a_f.reduce(lambda a, b: a + b) == expected


def test_reduce_with_first():
    a = [1, 2, 5, 7, 12, 15, 22, 26]
    expected = 100

    a_f = FINQ(a)

    assert a_f.reduce_with_first(10, lambda a, b: a + b) == expected
