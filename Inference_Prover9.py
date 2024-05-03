# from nltk.sem import Expression
from nltk import *

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