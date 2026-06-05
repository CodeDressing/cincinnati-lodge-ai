# ============================================================
# PROJECT MAPLE
# CINCINNATI LODGE AI
# PHASE 5 — ROUTING LAYER
# BLOCK 5.1 — app.py
# VERSION 5.1.1 — DATA SHAPE FIX
# ============================================================

from flask import Flask, render_template, request
import json


app = Flask(__name__)


# ============================================================
# SECTION 5.1.1 — JSON DATA LOADER
# ============================================================

def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


# ============================================================
# SECTION 5.1.2 — DATA ACCESS FUNCTIONS
# ============================================================

def get_lodge_info():
    return load_json("data/lodge_info.json")


def get_events():
    data = load_json("data/events.json")
    return data.get("events", [])


def get_faqs():
    data = load_json("data/faq.json")
    return data.get("faq_sections", [])


def get_seo_pages():
    data = load_json("data/seo_pages.json")
    return data.get("seo_pages", [])


def get_event_by_slug(slug):
    for event in get_events():
        if event.get("slug") == slug:
            return event
    return None


def get_seo_page_by_slug(slug):
    for page in get_seo_pages():
        if page.get("slug") == slug:
            return page
    return None


# ============================================================
# SECTION 5.1.3 — HOME PAGE
# ============================================================

@app.route("/")
def home():
    return render_template(
        "index.html",
        lodge_info=get_lodge_info(),
        events=get_events(),
        faqs=get_faqs()
    )


# ============================================================
# SECTION 5.1.4 — EVENTS
# ============================================================

@app.route("/events/")
def events_page():
    return render_template(
        "events.html",
        events=get_events()
    )


@app.route("/events/<slug>/")
def event_detail(slug):
    event = get_event_by_slug(slug)

    if event is None:
        return render_template("404.html"), 404

    return render_template(
        "event_detail.html",
        event=event
    )


# ============================================================
# SECTION 5.1.5 — SEO PAGES
# ============================================================

@app.route("/seo/")
def seo_index():
    pages = get_seo_pages()

    return render_template(
        "seo_page.html",
        page={
            "title": "SEO Pages",
            "meta_description": "SEO landing pages for the Morristown Masonic Center.",
            "primary_keyword": "Morristown Masonic Center SEO",
            "headline": "SEO Landing Pages",
            "content": "These pages support venue, community, event, and membership visibility."
        },
        seo_pages=pages
    )


@app.route("/<slug>/")
def seo_page(slug):
    page = get_seo_page_by_slug(slug)

    if page is None:
        return render_template("404.html"), 404

    return render_template(
        "seo_page.html",
        page=page,
        seo_pages=get_seo_pages()
    )


# ============================================================
# SECTION 5.1.6 — ASSISTANT
# ============================================================

@app.route("/assistant/", methods=["GET", "POST"])
def assistant():
    question = ""
    answer = None

    if request.method == "POST":
        question = request.form.get("question", "")
        answer = "Cincinnati Lodge AI received your question. Full AI logic will be added in a later phase."

    return render_template(
        "assistant.html",
        question=question,
        answer=answer
    )


# ============================================================
# SECTION 5.1.7 — ERROR HANDLER
# ============================================================

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


# ============================================================
# SECTION 5.1.8 — LOCAL STARTUP
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)