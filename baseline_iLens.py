from nltk import *
import json
from data.utils import *

read_expr = Expression.fromstring
prover = Prover9()


def read_json(filepath):
    with open(filepath, 'r', newline='', encoding='utf-8') as file:
        data = json.load(file)
    # Extract "premise-fol" and "conclusion-fol" fields
    extracted_data = []
    for obj in data:
        extracted_obj = {
            "premise-fol": obj.get("premise-fol", []),
            "conclusion-fol": obj.get("conclusion-fol", []),
            "premises": obj.get("premises", []),
            "conclusion": obj.get("conclusion", []),
            "label": obj.get("label", []),
        }
        extracted_data.append(extracted_obj)

    return extracted_data


def evaluate(conclusion, premises):
    premise_fol_data = []
    for premise in premises:
        premise = read_expr(premise)
        # print(premise)
        premise_fol_data.append(premise)

    conclusion_fol_data = read_expr(conclusion[0])

    truth_value = prover.prove(conclusion_fol_data, premise_fol_data)
    if truth_value:
        return "True"
    else:
        neg_c = read_expr("-(" + conclusion[0] + ")")
        neg_c = read_expr(conclusion[0])
        print(neg_c)
        negation_true = prover.prove(neg_c, premise_fol_data)
        if negation_true:
            return "False"
        else:
            return "Uncertain"


def baseline_infer(fol_data):
    results = []  # Store results for each example

    for item in fol_data:
        # Accessing data from the dictionary
        premises = item.get("premises", [])
        conclusion = item.get("conclusion", [])
        label = item.get("label", [])
        premise_fol = item.get("premise-fol", [])
        conclusion_fol = item.get("conclusion-fol", [])
        # print(premise_fol, "\n", conclusion_fol)

        try:
            premise_fol_data = []
            for premise in premise_fol:
                premise = read_expr(premise)
                # print(premise)
                premise_fol_data.append(premise)

            conclusion_fol_data = read_expr(conclusion_fol[0])

            print(premise_fol_data, "\n", conclusion_fol_data)

            try:
                proof_result = evaluate(conclusion_fol, premise_fol)
                print(proof_result)
                print("Proved successfully")
                error = None
            except Exception as e:
                print("Error in proving:", e)
                proof_result = "ERROR"
                error = str(e)
        except KeyError as ke:
            print("KeyError in accessing premise or conclusion:", ke)
            proof_result = "ERROR"
            error = str(ke)

        results.append({
            "premise": premises,
            "conclusion": conclusion,
            "premise-fol": premise_fol,
            "conclusion-fol": conclusion_fol,
            "actual_label": label,
            "predicted_label": proof_result,
            "error": error
        })
    return results


if __name__ == '__main__':
    with open('results/baseline_result.json', 'w', encoding='utf-8') as file:
        fol_data = read_json("data/merged_file.json")
        results = baseline_infer(fol_data)
        results_json = json.dumps(results, indent=4)
        file.write(results_json)