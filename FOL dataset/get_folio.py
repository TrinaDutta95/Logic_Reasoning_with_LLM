import requests

def preprocess():
    val_url = "https://raw.githubusercontent.com/Yale-LILY/FOLIO/main/data/v0.0/folio-validation.jsonl"
    train_url = "https://raw.githubusercontent.com/Yale-LILY/FOLIO/main/data/v0.0/folio-train.jsonl"

    val_filename = 'folio_validation.json'
    train_filename = 'folio_train.json'

    # Download the file
    response = requests.get(val_url)
    with open(val_filename, 'wb') as f:
        f.write(response.content)

    response = requests.get(train_url)
    with open(train_filename, 'wb') as f:
        f.write(response.content)

    print(f"Downloaded {train_filename}")


if __name__ == "__main__":
    # creating json files
    preprocess()