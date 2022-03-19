# Hansel: function call logging

*Note: it's a proof of concept.*

Hansel uses `sys.setprofile` to intercept functions calls and log parameters and return values of specified functions. It can filter and/or transform parameters and return values before saving.

*Note: it might only work in CPython.*

## Example

Suppose we have the following functions defined:

```python
>>> def inner(xi, yi):
...     return xi + yi
... 
>>> def outer(xo):
...     return inner(xo, inner(xo, xo))
...
```

To log the function calls, we can use `hansel` as follows:

```python
>>> from hansel import hansel, Function
>>>
>>> functions = [Function(outer)]
>>> with hansel(functions) as log:
...     outer(1)
... 
3
>>> log
['outer', {'xo': 1}, 3]
```

which only logs the outer funciton.

If we wanted to log the inner function:

```python
>>> functions = [Function(inner)]
>>> with hansel(functions) as log:
...     outer(1)
... 
3
>>> log
['inner', {'xi': 1, 'yi': 1}, 2, 'inner', {'xi': 1, 'yi': 2}, 3]
```

If we wanted to exclude a parameter and ignore the return:

```python
>>> from hansel.filters import exclude_params, ignore
>>>
>>> functions = [Function(inner, exclude_params("xi"), ignore)]
>>> with hansel(functions) as log:
...     outer(1)
... 
3
>>> log
['inner', {'yi': 1}, None, 'inner', {'yi': 2}, None]
```

or include only a parameter:

```python
>>> from hansel.filters import include_only
>>>
>>> functions = [Function(inner, param_filter=include_only("xi"), return_filter=lambda x: (x,))]
>>> with hansel(functions) as log:
...     outer(1)
... 
3
>>> log
['inner', {'xi': 1}, (2,), 'inner', {'xi': 1}, (3,)]
```

or log multiple functions:

```python
>>> functions = [Function(inner), Function(outer)]
>>> with hansel(functions) as log:
...     outer(1)
... 
3
>>> log
['outer', {'xo': 1}, 'inner', {'xi': 1, 'yi': 1}, 2, 'inner', {'xi': 1, 'yi': 2}, 3, 3]
```
