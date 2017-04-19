from types import FunctionType

from pytest import raises

from strict_hint.strict_hint import StrictHint
from tests import Bar
from tests import Foo


def test_accept_any_arg_when_no_annotation():
    @StrictHint()
    def func(r):
        return r

    assert func(1) == 1
    assert func('lorem ipsum') == 'lorem ipsum'


def test_accept_arg_with_value_matching_annotation():
    @StrictHint()
    def func(r: int):
        return r

    assert func(1) == 1


def test_accept_arg_with_value_matching_standard_interpreter_type():
    @StrictHint()
    def func(r: FunctionType):
        return r

    assert func(func) == func


def test_raise_type_error_arg_value_does_not_match_annotation():
    @StrictHint()
    def func(r: int):
        return r

    with raises(TypeError) as e:
        func('lorem ipsum')

    assert str(e.value) == "Argument r passed to func must be an instance of" \
                           " <class 'int'>, <class 'str'> given"


def test_accept_default_value_even_when_different_type():
    @StrictHint()
    def func(r: int = 'foo'):
        return r

    assert func() == 'foo'


def test_accept_value_equal_to_default_value_when_different_type():
    @StrictHint()
    def func(r: int = 'foo'):
        return r

    assert func('foo') == 'foo'


def test_accept_value_when_matches_one_of_annotated_types():
    @StrictHint()
    def func(a: (int, str)):
        pass

    func(1)
    func('lorem ipsum')


def test_raise_type_error_when_value_is_not_in_annotated_tuple():
    @StrictHint()
    def func(r: (int, str)):
        return r

    with raises(TypeError) as e:
        func([])

    assert str(
        e.value) == "Argument r passed to func must be an instance of" \
                    " (<class 'int'>, <class 'str'>), <class 'list'> given"


def test_func_alias_raise_type_error_when_value_is_not_a_list_of():
    @StrictHint()
    def func(r: [str]):
        return r

    with raises(TypeError) as e:
        func(1)

    assert str(
        e.value) == "Argument r passed to func must be an instance of" \
                    " [<class 'str'>], <class 'int'> given"


def test_accepts_any_return_value_if_no_annotation():
    @StrictHint()
    def func(r):
        return r

    assert func(1) == 1
    assert func('lorem ipsum') == 'lorem ipsum'


def test_accept_return_value_matching_annotation():
    @StrictHint()
    def func(r) -> str:
        return r

    assert func('lorem ipsum') == 'lorem ipsum'


def test_accept_return_value_matching_standard_interpreter_type():
    @StrictHint()
    def func(r) -> FunctionType:
        return r

    assert func(func) == func


def test_accept_return_value_matching_annotated_tuple():
    @StrictHint()
    def func(r) -> (int, str):
        return r

    assert func(1) == 1
    assert func('lorem ipsum') == 'lorem ipsum'


def test_raise_error_when_value_does_not_match_annotation():
    @StrictHint()
    def func(r) -> str:
        return r

    with raises(TypeError) as e:
        func(1)

    assert str(e.value) == "Value returned by func must be an instance of" \
                           " <class 'str'>, <class 'int'> returned"


def test_raise_error_when_value_does_not_match_annoted_tuple():
    @StrictHint()
    def func(r) -> (int, str):
        return r

    with raises(TypeError) as e:
        func([])

    assert str(
        e.value) == "Value returned by func must be an instance of" \
                    " (<class 'int'>, <class 'str'>), <class 'list'> returned"


def test_raise_error_when_value_is_not_list_of():
    @StrictHint()
    def func(r) -> [str]:
        return r

    with raises(TypeError) as e:
        func(1)

    assert str(
        e.value) == "Value returned by func must be an instance of" \
                    " [<class 'str'>], <class 'int'> returned"


def test_accept_user_defined_class():
    @StrictHint()
    def func(r: Foo) -> Foo:
        return r

    assert func(Foo())


def test_accept_user_defined_class_inheritance():
    @StrictHint()
    def func(r: object) -> object:
        return r

    assert func(Foo())


def test_raises_error_when_different_user_defined_class_passed():
    @StrictHint()
    def func(r: Foo) -> Foo:
        return r

    with raises(TypeError) as e:
        func(Bar())

    assert str(e.value) == "Argument r passed to func must be an instance of" \
                           " <class 'tests.Foo'>, <class 'tests.Bar'> given"


def test_raises_error_when_required_argument_omitted():
    @StrictHint()
    def func(r: Foo) -> Foo:
        return r

    with raises(TypeError) as e:
        func()

    assert str(e.value) == "func() missing 1 required positional argument: 'r'"


def test_raises_error_when_optional_argument_omitted():
    @StrictHint()
    def func(a, r: Foo = 2) -> tuple:
        return a, r

    assert func(1) == (1, 2)


def test_raised_error_includes_class_name():
    class Yada(object):
        @StrictHint()
        def func(self, r: Foo) -> Foo:
            return r

    with raises(TypeError) as e:
        Yada().func(Bar())

    assert str(e.value) == "Argument r passed to Yada.func must be an " \
                           "instance of <class 'tests.Foo'>, " \
                           "<class 'tests.Bar'> given"
