from finq import FINQ


def test_int_map():
    a = [1, 2, 5, 7, 12, 15, 22, 26]
    expected = [1, 4, 25, 49, 144, 225, 484, 676]

    func = lambda i: i * i
    a_f = FINQ(a)

    assert a_f.map(func).to_list() == expected


def test_maps_str_to_int():
    a = ['1', '2', '5', '7', '12', '15', '22', '26']
    expected = [1, 2, 5, 7, 12, 15, 22, 26]

    a_f = FINQ(a)

    assert a_f.map(int).to_list() == expected


def inc_add(a):
    def inc(i):
        nonlocal a
        a += 1
        return i + a - 1

    return inc


def test_maps_with_captured_variable():
    a = [1, 2, 5, 7, 12, 15, 22, 26]
    expected = [2, 4, 8, 11, 17, 21, 29, 34]

    func = inc_add(1)

    a_f = FINQ(a)

    assert a_f.map(func).to_list() == expected
