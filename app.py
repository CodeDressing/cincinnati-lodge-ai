# ============================================================
# PROJECT MAPLE
# CINCINNATI LODGE AI
# PHASE 6 — SEO ENGINE FOUNDATION
# BLOCK 6.1 — app.py
# VERSION 6.1.0 — ENTERPRISE SEO ROUTING UPGRADE
# ============================================================

from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime


# ============================================================
# SECTION 6.1.1 — APPLICATION BASE
# ============================================================

app = Flask(__name__)


# ============================================================
# SECTION 6.1.2 — PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
STORAGE_DIR = os.path.join(BASE_DIR, "storage")

LODGE_INFO_PATH = os.path.join(DATA_DIR, "lodge_info.json")
EVENTS_PATH = os.path.join(DATA_DIR, "events.json")
FAQ_PATH = os.path.join(DATA_DIR, "faq.json")
SEO_PAGES_PATH = os.path.join(DATA_DIR, "seo_pages.json")
QUESTION_LOG_PATH = os.path.join(BASE_DIR, "question_log.csv")


# ============================================================
# SECTION 6.1.3 — SAFE JSON LOADER
# ============================================================

def load_json(path):
    if not os.path.exists(path):
        return {}

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}


# ============================================================
# SECTION 6.1.4 — DATA ACCESS LAYER
# ============================================================

def get_lodge_info():
    return load_json(LODGE_INFO_PATH)


def get_events():
    data = load_json(EVENTS_PATH)
    return data.get("events", [])


def get_faqs():
    data = load_json(FAQ_PATH)
    return data.get("faq_sections", [])


def get_seo_pages():
    data = load_json(SEO_PAGES_PATH)
    return data.get("seo_pages", data.get("pages", []))


# ============================================================
# SECTION 6.1.5 — LOOKUP HELPERS
# ============================================================

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
# SECTION 6.1.6 — SEO PAGE BUILDER
# ============================================================

def build_static_page(title, headline, primary_keyword, meta_description, content):
    return {
        "title": title,
        "headline": headline,
        "primary_keyword": primary_keyword,
        "meta_description": meta_description,
        "content": content,
        "secondary_keywords": [],
        "slug": "",
        "page_type": "static_seo_page",
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }


# ============================================================
# SECTION 6.1.7 — QUESTION LOGGING ENGINE
# ============================================================

def log_question(question, source="assistant"):
    if not question:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clean_question = question.replace("\n", " ").replace(",", " ")

    log_line = f"{timestamp},{source},{clean_question}\n"

    with open(QUESTION_LOG_PATH, "a", encoding="utf-8") as file:
        file.write(log_line)


# ============================================================
# SECTION 6.1.8 — SIMPLE ASSISTANT RESPONSE ENGINE
# ============================================================

def generate_assistant_answer(question):
    lower_question = question.lower()

    if "event" in lower_question or "rental" in lower_question or "venue" in lower_question:
        return (
            "Cincinnati Lodge No. III can provide general information about public events, "
            "community programs, and venue-use topics. Official availability, rental details, "
            "pricing, and scheduling should always be confirmed directly through the lodge."
        )

    if "mason" in lower_question or "membership" in lower_question or "join" in lower_question:
        return (
            "Freemasonry is centered on brotherhood, integrity, service, charity, personal growth, "
            "and moral improvement. Men interested in learning more about membership can use this "
            "assistant as a starting point, but official membership conversations should happen "
            "directly with Cincinnati Lodge No. III."
        )

    if "history" in lower_question or "lodge" in lower_question:
        return (
            "Cincinnati Lodge No. III is connected to the historic Masonic tradition in Morristown, "
            "New Jersey. The lodge website and assistant are being developed to help explain lodge "
            "history, public programs, community involvement, and general Masonic information."
        )

    return (
        "Thank you for your question. This assistant provides general informational guidance about "
        "Cincinnati Lodge No. III, Freemasonry, lodge history, public events, community involvement, "
        "venue-use topics, and membership interest. Official lodge matters should be confirmed "
        "directly with Cincinnati Lodge No. III."
    )


# ============================================================
# SECTION 6.1.9 — TEMPLATE CONTEXT BUILDER
# ============================================================

def build_global_context():
    return {
        "lodge_info": get_lodge_info(),
        "events": get_events(),
        "faqs": get_faqs(),
        "seo_pages": get_seo_pages()
    }


# ============================================================
# SECTION 6.1.10 — HOME PAGE ROUTE
# ============================================================

@app.route("/")
def home():
    context = build_global_context()

    return render_template(
        "index.html",
        **context
    )


# ============================================================
# SECTION 6.1.11 — EVENTS ROUTES
# ============================================================

@app.route("/events/")
def events_page():
    context = build_global_context()

    return render_template(
        "events.html",
        **context
    )


@app.route("/events/<slug>/")
def event_detail(slug):
    event = get_event_by_slug(slug)

    if event is None:
        return render_template("404.html", lodge_info=get_lodge_info()), 404

    return render_template(
        "event_detail.html",
        lodge_info=get_lodge_info(),
        event=event,
        seo_pages=get_seo_pages()
    )


# ============================================================
# SECTION 6.1.12 — CORE SEO LANDING ROUTES
# ============================================================

@app.route("/venue/")
def venue_page():
    page = build_static_page(
        title="Venue Rentals in Morristown NJ",
        headline="A Flexible Event and Meeting Space in Morristown",
        primary_keyword="Morristown Event Venue",
        meta_description="Explore venue rental opportunities at Morristown Masonic Center, a flexible space for meetings, private events, workshops, community programs, and celebrations in Morristown, NJ.",
        content="The Morristown Masonic Center at 39 Maple Ave can support private gatherings, business meetings, educational programs, networking events, community functions, workshops, and selected celebrations."
    )

    return render_template(
        "seo_page.html",
        lodge_info=get_lodge_info(),
        page=page,
        seo_pages=get_seo_pages(),
        faqs=get_faqs()
    )


@app.route("/membership/")
def membership_page():
    page = build_static_page(
        title="Become a Mason in New Jersey",
        headline="Brotherhood, Leadership, Service, and Personal Growth",
        primary_keyword="Become a Mason NJ",
        meta_description="Learn about Freemasonry, brotherhood, leadership, service, personal development, and how interested men can begin learning about membership at Morristown Masonic Center.",
        content="Freemasonry is centered on brotherhood, integrity, charity, service, leadership, education, and lifelong self-improvement."
    )

    return render_template(
        "seo_page.html",
        lodge_info=get_lodge_info(),
        page=page,
        seo_pages=get_seo_pages(),
        faqs=get_faqs()
    )


@app.route("/contact/")
def contact_page():
    page = build_static_page(
        title="Contact Morristown Masonic Center",
        headline="Connect With the Lodge",
        primary_keyword="Morristown Masonic Center Contact",
        meta_description="Contact Morristown Masonic Center at 39 Maple Ave in Morristown, NJ for event information, venue rental questions, community programs, and membership interest.",
        content="Morristown Masonic Center is located at 39 Maple Ave, Morristown, NJ 07960."
    )

    return render_template(
        "seo_page.html",
        lodge_info=get_lodge_info(),
        page=page,
        seo_pages=get_seo_pages(),
        faqs=get_faqs()
    )


@app.route("/faq/")
def faq_page():
    page = build_static_page(
        title="Frequently Asked Questions",
        headline="Questions About the Lodge, Events, Venue Rentals, and Freemasonry",
        primary_keyword="Morristown Masonic Center FAQ",
        meta_description="Find answers to common questions about Morristown Masonic Center, venue rentals, events, community programs, Freemasonry, membership, and Lodge activities.",
        content="This page organizes common questions about venue rentals, membership, events, community programs, business networking, and lodge programming."
    )

    return render_template(
        "seo_page.html",
        lodge_info=get_lodge_info(),
        page=page,
        seo_pages=get_seo_pages(),
        faqs=get_faqs()
    )


# ============================================================
# SECTION 6.1.13 — SEO INDEX AND DYNAMIC SEO ROUTES
# ============================================================

@app.route("/seo/")
def seo_index():
    pages = get_seo_pages()

    page = build_static_page(
        title="SEO Landing Pages",
        headline="Cincinnati Lodge AI SEO Engine",
        primary_keyword="Morristown Masonic Center SEO",
        meta_description="SEO landing pages for Morristown Masonic Center, Cincinnati Lodge No. III, public events, venue rentals, membership interest, and community programming.",
        content="These pages support local search visibility for venue rentals, community events, membership education, lodge history, and Morristown-based searches."
    )

    return render_template(
        "seo_page.html",
        lodge_info=get_lodge_info(),
        page=page,
        seo_pages=pages,
        faqs=get_faqs()
    )


@app.route("/<slug>/")
def seo_page(slug):
    reserved_slugs = {
        "events",
        "venue",
        "membership",
        "contact",
        "faq",
        "assistant",
        "seo",
        "static",
        "api"
    }

    if slug in reserved_slugs:
        return render_template("404.html", lodge_info=get_lodge_info()), 404

    page = get_seo_page_by_slug(slug)

    if page is None:
        return render_template("404.html", lodge_info=get_lodge_info()), 404

    return render_template(
        "seo_page.html",
        lodge_info=get_lodge_info(),
        page=page,
        seo_pages=get_seo_pages(),
        faqs=get_faqs()
    )


# ============================================================
# SECTION 6.1.14 — ASSISTANT ROUTE
# ============================================================

@app.route("/assistant/", methods=["GET", "POST"])
def assistant():
    question = ""
    answer = None

    if request.method == "POST":
        question = request.form.get("question", "").strip()

        if question:
            log_question(question, source="assistant")
            answer = generate_assistant_answer(question)
        else:
            answer = "Please enter a question so the Lodge Assistant can respond."

    return render_template(
        "assistant.html",
        lodge_info=get_lodge_info(),
        question=question,
        answer=answer,
        seo_pages=get_seo_pages(),
        faqs=get_faqs()
    )


# ============================================================
# SECTION 6.1.15 — API HEALTH CHECKS
# ============================================================

@app.route("/api/health/")
def api_health():
    return jsonify({
        "status": "healthy",
        "project": "Cincinnati Lodge AI",
        "version": "6.1.0",
        "seo_engine": "active",
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/seo-pages/")
def api_seo_pages():
    return jsonify({
        "count": len(get_seo_pages()),
        "seo_pages": get_seo_pages()
    })


@app.route("/api/events/")
def api_events():
    return jsonify({
        "count": len(get_events()),
        "events": get_events()
    })


# ============================================================
# SECTION 6.1.16 — ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "404.html",
        lodge_info=get_lodge_info(),
        seo_pages=get_seo_pages()
    ), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template(
        "404.html",
        lodge_info=get_lodge_info(),
        seo_pages=get_seo_pages()
    ), 500


# ============================================================
# SECTION 6.1.17 — LOCAL STARTUP
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)