# 🎄🌟🌟 Smoke Basin 🎄🌟🌟

## 💾 Content Decoding

This challenge requires performing computations on a two-dimensional array, for example comparison with neighbor cells.

Although a two-dimensional array could have done the job, I went with a hash map using coordinates, defined as a `set`, as the key.

```python
def load_contents(filename: Path) -> Generator:
    """Load and convert contents from file

    :param filename: input filename
    :return: map generator
    """
    with open(filename, encoding='utf-8') as buffer:
        for i, line in enumerate(buffer.readlines()):
            for j, val in enumerate(line.strip()):
                yield (i, j), val
```

Decoding speed is appropriate.

## 💡 First Part

> Your first goal is to find the low points - the locations that are lower than any of its adjacent locations.





