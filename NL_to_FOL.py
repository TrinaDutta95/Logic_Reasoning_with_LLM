import amrlib
import json
import re
from amrlib_master import amrlib
import openai


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


def amr_conversion(premise, conclusion):
    # converting NL to AMR
    stog = amrlib.load_stog_model()
    premise_graphs = stog.parse_sents(premise)
    conclusion_graph = stog.parse_sents(conclusion)
    print("premise_graphs:", premise_graphs)
    print("conclusion_graph:", conclusion_graph)
    return premise_graphs, conclusion_graph


def get_completion(prompt, model="gpt-4"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def fol_conversion(p_graph, c_graph):
    # upload openai key
    openai.api_key =  "provide_api_key"
    # applying first prompt to generate fol
    prompt_1 = f"""
              Consider the given example: "premises":"Books contain tons of knowledge.\nWhen a person reads a book, that person gains knowledge. \nIf a person gains knowledge, they become smarter.\nHarry read the book \u201cWalden\u201d by Henry Thoreau.","premises-FOL":"\u2200x (Book(x) \u2192 Contains(x, knowledge))\n\u2200x \u2200y (ReadBook(x, y) \u2192 Gains(x, knowledge))\n\u2200x (Gains(x, knowledge) \u2192 Smarter(x))\nReadBook(harry, walden) \u2227 Book(walden)","conclusion":"Harry is smarter than before.","conclusion-FOL":"Smarter(harry)","label":"True"
              For the given premise amr graph and conclusion amr graph, convert them to explicit First Order
              Logic (fol) covering all the implicit relations following the same structure of the given example. Use the json format for your response with keys "premise-FOL" and "conclusion-FOL"
              {p_graph},{c_graph}
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
        fol_dict = fol_conversion(p_graph, c_graph)
        # Parse the string into a Python dictionary to ensure it is valid JSON
        try:
            fol_json = json.dumps(fol_dict)  # Serialize dictionary to JSON
            fol_data = json.loads(fol_json)
            print("JSON parsed successfully!")
            yield fol_data, actual_label
        except json.JSONDecodeError as e:
            print("Failed to parse JSON:", e)




