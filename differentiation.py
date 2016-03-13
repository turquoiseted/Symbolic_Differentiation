"""time to differentiate"""
import tests

"""
to do list:
o allow for chain rule
    -this is started
    -probs need refining a good deal
o allow for bracket chain rule
o do more advanced trig
o logs
o deal with un-formatted entry string i.e no spaces

o Add partial differentiation w.r.t. any variable once main is done
"""


def dif(equ):
    """
    Takes the input and finds out which way it should be differentiated
    :param equ: array
    """
    equ_array = parse_equation(equ)
    result = ""
    for x in equ_array:
        count = x.count("x")
        if count == 2:
            result += chain_rule(x)
        elif ("sin" in x) or ("cos" in x):
            result += trig_equ(x)
        elif "e" in x:
            result += exponential_equation(x)
        elif "^" in x:
            result += polynomial_equation(x)
        elif "x" in x:
            result += linear_equation(x)
        elif x == "y":
            result += "dy/dx"
        elif x == "dy/dx":
            result += "d2y/dx2"
        elif x.isdigit():
            result += "0"
        else:
            result += x
    result = parse_output(result)
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
    """
    Takes the outputted string and ensures good formatting/
    :param funct:
    :return:
    """
    # string.count will find my dupes

    funct_pieces = parse_equation(funct)
    if "1" in funct:
        for items in funct_pieces:
            if "1" in items:
                location = funct_pieces.index(items)
                if items != "1":
                    if (funct_pieces[location - 1] == " ") and (items[0] == "1") and (items[1] == "x"):
                        funct_pieces[location] = funct_pieces[location][1:]
                    elif (funct_pieces[location - 1] == " ") and (items[:2] == "1*") and (items[2] == "x"):
                        funct_pieces[location] = funct_pieces[location][2:]

    if "0" in funct_pieces:
        location = funct_pieces.index("0")

        if funct_pieces[location - 2] != "=":
            for x in range(4):
                funct_pieces.pop(location - 3)

    if "-" in funct:
        for items in funct_pieces:
            if "-" in items:
                location = funct_pieces.index(items)
                if funct_pieces[location - 2] != "=":
                    if funct_pieces[location - 2] == "+":
                        funct_pieces.insert(location - 2, "-")
                    else:
                        funct_pieces.insert(location - 2, "+")
                    funct_pieces.pop(location - 1)
                    funct_pieces[location] = funct_pieces[location][2:]
    output = ""

    for item in funct_pieces:
        output += item
    return output




tests.tests()
