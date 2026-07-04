# ============================================================
# PROJECT MAPLE / CINCINNATI LODGE AI
# FILE: app.py
# PHASE 8 — AI ASSISTANT INTELLIGENCE LAYER
# BLOCK 8.2 — Retrieval-Based Knowledge Assistant
# VERSION 8.2.0
# DATE: 2026-06-14
# PURPOSE:
# Controls Flask routing, JSON data loading, SEO page rendering,
# event routing, question logging, API endpoints, and the first
# retrieval-based assistant engine using FAQ, event, SEO, and
# lodge information datasets.
# ============================================================

from flask import Flask, render_template, request, jsonify
import json
import os
import re
from datetime import datetime


# ============================================================
# SECTION 8.2.1 — APPLICATION BASE
# ============================================================

app = Flask(__name__)


# ============================================================
# SECTION 8.2.2 — PROJECT PATHS
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
# SECTION 8.2.3 — SAFE JSON LOADER
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
# SECTION 8.2.4 — DATA ACCESS LAYER
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
# SECTION 8.2.5 — LOOKUP HELPERS
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
# SECTION 8.2.6 — TEXT NORMALIZATION HELPERS
# ============================================================

def normalize_text(value):
    if value is None:
        return ""

    value = str(value).lower()
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()

    return value


def tokenize_text(value):
    stop_words = {
        "a", "an", "and", "are", "as", "at", "be", "by", "can",
        "do", "does", "for", "from", "how", "i", "in", "is",
        "it", "of", "on", "or", "the", "this", "to", "we",
        "what", "when", "where", "who", "why", "with", "you"
    }

    normalized = normalize_text(value)

    return [
        token for token in normalized.split()
        if token not in stop_words and len(token) > 2
    ]


def score_text_match(question, target_text):
    question_tokens = set(tokenize_text(question))
    target_tokens = set(tokenize_text(target_text))

    if not question_tokens or not target_tokens:
        return 0

    direct_matches = question_tokens.intersection(target_tokens)
    score = len(direct_matches) * 10

    normalized_question = normalize_text(question)
    normalized_target = normalize_text(target_text)

    for token in question_tokens:
        if token in normalized_target:
            score += 2

    if normalized_question and normalized_question in normalized_target:
        score += 25

    return score


# ============================================================
# SECTION 8.2.7 — KNOWLEDGE INDEX BUILDER
# ============================================================

def build_knowledge_index():
    knowledge_items = []

    for section in get_faqs():
        section_name = section.get("section", "FAQ Section")

        for item in section.get("items", []):
            keywords = " ".join(item.get("keywords", []))

            knowledge_items.append({
                "type": "faq",
                "source": section_name,
                "title": item.get("question", "FAQ"),
                "answer": item.get("answer", ""),
                "url": "/faq/",
                "search_text": " ".join([
                    item.get("question", ""),
                    item.get("answer", ""),
                    keywords
                ])
            })

    for event in get_events():
        keywords = " ".join(event.get("seo_keywords", []))
        topic_examples = " ".join(event.get("topic_examples", []))
        revenue = " ".join(event.get("revenue_opportunities", []))
        rules = " ".join(event.get("rules", []))

        knowledge_items.append({
            "type": "event",
            "source": "Event Database",
            "title": event.get("title", "Event"),
            "answer": event.get("summary", event.get("short_description", "")),
            "url": f"/events/{event.get('slug', '')}/",
            "search_text": " ".join([
                event.get("title", ""),
                event.get("category", ""),
                event.get("program_type", ""),
                event.get("short_description", ""),
                event.get("summary", ""),
                event.get("details", ""),
                keywords,
                topic_examples,
                revenue,
                rules
            ])
        })

    for page in get_seo_pages():
        keywords = " ".join(page.get("secondary_keywords", []))

        knowledge_items.append({
            "type": "seo_page",
            "source": "SEO Page Database",
            "title": page.get("title", "Information Page"),
            "answer": page.get("meta_description", page.get("content", "")),
            "url": f"/{page.get('slug', '')}/",
            "search_text": " ".join([
                page.get("title", ""),
                page.get("headline", ""),
                page.get("primary_keyword", ""),
                page.get("meta_description", ""),
                page.get("content", ""),
                keywords
            ])
        })

    lodge_info = get_lodge_info()

    if lodge_info:
        knowledge_items.append({
            "type": "lodge_info",
            "source": "Lodge Information Database",
            "title": "Cincinnati Lodge No. III",
            "answer": (
                "Cincinnati Lodge No. III is connected to Morristown Masonic Center "
                "at 39 Maple Ave in Morristown, New Jersey. The Lodge supports "
                "brotherhood, service, leadership, education, community presence, "
                "venue information, events, and membership interest."
            ),
            "url": "/",
            "search_text": json.dumps(lodge_info)
        })

    return knowledge_items


# ============================================================
# SECTION 8.2.8 — RETRIEVAL ENGINE
# ============================================================

def retrieve_relevant_knowledge(question, limit=3):
    scored_items = []

    for item in build_knowledge_index():
        score = score_text_match(question, item.get("search_text", ""))

        if score > 0:
            scored_items.append({
                "score": score,
                "item": item
            })

    scored_items.sort(key=lambda result: result["score"], reverse=True)

    return scored_items[:limit]


# ============================================================
# SECTION 8.2.9 — INTENT CLASSIFICATION ENGINE
# ============================================================

def classify_question_intent(question):
    lower_question = normalize_text(question)

    intent_map = {
        "venue_rental": [
            "venue", "rent", "rental", "space", "meeting", "banquet",
            "fundraiser", "workshop", "business", "corporate", "private"
        ],
        "events": [
            "event", "events", "debate", "chess", "comedy", "networking",
            "halloween", "luck", "program", "programs"
        ],
        "membership": [
            "mason", "masonic", "freemason", "freemasonry", "join",
            "membership", "brotherhood", "petition"
        ],
        "location": [
            "where", "address", "location", "parking", "morristown",
            "maple", "directions"
        ],
        "seo_strategy": [
            "seo", "google", "search", "rank", "keyword", "traffic",
            "landing", "page"
        ]
    }

    scores = {}

    for intent, terms in intent_map.items():
        scores[intent] = sum(1 for term in terms if term in lower_question)

    best_intent = max(scores, key=scores.get)

    if scores[best_intent] == 0:
        return "general_information"

    return best_intent


# ============================================================
# SECTION 8.2.10 — ASSISTANT RESPONSE COMPOSER
# ============================================================

def compose_retrieval_answer(question):
    intent = classify_question_intent(question)
    matches = retrieve_relevant_knowledge(question, limit=3)

    if not matches:
        return (
            "I can help with general information about Cincinnati Lodge No. III, "
            "Morristown Masonic Center, venue rentals, public events, Freemasonry, "
            "membership interest, community programs, and lodge information. "
            "For official scheduling, rental approval, pricing, or membership matters, "
            "please contact the Lodge directly."
        )

    top_match = matches[0]["item"]

    answer_parts = [
        f"Based on the Lodge knowledge base, the closest match is: {top_match.get('title')}."
    ]

    if top_match.get("answer"):
        answer_parts.append(top_match.get("answer"))

    if intent == "venue_rental":
        answer_parts.append(
            "For venue use, scheduling, approval, pricing, and availability, official confirmation should come directly from the Lodge."
        )

    if intent == "membership":
        answer_parts.append(
            "For membership interest, the assistant can provide general educational information, but official membership steps should be handled directly with Cincinnati Lodge No. III."
        )

    if intent == "events":
        answer_parts.append(
            "You can also explore the Events page for current program concepts and event detail pages."
        )

    related_links = []

    for result in matches:
        item = result["item"]

        if item.get("url") and item.get("title"):
            related_links.append(f"{item.get('title')}: {item.get('url')}")

    if related_links:
        answer_parts.append("Related pages: " + " | ".join(related_links))

    return " ".join(answer_parts)


# ============================================================
# SECTION 8.2.11 — SEO PAGE BUILDER
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
# SECTION 8.2.12 — QUESTION LOGGING ENGINE
# ============================================================

def log_question(question, source="assistant"):
    if not question:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clean_question = question.replace("\n", " ").replace(",", " ")
    intent = classify_question_intent(question)

    log_line = f"{timestamp},{source},{intent},{clean_question}\n"

    with open(QUESTION_LOG_PATH, "a", encoding="utf-8") as file:
        file.write(log_line)


# ============================================================
# SECTION 8.2.13 — TEMPLATE CONTEXT BUILDER
# ============================================================

def build_global_context():
    return {
        "lodge_info": get_lodge_info(),
        "events": get_events(),
        "faqs": get_faqs(),
        "seo_pages": get_seo_pages()
    }


# ============================================================
# SECTION 8.2.14 — HOME PAGE ROUTE
# ============================================================

@app.route("/")
def home():
    context = build_global_context()

    return render_template(
        "index.html",
        **context
    )


# ============================================================
# SECTION 8.2.15 — EVENTS ROUTES
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
# SECTION 8.2.16 — CORE SEO LANDING ROUTES
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
# SECTION 8.2.17 — SEO INDEX AND DYNAMIC SEO ROUTES
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
# SECTION 8.2.18 — ASSISTANT ROUTE
# ============================================================

@app.route("/assistant/", methods=["GET", "POST"])
def assistant():
    question = ""
    answer = None

    if request.method == "POST":
        question = request.form.get("question", "").strip()

        if question:
            log_question(question, source="assistant")
            answer = compose_retrieval_answer(question)
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
# SECTION 8.2.19 — ASSISTANT API ROUTES
# ============================================================

@app.route("/api/assistant/ask/", methods=["POST"])
def api_assistant_ask():
    payload = request.get_json(silent=True) or {}
    question = payload.get("question", "").strip()

    if not question:
        return jsonify({
            "status": "error",
            "message": "Question is required."
        }), 400

    log_question(question, source="api_assistant")

    matches = retrieve_relevant_knowledge(question, limit=3)

    return jsonify({
        "status": "success",
        "question": question,
        "intent": classify_question_intent(question),
        "answer": compose_retrieval_answer(question),
        "matches": [
            {
                "score": match["score"],
                "type": match["item"].get("type"),
                "title": match["item"].get("title"),
                "url": match["item"].get("url")
            }
            for match in matches
        ]
    })


# ============================================================
# SECTION 8.2.20 — API HEALTH AND DATA ENDPOINTS
# ============================================================

@app.route("/api/health/")
def api_health():
    return jsonify({
        "status": "healthy",
        "project": "Cincinnati Lodge AI",
        "version": "8.2.0",
        "seo_engine": "active",
        "assistant_engine": "retrieval_based",
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


@app.route("/api/knowledge-index/")
def api_knowledge_index():
    knowledge_items = build_knowledge_index()

    return jsonify({
        "count": len(knowledge_items),
        "items": [
            {
                "type": item.get("type"),
                "source": item.get("source"),
                "title": item.get("title"),
                "url": item.get("url")
            }
            for item in knowledge_items
        ]
    })


# ============================================================
# SECTION 8.2.21 — ERROR HANDLERS
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
# SECTION 8.2.22 — LOCAL STARTUP
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)