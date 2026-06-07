# ============================================================
# PROJECT MAPLE
# CINCINNATI LODGE AI
# PHASE 5 — ROUTING LAYER
# BLOCK 5.1 — app.py
# VERSION 5.2.0 — ROUTE STABILITY UPGRADE
# ============================================================

from flask import Flask, render_template, request
import json
import os


# ============================================================
# SECTION 5.1.1 — APPLICATION FACTORY BASE
# ============================================================

app = Flask(__name__)


# ============================================================
# SECTION 5.1.2 — JSON DATA LOADER
# ============================================================

def load_json(path):
    if not os.path.exists(path):
        return {}

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


# ============================================================
# SECTION 5.1.3 — DATA ACCESS FUNCTIONS
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
    return data.get("seo_pages", data.get("pages", []))


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
# SECTION 5.1.4 — SHARED PAGE FALLBACK BUILDER
# ============================================================

def build_static_page(title, headline, primary_keyword, meta_description, content):
    return {
        "title": title,
        "headline": headline,
        "primary_keyword": primary_keyword,
        "meta_description": meta_description,
        "content": content,
        "secondary_keywords": [],
        "slug": ""
    }


# ============================================================
# SECTION 5.1.5 — HOME PAGE
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
# SECTION 5.1.6 — EVENTS ROUTES
# ============================================================

@app.route("/events/")
def events_page():
    return render_template(
        "events.html",
        lodge_info=get_lodge_info(),
        events=get_events()
    )


@app.route("/events/<slug>/")
def event_detail(slug):
    event = get_event_by_slug(slug)

    if event is None:
        return render_template("404.html"), 404

    return render_template(
        "event_detail.html",
        lodge_info=get_lodge_info(),
        event=event
    )


# ============================================================
# SECTION 5.1.7 — VENUE ROUTE
# ============================================================

@app.route("/venue/")
def venue_page():
    page = build_static_page(
        title="Venue Rentals",
        headline="A Flexible Event and Meeting Space in Morristown",
        primary_keyword="Morristown Event Venue",
        meta_description="Explore venue rental opportunities at Morristown Masonic Center, a flexible space for meetings, private events, workshops, community programs, and celebrations in Morristown, NJ.",
        content="The Morristown Masonic Center at 39 Maple Ave can support private gatherings, business meetings, educational programs, networking events, community functions, workshops, and selected celebrations. This page is ready to become the main venue rental conversion page for Project Maple."
    )

    return render_template(
        "seo_page.html",
        lodge_info=get_lodge_info(),
        page=page,
        seo_pages=get_seo_pages()
    )


# ============================================================
# SECTION 5.1.8 — MEMBERSHIP ROUTE
# ============================================================

@app.route("/membership/")
def membership_page():
    page = build_static_page(
        title="Become a Mason",
        headline="Brotherhood, Leadership, Service, and Personal Growth",
        primary_keyword="Become a Mason NJ",
        meta_description="Learn about Freemasonry, brotherhood, leadership, service, personal development, and how interested men can begin learning about membership at Morristown Masonic Center.",
        content="Freemasonry is centered on brotherhood, integrity, charity, service, leadership, education, and lifelong self-improvement. This page is ready to become the main membership pathway for men interested in learning more about becoming a Mason in New Jersey."
    )

    return render_template(
        "seo_page.html",
        lodge_info=get_lodge_info(),
        page=page,
        seo_pages=get_seo_pages()
    )


# ============================================================
# SECTION 5.1.9 — CONTACT ROUTE
# ============================================================

@app.route("/contact/")
def contact_page():
    page = build_static_page(
        title="Contact Morristown Masonic Center",
        headline="Connect With the Lodge",
        primary_keyword="Morristown Masonic Center Contact",
        meta_description="Contact Morristown Masonic Center at 39 Maple Ave in Morristown, NJ for event information, venue rental questions, community programs, and membership interest.",
        content="Morristown Masonic Center is located at 39 Maple Ave, Morristown, NJ 07960. This page is ready to become the main contact and inquiry page for venue rentals, community programs, events, and membership questions."
    )

    return render_template(
        "seo_page.html",
        lodge_info=get_lodge_info(),
        page=page,
        seo_pages=get_seo_pages()
    )


# ============================================================
# SECTION 5.1.10 — FAQ ROUTE
# ============================================================

@app.route("/faq/")
def faq_page():
    page = build_static_page(
        title="Frequently Asked Questions",
        headline="Questions About the Lodge, Events, Venue Rentals, and Freemasonry",
        primary_keyword="Morristown Masonic Center FAQ",
        meta_description="Find answers to common questions about Morristown Masonic Center, venue rentals, events, community programs, Freemasonry, membership, and Lodge activities.",
        content="This page organizes common questions about venue rentals, membership, events, Debate Night Live, Community Chess Club, business networking, and Lodge programming."
    )

    return render_template(
        "seo_page.html",
        lodge_info=get_lodge_info(),
        page=page,
        seo_pages=get_seo_pages(),
        faqs=get_faqs()
    )


# ============================================================
# SECTION 5.1.11 — SEO ROUTES
# ============================================================

@app.route("/seo/")
def seo_index():
    pages = get_seo_pages()

    page = build_static_page(
        title="SEO Pages",
        headline="SEO Landing Pages",
        primary_keyword="Morristown Masonic Center SEO",
        meta_description="SEO landing pages for the Morristown Masonic Center.",
        content="These pages support venue, community, event, and membership visibility."
    )

    return render_template(
        "seo_page.html",
        lodge_info=get_lodge_info(),
        page=page,
        seo_pages=pages
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
        "static"
    }

    if slug in reserved_slugs:
        return render_template("404.html"), 404

    page = get_seo_page_by_slug(slug)

    if page is None:
        return render_template("404.html"), 404

    return render_template(
        "seo_page.html",
        lodge_info=get_lodge_info(),
        page=page,
        seo_pages=get_seo_pages()
    )


# ============================================================
# SECTION 5.1.12 — ASSISTANT ROUTE
# ============================================================

@app.route("/assistant/", methods=["GET", "POST"])
def assistant():
    question = ""
    answer = None

    if request.method == "POST":
        question = request.form.get("question", "").strip()

        if question:
            answer = (
                "Cincinnati Lodge AI received your question. "
                "The full AI service layer will be connected in a later phase. "
                "For now, this route is stable, the form works, and the assistant page is ready for Phase 7 integration."
            )
        else:
            answer = "Please enter a question so the Lodge Assistant can respond."

    return render_template(
        "assistant.html",
        lodge_info=get_lodge_info(),
        question=question,
        answer=answer
    )


# ============================================================
# SECTION 5.1.13 — ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("404.html"), 500


# ============================================================
# SECTION 5.1.14 — LOCAL STARTUP
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)