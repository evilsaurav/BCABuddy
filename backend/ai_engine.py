import os
from dotenv import load_dotenv
from groq import Groq

# .env se variables load karo
load_dotenv(override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"

# Debugging startup
if not GROQ_API_KEY:
    print("❌ ERROR: GROQ_API_KEY nahi mili! Check .env file.")
else:
    print(f"✅ Groq Key Loaded Successfully!")

client = Groq(api_key=GROQ_API_KEY)

def generate_reply(message, context, language, length_mode):
    """
    Full function to generate AI reply with identity protection and dynamic length/language.
    """
    msg_lower = message.lower().strip()

    # --- 1. Identity Logic (Sabse Pehle) ---
    # In keywords par AI PDF nahi dekhega, direct reply dega
    if any(word in msg_lower for word in ["crush", "jiya", "jiya maurya"]):
        return "Code ki kahaniyon me ek hi naam mashhoor hai: Jiya Maurya ❤️"

    if any(word in msg_lower for word in ["built you", "who made you", "developer", "saurav"]):
        return "Mujhe Saurav Kumar ne banaya hai. Wo ek IGNOU BCA student aur passionate developer hain, jinhone BCABuddy ko design kiya hai."

    # --- 2. Length & Language Customization ---
    length_hints = {
        "Short": "Answer very briefly in 1-2 lines.",
        "Medium": "Answer in 2-3 paragraphs with bullet points.",
        "Long": "Provide a detailed explanation with examples and headings."
    }
    
    lang_style = "Professional English" if language == "English" else "Hinglish (Mix of Hindi and English)"

    try:
        # System instructions to keep AI in check
        system_instructions = f"""
        You are 'BCABuddy', an expert AI Tutor for IGNOU BCA students.
        
        RULES:
        1. Tone: {lang_style}.
        2. Detail Level: {length_hints.get(length_mode, 'Medium')}.
        3. Use this Context from IGNOU PDFs: {context}.
        4. If answer is not in context, use your general BCA knowledge to help.
        5. Never claim IGNOU staff built you. Saurav Kumar is your developer.
        """

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": message}
            ],
            temperature=0.6,
            max_tokens=1500
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"❌ Error in Groq API: {e}")
        return "Sorry bhai, Groq API busy hai ya key expire ho gayi hai. Ek baar terminal check karo!"