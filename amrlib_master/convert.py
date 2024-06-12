import amrlib
import json

def amr_conversion():
    # arguments passed
    #print("\nName of file to read:", sys.argv[1])
    #file = open(sys.argv[1], "r")

    # reading file in source
    #source = file.read().splitlines()
    premise = ["A dog never tells the truth.", "Some poker players are dogs."]
    conclusion = ["Some poker players never tell the truth."]

    # print(source)
    # print(len(source))

    # reading file in source

    stog = amrlib.load_stog_model()
    #graphs = stog.parse_sents(['This is a test of the system.', 'This is a second sentence.'])
    graphs = stog.parse_sents(premise)
    conclusion_graph = stog.parse_sents(conclusion)
    print(graphs, "\n",conclusion_graph)
    # saving amr graphs in a file
    with open('amr_graphs.txt', 'w') as f:
        for graph in graphs:
            f.write(f"{graph}\n")
            #print(graph)

    return graphs, conclusion_graph


if __name__ == '__main__':
    amr_conversion()

