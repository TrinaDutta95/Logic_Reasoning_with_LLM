from nltk import *
import json
from NL_to_FOL import processing_fol
import csv


def ex_inference():
    read_expr = Expression.fromstring
    # example1
    p1 = read_expr('Person(x) | Music(y) | Listen(x,y) -> FeelEmotion(x)')
    p2 = read_expr('Person(jack)')
    p3 = read_expr('Music(moonlight_sonata) ')
    p4 = read_expr('Listen(jack,moonlight_sonata)')
    c = read_expr('FeelEmotion(jack)')
    print(type(p1))
    # example 2
    q1 = read_expr('(Person(Heinrich_Schmidt) & Politician(Heinrich_Schmidt) & PoliticalParty(Heinrich_Schmidt,Nazi) & Country(Heinrich_Schmidt,Germany))')
    d = read_expr('(Person(Heinrich_Schmidt) & Country(Heinrich_Schmidt,Germany))')

    p = Prover9().prove(c, [p1,p2,p3,p4])
    q = Prover9().prove(d, [q1])
    print(p,q)
    print(type(p))



def infer_fol(fol_data, actual_label):
    if isinstance(fol_data, str):
        fol_data = fol_data.replace("\n","")
        fol_data = json.loads(fol_data)  # Convert JSON string to dictionary
    read_expr = Expression.fromstring
    # Accessing data from the dictionary
    premise_fol = fol_data["premise-fol"]
    conclusion_fol = fol_data["conclusion-fol"]
    # print(premise_fol, "\n", conclusion_fol)
    premise_fol_data = [read_expr(premise) for premise in premise_fol]
    conclusion_fol_data = [read_expr(premise) for premise in conclusion_fol]
    # print(premise_fol, "\n", conclusion_fol)
    # Proving the conclusion based on the premise
    # Prover9 instance
    prover = Prover9()
    try:
        proof_result = prover.prove(conclusion_fol_data, assumptions=premise_fol_data)
        proof_result = "True" if proof_result else "False"
        print(proof_result, type(proof_result))
    except Exception as e:
        print("Error in proving:", e)
        proof_result = "None"

    return {
        "premises": " | ".join(premise_fol),
        "conclusion": " | ".join(conclusion_fol),
        "predicted_label": proof_result,
        "actual_label": actual_label
    }


if __name__ == '__main__':
    with open('result.json', 'w', newline='', encoding='utf-8') as file:
        for fol_data, actual_label in processing_fol("FOL dataset/test.json"):
            print(fol_data, type(fol_data))
            result = infer_fol(fol_data, actual_label)
            json_output = json.dumps(result)
            print(json_output)  # Print to console for debugging
            file.write(json_output + '\n')
    file.close()