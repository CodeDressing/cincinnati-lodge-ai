# ============================================================
# PROJECT MAPLE
# CINCINNATI LODGE AI
# ============================================================

# ============================================================
# SECTION 1 - IMPORTS
# ============================================================

from flask import Flask
from flask import render_template
import json


# ============================================================
# SECTION 2 - APPLICATION CREATION
# ============================================================

app = Flask(__name__)


# ============================================================
# SECTION 3 - DATA LOADERS
# ============================================================

def load_lodge_info():

    with open("data/lodge_info.json", "r", encoding="utf-8") as file:
        return json.load(file)


def load_events():

    with open("data/events.json", "r", encoding="utf-8") as file:
        return json.load(file)


def load_faqs():

    with open("data/faq.json", "r", encoding="utf-8") as file:
        return json.load(file)


def load_seo_pages():

    with open("data/seo_pages.json", "r", encoding="utf-8") as file:
        return json.load(file)


# ============================================================
# SECTION 4 - HOME PAGE
# ============================================================

@app.route("/")
def home():

    lodge_info = load_lodge_info()
    events = load_events()
    faqs = load_faqs()

    return render_template(
        "index.html",
        lodge_info=lodge_info,
        events=events,
        faqs=faqs
    )


# ============================================================
# SECTION 5 - EVENTS PAGE
# ============================================================

@app.route("/events/")
def events_page():

    return render_template(
        "events.html",
        events=load_events()
    )


# ============================================================
# SECTION 6 - ASSISTANT PAGE
# ============================================================

@app.route("/assistant/")
def assistant():

    return render_template(
        "assistant.html",
        answer=None,
        question=""
    )


# ============================================================
# SECTION 7 - ERROR HANDLER
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404


# ============================================================
# SECTION 8 - APPLICATION STARTUP
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )