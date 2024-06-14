import amrlib
import json
import re
from amrlib_master import amrlib
import openai
from amr_logic_converter import AmrLogicConverter
from utils import *


# Function to split concatenated sentences into individual sentences
def split_sentences(input_list):
    result = []
    for text in input_list:
        # Split the text by newline characters
        sentences = re.split(r'\n', text)
        result.extend(sentences)
    return result


# Function to extract individual graphs from multi-sentence AMR input
def extract_individual_graphs(amr_list):
    individual_graphs = []
    for amr in amr_list:
        # Remove sentence annotations
        amr = '\n'.join([line for line in amr.split('\n') if not line.startswith('# ::snt')])
        individual_graphs.append(amr)
    return individual_graphs


def amr_conversion(premise, conclusion):
    # converting NL to AMR
    print(premise[0], conclusion)
    stog = amrlib.load_stog_model()
    # premise = split_sentences(premise)
    premise_graphs = stog.parse_sents(premise[0])
    # conclusion = split_sentences(conclusion)
    conclusion_graph = stog.parse_sents(conclusion)
    return premise_graphs, conclusion_graph


def amr_to_fol(amr):
    converter = AmrLogicConverter()
    logic = converter.convert(amr)
    return logic


def get_completion(prompt, model="gpt-4", temperature=0.2):
    """
    Generate a completion for the given prompt using the specified model.

    Parameters:
    prompt (str): The prompt to send to the model.
    model (str): The model to use for generating the completion. Default is "gpt-4".
    temperature (float): The degree of randomness of the model's output. Default is 0.

    Returns:
    str: The completion generated by the model.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return response.choices[0].message["content"]
    except openai.error.OpenAIError as e:
        print(f"An error occurred: {e}")
        return None


def fol_conversion(premise_graphs_list, conclusion_graphs_list, api_key):
    """
    Convert the given AMR to First Order Logic (FOL) using the OpenAI API.

    Parameters:
    premise_graphs_list (list): List of premises in AMR format.
    conclusion_graphs_list (list): List of conclusions in AMR format.
    api_key (str): OpenAI API key.

    Returns:
    dict: A dictionary with "premise-fol" and "conclusion-fol" keys containing the converted FOL expressions.
    """
    openai.api_key = api_key

    prompt_1 = f"""
    I will provide you with premises and conclusions in 
    /AMR, and you will convert them into First Order Logic (FOL) expressions. 
    /Follow the given examples for format and syntax.
    Examples:
    Example1:
    "premises":['# ::snt A dog never tells the truth.\n(t / tell-01\n      :polarity -\n      :ARG0 (d / dog)\n      :ARG1 (t2 / truth)\n      :time (e / ever))', '# ::snt Some poker players are dogs.\n(d / dog\n      :domain (p / person\n            :ARG0-of (p2 / play-01\n                  :ARG1 (p3 / poker))\n            :quant (s / some)))'] 
    "premises-FOL":["all x. (dog(x) -> -tells_truth(x))", "exists x. (poker_player(x) & dog(x))"]
    "conclusion":['# ::snt Some poker players never tell the truth.\n(t / tell-01\n      :polarity -\n      :ARG0 (p / person\n            :ARG0-of (p2 / play-01\n                  :ARG1 (p3 / poker))\n            :quant (s / some))\n      :ARG1 (t2 / truth)\n      :time (e / ever))']
    "conclusion-FOL":["exists x. (poker_player(x) & -tells_truth(x))"]
    
    Example2:
    "premises":['# ::snt All eels are fish. \n(f / fish\n      :domain (e / eel\n            :mod (a / all)))', '# ::snt No fish are plants. \n(p / plant\n      :domain (f / fish\n            :polarity -))', '# ::snt A thing is either a plant or animal.\n(o / or\n      :op1 (p / plant)\n      :op2 (a / animal)\n      :domain (t / thing))', '# ::snt Nothing that breathes is paper. \n(p / paper\n      :domain (n / nothing\n            :ARG0-of (b / breathe-01)))', '# ::snt All animals breathe.\n(b / breathe-01\n      :ARG0 (a / animal\n            :mod (a2 / all)))', '# ::snt If a sea eel is either an eel or a plant, then a sea eel is an eel or an animal.\n(h / have-condition-91\n      :ARG1 (o / or\n            :op1 (e / eel)\n            :op2 (a / animal)\n            :domain (e2 / eel\n                  :mod (s / sea)))\n      :ARG2 (o2 / or\n            :op1 (e3 / eel)\n            :op2 (p / plant)\n            :domain e2))']
    "premises-FOL":["all x. (fish(x) -> eel(x))", "all x. (fish(x) -> -plant(x))", "all x. (thing(x) -> (plant(x) | animal(x)))", "all x. (breathes(x) -> -paper(x))", "all x. (animal(x) -> breathes(x))", "(all x (eel(x) & (eel(x) | plant(x))) -> (eel(x) | animal(x)))"]
    "conclusion":['# ::snt Sea eel is an eel.\n(e / eel\n      :domain (e2 / eel\n            :mod (s / sea)))']
    "conclusion-FOL":["eel(sea_eel)"]
    
    Example3:
    "premises":['# ::snt Six, seven and eight are real numbers.\n(n / number\n      :ARG1-of (r / real-04)\n      :domain (a / and\n            :op1 6\n            :op2 7\n            :op3 8))', '# ::snt If a real number equals another real number adding one, the first number is larger.\n(h / have-degree-91\n      :ARG1 (n / number\n            :ord (o / ordinal-entity\n                  :value 1))\n      :ARG2 (l / large)\n      :ARG3 (m / more)\n      :condition (e / equal-01\n            :ARG1 (n2 / number\n                  :ARG1-of (r / real-04))\n            :ARG2 (n3 / number\n                  :mod (a / another)\n                  :ARG0-of (a2 / add-02\n                        :ARG1 (o2 / one)))))', '# ::snt If the number x is larger than number y, then y is not larger than x.\n(h / have-condition-91\n      :ARG1 (h2 / have-degree-91\n            :polarity -\n            :ARG1 (y / y)\n            :ARG2 (l / large)\n            :ARG3 (m / more)\n            :ARG4 (n / number\n                  :mod (v / variable\n                        :name (n2 / name\n                              :op1 "x"))))\n      :ARG2 (h3 / have-degree-91\n            :ARG1 (n3 / number\n                  :mod (v2 / variable\n                        :name (n4 / name\n                              :op1 "y")))\n            :ARG2 (l2 / large)\n            :ARG3 (m2 / more)\n            :ARG4 n))', '# ::snt Seven equals six plus one.\n(e / equal-01\n      :ARG1 (d / difference-of\n            :op1 7\n            :op2 6)\n      :ARG2 1)', '# ::snt Eight equals seven plus one.\n(e / equal-01\n      :ARG1 (d / difference-of\n            :op1 7\n            :op2 1)\n      :ARG2 8)', '# ::snt Two is positive.\n(p / positive\n      :domain (t / thing\n            :quant 2))', '# ::snt If a number is positive, then the double of it is also positive.\n(p / positive\n      :domain (d / double-01\n            :ARG1 (n / number))\n      :mod (a / also)\n      :condition (p2 / positive\n            :domain n))', '# ::snt Eight is the double of four.\n(d / double-01\n      :ARG1 (t / temporal-quantity\n            :quant 8\n            :unit (y / year))\n      :ARG3 (t2 / temporal-quantity\n            :quant 4\n            :unit (y2 / year)))', '# ::snt Four is the double of two.\n(d / double-01\n      :ARG1 (t / thing\n            :quant 4)\n      :ARG3 (t2 / thing\n            :quant 2))'] 
    "premises-FOL":["RealNum(six) & RealNum(seven) & RealNum(eight)", "all x. all y. (RealNum(x) & RealNum(y) & EqualAddOne(x, y) -> Larger(x, y))", "EqualAddOne(seven, six)", "EqualAddOne(eight, seven)", "Positive(two)", "all x. all y. ((Positive(x) & EqualDouble(y, x)) -> Positive(y))", "EqualDouble(eight, four)", "EqualDouble(four, two)"]
    "conclusion":['# ::snt Eight is positive.\n(p / positive\n      :domain (n / numerical-quantity\n            :quant 8))']
    "conclusion-FOL":["Positive(eight)"]
    
    Example4:
    "premise":['# ::snt All people who regularly drink coffee are dependent on caffeine.\n(d / depend-01\n      :ARG0 (p / person\n            :mod (a / all)\n            :ARG0-of (d2 / drink-01\n                  :ARG1 (c / coffee)\n                  :ARG1-of (r / regular-02)))\n      :ARG1 (c2 / caffeine))', '# ::snt People either regularly drink coffee or joke about being addicted to caffeine.\n(o / or\n      :op1 (d / drink-01\n            :ARG0 (p / person)\n            :ARG1 (c / coffee)\n            :ARG1-of (r / regular-02))\n      :op2 (j / joke-01\n            :ARG0 p\n            :ARG2 (a / addict-01\n                  :ARG1 p\n                  :ARG2 (c2 / caffeine))))', '# ::snt No one who jokes about being addicted to caffeine is unaware that caffeine is a drug.\n(r / realize-01\n      :polarity -\n      :ARG0 (n / no-one\n            :ARG0-of (j / joke-01\n                  :ARG2 (a / addict-01\n                        :ARG1 n\n                        :ARG2 (c / caffeine))))\n      :ARG1 (d / drug\n            :domain c))', '# ::snt Rina is either a student and unaware that caffeine is a drug, or neither a student nor unaware that caffeine is a drug.\n(o / or\n      :op1 (a / and\n            :op1 (p / person\n                  :ARG0-of (s / study-01)\n                  :domain (p2 / person\n                        :name (n / name\n                              :op1 "Rina")))\n            :op2 (r / realize-01\n                  :polarity -\n                  :ARG0 p2\n                  :ARG1 (d / drug\n                        :domain (c / caffeine))))\n      :op2 (a2 / and\n            :op1 (p3 / person\n                  :polarity -\n                  :ARG0-of (s2 / study-01)\n                  :domain p2)\n            :op2 (r2 / realize-01\n                  :polarity -\n                  :ARG0 p2\n                  :ARG1 d)))', '# ::snt If Rina is not a person dependent on caffeine and a student, then Rina is either a person dependent on caffeine and a student, or neither a person dependent on caffeine nor a student. \n(o / or\n      :op1 (d / depend-01\n            :ARG0 (p / person\n                  :name (n / name\n                        :op1 "Rina"))\n            :ARG1 (c / caffeine))\n      :op2 (d2 / depend-01\n            :polarity -\n            :ARG0 p\n            :ARG1 (p2 / person\n                  :ARG0-of (s / study-01)))\n      :op3 (d3 / depend-01\n            :polarity -\n            :ARG0 p\n            :ARG1 c)\n      :condition (d4 / depend-01\n            :polarity -\n            :ARG0 p\n            :ARG1 p2))']
    "premise-FOL":["all x. (RegularlyDrinksCoffee(x) -> DependentOnCaffeine(x))", "all x. (RegularlyDrinksCoffee(x) | JokesAboutAddiction(x))", "all x. (JokesAboutAddiction(x) -> -UnawareThatCaffeineIsDrug(x))", "(Student(Rina) & UnawareThatCaffeineIsDrug(Rina)) | (-Student(Rina) & -UnawareThatCaffeineIsDrug(Rina))", "-(DependentOnCaffeine(Rina) & Student(Rina)) -> ((DependentOnCaffeine(Rina) & Student(Rina)) | (-DependentOnCaffeine(Rina) & -Student(Rina)))"]
    "conclusion":['# ::snt Rina is a person who jokes about being addicted to caffeine or unaware that caffeine is a drug.\n(j / joke-01\n      :ARG0 (p / person\n            :name (n / name\n                  :op1 "Rina"))\n      :ARG2 (o / or\n            :op1 (a / addict-01\n                  :ARG1 p\n                  :ARG2 (c / caffeine))\n            :op2 (r / realize-01\n                  :polarity -\n                  :ARG0 p\n                  :ARG1 (d / drug\n                        :domain c))))']
    "conclusion-FOL":["exists x. (person(x) & (jokes_about_addiction(x) | unaware_of_caffeine_drug(x)))"]
    
    
    Ensure that:
    - Each FOL expression follows the correct syntax: Logical AND: `&`, Logical OR: `|`, Logical NOT: `-`, Implication: `->`.
    - Symbols are consistently used as either predicates or functions.
    - Quantifiers are correctly placed 
    - No quotations are required for any proper noun.
    - The FOL expressions are valid and well-formed for use in theorem provers like Prover9.
    - Make sure the FOL expressions are consistent, syntactically correct, and have balanced parentheses.
    - Make sure the output is not like a chat response.


    Your output should be a dictionary with the keys "premise-fol" for {premise_graphs_list} with all FOL expressions
    /in a single list and 
    "conclusion-fol" for {conclusion_graphs_list} with all FOL expressions in a single list.
    """
    response_q = get_completion(prompt_1)
    return response_q


def processing_fol(file_path):
    # reading json file to get list of examples
    api_key = "your key here"
    with open(file_path, 'r') as f:
        json_list = json.load(f)
        for example in json_list:
            premise = example["premises"]
            premise = [premise]
            print("premise:", premise)
            conclusion = example["conclusion"]
            conclusion = [conclusion]
            print("conclusion:", conclusion)
            actual_label = example["label"]
            print("actual_label:", actual_label)
            p_graph, c_graph = amr_conversion(premise, conclusion)
            print("p_graph:", p_graph)
            print("c_graph:", c_graph)

            fol_dict = fol_conversion(p_graph, c_graph, api_key)
            # Parse the string into a Python dictionary to ensure it is valid JSON
            try:
                fol_json = json.dumps(fol_dict)
                print(fol_json)# Serialize dictionary to JSON
                fol_data = json.loads(fol_json)
                print("JSON parsed successfully!")
                yield fol_data, actual_label
            except json.JSONDecodeError as e:
                print("Failed to parse JSON:", e)


if __name__ == '__main__':
    with open("data/fol_from_amr_gpt4.json", "a") as f:
        for fol_data, actual_label in processing_fol("data/updated_folio_validation.json"):
            print(fol_data, type(fol_data))
            f.write(fol_data + '\n')



