from finq import FINQ


def test_flat_map_list_of_lists_to_list():
    a = [[1, 2, 5], [7, 12], [15, 22, 26]]
    expected = [1, 2, 5, 7, 12, 15, 22, 26]

    a_f = FINQ(a)

    assert a_f.flat_map().to_list() == expected


def test_flat_map_list_of_tuples_to_list():
    a = [(1, 2, 5), (7, 12), (15, 22, 26)]
    expected = [1, 2, 5, 7, 12, 15, 22, 26]

    a_f = FINQ(a)

    assert a_f.flat_map().to_list() == expected


def test_flat_map_tuple_of_list_to_list():
    a = ([1, 2, 5], [7, 12], [15, 22, 26])
    expected = [1, 2, 5, 7, 12, 15, 22, 26]

    a_f = FINQ(a)

    assert a_f.flat_map().to_list() == expected


def test_flat_map_set_of_list_to_list():
    a = {(1, 2, 5), (7, 12), (15, 22, 26)}
    expected = [1, 2, 5, 7, 12, 15, 22, 26]

    a_f = FINQ(a)

    assert a_f.flat_map().to_list() == expected
