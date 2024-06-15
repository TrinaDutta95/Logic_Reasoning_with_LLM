import json
from utils import convert_to_nltk_rep, evaluate

class FolioDatasetUpdater:
    def __init__(self, error_token):
        self.ERROR_TOKEN = error_token

    def reformat_fol_samples(self, dataset):
        count = 0
        def reformat_fol_sample(sample):
            nonlocal count
            sample["premises-FOL"] = [
                convert_to_nltk_rep(premise) for premise in sample["premises-FOL"]
            ]
            sample["conclusion-FOL"] = convert_to_nltk_rep(sample["conclusion-FOL"])
            try:
                assert len(sample["premises"]) == len(sample["premises-FOL"])
                label = evaluate(sample["premises-FOL"], sample["conclusion-FOL"])
                assert sample["label"] == label
            except Exception as e:
                print(f"Error in parsing FOL: {e}")
                print(sample)
                count = count + 1
                print(count)
                # sample["label"] = self.ERROR_TOKEN
            return sample

        return [reformat_fol_sample(sample) for sample in dataset]

    def load_dataset(self, file_path):
        dataset = []
        with open(file_path, 'r') as file:
            content = file.read()
            # Split the content into individual JSON objects
            objects = content.strip().split('\n')
            for obj in objects:
                # Parse each JSON object separately
                dataset.append(json.loads(obj))
        return dataset


    def save_dataset(self, dataset, file_path):
        with open(file_path, 'w') as file:
            json.dump(dataset, file, indent=4)

def remove_lines_from_file(input_file, output_file, lines_to_remove):
    """
    Remove specified lines from a file.

    :param input_file: Path to the input file.
    :param output_file: Path to the output file where the result will be saved.
    :param lines_to_remove: List of line numbers to remove (1-based index).
    """
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Remove the specified lines (convert 1-based index to 0-based)
    lines_to_remove = set(line - 1 for line in lines_to_remove)
    filtered_lines = [line for index, line in enumerate(lines) if index not in lines_to_remove]

    with open(output_file, 'w') as file:
        file.writelines(filtered_lines)


if __name__ == "__main__":
    # creating json files
    # preprocess()
    input_file = 'new_logic_llama_folio_validation.json'
    output_file = 'updated_logicllama_fol.json'
    lines_to_remove = [3, 6, 10, 11, 12, 28, 30, 48, 88, 106, 107, 108, 109, 110, 111, 113, 115, 139, 140, 174, 175,
                       176]  # specify the lines you want to remove

    remove_lines_from_file(input_file, output_file, lines_to_remove)
    updater = FolioDatasetUpdater(error_token="ERROR")
    # input_train_path = 'folio_train.json'
    # output_train_path = 'updated_folio_train.json'
    input_val_path = 'updated_logicllama_fol.json'
    output_val_path = 'updated_logic_llama_folio_validation.json'

    # Load the dataset
    # dataset_train = updater.load_dataset(input_train_path)
    dataset_val = updater.load_dataset(input_val_path)

    # Update the dataset
    # updated_train = updater.reformat_fol_samples(dataset_train)
    updated_val = updater.reformat_fol_samples(dataset_val)

    # Save the updated dataset
    # updater.save_dataset(updated_train, output_train_path)
    updater.save_dataset(updated_val, output_val_path)

    print(f"Dataset has been updated and saved to {output_val_path}")