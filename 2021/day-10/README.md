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
| [`input.txt`](./input.txt) | `./day_10.py -p 1 input.txt` | `268845` | 0.5 ms | 

## Second Part

Following on the work laid out prior, the second part requires discarding previously matched lines. This done by checking if the `scan_syntax()` method returned at least a single entry.

```python
corrupted_line = any(True for _ in scan_syntax(line=line))
if corrupted_line:
    continue
```

The completion string is then built using a dedicated `autocomplete()` method:

```python
def autocomplete(line: str) -> str:
    chunks = list()
    for chunk in line:
        opening_token = chunk in OPENING_MAP
        if opening_token:
            chunks.insert(0, OPENING_MAP[chunk])
        else:
            chunks.pop(0)
    return ''.join(chunks)
```

No grounds were broken here, although push / pop operations are done on the other side of the list which results in the reversed ordering of the remaining items.

The higher level `solve_second_part()` is also straight forward.

```python
def solve_second_part(contents: Iterator[str]) -> int:
    scores = list()
    for line in contents:
        corrupted_line = any(True for _ in scan_syntax(line=line))
        if corrupted_line:
            continue
        completion_string = autocomplete(line=line)
        score = 0
        for char in completion_string:
            score = 5 * score + CLOSING_SCORE[char]
        scores.append(score)
    scores.sort()
    answer = scores[len(scores) // 2]
    return answer
```

| Contents                   | Command                      | Answer       | Time   |
|----------------------------|------------------------------|--------------|--------|
| [`input.txt`](./input.txt) | `./day_10.py -p 2 input.txt` | `4038824534` | 0.9 ms | 
