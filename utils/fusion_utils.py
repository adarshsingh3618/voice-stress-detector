# ----------------------------------------
# Fusion Engine
# ----------------------------------------

def calculate_final_stress(text_score, voice_score):

    # Basic weighted fusion
    final_score = (0.5 * text_score) + (0.5 * voice_score)

    return round(final_score, 1)

# ----------------------------------------
# Stress Level Mapping
# ----------------------------------------

def get_stress_level(score):

    if score == 0:
        return "None"
    elif score <= 3:
        return "Low"
    elif score < 7:
        return "Moderate"
    elif score < 9:
        return "High"
    else:
        return "Extreme"