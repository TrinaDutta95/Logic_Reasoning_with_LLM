from datasets import load_dataset
import os
import pandas as pd
from huggingface_hub import HfApi, HfFolder

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


if __name__ == "__main__":
    # creating json files
    preprocess()