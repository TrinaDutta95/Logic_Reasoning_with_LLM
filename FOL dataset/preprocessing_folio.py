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
                sample["label"] = self.ERROR_TOKEN
            return sample

        return [reformat_fol_sample(sample) for sample in dataset if sample["label"] != self.ERROR_TOKEN]

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


if __name__ == "__main__":
    # creating json files
    # preprocess()
    updater = FolioDatasetUpdater(error_token="ERROR")
    # input_train_path = 'folio_train.json'
    # output_train_path = 'updated_folio_train.json'
    input_val_path = 'folio_validation.json'
    output_val_path = 'updated_folio_validation.json'

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