from flask import Blueprint, request, jsonify, session
import uuid

from app.services.rag_service import retrieve_relevant_courses
from app.services.ai_service import generate_ai_response

from app.models.lead import Lead
from app.models.chat import ChatMessage

from app.extensions import db

chatbot = Blueprint(
    "chatbot",
    __name__
)


@chatbot.route("/chatbot", methods=["POST"])
def chatbot_reply():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "reply": "No request data received."
            })

        user_msg = data.get("message", "").strip()

        if not user_msg:
            return jsonify({
                "reply": "Please enter a message."
            })

        # ====================================
        # SESSION MANAGEMENT
        # ====================================

        if "chat_session" not in session:
            session["chat_session"] = str(uuid.uuid4())

        session_id = session["chat_session"]

        # ====================================
        # SAVE USER MESSAGE
        # ====================================

        user_chat = ChatMessage(
            session_id=session_id,
            role="user",
            message=user_msg
        )

        db.session.add(user_chat)
        db.session.commit()

        # ====================================
        # RETRIEVE RELEVANT COURSES
        # ====================================

        retrieved_courses = retrieve_relevant_courses(
            user_msg,
            top_k=3
        )

        # ====================================
        # BUILD COURSE CONTEXT
        # ====================================

        course_context = ""

        if retrieved_courses:

            for course in retrieved_courses:

                course_context += f"""

Course Name:
{course["title"]}

Category:
{course["category"]}

Duration:
{course["duration"]}

Fees:
₹{course["fees"]}

Description:
{course["description"]}

-----------------------------------
"""

        else:

            course_context = "No matching course found."

        # ====================================
        # GENERATE AI RESPONSE
        # ====================================

        reply = generate_ai_response(
            user_query=user_msg,
            course_context=course_context
        )

        # ====================================
        # SAVE BOT MESSAGE
        # ====================================

        bot_chat = ChatMessage(
            session_id=session_id,
            role="assistant",
            message=reply
        )

        db.session.add(bot_chat)

        # ====================================
        # LEAD CAPTURE
        # ====================================

        cleaned_msg = user_msg.replace(" ", "")

        if cleaned_msg.isdigit() and len(cleaned_msg) >= 10:

            existing_lead = Lead.query.filter_by(
                phone=cleaned_msg
            ).first()

            if not existing_lead:

                lead = Lead(
                    name="Chat User",
                    email="",
                    phone=cleaned_msg,
                    message="Captured via AI Chatbot"
                )

                db.session.add(lead)

                reply += (
                    "\n\n✅ Thank you! "
                    "Our admission team will contact you shortly."
                )

        db.session.commit()

        return jsonify({
            "reply": reply
        })

    except Exception as e:

        print("CHATBOT ERROR:", str(e))

        return jsonify({
            "reply": (
                "Sorry, something went wrong. "
                "Please try again later."
            )
        })