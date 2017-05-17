from typing import Dict, Tuple, List

from pytest import raises

from strict_hint import strict
from strict_hint.strict_hint import StrictHint


class TestArgsWithPrimitiveAnnotation:
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

    def test_accept_type_from_annotation_user_defined_class(self):
        @strict
        def func(r: StrictHint):
            return r

        assert isinstance(func(StrictHint()), StrictHint)

    def test_accept_default_value(self):
        @strict
        def func(r: int = 1):
            return r

        assert func(1) == 1

    def test_accept_default_value_even_when_different_type(self):
        @strict
        def func(r: int = None):
            return r

        assert func(None) is None

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
