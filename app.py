import os
import smtplib
from email.message import EmailMessage

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "luxurydine-dev-key")

@app.route("/")
def home():
    return render_template("home.html", title="Home")

@app.route("/menu")
def menu():
    return render_template("menu.html", title="Menu")

@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact")

@app.route("/reserve", methods=["POST"])
def reserve():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    date = request.form.get("date", "").strip()
    time = request.form.get("time", "").strip()

    if not all([name, phone, date, time]):
        flash("Please fill in all reservation fields.")
        return redirect(url_for("home"))

    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASS")
    to_email = os.environ.get("SMTP_TO", "jhapriyanshu107@gmail.com")

    if not smtp_user or not smtp_pass:
        flash("Reservation email is not configured. Please set SMTP_USER and SMTP_PASS.")
        return redirect(url_for("home"))

    msg = EmailMessage()
    msg["Subject"] = f"New Reservation — {name}"
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg.set_content(
        "LuxuryDine Reservation\n"
        f"Name: {name}\n"
        f"Phone: {phone}\n"
        f"Date: {date}\n"
        f"Time: {time}\n"
    )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(smtp_user, smtp_pass)
            smtp.send_message(msg)
        flash("Reservation sent successfully. We'll confirm shortly.")
    except Exception:
        flash("Something went wrong while sending your reservation. Please try again.")

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
