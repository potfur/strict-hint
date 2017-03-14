from types import FunctionType

from pytest import raises

from strict_hint import strict
from tests import Foo, Bar


def test_func_alias_func_alias_accept_any_arg_when_no_annotation():
    @strict
    def func(r):
        return r

    assert func(1) == 1
    assert func('lorem ipsum') == 'lorem ipsum'


def test_func_alias_accept_arg_with_value_matching_annotation():
    @strict
    def func(r: int):
        return r

    assert func(1) == 1


def test_func_alias_accept_arg_with_value_matching_standard_interpreter_type():
    @strict
    def func(r: FunctionType):
        return r

    assert func(func) == func


def test_func_alias_raise_type_error_arg_value_does_not_match_annotation():
    @strict
    def func(r: int):
        return r

    with raises(TypeError) as e:
        func('lorem ipsum')

    assert str(e.value) == "Argument r passed to func must be an instance of" \
                           " <class 'int'>, <class 'str'> given"


def test_func_alias_accept_default_value_even_when_different_type():
    @strict
    def func(r: int = 'foo'):
        return r

    assert func() == 'foo'


def test_func_alias_accept_value_equal_to_default_value_when_different_type():
    @strict
    def func(r: int = 'foo'):
        return r

    assert func('foo') == 'foo'


def test_func_alias_accept_value_when_matches_one_of_annotated_types():
    @strict
    def func(a: (int, str)):
        pass

    func(1)
    func('lorem ipsum')


def test_func_alias_raise_type_error_when_value_is_not_in_annotated_tuple():
    @strict
    def func(r: (int, str)):
        return r

    with raises(TypeError) as e:
        func([])

    assert str(
        e.value) == "Argument r passed to func must be an instance of" \
                    " (<class 'int'>, <class 'str'>), <class 'list'> given"


def test_func_alias_accepts_any_return_value_if_no_annotation():
    @strict
    def func(r):
        return r

    assert func(1) == 1
    assert func('lorem ipsum') == 'lorem ipsum'


def test_func_alias_accept_return_value_matching_annotation():
    @strict
    def func(r) -> str:
        return r

    assert func('lorem ipsum') == 'lorem ipsum'


def test_func_alias_accept_return_value_matching_standard_interpreter_type():
    @strict
    def func(r) -> FunctionType:
        return r

    assert func(func) == func


def test_func_alias_accept_return_value_matching_annotated_tuple():
    @strict
    def func(r) -> (int, str):
        return r

    assert func(1) == 1
    assert func('lorem ipsum') == 'lorem ipsum'


def test_func_alias_raise_error_when_value_does_not_match_annotation():
    @strict
    def func(r) -> str:
        return r

    with raises(TypeError) as e:
        func(1)

    assert str(e.value) == "Value returned by func must be an instance of" \
                           " <class 'str'>, <class 'int'> returned"


def test_func_alias_raise_error_when_value_does_not_match_annoted_tuple():
    @strict
    def func(r) -> (int, str):
        return r

    with raises(TypeError) as e:
        func([])

    assert str(
        e.value) == "Value returned by func must be an instance of" \
                    " (<class 'int'>, <class 'str'>), <class 'list'> returned"


def test_func_alias_accept_user_defined_class():
    @strict
    def func(r: Foo) -> Foo:
        return r

    assert func(Foo())


def test_func_alias_accept_user_defined_class_inheritance():
    @strict
    def func(r: object) -> object:
        return r

    assert func(Foo())


def test_func_alias_raises_error_when_different_user_defined_class_passed():
    @strict
    def func(r: Foo) -> Foo:
        return r

    with raises(TypeError) as e:
        func(Bar())

    assert str(e.value) == "Argument r passed to func must be an instance of" \
                           " <class 'tests.Foo'>, <class 'tests.Bar'> given"


def test_raises_error_when_required_argument_omitted():
    @strict
    def func(r: Foo) -> Foo:
        return r

    with raises(TypeError) as e:
        func()

    assert str(e.value) == "func() missing 1 required positional argument: 'r'"


def test_raised_error_includes_class_name():
    class Yada(object):
        @strict
        def func(self, r: Foo) -> Foo:
            return r

    with raises(TypeError) as e:
        Yada().func(Bar())

    assert str(e.value) == "Argument r passed to Yada.func must be an instance of" \
                           " <class 'tests.Foo'>, <class 'tests.Bar'> given"