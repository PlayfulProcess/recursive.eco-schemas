# -*- coding: utf-8 -*-
"""Rewrite the three Etteilla editions within Etteilla's own tradition.

Reads the LIVE decks pulled from Supabase (../_scratch_etteilla/deck-{I,II,III}.json,
with the author's R2 images) and rewrites each card's reading sections so they sit
inside Jean-Baptiste Alliette's (Etteilla's) actual cartomantic system, instead of
the generic modern-psychology text the minors currently carry.

What is rewritten, and why it is "within the tradition":
  * Etteilla's renamed/renumbered majors and their idiosyncratic meanings — the
    Bateleur as illness, the Capucin (Hermit) as the traitor, the Devil as raw
    force, the cosmogony/creation sequence of the first cards, the two
    significators (1 Le Chaos = male querent, 78 La Folie = female querent).
  * The COURT-AS-PERSON reading that is the signature of Etteilla/French
    cartomancy: every court card is a person, read by the suit's temperament and
    the rank's age/role, upright = well-disposed, reversed = ill-disposed.
  * Systematic reversed (renversé) meanings — Etteilla's own innovation.
  * The cosmogony scholarship (Etymology / Genesis / Historical / Hermetic) is
    preserved from the source decks and propagated to all three editions.

NOTE: the exact two-word period keyword printed on each historical card is NOT
asserted here where it could not be verified against a primary source; the
meanings are written faithfully in Etteilla's register. Sourcing the inscriptions
from Etteilla's 'Cours théorique' or Benebell Wen's reconstruction is a future
enrichment. (See build log.)
"""
import json
import os

HERE = os.path.dirname(__file__)
SCRATCH = os.path.join(HERE, "..", "..", "_scratch_etteilla")
GRAMMARS = os.path.join(HERE, "..", "grammars")

EDITIONS = {
    "I": {
        "slug": "etteilla-i-livre-de-thot",
        "title": "Etteilla I — Livre de Thot (Grand Etteilla, c. 1788–1791)",
        "edition_note": "The original deck — Jean-Baptiste Alliette's 'Livre de Thot', the first tarot ever "
                        "designed specifically for divination, with Basan's engravings and the Egyptian/"
                        "Hermetic framing Etteilla invented.",
        "printer": "Jean-Baptiste Alliette (Etteilla) / Basan, 1788–1791",
    },
    "II": {
        "slug": "etteilla-ii-egyptian",
        "title": "Etteilla II — Grand Étteilla Égyptien (Blocquel–Hodot, 1838–1845)",
        "edition_note": "The second edition, issued by Simon Blocquel (under the name 'Julia Orsini'), with "
                        "redesigned letterpress panels — the form in which the Etteilla system spread most widely.",
        "printer": "Simon-François Blocquel (as 'Julia Orsini'), 1838–1845",
    },
    "III": {
        "slug": "etteilla-iii-oracle-des-dames",
        "title": "Grand Jeu de l'Oracle des Dames (Etteilla III, c. 1865)",
        "edition_note": "The third edition — G. Regamey's vibrant chromolithographs for the 'Grand Jeu de "
                        "l'Oracle des Dames', the most decorative of the three Etteilla editions.",
        "printer": "G. Regamey / Haugard-Mauge, c. 1865",
    },
}

# --- Majors (Etteilla number -> short role, upright, reversed) ---------------
MAJORS = {
    1: ("Le Chaos — the male querent (significator)",
        "The male consultant himself: the matter as it now stands, full of unformed potential. The fertile "
        "void before the question takes shape.",
        "A question asked from confusion or anxiety; the void felt as emptiness rather than promise."),
    2: ("La Lumière — Light / Clarification",
        "Illumination and clarity — understanding dawning on the matter (Etteilla's 'éclaircissement').",
        "Fire and ardour turned destructive; clarity flaring into heat and haste."),
    3: ("Les Plantes — Growth / Discourse",
        "What is proposed takes root; growth, talk that bears fruit, the green beginning of a thing.",
        "Things still fluid and unsettled; words that run off like water, nothing yet rooted."),
    4: ("Le Ciel — The Heavens",
        "Favour from above: expansion, protection, a matter blessed and widening.",
        "A blessing withheld or delayed; distance, a sky that does not answer."),
    5: ("L'Homme et les Quadrupèdes — Man and Beasts",
        "The living world of work and livelihood; natural strength, sustenance, the body's labour.",
        "The brute in man; appetite unchecked, toil without reward."),
    6: ("Les Astres — The Stars",
        "The stars favourable: hope, guidance, a destiny inclined to the good.",
        "An ill or clouded star; hope deferred, a guiding light obscured."),
    7: ("Les Oiseaux et les Poissons — Birds and Fishes",
        "Air and water teeming: news, messages, plenty, journeys, fertile movement.",
        "Idle gossip, scattered news, a voyage or message delayed."),
    8: ("Le Repos — Rest",
        "The seventh day: rest, completion, peace earned after labour.",
        "Idleness and stagnation; rest curdled into inertia."),
    9: ("La Justice — Justice",
        "Lawful judgment, balance restored, a matter set right.",
        "Injustice, bias, the law bent or misused."),
    10: ("La Tempérance — Temperance",
         "Moderation and prudent management; opposites blended well.",
         "Excess and imbalance; the measure lost."),
    11: ("La Force — Strength",
         "Courage and self-mastery; force rightly governed.",
         "Weakness, or strength misused as domination."),
    12: ("La Prudence — Prudence",
         "Foresight and careful counsel (Etteilla set Prudence where ordinary tarot has the Hanged Man).",
         "Imprudence and rashness; a clear warning ignored."),
    13: ("Le Grand Prêtre — The High Priest",
         "Counsel, sanction, marriage, spiritual authority; a trusted guide.",
         "Hollow dogma, a bad counsellor, hypocrisy in high place."),
    14: ("Le Diable — Force / The Devil",
         "Raw force and vehemence — power over circumstance (Etteilla read the Devil as energy, not only evil).",
         "Fury and ravage; bondage to one's own passions."),
    15: ("Le Magicien / Le Bateleur — Illness",
         "The juggler's hand at work; in Etteilla's system the Bateleur governs illness and its cure — a "
         "matter of the body, skill applied.",
         "A charlatan, trickery; malady worsening, a false remedy."),
    16: ("Le Jugement Dernier — Last Judgement",
         "Awakening, a decisive change, renewal answering the trumpet's call.",
         "A verdict postponed; fear of change, the summons unheeded."),
    17: ("La Mort — Death",
         "Transformation, the necessary end that clears the ground.",
         "Inertia; a change resisted, an ending only half-made."),
    18: ("Le Capucin — The Traitor / Hermit",
         "The hooded solitary; in Etteilla's reading the Capucin is the traitor — concealment, a matter "
         "hidden, or prudent withdrawal.",
         "A secret enemy unmasked; treachery, false counsel exposed."),
    19: ("Le Temple Foudroyé — The Struck Temple",
         "The temple thrown down: sudden ruin, downfall, a structure broken open.",
         "A calamity narrowly escaped — but oppression, confinement, ruin deferred."),
    20: ("La Roue de Fortune — Wheel of Fortune",
         "Fortune turning upward: increase, elevation, luck in the matter.",
         "A fall; fortune reversed, gain turning to loss."),
    21: ("Le Despote Africain — The Sovereign",
         "Great power and a powerful protector; dissension mastered by a strong hand.",
         "Tyranny; a dangerous man, discord stirred from above."),
    0: ("La Folie — the female querent (significator)",
        "The female consultant herself, and the wild card outside the count: the matter unbound, open to "
        "any turn.",
        "Recklessness; a question asked in folly, energy with no rein."),
}

SUITS = {
    "batons": ("Bâtons", "Batons", "Fire", "enterprise, work, the countryside and growth"),
    "coupes": ("Coupes", "Cups", "Water", "love, affection, friendship and the heart"),
    "epees": ("Épées", "Swords", "Air", "conflict, law, arms and sharp trouble"),
    "deniers": ("Deniers", "Coins", "Earth", "money, trade, property and practical gain"),
}
SUIT_BASE = {"batons": 22, "coupes": 36, "epees": 50, "deniers": 64}

# Court-as-person: per suit, the four ranks (King, Queen, Knight, Page)
COURTS = {
    "batons": {
        "King": ("An enterprising, honourable man — of the country or of business; a good friend in practical affairs.",
                 "The same man turned harsh, grasping, or unreliable in his dealings."),
        "Queen": ("A capable, honest woman of warmth and industry; a good helper and counsellor.",
                  "A meddling or obstinate woman; help offered with strings."),
        "Knight": ("A departure, a young man setting out; enterprise on the move, news of work.",
                   "A hasty or quarrelsome youth; a journey or venture gone wrong."),
        "Page": ("A messenger, a youth bearing news of work or family; a small good beginning.",
                 "Bad news, a careless messenger, a rumour about one's affairs."),
    },
    "coupes": {
        "King": ("A fair, kindly, well-meaning man — often a man of feeling or of the Church; a benefactor in love or friendship.",
                 "A fickle or self-indulgent man; affection that cannot be trusted."),
        "Queen": ("A loving, fair-natured woman; devotion, friendship, a tender influence.",
                  "A jealous or capricious woman; love soured into possessiveness."),
        "Knight": ("An arrival, a lover or friend approaching; an invitation, a proposal of the heart.",
                   "A seducer or flatterer; an arrival that disappoints."),
        "Page": ("A fair youth bringing affection or good news; a sweet, sincere proposal.",
                 "A flatterer, an idle promise; feeling that is only on the surface."),
    },
    "epees": {
        "King": ("A man of law or of arms — a judge, soldier, or official; powerful, but often an adversary.",
                 "A cruel or vindictive man; authority used to wound, a dangerous enemy."),
        "Queen": ("A sharp, discerning woman, often a widow or one acquainted with sorrow; keen judgment.",
                  "A spiteful or grieving woman; malice, mourning, a bitter tongue."),
        "Knight": ("A soldier, the approach of conflict or a rival; swift, cutting action.",
                   "An enemy's attack, reckless aggression; conflict that overreaches."),
        "Page": ("A watcher or spy, a youth bearing sharp news; vigilance, a matter observed.",
                 "Surveillance turned hostile; a spy, slander, trouble carried by a youth."),
    },
    "deniers": {
        "King": ("A man of means — a merchant or man of property; reliable in money, a useful protector.",
                 "A miserly or corrupt man; wealth used coldly, gain without scruple."),
        "Queen": ("A prosperous, practical woman; security, a generous and capable manager.",
                  "A grasping or showy woman; luxury without warmth."),
        "Knight": ("Money arriving, a useful and dependable man; a profitable matter approaching.",
                   "A stalled payment, a heavy and unimaginative man; gain delayed."),
        "Page": ("A student or clerk, news of money or study; diligence, a small material beginning.",
                 "Bad news of money, a careless clerk; effort that earns little."),
    },
}

PIP_NUM = {
    1: ("a strong onset of the matter — the suit's force at its purest",
        "that force blocked or misdirected at the very start"),
    2: ("a meeting or exchange; the matter shared with another",
        "division, a pairing strained or broken"),
    3: ("increase; a third party, growth, the thing taking shape",
        "growth checked; effort scattered, a delay"),
    4: ("a settling, a small security, a needed pause",
        "stagnation; holding on too tightly"),
    5: ("a turn or loss within the matter — a test",
        "the loss easing, or the test deepening"),
    6: ("a passage, a road, fair give-and-take",
        "the way blocked; an exchange gone unequal"),
    7: ("a hope and a partial success, still uncertain",
        "the hope dashed; effort abandoned"),
    8: ("comings and goings, change, the matter in motion",
        "movement stalled; restlessness without progress"),
    9: ("near-fulfilment; intensity, the thing almost complete",
        "strain, delay, intensity turned against itself"),
    10: ("the matter at its fullest — completion, or surfeit",
         "excess and burden; a cycle that overstays"),
}
RANK_FROM_OFFSET = {0: "King", 1: "Queen", 2: "Knight", 3: "Page"}


def build_cosmo_map(deck_items):
    """number -> dict of preserved cosmogony sections."""
    cm = {}
    keys = ("Etymology", "Genesis Connection", "Historical Context", "Hermetic Correspondence")
    for it in deck_items:
        num = it.get("metadata", {}).get("number")
        try:
            num = int(num)
        except (TypeError, ValueError):
            continue
        extra = {k: it["sections"][k] for k in keys if k in it.get("sections", {})}
        if extra:
            cm[num] = extra
    return cm


def card_sections(num, arcana, suit, cosmo):
    secs = {}
    if arcana == "major" or suit is None:
        role, up, rev = MAJORS[num]
        secs["Card in Etteilla's System"] = role
        secs["Upright"] = up
        secs["Reversed"] = rev
    else:
        base = SUIT_BASE[suit]
        offset = num - base
        sdisp, seng, element, theme = SUITS[suit]
        if offset in RANK_FROM_OFFSET:
            rank = RANK_FROM_OFFSET[offset]
            up, rev = COURTS[suit][rank]
            secs["Card in Etteilla's System"] = (
                f"A court of {sdisp} ({seng}) — and so a PERSON. In Etteilla's cartomancy every court card "
                f"signifies someone in the querent's life, coloured by the suit ({theme}). Upright the person "
                f"is well-disposed; reversed, ill-disposed.")
            secs["Upright (the person well-disposed)"] = up
            secs["Reversed (the person ill-disposed)"] = rev
        else:
            pip = 14 - offset  # offset 4->10 ... 13->1
            up_n, rev_n = PIP_NUM[pip]
            secs["Card in Etteilla's System"] = (
                f"The {['','Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten'][pip]} of "
                f"{sdisp} ({seng}) — the suit of {element}, governing {theme}.")
            secs["Upright"] = f"{up_n}, within {theme.split(',')[0]}."
            secs["Reversed"] = f"{rev_n.capitalize()}."
    if num in cosmo:
        for k, v in cosmo[num].items():
            secs[k] = v
    return secs


SHARED_DESC = (
    "Jean-Baptiste Alliette — 'Etteilla' — created the first tarot deck made specifically for divination. "
    "He renamed and renumbered the cards around an Egyptian-Hermetic cosmogony: the first cards are the days "
    "of creation, two cards (Le Chaos and La Folie) are the male and female significators of the querent, "
    "and the trumps carry his own idiosyncratic meanings — the Bateleur as illness, the Capucin (Hermit) as "
    "the traitor, the Devil as raw force. He was also the first to give every card a systematic reversed "
    "meaning, and to read the sixteen court cards as PEOPLE in the querent's life.\n\n"
    "This edition is rewritten to sit inside that system: each card carries its place in Etteilla's "
    "structure, an Upright and a Reversed reading in his cartomantic register, and — for the courts — the "
    "person-reading that is the signature of French cartomancy. The cosmogony cards keep their etymology, "
    "Genesis, historical, and Hermetic notes.\n\n"
    "Scholarly note: the meanings are written faithfully to Etteilla's published system; the exact two-word "
    "keyword printed on each historical card is left for a future enrichment from a primary source "
    "(Etteilla's 'Cours théorique et pratique du livre de Thot') rather than guessed."
)


def main():
    # cosmogony sections shared across editions (sourced from deck I)
    deck1 = json.load(open(os.path.join(SCRATCH, "deck-I.json"), encoding="utf-8"))[0]["document_data"]
    cosmo = build_cosmo_map(deck1["items"])

    for ed, meta in EDITIONS.items():
        dd = json.load(open(os.path.join(SCRATCH, f"deck-{ed}.json"), encoding="utf-8"))[0]["document_data"]
        items = []
        for it in dd["items"]:
            md = it.get("metadata", {})
            try:
                num = int(md.get("number"))
            except (TypeError, ValueError):
                num = None
            arcana = md.get("arcana")
            suit = md.get("suit")
            new_it = {
                "id": it["id"],
                "name": it["name"],
                "sort_order": it.get("sort_order", len(items)),
                "category": arcana if arcana else "major",
                "level": 1,
                "keywords": it.get("keywords", []),
                "metadata": md,
                "sections": card_sections(num, arcana, suit, cosmo) if num is not None else it.get("sections", {}),
            }
            if it.get("image_url"):
                new_it["image_url"] = it["image_url"]
            items.append(new_it)

        grammar = {
            "_grammar_commons": {
                "schema_version": "1.0", "license": "CC-BY-SA-4.0",
                "attribution": [
                    {"name": "Jean-Baptiste Alliette (Etteilla)", "date": "1788–1791",
                     "note": "Original divinatory system, card titles, numbering, and reversed meanings"},
                    {"name": meta["printer"].split(",")[0], "date": meta["printer"].split(",")[-1].strip(),
                     "note": f"{meta['title']} edition"},
                    {"name": "Benebell Wen", "date": "2022",
                     "note": "Etteilla reconstruction research (benebellwen.com/etteilla)"},
                    {"name": "PlayfulProcess", "date": "2026",
                     "note": "Grammar architecture; readings rewritten within Etteilla's tradition"},
                ],
            },
            "name": dd.get("name"),
            "description": f"{meta['edition_note']}\n\n{SHARED_DESC}",
            "grammar_type": "tarot",
            "creator_name": "PlayfulProcess",
            "creator_link": "https://recursive.eco",
            "cover_image_url": dd.get("cover_image_url"),
            "tags": ["tarot", "etteilla", "cartomancy", "egyptian-tarot", "divination",
                     "livre-de-thot", "french-occult", "18th-century"],
            "roots": ["western-esoteric", "mysticism"],
            "shelves": ["wonder", "mirror"],
            "lineages": ["Andreotti"],
            "worldview": "esoteric",
            "is_published": False,
            "items": items,
        }
        out_dir = os.path.join(GRAMMARS, meta["slug"])
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "grammar.json"), "w", encoding="utf-8") as f:
            json.dump(grammar, f, indent=2, ensure_ascii=False)
        nimg = sum(1 for it in items if it.get("image_url"))
        print(f"Deck {ed}: wrote {meta['slug']}/grammar.json — {len(items)} items, {nimg} imaged")


if __name__ == "__main__":
    main()
