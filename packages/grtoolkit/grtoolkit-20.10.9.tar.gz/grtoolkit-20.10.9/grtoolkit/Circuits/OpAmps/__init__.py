# An op amp is an active circuit element designed to perform mathematical operations of addition, subtraction, multiplication, division, differentiation, and integration.

from grtoolkit.Math import solveEqs

def referenceMaterial():
    #Open reference material
    pass

def vd(v2,v1):
    """
    Differential voltage
    v1 = voltage between inverting terminal and ground
    v2 = voltage between non-inverting terminal and ground
    """
    return v2-v1

def i_out(i1,i2,i_plus, i_minus):
    """Output current"""
    return sum(i1, i2, i_plus, i_minus)

def v_o(A,vd):
    """
    Open loop voltage gain.
    Gain of the op amp without any external feedback from output to input.
    Sometimes voltage gain (A) is expressed in decibels (dB).
    A dB = 20*log_10(A)

    Usage:
        v_out(4, vd(4,6))
    """
    return A*vd

def mode(v_o, Vcc):
    """
    A practical limitation of the op amp is that the magnitude of its output voltage cannot exceed abs(Vcc).
    The output voltage is dependent on an limited by the power supply voltage.

    Although we shall always operate the op amp in the linear region, the
    possibility of saturation must be borne in mind when one designs with
    op amps, to avoid designing op amp circuits that will not work in the
    laboratory.
    """
    if v_o == Vcc:
        return "positive saturation"
    if v_o >= -Vcc and v_o <= Vcc:
        return "linear region"
    if v_o == -Vcc:
        return "negative saturation"

def invertingAmplifier(find="v_out", printEq=False, **kwargs):
    """variables
                v_out, v_in = voltage out/in
                R2, R1 = resistors (view reference image)
    """
    eq = list()
    eq.append("Eq(v_out,-R2/R1*v_in)")
    return solveEqs(eq, find, printEq=printEq, **kwargs)

def nonInvertingAmplifier(find="v_out", printEq=False, **kwargs):
    """variables: 
                v_out, v_in = voltage out/in
                R2, R1 = resistors (view reference image)
                """
    eq = list()
    eq.append("Eq(v_out,(1+R2/R1)*v_in)")
    return solveEqs(eq, find, printEq=printEq, **kwargs)

def voltageFollower(find="v_out", printEq=False, **kwargs):
    """variables: 
                v_out, v_in = voltage out/in (view reference image)
                """
    eq = list()
    eq.append("Eq(v_out,v_in)")
    return solveEqs(eq, find, printEq=printEq, **kwargs)

def summer(find="v_out", printEq=False, **kwargs):
    """variables: 
                v_out, v1, v2, v3 = voltage out/in 
                Rf, R3, R2, R1 = resistors (view reference image)
                """
    eq = list()
    eq.append("Eq(v_out,-(Rf/R1*v1 + Rf/R2*v2 + Rf/R3*v3))")
    return solveEqs(eq, find, printEq=printEq, **kwargs)

def differenceAmplifier(find="v_out", printEq=False, **kwargs):
    """variables: 
                v_out, v1, v2, v3 = voltage out/in 
                R2, R1 = resistors (view reference image)
                """
    eq = list()
    eq.append("Eq(v_out,R2/R1*(v2-v1)")
    return solveEqs(eq, find, printEq=printEq, **kwargs)

def DAC(Rf,R_list, V_list):
    """
    TO BE COMPLETED; this can use the summer function. It's the same thing.
    """
    eq = list()
    eq.append("Eq(-v_out,rf/r1*v1 + rf/r2*v2 + rf/r3*v3 + rf/r4*v4")
    # return solveEqs(eq, find, printEq=printEq, **kwargs)

def gainAmplifier():
    """
    TO BE COMPLETED
    """
    eq = list()
    eq.append("Eq(vo,Av*(v2-v1)")
    eq.append("Eq(Av = 1 + 2*R / R_G")