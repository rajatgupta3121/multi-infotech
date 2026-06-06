from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import current_app

from app.models.lead import Lead
from app.extensions import db
from app.services.email_service import send_lead_email


contact = Blueprint(
    "contact",
    __name__
)


@contact.route(
    "/contact",
    methods=["GET", "POST"]
)
def contact_page():

    if request.method == "POST":

        try:

            name = request.form.get(
                "name", ""
            ).strip()

            email = request.form.get(
                "email", ""
            ).strip()

            phone = request.form.get(
                "phone", ""
            ).strip()

            message = request.form.get(
                "message", ""
            ).strip()

            if not name or not email or not phone:

                flash(
                    "Please fill all required fields.",
                    "danger"
                )

                return redirect(
                    url_for(
                        "contact.contact_page"
                    )
                )

            if "@" not in email:

                flash(
                    "Please enter a valid email address.",
                    "danger"
                )

                return redirect(
                    url_for(
                        "contact.contact_page"
                    )
                )

            lead = Lead(
                name=name,
                email=email,
                phone=phone,
                message=message
            )

            db.session.add(lead)
            db.session.commit()

            try:

                send_lead_email(
                    name,
                    email,
                    phone,
                    message
                )

            except Exception as email_error:

                current_app.logger.error(
                    f"Email Error: {email_error}"
                )

            flash(
                "Your enquiry has been submitted successfully. Our team will contact you shortly.",
                "success"
            )

            return redirect(
                url_for(
                    "contact.contact_page"
                )
            )

        except Exception as e:

            db.session.rollback()

            current_app.logger.error(
                f"Contact Form Error: {e}"
            )

            flash(
                "Something went wrong. Please try again.",
                "danger"
            )

            return redirect(
                url_for(
                    "contact.contact_page"
                )
            )

    return render_template(
        "contact.html"
    )