# -*- coding: utf-8 -*-
"""Generate grammars/cary-yale-visconti-tarot/grammar.json.

The Cary-Yale (Visconti di Modrone) Tarot, Milan c. 1442, Bonifacio Bembo workshop
— the most lavish and most unusual of the surviving hand-painted decks. It is built
ONLY from the cards that survive (the Beinecke holds 67), because the deck is famous
precisely for its idiosyncratic, fragmentary survival:

  * SIX courts per suit, half of them female: King, Queen, Knight (male rider),
    Horsewoman (female rider), Knave (male page), Damsel (female page). The
    "Damsel of Swords" is the card that opened this whole project.
  * Three extra THEOLOGICAL VIRTUES — Faith, Hope, Charity — added to the usual
    cardinal virtues, found in no other tarot.
  * Only a handful of trumps survive.

Historical / iconographic grammar. Images: Wikimedia Commons,
Category:Cary-Yale Visconti Tarot (public domain). Filenames embedded verbatim.
"""
import json
import os
import urllib.parse

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "grammars", "cary-yale-visconti-tarot")
COMMONS = "https://commons.wikimedia.org/wiki/Special:FilePath/"


def img(filename):
    return COMMONS + urllib.parse.quote(filename)


TRADITION_NOTE = (
    "These cards were made to play a game — the Italian *trionfi* / *tarocchi* "
    "card game — not for divination, which arrived centuries later. The notes here "
    "are historical and iconographic; any reading is a modern interpretive overlay, "
    "not part of the deck's original use."
)


# ---- Surviving trumps & virtues (hand-authored) ----------------------------
# (id, name, italian, filename, iconography, history, reading)
TRUMPS = [
    ("trump-emperor", "The Emperor", "L'Imperatore", "Cary-Yale Tarot deck - The Emperor.jpg",
     "An enthroned, bearded emperor in gold brocade holding an orb, the imperial eagle on display, "
     "attendants at his feet.",
     "One of the few trumps to survive in this deck. The Cary-Yale was likely made for the 1441 "
     "marriage of Bianca Maria Visconti and Francesco Sforza; its emperor is dynastic propaganda in gold.",
     "Temporal authority and the architecture of rule — the masculine throne the whole procession serves."),
    ("trump-empress", "The Empress", "L'Imperatrice", "Cary-Yale Tarot deck - The Empress.jpg",
     "A crowned empress enthroned in brocade, bearing a shield and sceptre, ladies in attendance.",
     "A surviving trump. The Cary-Yale's courtly women are rendered with unusual individuality — part of "
     "the deck's preoccupation with the feminine that also produced its female knights and pages.",
     "Sovereign abundance, the generative authority that rules from the throne."),
    ("trump-lovers", "The Lovers", "L'Amore", "Cary-Yale Tarot deck - The Lovers.jpg",
     "A couple beneath a draped pavilion clasp hands while a blindfolded Cupid hovers above on a column; "
     "a dog and attendants frame the scene.",
     "Among the most celebrated surviving Cary-Yale cards — very probably a portrait of the Visconti-Sforza "
     "wedding the deck was made to honour.",
     "Union as alliance, love bound to lineage — desire formalised into a marriage of houses."),
    ("trump-chariot", "The Chariot", "Il Carro", "Cary-Yale Tarot deck - Chariot.jpg",
     "A crowned noblewoman rides a canopied triumphal car drawn by two white horses, attendants walking "
     "alongside.",
     "The card that names the game (trionfo / triumph). The Cary-Yale chariot is driven by a woman, in "
     "keeping with the deck's foregrounding of female figures.",
     "Triumph and momentum — the self borne forward in a victory parade over what it has mastered."),
    ("trump-strength", "Strength", "La Fortezza", "Cary-Yale Tarot deck - Strength.jpg",
     "A figure in courtly dress overpowers a lion, wrenching open or subduing its jaws — the Herculean "
     "image of fortitude.",
     "A surviving cardinal virtue. In the Cary-Yale the cardinal virtues sit alongside the rare theological "
     "virtues (Faith, Hope, Charity) — an unusually complete moral programme.",
     "Fortitude — strength of soul that masters the beast through steady will rather than rage."),
    ("trump-death", "Death", "La Morte", "Cary-Yale Tarot deck - Death.jpg",
     "A mounted or standing skeletal figure with a great bow, riding across the gold over fallen bodies.",
     "A surviving trump, here given the dignity of full gold-ground treatment — Death as a noble rider, "
     "not a grotesque.",
     "The great leveller — the end that rides through every estate without exception."),
    ("trump-judgement", "Judgement", "Il Giudizio", "Cary-Yale Tarot deck - Judgement.jpg",
     "Trumpeting angels above; below, the dead rise from their tombs at the summons, hands lifted.",
     "A surviving trump. The Last Judgement is the most overtly Christian of the triumphs and a natural "
     "companion to the deck's theological virtues.",
     "The call and the reckoning — awakening, summons, the dead rising to answer."),
    ("trump-world", "The World", "Il Mondo", "Cary-Yale Tarot deck - World.jpg",
     "A crowned figure (Fame, or a lady) presides above a landscape with a walled city, knights, and ship "
     "— the world spread out to be surveyed and won.",
     "The highest triumph. The Cary-Yale's World is more a panorama of earthly glory than the later cosmic "
     "wreath — fitting for a dynastic deck.",
     "Completion and dominion — the whole world held up to be seen and possessed."),
    # The three theological virtues — unique to the Cary-Yale
    ("virtue-faith", "Faith", "La Fede", "Cary-Yale Tarot deck - Faith.jpg",
     "A woman holds a chalice and cross, sometimes with a kneeling figure — the personification of Faith "
     "(Fides).",
     "One of the three THEOLOGICAL virtues found in no other tarot. Their presence suggests the Cary-Yale "
     "was conceived as a complete moral cosmos — the four cardinal plus the three theological virtues.",
     "Faith — trust that orients the soul beyond what it can prove, the first of the theological virtues."),
    ("virtue-hope", "Hope", "La Speranza", "Cary-Yale Tarot deck - Hope.jpg",
     "A woman gazes upward with hands clasped in prayer, often with an anchor — the personification of Hope "
     "(Spes).",
     "A theological virtue unique to this deck. The anchor is Hope's ancient attribute; here it joins the "
     "tarot for the only time in its history.",
     "Hope — the upward reach that endures through the dark, the anchor of the soul."),
    ("virtue-charity", "Charity", "La Carità", "Cary-Yale Tarot deck - Charity.jpg",
     "A woman nurses or tends children, sometimes with a flame — the personification of Charity (Caritas), "
     "greatest of the three.",
     "The third and greatest theological virtue, unique to the Cary-Yale. Charity nursing children is the "
     "classic Caritas image carried over from devotional painting.",
     "Charity — love that gives itself away, named by tradition the greatest of the virtues."),
]

# ---- Surviving pips & courts: parsed from the real Commons file list --------
# Only canonical "Cary-Yale Tarot deck - <Rank> of <Suit>.jpg" files are used.
CARY_FILES = [
    "Cary-Yale Tarot deck - Ace of Arrows.jpg", "Cary-Yale Tarot deck - Ace of Coins.jpg",
    "Cary-Yale Tarot deck - Ace of Cups.jpg", "Cary-Yale Tarot deck - Ace of Spades.jpg",
    "Cary-Yale Tarot deck - Two of Arrows.jpg", "Cary-Yale Tarot deck - Two of Coins.jpg",
    "Cary-Yale Tarot deck - Two of Cups.jpg", "Cary-Yale Tarot deck - Two of Spades.jpg",
    "Cary-Yale Tarot deck - Three of Arrows.jpg", "Cary-Yale Tarot deck - Three of Cups.jpg",
    "Cary-Yale Tarot deck - Three of Spades.jpg", "Cary-Yale Tarot deck - Four of Arrows.jpg",
    "Cary-Yale Tarot deck - Four of Coins.jpg", "Cary-Yale Tarot deck - Four of Cups.jpg",
    "Cary-Yale Tarot deck - Four of Spades.jpg", "Cary-Yale Tarot deck - Five of Arrows.jpg",
    "Cary-Yale Tarot deck - Five of Coins.jpg", "Cary-Yale Tarot deck - Five of Cups.jpg",
    "Cary-Yale Tarot deck - Five of Spades.jpg", "Cary-Yale Tarot deck - Six of Arrows.jpg",
    "Cary-Yale Tarot deck - Six of Coins.jpg", "Cary-Yale Tarot deck - Six of Cups.jpg",
    "Cary-Yale Tarot deck - Six of Swords.jpg", "Cary-Yale Tarot deck - Seven of Arrows.jpg",
    "Cary-Yale Tarot deck - Seven of Coins.jpg", "Cary-Yale Tarot deck - Seven of Cups.jpg",
    "Cary-Yale Tarot deck - Seven of Swords.jpg", "Cary-Yale Tarot deck - Eight of Arrows.jpg",
    "Cary-Yale Tarot deck - Eight of Coins.jpg", "Cary-Yale Tarot deck - Eight of Cups.jpg",
    "Cary-Yale Tarot deck - Eight of Swords.jpg", "Cary-Yale Tarot deck - Nine of Arrows.jpg",
    "Cary-Yale Tarot deck - Nine of Coins.jpg", "Cary-Yale Tarot deck - Nine of Cups.jpg",
    "Cary-Yale Tarot deck - Nine of Spades.jpg", "Cary-Yale Tarot deck - Ten of Arrows.jpg",
    "Cary-Yale Tarot deck - Ten of Coins.jpg", "Cary-Yale Tarot deck - Ten of Cups.jpg",
    "Cary-Yale Tarot deck - Ten of Sword.jpg",
    # courts (six per suit, where they survive)
    "Cary-Yale Tarot deck - Knave of Cups.jpg", "Cary-Yale Tarot deck - Knave of Staves.jpg",
    "Cary-Yale Tarot deck - Horsewoman of Coins.jpg", "Cary-Yale Tarot deck - Horsewoman of Staves.jpg",
    "Cary-Yale Tarot deck - Horsewoman of Swords.jpg", "Cary-Yale Tarot deck - Knight of Coins.jpg",
    "Cary-Yale Tarot deck - Knight of Cups.jpg", "Cary-Yale Tarot deck - Damsel of Coins.jpg",
    "Cary-Yale Tarot deck - Damsel of Cups.jpg", "Cary-Yale Tarot deck - Damsel of Staves.jpg",
    "Cary-Yale Tarot deck - Damsel of Swords.jpg", "Cary-Yale Tarot deck - Queen of Coins.jpg",
    "Cary-Yale Tarot deck - Queen of Staves.jpg", "Cary-Yale Tarot deck - Queen of Swords.jpg",
    "Cary-Yale Tarot deck - King of Coins.jpg", "Cary-Yale Tarot deck - King of Cups.jpg",
    "Cary-Yale Tarot deck - King of Sword.jpg",
]

# Normalise the deck's idiosyncratic suit labels to four suits.
SUIT_NORM = {
    "arrows": ("Batons", "Bastoni", "Fire", "will, work, and growth"),
    "staves": ("Batons", "Bastoni", "Fire", "will, work, and growth"),
    "coins": ("Coins", "Denari", "Earth", "the material world — money, body, and provision"),
    "cups": ("Cups", "Coppe", "Water", "feeling, love, and devotion"),
    "spades": ("Swords", "Spade", "Air", "mind, conflict, and decision"),
    "swords": ("Swords", "Spade", "Air", "mind, conflict, and decision"),
    "sword": ("Swords", "Spade", "Air", "mind, conflict, and decision"),
}
RANK_NORM = {
    "ace": ("Ace", 1), "two": ("Two", 2), "three": ("Three", 3), "four": ("Four", 4),
    "five": ("Five", 5), "six": ("Six", 6), "seven": ("Seven", 7), "eight": ("Eight", 8),
    "nine": ("Nine", 9), "ten": ("Ten", 10),
    "knave": ("Knave", 11), "damsel": ("Damsel", 12), "knight": ("Knight", 13),
    "horsewoman": ("Horsewoman", 14), "queen": ("Queen", 15), "king": ("King", 16),
}
COURT_ROLE = {
    "Knave": "the male page of the suit — its youth, the student and messenger",
    "Damsel": "the female page — a court rank found almost only in this deck, the maiden of the suit",
    "Knight": "the male rider — the suit questing, active, in motion",
    "Horsewoman": "the female rider — a female knight unique to the Cary-Yale, the suit's energy embodied in a noblewoman on horseback",
    "Queen": "the inward sovereignty of the suit — it held, nurtured, understood",
    "King": "the outward authority of the suit — it commanded and ruled in the world",
}

PIP_MEANING = {
    1: "the pure root of the suit, its whole nature held in one",
    2: "duality and exchange — pairing, the first relationship",
    3: "first increase — growth and fellowship",
    4: "stability and foundation — the settled square",
    5: "tension and loss — friction within the suit",
    6: "harmony and reciprocity — give and take in balance",
    7: "striving — effort against resistance",
    8: "movement and change — energy in motion",
    9: "near-fullness — the suit almost complete",
    10: "completion — the suit in full, plenty and burden together",
}


def parse_card(fname):
    core = fname[len("Cary-Yale Tarot deck - "):-len(".jpg")]
    parts = core.lower().split(" of ")
    if len(parts) != 2:
        return None
    rank_raw, suit_raw = parts[0].strip(), parts[1].strip()
    if rank_raw not in RANK_NORM or suit_raw not in SUIT_NORM:
        return None
    return RANK_NORM[rank_raw], SUIT_NORM[suit_raw], fname


items = []
sort_order = 0

# Trumps & virtues
for tid, name, ital, fname, icon, hist, reading in TRUMPS:
    u = img(fname)
    cat = "virtue" if tid.startswith("virtue") else "trump"
    items.append({
        "id": tid, "name": name, "sort_order": sort_order, "category": cat, "level": 1,
        "keywords": [name.lower(), ital.lower(), "trump" if cat == "trump" else "theological virtue",
                     "cary-yale"],
        "image_url": u,
        "metadata": {
            "arcana": "trump", "italian_name": ital, "status": "surviving",
            "museum": "Beinecke Rare Book & Manuscript Library, Yale University",
            "illustrations": [{
                "url": u, "artist": "Bonifacio Bembo workshop", "artist_dates": "active c. 1444–1482",
                "edition": "Cary-Yale (Visconti di Modrone) Tarot, c. 1442",
                "scene": f"{name} ({ital})", "license": "Public Domain", "is_primary": True,
            }],
        },
        "sections": {"Iconography": icon, "History": hist, "Reading": reading},
    })
    sort_order += 1

# Pips & courts (only those that survive, parsed from filenames)
suit_order = {"Coins": 0, "Cups": 1, "Swords": 2, "Batons": 3}
parsed = [p for p in (parse_card(f) for f in CARY_FILES) if p]
parsed.sort(key=lambda p: (suit_order[p[1][0]], p[0][1]))
for (rank_disp, rank_num), (suit_disp, suit_ital, element, theme), fname in parsed:
    u = img(fname)
    is_court = rank_num >= 11
    cardname = f"{rank_disp} of {suit_disp}"
    sid = suit_disp.lower()
    item_id = f"{sid}-{rank_disp.lower()}"
    if is_court:
        icon = (f"{cardname}: a courtly figure of the Visconti-Sforza house in gold brocade bearing the "
                f"emblem of {suit_disp}. The Cary-Yale is unique for its six-rank courts — King, Queen, "
                f"Knight, Horsewoman, Knave, and Damsel — half of them women.")
        hist = (f"A surviving court card of {suit_disp} ({suit_ital}). The female Horsewoman and Damsel ranks "
                f"that swell these courts appear in almost no other tarot, and gave the deck 86 cards in its "
                f"original state.")
        reading = f"{cardname} — {COURT_ROLE[rank_disp]}, within {theme}."
    else:
        emblem = "emblem" if rank_num == 1 else "emblems"
        icon = (f"{cardname}: {rank_num} gold-and-colour {suit_disp.lower()[:-1] if suit_disp.endswith('s') else suit_disp.lower()} "
                f"{emblem} arranged with scrolling decoration on a tooled gold ground — a decorative pip, "
                f"not a narrative scene.")
        hist = (f"A surviving pip of {suit_disp} ({suit_ital}), the suit of {element}, painted for the game "
                f"of trionfi.")
        reading = f"{cardname} — {PIP_MEANING[rank_num]}, within {theme}."
    items.append({
        "id": item_id, "name": cardname, "sort_order": sort_order,
        "category": f"suit-{sid}", "level": 1,
        "keywords": [suit_disp.lower(), element.lower(), rank_disp.lower(),
                     "court card" if is_court else "pip", suit_ital.lower()],
        "image_url": u,
        "metadata": {
            "arcana": "minor", "suit": suit_disp, "suit_italian": suit_ital, "element": element,
            "rank": rank_disp, "court": is_court, "status": "surviving",
            "illustrations": [{
                "url": u, "artist": "Bonifacio Bembo workshop", "artist_dates": "active c. 1444–1482",
                "edition": "Cary-Yale (Visconti di Modrone) Tarot, c. 1442",
                "scene": cardname, "license": "Public Domain", "is_primary": True,
            }],
        },
        "sections": {"Iconography": icon, "History": hist, "Reading": reading},
    })
    sort_order += 1

# ---- L2 emergences ----------------------------------------------------------
all_ids = {it["id"] for it in items}
trump_ids = [it["id"] for it in items if it["category"] == "trump"]
virtue_ids = [it["id"] for it in items if it["category"] == "virtue"]
emergences = [
    ("emg-surviving-trumps", "The Surviving Trumps", trump_ids,
     img("Cary-Yale Tarot deck - The Lovers.jpg"),
     {"About these Cards": "Only a handful of the Cary-Yale's triumphs survive: the Emperor, Empress, "
      "Lovers, Chariot, Strength, Death, Judgement, and the World. The rest are lost. What remains is enough "
      "to show a deck of extraordinary richness — full gold grounds, individualised faces, dynastic pride.",
      "How to Use": "Read these as the fragments of a once-complete procession of estates, made to "
      "celebrate a ducal marriage."}),
    ("emg-theological-virtues", "The Theological Virtues — Faith, Hope, Charity",
     virtue_ids, img("Cary-Yale Tarot deck - Faith.jpg"),
     {"About these Cards": "The Cary-Yale alone among tarots adds the three THEOLOGICAL virtues — Faith, "
      "Hope, and Charity — to the usual cardinal virtues. No other tarot deck contains them. They turn the "
      "deck into a complete medieval moral cosmos.",
      "Why this Matters": "These three cards are the single strongest sign that the early tarot trumps were "
      "conceived as a moral and cosmological ladder, not a random gallery — and a reminder of how much the "
      "'standard' 22-trump sequence is a later simplification."}),
]
for sid, sdisp in [("coins", "Coins"), ("cups", "Cups"), ("swords", "Swords"), ("batons", "Batons")]:
    children = [it["id"] for it in items if it["category"] == f"suit-{sid}"]
    if not children:
        continue
    rep = next((it["image_url"] for it in items if it["category"] == f"suit-{sid}"
                and it["metadata"].get("court")), children and
               next(it["image_url"] for it in items if it["category"] == f"suit-{sid}"))
    emergences.append((
        f"emg-suit-{sid}", f"Suit of {sdisp} — with the Six-Rank Court", children, rep,
        {"About this Suit": f"The surviving {sdisp} cards of the Cary-Yale. Like all four suits here, its "
         f"court runs to six ranks — King, Queen, Knight, Horsewoman, Knave, Damsel — doubling the usual "
         f"nobility with female riders and pages.",
         "How to Use": f"Browse the suit to see the Cary-Yale's defining peculiarity: a court half made of "
         f"women, unmatched in any other historical tarot."}))

for eid, ename, children, image_url, sections in emergences:
    children = [c for c in children if c in all_ids]
    items.append({
        "id": eid, "name": ename, "sort_order": sort_order, "category": "emergence", "level": 2,
        "composite_of": children, "relationship_type": "emergence",
        "image_url": image_url, "metadata": {}, "sections": sections,
    })
    sort_order += 1

for it in items:
    if it.get("category") != "emergence":
        it["sections"]["Tradition Note"] = TRADITION_NOTE

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0", "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Bonifacio Bembo (workshop)", "date": "c. 1442",
             "note": "Painter of the Cary-Yale (Visconti di Modrone) Tarot, Milan"},
            {"name": "Beinecke Rare Book & Manuscript Library, Yale", "date": "holding institution",
             "note": "Holds the 67 surviving Cary-Yale cards (Cary Collection of Playing Cards)"},
            {"name": "Wikimedia Commons", "date": "public domain",
             "note": "Card images, Category:Cary-Yale Visconti Tarot"},
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar architecture and summaries"},
        ],
    },
    "name": "Cary-Yale Visconti Tarot — The Lavish Outlier (c. 1442)",
    "description": (
        "The most lavish and most unusual of the surviving hand-painted tarots. Around 1442 the workshop of "
        "Bonifacio Bembo painted the Cary-Yale, or Visconti di Modrone, deck in Milan — probably for the "
        "marriage of Bianca Maria Visconti and Francesco Sforza. It is built here only from the cards that "
        "survive (67, held at Yale's Beinecke Library), because the deck is famous precisely for what it "
        "contains.\n\n"
        "Two features set it apart from every other tarot. First, its courts have SIX ranks, not four — "
        "King, Queen, Knight, Knave, and, uniquely, a female Horsewoman and a female Damsel — so its court "
        "is half women. The 'Damsel of Swords' is one of these. Second, it adds the three THEOLOGICAL "
        "virtues — Faith, Hope, and Charity — to the usual cardinal virtues, found in no other tarot, "
        "turning the deck into a complete medieval moral cosmos. In its original state it may have held 86 "
        "cards.\n\n"
        "Each card carries an Iconography note (what Bembo painted), a History note, and a light Reading. "
        "This is a historical/iconographic grammar, not a divination deck. It is the sister of the "
        "Pierpont Morgan-Bergamo (Visconti-Sforza) and Brera-Brambilla decks from the same workshop.\n\n"
        "PUBLIC DOMAIN ILLUSTRATION REFERENCES: Bonifacio Bembo workshop, Cary-Yale / Visconti di Modrone "
        "Tarot, c. 1442 (Beinecke Rare Book & Manuscript Library, Yale, Cary Collection) — gold-ground "
        "tempera, International Gothic. All on Wikimedia Commons, Category:Cary-Yale Visconti Tarot."
    ),
    "grammar_type": "tarot",
    "creator_name": "PlayfulProcess",
    "creator_link": "https://recursive.eco",
    "cover_image_url": img("Cary-Yale Tarot deck - Damsel of Swords.jpg"),
    "tags": ["tarot", "cary-yale", "visconti-di-modrone", "history", "bonifacio-bembo",
             "trionfi", "milan", "15th-century", "public-domain", "theological-virtues"],
    "roots": ["western-esoteric", "renaissance"],
    "shelves": ["wonder", "mirror"],
    "lineages": ["Andreotti"],
    "worldview": "historical",
    "is_published": False,
    "items": items,
}

os.makedirs(OUT_DIR, exist_ok=True)
out_path = os.path.join(OUT_DIR, "grammar.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)
n_t = sum(1 for it in items if it["category"] in ("trump", "virtue"))
n_m = sum(1 for it in items if str(it["category"]).startswith("suit-"))
n_e = sum(1 for it in items if it["category"] == "emergence")
print(f"Wrote {out_path}")
print(f"  items: {len(items)}  (trumps/virtues {n_t}, minors {n_m}, emergences {n_e})")
print(f"  with image_url: {sum(1 for it in items if it.get('image_url'))}")
