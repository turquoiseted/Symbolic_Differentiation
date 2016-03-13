"""time to differentiate"""

"""
to do list:
o parse output
    - replace +s with -s when relevant
o allow for chain rule
o allow for bracket chain rule
o do more advanced trig
o logs
"""


def dif(equ):
    """
    Takes the input and finds out which way it should be differentiated
    :param equ:
    """
    equ_array = parse_equation(equ)
    result = ""
    for x in equ_array:
        if ("sin" in x) or ("cos" in x):
            result += trig_equ(x)
        elif "e" in x:
            result += exponential_equation(x)
        elif "^" in x:
            result += polynomial_equation(x)
        elif "x" in x:
            result += linear_equation(x)
        elif x == "y":
            result += "dy/dx"
        elif x.isdigit():
            result += "0"
            # needs formatting
        else:
            result += x
    result = parse_output(result)
    return result


def trig_equ(funct):
    """
    trig
    :param funct:
    """
    if (funct[:3] == "cos") or (funct[:3] == "sin"):
        new_equ = ""
        equation = funct[4:-1]
        if "cos" in funct:
            new_equ += "-"
            if equation == "x":
                return "-sin(x)"
            new_equ += dif(equation)
            new_equ += "sin(" + equation + ")"
            return new_equ

        elif "sin" in funct:
            if equation == "x":
                return "cos(x)"
            new_equ += dif(equation)
            new_equ += "cos(" + equation + ")"
            return new_equ

    else:
        coefficient = parse_coefficient(funct)
        funct = funct[len(coefficient):]
        equation = funct[4:-1]

        if "cos" in funct:
            new_equ = "-"
            if equation == "x":
                new_equ += coefficient + "sin(x)"
                return new_equ

            bracket = dif(equation)
            new_equ += str(int(parse_coefficient(bracket)) * int(coefficient))
            new_equ += bracket[len(parse_coefficient(bracket)):]
            new_equ += "sin(" + equation + ")"
            return new_equ

        elif "sin" in funct:
            new_equ = ""
            if equation == "x":
                new_equ += coefficient + "cos(x)"
                return new_equ

            bracket = dif(equation)
            new_equ += str(int(parse_coefficient(bracket)) * int(coefficient))
            new_equ += bracket[len(parse_coefficient(bracket)):]
            new_equ += "cos(" + equation + ")"
            return new_equ


def exponential_equation(funct):
    """
    Gives the output for a function which have exponential parts to it
    :param funct:
    """
    if funct[0] == "e":
        if len(funct) == 3:
            return funct
        else:
            equ = funct[2:]
            return str(polynomial_equation(equ)) + funct
    else:
        coefficient = parse_coefficient(funct)
        funct = funct[len(coefficient):]
        if len(funct) == 3:
            return coefficient + funct
        else:
            equ = funct[2:]
            equ = polynomial_equation(equ)
            funct_coeff = int(parse_coefficient(equ))
            equ = equ[len(str(funct_coeff)):]
            return str(funct_coeff * int(coefficient)) + equ + funct


def linear_equation(funct):
    """
    Gives the output for a function that is linear
    :param funct: string
    """
    if funct == "x":
        return "1"

    return parse_coefficient(funct)


def polynomial_equation(funct):
    """
    Gives the output for a function that has nth degree
    :param funct: string
    """
    if "^" not in funct:
        return linear_equation(funct)
    else:
        multiplier_location = (funct.index("^") + 1)
        if funct[0] == "x":
            multiplier = str(funct[multiplier_location:])
            if multiplier == "2":
                return multiplier + "x"
            else:
                return multiplier + "x^" + str((int(multiplier) - 1))
        else:
            coefficient = parse_coefficient(funct)
            multiplier = int(funct[multiplier_location:])  # error
            new_coefficient = int(coefficient) * int(multiplier)
            if multiplier == 2:
                return str(new_coefficient) + "x"
            else:
                return str(new_coefficient) + "x^" + str(int(multiplier) - 1)


def parse_equation(equ):
    """
    Break the given string into all the pieces of the equation to be sorted after
    :param equ: string
    """
    array = []
    val = ""
    count = 0
    brackets = False
    for x in equ:
        count += 1
        if brackets:
            if x != ")":
                val += x
            else:
                brackets = False
                val += x
                array.append(val)
                val = ""
                # bracket function needs finish
        elif x == "(":
            val += x
            brackets = True
        elif (x != " ") and (count != len(equ)):
            val += x
        elif x == " ":
            array.append(val)
            array.append(" ")
            val = ""
        else:
            val += x
            array.append(val)

    return array


def parse_coefficient(funct):
    """
    Works out the just the coefficient of the given function
    :param funct:
    """
    coefficient = ""
    count = 0
    while (funct[count] != "x") and (funct[count] != "e") and (funct[count] != "c") and (funct[count] != "s"):
        coefficient += funct[count]
        count += 1

    return coefficient


def parse_output(funct):
    funct_pieces = parse_equation(funct)
    if "0" in funct_pieces:
        location = funct_pieces.index("0")

        if funct_pieces[location - 2] != "=":
            for x in range(4):
                funct_pieces.pop(location - 3)

    elif "-1" in funct:
        # this needs to find the -1x and replace it with - x

        output = ""
        for item in funct_pieces:
            output += item
        return output
    else:
        return funct


#####TESTS#####
def tests():
    print(dif("y = 1"))

    # test 0.5 - values
    assert dif("y = 1") == "dy/dx = 0"
    # test 1 - parse equ, very simple linear
    assert parse_equation("y = x") == ["y", " ", "=", " ", "x"]
    assert dif("y = x") == "dy/dx = 1"
    assert dif("y = x + 2") == "dy/dx = 1"  # ammended
    # test 2 - squares
    assert parse_equation("x^2") == ["x^2"]
    assert dif("y = x^2") == "dy/dx = 2x"
    # test 3 - coefficents & linear
    assert dif("y = 2x") == "dy/dx = 2"
    # test 4 - linear equation moved to a funct
    assert linear_equation("x") == "1"
    assert linear_equation("20x") == "20"
    # test 5 - basic polynomials
    assert polynomial_equation("x^2") == "2x"
    assert polynomial_equation("2x^2") == "4x"
    assert polynomial_equation("x^3") == "3x^2"
    assert polynomial_equation("25x^4") == "100x^3"
    # text 5.5 - more adv polynomials
    assert dif("y = x^3") == "dy/dx = 3x^2"
    assert dif("y = 3x^5 + 2x + 5x^2") == "dy/dx = 15x^4 + 2 + 10x"
    # test 6 - exponents
    assert dif("y = e^x") == "dy/dx = e^x"
    # test 7 - more adv exponents
    assert dif("y = e^2x^2") == "dy/dx = 4xe^2x^2"
    assert dif("y = 3e^x") == "dy/dx = 3e^x"
    assert dif("y = 3e^2x^2") == "dy/dx = 12xe^2x^2"
    # test 8 - basic trig
    assert dif("y = cos(x)") == "dy/dx = -sin(x)"
    assert dif("y = sin(x)") == "dy/dx = cos(x)"
    # test 9 - more adv trig
    assert dif("y = cos(2x)") == "dy/dx = -2sin(2x)"
    assert dif("y = sin(2x)") == "dy/dx = 2cos(2x)"
    assert dif("y = 3sin(x^2)") == "dy/dx = 6xcos(x^2)"
    # test 10 - parse output
    assert dif("y = 2x + 2") == "dy/dx = 2"
    assert dif("y = 3sin(x^2) + 6") == "dy/dx = 6xcos(x^2)"
    # test 11 - negative powers
    assert dif("y = x^-1") == "dy/dx = -1x^-2"
    # assert dif("y = x + x^-1") == "dy/dx = 1 + -1x^-2" #this needs to be better output
    assert dif("y = x + x^-1") == "dy/dx = 1 - x^-2"


tests()
