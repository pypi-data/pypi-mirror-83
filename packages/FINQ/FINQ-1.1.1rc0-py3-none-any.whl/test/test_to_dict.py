from finq import FINQ, First, RPairWith, PairWith, Second


def test_dict_builds():
    a = [1, 1, 2, 3, 3, 3]
    expected = {0: [2], 1: [1, 1, 3, 3, 3]}
    func = lambda i: i % 2

    assert FINQ(a).group_by(func).map(RPairWith(First, func)).to_dict() == expected


def test_dict_builds_with_custom_key():
    a = [1, 1, 2, 3, 3, 3]
    expected = {0: [2], 1: [1, 1, 3, 3, 3]}
    func = lambda i: i % 2

    assert FINQ(a).group_by(func).map(PairWith(First, func)).to_dict(Second, First) == expected
