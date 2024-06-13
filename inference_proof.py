from nltk import *

if __name__ == '__main__':
    read_expr = Expression.fromstring
    a1 = read_expr("all x. (bakery(x) -> -spicy(x))")
    a2 = read_expr("all x. (cupcake(x) -> bakery(x))")
    a3 = read_expr("all x. (hotpot(x) -> spicy(x))")
    a4 = read_expr("all x. (product_of_Baked_by_Melissa(x) -> cupcake(x))")
    a5 = read_expr("all x. (dried_Thai_chili(x) & (spicy(x) | bakery(x)) -> (hotpot(x) | spicy(x)))")
    a6 = read_expr("(AttendsSchoolEvents(Bonnie) & VeryEngagedWithSchoolEvents(Bonnie) & StudentAtSchool(Bonnie)) | (-AttendsSchoolEvents(Bonnie) & -VeryEngagedWithSchoolEvents(Bonnie) & -StudentAtSchool(Bonnie))")
    a7 = read_expr("EqualDouble(eight, four)")
    a8 = read_expr("EqualDouble(four, two)")
    e = "exists x. (dried_Thai_chili(x) & product_of_Baked_by_Melissa(x))"
    d = read_expr("-("+e+")")
    print([a1,a2,a3,a4,a5])
    mace = Mace()
    # first example
    print("##########-first-example-###########")
    print("mace:", mace.build_model(d,[a1,a2,a3,a4,a5]))
    q = Prover9().prove(d, [a1,a2,a3,a4,a5])
    print("prover:", q)
    mb = MaceCommand(assumptions=[a1,a2,a3,a4,a5])
    mb.build_model()
    print("mace model:", mb.model(format='cooked'))

#https://www.cs.utexas.edu/~mooney/cs343/slide-handouts/inference.4.pdf