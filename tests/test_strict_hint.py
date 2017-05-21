from types import FunctionType
from typing import Dict, Tuple, List, NewType

from pytest import raises

from strict_hint import strict
from strict_hint.strict_hint import StrictHint


class TestArgsWithPrimitiveAnnotation:
    def test_accept_no_arguments(self):
        @strict
        def func():
            return ''

        assert func() == ''

    def test_accept_when_no_annotation(self):
        @strict
        def func(r):
            return r

        assert func(1) == 1

    def test_accept_type_from_annotation(self):
        @strict
        def func(r: int):
            return r

        assert func(1) == 1

    def test_accept_type_from_annotation_tuple(self):
        @strict
        def func(r: (int, str)):
            return r

        assert func(1) == 1
        assert func('one') == 'one'

    def test_accept_type_from_annotation_list_of(self):
        @strict
        def func(r: [int]):
            return r

        assert func([1]) == [1]

    def test_accept_type_from_annotation_interpreter_type(self):
        @strict
        def func(r: FunctionType):
            return r

        assert func(func) == func

    def test_accept_type_from_annotation_user_defined_class(self):
        @strict
        def func(r: StrictHint):
            return r

        assert isinstance(func(StrictHint()), StrictHint)

    def test_accept_default_value(self):
        @strict
        def func(r: int = 1):
            return r

        assert func() == 1

    def test_accept_default_value_even_when_different_type(self):
        @strict
        def func(r: int = 'foo'):
            return r

        assert func() == 'foo'

    def test_raise_error_when_type_different(self):
        @strict
        def func(r: int):
            return r

        with raises(TypeError) as e:
            func('foo')

        assert str(e.value) == "Argument r passed to func must be an " \
                               "instance of <class 'int'>, <class 'str'> given"

    def test_raise_error_when_type_not_in_tuple(self):
        @strict
        def func(r: (int, float)):
            return r

        with raises(TypeError) as e:
            func('foo')

        assert str(e.value) == "Argument r passed to func must be an " \
                               "instance of (<class 'int'>, <class 'float'>)" \
                               ", <class 'str'> given"

    def test_raise_error_when_type_not_a_list_of(self):
        @strict
        def func(r: [int]):
            return r

        with raises(TypeError) as e:
            func('foo')

        assert str(e.value) == "Argument r passed to func must be an " \
                               "instance of [<class 'int'>], <class 'str'> " \
                               "given"

    def test_raise_error_when_type_not_a_interpreter_type(self):
        @strict
        def func(r: FunctionType):
            return r

        with raises(TypeError) as e:
            func('foo')

        assert str(e.value) == "Argument r passed to func must be an " \
                               "instance of <class 'function'>, " \
                               "<class 'str'> given"

    def test_raise_error_when_type_not_a_user_defined_class(self):
        @strict
        def func(r: StrictHint):
            return r

        with raises(TypeError) as e:
            func('foo')

        assert str(e.value) == "Argument r passed to func must be an " \
                               "instance of " \
                               "<class 'strict_hint.strict_hint.StrictHint'>" \
                               ", <class 'str'> given"


class TestKwargsWithPrimitiveAnnotation:
    def test_accept_when_no_annotation(self):
        @strict
        def func(r, *args, o=False):
            return r, o

        assert func(1, o=True) == (1, True)

    def test_accept_type_from_annotation(self):
        @strict
        def func(r, *args, o: bool = False):
            return r, o

        assert func(1, o=True) == (1, True)

    def test_accept_type_from_annotation_tuple(self):
        @strict
        def func(r, *args, o: (int, float) = 0):
            return r, o

        assert func(1, o=1) == (1, 1)

    def test_accept_type_from_annotation_list_of(self):
        @strict
        def func(r, *args, o: [int] = None):
            return r, o

        assert func(1, o=[0]) == (1, [0])

    def test_accept_type_from_annotation_interpreter_type(self):
        @strict
        def func(r, *args, o: FunctionType = None):
            return r, o

        assert func(1, o=func) == (1, func)

    def test_accept_type_from_annotation_user_defined_class(self):
        @strict
        def func(r, *args, o: StrictHint = None):
            return r, o

        assert isinstance(func(1, o=StrictHint())[1], StrictHint)

    def test_accept_default_value(self):
        @strict
        def func(r, *args, o: int = 0):
            return r, o

        assert func(1) == (1, 0)

    def test_accept_default_value_even_when_different_type(self):
        @strict
        def func(r, *args, o: float = 'foo'):
            return r, o

        assert func(1) == (1, 'foo')

    def test_raise_error_when_type_different(self):
        @strict
        def func(r, *args, o: bool = False):
            return r, o

        with raises(TypeError) as e:
            func(1, o='foo')

        assert str(e.value) == "Argument o passed to func must be an " \
                               "instance of <class 'bool'>, " \
                               "<class 'str'> given"

    def test_raise_error_when_type_not_in_tuple(self):
        @strict
        def func(r, *args, o: (int, float) = 0):
            return r, o

        with raises(TypeError) as e:
            func(1, o='foo')

        assert str(e.value) == "Argument o passed to func must be an " \
                               "instance of (<class 'int'>, <class 'float'>)" \
                               ", <class 'str'> given"

    def test_raise_error_when_type_not_a_list_of(self):
        @strict
        def func(r, *args, o: [int] = 0):
            return r, o

        with raises(TypeError) as e:
            func(1, o='foo')

        assert str(e.value) == "Argument o passed to func must be an " \
                               "instance of [<class 'int'>], " \
                               "<class 'str'> given"

    def test_raise_error_when_type_not_a_interpreter_type(self):
        @strict
        def func(r, *args, o: FunctionType = 0):
            return r, o

        with raises(TypeError) as e:
            func(1, o='foo')

        assert str(e.value) == "Argument o passed to func must be an " \
                               "instance of <class 'function'>, " \
                               "<class 'str'> given"

    def test_raise_error_when_type_not_a_user_defined_class(self):
        @strict
        def func(r, *args, o: StrictHint = 0):
            return r, o

        with raises(TypeError) as e:
            func(1, o='foo')

        assert str(e.value) == "Argument o passed to func must be an " \
                               "instance of " \
                               "<class 'strict_hint.strict_hint.StrictHint'>" \
                               ", <class 'str'> given"


class TestReturnValueWithPrimitiveAnnotation:
    def test_accept_type_from_annotation(self):
        @strict
        def func(r) -> int:
            return r

        assert func(1) == 1

    def test_accept_type_from_annotation_tuple(self):
        @strict
        def func(r) -> (int, str):
            return r

        assert func(1) == 1
        assert func('one') == 'one'

    def test_accept_type_from_annotation_list_of(self):
        @strict
        def func(r) -> [int]:
            return r

        assert func([1]) == [1]

    def test_accept_type_from_annotation_interpreter_type(self):
        @strict
        def func(r) -> FunctionType:
            return r

        assert func(func) == func

    def test_accept_type_from_annotation_user_defined_class(self):
        @strict
        def func(r) -> StrictHint:
            return r

        assert isinstance(func(StrictHint()), StrictHint)

    def test_raise_error_when_type_different(self):
        @strict
        def func(r) -> int:
            return r

        with raises(TypeError) as e:
            func('foo')

        assert str(e.value) == "Value returned by func must be an instance " \
                               "of <class 'int'>, <class 'str'> returned"

    def test_raise_error_when_type_not_in_tuple(self):
        @strict
        def func(r) -> (int, float):
            return r

        with raises(TypeError) as e:
            func('foo')

        assert str(e.value) == "Value returned by func must be an instance " \
                               "of (<class 'int'>, <class 'float'>), " \
                               "<class 'str'> returned"

    def test_raise_error_when_type_not_a_list_of(self):
        @strict
        def func(r) -> [int]:
            return r

        with raises(TypeError) as e:
            func('foo')

        assert str(e.value) == "Value returned by func must be an instance " \
                               "of [<class 'int'>], <class 'str'> returned"

    def test_raise_error_when_type_not_a_interpreter_type(self):
        @strict
        def func(r) -> FunctionType:
            return r

        with raises(TypeError) as e:
            func('foo')

        assert str(e.value) == "Value returned by func must be an " \
                               "instance of <class 'function'>, " \
                               "<class 'str'> returned"

    def test_raise_error_when_type_not_a_user_defined_class(self):
        @strict
        def func(r) -> StrictHint:
            return r

        with raises(TypeError) as e:
            func('foo')

        assert str(e.value) == "Value returned by func must be an instance " \
                               "of " \
                               "<class 'strict_hint.strict_hint.StrictHint'>" \
                               ", <class 'str'> returned"


class TestArgumentsWithTypingAnnotation:
    def test_accept_type_from_annotation_dict(self):
        @strict
        def func(r: Dict):
            return r

        assert func({}) == {}

    def test_accept_type_from_annotation_tuple(self):
        @strict
        def func(r: Tuple[int, str]):
            return r

        assert func((1, 'foo')) == (1, 'foo')

    def test_accept_type_from_annotation_list_of(self):
        @strict
        def func(r: List[int]):
            return r

        assert func([1]) == [1]

    def test_accept_type_from_annotation_user_defined_type(self):
        StrictHintType = NewType('StrictHintType', StrictHint)

        @strict
        def func(r: StrictHintType):
            return r

        assert isinstance(func(StrictHint()), StrictHint)

    def test_raise_error_when_type_different(self):
        @strict
        def func(r: Dict):
            return r

        with raises(TypeError) as e:
            func('foo')

        assert str(e.value) == "Argument r passed to func must be an " \
                               "instance of typing.Dict, <class 'str'> given"

    def test_raise_error_when_type_not_in_tuple(self):
        @strict
        def func(r: Tuple[int, str]):
            return r

        with raises(TypeError) as e:
            func('foo')

        assert str(e.value) == "Argument r passed to func must be an " \
                               "instance of typing.Tuple[int, str], " \
                               "<class 'str'> given"

    def test_raise_error_when_type_not_a_list_of(self):
        @strict
        def func(r: List[int]):
            return r

        with raises(TypeError) as e:
            func('foo')

        assert str(e.value) == "Argument r passed to func must be an " \
                               "instance of typing.List[int], " \
                               "<class 'str'> given"

    def test_raise_error_when_type_not_a_user_defined_class(self):
        new_type = NewType('StrictHintType', StrictHint)

        @strict
        def func(r: new_type):
            return r

        with raises(TypeError) as e:
            func('foo')

        assert str(e.value) == "Argument r passed to func must be an " \
                               "instance of StrictHintType, " \
                               "<class 'str'> given"


class TestKwargsWithTypingAnnotation:
    def test_accept_type_from_annotation_dict(self):
        @strict
        def func(r, *args, o: Dict = False):
            return r, o

        assert func(1, o={}) == (1, {})

    def test_accept_type_from_annotation_tuple(self):
        @strict
        def func(r, *args, o: Tuple[int, str] = 0):
            return r, o

        assert func(1, o=(1, 'foo')) == (1, (1, 'foo'))

    def test_accept_type_from_annotation_list_of(self):
        @strict
        def func(r, *args, o: List[int] = None):
            return r, o

        assert func(1, o=[0]) == (1, [0])

    def test_accept_type_from_annotation_user_defined_type(self):
        StrictHintType = NewType('StrictHintType', StrictHint)

        @strict
        def func(r, *args, o: StrictHintType = None):
            return r, o

        assert isinstance(func(1, o=StrictHint())[1], StrictHint)

    def test_raise_error_when_type_different(self):
        @strict
        def func(r, *args, o: Dict = None):
            return r, o

        with raises(TypeError) as e:
            func(1, o='foo')

        assert str(e.value) == "Argument o passed to func must be an " \
                               "instance of typing.Dict, <class 'str'> given"

    def test_raise_error_when_type_not_in_tuple(self):
        @strict
        def func(r, *args, o: Tuple[int, float] = 0):
            return r, o

        with raises(TypeError) as e:
            func(1, o='foo')

        assert str(e.value) == "Argument o passed to func must be an " \
                               "instance of typing.Tuple[int, float], " \
                               "<class 'str'> given"

    def test_raise_error_when_type_not_a_list_of(self):
        @strict
        def func(r, *args, o: List[int] = 0):
            return r, o

        with raises(TypeError) as e:
            func(1, o='foo')

        assert str(e.value) == "Argument o passed to func must be an " \
                               "instance of typing.List[int], " \
                               "<class 'str'> given"

    def test_raise_error_when_type_not_a_user_defined_class(self):
        StrictHintType = NewType('StrictHintType', StrictHint)

        @strict
        def func(r, *args, o: StrictHintType = 0):
            return r, o

        with raises(TypeError) as e:
            func(1, o='foo')

        assert str(e.value) == "Argument o passed to func must be an " \
                               "instance of StrictHintType, " \
                               "<class 'str'> given"


class TestReturnValueWithTypingAnnotation:
    def test_accept_type_from_annotation_dict(self):
        @strict
        def func(r) -> Dict:
            return r

        assert func({}) == {}

    def test_accept_type_from_annotation_tuple(self):
        @strict
        def func(r) -> Tuple[int, str]:
            return r

        assert func((1, 'foo')) == (1, 'foo')

    def test_accept_type_from_annotation_list_of(self):
        @strict
        def func(r) -> List[int]:
            return r

        assert func([1]) == [1]

    def test_accept_type_from_annotation_user_defined_type(self):
        StrictHintType = NewType('StrictHintType', StrictHint)

        @strict
        def func(r) -> StrictHintType:
            return r

        assert isinstance(func(StrictHint()), StrictHint)

    def test_raise_error_when_type_different(self):
        @strict
        def func(r) -> Dict:
            return r

        with raises(TypeError) as e:
            func('foo')

        assert str(e.value) == "Value returned by func must be an instance " \
                               "of typing.Dict, <class 'str'> returned"

    def test_raise_error_when_type_not_in_tuple(self):
        @strict
        def func(r: Tuple[int, str]):
            return r

        with raises(TypeError) as e:
            func('foo')

        assert str(e.value) == "Argument r passed to func must be an " \
                               "instance of typing.Tuple[int, str], " \
                               "<class 'str'> given"

    def test_raise_error_when_type_not_a_list_of(self):
        @strict
        def func(r: List[int]):
            return r

        with raises(TypeError) as e:
            func('foo')

        assert str(e.value) == "Argument r passed to func must be an " \
                               "instance of typing.List[int], " \
                               "<class 'str'> given"

    def test_raise_error_when_type_not_a_user_defined_class(self):
        new_type = NewType('StrictHintType', StrictHint)

        @strict
        def func(r: new_type):
            return r

        with raises(TypeError) as e:
            func('foo')

        assert str(e.value) == "Argument r passed to func must be an " \
                               "instance of StrictHintType, " \
                               "<class 'str'> given"
