from iLens_gpt4 import *
read_expr = Expression.fromstring
prover = Prover9()
mace = Mace()


def main(fol_data):

    results = []  # Store results for each example
    api_key = "add your api key here"
    for item in fol_data:
        # Accessing data from the dictionary
        premises = item.get("premises", [])
        print(premises)
        conclusion = item.get("conclusion", [])
        actual_label = item.get("actual_label", [])
        predicted_label = item.get("predicted_label", [])
        error = item.get("error", [])
        premise_fol = item.get("premise-fol", [])
        len_premise = len(premises)
        len_new_premise = 0
        conclusion_fol = item.get("conclusion-fol", [])
        count = 1
        while count < 5 and len_new_premise < 3*len_premise:
            if predicted_label == "Uncertain" and actual_label != "Uncertain":
                print("Pass1")
                count = count + 1
                print("premise:", premises, "\n", "conclusion:", conclusion, "\n", "premise_fol:", premise_fol, "\n", "conclusion_fol:", conclusion_fol, "actual_label:", actual_label, "\n", "predicted_label:", predicted_label, "\n", "error:", error)
                proof_result, premise, conclusion, premise_fol, conclusion_fol, error = iter_inference_with_mace(premises, conclusion, premise_fol, conclusion_fol, actual_label, predicted_label, error, api_key)
                predicted_label = proof_result
            elif predicted_label == "ERROR":
                count = count + 1
                print("premise:", premises, "\n", "conclusion:", conclusion, "\n", "premise_fol:", premise_fol, "\n",
                      "conclusion_fol:", conclusion_fol, "actual_label:", actual_label, "\n", "predicted_label:",
                      predicted_label, "\n", "error:", error)
                print("Pass2")
                fol_data, actual_label = iter_inference_for_error(premise_fol, conclusion_fol, actual_label, predicted_label, error, api_key)
                print(fol_data, actual_label)
                proof_result, premise_fol, conclusion_fol, error = get_result(fol_data, conclusion_fol)
                predicted_label = proof_result
            else:
                print("Pass3")
                count = count + 1
                proof_result = predicted_label

            len_new_premise = len(premise_fol)

        results.append({"predicted_label": proof_result, "actual_label": actual_label, "error": error})
    return results


if __name__ == '__main__':
    with open('results/test_result.json', 'w', encoding='utf-8') as f:
        fol_data = read_json("data/test.json")
        results = main(fol_data)
        results_json = json.dumps(results, indent=4)
        f.write(results_json)










