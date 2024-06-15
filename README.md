# Ongoing work on integrating Large Language Models(LLM) with logical reasoning- ILENS: Iterative Logical Enhancement via Neurosymbolic Computation and Common Sense
This project is to improve task of inference with logic. Natural Language(NL) Premises and Conclusions are converted to First order Logic(FOL) using LLM. We try to fix certain errors in this 
conversion and ambiguity present in NL.

## Dataset
We have considered `FOLIO` dataset.
## Citation
If you use the FOLIO dataset or this preprocessing utility, please cite the original works:

```bibtex
@article{han2022folio,
  title={FOLIO: Natural Language Reasoning with First-Order Logic},
  author={Han, Simeng and others},
  journal={arXiv preprint arXiv:2209.00840},
  url={https://arxiv.org/abs/2209.00840},
  year={2022}
}
```

```bibtex
@inproceedings{OGLZ_LINC_2023,
	author={Theo X. Olausson* and Alex Gu* and Ben Lipkin* and Cedegao E. Zhang* and Armando Solar-Lezama and Joshua B. Tenenbaum and Roger P. Levy},
	title={LINC: A neuro-symbolic approach for logical reasoning by combining language models with first-order logic provers},
	year={2023},
	journal={Proceedings of the Conference on Empirical Methods in Natural Language Processing},
}
```

## Logic Reasoning Inference
We are using [Prover9, Mace 4](https://www.cs.unm.edu/~mccune/prover9/) extension from NLTK. For more details on installation [check here](https://www.nltk.org/howto/inference.html).

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
To run example baseline inference
```bash
python baseline_iLens.py
```
To run example main system inference
```bash
python iterative_iLens.py
```
To convert NL to AMR to FOL, you will need openai==0.28.0 and openai_key
```bash
python NL_to_FOL.py
```
