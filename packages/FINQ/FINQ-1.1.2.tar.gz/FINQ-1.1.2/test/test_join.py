from finq import FINQ


def test_join():
    a = [1, 2, 5, 7]
    expected = '1257'

    a_f = FINQ(a)

    assert a_f.map(str).join() == expected


def test_join_with_delim():
    a = [1, 2, 5, 7]
    expected = '1, 2, 5, 7'

    a_f = FINQ(a)

    assert a_f.map(str).join(', ') == expected
