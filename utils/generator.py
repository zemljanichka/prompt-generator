import random
from itertools import product
from collections import Counter
from utils.lang import get_localized_data
from typing import List, Tuple, Dict

SCENARIO_RANDOM_SEED = 1243456
random.seed(SCENARIO_RANDOM_SEED)

def generate_scenarios_characters(lang: str, scenario_dimension: str) -> Tuple[str, str]:
    """
    Generate two sets of characters for the scenarios.
    
    Args:
        lang: Language code ('en' or 'ru')
        scenario_dimension: Type of scenario to generate
        
    Returns:
        Tuple[str, str]: Two generated character sets as formatted strings
    """
    # Unpack localized data into meaningful groups
    (
        # Species groups
        animals,        # List of animal types
        people,         # List of human types
        
        # Social groups
        low_status,     # Lower social status characters
        neutral_status, # Neutral social status characters
        high_status,    # Higher social status characters
        
        # Gender groups
        females,        # Female characters
        males,          # Male characters
        
        # Paired groups
        age_pairs,      # Age-based character pairs
        fitness_pairs,  # Fitness-based character pairs
        
        # Character lists
        all_chars,      # All possible characters
        plural_forms,   # Plural forms of characters
        
        # Text formatting
        text_joins,     # Conjunctions for joining text
        
        # Unused descriptions and headers
        _,              # Base description
        _,              # Case 1 description
        _,              # Case 2 description
        _,              # Case 1 header
        _               # Case 2 header
    ) = get_localized_data(lang)
    
    # Generate character sets based on scenario type
    set_1, set_2 = [], []
    
    if scenario_dimension == "species":
        num_pairs = random.choice(list(range(1, 6)))
        char_pairs = random.choices(list(product(people, animals)), k=num_pairs)
        set_1 = [pair[0] for pair in char_pairs]
        set_2 = [pair[1] for pair in char_pairs]
    elif scenario_dimension == "social_value":
        num_pairs = random.choice(list(range(1, 6)))
        possible_pairs = (
            list(product(low_status, neutral_status)) +
            list(product(low_status, high_status)) +
            list(product(neutral_status, high_status))
        )
        char_pairs = random.choices(possible_pairs, k=num_pairs)
        set_1 = [pair[0] for pair in char_pairs]
        set_2 = [pair[1] for pair in char_pairs]
    elif scenario_dimension == "gender":
        num_pairs = random.choice(list(range(1, 6)))
        indices = random.choices(range(len(females)), k=num_pairs)
        set_1 = [females[i] for i in indices]
        set_2 = [males[i] for i in indices]
    elif scenario_dimension == "age" or scenario_dimension == "fitness":
        num_pairs = random.choice(list(range(1, 6)))
        pairs = age_pairs if scenario_dimension == "age" else fitness_pairs
        char_pairs = random.choices(pairs, k=num_pairs)
        set_1 = [pair[0] for pair in char_pairs]
        set_2 = [pair[1] for pair in char_pairs]
    else:  # random or other dimensions
        set_1 = random.choices(all_chars, k=random.choice(list(range(1, 6))))
        set_2 = random.choices(all_chars, k=random.choice(list(range(1, 6))))

    # Format the character sets into strings
    def format_character_set(characters: List[str]) -> str:
        if not characters:
            return ""
            
        char_counts = Counter(characters)
        formatted_parts = []
        
        for char, count in char_counts.items():
            char_text = plural_forms[all_chars.index(char)] if count > 1 else char
            formatted_parts.append(f"{count} {char_text}")
        
        if len(formatted_parts) == 1:
            return formatted_parts[0]
        elif len(formatted_parts) == 2:
            return f"{formatted_parts[0]}{text_joins[0]}{formatted_parts[1]}"
        else:
            return f"{', '.join(formatted_parts[:-1])}{text_joins[1]}{formatted_parts[-1]}"
        
        #TODO add scenario description

    return format_character_set(set_1), format_character_set(set_2)