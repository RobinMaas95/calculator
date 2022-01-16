"""Simple calculator that can handle addition, subtraction, multiplication and division."""

import string
import re
import operator
from typing import List, Union

OPERATIONS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


def get_user_input():
    """Get user input."""
    user_input = input("Enter your term (q to exit): ")
    if user_input == "q":
        return None
    return user_input


def push_into_list(push_object: Union[List, str], target_list: list, depth: int):
    """
    Helper function: Push the object into the list.

    Parameters
    ----------
    push_object : Union[List, str]
        Object to be pushed into the list.
    target_list : list
        The list to be pushed into.
    depth : int
        Depth to iterate while inserting.
    """
    while depth:
        target_list = target_list[-1]
        depth -= 1

    target_list.append(push_object)


def parse_parentheses(input_string: str) -> list:
    """
    Parse over the input string an return it as a list with sublist.

    The sublist represent a paranetheses term, normal strings represent
    terms outside of parentheses.

    Parameters
    ----------
    input_string : str
        String to be parsed.

    Returns
    -------
    list
        List with sublists. Each sublist represents a term that was inside parentheses.

    Raises
    ------
    ValueError
        Raised when a parentheses is not closed.

    """
    groups: List[List[Union[List, str]]] = []
    depth = 0

    try:
        for char in input_string:
            if char == "(":
                push_into_list([], groups, depth)
                depth += 1
            elif char == ")":
                depth -= 1
            else:
                push_into_list(char, groups, depth)
    except IndexError as index_error:
        raise ValueError("Parentheses mismatch") from index_error

    if depth > 0:
        raise ValueError("Parentheses mismatch")
    return groups


def resolve_parentheses(parsed_input: list) -> list:
    """
    Resolve all terms inside parentheses.

    Iterate over the list and resolve all terms inside parentheses. Solve nested terms
    recursively.

    Parameters
    ----------
    parsed_input : list
        String to be solved

    Returns
    -------
    str
        String that contains all terms that are not inside parentheses plus the result of
        the terms inside parentheses in the original order.
    """
    parentheses_strings: List[Union[str, float]] = []
    for parse_section in parsed_input:
        if "[" in str(parse_section)[1:-1]:
            parse_section = resolve_parentheses(parse_section)
            parse_section = [str(i) for i in parse_section]
            calculation_str = "".join(parse_section)
            if calculation_str in ["+", "-", "*", "/"]:
                parentheses_strings.append(calculation_str)
            else:
                calculation_str = resolve_division_multiplication(calculation_str)
                parentheses_strings.append(eval_math_expr(calculation_str))
        else:
            parse_section = [str(i) for i in parse_section]
            calculation_str = "".join(parse_section)
            if calculation_str in ["+", "-", "*", "/"]:
                parentheses_strings.append(calculation_str)
            else:
                calculation_str = resolve_division_multiplication(calculation_str)
                parentheses_strings.append(eval_math_expr(calculation_str))
    return parentheses_strings


def resolve_division_multiplication(parsed_input: str) -> str:
    """
    Resolve all divisions and multiplications inside the string.

    Parameters
    ----------
    parsed_input : str
        Input string to be resolved.

    Returns
    -------
    str
        String with all additions and subtractions and the resolved multiplication and division
        in the original order.
    """
    if ("/" in parsed_input) or ("*" in parsed_input):
        updated_input = ""
        subterms = re.split(r"[-\+]", parsed_input)
        for subterm in subterms:
            if len(subterm) == 1:
                updated_input += subterm
                if len(parsed_input) != 1:
                    updated_input = updated_input + parsed_input[1]
                    parsed_input = parsed_input[2:]
            else:
                # Evaluate subterm (must include division or multiplication)
                result = eval_math_expr(subterm)
                updated_input += str(result)
                if len(subterm) != len(parsed_input):
                    updated_input = updated_input + parsed_input[len(subterm)]
                    parsed_input = parsed_input[len(subterm) + 1 :]
        return updated_input
    return parsed_input


def get_number(input_string: str) -> tuple:
    """
    Return a float out of the input string.

    Parameters
    ----------
    input_string : str
        String with the number.

    Returns
    -------
    tuple
        The number and the length of the number in the string.
    """
    number_sting = ""
    if input_string[0] == "-":
        number_sting += "-"
        input_string = input_string[1:]
    for character in input_string:
        if not character.isdigit():
            if character == ".":
                number_sting += "."
            else:
                break
        else:
            number_sting += character
    return (float(number_sting), len(number_sting))


def perform_operation(operator_sign: str, num1: float, num2: float) -> float:
    """
    Perform the operation on the two numbers.

    Parameters
    ----------
    operator_sign : str
        Plus, minus, multiplication or division.
    num1 : float
        Number 1.
    num2 : float
        Number 2.

    Returns
    -------
    float
        Result of the operation.

    Raises
    ------
    ValueError
        Raise when the operator is not supported.
    """
    operation_object = OPERATIONS.get(operator_sign, None)
    if operation_object is not None:
        return operation_object(num1, num2)
    raise ValueError(f"Not supported operator: {operator_sign}")


def eval_math_expr(input_string: str) -> float:
    """
    Perform the resolving of a term.

    Only supports addition, subtraction, multiplication and division.
    Calculates the result from left to right. Parentheses and multiplication/division
    must be sorted out before this function is called (e.g. by calling this function
    with the corresponding subterms first).

    Parameters
    ----------
    input_string : str
        String to be resolved.

    Returns
    -------
    float
        Result of the term.
    """
    while True:
        number1, end_number1 = get_number(input_string)
        input_string = input_string[end_number1:]
        if input_string == "":
            return number1
        operater_sign = input_string[0]
        input_string = input_string[1:]
        number2, end_number2 = get_number(input_string)
        number1 = perform_operation(operater_sign, number1, number2)
        input_string = str(number1) + input_string[end_number2:]


def main():
    """Main function."""
    user_input = get_user_input()
    if user_input is None:
        print("Bye!")
        return
    print(f"You entered: {user_input}")
    user_input = user_input.translate({ord(c): None for c in string.whitespace})
    user_input = (
        "(" + user_input + ")"
    )  # It was easier to add parentheses to the input instead of creating a new function for
    # terms without any parentheses

    parenthesis_list = parse_parentheses(user_input)
    result = resolve_parentheses(parenthesis_list)[0]

    print(f"The result is: {result}")

    return result  # For testing


if __name__ == "__main__":
    main()
