import parse_output
import parse_equation
"""time to differentiate"""

"""
to do list:
o allow for chain rule
    -this is started
    -probs need refining a good deal
o allow for bracket chain rule
o do more advanced trig
o logs
o deal with un-formatted entry string i.e no spaces
o output in e followed by trig then descending powers

o Add partial differentiation w.r.t. any variable once main is done
"""


def dif(equ):
    """
    Takes the input and finds out which way it should be differentiated
    :param equ: array
    """
    equ_array = parse_equation.parse_equation(equ)
    result = ""
    for x in equ_array:
        count = x.count("x")
        if count == 2:
            result += chain_rule(x)
        elif "log" in x:
            result += log_equ(x)
        elif ("sin" in x) or ("cos" in x) or ("tan" in x):
            result += trig_equ(x)
        elif "e" in x:
            result += exponential_equation(x)
        elif "x" in x:
            result += polynomial_equation(x)
        elif x == "y":
            result += "dy/dx"
        elif x == "dy/dx":
            result += "d2y/dx2"
        elif x.isdigit():
            result += "0"
        else:
            result += x

    result = parse_output.parse_output(result)
    return result


def chain_rule(funct):
    """
    Deals with multiple x equations by using the chain rule
    :param funct:
    :return:
    """
    first_funct = ""
    count = 0
    for char in funct:
        if char != "*":
            first_funct += funct[count]
            count += 1
        elif char == "*":
            break

    second_funct = funct[count + 1:]
    return dif(first_funct) + "*" + second_funct + " + " + dif(second_funct) + "*" + first_funct


def log_equ(funct):
    """
    Gives the output for a function which has logarithmic parts to it
    :param funct:
    """
    if funct[:3] == "log":
        equ = funct[4:-1]
        return str(polynomial_equation(equ)) + "/" + equ
    # else:
    #     coefficient = parse_coefficient(funct)
    #     funct = funct[len(coefficient):]
    #     if len(funct) == 3:
    #         return coefficient + funct
    #     else:
    #         equ = funct[2:]
    #         equ = polynomial_equation(equ)
    #         funct_coeff = int(parse_coefficient(equ))
    #         equ = equ[len(str(funct_coeff)):]
    #         return str(funct_coeff * int(coefficient)) + equ + funct


def trig_equ(funct):
    """
    trig
    :param funct:
    """
    if (funct[:3] == "cos") or (funct[:3] == "sin") or (funct[:3] == "tan"):
        new_equ = ""
        equation = funct[4:-1]
        if "cos" in funct:
            new_equ += "-"
            new_equ += dif(equation)
            new_equ += "sin(" + equation + ")"
            return new_equ

        elif "sin" in funct:
            if equation == "x":
                return "cos(x)"
            new_equ += dif(equation)
            new_equ += "cos(" + equation + ")"
            return new_equ

        elif "tan" in funct:
            if equation == "x":
                return "sec^2(x)"
            new_equ += dif(equation)
            new_equ += "sec^2(" + equation + ")"
            return new_equ

    else:
        coefficient = parse_coefficient(funct)
        funct = funct[len(coefficient):]
        equation = funct[4:-1]
        if "cos" in funct:
            new_equ = "-"
            return trig_chain_rule(coefficient, equation, new_equ, funct)

        elif "sin" in funct:
            new_equ = ""
            return trig_chain_rule(coefficient, equation, new_equ, funct)

        elif "tan" in funct:
            new_equ = ""
            return trig_chain_rule(coefficient, equation, new_equ, funct)


def trig_chain_rule(coefficient, equation, new_equ, funct):
    """
    Reduces clutter in the trig function by doing the chain rule seperatly
    :param funct:
    :param coefficient:
    :param equation:
    :param new_equ:
    :return:
    """
    bracket = dif(equation)
    new_equ += str(int(parse_coefficient(bracket)) * int(coefficient))
    new_equ += bracket[len(parse_coefficient(bracket)):]
    if "cos" in funct:
        new_equ += "sin(" + equation + ")"
    elif "sin" in funct:
        new_equ += "cos(" + equation + ")"
    elif "tan" in funct:
        new_equ += "sec^2(" + equation + ")"

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


def parse_coefficient(funct):
    """
    Works out the just the coefficient of the given function
    :param funct:
    """
    if funct[0] == "x":
        coefficient = 1
    else:
        coefficient = ""
        count = 0
        check_alpha = ["x", "c", "e", "s", "t", "n"]
        while funct[count] not in check_alpha:
            coefficient += funct[count]
            count += 1

    return coefficient
