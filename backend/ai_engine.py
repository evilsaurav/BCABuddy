"""
AI Engine Interface for BCABuddy

This file acts as an abstraction layer.
Today: dummy responses
Tomorrow: real AI (Groq / OpenAI / Azure / etc.)
"""

def generate_reply(message: str, mode: str, language: str) -> str:
    """
    Generate a reply for the user.
    This is a placeholder for real AI logic.
    """

    return (
        f"😄 Warm-up mode active!\n\n"
        f"You asked:\n"
        f"• Question: {message}\n"
        f"• Mode: {mode}\n"
        f"• Language: {language}\n\n"
        f"Next step me main sach-me smart ho jaunga 💪"
    )

