from finq import FINQ


def collector(l: list):
    def write(s: str):
        l.append(s)

    write.collector = l

    return write


def test_foreach():
    a = [1, 2, 5, 7]
    expected = ['1', '2', '5', '7']

    mock = collector([])
    a_f = FINQ(a)

    a_f.map(str).for_each(mock)

    assert mock.collector == expected
