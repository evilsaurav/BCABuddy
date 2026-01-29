import os
from dotenv import load_dotenv
from groq import Groq, BadRequestError

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in .env")

client = Groq(api_key=GROQ_API_KEY)


def build_system_prompt(mode: str, language: str) -> str:
    persona = (
        "You are BCABuddy, a friendly senior and study companion for IGNOU BCA students. "
        "You explain concepts clearly, in an exam-oriented way. "
        "You are supportive, slightly witty, and never rude. "
        "You never mention that you are an AI model."
    )

    language_rule = (
        "Respond in Hinglish (Roman Hindi + simple English)."
        if language.lower() == "hinglish"
        else "Respond in clear, simple English."
    )

    mode_rules = {
        "Assignment": "Give structured, exam-ready answers with headings.",
        "PYQ": "Focus on marks, key points, and examiner expectations.",
        "Notes": "Use bullet points for easy revision.",
        "Viva": "Answer briefly like an oral exam.",
        "Lab": "Explain step-by-step with practical clarity.",
        "Summary": "Give a very short summary with key points only.",
    }

    return f"{persona}\n{language_rule}\n{mode_rules.get(mode, 'Explain clearly.')}"


def generate_reply(message: str, mode: str, language: str) -> str:
    system_prompt = build_system_prompt(mode, language)

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
            temperature=0.4,
            max_tokens=800,
        )
        return response.choices[0].message.content.strip()

    except BadRequestError as e:
        return (
            "⚠️ BCABuddy internal issue: Model temporarily unavailable.\n"
            "Please try again in a moment."
        )

    except Exception as e:
        return f"⚠️ BCABuddy error: {str(e)}"
