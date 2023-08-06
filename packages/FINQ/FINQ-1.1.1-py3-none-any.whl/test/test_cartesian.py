from finq import FINQ, PairSum, TupleSum


def test_cartesian_product():
    a = [1, 2, 5]
    b = [2, 3, 6]
    expected = [(1, 2), (1, 3), (1, 6), (2, 2), (2, 3), (2, 6), (5, 2), (5, 3), (5, 6)]

    assert FINQ(a).cartesian_product(b).to_list() == expected


def test_cartesian_product_with_mapping():
    a = [1, 2, 5]
    b = [2, 3, 6]
    expected = [3, 4, 7, 4, 5, 8, 7, 8, 11]

    assert FINQ(a).cartesian_product(b, PairSum).to_list() == expected


def test_cartesian_power():
    a = [1, 2, 5]
    expected = [(1, 1), (1, 2), (1, 5), (2, 1), (2, 2), (2, 5), (5, 1), (5, 2), (5, 5)]

    assert FINQ(a).cartesian_power(2).to_list() == expected


def test_cartesian_power_three():
    a = [1, 2]
    expected = [(1, 1, 1), (1, 1, 2), (1, 2, 1), (1, 2, 2), (2, 1, 1), (2, 1, 2), (2, 2, 1), (2, 2, 2)]

    assert FINQ(a).cartesian_power(3).to_list() == expected


def test_cartesian_first_power():
    a = [1, 2, 5]
    expected = [1, 2, 5]

    assert FINQ(a).cartesian_power(1).to_list() == expected


def test_cartesian_zero_power():
    a = [1, 2, 5]
    expected = []

    assert FINQ(a).cartesian_power(0).to_list() == expected


def test_cartesian_power_with_mapping():
    a = [1, 2, 5]
    expected = [2, 3, 6, 3, 4, 7, 6, 7, 10]

    assert FINQ(a).cartesian_power(2, PairSum).to_list() == expected


def test_cartesian_power_three_with_mapping():
    a = [1, 2]
    expected = [3, 4, 4, 5, 4, 5, 5, 6]

    assert FINQ(a).cartesian_power(3, TupleSum).to_list() == expected