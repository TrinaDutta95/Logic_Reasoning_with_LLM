from nltk import *
import json
from NL_to_FOL import processing_fol


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


def preprocess_fol(data):
    # First replace '∧' with '&'
    processed_data = data.replace("∧", "&")

    # Then check for commas to split into multiple premises
    if "," in processed_data:
        premises = []
        depth = 0
        last_split = 0
        for i, char in enumerate(processed_data):
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            elif char == ',' and depth == 0:
                premises.append(processed_data[last_split:i].strip())
                last_split = i + 1
        premises.append(processed_data[last_split:].strip())  # add the last premise
        return premises

    # If there are no commas to split, return the data as a single item list
    return [processed_data]


def infer_fol(fol_data):
    read_expr = Expression.fromstring
    # Accessing data from the dictionary
    premise_fol = preprocess_fol(fol_data["premise-FOL"])
    conclusion_fol = preprocess_fol(fol_data["conclusion-FOL"])
    # print(premise_fol, "\n", conclusion_fol)
    premise_fol = [read_expr(premise) for premise in premise_fol]
    conclusion_fol = read_expr(conclusion_fol[0])  # Assuming only one conclusion
    # print(premise_fol, "\n", conclusion_fol)
    # Proving the conclusion based on the premise
    # Prover9 instance
    prover = Prover9()
    try:
        proof_result = prover.prove(conclusion_fol, assumptions=premise_fol)
        return proof_result
    except Exception as e:
        print("Error in proving:", e)
        return None


if __name__ == '__main__':
    for fol_data in processing_fol("FOL dataset/test_folio.json"):
        print(json.dumps(fol_data, indent=2))
        print(infer_fol(fol_data))