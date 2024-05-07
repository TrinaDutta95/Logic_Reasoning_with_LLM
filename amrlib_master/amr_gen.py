import amrlib
import re 

stog = amrlib.load_stog_model("amrlib/data/model_stog")
graphs = stog.parse_sents(['a man has been found stabbed to death at his home, police have said.'])
amr_file = open("amr4.txt", "w")
for graph in graphs:
    #print(graph)
    ngraph = graph.replace("\n", "")
    ngraph = ngraph.replace("    ","")
    print(ngraph)
    amr_file.write(graph)
amr_file.close()

amr_file = open("amr4.txt", "r")

tokens = []
for line in amr_file:
    line = line.replace("\n", "")
    line = line.replace("   ", "")
    # print(line)
    if line.startswith(':op'):
        #print(line)
        tokens.append(line)

print(tokens)

amr_file = open("amr4.txt", "a")
amr_file.write("\n")
results = set()
# results = re.findall(r'\(.*?\)', ngraph )
for start in range(len(ngraph)):
    string = ngraph[start:]
    results.update(re.findall('\(.*?\)', string))

print("The string between brackets:")
#print(results)

s_results = sorted(results, key = len)
print(s_results)
# print(s_results[3])
print(len(s_results))
count=0
new_results = []
for result in s_results:
    # print(count)
    # print(result)
    count = count+1
    n_l = 0
    n_r = 0
    for char in result:
        if char == "(":
            n_l = n_l+1
        elif char == ")":
            n_r = n_r+1
    
    if n_l == n_r:
        print(result)
        amr_file.write(result)
        new_results.append(result) 


print(new_results)



    
amr_file.close()
