from finq import FINQ
from test.test_foreach import collector


def test_peek():
    a = [1, 2, 5, 7]
    expected = ['1', '1', '2', '2', '5', '5', '7', '7']

    mock = collector([])
    a_f = FINQ(a)

    a_f.map(str).peek(mock).for_each(mock)

    assert mock.collector == expected
