import calculator.calculator as calc
from parametrization import Parametrization
import pytest
import re


def test_single_value(mocker):
    mocker.patch("builtins.input", lambda _: "1")
    result = calc.main()
    assert result == 1


@Parametrization.parameters("user_input", "expected_result")
@Parametrization.case("addition", "10 + 2", 12.0)
@Parametrization.case("subtraction", "1 - 2", -1.0)
@Parametrization.case("multiplication", "1 * 2", 2.0)
@Parametrization.case("division", "1 / 2", 0.5)
def test_no_parentheses_no_order(mocker, user_input, expected_result):
    mocker.patch("builtins.input", lambda _: user_input)
    result = calc.main()
    assert result == expected_result


@Parametrization.parameters("user_input", "expected_result")
@Parametrization.case("addition", "(1 + 2) +1", 4.0)
@Parametrization.case("subtraction", "(1 - 2) - 1", -2.0)
@Parametrization.case("multiplication", "(1 * 2) * 3", 6.0)
@Parametrization.case("division", "(10 / 2) / 2", 2.5)
def test_parentheses_no_order(mocker, user_input, expected_result):
    mocker.patch("builtins.input", lambda _: user_input)
    result = calc.main()
    assert result == expected_result


@Parametrization.parameters("user_input", "expected_result")
@Parametrization.case("single_md_w_as_left_to_right", "18/3 - 1 + 2", 7.0)
@Parametrization.case("single_md_w_as_shuffeld", "1 - 18/3 + 2", -3.0)
@Parametrization.case("multiple_md_w_as_left_to_right", "18/3 + 1 + 2 - 18/3", 3.0)
def test_no_parentheses_mixed(mocker, user_input, expected_result):
    mocker.patch("builtins.input", lambda _: user_input)
    result = calc.main()
    assert result == expected_result


def test_multiple_parentheses_mixed(mocker):
    mocker.patch("builtins.input", lambda _: "((10 + 2) * 2) + ((1 + 2) / 3)")
    result = calc.main()
    assert result == 25.0


def test_term_from_task(mocker):
    mocker.patch("builtins.input", lambda _: "(10 + 8) * 3/8 +3")
    result = calc.main()
    assert result == 9.75


def test_not_supported_operator(mocker):
    mocker.patch("builtins.input", lambda _: "1 ^ 2")
    with pytest.raises(ValueError, match=re.escape("Not supported operator: ^")):
        calc.main()
