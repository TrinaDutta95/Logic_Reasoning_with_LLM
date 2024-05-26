from nltk.sem import Expression
from nltk import *
from nltk.inference.api import ModelBuilder
from nltk.inference import Mace

# Prover9 example
read_expr = Expression.fromstring
# example1
p1 = read_expr('(Person(x) | Music(y) | Listen(x,y) -> FeelEmotion(x))')
p2 = read_expr('Person(jack)')
p3 = read_expr('Music(moonlight_sonata) ')
p4 = read_expr('Listen(jack,moonlight_sonata)')
c = read_expr('FeelEmotion(jack)')
# example 2
q1 = read_expr('NaziPolitician(heinrich_schmidt)')
d = read_expr('German(heinrich_schmidt)')

p = Prover9().prove(c, [p1,p2,p3,p4])
q = Prover9().prove(d, [q1])
print(p,q)

print("------Using Prover9Command to prove and get proof steps-------")
p = Prover9Command(c, assumptions=[p1,p2,p3,p4])
q = Prover9Command(d, assumptions=[q1])

q2 = read_expr('Cat(heinrich_schmidt)')
q3 = read_expr('all x.(Person(x) | NaziPolitician(x) -> German(x))')
q.add_assumptions([q2, q3])
q.print_assumptions()
print(q.prove())
print("---------")
print(q.proof())


# ProverCommand example
print("****Using ResolutionProver to prove and get proof steps*****")
resolution_p = ResolutionProver().prove(c, [p1,p2,p3,p4], verbose=True)
resolution_q = ResolutionProver().prove(d, [q1], verbose=True)
print("*********")
print(resolution_p)
print("**********")
print(resolution_q)
print("*********")

resolution_p = ResolutionProverCommand(c, [p1,p2,p3,p4])
resolution_q = ResolutionProverCommand(d, [q1])
resolution_p.prove()
print("----------")
print(resolution_p.proof())
print(resolution_p.assumptions())
print(resolution_p.goal())

resolution_q.prove()
print("-----------")
print(resolution_q.proof())
print(resolution_q.assumptions())
print(resolution_q.goal())



# Code:
mace = Mace()
#q6 = read_expr('all x.(NaziGermanPolitician(x) -> German(x))& NaziGermanPolitician(HeinrichSchmidt)')
q6 = read_expr('all x.(NaziGermanPolitician(x) -> German(x))')
q7 = read_expr('NaziGermanPolitician(HeinrichSchmidt)')
e = read_expr('German(HeinrichSchmidt)')
print("##########-third-example-###########")
# prove result from mace4
print(mace.build_model(None, [q6,q7,e]))
print(mace.build_model(e,[q6,q7]))
# prove result from prover9
p = Prover9().prove(e, [q6, q7])
print(p)
# Finding a model
mb = MaceCommand(assumptions=[q6, q7])
print(mb.build_model())

print(mb.model(format='cooked'))
