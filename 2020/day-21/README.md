# Day 21: Allergen Assessment

Goal is to determine which ingredients cannot possibly contain any of the allergens in your list.

## Content Decoding

Contents are formatted in a series of **lines**. Each line has **two parts**: a **list of ingredients** and a **list of some or all allergens** in parenthesizes. Both lists contain items separated by single space characters.

```
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
```

After decoding:

```python
line = {
    'line': 1,
    'ingredients': ['mxmxvkd', 'kfcds', 'sqjhc', 'nhms'],
    'some_allergens': ['dairy', 'fish'],
}
```

### Multiple Stage String Split Decoding

This decoding methods involves a number of split stages:

* For each line until EOF:
    1. Test if it contains the line ending used when contents is present.
        * If not present, ignore this line and iterate again.
    1. Split line contents using `` (contains `` as separator into groups.
    1. Split each group using the space character `` `` as separator into a list of strings.
    1. Group lists in a dictionary structure.
    1. Yield the dictionary.

```python
def load_food_list(file: Path) -> Iterator[dict[str, any]]:
    line_ending = ')\n'
    for i, line in enumerate(open(file)):
        if not line.endswith(line_ending):
            continue
        groups = line.strip(line_ending).split(' (contains ')
        ingredients = groups[0].split()
        allergens = groups[1].split(', ')
        assert all(map(len, (ingredients, allergens)))
        food: dict = {
            'line': 1 + i,
            'ingredients': ingredients,
            'some_allergens': allergens,
            }
        yield food
```

## Data Recon

### Test for Lines with All Allergens Listed

The challenge states:

> Each allergen is found in exactly one ingredient. Each ingredient contains zero or one allergen. Allergens aren't always marked; when they're listed, the ingredient that contains each listed allergen will be somewhere in the corresponding ingredients list. However, even if an allergen isn't listed, the ingredient that contains that allergen could still be present: maybe they forgot to label it, or maybe it was labeled in a language you don't know.

A key point is the statement ``Allergens aren't always marked``. Being the case would allow assigning a set of known allergens to a set of ingredients. This can be tested by filtering lines with the same number of ingredients and allergens.

```python
if len(ingredients) == len(allergens):
    print(f'Found closed set at line {line}')
```

Contents File | Total Lines | Lines with All Allergens
--- | --- | ---
Example.txt | 4 | 0
Input.txt | 34 | 0

Although worth a try, *there are no lines with all allergens* being indicated. 

### Determining Known Allergens Set

The challenge states:

> Allergens aren't always marked.

However this is true on a per-food basis. The set of allergens can be compiled by iterating through all the food items.

```python
    ingredients = set()
    allergens = set()
    for food in foods:
        ingredients.update(food['ingredients'])
        allergens.update(food['some_allergens'])

```

Contents File | Ingredients | Allergens
--- | --- | ---
Example.txt | 7 | 3
Input.txt | 200 | 8

### Ingredients by Allergens Map

The challenge states:

> Each allergen is found in exactly one ingredient.

This statement implies that for all foods containing the allergen, ingredients which are not present in all the foods does not contain the corresponding allergen.

The idea consists in:

* Compile a set of ingredients
* Compile a map of food ingredients by allergen
* For each allergen:
    1. Get a list of ingredients present in all the food ingredients containing the allergen
    1. Remove these ingredients from the copy of the ingredient list

```python
def list_safe_ingredients(foods: list[dict[str, any]]) -> set[str]:
    safe_ingredients = {ingredient
                        for f in foods
                        for ingredient in f['ingredients']}
    ingredients_by_allergen = dict()
    for food in foods:
        ingredients = set(food['ingredients'])
        for allergen in food['some_allergens']:
            if allergen not in ingredients_by_allergen:
                ingredients_by_allergen[allergen] = [ingredients]
            else:
                ingredients_by_allergen[allergen].append(ingredients)
    for allergen, food_ingredients in ingredients_by_allergen.items():
        unsafe_ingredients = set.intersection(*food_ingredients)
        safe_ingredients -= unsafe_ingredients
    return safe_ingredients
```

### Counting Occurrences of Safe Ingredients

The submission question is as follows:

> How many times do any of those ingredients appear?

This count is obtained by iterating over each safe ingredients and over all foods.

```python
count = lambda i: sum(1 for f in foods if i in f['ingredients'])
submission = sum(count(i) for i in safe_ingredients)
```
