# daproli [![PyPI version](https://badge.fury.io/py/daproli.svg)](https://pypi.org/project/daproli/) [![Build Status](https://travis-ci.com/ermshaua/daproli.svg?branch=master)](https://travis-ci.com/ermshaua/daproli) [![Downloads](https://pepy.tech/badge/daproli)](https://pepy.tech/project/daproli)
A small data processing library that attempts to make data transformation more declarative.

## Installation

You can install daproli with PyPi:
`python -m pip install daproli`

## Examples

Let's first import daproli.

```python3
>>> import daproli as dp
```

The library provides basic data transformation methods. In default mode, all transformations are single-threaded and silent. You can specify the amount of jobs with ```n_jobs```, provide further parameters like ```backend``` for the ```joblib``` module and increase the verbosity level with ```verbose```. 

```python3
>>> names = ['John', 'Susan', 'Mike']
>>> numbers = range(10)
```

```python3
>>> even_numbers = range(0, 10, 2)
>>> odd_numbers = range(1, 10, 2)
```

```python3
>>> dp.map(str.lower, names)
['john', 'susan', 'mike']
```

```python3
>>> dp.filter(lambda n : len(n) % 2 == 0, names)
['John', 'Mike']
```

```python3
>>> dp.split(lambda x : x % 2 == 0, numbers)
[[1, 3, 5, 7, 9], [0, 2, 4, 6, 8]]
```

```python3
>>> dp.expand(lambda x : (x, x**2), numbers)
[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]]
```

```python3
>>> dp.combine(lambda x, y : (x,y), even_numbers, odd_numbers)
[(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]
```

```python3
>>> dp.join(lambda x, y : y-x == 3, even_numbers, odd_numbers)
[(0, 3), (2, 5), (4, 7), (6, 9)]
```

daproli implements basic data manipulation functions.

```python3
>>> dp.windowed(numbers, 2, step=2)
[[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]
```
```python3
>>> dp.flatten([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

Additionally, it provides a data transformation pipeline framework. All transformation and manipulation procedures have respective transformers with the same arguments. There are also utility transformers like ```Union``` or ```Manipulator``` that help to connect transformers or make global changes to the data container.

```python3
>>> dp.Pipeline(
        dp.Splitter(lambda x: x % 2 == 1),
        dp.Union(
            dp.Mapper(lambda x: x ** 2),
            dp.Mapper(lambda x: x ** 3),
        ),
        dp.Combiner(lambda x1, x2: (x1, x2))
    ).transform(numbers)
[(0, 1), (4, 27), (16, 125), (36, 343), (64, 729)]
```

```python3
>>> dp.Pipeline(
        dp.Filter(lambda x : x > 1),
        dp.Filter(lambda x : all(x % idx != 0 for idx in range(2, x))),
    ).transform(numbers)
[2, 3, 5, 7]
```

You can find more examples <a href="https://github.com/ermshaua/daproli/tree/master/daproli/examples">here</a>. 
