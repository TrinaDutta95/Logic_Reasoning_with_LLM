import json

def main():
    # Load the JSON files
    with open('data/updated_folio_validation.json', 'r') as f1, open('data/fol_from_amr_gpt4.json', 'r') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    # Define the keys to transfer
    keys_to_transfer = ["premises", "conclusion", "label"]

    # Check if both files have the same length of JSON objects
    if len(data1) != len(data2):
        raise ValueError("The two JSON files must have the same number of JSON objects")

    # Merge the specified keys from data1 to data2
    for obj1, obj2 in zip(data1, data2):
        for key in keys_to_transfer:
            if key in obj1:
                obj2[key] = obj1[key]

    # Save the merged result to a new file
    with open('data/merged_file.json', 'w') as f_out:
        json.dump(data2, f_out, indent=4)

    print("Merging completed. The result is saved in 'merged_file.json'")


if __name__ == '__main__':
    main()
