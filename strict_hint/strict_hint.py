from inspect import signature


class StrictHint(object):
    def __init__(self):
        pass

    def __call__(self, wrapped):
        def wrapper(*args, **kwargs):
            sig = signature(wrapped)

            self.__validate_args(wrapped, sig, args)
            result = wrapped(*args, **kwargs)
            self.__validate_return(wrapped, sig, result)

            return result

        return wrapper

    def __validate_args(self, func, sig, args):
        args = dict(zip(sig.parameters.keys(), args))
        if not args:
            return

        for param_name, param in sig.parameters.items():
            if param.annotation == param.empty:
                continue

            if not self.__matches_hint(
                    args[param_name], param.annotation, param.default
            ):
                raise TypeError(
                    'Argument %s passed to %s must be an instance of %s,'
                    ' %s given' % (
                        param_name, self.__func_name(func), param.annotation,
                        type(args[param_name])
                    )
                )

    def __validate_return(self, func, sig, result):
        if sig.return_annotation == sig.empty:
            return

        if not self.__matches_hint(result, sig.return_annotation):
            raise TypeError(
                "Value returned by %s must be an instance of %s,"
                " %s returned" % (
                    self.__func_name(func), sig.return_annotation, type(result)
                )
            )

    def __matches_hint(self, value, expected, default=None):
        return isinstance(value, expected) or value == default

    def __func_name(self, func):
        return func.__qualname__.split('.<locals>.', 1)[-1]
