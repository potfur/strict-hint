from functools import wraps
from inspect import signature, Parameter


class TypeHintError(TypeError):
    pass


class ArgumentTypeHintError(TypeHintError):
    def __init__(self, argument_name, func_name, expected_type, given_type):
        super().__init__(
            'Argument %s passed to %s must be an instance of %s, %s given' % (
                argument_name, func_name, expected_type, given_type
            )
        )


class ReturnValueTypeHintError(TypeHintError):
    def __init__(self, func_name, expected_type, given_type):
        super().__init__(
            "Value returned by %s must be an instance of %s, %s returned" % (
                func_name, expected_type, given_type
            )
        )


class StrictHint(object):
    def __call__(self, func):
        self.func = func
        self.sig = signature(func)

        @wraps(self.func)
        def wrapper(*args, **kwargs):
            self.__assert_args(args)
            self.__assert_kwargs(kwargs)
            result = self.func(*args, **kwargs)
            self.__assert_return(result)

            return result

        return wrapper

    def __assert_args(self, args: tuple):
        args = dict(zip(self.sig.parameters.keys(), args))
        if not args:
            return

        for param in args.keys():
            self.__assert_param(param, self.sig.parameters[param], args)

    def __assert_kwargs(self, kwargs: dict):
        if not kwargs:
            return

        for param in kwargs.keys():
            self.__assert_param(param, self.sig.parameters[param], kwargs)

    def __assert_param(self, name: str, param: Parameter, values: dict):
        if param.annotation == param.empty:
            return

        try:
            val = values[name]
        except KeyError:
            val = param.default

        if not self.__matches_hint(val, param.annotation, param.default):
            raise ArgumentTypeHintError(
                name,
                self.__func_name(self.func),
                self.__type_name(param.annotation),
                type(values[name])
            )

    def __assert_return(self, result: Parameter):
        if self.sig.return_annotation == self.sig.empty:
            return

        if not self.__matches_hint(result, self.sig.return_annotation):
            raise ReturnValueTypeHintError(
                self.__func_name(self.func),
                self.sig.return_annotation,
                type(result)
            )

    def __matches_hint(self, value, expected, default=None):
        if type(expected) == list:
            expected = list
        elif hasattr(expected, '__origin__'):
            expected = self.__simplify_type(expected)
        elif hasattr(expected, '__supertype__'):
            expected = expected.__supertype__

        try:
            return value == default or isinstance(value, expected)
        except TypeError:
            return issubclass(value, expected)

    def __simplify_type(self, expected):
        while expected.__origin__ is not None:
            expected = expected.__origin__
        return expected.__extra__

    def __func_name(self, func):
        return func.__qualname__.split('.<locals>.', 1)[-1]

    def __type_name(self, t):
        if hasattr(t, '__supertype__'):
            return t.__name__
        return t
