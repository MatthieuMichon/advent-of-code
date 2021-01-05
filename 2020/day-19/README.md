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

## Part 2

Initial implementation was unrolling the recurrent rules on a depth matching the longest message. This turned up being too slow and memory intensive.

```python
retval: dict[int, list] = dict()
for k, v in rules.items():
    rule_is_recursive = k in v
    if rule_is_recursive:
        unrolled_rule = v[:v.index('|')]
        repeating_group = v[v.index('|')+1:]
        rule_suffix = repeating_group.copy()
        for depth in range(max_depth):
            i = rule_suffix.index(k)
            rule_suffix[i:i+1] = repeating_group
            unrolled_rule.extend(['|'] + rule_suffix)
        retval[k] = [item for item in unrolled_rule if item != k]
    else:
        retval[k] = v
return retval
```

Looking into third-party implementations it appeared that there was no other way than crafting a solution with some hard coded assumptions: that both modified rules relied only on two other rules yielding matches with the exact same lengths.

```python
rule_31_solutions = set(graph_rules(rules, 31))
rule_31_sol_lengths = {len(s) for s in rule_31_solutions}
rule_42_solutions = set(graph_rules(rules, 42))
rule_42_sol_lengths = {len(s) for s in rule_42_solutions}
assert rule_31_sol_lengths == rule_42_sol_lengths
block_len = next(iter(rule_31_sol_lengths))

valid_messages = 0
for msg in messages:
    words = [msg[0 + i:block_len + i] for i in range(0, len(msg), block_len)]
    word_cnt = len(words)
    rule_31_match_cnt = 0
    for word in reversed(words):  # reverse since rule 31 matches at the end of message
        if word in rule_31_solutions:
            rule_31_match_cnt += 1
        else:
            break
    if 0 < rule_31_match_cnt < word_cnt/2 and all(word in rule_42_solutions for word in words[:-rule_31_match_cnt]):
        valid_messages += 1

return valid_messages
```
