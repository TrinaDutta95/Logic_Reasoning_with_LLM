from nltk.sem import Expression
from nltk.inference import MaceCommand

read_expr = Expression.fromstring


def gen_counterexample(premise_fol):
    try:
        premise_fol_data = [read_expr(premise) for premise in premise_fol]
        print("Premises (FOL):", [str(expr) for expr in premise_fol_data])

        mb = MaceCommand(premise_fol_data, max_models=1)
        mb.build_model()
        print("mace model:", mb.model(format='cooked'))
    except Exception as e:
        print("Error generating model:", str(e))
        return None



# Example usage with your premises:
premises = [
    "all x. (bakery(x) -> -spicy(x))",
    "all x. (cupcake(x) -> bakery(x))",
    "all x. (hotpot(x) -> spicy(x))",
    "all x. (product_of_Baked_by_Melissa(x) -> cupcake(x))",
    "all x. ((dried_Thai_chili(x) & (spicy(x) | bakery(x))) -> (hotpot(x) | spicy(x)))"
]

if __name__ == '__main__':
    gen_counterexample(premises)
