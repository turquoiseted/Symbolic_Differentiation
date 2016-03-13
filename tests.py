import differentiation

#####TESTS#####


def tests():
    print(differentiation.dif("y = x^2*x"))

    # test 0.5 - values
    assert differentiation.dif("y = 1") == "dy/dx = 0"
    # test 1 - parse equ, very simple linear
    assert differentiation.parse_equation("y = x") == ["y", " ", "=", " ", "x"]
    assert differentiation.dif("y = x") == "dy/dx = 1"
    assert differentiation.dif("y = x + 2") == "dy/dx = 1"  # ammended
    # test 2 - squares
    assert differentiation.parse_equation("x^2") == ["x^2"]
    assert differentiation.dif("y = x^2") == "dy/dx = 2x"
    # test 3 - coefficents & linear
    assert differentiation.dif("y = 2x") == "dy/dx = 2"
    # test 4 - linear equation moved to a funct
    assert differentiation.linear_equation("x") == "1"
    assert differentiation.linear_equation("20x") == "20"
    # test 5 - basic polynomials
    assert differentiation.polynomial_equation("x^2") == "2x"
    assert differentiation.polynomial_equation("2x^2") == "4x"
    assert differentiation.polynomial_equation("x^3") == "3x^2"
    assert differentiation.polynomial_equation("25x^4") == "100x^3"
    # text 5.5 - more adv polynomials
    assert differentiation.dif("y = x^3") == "dy/dx = 3x^2"
    assert differentiation.dif("y = 3x^5 + 2x + 5x^2") == "dy/dx = 15x^4 + 2 + 10x"
    # test 6 - exponents
    assert differentiation.dif("y = e^x") == "dy/dx = e^x"
    # test 7 - more adv exponents
    assert differentiation.dif("y = e^2x^2") == "dy/dx = 4xe^2x^2"
    assert differentiation.dif("y = 3e^x") == "dy/dx = 3e^x"
    assert differentiation.dif("y = 3e^2x^2") == "dy/dx = 12xe^2x^2"
    # test 8 - basic trig
    assert differentiation.dif("y = cos(x)") == "dy/dx = -sin(x)"
    assert differentiation.dif("y = sin(x)") == "dy/dx = cos(x)"
    # test 9 - more adv trig
    assert differentiation.dif("y = cos(2x)") == "dy/dx = -2sin(2x)"
    assert differentiation.dif("y = sin(2x)") == "dy/dx = 2cos(2x)"
    assert differentiation.dif("y = 3sin(x^2)") == "dy/dx = 6xcos(x^2)"
    # test 10 - parse output
    assert differentiation.dif("y = 2x + 2") == "dy/dx = 2"
    assert differentiation.dif("y = 3sin(x^2) + 6") == "dy/dx = 6xcos(x^2)"
    # test 11 - negative powers
    assert differentiation.dif("y = x^-1") == "dy/dx = -1x^-2"
    # assert dif("y = x + x^-1") == "dy/dx = 1 + -1x^-2" #this needs to be better output
    assert differentiation.dif("y = x + x^-1") == "dy/dx = 1 - x^-2"
    # test 11.5 - output gathers like terms
    # assert dif("y = x^2 + x^2") == "dy/dx = 4x"
    # assert dif("y = x + x") == "dy/dx = 2"
    # test 12 - chain rule, multiple x's
    assert differentiation.dif("y = x^2*x") == 'dy/dx = 2x*x + x^2'

    # assorted tests
    assert differentiation.parse_output("dy/dx = 1x") == "dy/dx = x"
