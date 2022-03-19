from __future__ import annotations

import sys
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any

from .filters import keep


@dataclass
class Function:
    function: callable
    param_filter: callable[[dict[str, Any]], dict[str, Any]] = keep
    return_filter: callable[[Any], Any] = keep


def get_hansel(functions: dict[str, Function], stack: list):
    def hansel(frame, event, arg):
        func = functions.get(frame.f_code)
        if func is None:
            return
        elif event == "call":
            function_name = frame.f_code.co_name
            stack.append(function_name)

            params = frame.f_locals.copy()
            params = func.param_filter(params)
            stack.append(params)
        elif event == "return":
            stack.append(func.return_filter(arg))

    return hansel


@contextmanager
def hansel(functions: list[Function]):
    functions = {f.function.__code__: f for f in functions}
    output = []
    sys.setprofile(get_hansel(functions, output))
    yield output
    sys.setprofile(None)
