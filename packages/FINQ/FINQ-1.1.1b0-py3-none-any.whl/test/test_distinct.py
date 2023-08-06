from finq import FINQ


def test_distinct():
    a = [125,627,77734,24,42,53,536,236,263,125,125,125,7,24,42,5]
    expected = [125,627,77734,24,42,53,536,236,263,7,5]

    assert FINQ(a).distinct().to_list() == expected