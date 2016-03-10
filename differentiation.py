"time to differentiate"

def dif(equ):
    """
    Takes the input and finds out which way it should be differentiated
    """
    equ_array = parseEquation(equ)
    result = ""
    val = ""
    for x in equ_array:
        if ("sin" in x) or ("cos" in x):
            result += trigEqu(x)
        elif "e" in x:
            result += exponentialEqu(x)
        elif "^" in x:
            result += polynomialEqu(x)
        elif "x" in x:
            result += linearEqu(x)
        elif x == "y":
            result += "dy/dx"
        elif x.isdigit():
            result += "0"
            ##needs formatting
        else: 
            result += x
    return result

def trigEqu(funct):
    """
    trig
    """
    if (funct[:3] == "cos") or (funct[:3] == "sin"):
        new_equ = ""
        equation = funct[4:-1]
        if "cos" in funct :
            new_equ += "-"
            if equation == "x":
                return "-sin(x)"
            new_equ += dif(equation)
            new_equ += "sin(" + equation + ")"
            return new_equ
        
        elif "sin" in funct :
            if equation == "x":
                return "cos(x)"
            new_equ += dif(equation)
            new_equ += "cos(" + equation + ")"
            return new_equ

    else:
        coeff = parseCoefficent(funct)
        funct = funct[len(coeff):]
        equation = funct[4:-1]
        
        if "cos" in funct :
            new_equ = "-"
            equation = funct[4:-1]
            if equation == "x":
                new_equ += coeff + "sin(x)"
                return new_equ

            bracket = dif(equation)
            new_equ += str(int(parseCoefficent(bracket))*int(coeff))
            new_equ += bracket[len(parseCoefficent(bracket)):]
            new_equ += "sin(" + equation + ")"
            return new_equ
        
        elif "sin" in funct :
            new_equ = ""
            equation = funct[4:-1]
            if equation == "x":
                new_equ += coeff + "cos(x)"
                return new_equ
            
            bracket = dif(equation)
            new_equ += str(int(parseCoefficent(bracket))*int(coeff))
            new_equ += bracket[len(parseCoefficent(bracket)):]
            new_equ += "cos(" + equation + ")"
            return new_equ
        
    
def exponentialEqu(funct):
    """
    Gives the output for a function which have exponential parts to it
    """
    if funct[0] == "e":
        if len(funct) == 3:
            return funct
        else:
            equ = funct[2:]
            return str(polynomialEqu(equ)) + funct
    else:
        coeff = parseCoefficent(funct)
        funct = funct[len(coeff):]
        if len(funct) == 3:
            return coeff + funct
        else:
            equ = funct[2:]
            equ = polynomialEqu(equ)
            funct_coeff = int(parseCoefficent(equ))
            equ = equ[len(str(funct_coeff)):]
            return  str(funct_coeff*int(coeff))+ equ + funct
        

def linearEqu(funct):
    """
    Gives the output for a function that is linear
    """
    if funct == "x":
        return "1"

    return parseCoefficent(funct)

def polynomialEqu(funct):
    """
    Gives the output for a function that has nth degree
    """
    if "^" not in funct:
        return linearEqu(funct)
    else:
        new_coeff = 0
        mult_location = (funct.index("^") + 1)
        multipler = ""
        if funct[0] == "x":
            multiplier = str(funct[mult_location:])
            if multiplier == "2":
                return multiplier + "x"
            else:
                return multiplier + "x^" + str((int(multiplier) - 1))
        else:
            coeff = parseCoefficent(funct)
            multiplier = int(funct[mult_location:]) #error
            new_coeff = int(coeff)*int(multiplier)
            if multiplier == 2:
                return str(new_coeff) + "x"
            else:
                return str(new_coeff) + "x^" + str(int(multiplier) - 1)
            

    
def parseEquation(equ):
    """
    Break the given string into all the pieces of the equation to be sorted after
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
                ##bracket function needs finish
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

def parseCoefficent(funct):
    """
    Works out the just the coefficent of the given function
    """
    coeff = ""
    count = 0
    while (funct[count] != "x") and (funct[count] != "e") and (funct[count] != "c") and (funct[count] != "s"):
        coeff += funct[count]
        count += 1
        
    return coeff

#####TESTS#####
def tests():
    
    print()
    
    #test 0.5
    assert dif("y = 1") == "dy/dx = 0"
    #test 1
    assert parseEquation("y = x") == ["y", " ", "=", " ", "x"]
    assert dif("y = x") == "dy/dx = 1"
    assert dif("y = x + 2") == "dy/dx = 1 + 0" #ammended
    #test 2
    assert parseEquation("x^2") == ["x^2"]
    assert dif("y = x^2") == "dy/dx = 2x"
    #test 3
    assert dif("y = 2x") == "dy/dx = 2"
    #test 4
    assert linearEqu("x") == "1"
    assert linearEqu("20x") == "20"
    #test 5
    assert polynomialEqu("x^2") == "2x"
    assert polynomialEqu("2x^2") == "4x"
    assert polynomialEqu("x^3") == "3x^2"
    assert polynomialEqu("25x^4") == "100x^3"
    #text 5.5
    assert dif("y = x^3") == "dy/dx = 3x^2"
    assert dif("y = 3x^5 + 2x + 5x^2") == "dy/dx = 15x^4 + 2 + 10x"
    #test 6
    assert dif("y = e^x") == "dy/dx = e^x"
    #test 7
    assert dif("y = e^2x^2") == "dy/dx = 4xe^2x^2"
    assert dif("y = 3e^x") == "dy/dx = 3e^x"
    assert dif("y = 3e^2x^2") == "dy/dx = 12xe^2x^2"
    #test 8
    assert dif("y = cos(x)") == "dy/dx = -sin(x)"
    assert dif("y = sin(x)") == "dy/dx = cos(x)"
    #test 9
    assert dif("y = cos(2x)") == "dy/dx = -2sin(2x)"
    assert dif("y = sin(2x)") == "dy/dx = 2cos(2x)"
    assert dif("y = 3sin(x^2)") == "dy/dx = 6xcos(x^2)"
    

tests()
