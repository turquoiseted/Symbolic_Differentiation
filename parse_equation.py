split_character = [" ", "+", "="]


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
            elif x != equ[-1]: # this is shit and should be improved post haste
                brackets = False
                val += x
            else:
                brackets = False
                val += x
                array.append(val)
                val = ""
                # bracket function needs finish

        # Check if its a bracket so all content is kept by brackets
        elif x == "(":
            val += x
            brackets = True
        elif (x not in split_character) and (count != len(equ)):
            val += x
        # split each value
        elif x in split_character:
            if val != "":
                array.append(val)
            array.append(x)
            val = ""
        else:
            val += x
            array.append(val)

    return array
