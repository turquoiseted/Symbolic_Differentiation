import differentiation


def integrate(equ):
    """
    Works out what kind of equation the given segment is so it can be differentiated
    :param equ:
    :return:
    """
    if "x" in equ:
        return polynomial_equation(equ)
    else:
        return constant_equation(equ)


def constant_equation(funct):
    """
    Returns the integrated version of a constant
    :param funct:
    :return:
    """
    return funct + "x"


def polynomial_equation(funct):
    """
    Returns the integrated version of any polynomial
    :param funct:
    :return:
    """
    coeff = str(differentiation.parse_coefficient(funct))
    if "^" not in funct:
        divisor = "1"
    else:
        divisor_location = str(funct.index("^") + 1)
        divisor = funct[divisor_location:]
    if divisor == "-1":
        pass
    else:
        divisor = str(int(divisor) + 1)
        coeff += "/" + divisor
        return coeff + "x^" + str(divisor)


def tests():
    print()
    assert integrate("x") == "1/2x^2"
    assert integrate("1") == "1x"
    assert integrate("5") == "5x"
    assert integrate("2x") == "2/2x^2"

tests()
