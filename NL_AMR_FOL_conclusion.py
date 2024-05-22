from NL_to_FOL import *
from nltk import *

p1 = ['Heinrich Scmidt was a Nazi German politician.']
conclusion1 = ["Heinrich Schmidt was German."]
result1 = True

#NL convert to AMR
premise_g, conclusion_g = amr_conversion(p1, conclusion1)

#AMR convert to FOL
premise_fol = amr_to_fol(premise_g)
conclusion_fol = amr_to_fol(conclusion1)

print("*************AMR to FOL*******")
print("premise FOL:",premise_fol)
print("conclusion FOL:", conclusion_fol)

#prover9
read_expr = Expression.fromstring
case_p1 = read_expr(premise_fol)
case_conclusion1 = read_expr(conclusion_fol)

prove1 = Prover9().prove(case_conclusion1,  [case_p1])
print(prove1)
