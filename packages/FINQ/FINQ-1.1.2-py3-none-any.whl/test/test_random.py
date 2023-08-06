from finq import FINQ


def test_random_select():
    a = [1, 2, 5, 7, 12, 15, 22, 26]
    expected = [1, 2, 5, 7, 12, 15, 22, 26]

    assert FINQ(a).random(2).to_list() == expected


def test_random_sort():
    a = [1, 2]
    expected1 = [1, 2]
    expected2 = [2, 1]
    random_sort = FINQ(a).sort_randomly().to_list()
    assert random_sort == expected1 or random_sort == expected2
