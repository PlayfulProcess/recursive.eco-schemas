#!/usr/bin/env python3
"""
Populate VBT-112 stub cards with full L2/L3 metadata, emergent patterns, and reflection questions.
Uses lookup tables keyed by practice_cluster and content keywords.
"""

import json
import re

INPUT = "grammars/vbt-112-gateways/grammar.json"
OUTPUT = INPUT  # overwrite in place

# ── L2/L3 defaults by practice_cluster ──────────────────────────────────────

CLUSTER_DEFAULTS = {
    "Breath Practices": {
        "L2": {"practice_domain": "breath_and_body", "experiential_quality": "stillness_in_movement", "relational_mode": "self_with_body"},
        "L3": {"wallis_cluster": "Breath Practices", "tillich_anxiety": "ontic", "tillich_courage": "as_part", "palmer_season": "winter", "playful_process_phase": "unity", "element": "vāyu_air", "chakra": "anāhata"},
        "upaya": "āṇavopāya",
    },
    "Kuṇḍalinī & Subtle Body": {
        "L2": {"practice_domain": "kundalini_subtle_body", "experiential_quality": "somatic_awakening", "relational_mode": "self_with_body"},
        "L3": {"wallis_cluster": "Kuṇḍalinī & Subtle Body", "tillich_anxiety": "ontic", "tillich_courage": "as_oneself", "palmer_season": "spring", "playful_process_phase": "differentiation", "element": "tejas_fire", "chakra": "mūlādhāra"},
        "upaya": "āṇavopāya",
    },
    "Esoteric Practices": {
        "L2": {"practice_domain": "esoteric_mantric", "experiential_quality": "threshold_awareness", "relational_mode": "self_with_source"},
        "L3": {"wallis_cluster": "Esoteric Practices", "tillich_anxiety": "spiritual", "tillich_courage": "as_oneself", "palmer_season": "winter", "playful_process_phase": "unity", "element": "ākāśa_space", "chakra": "ājñā"},
        "upaya": "śāktopāya",
    },
    "Emptiness Practices": {
        "L2": {"practice_domain": "emptiness_space", "experiential_quality": "void_spaciousness", "relational_mode": "self_with_void"},
        "L3": {"wallis_cluster": "Emptiness Practices", "tillich_anxiety": "spiritual", "tillich_courage": "absolute_faith", "palmer_season": "winter", "playful_process_phase": "return", "element": "ākāśa_space", "chakra": "sahasrāra"},
        "upaya": "śāmbhavopāya",
    },
    "Traditional Tantrik Yoga": {
        "L2": {"practice_domain": "tantrik_yoga", "experiential_quality": "expansion_dissolution", "relational_mode": "self_with_body"},
        "L3": {"wallis_cluster": "Traditional Tantrik Yoga", "tillich_anxiety": "ontic", "tillich_courage": "as_oneself", "palmer_season": "autumn", "playful_process_phase": "synthesis", "element": "tejas_fire", "chakra": "maṇipūra"},
        "upaya": "āṇavopāya",
    },
    "Bliss Practices": {
        "L2": {"practice_domain": "bliss_sensual", "experiential_quality": "sensory_immersion", "relational_mode": "self_with_world"},
        "L3": {"wallis_cluster": "Bliss Practices", "tillich_anxiety": "moral", "tillich_courage": "as_part", "palmer_season": "summer", "playful_process_phase": "unity", "element": "ap_water", "chakra": "svādhiṣṭhāna"},
        "upaya": "śāktopāya",
    },
    "Daily Life Practices": {
        "L2": {"practice_domain": "daily_life", "experiential_quality": "threshold_awareness", "relational_mode": "self_with_world"},
        "L3": {"wallis_cluster": "Daily Life Practices", "tillich_anxiety": "ontic", "tillich_courage": "as_part", "palmer_season": "autumn", "playful_process_phase": "synthesis", "element": "pṛthivī_earth", "chakra": "anāhata"},
        "upaya": "śāktopāya",
    },
    "Contemplative Practices": {
        "L2": {"practice_domain": "contemplative_philosophical", "experiential_quality": "cognitive_release", "relational_mode": "self_dissolving"},
        "L3": {"wallis_cluster": "Contemplative Practices", "tillich_anxiety": "spiritual", "tillich_courage": "absolute_faith", "palmer_season": "autumn", "playful_process_phase": "synthesis", "element": "ākāśa_space", "chakra": "ājñā"},
        "upaya": "śāmbhavopāya",
    },
    "Becoming One with Bhairava": {
        "L2": {"practice_domain": "contemplative_philosophical", "experiential_quality": "unity_recognition", "relational_mode": "self_dissolving"},
        "L3": {"wallis_cluster": "Becoming One with Bhairava", "tillich_anxiety": "spiritual", "tillich_courage": "absolute_faith", "palmer_season": "winter", "playful_process_phase": "return", "element": "ākāśa_space", "chakra": "sahasrāra"},
        "upaya": "anupāya",
    },
    "Final Practices": {
        "L2": {"practice_domain": "contemplative_philosophical", "experiential_quality": "unity_recognition", "relational_mode": "self_dissolving"},
        "L3": {"wallis_cluster": "Final Practices", "tillich_anxiety": "spiritual", "tillich_courage": "absolute_faith", "palmer_season": "winter", "playful_process_phase": "return", "element": "ākāśa_space", "chakra": "sahasrāra"},
        "upaya": "anupāya",
    },
    "Concluding Teachings": {
        "L2": {"practice_domain": "concluding_reinterpretation", "experiential_quality": "unity_recognition", "relational_mode": "self_dissolving"},
        "L3": {"wallis_cluster": "Concluding Teachings", "tillich_anxiety": "spiritual", "tillich_courage": "absolute_faith", "palmer_season": "winter", "playful_process_phase": "return", "element": "ākāśa_space", "chakra": "sahasrāra"},
        "upaya": "anupāya",
    },
    "Yogic Practices: Bindu, Nāda, Uccāra": {
        "L2": {"practice_domain": "esoteric_mantric", "experiential_quality": "somatic_awakening", "relational_mode": "self_with_body"},
        "L3": {"wallis_cluster": "Yogic Practices: Bindu, Nāda, Uccāra", "tillich_anxiety": "ontic", "tillich_courage": "as_oneself", "palmer_season": "spring", "playful_process_phase": "differentiation", "element": "ākāśa_space", "chakra": "viśuddha"},
        "upaya": "āṇavopāya",
    },
}

# ── Keyword-based overrides for experiential_quality ───────────────────────

def refine_experiential_quality(summary):
    """Refine experiential_quality based on practice content keywords."""
    s = summary.lower()
    if any(w in s for w in ["void", "empty", "nothing", "space", "spacious"]):
        return "void_spaciousness"
    if any(w in s for w in ["bliss", "joy", "pleasure", "delight", "happiness", "rapture"]):
        return "sensory_immersion"
    if any(w in s for w in ["dissolv", "inciner", "burn", "fire", "melt"]):
        return "expansion_dissolution"
    if any(w in s for w in ["sleep", "dream", "liminal", "threshold", "between", "edge", "sneeze", "anger", "wonder"]):
        return "threshold_awareness"
    if any(w in s for w in ["still", "unmoving", "tranquil", "peace", "calm", "serene"]):
        return "stillness_in_movement"
    if any(w in s for w in ["devot", "surrender", "prayer", "worship"]):
        return "devotional_surrender"
    if any(w in s for w in ["body", "skin", "tissue", "breath", "needle", "armpit", "tongue"]):
        return "somatic_awakening"
    if any(w in s for w in ["contempl", "cognit", "mind", "thought", "i am", "conscious", "aware"]):
        return "cognitive_release"
    if any(w in s for w in ["everywhere", "all-pervas", "omniscient", "one", "unity", "same in all"]):
        return "unity_recognition"
    return None

def refine_relational_mode(summary):
    s = summary.lower()
    if any(w in s for w in ["other", "friend", "foe", "partner", "beloved", "another's body"]):
        return "self_with_other"
    if any(w in s for w in ["everywhere", "universe", "world", "all bodies", "all beings"]):
        return "self_with_world"
    if any(w in s for w in ["void", "empty", "nothing", "spaceless"]):
        return "self_with_void"
    if any(w in s for w in ["dissolv", "no bondage", "no mental", "waveless", "supportless"]):
        return "self_dissolving"
    if any(w in s for w in ["body", "skin", "breath", "arm", "tongue", "eye", "ear", "needle"]):
        return "self_with_body"
    if any(w in s for w in ["bhairav", "śiva", "god", "divine", "lord", "supreme"]):
        return "self_with_source"
    return None

def refine_element(summary):
    s = summary.lower()
    if any(w in s for w in ["fire", "inciner", "burn", "flame", "lightning"]):
        return "tejas_fire"
    if any(w in s for w in ["water", "ocean", "wave", "flood", "nectar"]):
        return "ap_water"
    if any(w in s for w in ["breath", "air", "wind", "prāṇa"]):
        return "vāyu_air"
    if any(w in s for w in ["space", "sky", "void", "empty", "ākāśa"]):
        return "ākāśa_space"
    if any(w in s for w in ["body", "ground", "earth", "seat", "needle", "well"]):
        return "pṛthivī_earth"
    return None

def refine_chakra(summary):
    s = summary.lower()
    if any(w in s for w in ["crown", "dvādaśānta", "upper limit", "above the head"]):
        return "dvādaśānta"
    if any(w in s for w in ["heart", "lotus", "anāhata", "center"]):
        return "anāhata"
    if any(w in s for w in ["root", "mūlādhāra", "base", "lower gate"]):
        return "mūlādhāra"
    if any(w in s for w in ["throat", "viśuddha", "sound", "phoneme", "visarga", "vowel"]):
        return "viśuddha"
    if any(w in s for w in ["eye", "gaze", "ājñā", "brow", "third eye"]):
        return "ājñā"
    if any(w in s for w in ["navel", "maṇipūra", "fire", "belly"]):
        return "maṇipūra"
    if any(w in s for w in ["sexual", "genital", "svādhiṣṭhāna", "pleasure"]):
        return "svādhiṣṭhāna"
    return None

def refine_palmer(summary):
    s = summary.lower()
    if any(w in s for w in ["void", "dark", "empty", "nothing", "formless", "dissolv"]):
        return "winter"
    if any(w in s for w in ["ris", "awaken", "dawn", "lightning", "spring", "emerge"]):
        return "spring"
    if any(w in s for w in ["bliss", "joy", "full", "delight", "rapture", "music", "food"]):
        return "summer"
    if any(w in s for w in ["release", "let go", "integrat", "daily", "life", "sleep", "ordinary"]):
        return "autumn"
    return None

# ── Emergent patterns by content keywords ─────────────────────────────────

CROSS_TRADITION_MAP = {
    "void": "Buddhist śūnyatā, Meister Eckhart's Gelassenheit, Daoist wu",
    "empty": "Buddhist śūnyatā, Apophatic theology, Daoist emptiness",
    "space": "Dzogchen sky-gazing, Sufi fana, Christian cloud of unknowing",
    "breath": "Zen breath counting, Hesychast prayer of the heart, pranayama",
    "fire": "Zoroastrian sacred fire, Kabbalistic pillar of severity, Kundalini yoga",
    "joy": "Sufi ecstatic states, Hasidic simcha, Teresa of Ávila's interior castle",
    "bliss": "Vedantic ānanda, Sufi wajd, Tantric mahāsukha",
    "music": "Sufi samā, Nāda yoga, Hildegard of Bingen's symphonia",
    "sleep": "Yoga nidra, Tibetan dream yoga, Taoist sleeping meditation",
    "darkness": "St. John of the Cross's dark night, Kabbalistic tzimtzum, Tibetan dark retreat",
    "desire": "Sufi longing (shawq), Bhakti viraha, Rumi's reed flute",
    "sky": "Dzogchen sky-gazing (khorde rushen), Sufi mushāhada, natural awareness traditions",
    "body": "Vipassana body scanning, Feldenkrais awareness, somatic experiencing",
    "mind": "Zen shikantaza, Dzogchen rigpa, Advaita self-inquiry",
    "love": "Bhakti yoga, Sufi ishq, Christian agape, Tantric union",
    "anger": "Tibetan tonglen, NVC empathy practice, Stoic premeditatio",
    "gaze": "Zen wall-gazing, Sufi tawajjuh, Hindu trataka",
    "whirl": "Sufi whirling (sema), ecstatic dance traditions, shamanic spinning",
    "sound": "Nāda yoga, Gregorian chant, Aboriginal didgeridoo meditation",
    "needle": "Acupuncture awareness, focusing on pain in Zen, somatic experiencing",
    "ocean": "Sufi drop-in-ocean, Vedantic wave-and-ocean, Rumi's sea metaphors",
    "magic": "Buddhist māyā, Hindu līlā, Plato's cave allegory",
    "dream": "Tibetan dream yoga, Aboriginal dreamtime, Jungian active imagination",
    "food": "Zen oryoki, mindful eating, Eucharistic presence",
    "well": "Sufi heart as well, Celtic holy wells, looking into depths traditions",
}

POLARITY_MAP = {
    "void": "fullness/emptiness, being/nonbeing",
    "fire": "creation/destruction, purification/dissolution",
    "space": "bounded/unbounded, container/contained",
    "body": "form/formless, dense/subtle",
    "breath": "inhalation/exhalation, expansion/contraction",
    "joy": "pleasure/pain, attachment/freedom",
    "bliss": "desire/fulfillment, seeking/finding",
    "sleep": "waking/sleeping, consciousness/unconsciousness",
    "dark": "light/darkness, known/unknown",
    "desire": "grasping/releasing, wanting/having",
    "mind": "thought/silence, knowing/unknowing",
    "sky": "earth/sky, finite/infinite",
    "gaze": "seeing/being, subject/object",
    "sound": "sound/silence, vibration/stillness",
    "love": "union/separation, self/other",
    "anger": "contraction/expansion, reaction/response",
    "ocean": "wave/ocean, particular/universal",
}

SOMATIC_MAP = {
    "crown": "crown of head, dvādaśānta",
    "heart": "heart center, chest cavity",
    "root": "pelvic floor, base of spine",
    "breath": "nostrils, lungs, diaphragm",
    "eye": "eyes, visual field, brow center",
    "body": "whole body awareness",
    "skin": "skin surface, boundary awareness",
    "tongue": "palate, throat, oral cavity",
    "arm": "armpits, upper body hollows",
    "ear": "ears, auditory field",
    "belly": "navel, solar plexus",
    "well": "vertigo center, vestibular system",
    "needle": "point of contact, acute sensation",
    "swing": "vestibular system, inner ear",
    "whirl": "whole body, vestibular system, proprioception",
}

PSYCH_MAP = {
    "void": "Encountering the groundlessness that underlies all constructed identity",
    "empty": "The freedom that comes when concepts about self are seen through",
    "fire": "Transformation through the burning away of what no longer serves",
    "joy": "The capacity for pleasure as a doorway to presence",
    "bliss": "Allowing embodied delight without the need to grasp or repeat it",
    "sleep": "The wisdom available at the edges of consciousness",
    "dark": "Meeting the unknown without the compulsion to illuminate it",
    "desire": "Seeing wanting itself as a form of creative energy",
    "mind": "The discovery that awareness is not produced by thought",
    "sky": "The spaciousness that contains everything without being diminished",
    "body": "Trusting the body's intelligence beyond conceptual understanding",
    "love": "The recognition that connection is more fundamental than separation",
    "anger": "Strong emotion as a gateway rather than an obstacle",
    "gaze": "Pure perception before the mind adds interpretation",
    "sound": "Vibration as the bridge between form and formlessness",
    "food": "Nourishment as a practice of presence and gratitude",
    "magic": "The constructed nature of what we take to be real",
    "ocean": "Individual identity as a temporary pattern in infinite consciousness",
    "well": "The vertigo of looking into depths as a doorway to freedom from support",
    "dream": "The creative power that constructs experience in all states",
    "whirl": "Surrender of control as a path to clarity",
    "needle": "Acute sensation as a concentrative anchor",
}

# ── Reflection questions by theme ─────────────────────────────────────────

REFLECTION_QUESTIONS = {
    "void": "What remains when you stop filling the silence?",
    "empty": "Can you rest in not-knowing without reaching for an answer?",
    "space": "Where do you feel most spacious in your life right now?",
    "fire": "What in you is ready to be burned away?",
    "breath": "What happens when you simply follow the breath without trying to change it?",
    "joy": "When did you last allow joy to simply be, without needing to understand it?",
    "bliss": "Can you let pleasure teach you something about your true nature?",
    "sleep": "What wisdom arrives at the threshold between waking and sleeping?",
    "dark": "What are you willing to sit with in total darkness?",
    "desire": "What if your wanting is not a problem but a doorway?",
    "mind": "Who are you when thought pauses?",
    "sky": "What would it feel like to have no edges?",
    "body": "Where in your body does awareness feel most alive right now?",
    "gaze": "What happens when you look without naming?",
    "love": "Whose consciousness feels closest to your own?",
    "anger": "What is the stillness at the center of your strongest feeling?",
    "sound": "What do you hear when the last note fades?",
    "food": "When did nourishment last surprise you with presence?",
    "magic": "How real is the world you are constructing right now?",
    "ocean": "Are you the wave, or are you the water?",
    "well": "What happens when you look into a depth you cannot measure?",
    "dream": "What is dreaming you right now?",
    "whirl": "What becomes clear when you stop trying to hold still?",
    "needle": "Where does attention go when sensation becomes acute?",
    "devot": "What are you devoted to without knowing why?",
    "music": "What sound could you dissolve into completely?",
    "bondage": "What would freedom feel like if it were already here?",
    "i am": "What does 'I' point to when you follow it all the way?",
    "everywhere": "What if you were already everywhere you needed to be?",
    "conscious": "Is awareness something you have, or something you are?",
    "omniscient": "What if you already possessed every quality of the divine?",
    "equal": "What changes when you see friend and stranger as the same?",
    "hatred": "What lives in the center between craving and aversion?",
    "purity": "What freedom arrives when you drop the categories of pure and impure?",
}


def find_keyword_match(summary, mapping):
    """Find the first matching keyword from a mapping dict."""
    s = summary.lower()
    for keyword, value in mapping.items():
        if keyword in s:
            return value
    return None


def populate_stub(card):
    """Populate a stub card with full L2/L3 metadata."""
    cluster = card.get("practice_cluster", "")
    summary = card.get("practice_summary_en", "")
    name = card.get("name_en", "")

    defaults = CLUSTER_DEFAULTS.get(cluster, CLUSTER_DEFAULTS["Daily Life Practices"])

    # Set upaya
    if "upaya" not in card or not card["upaya"]:
        card["upaya"] = defaults["upaya"]

    # Build L2 with refinements
    l2 = dict(defaults["L2"])
    eq = refine_experiential_quality(summary)
    if eq:
        l2["experiential_quality"] = eq
    rm = refine_relational_mode(summary)
    if rm:
        l2["relational_mode"] = rm
    card["L2"] = l2

    # Build L3 with refinements
    l3 = dict(defaults["L3"])
    el = refine_element(summary)
    if el:
        l3["element"] = el
    ch = refine_chakra(summary)
    if ch:
        l3["chakra"] = ch
    ps = refine_palmer(summary)
    if ps:
        l3["palmer_season"] = ps
    card["L3"] = l3

    # Emergent patterns
    cross = find_keyword_match(summary + " " + name, CROSS_TRADITION_MAP)
    polarity = find_keyword_match(summary + " " + name, POLARITY_MAP)
    somatic = find_keyword_match(summary + " " + name, SOMATIC_MAP)
    psych = find_keyword_match(summary + " " + name, PSYCH_MAP)

    card["emergent_patterns"] = {
        "polarity": polarity or "form/formless, technique/spontaneity",
        "cross_tradition": cross or "Contemplative traditions worldwide recognize this gateway",
        "somatic_locus": somatic or "whole body awareness",
        "psychological_resonance": psych or "The recognition that awareness itself is the ultimate refuge",
    }

    # Reflection question
    question = find_keyword_match(summary + " " + name, REFLECTION_QUESTIONS)
    card["reflection_question"] = question or "What opens in you when you practice this gateway?"

    # Ensure empty fields exist
    for field in ["sanskrit_transliteration", "sanskrit_devanagari", "translation_pt", "practice_summary_pt", "name_pt"]:
        if field not in card:
            card[field] = ""

    # Image filename
    num = card.get("yukti_number", 0)
    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    card["image_filename"] = f"yukti-{num:03d}-{slug}.png"

    return card


def main():
    with open(INPUT, 'r') as f:
        data = json.load(f)

    cards = data.get("yukti_cards", data.get("cards", []))

    # The stubs might be at the top level in different keys
    # Check the structure
    if "yukti_cards" in data:
        key = "yukti_cards"
    elif "cards" in data:
        key = "cards"
    else:
        # Cards might be mixed in at top level
        print("Could not find cards array, checking structure...")
        print(list(data.keys()))
        return

    populated = 0
    for card in data[key]:
        cid = card.get("id", "")
        # Skip structural cards, template, and already-populated cards
        if cid.startswith("S-") or cid == "TEMPLATE":
            continue
        if "L2" in card and card["L2"]:
            # Already populated
            continue
        populate_stub(card)
        populated += 1

    # Remove TEMPLATE card
    data[key] = [c for c in data[key] if c.get("id") != "TEMPLATE"]

    with open(OUTPUT, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Populated {populated} stub cards")
    print(f"Total cards: {len(data[key])}")
    print(f"Written to {OUTPUT}")


if __name__ == "__main__":
    main()
