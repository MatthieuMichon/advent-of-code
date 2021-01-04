# Day 19: Monster Messages

## Content Decoding

Input contents are divided in two sections: rules and received messages.

Rules for valid messages start with a unique number; semi-colon; space than either:
* a single char enclosed in double quotes
* a set of numbers and pipes separated with spaces

```
0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"
```

Each rules has an unique number, making them easy to load in map.

```python
fp = itertools.dropwhile(lambda l: l == '\n', open(file))
convert = lambda t: int(t) if t.isnumeric() else t.replace('"', '')
rule_map: dict[int, any] = dict()
received_messages = list()
for parts in (line.strip().split(RULE_NUMBER_SUFFIX) for line in fp):
    if len(parts) == 2:
        tokens = parts[1].strip().split(SEPARATOR)
        rule_map[int(parts[0])] = [convert(t) for t in tokens]
    else:
        received_messages.append(parts[0])
``` 

## Graping Rules

Instead of relying on regexes, the solver attempts to graph all valid message rules. The rule map is traversed in a top-down fashion, the only tricky part being handling the multiple options which arise when the pipe ``|`` character is encountered.

```python
rules = rule_map[rule_index]
if isinstance(rules[0], str):
    return rules
temp = list()
retval = list()
for r in rules:
    if r != '|':
        temp.append(graph_rules(rule_map, r))
    else:
        retval.extend(''.join(c) for c in itertools.product(*temp))
        temp = list()
retval.extend(''.join(c) for c in itertools.product(*temp))
return retval
```

