import json
from conversions import *


def processing_fol(file_path):
    # reading json file to get list of examples
    api_key = "your key here"
    with open(file_path, 'r') as f:
        json_list = json.load(f)
        print(json_list)
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

            fol_dict = fol_conversion(p_graph, c_graph, api_key)
            # Parse the string into a Python dictionary to ensure it is valid JSON
            try:
                fol_json = json.dumps(fol_dict)
                print(fol_json)  # Serialize dictionary to JSON
                fol_data = json.loads(fol_json)
                print("JSON parsed successfully!")
                yield fol_data, actual_label
            except json.JSONDecodeError as e:
                print("Failed to parse JSON:", e)


if __name__ == '__main__':
    with open("data/fol_logiqa.json", "a") as f:  # add file that you want to store data at
        for fol_data, actual_label in processing_fol("data/test1.json"):  # add file which you want to process
            print(fol_data, type(fol_data))
            f.write(fol_data + '\n')



