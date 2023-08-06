from finq import FINQ


def test_first():
    a = [1, 2, 5, 7, 12, 15, 22, 26]

    a_f = FINQ(a)

    assert a_f.first() == 1


def test_first_twice():
    a = [1, 2, 5, 7, 12, 15, 22, 26]

    a_f = FINQ(a)

    assert a_f.first() == 1
    assert a_f.first() == 1


def test_to_set():
    a = [1, 2, 5, 7, 12, 15, 22, 26]
    expected = {1, 2, 5, 7, 12, 15, 22, 26}

    a_f = FINQ(a)

    assert a_f.to_set() == expected


def test_to_list():
    a = {1, 2, 5, 7, 12, 15, 22, 26}
    expected = [1, 2, 5, 7, 12, 15, 22, 26]

    a_f = FINQ(a)

    assert a_f.to_list() == expected
