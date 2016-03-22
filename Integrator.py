def integrate(equ):
    if "x" in equ:
        return "1/2x^2"


def tests():
    print()
    assert "int(x)" == "1/2x^2"