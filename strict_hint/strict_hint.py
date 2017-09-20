from functools import wraps
from inspect import signature, Parameter
from typing import Tuple, List, Dict, Type


class TypeHintError(TypeError):
    pass


class ArgumentTypeHintError(TypeHintError):
    def __init__(
            self, argument_name, func_name, expected_type, given_type
    ) -> None:
        super().__init__(
            'Argument %s passed to %s must be an instance of %s, %s given' % (
                argument_name, func_name, expected_type, given_type
            )
        )


class ReturnValueTypeHintError(TypeHintError):
    def __init__(
            self, func_name, expected_type, given_type
    ) -> None:
        super().__init__(
            "Value returned by %s must be an instance of %s, %s returned" % (
                func_name, expected_type, given_type
            )
        )


class StrictHint(object):
    __func = None
    __sig = None

    def __call__(self, func):
        self.__func = func
        self.__sig = signature(func)

        @wraps(self.__func)
        def wrapper(*args, **kwargs):
            self.__assert_args(args)
            self.__assert_kwargs(kwargs)
            result = self.__func(*args, **kwargs)
            self.__assert_return(result)

            return result

        return wrapper

    def __assert_args(self, args: tuple) -> None:
        argvals = dict(zip(self.__sig.parameters.keys(), args))
        if not argvals:
            return

        for param in argvals.keys():
            self.__assert_param(param, self.__sig.parameters[param], argvals)

    def __assert_kwargs(self, kwargs: dict) -> None:
        if not kwargs:
            return

        for param in kwargs.keys():
            self.__assert_param(param, self.__sig.parameters[param], kwargs)

    def __assert_param(
            self, name: str, param: Parameter, values: dict
    ) -> None:
        if param.annotation == param.empty:
            return

        val = values[name]
        if not self.__matches_hint(val, param.annotation, param.default):
            raise ArgumentTypeHintError(
                name,
                self.__func_name(self.__func),
                param.annotation,
                type(values[name])
            )

    def __assert_return(self, result: Parameter) -> None:
        if self.__sig.return_annotation == self.__sig.empty:
            return

        if not self.__matches_hint(result, self.__sig.return_annotation):
            raise ReturnValueTypeHintError(
                self.__func_name(self.__func),
                self.__sig.return_annotation,
                type(result)
            )

    def __matches_hint(self, value, expected, default=None) -> bool:
        if type(expected) == list:
            expected = list

        try:
            if expected.__module__ == 'typing':
                expected = self.__simplify_typing(expected)
        except AttributeError:
            pass

        return value == default or isinstance(value, expected)

    def __simplify_typing(self, expected) -> Type:
        if not hasattr(expected, '__name__'):
            return expected.__args__

        mapping = {
            Tuple.__name__: tuple,
            List.__name__: list,
            Dict.__name__: dict,
        }
        if expected.__name__ in mapping:
            return mapping[expected.__name__]

        if hasattr(expected, '__supertype__'):
            return expected.__supertype__

    def __func_name(self, func) -> str:
        return func.__qualname__.split('.<locals>.', 1)[-1]
