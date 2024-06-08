from nltk import *
import json
from NL_to_FOL import processing_fol
from data.utils import *

read_expr = Expression.fromstring
prover = Prover9()


def evaluate(premises, conclusion):
    truth_value = prover.prove(conclusion, premises)
    if truth_value:
        return "True"
    else:
        neg_c = read_expr("-(" + conclusion + ")")
        negation_true = prover.prove(neg_c, premises)
        if negation_true:
            return "False"
        else:
            return "Uncertain"


def infer_fol(fol_data, actual_label):
    if isinstance(fol_data, str):
        fol_data = fol_data.replace("\n","")
        fol_data = json.loads(fol_data)  # Convert JSON string to dictionary

    # Accessing data from the dictionary
    try:
        # reformat fol
        '''
        fol_data["premise-fol"] = [
            convert_to_nltk_rep(premise) for premise in fol_data["premise-fol"]
        ]
        fol_data["conclusion-fol"] = [
            convert_to_nltk_rep(premise) for premise in fol_data["conclusion-fol"]
        ]
        '''
        premise_fol = fol_data["premise-fol"]
        conclusion_fol = fol_data["conclusion-fol"]
        print(premise_fol)

        # print(premise_fol, "\n", conclusion_fol)
        premise_fol_data = [read_expr(premise) for premise in premise_fol]
        conclusion_fol_data = [read_expr(premise) for premise in conclusion_fol]

        # print(premise_fol, "\n", conclusion_fol)

        try:
            proof_result = evaluate(premise_fol_data, conclusion_fol_data)
            print(proof_result, type(proof_result))
        except Exception as e:
            print("Error in proving:", e)
            proof_result = "None"
    except KeyError as ke:
        print("KeyError in accessing premise or conclusion:", ke)
        premise_fol = []
        conclusion_fol = []
        proof_result = "None"

    return {
        "premises": " | ".join(premise_fol),
        "conclusion": " | ".join(conclusion_fol),
        "predicted_label": proof_result,
        "actual_label": actual_label
    }


if __name__ == '__main__':
    with open('result.json', 'w', newline='', encoding='utf-8') as file:
        for fol_data, actual_label in processing_fol("data/test.json"):
            print(fol_data, type(fol_data))
            result = infer_fol(fol_data, actual_label)
            json_output = json.dumps(result)
            print(json_output)  # Print to console for debugging
            file.write(json_output + '\n')
    file.close()