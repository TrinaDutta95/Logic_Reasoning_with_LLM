# FOLIO Dataset Enhancement Repository
This repository contains the Python script preprocessing_folio.py which updates and preprocesses the FOLIO dataset. FOLIO is an expert-written, open-domain dataset designed for natural language reasoning using first-order logic. The script modifies specific columns or attributes and outputs two JSON files, one for training and another for validation.

## About the FOLIO Dataset
FOLIO stands for Natural Language Reasoning with First-Order Logic and provides logically complex and diverse datasets for training machine learning models in tasks that involve logical reasoning. The dataset includes:

- Premises in natural language
- First-Order Logic (FOL) formula annotations for the premises
- Natural language conclusions
- FOL formula annotations for the conclusions
- Truth value labels for the conclusions
- Unique identifiers for stories and individual examples
- Source tags indicating whether the data is from the WikiLogic or HybLogic sets
For further details on the dataset, including methodology and analyses, refer to the [associated paper](https://arxiv.org/pdf/2209.00840).

## Data Format and Structure
The dataset is updated in JSON format with the following structure for each entry:

- premises: Natural language premises
- premises-FOL: FOL annotations for the premises
- conclusion: Natural language conclusion
- conclusion-FOL: FOL annotations for the conclusion
- label: Truth value label for the conclusion

## Requirements
- Ensure you have Python and datasets installed on your machine.
```bash
pip install requirements.txt
```
- You need to set Hugging Face login through tokens:
** For Windows: `set HF_TOKEN=your_actual_token_here`
** On macOS/Linux: `export HF_TOKEN=your_actual_token_here`



## Instructions
- Clone this repository to your local environment.
- Navigate to the directory containing preprocessing_folio.py.
Run the script using Python:
```bash
python preprocessing_folio.py
```
This will generate two files: `updated_folio_train.json` and `updated_folio_validation.json` in the specified output directory.
## Contribution
We encourage contributions from the community. If you have data points to add or enhancements to the preprocessing logic, please submit a pull request.

## Citation
If you use the FOLIO dataset or this preprocessing utility, please cite the original work:

```bibtex
@article{han2022folio,
  title={FOLIO: Natural Language Reasoning with First-Order Logic},
  author={Han, Simeng and others},
  journal={arXiv preprint arXiv:2209.00840},
  url={https://arxiv.org/abs/2209.00840},
  year={2022}
}```
