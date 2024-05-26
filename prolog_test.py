from pyswip import Prolog
prolog = Prolog()
prolog.assertz("father(michael,john)")
prolog.assertz("father(michael,gina)")
list(prolog.query("father(michael,X)")) == [{'X': 'john'}, {'X': 'gina'}]
for soln in prolog.query("father(X,Y)"):
    print(soln["X"], "is the father of", soln["Y"])


prolog2 = Prolog()
q1 = 'German(X) :- NaziGermanPolitician(X)'
q2 = 'NaziGermanPolitician(HeinrichSchmidt)'
c1 = 'German(HeinrichSchmidt)'
prolog2.assertz(q1)
prolog2.assertz(q2)
result = list(prolog2.query("German(X)"))==[{'X':'HeinrichSchmidt'}]
print(result)
for soln in prolog2.query("German(X)"):
    print(soln["X"], "is German.")
