def keep(x):
    return x


def ignore(x):
    return None


def include_only(*names: str):
    def func(x):
        return {name: x[name] for name in names}

    return func


def exclude_params(*names: str):
    def func(x):
        for name in names:
            del x[name]
        return x

    return func
