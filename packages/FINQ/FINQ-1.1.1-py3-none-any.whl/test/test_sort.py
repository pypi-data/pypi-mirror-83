from finq import FINQ


def test_sorts_ints():
    a = [7, 15, 2, 22, 1, 12, 5, 26]
    expected = [1, 2, 5, 7, 12, 15, 22, 26]

    a_f = FINQ(a)

    assert a_f.sort().to_list() == expected


def test_sorts_strings():
    a = ['7', '15', '2', '22', '1', '12', '5', '26']
    expected = ['1', '12', '15', '2', '22', '26', '5', '7']

    a_f = FINQ(a)

    assert a_f.sort().to_list() == expected
