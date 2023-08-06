from finq import FINQ


def test_concat_different():
    a = FINQ([1, 2, 5, 7, 12, 15, 22, 26])
    b = [2, 4, 79, 1, 125, 6]
    expected = [1, 2, 5, 7, 12, 15, 22, 26, 2, 4, 79, 1, 125, 6]

    assert a.concat(b).to_list() == expected


def test_concat_same():
    a_f = FINQ([1, 2, 5, 7, 12, 15, 22, 26])
    expected = [1, 2, 5, 7, 12, 15, 22, 26, 1, 2, 5, 7, 12, 15, 22, 26]

    assert a_f.concat(a_f).to_list() == expected
