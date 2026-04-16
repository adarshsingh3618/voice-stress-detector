from google import genai
import os
import json
import re
import time


# ----------------------------------------
# Configure Gemini Client
# ----------------------------------------
def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")

    return genai.Client(api_key=api_key)


# ----------------------------------------
# Text Stress Analyzer (SAFE + RETRY)
# ----------------------------------------
def analyze_text_stress(client, user_input):

    prompt = f"""
    Analyze the user's stress.

    Message: "{user_input}"

    Return ONLY JSON. No explanation. No extra text.

    Format:
    {{
        "stress_score": number (0-10),
        "emotion": "one word",
        "reason": "short"
    }}
    """

    # ----------------------------------------
    # RETRY LOGIC (3 attempts)
    # ----------------------------------------
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            text = response.text.strip()

            # Extract JSON
            json_match = re.search(r'\{.*\}', text, re.DOTALL)

            if json_match:
                data = json.loads(json_match.group(0))
            else:
                raise ValueError("No JSON found")

            break  # success

        except Exception:
            if attempt < 2:
                time.sleep(2)
            else:
                data = {
                    "stress_score": 5,
                    "emotion": "unknown",
                    "reason": "API unavailable"
                }

    # ----------------------------------------
    # SAFETY CHECK (0–10)
    # ----------------------------------------
    score = data.get("stress_score", 5)
    data["stress_score"] = max(0, min(10, score))

    # ----------------------------------------
    # NORMALIZE EMOTION
    # ----------------------------------------
    data["emotion"] = data.get("emotion", "unknown").lower()

    return data
def generate_companion_response(client, chat_history, stress_score, level):

    latest_user_msg = ""
    for role, msg in reversed(chat_history):
        if role == "user":
            latest_user_msg = msg.lower().strip()
            break

    # ----------------------------------------
    # 🔴 CRISIS DETECTION
    # ----------------------------------------
    crisis_keywords = [
        "kill myself", "suicide", "die", "end my life",
        "i don't want to live", "self harm"
    ]

    if any(word in latest_user_msg for word in crisis_keywords):
        return (
            "I'm really sorry you're feeling this way. You’re not alone.\n\n"
            "Please reach out to someone right now:\n"
            "📞 A trusted person\n"
            "📞 A mental health helpline\n\n"
            "I'm here with you."
        )

    # ----------------------------------------
    # 🧠 INTENT → HINT (NOT RESPONSE)
    # ----------------------------------------
    intent_hint = ""

    if "study" in latest_user_msg:
        intent_hint = "User wants to study but is distracted. Suggest small realistic steps."

    elif "distract" in latest_user_msg:
        intent_hint = "User wants distraction. Suggest light and engaging activities."

    elif "alone" in latest_user_msg or "she leave" in latest_user_msg:
        intent_hint = "User feels heartbroken and alone. Provide emotional support."

    elif "meditat" in latest_user_msg:
        intent_hint = "User wants to try meditation. Guide simple breathing."

    elif "what should i do" in latest_user_msg:
        intent_hint = "User is confused. Give one simple actionable step."

    elif len(latest_user_msg) <= 3:
        intent_hint = "User gave short reply. Ask gently and guide next step."

    # ----------------------------------------
    # 🧠 BUILD MEMORY CONTEXT
    # ----------------------------------------
    history_text = ""
    for role, msg in chat_history:
        if role == "user":
            history_text += f"User: {msg}\n"
        else:
            history_text += f"Assistant: {msg}\n"

    # ----------------------------------------
    # 🎯 GEMINI PROMPT (THIS IS THE MAGIC)
    # ----------------------------------------
    prompt = f"""
    You are a supportive AI companion.

    Stress level: {level}
    Stress score: {stress_score}/10

    Conversation:
    {history_text}

    Extra guidance:
    {intent_hint}

    Rules:
    - Do NOT repeat previous responses
    - Be natural and human
    - Give NEW responses each time
    - Keep it short (2–4 lines)
    - Be empathetic
    - Give practical suggestions when needed

    Respond to the latest user message.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        print("RAW RESPONSE:", response.text)
        return response.text.strip()

    except Exception as e:
        print("Gemini Error:", e)

        return (
            "AI is temporarily unavailable. But I’m still here with you.\n"
            "Let’s take one small step—what’s bothering you the most right now?"
        )