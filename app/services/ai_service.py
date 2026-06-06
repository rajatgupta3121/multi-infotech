from groq import Groq
from dotenv import load_dotenv
import os
import re

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def format_course_response(text):

    if not text:
        return text

    text = text.strip()

    # Convert bold course title to heading
    text = re.sub(
        r"\*\*(.*?)\*\*",
        r"# \1",
        text,
        count=1
    )

    # Clean multiple blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Replace common labels
    replacements = {
        "Course Name:": "🎓 **Course Name:**",
        "Fees:": "💰 **Fees:**",
        "Duration:": "⏳ **Duration:**",
        "Category:": "📂 **Category:**",
        "Description:": "📖 **Description:**",
        "Career Opportunities:": "🚀 **Career Opportunities:**",
        "Key Highlights:": "✨ **Key Highlights:**",
        "Career Scope:": "🚀 **Career Scope:**"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    if "Admission Support" not in text:
        text += "\n\n---\n📞 **Admission Support:** +91 97946 60840"

    return text


def generate_ai_response(user_query, course_context):

    system_prompt = """
You are the official AI Admission Counselor of Multi Infotech Institute.

Rules:

1. Answer only from provided context.
2. Never invent fees, duration or syllabus.
3. Use markdown formatting.
4. Use bullet points.
5. Keep answers concise.
6. Use headings.
7. Maximum 250 words.
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                }
            ] + messages,
            temperature=0.2,
            max_tokens=500
        )

        raw_response = response.choices[0].message.content

        return format_course_response(
            raw_response
        )

    except Exception as e:

        print("AI ERROR:", str(e))

        return (
            "Sorry, the AI assistant is currently unavailable."
        )