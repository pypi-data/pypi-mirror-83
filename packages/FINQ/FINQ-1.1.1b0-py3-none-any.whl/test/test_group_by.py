from collections import Counter

from finq import FINQ


def test_group_by_identity():
    a = [1, 1, 2, 3, 3, 3]
    expected = [[1, 1], [2], [3, 3, 3]]

    assert FINQ(a).group_by().to_list() == expected


def test_group_by_func():
    a = [1, 1, 2, 3, 3, 3]
    expected = [[1, 1, 3, 3, 3], [2]]
    func = lambda i: i % 2

    assert FINQ(a).group_by(func).to_list() == expected


def test_flat_group_by_equals_argument():
    a = [1, 1, 2, 3, 3, 3]
    expected = Counter([1, 1, 2, 3, 3, 3])
    func = lambda i: i % 2

    assert FINQ(a).group_by(func).flatten().to_counter() == expected
