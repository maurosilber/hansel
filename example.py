from hansel import Function, hansel
from hansel.filters import exclude_params, ignore, include_only


def inner(xi, yi):
    return xi + yi


def outer(xo):
    return inner(xo, inner(xo, xo))


conditions = {
    "Trace outer": [Function(outer)],
    "Trace inner": [Function(inner)],
    "Trace inner excluding xi and return": [
        Function(inner, exclude_params("xi"), ignore)
    ],
    "Trace inner including only xi and wrapping return in a tuple": [
        Function(inner, param_filter=include_only("xi"), return_filter=lambda x: (x,))
    ],
    "Trace both": [Function(inner), Function(outer)],
}


for msg, functions in conditions.items():
    print(msg)
    print("=" * (len(msg) + 2))

    with hansel(functions) as log:
        outer(1)

    print(log)
    print()
