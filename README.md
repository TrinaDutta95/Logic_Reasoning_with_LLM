# Ongoing work on integrating Large Language Models(LLM) with logical reasoning
This project is to improve task of inference with logic. Natural Language(NL) Premises and Conclusions are converted to First order Logic(FOL) using LLM. We try to fix certain errors in this 
conversion and ambiguity present in NL.

## Dataset
We have considered `FOLIO` and `LOGICINFERENCE` dataset.

## Logic Reasoning Inference
We are using [Prover9](https://www.cs.unm.edu/~mccune/prover9/) extension from NLTK. For more details on installation [check here](https://www.nltk.org/howto/inference.html).

## Prerequisites and Installation
You will need Python installed. 
### Prover9 installation
Prover9 works only on Linux and mac os x right now. So, for those devices follow these steps to install Prover9
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
- You will also need NLTK library and amrlib
```bash
pip install nltk, amrlib
```
### amrlib Installation
Please check the original [repository](https://github.com/bjascob/amrlib) to install amrlib models
## Usage 
To run example Prover9 inference with proof steps (need to move prooftrans into '/usr/local/bin/'), and there are two methods (Prover9Command and ResolutionProver) can do same task.
```bash
python prover9_test.py
```
To run example Prover9 inference
```bash
python Inference_Prover9.py
```
To convert NL to AMR to FOL, you will need openai==0.28.0 and openai_key
```bash
python NL_to_FOL.py
```
