# Day 18: Operation Order

## Notes

### Content Decoder

Input description:
1. one expression per line
1. an expression contains a number of tokens separated by a single space character
1. opening and closing parenthesis are adjacent to respectively right and left number, ex. ``1 + (2 + 3) + 4``.

```python
expanded_expression: str = expression.replace('(', '( ').replace(')', ' )')
tokens: list[str] = expanded_expression.strip().split(TOKEN_DELIMITER)
```

### Evaluation

Due to parenthesis operations may require to be reordered. The shunting-yard algorithm is well fitted for this task.

```python
for t in tokens:
    if t.isnumeric():
        output_queue.append(int(t))
    elif t in ['+', '*']:
        while len(operator_stack) and operator_stack[-1] != '(':
            output_queue.append(operator_stack.pop())
        operator_stack.append(t)
    elif t == '(':
        operator_stack.append(t)
    elif t == ')':
        while operator_stack[-1] != '(':
            output_queue.append(operator_stack.pop())
        if operator_stack[-1] == '(':
            operator_stack.pop()
while len(operator_stack):
    output_queue.append(operator_stack.pop())
```

### RPN Stack Execution

Now we are left with a flattened RPN sequence which once processed gives the result of the input expression.

```python
stack: list[int] = list()
for t in tokens:
    if t in OPERATORS:
        arg_a: int = stack.pop()
        arg_b: int = stack.pop()
        result: int = 0
        if t == '+':
            result = arg_a + arg_b
        if t == '*':
            result = arg_a * arg_b
        stack.append(result)
    else:
        stack.append(t)

retval: int = stack.pop()
return retval
```  

### Part Two

The second part of the challenge introduces the notion of operator precedence. The priority of the addition and multiplication is inverted compared to the natural one (obviously to avoid using any built-it evaluation() method).

This requires a simple modification in the the evaluation step for stashing the lower priority operator when following a higher priority one:

```diff
        elif t in ['+', '*']:
-            while len(operator_stack) and operator_stack[-1] != '(':
                op = operator_stack.pop()
                output_queue.append(op)
            operator_stack.append(t)

        elif t in ['+', '*']:
+            while len(operator_stack) and (operator_stack[-1] == '+') and (t == '*') and operator_stack[-1] != '(':
                op = operator_stack.pop()
                output_queue.append(op)
            operator_stack.append(t)
```
