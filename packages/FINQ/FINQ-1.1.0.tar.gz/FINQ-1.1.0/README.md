# FINQ
Lightweight conveyor data processing python framework, which allows to quickly write long queries without a fear that it'll become unreadable, 
because FINQ as opposed to standard library allows you to write each logical part of query at next line without tearing it and expanding logical block over whole function


## Basic functions
| Function                                         | IsTerminal | Description                                                                                                               |
|--------------------------------------------------|------------|---------------------------------------------------------------------------------------------------------------------------|
| `concat(b:Iterable[T])`                          | -          | Concatenates two sequences, creating sequence that contains of the first iterable then of second iterable.                |
| `map(*f:T -> T2)`                                | -          | Applies composition of given functions to every element of sequence.                                                      |
| `zip(b:Iterable[T])`                             | -          | Pairs corresponding elements of two sequences in pairs.                                                                   |
| `flat_map(f:T -> Collection[T2] = Identity)`     | -          | Applies given function to every element to get collection, then glues these collections.                                  |
| `flatten(f:T -> Collection[T] = Identity)`       | -          | Applies given function to every element to get collection, then glues these collections. Repeats while all elements are iterables.|
| `filter(f:T -> bool)`                            | -          | Removes elements that doesn't satisfy predicate from sequence.                                                            |
| `distinct(f:T -> T2)`                            | -          | Skips elements which _f(element)_ repeated.                                                                               |
| `sort(f:T -> int)`                               | -          | Sorts sequence elements by key given by _f_.                                                                              |
| `skip(count:int)`                                | -          | Skips _count_ elements from sequence.                                                                                     |
| `take(count:int)`                                | -          | Limits sequence by _count_ elements, dropping other.                                                                      |
| `cartesian_product(b:Iterable[T1], mapping:T×T1 -> T2)` | -   | Returns Cartesian product of two sequences after application of mapping if specified.                                     |
| `cartesian_power(pow:int, mapping:T^pow -> T2)`  | -          | Returns Cartesian power of sequence after application of mapping if specified.                                            |
| `pairs()`                                        | -          | Returns Cartesian square of sequence. Equivalent to Cartesian square with Identity mapping.                               |
| `enumerate(start=0)`                             | -          | Maps sequence elements to pair which first value is index in sequence starting by _start_.                                |
| `peek(f:T -> ())`                                | -          | Applies function to each element in sequence leaving sequence unchanged.                                                  |
| `group_by(f:T -> T2 = Identity)`                 | -          | Splits sequence into sequence of lists of elements which _f(x)_ is the same.                                              |
| `random(precentage:float)`                       | -          | Takes roughly _percentage_*100% of random elements of sequence.                                                           |
| `sort_randomly()`                                | -          | Shuffles sequence.                                                                                                        |
| `join(delimiter:str)`                            | +          | Joins sequence by _delimiter_.                                                                                            |
| `for_each(f:T -> () = Consumer)`                 | +          | Calls _f_ for every element of a sequence. Equivalent to:<br> <code>for e in collection:</code><br><code>    f(e)</code>. |
| `any(f:T -> bool = IdentityTrue)`                | +          | Checks if there exist element in sequence that satisfies predicate.                                                       |
| `none(f:T -> bool = IdentityTrue)`               | +          | Checks if there no element in sequence that satisfies predicate.                                                          |
| `first()`                                        | +          | Takes first element of sequence.                                                                                          |
| `to_list()`                                      | +          | Creates default python-list containing all sequence elements.                                                             |
| `to_set()`                                       | +          | Creates default python-set containing all distinct sequence elements.                                                     |
| `to_counter()`                                   | +          | Creates Counter containing all sequence elements.                                                                         |
| `to_dict(key:T -> TKey = First, value:T -> TValue = Second)` | + | Creates default python-dict containing mapping (key(x), value(x)) for every x in sequence.                             |
| `count()`                                        | +          | Returns count of elements in sequence.                                                                                    |
| `min()`                                          | +          | Finds minimal element in sequence.                                                                                        |
| `max()`                                          | +          | Finds maximal element in sequence.                                                                                        |
| `sum()`                                          | +          | Sums all elements of sequence. Works only for summable types.                                                             |
| `max_diff()`                                     | +          | Counts maximal difference between elements. Equal to difference between max and min for sequence.                         |
| `reduce(f:T×T -> T)`                             | +          | Applies function to first two elements, then to result and next element until elements end. Allows to specify first element. |
| `reduce_with_first(first:T, f:T×T -> T)`         | +          | Applies function to first two elements, then to result and next element until elements end.                               |

## Constant functions

* `Identity: T -> T = λf: f`
* `Consumer: T -> () = λf: None`
* `IdentityTrue: T -> bool = λf: True`
* `IdentityFalse: T -> bool = λf: False`
* `Sum: T×T -> T = λa,b: a + b`
* `PairSum: T^2 -> T = λt: t[0] + t[1]`
* `First: T^n -> T = λt: t[0]`
* `Second: T^n -> T = λt: t[1]`
* `Multiply: T×T -> T = λa,b: a * b`
* `Square: T -> T = λa: a * a`
* `OneArgRandom: T -> float = λv: random()`