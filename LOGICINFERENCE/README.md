# LOGICINFERENCE Dataset Repository
This repository hosts the LOGICINFERENCE dataset in JSON format, tailored for easier integration and manipulation in various machine learning projects. Originally designed to evaluate the ability of models to perform logical inference, the dataset here has been converted from the default TFRecord format to JSON files, enhancing accessibility and usability.

## About the LOGICINFERENCE Dataset
The LogicInference dataset focuses on propositional logic and a subset of first-order logic, presented in both semi-formal logical notation and natural language. It aims to:

1. Evaluate the capacity of models to execute logical inference and verify the authenticity of inference chains.
2. Investigate whether mastering abstract logical inference skills can be beneficial in real-world applications.
For more details on the dataset's design and purpose, refer to the [original paper](https://arxiv.org/abs/2203.15099).

## Citing the Dataset
If you use this dataset, please cite the original creators as follows:

```bibtex
@inproceedings{ontanon2022logicinference,
  url = {https://openreview.net/pdf?id=HAGeIS_Lcg9},
  author = {Onta\~{n}\'{o}n, Santiago and Ainslie, Joshua and Cvicek, Vaclav and Fisher, Zachary},
  title = {{LogicInference}: A New Dataset for Teaching Logical Inference to seq2seq Models},
  booktitle = {Proceedings of ICLR 2022 workshop on Objects, Structure and Causality},
  year = {2022}
}
```
## Dataset Generation
### Prerequisites
Before generating the dataset, ensure you have Python 3 installed.
```bash
pip install requirements.txt
```
### Instructions
1. Clone this repository to your local machine.
2. Navigate to the repository directory and open the `generate_dataset.py` file.
3. Modify the `TARGET_FOLDER` variable in generate_dataset.py to specify the desired output directory for the dataset.
4. Optionally, adjust other generation parameters within `generate_dataset.py` to tailor the dataset as needed.
5. Run the following command to generate the dataset:
```bash
python3 generate_dataset.py
```
This process may take some time as it generates all dataset splits (IID/OOD/length) simultaneously.

### Sample Data Generation
To generate and view sample data without creating the full dataset, run:
```bash
python3 generate_sample_data.py
```

### Format
Each example in the dataset is structured as a JSON object with two key-value pairs:

- `inputs`: Contains the logic problem in question.
- `targets`: Contains the expected logical conclusion.
This format is designed to be easily utilized by various data processing and machine learning frameworks.

### Contribution
Contributions to the dataset or the generation scripts are welcome. Please submit issues and pull requests as needed, adhering to the existing coding standards and practices.

Feel free to clone and adapt this repository to suit your needs, and consider sharing improvements or variations back with the community.