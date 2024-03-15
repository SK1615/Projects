import collections
import copy

class InvalidAgent(Exception):
    pass

class InvalidScoreVectorLength(Exception):
    pass

class InvalidTieKey(Exception):
    pass

class InvalidTieBreak(Exception):
    pass

def generate_preferences(values):
    """the function generates the preferences from the given data set and sorts data's in Workbook containing preference values,
        finally it returns dictionary mapping the agent ID's in preference order"""
    preferences = {}

    for Agent_id, row in enumerate(values.iter_rows(values_only=True), start=1):
        Agent_Score = list(row)
        preference_order = sorted(range(1, len(Agent_Score) + 1), key=lambda k: (-Agent_Score[k - 1], -k))
        preferences[Agent_id] = preference_order
    return preferences


def range_voting(values, tie_break):
    """this function performs range voting operation and returns selected alternative,
    the paramters used here are values- values from worksheet which has valuation data, tie_break,
    it returns selected alternatives and raise value error if tie_break option is invalid or no scores are calculated, raises 'InvalidTieBreak' if tie_break option is invalid. """
    scores = {}
    for row in values.rows:
        Calculation = [data.value for data in row]
        for Vote_Index, value in enumerate(Calculation):
            scores[Vote_Index + 1] = scores.get(Vote_Index + 1, 0) + value
    return Tie_break(generate_preferences(values), scores, tie_break)

def Tie_break(preferences, score_dic, tie_break):
    """
    this function is used in case scores are equal,
    preferences in this function is used to map agent id's to  preference order in the dictionary,
    score_dic in this function is used to map alternative id's to scores in the dictionary,
    tie_break in this function is used in case of tie breaking method ("max", "min", or agent ID),
    also returns the alternative after tie-breaking, and raises value error if the tie_break option is invalid,
    it raises 'InvalidTieKey' If the tie_break option is incorrect."""
    try:
        Same_Counting = [key for key, value in score_dic.items() if value == max(score_dic.values())]
        if len(Same_Counting) > 1:
            if isinstance(tie_break, int) and tie_break in preferences:
                return next((i for i in preferences[tie_break] if i in Same_Counting), None)
            elif tie_break == "max":
                return max(Same_Counting)
            elif tie_break == "min":
                return min(Same_Counting)
            else:
                raise InvalidTieKey
        else:
            return Same_Counting[0]
    except InvalidTieKey:
        raise ValueError("Incorrect_Tie_Break")

def Score_Calculation(preferences, score_vector, tie_break):
    """Score_Calculation function calculates scores based on preferences and score_vector,
    the parameter preferences dictionary maps agent id's to preference orders,
    the score_vector list used to list the Scores provided for every alternate position,
    tie_break is a string or integer used in tie-breaking method ("max", "min", or agent ID),
    it return the preferred option after tie-breaking and score calculation, if tie_break option is invalid it raises value error,
    if tie_break option is incorrect it raises InvalidTieKey """
    score_dic = {}
    for _, preference in preferences.items():
        for Calculation_index, alternative in enumerate(preference):
            score_dic[alternative] = score_dic.get(alternative, 0) + score_vector[Calculation_index]

    return Tie_break(preferences, score_dic, tie_break)

def dictatorship(preferences, agent):
    """ this function implement dictatorship rule and returns the selected alternative,
    the parameters used here are preferences, agent- is an integer which gives the ID of the dictatorial agent,
    it returns sthe elected alternative integer according to the dictatorship rule, if the particular agent id is not present in the profile
    then it raises 'InvalidAgent'."""
    if agent not in preferences:
        raise InvalidAgent("Agent_ID is not present in the profile")
    return preferences[agent][0]

def scoring_rule(preferences, score_vector, tie_break):
    """this function implements generic scoring rule, the parameters used here are preferences, score_vector, tie_break and they are explained earlier,
    it returns selected alternative according to the scoring rule algorithm, it raises InvalidScoreVectorLength if the length of score_vector is incorrect."""
    if len(score_vector) != len(preferences[1]):
        raise InvalidScoreVectorLength("Incorrect Input")
    score_vector.sort(reverse=True)
    return Score_Calculation(preferences, score_vector, tie_break)

def plurality(preferences, tie_break):
    """ this function implements the plurality rule, the parameters used here are preferences and tie_break,
    it returns selected alternative according to the plurality algorithm,
    it raises InvalidScoreVectorLength if the length of score vector is incorrect"""
    score_vector = [1] + [0] * (len(list(preferences.values())[0]) - 1)
    return Score_Calculation(preferences, score_vector, tie_break)

def veto(preferences, tie_break):
    """ this functioin implements the veto rule,function uses the parameters preferences, tie_break, it returns selected alternative according to veto algorithm,
    raises InvalidScoreVectorLength if length of score vector is incorrect. """
    score_vector = [1] * (len(list(preferences.values())[0]) - 1) + [0]
    return Score_Calculation(preferences, score_vector, tie_break)

def borda(preferences, tie_break):
    """ this functioin implements the borda count rule,function uses the parameters preferences, tie_break, it returns selected alternative according to borda count algorithm,
    raises InvalidScoreVectorLength if length of score vector is incorrect. """
    score_vector = list(range(len(list(preferences.values())[0]) - 1, -1, -1))
    return Score_Calculation(preferences, score_vector, tie_break)

def harmonic(preferences, tie_break):
    """ this functioin implements the harmonic rule,function uses the parameters preferences, tie_break, it returns selected alternative according to harmonic algorithm,
    raises InvalidScoreVectorLength if length of score vector is incorrect. """
    score_vector = [1 / harmonic_Index for harmonic_Index in range(1, len(list(preferences.values())[0]) + 1)]
    return Score_Calculation(preferences, score_vector, tie_break)

def STV(preference: dict, tie_break):
    """ this functioin implements the stv algorithm for preferential voting,function uses the parameters preferences-dictionary,
    it returns selected alternative after applying stv algorithm. If there is a tie, the tie_break function is used."""
    Left_over_Candidates = set(alternative for prefs in preference.values() for alternative in prefs)
    Preferences_Works = copy.deepcopy(preference)
    while len(Left_over_Candidates) > 1:
        """it counts votes that are in first place using collections counter for efficiency"""
        Starting_Vote_count = collections.Counter(Preferences_Works[key][0] for key in Preferences_Works)
        Min_Votes = min(Starting_Vote_count.values())
        Candidates_to_be_removed = [candidate for candidate, Vote in Starting_Vote_count.items() if Vote == Min_Votes]

        Left_over_Candidates -= set(Candidates_to_be_removed)
        for Candidates_Removed in Candidates_to_be_removed:
            for key in Preferences_Works:
                if Candidates_Removed in Preferences_Works[key]:
                    index = Preferences_Works[key].index(Candidates_Removed)
                    if index < len(Preferences_Works[key]) - 1:
                        Next_Preferrable_Candidate = Preferences_Works[key][index + 1]
                        Starting_Vote_count[Next_Preferrable_Candidate] += 1
                        Preferences_Works[key].remove(Candidates_Removed)
    if len(Left_over_Candidates) == 1:
        return list(Left_over_Candidates)[0]
    else:
        return tie_break(list(Left_over_Candidates))
