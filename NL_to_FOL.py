import amrlib
import json
import re
from amrlib_master import amrlib
import openai
from amr_logic_converter import AmrLogicConverter


def read_json_file(file_path):
    # reading file in source
    with open(file_path) as user_file:
        data = user_file.read()

    objects = []
    depth = 0
    start = 0

    # Iterate over each character in the data
    for i, char in enumerate(data):
        if char == '{':
            if depth == 0:
                start = i  # Mark the start of a JSON object
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                # End of a JSON object
                objects.append(data[start:i + 1])

    # Convert string objects to dictionaries
    json_list = [json.loads(obj) for obj in objects]
    return json_list

# Function to split concatenated sentences into individual sentences
def split_sentences(input_list):
    result = []
    for text in input_list:
        # Split the text by newline characters
        sentences = re.split(r'\n', text)
        result.extend(sentences)
    return result

# Function to extract individual graphs from multi-sentence AMR input
def extract_individual_graphs(amr_list):
    individual_graphs = []
    for amr in amr_list:
        # Remove sentence annotations
        amr = '\n'.join([line for line in amr.split('\n') if not line.startswith('# ::snt')])
        individual_graphs.append(amr)
    return individual_graphs

def amr_conversion(premise, conclusion):
    # converting NL to AMR
    stog = amrlib.load_stog_model()
    premise = split_sentences(premise)
    premise_graphs = stog.parse_sents(premise)
    conclusion = split_sentences(conclusion)
    conclusion_graph = stog.parse_sents(conclusion)
    return premise_graphs, conclusion_graph


def amr_to_fol(amr):
    converter = AmrLogicConverter()
    logic = converter.convert(amr)
    return logic


def get_completion(prompt, model="gpt-4"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def fol_conversion(premise_graphs_list, conclusion_graphs_list):
    # upload openai key
    openai.api_key = "provide it here"

    # applying first prompt to generate fol
    prompt_1 = f"""
    Consider this example: "premises":"When the Monkeypox virus occurs in a being, it may get Monkeypox. \nMonkeypox virus can occur in certain animals.\nHumans are mammals.\nMammals are animals.\nSymptoms of Monkeypox include fever, headache, muscle pains, and tiredness. \nPeople feel tired when they get the flu.","premises-FOL":"exist x (OccurIn(monkeypoxVirus, x) & Get(x, monkeypoxVirus))\nexist x (Animal(x) & OccurIn(monkeypoxVirus, x))\nall x (Human(x) -> Mammal(x))\nall x (Mammal(x) -> Animal(x))\nexist x (SymptomOf(x, monkeypoxVirus) & (Fever(x) | Headache(x) | MusclePain(x) | Tired(x)))\nall x (Human(x) & Get(x, flu) -> Feel(x, tired)).","conclusion":"There is an animal.","conclusion-FOL":"exist x (Animal(x))"
    Using common sense, convert the given AMR to First Order Logic (FOL) with balanced parentheses as shown in the above example that will be acceptable by Prover9 
              /with the NLTK extension and ensure the FOL is well-formed and uses the following syntax: Logical AND: `&`, Logical OR: `|`,
              /Logical NOT: `~`, Implication: `->`. 
              /Apply negation to the entire quantified expression, not just to the variable.
            /Your output should be in JSON format with the keys "premise-fol" for {premise_graphs_list} with all FOL expressions in a single list and 
            /"conclusion-fol" for {conclusion_graphs_list} with all FOL expressions in a single list.
              """
    response_q = get_completion(prompt_1)
    print(response_q)
    return response_q


def processing_fol(file_path):
    # reading json file to get list of examples
    json_list = read_json_file(file_path)
    for example in json_list:
        premise = example["premises"]
        premise = [premise]
        print("premise:", premise)
        conclusion = example["conclusion"]
        conclusion = [conclusion]
        print("conclusion:", conclusion)
        actual_label = example["label"]
        print("actual_label:", actual_label)
        p_graph, c_graph = amr_conversion(premise, conclusion)
        print("p_graph:", p_graph)
        print("c_graph:", c_graph)
        '''
        # Extract individual AMR graphs
        individual_premise_amr = extract_individual_graphs(p_graph)
        individual_conclusion_amr = extract_individual_graphs(c_graph)

        # Save individual graphs to a list
        premise_graphs_list = individual_premise_amr
        conclusion_graphs_list = individual_conclusion_amr
        print(premise_graphs_list, conclusion_graphs_list)
        '''
        fol_dict = fol_conversion(p_graph, c_graph)
        # Parse the string into a Python dictionary to ensure it is valid JSON
        try:
            fol_json = json.dumps(fol_dict)  # Serialize dictionary to JSON
            fol_data = json.loads(fol_json)
            print("JSON parsed successfully!")
            yield fol_data, actual_label
        except json.JSONDecodeError as e:
            print("Failed to parse JSON:", e)


if __name__ == '__main__':
    for fol_data, actual_label in processing_fol("FOL dataset/test.json"):
        print(fol_data, type(fol_data))



