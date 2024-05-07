import amrlib
import json
from amrlib_master import amrlib


def amr_conversion(file_path):
    # reading file in source
    with open(file_path, "r") as user_file:
        file = user_file.readline()
        example = json.loads(file)

    premise = example["premises"]
    print("premise:", premise)
    conclusion = example["conclusion"]
    print("conclusion:", conclusion)

    stog = amrlib.load_stog_model()
    premise_graphs = stog.parse_sents(premise)
    conclusion_graph = stog.parse_sents(conclusion)
    return premise_graphs, conclusion_graph


def fol_conversion(file_path):
    amr_conversion(file_path)


if __name__ == '__main__':
    fol_conversion("FOL dataset/test_folio.json")
