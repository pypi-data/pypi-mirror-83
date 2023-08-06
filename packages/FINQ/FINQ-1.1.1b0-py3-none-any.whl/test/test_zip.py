from finq import FINQ


def test_zip():
    a = [1, 2, 5, 7, 12, 15, 22, 26]
    b = [1, 2, 5, 7, 12, 15, 22, 26]
    expected = [(1, 1), (2, 2), (5, 5), (7, 7), (12, 12), (15, 15), (22, 22), (26, 26)]

    assert FINQ(a).zip(b).to_list() == expected
