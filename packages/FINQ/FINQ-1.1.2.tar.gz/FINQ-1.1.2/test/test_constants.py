from finq import Identity, Consumer, IdentityTrue, IdentityFalse, Sum, Multiply, Square, PairSum, TupleSum, First, \
    Second, FINQ, PairWith, Compose


def test_identity():
    a = 125123621
    assert Identity(a) == a


def test_consumer():
    a = 125123621
    assert Consumer(a) is None


def test_identity_true():
    a = 125123621
    assert IdentityTrue(a)


def test_identity_false():
    a = 125123621
    assert not IdentityFalse(a)


def test_sum():
    a = 125123621
    b = 125123622
    assert Sum(a, b) == a + b


def test_multiply():
    a = 125123621
    b = 125123622
    assert Multiply(a, b) == a * b


def test_square():
    a = 125123621
    assert Square(a) == a * a


def test_pair_sum():
    a = 125123621, 125123622
    assert PairSum(a) == a[0] + a[1]


def test_pair_tuple_sum():
    a = 125123621, 125123622
    assert TupleSum(a) == a[0] + a[1]


def test_empty_tuple_sum():
    a = ()
    assert TupleSum(a) == 0


def test_singular_tuple_sum():
    a = (125123621,)
    assert TupleSum(a) == a[0]


def test_triple_tuple_sum():
    a = (125123621, 125123621, 125123621)
    assert TupleSum(a) == a[0] * 3


def test_first():
    a = 125123621, 125123622
    assert First(a) == a[0]


def test_second():
    a = 125123621, 125123622
    assert Second(a) == a[1]


def test_pair_with_identity():
    a = [1, 1, 2, 3, 3, 3]
    expected = [(1, 1), (1, 1), (2, 2), (3, 3), (3, 3), (3, 3)]

    assert FINQ(a).map(PairWith(Identity)).to_list() == expected


def a(w):
    def _a(x):
        w.append('a'+str(x))
        return x + 1

    return _a


def b(w):
    def _b(x):
        w.append('b'+str(x))
        return x - 1

    return _b


def test_compose():
    ll = []

    expectedF = Identity
    composition = Compose(a(ll), b(ll))

    expected = FINQ(range(100))
    composition(0)
    assert ll == ['a0', 'b1']
    assert FINQ(range(100)).map(composition).to_list() == expected.map(expectedF).to_list()
