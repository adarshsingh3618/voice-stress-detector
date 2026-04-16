from utils.gemini_utils import configure_gemini, analyze_text_stress
from utils.fusion_utils import calculate_final_stress, get_stress_level

client = configure_gemini()

# TEXT INPUT
text_result = analyze_text_stress(
    client,
    "I feel very overwhelmed and tired"
)

text_score = text_result["stress_score"]

# FAKE VOICE SCORE (for now)
voice_score = 7.5

# FUSION
final_score = calculate_final_stress(text_score, voice_score)
level = get_stress_level(final_score)

print("Text Score:", text_score)
print("Voice Score:", voice_score)
print("Final Score:", final_score)
print("Level:", level)