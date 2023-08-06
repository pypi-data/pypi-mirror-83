from finq import FINQ


def test_flatten_once():
    a = [[1], 4, [5]]
    expected = [1, 4, 5]

    assert FINQ(a).flatten().to_list() == expected


def test_flatten_more_than_once():
    a = [[[[1]]], 4, [5]]
    expected = [1, 4, 5]

    assert FINQ(a).flatten().to_list() == expected


def test_doesnt_flatten_flat_collection():
    a = [1, 4, 5]
    expected = [1, 4, 5]

    assert FINQ(a).flatten().to_list() == expected
