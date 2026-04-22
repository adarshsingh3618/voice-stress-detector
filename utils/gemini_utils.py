from google import genai
import os
import json
import re
import time
from dotenv import load_dotenv

# ----------------------------------------
# LOAD ENV VARIABLES (.env support)
# ----------------------------------------
load_dotenv()


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

    Return ONLY JSON.

    Format:
    {{
        "stress_score": number (0-10),
        "emotion": "one word",
        "reason": "short"
    }}
    """

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            text = response.text.strip()

            json_match = re.search(r'\{.*\}', text, re.DOTALL)

            if json_match:
                data = json.loads(json_match.group(0))
            else:
                raise ValueError("No JSON found")

            break

        except Exception as e:
            print("Stress Analysis Error:", e)
            if attempt < 2:
                time.sleep(2)
            else:
                data = {
                    "stress_score": 5,
                    "emotion": "unknown",
                    "reason": "fallback"
                }

    # Clamp score
    score = data.get("stress_score", 5)
    data["stress_score"] = max(0, min(10, score))

    data["emotion"] = data.get("emotion", "unknown").lower()

    return data


# ----------------------------------------
# Companion Response (Hybrid AI)
# ----------------------------------------
def generate_companion_response(client, chat_history, stress_score, level):

    # Get latest message
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
            "I'm really sorry you're feeling this way. You're not alone.\n\n"
            "Please reach out to someone right now:\n"
            "📞 A trusted person\n"
            "📞 A mental health helpline\n\n"
            "I'm here with you."
        )

    # ----------------------------------------
    # 🧠 INTENT HINT (GUIDE GEMINI)
    # ----------------------------------------
    intent_hint = ""

    if "study" in latest_user_msg:
        intent_hint = "User wants to study but is distracted. Suggest small steps."

    elif "distract" in latest_user_msg:
        intent_hint = "User wants distraction. Suggest light activities."

    elif "alone" in latest_user_msg or "leave" in latest_user_msg:
        intent_hint = "User feels lonely or heartbroken. Provide emotional support."

    elif "meditat" in latest_user_msg:
        intent_hint = "User wants meditation. Guide simple breathing."

    elif "what should i do" in latest_user_msg:
        intent_hint = "User is confused. Give one simple actionable step."

    elif len(latest_user_msg) <= 3:
        intent_hint = "User gave short reply. Ask follow-up gently."

    # ----------------------------------------
    # 🧠 BUILD CONTEXT
    # ----------------------------------------
    history_text = ""
    for role, msg in chat_history:
        if role == "user":
            history_text += f"User: {msg}\n"
        else:
            history_text += f"Assistant: {msg}\n"

    # ----------------------------------------
    # 🎯 GEMINI PROMPT
    # ----------------------------------------
    prompt = f"""
    You are a supportive AI companion.

    Stress level: {level}
    Stress score: {stress_score}/10

    Conversation:
    {history_text}

    Guidance:
    {intent_hint}

    Rules:
    - Do NOT repeat responses
    - Be natural and empathetic
    - Give NEW suggestions each time
    - Keep it short (2–4 lines)
    - Help the user practically

    Respond to the latest message.
    """

    # ----------------------------------------
    # 🔁 SAFE CALL
    # ----------------------------------------
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        reply = response.text.strip()
        print("RAW RESPONSE:", reply)

        # Prevent exact repetition
        if len(chat_history) > 1:
            last_reply = chat_history[-1][1]
            if reply == last_reply:
                reply += "\n\nLet's try a slightly different approach."

        return reply

    except Exception as e:
        print("Gemini Error:", e)

        return (
            f"I can see you're feeling {level.lower()} right now.\n"
            "Let's take it step by step.\n"
            "Tell me what's bothering you most."
        )