import amrlib
import sys

# arguments passed
#print("\nName of file to read:", sys.argv[1])
#file = open(sys.argv[1], "r")

# reading file in source
#source = file.read().splitlines()
source = ['''People in this club who perform in school talent shows often attend and are very engaged with school events.
People in this club either perform in school talent shows often or are inactive and disinterested community members.
People in this club who chaperone high school dances are not students who attend the school.
All people in this club who are inactive and disinterested members of their community chaperone high school dances.
All young children and teenagers in this club who wish to further their academic careers and educational opportunities are students who attend the school.

Bonnie is in this club and she either both attends and is very engaged with school events and is a student who attends the school or is not someone who bot
h attends and is very engaged with school events and is not a student who attends the school.''']
print(source)
print(len(source))

stog = amrlib.load_stog_model()
#graphs = stog.parse_sents(['This is a test of the system.', 'This is a second sentence.'])
graphs = stog.parse_sents(source)

# saving amr graphs in a file
with open('amr_graphs.txt', 'w') as f:
    for graph in graphs:
        f.write(f"{graph}\n")
        print(graph)
