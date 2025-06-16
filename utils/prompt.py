def construct_prompt(
    case1: str,
    case2: str,
    pedestrians_set_1: str,
    pedestrians_set_2: str,
    case1_header: str,
    case2_header: str,
    description: str = "",
    ending: str = "",
    lang: str = "en"
) -> str:
    """
    Constructs the final prompt by combining all parts.
    
    Args:
        description: Base scenario description
        case1: Description for case 1
        case2: Description for case 2
        pedestrians_set_1: First set of generated pedestrians
        pedestrians_set_2: Second set of generated pedestrians
        case1_header: Header for case 1
        case2_header: Header for case 2
        ending: Optional ending text (default: "")
        lang: Language code
        
    Returns:
        str: Complete formatted prompt
    """
    # Construct the complete prompt
    prompt = (
        #f"{description}\n\n"
        f"{case1_header}"
        f"{case1} {pedestrians_set_1}.\n\n"
        f"{case2_header}"
        f"{case2} {pedestrians_set_2}."
    )
    
    # Add ending if provided
    if description:
        prompt = f"{description}\n\n" + prompt
        
    if ending:
        prompt += f"\n\n{ending}"
    
    return prompt