# FINQ
Lightweight conveyor data processing python framework, which allows to quickly write long queries without a fear that it'll become unreadable, 
because FINQ as opposed to standard library allows you to write each logical part of query at next line without tearing it and expanding logical block over whole function

## Start
To start conveyor processing of your iterable you need to wrap it with `FINQ()` object which then allows you to call Basic methods

## Basic methods
| Method                                           | IsTerminal | Description                                                                                                               |
|--------------------------------------------------|------------|---------------------------------------------------------------------------------------------------------------------------|
| `concat(b:Iterable[T])`                          | -          | Concatenates two sequences, creating sequence that contains items of the first iterable then of second iterable.          |
| `map(*f:T -> T2)`                                | -          | Applies composition of given functions to every element of sequence.                                                      |
| `zip(b:Iterable[T])`                             | -          | Pairs corresponding elements of two sequences in pairs.                                                                   |
| `flat_map(f:T -> Collection[T2] = Identity)`     | -          | Applies given function to every element to get collection, then glues these collections.                                  |
| `flatten(f:T -> Collection[T] = Identity)`       | -          | Applies given function to every element to get collection, then glues these collections. Repeats while all elements are iterables. |
| `filter(f:T -> bool)`                            | -          | Removes elements that doesn't satisfy predicate from sequence.                                                            |
| `distinct(f:T -> T2)`                            | -          | Skips elements which `f(element)` repeated.                                                                               |
| `sort(f:T -> int)`                               | -          | Sorts sequence elements by key given by `f`.                                                                              |
| `skip(count:int)`                                | -          | Skips `count` elements from sequence.                                                                                     |
| `take(count:int)`                                | -          | Limits sequence by `count` elements, dropping others.                                                                      |
| `cartesian_product(b:Iterable[T1], mapping:T×T1 -> T2)` | -   | Returns Cartesian product of two sequences after application of mapping if specified.                                     |
| `cartesian_power(pow:int, mapping:T^pow -> T2)`  | -          | Returns Cartesian power of sequence after application of mapping if specified.                                            |
| `pairs()`                                        | -          | Returns Cartesian square of sequence. Equivalent to Cartesian square with Identity mapping.                               |
| `enumerate(start=0)`                             | -          | Maps sequence elements to pair which first value is index in sequence starting by `start`.                                |
| `peek(f:T -> ())`                                | -          | Applies function to each element in sequence leaving sequence unchanged.                                                  |
| `group_by(mapping:T -> T2 = Identity)`           | -          | Splits sequence into sequence of lists of elements which `f(x)` is the same.                                              |
| `random(precentage:float)`                       | -          | Takes roughly `percentage*100%` of random elements of sequence.                                                           |
| `sort_randomly()`                                | -          | Shuffles sequence.                                                                                                        |
| `join(delimiter:str)`                            | +          | Joins sequence by `delimiter`.                                                                                            |
| `for_each(f:T -> () = Consumer)`                 | +          | Calls `f` for every element of a sequence. Equivalent to:<br> <code>for e in collection:</code><br><code>    f(e)</code>. |
| `all(f:T -> bool = IdentityTrue)`                | +          | Checks if all elements in sequence satisfy predicate.                                                       |
| `any(f:T -> bool = IdentityTrue)`                | +          | Checks if there exist element in sequence that satisfies predicate.                                                       |
| `none(f:T -> bool = IdentityTrue)`               | +          | Checks if there no element in sequence that satisfies predicate.                                                          |
| `first()`                                        | +          | Takes first element of sequence.                                                                                          |
| `to_list()`                                      | +          | Creates default python-list containing all sequence elements.                                                             |
| `to_set()`                                       | +          | Creates default python-set containing all distinct sequence elements.                                                     |
| `to_counter()`                                   | +          | Creates Counter containing all sequence elements.                                                                         |
| `to_dict(key:T -> TKey = First, value:T -> TValue = Second)` | + | Creates default python-dict containing mapping `(key(x), value(x))` for every `x` in sequence.                             |
| `count()`                                        | +          | Returns count of elements in sequence.                                                                                    |
| `min()`                                          | +          | Finds minimal element in sequence.                                                                                        |
| `max()`                                          | +          | Finds maximal element in sequence.                                                                                        |
| `sum()`                                          | +          | Sums all elements of sequence. Works only for summable types.                                                             |
| `max_diff()`                                     | +          | Counts maximal difference between elements. Equal to difference between max and min for sequence.                         |
| `reduce(f:T×T -> T, /, first:T)`                 | +          | Applies function to first two elements, then to result and next element until elements end. Allows to specify first element. |

## Constant functions
These functions aren't intended to be called manually. Instead you have to pass them as an arguments to FINQ methods as mappings, reducers, predicates.
Ordered Collection here is any collection which provides `__get_item__` based on index (Tuple, List)

| Method          |               | Returns |
|-----------------|---------------|-------------|
| `Identity`      | `T -> T`      | Given argument |
| `Consumer`      | `T -> None`   | None |
| `IdentityTrue`  | `T -> bool`   | True for any argument |
| `IdentityFalse` | `T -> bool`   | False for any value |
| `Sum`           | `T×T -> T`    | Sum of two given values |
| `PairSum`       | `T² -> T`     | Sum of first two values of Ordered Collection |
| `First`         | `Tⁿ -> T`     | First value of Ordered Collection |
| `Second`        | `Tⁿ -> T`     | Second value of Ordered Collection |
| `Multiply`      | `T×T -> T`    | Product of two given value |
| `Square`        | `T -> T`      | Square of given value |
| `OneArgRandom`  | `T -> float`  | Random value independent of given value |
| `TupleSum`      | `Tⁿ -> T`      | Sum of given Ordered Collection |
| `PairWith`      | `Fⁿ -> (T -> T²)` | Function that, when applied to value `e` returns `e, f1(f2(...fn(e)...))` |
| `RPairWith`     | `Fⁿ -> (T -> T²)` | Function that, when applied to value `e` returns `f1(f2(...fn(e)...)), e` |
| `Compose`       | `Fⁿ -> F`      | Function that, when applied to value `e` returns `f1(f2(...fn(e)...))` |
