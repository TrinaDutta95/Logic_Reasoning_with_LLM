import json

# Function to read the JSON data from a file
def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Function to transform the data format
def transform_data(fol_data):
    transformed_data = []
    for item in fol_data:
        new_item = {
            "premises-FOL": item.get("premises-FOL", []),
            "conclusion-FOL": item.get("conclusion-FOL", []),
        }
        transformed_data.append(new_item)
    return transformed_data

# Function to write the transformed data to a file
def write_transformed_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            json_line = json.dumps(item, ensure_ascii=False)
            f.write(json_line + '\n')


if __name__ == '__main__':
    # Read the input data
    fol_data = read_json("logic_llama_folio_validation.json")

    # Transform the data
    transformed_data = transform_data(fol_data)

    # Write the transformed data to a new file
    write_transformed_data("new_logic_llama_folio_validation.json", transformed_data)
