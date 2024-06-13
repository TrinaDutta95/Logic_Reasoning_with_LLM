from nltk import *
import json
from data.utils import *
import openai
from baseline_iLens import evaluate
from NL_to_FOL import get_completion
read_expr = Expression.fromstring
prover = Prover9()
mace = Mace()


def read_json(filepath):
    with open(filepath, 'r', newline='', encoding='utf-8') as file:
        data = json.load(file)
    # Extract "premise-fol" and "conclusion-fol" fields
    extracted_data = []
    for obj in data:
        extracted_obj = {
            "premises": obj.get("premise", []),
            "conclusion": obj.get("conclusion", []),
            "premise-fol": obj.get("premise-fol", []),
            "conclusion-fol": obj.get("conclusion-fol", []),
            "actual_label": obj.get("actual_label", []),
            "predicted_label": obj.get("predicted_label", []),
            "error": obj.get("error", [])
        }
        extracted_data.append(extracted_obj)

    return extracted_data


def gen_counterexample(premise_fol):
    premise_fol_data = []
    for premise in premise_fol:
        premise = read_expr(premise)
        # print(premise)
        premise_fol_data.append(premise)
    print("premise to fol output:", premise_fol_data)
    mb = MaceCommand(assumptions=premise_fol_data)  # , max_models=1)
    mb.build_model()
    result = mb.model(format='cooked')
    print("mace model:", result)
    return str(result)


def gen_updatednl(counter_example, premises, conclusion, api_key):
    """
        Update the First Order Logic (FOL) statements with Mace4 counterexamples using the OpenAI API.

        Parameters:
        counter_example (str): the FOL-counterexample
        premises (list): the list of premises
        conclusion (str): the conclusion
        api_key (str): OpenAI API key.

        Returns:
        dict: A dictionary with "premise-fol" and "conclusion-fol" keys containing the converted FOL expressions.
        """
    openai.api_key = api_key
    prompt_2 = f"""Your task is to read and understand the {counter_example} generated from Mace4 and use 
    /common sense knowledge to find any missing information or logic chain and generate First Order Logic (FOL) from the 
    /provided natural language {premises} and {conclusion}.
    Follow the given example for format and syntax.
    Example:
    "premises": [
            "If people perform in school talent shows often, then they attend and are very engaged with school events.",
            "People either perform in school talent shows often or are inactive and disinterested members of their community.",
            "If people chaperone high school dances, then they are not students who attend the school.",
            "All people who are inactive and disinterested members of their community chaperone high school dances.",
            "All young children and teenagers who wish to further their academic careers and educational opportunities are students who attend the school.",
            "Bonnie either both attends and is very engaged with school events and is a student who attends the school, or she neither attends and is very engaged with school events nor is a student who attends the school. "
        ],
        "premises-FOL": [
            "all x. (TalentShows(x) -> Engaged(x))",
            "all x. (TalentShows(x) | Inactive(x))",
            "all x. (Chaperone(x) -> -Students(x))",
            "all x. (Inactive(x) -> Chaperone(x))",
            "all x. (AcademicCareer(x) -> Students(x))",
            "(((Engaged(Bonnie) & Students(Bonnie)) & -(-Engaged(Bonnie) & -Students(Bonnie))) | (-(Engaged(Bonnie) & Students(Bonnie)) & (-Engaged(Bonnie) & -Students(Bonnie))))"
        ],
        "conclusion": "If Bonnie is either both a young child or teenager who wishes to further her academic career and educational opportunities and chaperones high school dances or neither is a young child nor teenager who wishes to further her academic career and educational opportunities, then Bonnie is either a student who attends the school or is an inactive and disinterested member of the community.",
        "conclusion-FOL": "((AcademicCareer(Bonnie) & -Chaperone(Bonnie)) | (-AcademicCareer(Bonnie) & Chaperone(Bonnie))) -> ((AcademicCareer(Bonnie) & -Inactive(Bonnie)) | (-AcademicCareer(Bonnie) & Inactive(Bonnie)))"
    Ensure that:
    - Do not use symbols as both relation and function.
    - Symbols are consistently used as either predicates or functions with consistent arities.
    - Quantifiers are correctly placed 
    - No quotations are required for any proper noun.
    - Make sure your output has both premise and conclusion expressions
    - The FOL expressions are valid and well-formed for use in theorem provers like Prover9.
    - Make sure the FOL expressions are consistent, syntactically correct, and have balanced parentheses.
    - Make sure the output is not like a chat response.
    
     Your output should be a dictionary with the keys "premises-FOL" for premises with all FOL expressions
    /in a single list and "conclusion-FOL" for conclusion with FOL expression in a single list.
    """
    response = get_completion(prompt_2)
    return response


def fix_error(premise_fol, conclusion_fol, error, api_key):
    """
            Fix the First Order Logic (FOL) from the given error using the OpenAI API.

            Parameters:
            premise_fol (list): List of premises in FOL format.
            conclusion_fol (list): List of conclusions in FOL format.
            error (str): The error message.
            api_key (str): OpenAI API key.

            Returns:
            dict: A dictionary with "premise-fol" and "conclusion-fol" keys containing the converted FOL expressions.
            """
    openai.api_key = api_key
    prompt_3 = f"""Your task is to fix some errors in first order logic statements. 
    /I will provide you with the {error} and the first order logic {premise_fol} and 
    /{conclusion_fol} such that they do not contain that error. 
    Follow the given examples for format and syntax:
    Example1:
    "premises-FOL": [
            "all x. all y. (LaLigaSoccerTeam(x) & LaLigaSoccerTeam(y) & MorePoints(x, y) -> RankHigherThan(x, y))",
            "all x. all y. (LaLigaSoccerTeam(x) & LaLigaSoccerTeam(y) & -MorePoints(x, y) & -MorePoints(y, x) & MorePointsInGameBetween(x, y) ->  RankHigherThan(x, y))",
            "LaLigaSoccerTeam(RealMadrid) & LaLigaSoccerTeam(Barcelona)",
            "MorePoints(RealMadrid, Barcelona)",
            "-MorePointsInGameBetween(RealMadrid, Barcelona) & -MorePointsInGameBetween(Barcelona, RealMadrid)"
        ],
    "conclusion-FOL": "RankHigherThan(RealMadrid, Barcelona)"
    
    Example2:
    "premises-FOL": [
            "all x. (ProfessionalAthlete(x) -> SpendOn(x, MostOfTheirTime, Sports))",
            "all x. (OlympicGoldMedalWinner(x) -> ProfessionalAthlete(x))",
            "all x. (FullTimeScientist(x) -> -SpendOn(x, MostOfTheirTime, Sports))",
            "all x. (NobelPhysicsLaureate(x) -> FullTimeScientist(x))",
            "SpendOn(Amy, MostOfTheirTime, Sports) | OlympicGoldMedalWinner(Amy)",
            "-NobelPhysicsLaureate(Amy) -> -OlympicGoldMedalWinner(Amy)"
        ],
        
    "conclusion-FOL": "-OlympicGoldMedalWinner(Amy) -> NobelPhysicsLaureate(Amy)",
    
    Example3:
    "premises-FOL": [
            "all x. (Song(x) -> -Visual(x))",
            "all x. (FolkSong(x) -> Song(x))",
            "all x. (Video(x) -> Visual(x))",
            "all x. (Movie(x) -> Video(x))",
            "all x. (ScifiMovie(x) -> Movie(x))",
            "ScifiMovie(Inception)",
            "-FolkSong(Mac) & -ScifiMovie(Mac)"
        ],
    "conclusion-FOL": "FolkSong(Inception)"
    
    Example4:
    "premises-FOL": [
            "all x. (Chef(x) -> Can(x, Cook))",
            "exists x. (-Chef(x) & Can(x, Cook))",
            "all x. (Can(x, Cook) -> (CanMake(x, ScrambledEggs) & CanMake(x, Pasta)))",
            "all x. (CanMake(x, Cookies) & CanMake(x, Muffins) -> Baker(x))",
            "all x. ((Baker(x) & CanMake(x, ScrambledEggs)) -> CanMake(x, GoodBreakfast))",
            "CanMake(Luke, Cookies) & (CanMake(Luke, ScrambledEggs) & CanMake(Luke, Muffins) & -CanMake(Luke, Pasta)"
        ],
    "conclusion-FOL": "CanMake(Luke, GoodBreakfast)"
    
    Example5:
    "premises-FOL": [
            "exists x. exists y. (Develop(eTS, x) & Develop(eTS, y) & StandardizedTest(x) & StandardizedTest(y) & In(x, UnitedState) & In(y, UnitedState) & For(x, kOneTwoAndHigherEducation) & For(y, kOneTwoAndHigherEducation))",
            "exists x. (Administer(eTS, x) & InternationalTest(x) & (TOEFL(x) | TOEIC(x) | GRE(x) | SubjectTest(x)))",
            "exists x. (Develop(eTS, x) & AssociatedWith(x, EntryToUSEducationInstitution))",
            "exists x. (Develop(eTS, x) & StateWideAssesment(x) & UsedFor(x, AccountabilityTesting))"
        ],
    "conclusion-FOL": "exists x. exists y. (Develop(eTS, x) & StateWideAssesment(x) & Develop(eTS, y) & AssociatedWith(y, EntryToUSEducationInstitution))",
    
    Example6:
    "premises-FOL": [
            "Actor(DaveedDiggs) & FilmProducer(DaveedDiggs)",
            "exists x. exists y.(PlaysIn(DaveedDiggs, x, Hamilton) & (-(x=y)) & PlaysIn(DaveedDiggs, y, Hamilton)) & OnBroadway(Hamilton) & Musical(Hamilton)",
            "exists x. exists y.(Actor(x) & PlaysIn(x, y, Hamilton) & Wins(x, BestActorAward))",
            "exists x. (Actor(x) & PlaysIn(x, ThomasJefferson, Hamilton) & Wins(x, BestActorAward))",
            "Plays(DaveedDiggs, ThomasJefferson)",
            "all x. ((Musical(x) & OnBroadway(x)) -> -Film(x))"
        ], 
    "conclusion-FOL": "Film(Hamilton)"
    
    Ensure that:
    - Do not use symbols/arities as both relation and function.
    - The FOL expressions are valid and well-formed for use in theorem provers like Prover9 with consistent arities..
    - Make sure the FOL expressions are consistent, syntactically correct, and have balanced parentheses.
    - Do not describe your answer like a chat response.
    - Make sure your output has both premise and conclusion expressions
    Your output should be a dictionary with the keys "premises-FOL" for premises with all FOL expressions
    /in a single list and "conclusion-FOL" for conclusion with FOL expression in a single list.

        """
    response_t = get_completion(prompt_3)
    return response_t


def iter_inference_with_mace(premises, conclusion, premise_fol, conclusion_fol, actual_label, predicted_label, error, api_key):
    counter_example = gen_counterexample(premise_fol)
    print(counter_example)
    fol_dict = gen_updatednl(counter_example, premises, conclusion, api_key)
    fol_data = json.loads(fol_dict)
    print(type(fol_data))
    proof_result, premise_fol, conclusion_fol, error = get_result(fol_data, conclusion_fol)
    return proof_result, premises, conclusion, premise_fol, conclusion_fol, error


def get_result(fol_data, conclusion_fol):
    print(fol_data)
    # Accessing data from the dictionary
    premise_fol = fol_data.get("premises-FOL", [])
    new_conclusion_fol = fol_data.get("conclusion-FOL", [])
    if len(new_conclusion_fol) == 0:
        new_conclusion_fol = conclusion_fol
    print(premise_fol, new_conclusion_fol)
    try:
        proof_result = evaluate(new_conclusion_fol, premise_fol)
        print(proof_result)
        print("Proved successfully")
        error = None
    except Exception as e:
        print("Error in proving:", e)
        proof_result = "ERROR"
        error = str(e)
    return proof_result, premise_fol, new_conclusion_fol, error


def iter_inference_for_error(premise_fol, conclusion_fol, actual_label, predicted_label, error, api_key):
    print(premise_fol, conclusion_fol, actual_label, predicted_label, error)
    print(type(error))
    fol_dict = fix_error(premise_fol, conclusion_fol, error, api_key)
    print(type(fol_dict))
    fol_data = json.loads(fol_dict)
    print(type(fol_data))
    print(fol_data)
    return fol_data, actual_label


def main(fol_data):

    results = []  # Store results for each example
    api_key = "add api key here"
    for item in fol_data:
        # Accessing data from the dictionary
        premises = item.get("premises", [])
        print(premises)
        conclusion = item.get("conclusion", [])
        actual_label = item.get("actual_label", [])
        predicted_label = item.get("predicted_label", [])
        error = item.get("error", [])
        premise_fol = item.get("premise-fol", [])
        len_premise = len(premises)
        len_new_premise = 0
        conclusion_fol = item.get("conclusion-fol", [])
        count = 1
        while count < 5 and len_new_premise < 3*len_premise:
            if predicted_label == "Uncertain" and actual_label != "Uncertain":
                print("Pass1")
                count = count + 1
                print("premise:", premises, "\n", "conclusion:", conclusion, "\n", "premise_fol:", premise_fol, "\n", "conclusion_fol:", conclusion_fol, "actual_label:", actual_label, "\n", "predicted_label:", predicted_label, "\n", "error:", error)
                proof_result, premise, conclusion, premise_fol, conclusion_fol, error = iter_inference_with_mace(premises, conclusion, premise_fol, conclusion_fol, actual_label, predicted_label, error, api_key)
                predicted_label = proof_result
            elif predicted_label == "ERROR":
                count = count + 1
                print("premise:", premises, "\n", "conclusion:", conclusion, "\n", "premise_fol:", premise_fol, "\n",
                      "conclusion_fol:", conclusion_fol, "actual_label:", actual_label, "\n", "predicted_label:",
                      predicted_label, "\n", "error:", error)
                print("Pass2")
                fol_data, actual_label = iter_inference_for_error(premise_fol, conclusion_fol, actual_label, predicted_label, error, api_key)
                print(fol_data, actual_label)
                proof_result, premise_fol, conclusion_fol, error = get_result(fol_data, conclusion_fol)
                predicted_label = proof_result
            else:
                print("Pass3")
                count = count + 1
                proof_result = predicted_label
            len_new_premise = len(premise_fol)
            results.append({"predicted_label": proof_result, "actual_label": actual_label})

    return results


if __name__ == '__main__':
    with open('results/iter_results_2.json', 'w', encoding='utf-8') as f:
        fol_data = read_json("data/iter_fol.json")
        results = main(fol_data)
        results_json = json.dumps(results, indent=4)
        f.write(results_json)










