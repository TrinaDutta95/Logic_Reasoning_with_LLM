# Ongoing work on integrating Large Language Models(LLM) with logical reasoning
This project is to improve task of inference with logic. Natural Language(NL) Premises and Conclusions are converted to First order Logic(FOL) using LLM. We try to fix certain errors in this 
conversion and ambiguity present in NL.

## Dataset
We have considered `FOLIO` and `LOGICINFERENCE` dataset.

## Logic Reasoning Inference
We are using [Prover9](https://www.cs.unm.edu/~mccune/prover9/) extension from NLTK. For more details on installation [check here](https://www.nltk.org/howto/inference.html).

## Prerequisites and Installation
You will need Python installed. Prover9 works only on Linux and mac os x right now. So, for those devices follow these steps to install Prover9
- Download [Prover9](https://www.cs.unm.edu/~mccune/prover9/download/)
- Run the following commands
```bash
% zcat LADR-2009-11A.tar.gz | tar xvf -
% cd LADR-2009-11A
% make all
```
- After it runs successfully, move the Prover9 into an appropriate location(one of the following)
```bash
['/usr/local/bin/prover9',
 '/usr/local/bin/prover9/bin',
 '/usr/local/bin',
 '/usr/bin',
 '/usr/local/prover9',
 '/usr/local/share/prover9']
```
- You will also need NLTK library
```bash
pip install nltk
```
## Usage 
```bash
python Inference_Prover9.py
```
