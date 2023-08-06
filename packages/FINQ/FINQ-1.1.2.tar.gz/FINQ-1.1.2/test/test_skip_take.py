from finq import FINQ


def test_skips():
    a = [1, 2, 5, 7, 12, 15, 22, 26]
    expected = [7, 12, 15, 22, 26]

    a_f = FINQ(a)

    assert a_f.skip(3).to_list() == expected


def test_takes():
    a = ['7', '15', '2', '22', '1', '12', '5', '26']
    expected = ['7', '15', '2', '22']

    a_f = FINQ(a)

    assert a_f.take(4).to_list() == expected


def test_takes_more_than_exist():
    a = [1, 2, 5, 7, 12, 15, 22, 26]
    expected = [1, 2, 5, 7, 12, 15, 22, 26]

    a_f = FINQ(a)

    assert a_f.take(40).to_list() == expected


def test_skips_more_than_exist():
    a = [1, 2, 5, 7, 12, 15, 22, 26]
    expected = []

    a_f = FINQ(a)

    assert a_f.skip(40).to_list() == expected
