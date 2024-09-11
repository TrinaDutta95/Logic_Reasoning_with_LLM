import json


def preprocess_logicnli():
    with open("./LogicNLI_test.json", "r") as f:
        lines = f.readlines()

    # List to store modified entries
    modified_dataset = []

    # Mapping for changing the labels
    label_map = {
        "entailment": "True",
        "contradiction": "False",
        "neutral": "Unknown"
    }

    # Process each line (each entry)
    for line in lines:
        # Parse the JSON object
        entry = json.loads(line)

        # Modify the "label" field if it's in the mapping
        if entry['label'] in label_map:
            entry['label'] = label_map[entry['label']]

        # Append the modified entry to the list
        modified_dataset.append(entry)

    # Save the modified dataset back to a new JSON file
    with open("./LogicNLI_test_modified.json", "w") as f:
        for entry in modified_dataset:
            # Write each modified entry as a new line in the JSON file
            f.write(json.dumps(entry) + "\n")


if __name__ == "__main__":
    # creating json files
    preprocess_logicnli()