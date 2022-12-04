# Syntax Scoring

## Content Decoding

> The navigation subsystem syntax is made of several lines containing chunks.

The challenge offers the following hierarchy:

```
file > line > chunk
```

The corresponding decoding logic:

```python
with open(filename, encoding='utf-8') as buffer:
    for line in buffer.readlines():
        chunks = line.strip()
        yield chunks
```

## First Part

Starting from the end:

> Find the **first** illegal character in each corrupted line of the navigation subsystem. What is the total syntax error score for those errors?

The corresponding high-level method:

```python
def solve_first_part(contents: Generator) -> int:
    answer = 0
    for line in contents:
        for se in scan_syntax(line):
            answer += ERROR_SCORE[se]
            break
    return answer
```

The rest of the code consists in structure declarations.

| Contents                   | Command                      | Answer   | Time   |
|----------------------------|------------------------------|----------|--------|
| [`input.txt`](./input.txt) | `./day_20.py -p 1 input.txt` | `268845` | 0.5 ms | 

