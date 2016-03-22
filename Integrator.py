import differentiation


def integrate(equ):
    """
    Works out what kind of equation the given segment is so it can be differentiated
    :param equ:
    :return:
    """
    if "x" in equ:
        return "1/2x^2"
    else:
        return constant_equation(equ)


def constant_equation(funct):
    coeff = differentiation.parse_coefficient(funct)
    return coeff + "x"


def tests():
    print()
    assert "x" == "1/2x^2"
    assert "1" == "x"
    assert "5" == "5x"
