import parse_equation
check_gap = ["=", " ", "+", "-"]


def parse_output(funct):
    """
    Takes the outputted string and ensures good formatting, avoiding 1* +- etc
    :param funct:
    :return:
    """
    funct_pieces = parse_equation.parse_equation(funct)
    output = ""
    #check if its a full equation
    if len(funct) > 5:
        # replace any 1s so functionally they are on their own
        if "1" in funct:
            for items in funct_pieces:
                if "1" in items:
                    location = funct_pieces.index(items)
                    if items != "1":
                        alpha_check = ["x", "c", "s", "t", "l"]
                        if (funct_pieces[location - 1] in check_gap) and (items[0] == "1") and (items[1] in alpha_check):
                            funct_pieces[location] = funct_pieces[location][1:]
                        elif (funct_pieces[location - 1] == " ") and (items[:2] == "1*") and (items[2] == "x"):
                            funct_pieces[location] = funct_pieces[location][2:]
                        #this can probs be removed
                        elif (funct_pieces[location - 1] == " ") and (items[:2] == "-1") and (items[2] in alpha_check):
                            funct_pieces[location] = funct_pieces[location][0] + funct_pieces[location][2:]

        # remove any floating 0s
        if "0" in funct_pieces:
            location = funct_pieces.index("0")
            if funct_pieces[location - 2] != "=":
                for x in range(4):
                    funct_pieces.pop(location - 3)

        # test for multiple integers
        new_int = 0
        count = 0
        bool_check = False
        banned_values = ["=", " ", "+", "-", "0", ""]
        while count < len(funct_pieces):
            if ("x" not in funct_pieces[count]) and (funct_pieces[count] not in banned_values):
                bool_check = True
                if funct_pieces[count - 2] == "=":
                    new_int += int(funct_pieces[count])
                    for x in range(2):
                        funct_pieces.pop(count - 1)
                    count -= 2
                else:
                    new_int += int(funct_pieces[count])
                    for x in range(4):
                        funct_pieces.pop(count - 3)
                    count -= 4
            count += 1

        # if there has been integers put them onto the end
        if bool_check:
            if (funct_pieces[-1] == "=") or (funct_pieces[-1] == " "):
                funct_pieces.append(" ")
                funct_pieces.append(str(new_int))
            else:
                funct_pieces.append(" ")
                funct_pieces.append("+")
                funct_pieces.append(" ")
                funct_pieces.append(str(new_int))

        # replace negative numbers with a minus sign
        if "-" in funct:
            for items in funct_pieces:
                if "-" in items:
                    if items != "-":
                        location = funct_pieces.index(items)
                        if funct_pieces[location - 2] != "=":
                            if funct_pieces[location - 2] == "+":
                                funct_pieces.insert(location - 2, "-")
                            else:
                                funct_pieces.insert(location - 2, "+")
                            funct_pieces.pop(location - 1)
                            funct_pieces[location] = funct_pieces[location][1:]

    for item in funct_pieces:
        output += item
    return output
