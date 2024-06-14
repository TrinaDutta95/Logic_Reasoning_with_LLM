from nltk import *

if __name__ == '__main__':
    read_expr = Expression.fromstring
    a1 = read_expr("all x. (DesignStyle(x, Zaha_Hadid) -> Timeless(x))")
    a2 = read_expr("all x. (MassProductDesign(x) -> -Timeless(x))")
    a3 = read_expr("DesignStyle(Zaha_Hadid) | DesignStyle(Kelly_Wearstler)")
    a4 = read_expr("all x. (DesignStyle(x, Kelly_Wearstler) -> Evocative(x))")
    a5 = read_expr("all x. (DesignStyle(x, Kelly_Wearstler) -> Dreamy(x))")
    a6 = read_expr("all x. (DesignBy(x, Max) & Timeless(x) -> (MassProductDesign(x) & Evocative(x)))")
    a7 = read_expr("EqualDouble(eight, four)")
    a8 = read_expr("EqualDouble(four, two)")
    e = read_expr("exists x. (DesignBy(x, Max) & MassProductDesign(x))")
    # d = read_expr("-("+e+")")
    print([a1,a2,a3,a4,a5])
    mace = Mace()
    # first example
    print("##########-first-example-###########")
    print("mace:", mace.build_model(e,[a1,a2,a3,a4,a5,a6]))
    q = Prover9().prove(e, [a1,a2,a3,a4,a5,a6])
    print("prover:", q)
    mb = MaceCommand(assumptions=[a1,a2,a3,a4,a5,a6])
    mb.build_model()
    print("mace model:", mb.model(format='cooked'))

#https://www.cs.utexas.edu/~mooney/cs343/slide-handouts/inference.4.pdf