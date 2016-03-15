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
