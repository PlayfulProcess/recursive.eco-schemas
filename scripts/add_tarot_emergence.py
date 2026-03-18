#!/usr/bin/env python3
"""
Add L2 and L3 emergence items to the Tarot of All Tarots grammar.

L2 groups:
  - Major Arcana (22 cards)
  - Wands suit (14 cards)
  - Cups suit (14 cards)
  - Swords suit (14 cards)
  - Pentacles suit (14 cards)
  - The Fool's Journey: First Half (cards 0-10)
  - The Fool's Journey: Second Half (cards 11-21)
  - Pip cards (Ace-Ten across all suits)
  - Court cards (Page-King across all suits)

L3 meta-categories:
  - The Major Arcana (L2 groups: major, fool's journey halves)
  - The Minor Arcana (L2 groups: 4 suits, pips, courts)
"""

import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAMMAR_PATH = os.path.join(BASE, "grammars", "tarot-of-all-tarots", "grammar.json")

with open(GRAMMAR_PATH) as f:
    grammar = json.load(f)

items = grammar["items"]
sort_order = max(i["sort_order"] for i in items) + 1

# Index L1 IDs
major_ids = [i["id"] for i in items if i["metadata"]["arcana"] == "major"]
wands_ids = [i["id"] for i in items if i["metadata"].get("suit") == "wands"]
cups_ids = [i["id"] for i in items if i["metadata"].get("suit") == "cups"]
swords_ids = [i["id"] for i in items if i["metadata"].get("suit") == "swords"]
pentacles_ids = [i["id"] for i in items if i["metadata"].get("suit") == "pentacles"]
fools_first = [i["id"] for i in items if i["metadata"]["arcana"] == "major" and i["metadata"]["number"] <= 10]
fools_second = [i["id"] for i in items if i["metadata"]["arcana"] == "major" and i["metadata"]["number"] >= 11]
pip_ids = [i["id"] for i in items if i["metadata"]["arcana"] == "minor" and i["metadata"]["number"] <= 10]
court_ids = [i["id"] for i in items if i["metadata"]["arcana"] == "minor" and i["metadata"]["number"] >= 11]

# ─── L2 items ────────────────────────────────────────────────────────────────

l2_items = []

l2_items.append({
    "id": "major-arcana",
    "name": "The Major Arcana",
    "sort_order": sort_order,
    "category": "arcana-group",
    "level": 2,
    "composite_of": major_ids,
    "relationship_type": "emergence",
    "sections": {
        "About": "The 22 trumps of the tarot — from The Fool (0) to The World (21). These are the archetypes: the deep patterns of human experience that recur across cultures and centuries. In the Fool's Journey reading, these 22 cards map the soul's path from innocent departure through initiation, descent, and return to wholeness.",
        "How to Use": "Draw from the Major Arcana alone when you need big-picture guidance. These cards don't answer 'what should I do about Tuesday's meeting?' — they answer 'what is the deep pattern operating in my life right now?' Each card is a teacher. Sit with it. Let it speak."
    },
    "keywords": ["archetypes", "soul journey", "major themes"],
    "metadata": {}
})
sort_order += 1

l2_items.append({
    "id": "fools-journey-first-half",
    "name": "The Fool's Journey: Outer World (0–10)",
    "sort_order": sort_order,
    "category": "arcana-group",
    "level": 2,
    "composite_of": fools_first,
    "relationship_type": "emergence",
    "sections": {
        "About": "Cards 0 through 10 trace the Fool's encounter with the outer world — the teachers, institutions, and forces that shape conscious identity. From the Magician's focused will through the Hierophant's tradition to the Wheel of Fortune's reminder that no external arrangement is permanent. This is the journey of building an ego strong enough to survive what comes next.",
        "How to Use": "When these cards dominate a reading, the question concerns your relationship to external structures: career, authority, relationships, institutions. The first half asks: how are you meeting the world? What are you building? What forces are you learning to navigate?"
    },
    "keywords": ["outer journey", "ego formation", "worldly lessons"],
    "metadata": {}
})
sort_order += 1

l2_items.append({
    "id": "fools-journey-second-half",
    "name": "The Fool's Journey: Inner World (11–21)",
    "sort_order": sort_order,
    "category": "arcana-group",
    "level": 2,
    "composite_of": fools_second,
    "relationship_type": "emergence",
    "sections": {
        "About": "Cards 11 through 21 trace the Fool's descent into the inner world — the reckoning with shadow, the dissolution of false structures, and the return to wholeness. From Justice's accountability through Death's transformation and the Tower's destruction to the World's integration. This is the journey of the soul finding itself by losing everything it thought it was.",
        "How to Use": "When these cards dominate a reading, the question concerns your inner transformation: identity, shadow work, spiritual crisis, and integration. The second half asks: what is dying in you? What is being born? What must you face that you've been avoiding?"
    },
    "keywords": ["inner journey", "shadow work", "transformation", "integration"],
    "metadata": {}
})
sort_order += 1

SUIT_BRIEF = {
    "wands": "passion, creativity, ambition, purpose — the things that ignite you",
    "cups": "emotions, relationships, intuition, dreams — the things that move you",
    "swords": "thoughts, communication, conflict, truth — the things that cut through",
    "pentacles": "money, health, work, home — the things that ground you",
}

for suit_key, suit_name, suit_ids, element, desc in [
    ("wands", "Wands", wands_ids, "Fire",
     "The suit of Fire — will, passion, creativity, and the drive to make things happen. Wands trace the arc of creative energy from its first spark (Ace) through its full expression (Ten), and from the eager Page through the commanding King. In readings, Wands answer questions about purpose, ambition, and the things that light you up."),
    ("cups", "Cups", cups_ids, "Water",
     "The suit of Water — emotion, intuition, love, and the currents of the unconscious. Cups trace the arc of emotional experience from the first offering of love (Ace) through the weight of fulfilled dreams (Ten), and from the dreamy Page through the compassionate King. In readings, Cups answer questions about feelings, relationships, and the life of the heart."),
    ("swords", "Swords", swords_ids, "Air",
     "The suit of Air — intellect, truth, conflict, and the power of the mind. Swords trace the arc of mental experience from the first flash of insight (Ace) through the final reckoning (Ten), and from the curious Page through the authoritative King. In readings, Swords answer questions about communication, decisions, and the truths you need to face."),
    ("pentacles", "Pentacles", pentacles_ids, "Earth",
     "The suit of Earth — material reality, the body, craft, and the slow work of building something that lasts. Pentacles trace the arc of manifestation from the first seed of abundance (Ace) through the completed legacy (Ten), and from the studious Page through the prosperous King. In readings, Pentacles answer questions about money, health, work, and the physical world."),
]:
    l2_items.append({
        "id": f"suit-{suit_key}",
        "name": f"The Suit of {suit_name}",
        "sort_order": sort_order,
        "category": "suit-group",
        "level": 2,
        "composite_of": suit_ids,
        "relationship_type": "emergence",
        "sections": {
            "About": desc,
            "How to Use": f"When {suit_name} dominate a reading, the question lives in the {element} element: {SUIT_BRIEF[suit_key]}. Read the number for the stage of the journey and the court rank for the maturity of the energy."
        },
        "keywords": [suit_key, element.lower(), "minor arcana"],
        "metadata": {"element": element}
    })
    sort_order += 1

l2_items.append({
    "id": "pip-cards",
    "name": "The Pip Cards (Ace through Ten)",
    "sort_order": sort_order,
    "category": "structural-group",
    "level": 2,
    "composite_of": pip_ids,
    "relationship_type": "emergence",
    "sections": {
        "About": "The 40 numbered cards — Ace through Ten in each of the four suits. These trace the universal arc of any endeavor: seed (Ace), duality (Two), creation (Three), stability (Four), disruption (Five), harmony (Six), reflection (Seven), mastery (Eight), culmination (Nine), completion (Ten). The same journey in Fire, Water, Air, and Earth.",
        "How to Use": "Read the number first, then the suit. The number tells you WHERE you are in the cycle; the suit tells you WHICH domain of life is active. A Five of Cups and a Five of Swords are both disruptions — but one disrupts feeling, the other disrupts thought."
    },
    "keywords": ["pips", "numbered cards", "cycle", "journey"],
    "metadata": {}
})
sort_order += 1

l2_items.append({
    "id": "court-cards",
    "name": "The Court Cards (Page through King)",
    "sort_order": sort_order,
    "category": "structural-group",
    "level": 2,
    "composite_of": court_ids,
    "relationship_type": "emergence",
    "sections": {
        "About": "The 16 court cards — Page, Knight, Queen, and King in each suit. These represent people in your life, aspects of yourself, or energies you're being asked to embody. Pages are students and messengers. Knights are questers and extremists. Queens hold inward mastery. Kings wield outward authority. Each expresses their element at a different level of maturity.",
        "How to Use": "When a court card appears, ask three questions: (1) Is this a person in my life? (2) Is this an aspect of myself? (3) Is this an energy I need to cultivate? Often the answer is all three. The suit tells you the domain; the rank tells you the maturity."
    },
    "keywords": ["court cards", "people", "personality", "maturity"],
    "metadata": {}
})
sort_order += 1

# ─── L3 meta-categories ──────────────────────────────────────────────────────

l3_major_composites = ["major-arcana", "fools-journey-first-half", "fools-journey-second-half"]
l3_minor_composites = ["suit-wands", "suit-cups", "suit-swords", "suit-pentacles", "pip-cards", "court-cards"]

l2_items.append({
    "id": "meta-major-arcana",
    "name": "The Archetypal Journey",
    "sort_order": sort_order,
    "category": "meta",
    "level": 3,
    "composite_of": l3_major_composites,
    "relationship_type": "emergence",
    "sections": {
        "About": "The Major Arcana as a complete initiatory path — 22 stations from innocence to integration. Viewed across five centuries of decks, the same archetypes appear in every tradition: the Fool begins, the Magician channels, the Priestess receives, and twenty cards later the World dances. The names change (Marseille's Le Mat, Sola Busca's Mato, Etteilla's Le Chaos) but the pattern endures.",
        "How to Use": "Use this meta-category to explore the Major Arcana as a story rather than isolated symbols. The Fool's Journey is the tarot's hidden narrative — each card makes deeper sense in the context of what comes before and after."
    },
    "keywords": ["fool's journey", "archetypes", "initiation", "meta"],
    "metadata": {}
})
sort_order += 1

l2_items.append({
    "id": "meta-minor-arcana",
    "name": "The Four Elements in Practice",
    "sort_order": sort_order,
    "category": "meta",
    "level": 3,
    "composite_of": l3_minor_composites,
    "relationship_type": "emergence",
    "sections": {
        "About": "The Minor Arcana as a map of daily life through the four elements. Fire (Wands) for will and creativity. Water (Cups) for emotion and intuition. Air (Swords) for intellect and truth. Earth (Pentacles) for body and material world. Together they cover the full spectrum of human experience — not as archetypes but as the practical, lived reality those archetypes manifest through.",
        "How to Use": "Use this meta-category to understand the Minor Arcana as a system. The four suits are four lenses on the same experience. When you draw a Minor card, you're being told not just what energy is present but which element of your life needs attention."
    },
    "keywords": ["four elements", "daily life", "practice", "meta"],
    "metadata": {}
})
sort_order += 1

# Add all L2/L3 items to grammar
grammar["items"].extend(l2_items)

with open(GRAMMAR_PATH, "w") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)

l2_count = sum(1 for i in l2_items if i["level"] == 2)
l3_count = sum(1 for i in l2_items if i["level"] == 3)
print(f"Added {l2_count} L2 items and {l3_count} L3 items")
print(f"Total items: {len(grammar['items'])}")
print(f"File size: {os.path.getsize(GRAMMAR_PATH) / 1024:.0f} KB")
