from nltk import *
import json
from data.utils import *
import openai
from baseline_iLens import evaluate
from NL_to_FOL import get_completion
read_expr = Expression.fromstring
prover = Prover9()
mace = Mace()


def read_json(filepath):
    with open(filepath, 'r', newline='', encoding='utf-8') as file:
        data = json.load(file)
    # Extract "premise-fol" and "conclusion-fol" fields
    extracted_data = []
    for obj in data:
        extracted_obj = {
            "premises": obj.get("premise", []),
            "conclusion": obj.get("conclusion", []),
            "premise-fol": obj.get("premise-fol", []),
            "conclusion-fol": obj.get("conclusion-fol", []),
            "actual_label": obj.get("actual_label", []),
            "predicted_label": obj.get("predicted_label", []),
            "error": obj.get("error", [])
        }
        extracted_data.append(extracted_obj)

    return extracted_data


def gen_counterexample(premise_fol):
    premise_fol_data = []
    for premise in premise_fol:
        premise = read_expr(premise)
        # print(premise)
        premise_fol_data.append(premise)
    print("premise to fol output:", premise_fol_data)
    mb = MaceCommand(assumptions=premise_fol_data)  # , max_models=1)
    mb.build_model()
    result = mb.model(format='cooked')
    print("mace model:", result)
    return str(result)


def gen_updatednl(counter_example, premises, conclusion, api_key):
    """
        Update the First Order Logic (FOL) statements with Mace4 counterexamples using the OpenAI API.

        Parameters:
        counter_example (str): the FOL-counterexample
        premises (list): the list of premises
        conclusion (str): the conclusion
        api_key (str): OpenAI API key.

        Returns:
        dict: A dictionary with "premise-fol" and "conclusion-fol" keys containing the converted FOL expressions.
        """
    openai.api_key = api_key
    prompt_2 = f"""Your task is to read and understand the {counter_example} generated from Mace4 and use 
    /common sense knowledge to find any missing information or logic chain and generate First Order Logic (FOL) from the 
    /provided natural language {premises} and {conclusion}.
    Follow the given example for format and syntax.
    Example:
    "premises": [
            "If people perform in school talent shows often, then they attend and are very engaged with school events.",
            "People either perform in school talent shows often or are inactive and disinterested members of their community.",
            "If people chaperone high school dances, then they are not students who attend the school.",
            "All people who are inactive and disinterested members of their community chaperone high school dances.",
            "All young children and teenagers who wish to further their academic careers and educational opportunities are students who attend the school.",
            "Bonnie either both attends and is very engaged with school events and is a student who attends the school, or she neither attends and is very engaged with school events nor is a student who attends the school. "
        ],
        "premises-FOL": [
            "all x. (TalentShows(x) -> Engaged(x))",
            "all x. (TalentShows(x) | Inactive(x))",
            "all x. (Chaperone(x) -> -Students(x))",
            "all x. (Inactive(x) -> Chaperone(x))",
            "all x. (AcademicCareer(x) -> Students(x))",
            "(((Engaged(Bonnie) & Students(Bonnie)) & -(-Engaged(Bonnie) & -Students(Bonnie))) | (-(Engaged(Bonnie) & Students(Bonnie)) & (-Engaged(Bonnie) & -Students(Bonnie))))"
        ],
        "conclusion": "If Bonnie is either both a young child or teenager who wishes to further her academic career and educational opportunities and chaperones high school dances or neither is a young child nor teenager who wishes to further her academic career and educational opportunities, then Bonnie is either a student who attends the school or is an inactive and disinterested member of the community.",
        "conclusion-FOL": "((AcademicCareer(Bonnie) & -Chaperone(Bonnie)) | (-AcademicCareer(Bonnie) & Chaperone(Bonnie))) -> ((AcademicCareer(Bonnie) & -Inactive(Bonnie)) | (-AcademicCareer(Bonnie) & Inactive(Bonnie)))"
    Ensure that:
    - Each FOL expression follows the correct syntax: Logical AND: `&`, Logical OR: `|`, Logical NOT: `-`, Implication: `->`.
    - Symbols are consistently used as either predicates or functions with consistent arities.
    - Quantifiers are correctly placed 
    - No quotations are required for any proper noun.
    - The FOL expressions are valid and well-formed for use in theorem provers like Prover9.
    - Make sure the FOL expressions are consistent, syntactically correct, and have balanced parentheses.
    - Make sure the output is not like a chat response.
    
     Your output should be a dictionary with the keys "premises-FOL" for premises with all FOL expressions
    /in a single list and "conclusion-FOL" for conclusion with FOL expression in a single list.
    """
    response = get_completion(prompt_2)
    return response


def fix_error(premise_fol, conclusion_fol, error, api_key):
    """
            Fix the First Order Logic (FOL) from the given error using the OpenAI API.

            Parameters:
            premise_fol (list): List of premises in FOL format.
            conclusion_fol (list): List of conclusions in FOL format.
            error (str): The error message.
            api_key (str): OpenAI API key.

            Returns:
            dict: A dictionary with "premise-fol" and "conclusion-fol" keys containing the converted FOL expressions.
            """
    openai.api_key = api_key
    prompt_3 = f"""Your task is to fix some errors in first order logic statements. 
    /I will provide you with the {error} and the first order logic {premise_fol} and 
    /{conclusion_fol} such that they do not contain that error. 
    Follow the given example for format and syntax.
    
    Ensure that:
    - The FOL expressions are valid and well-formed for use in theorem provers like Prover9 with consistent arities..
    - Make sure the FOL expressions are consistent, syntactically correct, and have balanced parentheses.
    - Do not describe your answer like a chat response.
    - Your output should only contain the fixed fol expressions in dictionary format with keys "premises-FOL" and 
    /"conclusion-FOL".

        """
    response = get_completion(prompt_3)
    return response


def iter_inference_with_mace(premises, conclusion, premise_fol, conclusion_fol, actual_label, predicted_label, error, api_key):
    counter_example = gen_counterexample(premise_fol)
    print("hello")
    print(counter_example)
    fol_dict = gen_updatednl(counter_example, premises, conclusion, api_key)
    fol_data = json.loads(fol_dict)
    print(type(fol_data))
    proof_result, premise_fol, conclusion_fol, error = get_result(fol_data)
    return proof_result, premises, conclusion, premise_fol, conclusion_fol, error


def get_result(fol_data):
    print(fol_data)
    # Accessing data from the dictionary
    premise_fol = fol_data.get("premises-FOL", [])
    conclusion_fol = fol_data.get("conclusion-FOL", [])
    print(premise_fol, conclusion_fol)
    try:
        proof_result = evaluate(conclusion_fol, premise_fol)
        print(proof_result)
        print("Proved successfully")
        error = None
    except Exception as e:
        print("Error in proving:", e)
        proof_result = "ERROR"
        error = str(e)
    return proof_result, premise_fol, conclusion_fol, error


def iter_inference_for_error(premise_fol, conclusion_fol, actual_label, predicted_label, error, api_key):
    print(premise_fol, conclusion_fol, actual_label, predicted_label, error)
    print(type(error))
    fol_dict = fix_error(premise_fol, conclusion_fol, error, api_key)
    print(type(fol_dict))
    fol_json = json.dumps(fol_dict)
    print(type(fol_json))
    fol_data = json.loads(fol_json)
    print(type(fol_data))
    print(fol_data)
    return fol_data, actual_label


def main(fol_data):
    results = []  # Store results for each example
    api_key = "add api key here"
    for item in fol_data:
        # Accessing data from the dictionary
        premises = item.get("premises", [])
        print(premises)
        conclusion = item.get("conclusion", [])
        actual_label = item.get("label", [])
        predicted_label = item.get("predicted_label", [])
        error = item.get("error", [])
        premise_fol = item.get("premise-fol", [])
        conclusion_fol = item.get("conclusion-fol", [])

        if predicted_label == "Uncertain" and actual_label != "Uncertain":
            print("Pass1")
            print("premise:", premises, "\n", "conclusion:", conclusion, "\n", "premise_fol:", premise_fol, "\n", "conclusion_fol:", conclusion_fol)
            proof_result, premise, conclusion, premise_fol, conclusion_fol, error = iter_inference_with_mace(premises, conclusion, premise_fol, conclusion_fol, actual_label, predicted_label, error, api_key)
            if proof_result == "Uncertain":
                print("Pass1-1")
                proof_result, premise, conclusion, premise_fol, conclusion_fol, error = iter_inference_with_mace(premises, conclusion, premise_fol, conclusion_fol, actual_label, predicted_label, error, api_key)
            elif proof_result == "ERROR":
                print("Pass1-2")
                fol_dict = fix_error(premise_fol, conclusion_fol, error, api_key)
                fol_data = json.loads(fol_dict)
                print(type(fol_data))
                proof_result, premise_fol, conclusion_fol, error = get_result(fol_data)
        elif predicted_label == "ERROR":
            print("Pass2")
            fol_data, actual_label = iter_inference_for_error(premise_fol, conclusion_fol, actual_label, predicted_label, error, api_key)
            print(fol_data, actual_label)
            proof_result, premise_fol, conclusion_fol, error = get_result(fol_data)
            if proof_result == "Uncertain":
                print("Pass2-1")
                proof_result, premise, conclusion, premise_fol, conclusion_fol, error = iter_inference_with_mace(premises, conclusion, premise_fol, conclusion_fol, actual_label, predicted_label, error, api_key)
            elif proof_result == "ERROR":
                print("Pass2-2")
                fol_dict = fix_error(premise_fol, conclusion_fol, error, api_key)
                fol_data = json.loads(fol_data)
                print(type(fol_data))
                proof_result, premise_fol, conclusion_fol, error = get_result(fol_data)
        else:
            print("Pass3")
            proof_result = predicted_label
        results.append({"predicted_label": proof_result, "actual_label": actual_label})
    return results


if __name__ == '__main__':
    with open('results/test_result.json', 'w', encoding='utf-8') as f:
        fol_data = read_json("data/test.json")
        results = main(fol_data)
        results_json = json.dumps(results, indent=4)
        f.write(results_json)










