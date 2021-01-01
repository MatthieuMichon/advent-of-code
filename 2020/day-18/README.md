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

## Part One

As you look out the window and notice a heavily-forested continent slowly appear over the horizon, you are interrupted by the child sitting next to you. They're curious if you could help them with their math homework.

Unfortunately, it seems like this "math" follows different rules than you remember.

The homework (your puzzle input) consists of a series of expressions that consist of addition (+), multiplication (*), and parenthesis ((...)). Just like normal math, parenthesis indicate that the expression inside must be evaluated before it can be used by the surrounding expression. Addition still finds the sum of the numbers on both sides of the operator, and multiplication still finds the product.

However, the rules of operator precedence have changed. Rather than evaluating multiplication before addition, the operators have the same precedence, and are evaluated left-to-right regardless of the order in which they appear.

For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are as follows:

```
1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
      9   + 4 * 5 + 6
         13   * 5 + 6
             65   + 6
                 71
```

Parentheses can override this order; for example, here is what happens if parenthesis are added to form 1 + (2 * 3) + (4 * (5 + 6)):

```
1 + (2 * 3) + (4 * (5 + 6))
1 +    6    + (4 * (5 + 6))
     7      + (4 * (5 + 6))
     7      + (4 *   11   )
     7      +     44
            51
```

Here are a few more examples:

```
    2 * 3 + (4 * 5) becomes 26.
    5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
    5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
    ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.
```

Before you can help with the homework, you need to understand it yourself. Evaluate the expression on each line of the homework; what is the sum of the resulting values?
