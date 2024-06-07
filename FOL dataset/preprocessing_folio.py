from datasets import load_dataset
import os, json
from huggingface_hub import HfApi, HfFolder
import pandas as pd
from utils import convert_to_nltk_rep, evaluate


def preprocess():
    os.environ['HF_TOKEN'] = 'add hf token here'
    # Authenticate using the HF token from the environment variable
    token = os.getenv('HF_TOKEN')
    if not token:
        raise ValueError("No Hugging Face token found. Set the HF_TOKEN environment variable.")

    HfFolder.save_token(token)  # Saves token to Hugging Face folder for subsequent requests
    # Load the dataset from Hugging Face
    dataset = load_dataset("yale-nlp/FOLIO")

    # Removing unwanted columns
    train = dataset['train'].remove_columns(['example_id', 'story_id'])
    validation = dataset['validation'].remove_columns(['example_id', 'story_id'])

    # Save the modified datasets as JSON
    train.to_json('folio_train.json')
    validation.to_json('folio_validation.json')
    print("Datasets saved as 'train.json' and 'validation.json'")


def convert_json_to_csv(json_filepath, csv_filepath):
    # Load the JSON file into a DataFrame
    df = pd.read_json(json_filepath, lines=True)  # use lines=True if your JSON is in jsonl format

    # Save the DataFrame to a CSV file
    df.to_csv(csv_filepath, index=False)
    print(f"Converted {json_filepath} to {csv_filepath}")


class FolioDatasetUpdater:
    def __init__(self, error_token):
        self.ERROR_TOKEN = error_token

    def reformat_fol_samples(self, dataset):
        def reformat_fol_sample(sample):
            sample["premises-FOL"] = [
                convert_to_nltk_rep(premise) for premise in sample["premises-FOL"]
            ]
            sample["conclusion-FOL"] = convert_to_nltk_rep(sample["conclusion-FOL"])
            try:
                assert len(sample["premises"]) == len(sample["premises-FOL"])
                label = evaluate(sample["premises-FOL"], sample["conclusion-FOL"])
                assert sample["label"] == label
            except Exception as e:
                # print(f"Error in parsing FOL: {e}")
                # print(sample)
                sample["label"] = self.ERROR_TOKEN
            return sample

        return [reformat_fol_sample(sample) for sample in dataset if sample["label"] != self.ERROR_TOKEN]

    def load_dataset(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def save_dataset(self, dataset, file_path):
        with open(file_path, 'w') as file:
            json.dump(dataset, file, indent=4)


if __name__ == "__main__":
    # creating json files
    # preprocess()
    updater = FolioDatasetUpdater(error_token="ERROR")
    input_train_path = '/folio_train.json'
    output_train_path = '/updated_folio_train.json'
    input_val_path = 'folio_validation.json'
    output_val_path = 'updated_folio_validation.json'

    # Load the dataset
    dataset_train = updater.load_dataset(input_train_path)
    dataset_val = updater.load_dataset(input_val_path)

    # Update the dataset
    updated_train = updater.reformat_fol_samples(dataset_train)
    updated_val = updater.reformat_fol_samples(dataset_val)

    # Save the updated dataset
    updater.save_dataset(updated_train, output_train_path)
    updater.save_dataset(updated_val, output_val_path)

    print(f"Dataset has been updated and saved to {output_train_path}{output_val_path}")

