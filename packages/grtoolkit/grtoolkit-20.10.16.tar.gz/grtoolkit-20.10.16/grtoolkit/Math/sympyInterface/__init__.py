import re
from re import sub

def gen_sorted_bracket_pairs(expr): #ordered bracket pairs
    open_brackets = [m.start() for m in re.finditer('\(', expr)]
    close_brackets = [m.start() for m in re.finditer('\)', expr)]
    # copyOpen = open_brackets
    taken = list()
    bracket_pairs = list()
    
    all_open_brackets = [[open,'o'] for open in open_brackets]
    all_close_brackets = [[close,'c'] for close in close_brackets]
    all_brackets = sorted(all_open_brackets + all_close_brackets)

    if len(all_open_brackets) != len(all_close_brackets):
        raise "Error: Non-even brackets."

    for b in range(len(all_brackets)):
        if all_brackets[b][1] == "c":
            i = 1
            while True:
                if all_brackets[b-i][1] == "o" and b-i not in taken:
                    bracket_pairs.append([all_brackets[b-i][0],all_brackets[b][0]])
                    taken.append(b-i)
                    break
                i+=1
    sorted_bracket_pairs = sorted(bracket_pairs)
    # print(sorted(sorted_bracket_pairs)) ### BRACKET PAIRS
    return sorted_bracket_pairs

def gen_func_bps(func_name, expr, sorted_bracket_pairs): #bracket pair after function namefunction opening and closing bracket pairs in str
    funcs = [m.start() for m in re.finditer(func_name, expr)]
    master_func_bracket_pairs = list()

    for i in range(len(sorted_bracket_pairs)):
    # print(bracket_pairs[i])
        for func in funcs:
            if func > sorted_bracket_pairs[i][0] and func < sorted_bracket_pairs[i+1][0]:
                master_func_bracket_pairs.append(sorted_bracket_pairs[i+1])
    return master_func_bracket_pairs

def gen_func_sub_bps(func_bps,sorted_bracket_pairs): 
    """function sub bracket pairs"""
    #Find bracket pairs inside func_bps:
    func_sub_bps = list()
    for fbp in func_bps:
        temp_sub_bps = list()
        for bp in sorted_bracket_pairs:
            if bp[0]>fbp[0] and bp[1]<fbp[1]:
                temp_sub_bps.append(bp)
        func_sub_bps.append(temp_sub_bps)
    return func_sub_bps

def gen_func_commas(expr, func_bps, func_sub_bps):
    #Find commas inside function bracket pairs that are not inside function sub bracket pairs
    commas = [m.start() for m in re.finditer(',', expr)]
    func_commas = list()
    ## for each comma:
    i=0
    for fbp in func_bps:
        temp_comma = list()
        for comma in commas:
        ## if comma within function bracket pair:
            if comma > fbp[0] and comma < fbp[1]: #if comma within function brackets
                AND_counter = list()
                for sfbp in func_sub_bps[i]: # if comma not within any bracket pair within function
                    if comma < sfbp[0] or comma > sfbp[1]:  # is comma outside of this sub-bracket?
                        AND_counter.append(1)
                    else:
                        AND_counter.append(0)
                if sum(AND_counter) == len(AND_counter): # append comma only when outside all sub-brackets
                    temp_comma.append(comma)
        if comma:
            func_commas.append(temp_comma)
        i+=1
    return func_commas

def gen_ranges2protect(func_bps, func_comma):
    #generating list of ranges to protect
    zipped_list = list(zip(func_bps,func_comma))
    ranges2protect = list()
    i=0
    for func, fcommas in zipped_list:
        i=0
        mini_r2p=list()
        for fcomma in fcommas:
            if (len(fcommas)-i)>1:
                # print(expr[fcommas[i]+1:fcommas[i+1]])
                mini_r2p.append([fcommas[i]+1, fcommas[i+1]])
            else:
                # print(expr[fcomma+1:func[1]])
                mini_r2p.append([fcomma+1,func[1]])
            i+=1
        ranges2protect.append(mini_r2p)
    return ranges2protect

def gen_protect_zones_copy(expr, ranges2protect):
    protect_zones_copy = list()
    for a in ranges2protect:
        for b in a:
            # print(expr[b[0]:b[1]])
            protect_zones_copy.append(expr[b[0]:b[1]])
    return protect_zones_copy

def gen_protect_zones(expr, func_list):
    protect_zones = list()
    protect_zone_ranges= list()
    for func in func_list:
        sorted_bracket_pairs = gen_sorted_bracket_pairs(expr)
        func_bps = gen_func_bps(func, expr, sorted_bracket_pairs)
        func_sub_bps = gen_func_sub_bps(func_bps,sorted_bracket_pairs)
        func_commas = gen_func_commas(expr, func_bps, func_sub_bps)
        ranges2protect = gen_ranges2protect(func_bps, func_commas)
        func_protect_zones = gen_protect_zones_copy(expr, ranges2protect)
        protect_zones = protect_zones + func_protect_zones
        protect_zone_ranges = protect_zone_ranges + ranges2protect

    #flatten list
    protect_zones_ranges_copy = list()
    for a in protect_zone_ranges:
        for b in a:
            # print(expr[b[0]:b[1]])
            protect_zones_ranges_copy.append([b[0],b[1]])

    zipped_list = sorted(list(zip(protect_zones_ranges_copy,protect_zones)))
    sorted_protect_zones = [item[1] for item in zipped_list]
    sorted_protect_zones.reverse()
    sorted_protect_zones_ranges_copy = [item[0] for item in zipped_list]
    sorted_protect_zones_ranges_copy.reverse()

    # return protect_zones
    # return list(zip(protect_zones_copy,protect_zones))
    return sorted_protect_zones, sorted_protect_zones_ranges_copy

def gen_replace_zones(expr, func_list):
    replace_zones = list()
    for func in func_list:
        sorted_bracket_pairs = gen_sorted_bracket_pairs(expr)
        func_bps = gen_func_bps(func, expr, sorted_bracket_pairs)
        func_sub_bps = gen_func_sub_bps(func_bps,sorted_bracket_pairs)
        func_commas = gen_func_commas(expr, func_bps, func_sub_bps)
        ranges2replace = gen_ranges2protect(func_bps, func_commas)
        replace_zones = replace_zones + ranges2replace

    replace_zones_copy = list()
    for a in replace_zones:
        for b in a:
            # print(expr[b[0]:b[1]])
            replace_zones_copy.append([b[0],b[1]])
    return replace_zones_copy

def stringMutation(old, new, replacement_range):
    #slice into 3 parts
    pre = old[:replacement_range[0]]
    # cen = old[replacement_range[0]:replacement_range[1]]
    suf = old[replacement_range[1]:]
    return pre + new + suf

def preSympifySub(expr,**kwargs):
    """
    Designed this as a reponse to the fact that sympify evaluates expressions when performed and therefore would integrate and/or differentiate before I would have a chance to perform substitution.
    Usage:
        preSympifySub(r'Eq(v, L*diff(i,t))',i="10*t*exp(-5*t)")
    """

    for k,v in kwargs.items():
        v=str(v)

    func_list = ["integrate", "diff"]
    func_pres = list()

    # Check if any function listed is present in expr
    for func in func_list:
        if func in str(expr):
            func_pres.append(1)
        else:
            func_pres.append(0)

    if sum(func_pres) >= 1:
        protect_zones, _ = gen_protect_zones(str(expr), func_list)
        for k,v in kwargs.items():
            regex = rf'(?<!\w|\d){k}(?!\w|\d)'
            expr = sub(regex,rf"({str(v)})",str(expr))

        _, undue_replace_zones_ranges = gen_protect_zones(str(expr), func_list)
        for protect, replaced in list(zip(protect_zones, undue_replace_zones_ranges)):
            # expr = expr.replace(replaced,protect)
            expr = stringMutation(expr,protect,replaced)
    else:
        for k,v in kwargs.items():
            regex = rf'(?<!\w|\d){k}(?!\w|\d)'
            expr = sub(regex,rf"({str(v)})",str(expr))
    return expr

# def Capacitance(find="C", printEq=False, **kwargs):
#     """
#     Usage: the ratio of the charge on one plate of a capacitor to the voltage difference between the two plates, measured in farads (F).

#     Variables: 
#                 C = capacitance (1 Farads = 1 Coulomb/Volt)
#                 epsilon = permitivity of the dielectric material between plates
#                 A = surface area of each plate
#                 d = distance between plates"""
#     eq = list()
#     eq.append("Eq(C,epsilon*A/d)")    
#     return solveEqs(eq, find, printEq=printEq, **kwargs)

# def solveEqs(eq, find, printEq=False, **kwargs):
#     """
#     Solves multiple equations independently in search for variable.
#     Allows substitution via kwargs.
#     In other words, algebraSolve() on multiple equations at once.

#     Usage:
#         eq = list()
#         eq.append("Eq(a_tan, dv/dt)")
#         eq.append("Eq(a_tan, r*dw/dt)")
#         eq.append("Eq(a_tan, r*alpha)")
#         solveEqs(eq, "a_tan", printEq=printEq, **kwargs)

#     Returns:
#         [
#             ans1,
#             ans2,
#             ans3
#         ]
#     """
#     #CREATE SET OF ARGUMENTS SUPPLIED TO FUNCTION
#     availSet = {find}
#     for k,v in kwargs.items():
#         availSet.add(k)
#         v=str(v)
#     eq = [preSympifySub(expr,**kwargs) for expr in eq]
#     eq = [sympify(expr) for expr in eq]
#     freesym = [expr.free_symbols for expr in eq]
#     freevar = []
#     solution = list()
#     #CONVERT LIST OF SETS OF SYMBOLS INTO LIST OF SETS OF STR
#     for freeset in freesym:
#         tempset = set()
#         for sym in freeset:
#             tempset.add(sym.name)
#         freevar.append(tempset)
#     unknowns = [freeset-availSet for freeset in freevar]            # Eliminate variables requested in function arguments: find and knowns
#     unknowns_count = [len(unknownset) for unknownset in unknowns]   # How many unknowns are left in each equation?
#     find_avail = [find in freevarset for freevarset in freevar]     # Is the variable in question available in this equation?
#     index = list(range(len(unknowns_count)))
#     zipper = list(zip(index, unknowns_count, find_avail))

#     for zippedList in zipper:
#         solution.append(algebraSolve(eq[zippedList[0]],find, **kwargs))

#     printEquationsSolution(eq, solution) #print Equations and Solutions to console
#     return solution

# def printEquations(eq):
#     # print("Equations:\n")
#     for equation in eq:
#         print(equation)

# def printEquationsSolution(eq, solution, printEq=True):
#     #if printEq:
#     print("\n")
#     print("Equations"), printEquations(eq), print("\n")
#     print("Solutions"), printEquations(solution), print("\n")

# def algebraSolve(expr, solve_for,**kwargs):
#     """
#     Solves single algebraic string equation. 
    
#     Usage: algebraSolve("x**2 + 3*x - 1/2 + y", "x", y=24)

#     Returns: [ans]
#     """
#     expr = preSympifySub(expr,**kwargs)
#     expr=sympify(expr)
#     #GENERATE VARIABLE SYMBOLS FROM EXPRESSION
#     for sym in expr.free_symbols: 
#         exec(f"{sym.name}=symbols('{sym.name}')")
#         #MAKE solve_for STRING EQUAL REQUIRED EXPRESSION VARIABLE SYMBOL
#         if solve_for == sym.name:    
#             solve_for = sym
        
#         # SUBSTITUTE KARGs FOR EXPRESSION SYMBOLS
#         for k, v in kwargs.items():
#             if k == sym.name:
#                 expr=expr.subs(k,v)
#     return solve(expr, solve_for)

if __name__ == "__main__":
    pass
    # expr = 'eq.append("Eq(w,integrate(C*v,(v,v0,v1))-integrate(C*v,(v,v0,v1))+integrate(8*diff(v**2,v),(v,v0,vt), (v4,f3)))")'
    
    # print(expr, "\n")
    # expr2 = preSympifySub(expr,v="99*red_ballons")
    # print(expr2) 
    
    # import grtoolkit.Circuits as c 
    # c.Capacitors.Capacitance("C", 
    #                         epsilon=48,
    #                         A = 89,
    #                         d = 79) 
    # from grtoolkit.Math import solveEqs

    # from sympy import sympify, solve, symbols
    # Capacitance("C", epsilon=49, A=56, d=79)