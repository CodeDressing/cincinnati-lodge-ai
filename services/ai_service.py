# ============================================================
# PROJECT MAPLE / CINCINNATI LODGE AI
# FILE: services/ai_service.py
# PHASE 9 — AI PREDICTION SERVICE LAYER
# BLOCK 9.2 — Predictive AI Orchestration Service
# VERSION 9.2.0
# DATE: 2026-06-14
# PURPOSE:
# Central AI service for question intent prediction, opportunity
# scoring, knowledge retrieval, recommendation prediction, SEO
# priority forecasting, event recommendation, and future machine
# learning / deep learning expansion.
# ============================================================

import json
import os
import re
from datetime import datetime


# ============================================================
# SECTION 9.2.1 — PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

LODGE_INFO_PATH = os.path.join(DATA_DIR, "lodge_info.json")
EVENTS_PATH = os.path.join(DATA_DIR, "events.json")
FAQ_PATH = os.path.join(DATA_DIR, "faq.json")
SEO_PAGES_PATH = os.path.join(DATA_DIR, "seo_pages.json")
QUESTION_LOG_PATH = os.path.join(BASE_DIR, "question_log.csv")


# ============================================================
# SECTION 9.2.2 — SAFE DATA LOADING
# ============================================================

def load_json(path):
    if not os.path.exists(path):
        return {}

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}


def get_lodge_info():
    return load_json(LODGE_INFO_PATH)


def get_events():
    return load_json(EVENTS_PATH).get("events", [])


def get_faq_sections():
    return load_json(FAQ_PATH).get("faq_sections", [])


def get_seo_pages():
    data = load_json(SEO_PAGES_PATH)
    return data.get("seo_pages", data.get("pages", []))


# ============================================================
# SECTION 9.2.3 — TEXT NORMALIZATION PIPELINE
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
        "could", "do", "does", "for", "from", "how", "i", "in",
        "is", "it", "me", "my", "of", "on", "or", "our", "the",
        "this", "to", "we", "what", "when", "where", "who", "why",
        "with", "you", "your", "about", "there", "here"
    }

    normalized = normalize_text(value)

    return [
        token for token in normalized.split()
        if token not in stop_words and len(token) > 2
    ]


# ============================================================
# SECTION 9.2.4 — INTENT MODEL
# ============================================================

INTENT_MODEL = {
    "venue_rental": {
        "label": "Venue Rental Intent",
        "terms": [
            "venue", "rent", "rental", "space", "meeting", "banquet",
            "fundraiser", "workshop", "business", "corporate", "private",
            "party", "event", "room", "hall", "host", "reserve"
        ],
        "base_value": 95
    },
    "events": {
        "label": "Event Discovery Intent",
        "terms": [
            "event", "events", "debate", "chess", "comedy", "networking",
            "halloween", "luck", "program", "programs", "calendar",
            "night", "show", "club", "attend"
        ],
        "base_value": 88
    },
    "membership": {
        "label": "Membership Interest Intent",
        "terms": [
            "mason", "masonic", "freemason", "freemasonry", "join",
            "membership", "brotherhood", "petition", "become"
        ],
        "base_value": 82
    },
    "seo_strategy": {
        "label": "SEO Strategy Intent",
        "terms": [
            "seo", "google", "search", "rank", "keyword", "traffic",
            "landing", "page", "content", "visibility"
        ],
        "base_value": 78
    },
    "location": {
        "label": "Location Intent",
        "terms": [
            "where", "address", "location", "parking", "morristown",
            "maple", "directions", "near", "visit"
        ],
        "base_value": 65
    }
}


# ============================================================
# SECTION 9.2.5 — INTENT PREDICTION ENGINE
# ============================================================

def predict_intent(question):
    normalized_question = normalize_text(question)
    scored_intents = []

    for intent_key, config in INTENT_MODEL.items():
        score = 0

        for term in config["terms"]:
            if term in normalized_question:
                score += 10

        if score > 0:
            scored_intents.append({
                "intent": intent_key,
                "label": config["label"],
                "score": score,
                "base_value": config["base_value"]
            })

    if not scored_intents:
        return {
            "intent": "general_information",
            "label": "General Information Intent",
            "score": 0,
            "confidence": 0.25,
            "base_value": 50
        }

    scored_intents.sort(
        key=lambda item: (item["score"], item["base_value"]),
        reverse=True
    )

    best = scored_intents[0]
    confidence = min(0.96, 0.35 + (best["score"] / 100))

    return {
        "intent": best["intent"],
        "label": best["label"],
        "score": best["score"],
        "confidence": round(confidence, 2),
        "base_value": best["base_value"]
    }


# ============================================================
# SECTION 9.2.6 — OPPORTUNITY PREDICTION ENGINE
# ============================================================

def predict_opportunity_score(question, intent_result):
    tokens = tokenize_text(question)
    token_count = len(tokens)

    base_value = intent_result.get("base_value", 50)
    confidence = intent_result.get("confidence", 0.25)

    specificity_bonus = min(20, token_count * 2)

    commercial_terms = {
        "rent", "rental", "venue", "business", "corporate",
        "fundraiser", "private", "meeting", "banquet", "workshop"
    }

    commercial_bonus = 0

    for token in tokens:
        if token in commercial_terms:
            commercial_bonus += 5

    commercial_bonus = min(commercial_bonus, 20)

    raw_score = (base_value * confidence) + specificity_bonus + commercial_bonus

    final_score = max(1, min(100, round(raw_score)))

    if final_score >= 85:
        tier = "High Opportunity"
    elif final_score >= 65:
        tier = "Medium Opportunity"
    else:
        tier = "Low Opportunity"

    return {
        "score": final_score,
        "tier": tier,
        "specificity_bonus": specificity_bonus,
        "commercial_bonus": commercial_bonus
    }


# ============================================================
# SECTION 9.2.7 — KNOWLEDGE ITEM BUILDERS
# ============================================================

def build_faq_items():
    items = []

    for section in get_faq_sections():
        section_name = section.get("section", "FAQ Section")

        for faq in section.get("items", []):
            keywords = " ".join(faq.get("keywords", []))

            items.append({
                "type": "faq",
                "source": section_name,
                "title": faq.get("question", "FAQ"),
                "summary": faq.get("answer", ""),
                "url": "/faq/",
                "search_text": " ".join([
                    faq.get("question", ""),
                    faq.get("answer", ""),
                    keywords
                ])
            })

    return items


def build_event_items():
    items = []

    for event in get_events():
        items.append({
            "type": "event",
            "source": "Event Database",
            "title": event.get("title", "Event"),
            "summary": event.get("summary", event.get("short_description", "")),
            "url": f"/events/{event.get('slug', '')}/",
            "search_text": " ".join([
                event.get("title", ""),
                event.get("category", ""),
                event.get("program_type", ""),
                event.get("short_description", ""),
                event.get("summary", ""),
                event.get("details", ""),
                " ".join(event.get("seo_keywords", [])),
                " ".join(event.get("rules", [])),
                " ".join(event.get("revenue_opportunities", []))
            ])
        })

    return items


def build_seo_page_items():
    items = []

    for page in get_seo_pages():
        items.append({
            "type": "seo_page",
            "source": "SEO Page Database",
            "title": page.get("title", "SEO Page"),
            "summary": page.get("meta_description", page.get("content", "")),
            "url": f"/{page.get('slug', '')}/",
            "search_text": " ".join([
                page.get("title", ""),
                page.get("headline", ""),
                page.get("primary_keyword", ""),
                page.get("meta_description", ""),
                page.get("content", ""),
                " ".join(page.get("secondary_keywords", []))
            ])
        })

    return items


def build_lodge_items():
    lodge_info = get_lodge_info()

    if not lodge_info:
        return []

    return [
        {
            "type": "lodge_info",
            "source": "Lodge Information Database",
            "title": "Cincinnati Lodge No. III",
            "summary": (
                "Cincinnati Lodge No. III is connected to Morristown Masonic Center "
                "at 39 Maple Ave in Morristown, New Jersey. The Lodge supports "
                "brotherhood, leadership, service, education, community programs, "
                "events, venue information, and membership interest."
            ),
            "url": "/",
            "search_text": json.dumps(lodge_info)
        }
    ]


def build_knowledge_index():
    return (
        build_faq_items()
        + build_event_items()
        + build_seo_page_items()
        + build_lodge_items()
    )


# ============================================================
# SECTION 9.2.8 — RETRIEVAL SCORING ENGINE
# ============================================================

def score_match(question, knowledge_text):
    question_tokens = set(tokenize_text(question))
    knowledge_tokens = set(tokenize_text(knowledge_text))

    if not question_tokens or not knowledge_tokens:
        return 0

    direct_overlap = question_tokens.intersection(knowledge_tokens)
    score = len(direct_overlap) * 12

    normalized_question = normalize_text(question)
    normalized_knowledge = normalize_text(knowledge_text)

    for token in question_tokens:
        if token in normalized_knowledge:
            score += 3

    if normalized_question and normalized_question in normalized_knowledge:
        score += 30

    return score


def retrieve_matches(question, limit=5):
    results = []

    for item in build_knowledge_index():
        score = score_match(question, item.get("search_text", ""))

        if score > 0:
            results.append({
                "score": score,
                "type": item.get("type"),
                "source": item.get("source"),
                "title": item.get("title"),
                "summary": item.get("summary"),
                "url": item.get("url")
            })

    results.sort(key=lambda item: item["score"], reverse=True)

    return results[:limit]


# ============================================================
# SECTION 9.2.9 — RECOMMENDATION PREDICTION ENGINE
# ============================================================

def predict_recommendations(question, intent_result, matches):
    recommendations = []
    intent = intent_result.get("intent")

    if intent == "venue_rental":
        recommendations.extend([
            {
                "label": "Explore Venue Rentals",
                "url": "/venue/",
                "reason": "Predicted rental, venue, or meeting-space intent."
            },
            {
                "label": "Morristown Event Venue",
                "url": "/morristown-event-venue/",
                "reason": "High-value local venue landing page."
            },
            {
                "label": "Morristown Meeting Space",
                "url": "/morristown-meeting-space/",
                "reason": "Relevant to meeting and space-related searches."
            }
        ])

    if intent == "events":
        recommendations.append({
            "label": "View Events",
            "url": "/events/",
            "reason": "Predicted event discovery intent."
        })

    if intent == "membership":
        recommendations.extend([
            {
                "label": "Become a Mason",
                "url": "/membership/",
                "reason": "Predicted membership or Freemasonry interest."
            },
            {
                "label": "Freemasonry in Morristown",
                "url": "/freemasonry-morristown-nj/",
                "reason": "Relevant educational landing page."
            }
        ])

    for match in matches[:3]:
        recommendations.append({
            "label": match.get("title"),
            "url": match.get("url"),
            "reason": f"Relevant {match.get('type')} match from the knowledge base."
        })

    seen_urls = set()
    unique = []

    for item in recommendations:
        url = item.get("url")

        if url and url not in seen_urls:
            unique.append(item)
            seen_urls.add(url)

    return unique[:5]


# ============================================================
# SECTION 9.2.10 — RESPONSE COMPOSITION ENGINE
# ============================================================

def compose_answer(question, intent_result, opportunity_result, matches, recommendations):
    if not matches:
        return (
            "I can help with general information about Cincinnati Lodge No. III, "
            "Morristown Masonic Center, venue rentals, events, Freemasonry, "
            "membership interest, community programs, and lodge information. "
            "For official scheduling, rental approval, pricing, or membership matters, "
            "please contact the Lodge directly."
        )

    top_match = matches[0]

    answer_parts = [
        f"I predicted this question as {intent_result.get('label')} "
        f"with {int(intent_result.get('confidence', 0) * 100)}% confidence.",
        f"Opportunity score: {opportunity_result.get('score')}/100 "
        f"({opportunity_result.get('tier')}).",
        f"The strongest knowledge match is: {top_match.get('title')}.",
        top_match.get("summary", "")
    ]

    if intent_result.get("intent") == "venue_rental":
        answer_parts.append(
            "For venue use, scheduling, approval, pricing, and availability, official confirmation should come directly from the Lodge."
        )

    if intent_result.get("intent") == "membership":
        answer_parts.append(
            "For membership interest, I can provide general educational information, but official membership steps should be handled directly with Cincinnati Lodge No. III."
        )

    if recommendations:
        links = [
            f"{item.get('label')}: {item.get('url')}"
            for item in recommendations
            if item.get("label") and item.get("url")
        ]

        if links:
            answer_parts.append("Recommended next steps: " + " | ".join(links))

    return " ".join(part for part in answer_parts if part)


# ============================================================
# SECTION 9.2.11 — QUESTION LOGGING / TRAINING DATA
# ============================================================

def log_question(question, source="ai_service"):
    if not question:
        return

    intent_result = predict_intent(question)
    opportunity_result = predict_opportunity_score(question, intent_result)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clean_question = question.replace("\n", " ").replace(",", " ")

    line = ",".join([
        timestamp,
        source,
        intent_result.get("intent", "general_information"),
        str(intent_result.get("confidence", 0)),
        str(opportunity_result.get("score", 0)),
        opportunity_result.get("tier", "Unknown"),
        clean_question
    ])

    with open(QUESTION_LOG_PATH, "a", encoding="utf-8") as file:
        file.write(line + "\n")


# ============================================================
# SECTION 9.2.12 — PUBLIC AI SERVICE API
# ============================================================

def process_question(question, source="ai_service"):
    question = (question or "").strip()

    if not question:
        return {
            "status": "error",
            "message": "Question is required.",
            "answer": "Please enter a question so Cincinnati Lodge AI can respond.",
            "intent": "none",
            "confidence": 0,
            "opportunity_score": 0,
            "opportunity_tier": "None",
            "matches": [],
            "recommendations": []
        }

    intent_result = predict_intent(question)
    opportunity_result = predict_opportunity_score(question, intent_result)
    matches = retrieve_matches(question, limit=5)

    recommendations = predict_recommendations(
        question=question,
        intent_result=intent_result,
        matches=matches
    )

    answer = compose_answer(
        question=question,
        intent_result=intent_result,
        opportunity_result=opportunity_result,
        matches=matches,
        recommendations=recommendations
    )

    log_question(question, source=source)

    return {
        "status": "success",
        "question": question,
        "intent": intent_result.get("intent"),
        "intent_label": intent_result.get("label"),
        "confidence": intent_result.get("confidence"),
        "opportunity_score": opportunity_result.get("score"),
        "opportunity_tier": opportunity_result.get("tier"),
        "answer": answer,
        "matches": matches,
        "recommendations": recommendations
    }


def get_ai_system_status():
    return {
        "status": "active",
        "service": "Cincinnati Lodge AI Service",
        "version": "9.2.0",
        "knowledge_items": len(build_knowledge_index()),
        "faq_items": len(build_faq_items()),
        "event_items": len(build_event_items()),
        "seo_page_items": len(build_seo_page_items()),
        "lodge_items": len(build_lodge_items()),
        "prediction_modes": [
            "intent_prediction",
            "opportunity_scoring",
            "knowledge_retrieval",
            "recommendation_prediction",
            "seo_priority_forecasting",
            "future_semantic_search",
            "future_supervised_learning",
            "future_deep_learning"
        ]
    }


# ============================================================
# END FILE — services/ai_service.py
# ============================================================