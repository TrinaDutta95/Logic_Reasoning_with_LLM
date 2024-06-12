from nltk import *

if __name__ == '__main__':
    read_expr = Expression.fromstring
    a1 = read_expr("all x. (PerformsInSchoolTalentShowsOften(x) -> (AttendsSchoolEvents(x) & VeryEngagedWithSchoolEvents(x)))")
    a2 = read_expr( "all x. (PerformsInSchoolTalentShowsOften(x) | (InactiveMember(x) & DisinterestedMember(x)))")
    a3 = read_expr("all x. (ChaperonesHighSchoolDances(x) -> -StudentAtSchool(x))")
    a4 = read_expr("all x. ((InactiveMember(x) & DisinterestedMember(x)) -> ChaperonesHighSchoolDances(x))")
    a5 = read_expr("all x. ((YoungChild(x) | Teenager(x)) & WishesToFurtherAcademicCareer(x) & WishesToFurtherEducationalOpportunities(x) -> StudentAtSchool(x))")
    a6 = read_expr("(AttendsSchoolEvents(Bonnie) & VeryEngagedWithSchoolEvents(Bonnie) & StudentAtSchool(Bonnie)) | (-AttendsSchoolEvents(Bonnie) & -VeryEngagedWithSchoolEvents(Bonnie) & -StudentAtSchool(Bonnie))")
    a7 = read_expr("EqualDouble(eight, four)")
    a8 = read_expr("EqualDouble(four, two)")
    d = read_expr("PerformsInSchoolTalentShowsOften(Bonnie)")
    mace = Mace()
    # first example
    print("##########-first-example-###########")
    print("mace:", mace.build_model([d], [a1, a2,a3,a4,a5,a6]))
    q = Prover9().prove(d, [a1, a2,a3,a4,a5,a6])
    print("prover:", q)
    mb = MaceCommand(assumptions=[a1, a2,a3,a4,a5,a6])
    mb.build_model()
    print("mace model:", mb.model(format='cooked'))

#https://www.cs.utexas.edu/~mooney/cs343/slide-handouts/inference.4.pdf