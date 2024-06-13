from nltk.sem import Expression
from nltk.inference import MaceCommand
from nltk import *
read_expr = Expression.fromstring
mace = Mace()


def gen_counterexample(premise_fol):
    premise_fol_data = []
    for premise in premise_fol:
        premise = read_expr(premise)
        # print(premise)
        premise_fol_data.append(premise)
    print("premise to fol output:", premise_fol_data)
    conclusion_fol_data = read_expr(conclusion[0])
    print("Premises (FOL):", [expr for expr in premise_fol_data])
    print("mace:", mace.build_model(conclusion_fol_data, premise_fol_data))
    q = Prover9().prove(conclusion_fol_data, premise_fol_data)
    print("prover:", q)
    mb = MaceCommand(assumptions=premise_fol_data)  # , max_models=1)
    mb.build_model()
    result = mb.model(format='cooked')
    print("mace model:", result)
    return str(result)


# Example usage with your premises:
premises = [
            "all x. (bakery(x) -> -spicy(x))",
            "all x. (cupcake(x) -> bakery(x))",
            "all x. (hotpot(x) -> spicy(x))",
            "all x. (product_of_Baked_by_Melissa(x) -> cupcake(x))",
            "all x. (dried_Thai_chili(x) & (spicy(x) | bakery(x))) -> (hotpot(x) | spicy(x))"
        ]

conclusion = [
            "exists x. (dried_Thai_chili(x) & product_of_Baked_by_Melissa(x))"
        ]

if __name__ == '__main__':
    gen_counterexample(premises)
