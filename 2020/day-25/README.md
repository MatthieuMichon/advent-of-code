# Day 25: Combo Breaker

## Summary

Puzzle | Decode | Transform | Iterate | Answer
--- | --- | --- | --- | ---
Day 25 | - | - | - | -

## First Thoughts

### Transform Function

> To transform a *subject number*, start with the value `1`. Then, a number of times called the loop size, perform the two steps below.
>
> * Set the value to itself multiplied by the *subject number*.
> * Set the value to the remainder after dividing the value by `20201227`.
>
> The loop size is secret.

The transformation takes two variables `loop_size` and `subject_number` as an input and executes the following steps before returning its result.

```python
def transform(subject_number: int, loop_size: int) -> int:
    ...
```

Its docstring would be:

```python
    """Transform a subject number and loop size into a public key

    :param subject_number: transformation input value
    :param loop_size: number of iterations
    :return: key value 
    """
```
The algorithm would be as follows:

1. Set `value` to `1`.
1. Loop for `loop_size` times:
    1. assign to `value` its product by `subject_number`
    1. assign to `value` the remainder of its division by `20201227`
1. Return `value`

A simple implementation in Python would be:

```python
def transform(subject_number: int, loop_size: int) -> int:
    value: int = 1
    for _ in range(loop_size):
        value *= subject_number
        value %= 20201227
    return value
```

### Cryptographic Handshake

> * The card transforms the subject number of `7` according to the card's secret loop size. The result is called the card's public key.
> * The door transforms the subject number of `7` according to the door's secret loop size. The result is called the door's public key.
> * The card and door use the wireless RFID signal to transmit the two public keys (your puzzle input) to the other device. Now, the card has the door's public key, and the door has the card's public key. Because you can eavesdrop on the signal, you have both public keys, but neither device's loop size.
> * The card transforms the subject number of the door's public key according to the card's loop size. The result is the encryption key.
> * The door transforms the subject number of the card's public key according to the door's loop size. The result is the same encryption key as the card calculated.

1. Set `card_public_key` with `transform(subject_number=7, loop_size=card_secret_loop_size)`
1. Set `door_public_key` with `transform(subject_number=7, loop_size=door_secret_loop_size)`
1. Card and door exchange their respective public keys
1. Set `encryption_key` with `transform(subject_number=card_public_key, loop_size=door_secret_loop_size)`
1. Set `encryption_key` with `transform(subject_number=door_public_key, loop_size=card_secret_loop_size)`

The unknown values end up being the *encryption key* which depends on the either *loop_size* values. As indicated in the puzzle statement simple trial and error with *loop_size* value would allow one to compute the *encryption key*.

### Puzzle Input Decoding

> The card and door use the wireless RFID signal to transmit the two public keys (your puzzle input) to the other device.

The statement implies that puzzle input yields two public key encoded as integers. This implies the following `load_public_keys()` method.

```python
def load_public_keys(file: Path) -> tuple[int]:
    ...
```

The input file is constituted by two integers separated by a new line:

```
15335876
15086442
``` 

Thus the input decoding method would look like the following:

```python
def load_public_keys(file: Path) -> tuple[int]:
    public_keys_str = open(file).read().strip().split(os.linesep)
    public_keys = tuple(int(k) for k in public_keys_str)
    return public_keys
```

## Implementation

The goal of this puzzle is to compute the encryption key, with the only unknown value being the `loop_size` parameter which controls the number of iterations performed by the `transform()` method.

```python
def compute_encryption_key(public_keys: tuple) -> int:
    card_pk, door_pk = public_keys
    key = card_pk - 1
    loop_size: int = 0
    while key != card_pk:
        loop_size += 1
        key = transform(subject_number=7, loop_size=loop_size)
    encryption_key = transform(subject_number=door_pk, loop_size=loop_size)
    return encryption_key
```

### Performance Issues

The basic implementation of the transform() method is however not suited for computing results with a loop_size greater than four orders of magnitude.

The critical path being the arithmetical operations performed inside the loop:

```python
for _ in range(loop_size):
    value *= subject_number
    value %= 20201227
```

The modulus operation can deferred outside of the loop cutting down the total number of operations.

```python
for _ in range(loop_size):
    value *= subject_number
value %= 20201227
```

Further the repeating multiplication inside the loop is equivalent to the subject number power to the loop size:

```python
value *= subject_number**loop_size
value %= 20201227
```

Although much faster, the processing speed still requires improvement. The next step consists in inlining calls to `transform()`:

```python
def compute_encryption_key(public_keys: tuple) -> int:
    card_pk, door_pk = public_keys
    loop_size: int = 0
    loop_size_factor = 7
    while loop_size_factor % 20201227 != card_pk:
        loop_size += 1
        loop_size_factor *= 7
    loop_size += 1
    encryption_key = transform(subject_number=door_pk, loop_size=loop_size)
    return encryption_key
```

The result is now obtain in a few dozen of seconds.

[python-collections-counter]: https://docs.python.org/3/library/collections.html#collections.Counter
[python-iterable-unpacking]: https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists
