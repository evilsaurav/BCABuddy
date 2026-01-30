import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(override=True)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"

client = Groq(api_key=GROQ_API_KEY)

def generate_reply(message, context, language, length_mode):
    msg_lower = message.lower().strip()

    # --- 1. SUPER PRIORITY: Identity Logic (No AI Needed Here) ---
    # Agar user developer ya crush ke baare mein puche, toh seedha reply do
    
    if any(word in msg_lower for word in ["crush", "jiya", "jiya maurya"]):
        return "Code ki kahaniyon me ek hi naam mashhoor hai: Jiya Maurya ❤️"

    if any(word in msg_lower for word in ["built you", "who made you", "developer", "saurav"]):
        return "Mujhe Saurav Kumar ne banaya hai. Wo ek IGNOU BCA student aur passionate developer hain, jinhone BCABuddy ko design kiya hai."

    # --- 2. Prompt Customization (BCA Tutoring) ---
    length_hints = {
        "Short": "Answer in 1-2 bullet points or sentences.",
        "Medium": "Answer in 2 paragraphs with key points.",
        "Long": "Provide a comprehensive guide with examples and structure."
    }
    
    lang_style = "Professional English" if language == "English" else "Hinglish (Mix of Hindi and English)"

    try:
        # Strict System Prompt
        system_instructions = f"""
        You are 'BCABuddy', an AI Tutor for IGNOU BCA.
        Context: {context}
        Rules:
        - Style: {lang_style}
        - Length: {length_hints.get(length_mode, 'Medium')}
        - Never claim IGNOU staff built you.
        - If answer not in context, use general BCA knowledge.
        """

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": message}
            ],
            temperature=0.6,
            max_tokens=1200
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error: {e}")
        return "Bhai, Groq API busy hai. Please try again!"