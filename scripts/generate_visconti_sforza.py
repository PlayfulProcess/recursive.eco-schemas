# -*- coding: utf-8 -*-
"""Generate grammars/visconti-sforza-tarot/grammar.json.

The Pierpont Morgan-Bergamo (Visconti-Sforza) tarot, Milan c.1451, workshop of
Bonifacio Bembo. Full 78-card historical deck: 22 trionfi (major arcana) + 56
minors. Four cards never survived (The Devil, The Tower, Knight of Coins, Three
of Swords); six majors were repainted by a later hand (Fortitude, Temperance,
Star, Moon, Sun, World). This is a historical / iconographic grammar, not a
modern divination deck.

Public domain images: Wikimedia Commons, Category:Pierpont Morgan-Bergamo
Visconti-Sforza Tarot. Verified filenames embedded below.
"""
import json
import os
import urllib.parse

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "grammars", "visconti-sforza-tarot")
COMMONS = "https://commons.wikimedia.org/wiki/Special:FilePath/"


def img(filename):
    if not filename:
        return None
    return COMMONS + urllib.parse.quote(filename)


TRADITION_NOTE = (
    "These cards were made to play a game — the Italian *trionfi* / *tarocchi* "
    "card game — not for divination, which arrived centuries later. The notes here "
    "are historical and iconographic; any reading is a modern interpretive overlay, "
    "not part of the deck's original use."
)


# ---------------------------------------------------------------------------
# 22 trionfi (major arcana). hand: "bembo" | "second" | "lost"
# ---------------------------------------------------------------------------
MAJORS = [
    (0, "il-matto", "The Fool", "Il Matto", "Visconti-sforza-00-fool.jpg", "bembo",
     "A ragged man in a tattered tunic, bare-legged, seven feathers standing in his hair and a club over his shoulder. He is the village madman, the social outcast painted with the same gold leaf as kings.",
     "Unnumbered and unnamed in the original game — the wild card that stands outside the sequence of triumphs. It survives in the Morgan Library portion of the deck.",
     "The zero before counting begins: the holy fool, innocence and folly walking together at the edge of the procession."),
    (1, "il-bagatto", "The Magician", "Il Bagatto", "Visconti-sforza-01-magician.jpg", "bembo",
     "A young man seated at a table set with small objects, a wand or knife in hand — a market conjuror, cobbler, or sleight-of-hand trickster.",
     "\"Bagatella\" means a trifle; he is the lowest of the triumphs, the everyman who opens the parade. The earliest, most worldly figure of the trumps.",
     "Human skill and craft, the hand at work — beginnings rooted in the ordinary and the makeshift."),
    (2, "la-papessa", "The Popess", "La Papessa", "Visconti-sforza-02-popess.jpg", "bembo",
     "A crowned woman in the brown habit of a nun, a triple papal tiara on her head and a book in her lap.",
     "The most scandalous card in the deck: she is almost certainly Sister Maifreda da Pirovano, a Visconti kinswoman elected 'popess' by the heretical Guglielmite sect and burned at the stake in 1300. A buried family memory rendered in gold.",
     "Hidden wisdom and forbidden authority — the feminine that holds a sacred book the world would rather she did not open."),
    (3, "limperatrice", "The Empress", "L'Imperatrice", "Visconti-sforza-03-empress.jpg", "bembo",
     "A crowned, enthroned woman bearing a shield emblazoned with the imperial eagle of the Visconti.",
     "Worldly feminine sovereignty wedded to the dynasty's heraldry — the Empress is the house made flesh.",
     "Abundance, fertile authority, the generative power that rules from a throne rather than a garden."),
    (4, "limperatore", "The Emperor", "L'Imperatore", "Visconti-sforza-04-emperor.jpg", "bembo",
     "A bearded sovereign enthroned, the imperial eagle on his shield, an orb or sceptre in hand.",
     "Temporal masculine power — a portrait of dynastic legitimacy in an age when the Visconti and Sforza were buying and marrying their way toward a crown.",
     "Structure, command, the steadying weight of the throne and the law it enforces."),
    (5, "il-papa", "The Pope", "Il Papa", "Visconti-sforza-05-pope.jpg", "bembo",
     "A pope in the triple tiara, hand raised in blessing, the crossed keys of Saint Peter near him.",
     "Spiritual authority answering the temporal Emperor — the sanctioned hierophant of the established Church.",
     "Tradition, blessing, the institutional channel through which the sacred is made official."),
    (6, "lamore", "The Lovers", "L'Amore", "Visconti-sforza-06-love.jpg", "bembo",
     "A couple stand hand in hand beneath a canopy while a blindfolded Cupid takes aim from a pedestal above them.",
     "Likely a Visconti-Sforza marriage portrait — possibly Francesco Sforza and Bianca Maria Visconti, whose union produced the deck's patrons. Here love is dynastic alliance.",
     "Union and choice, the binding of two houses — desire pressed into the service of lineage."),
    (7, "il-carro", "The Chariot", "Il Carro", "Visconti-sforza-07-chariot.jpg", "bembo",
     "A crowned lady stands in a triumphal car, sometimes drawn by winged horses, holding orb and sceptre.",
     "The card that names the whole game: a Roman-style 'trionfo', the victory parade from which 'trumps' descend.",
     "Victory and momentum, the self carried forward in triumph over what it has mastered."),
    (8, "la-giustizia", "Justice", "La Giustizia", "Visconti-sforza-08-justice.jpg", "bembo",
     "An enthroned woman holds an upraised sword and a balance; above her a small armoured knight rides across the gold.",
     "In this pre-occult ordering Justice sits at VIII (the Golden Dawn would later swap it with Strength). The mounted knight is a Visconti flourish.",
     "Balance and reckoning, the blade and the scale — measure applied without flinching."),
    (9, "il-vecchio", "The Hermit", "Il Vecchio (Il Tempo)", "Visconti-sforza-09-time.jpg", "bembo",
     "A stooped old man with a long beard holds aloft not a lantern but an hourglass, wrapped in heavy robes.",
     "Originally 'Il Tempo' — Time, or the Old Man — not yet the lamp-bearing Hermit of later decks. The hourglass marks his true subject.",
     "Time, age, and solitary measure — the slow accounting of hours that no triumph escapes."),
    (10, "la-ruota", "Wheel of Fortune", "La Ruota della Fortuna", "Visconti-sforza-10-fortune.jpg", "bembo",
     "A blindfolded Fortuna turns a great wheel; four figures cling to it, some sprouting asses' ears and tails as they rise and fall, mottoes streaming from their mouths.",
     "A medieval commonplace given Bembo's gold — 'regnabo, regno, regnavi, sum sine regno' (I shall reign, I reign, I have reigned, I am without reign).",
     "The turning of fortune, rise and fall — the one law that levels emperor and fool alike."),
    (11, "la-fortezza", "Strength", "La Fortezza", "Visconti-sforza-11-fortitude.jpg", "second",
     "A standing figure subdues a lion, gripping it in a Hercules-like display of mastery.",
     "One of the six cards repainted by a later hand (c.1480s–90s, often attributed to Antonio Cicognara) after the Bembo original was lost. The style is visibly different from the first artist's.",
     "Fortitude — courage that masters the beast not by force alone but by steady will."),
    (12, "il-traditore", "The Hanged Man", "Il Traditore (L'Appeso)", "Visconti-sforza-12-traitor.jpg", "bembo",
     "A youth hangs upside down by one ankle from a wooden frame, hands bound behind his back, the free leg crossed.",
     "A 'pittura infamante' — the shaming portrait Italian cities painted of traitors and debtors, hung by the foot. Only later did occultists read it as sacrifice.",
     "Suspension and reversal — the inverted view, the betrayer's punishment, the world seen from upside down."),
    (13, "la-morte", "Death", "La Morte", "Visconti-sforza-13-death.jpg", "bembo",
     "A gaunt skeletal figure stands on foot drawing a great bow, or bearing a scythe across barren ground.",
     "Unnamed and unnumbered in the original deck — the card too plain to need a label. The great equaliser of the danse macabre.",
     "Transition and the great levelling — the end that makes no exception for rank or gold."),
    (14, "la-temperanza", "Temperance", "La Temperanza", "Visconti-sforza-14-temperance.jpg", "second",
     "A winged woman pours liquid between two vessels in an unbroken stream.",
     "Another of the six later-hand restorations. Temperance's gesture — mixing without spilling — is among the oldest stable tarot images.",
     "Tempering and flow — the patient blending of waters, moderation as a living art."),
    (15, "il-diavolo", "The Devil", "Il Diavolo", None, "lost",
     "No Bembo card survives. Later decks in the tradition show a horned, clawed figure presiding over bound captives; the Visconti-Sforza original is simply gone.",
     "One of four cards never recovered from this deck. Whether it was lost, destroyed, or — as some suggest — deliberately removed, we cannot know. Its absence is part of the deck's history.",
     "Bondage, appetite, the shadow side of power — read here through a deliberate, instructive silence."),
    (16, "la-torre", "The Tower", "La Torre (La Casa del Diavolo)", None, "lost",
     "No Bembo card survives. In the broader tradition the Tower — 'the House of the Devil', or 'the Fire' — shows a struck tower and falling figures.",
     "The second of the deck's permanently lost cards. The early Italian decks often called it the Fire or the House of God; here only the gap remains.",
     "Sudden collapse and the breaking of false structures — present in this deck only as a missing card, an emptiness where catastrophe should be."),
    (17, "la-stella", "The Star", "La Stella", "Visconti-sforza-17-star.jpg", "second",
     "A woman stands holding aloft a single great eight-pointed star against the gold.",
     "One of the six later restorations. The Visconti Star is a simple votive figure, far from the kneeling water-pourer of the Marseille and Waite decks.",
     "Hope and orientation — a fixed light to steer by after the dark of Death and the lost Tower."),
    (18, "la-luna", "The Moon", "La Luna", "Visconti-sforza-18-moon.jpg", "second",
     "A woman holds up a crescent moon, robed and serene.",
     "Later-hand restoration. The eerie dogs-and-crayfish landscape of later Moon cards is a much later invention; here the Moon is simply held, like an attribute.",
     "Reflection and the night mind — the borrowed light that governs tides and dreams."),
    (19, "il-sole", "The Sun", "Il Sole", "Visconti-sforza-19-sun.jpg", "second",
     "A winged child (putto) floats above a hilly landscape, lifting a radiant human-faced sun overhead.",
     "Among the six repainted cards. The cherub bearing the sun is one of Bembo's most charming surviving compositions in the restored hand.",
     "Vitality and the lit world — radiance carried by something small and unafraid."),
    (20, "il-giudizio", "Judgement", "Il Giudizio", "Visconti-sforza-20-judgment.jpg", "second",
     "God the Father with attendant angels sounds the trumpet above; below, the dead rise naked from their tombs.",
     "Later-hand restoration. A straightforward Last Judgement, the most explicitly Christian of the trumps.",
     "The call and the reckoning — awakening, summons, the dead rising to answer."),
    (21, "il-mondo", "The World", "Il Mondo", "Visconti-sforza-21-world.jpg", "second",
     "Two winged putti hold up a great orb in which a walled city floats above water and hills, crowned by a star or a standing figure.",
     "The last and highest triumph, and the final card of the six restorations — the triumph that overcomes all other triumphs.",
     "Completion and wholeness — the cosmos held up to be seen, the journey of the trionfi closed."),
]

# ---------------------------------------------------------------------------
# 56 minors. Suits map to Bembo filename stems; lost cards have no image.
# ---------------------------------------------------------------------------
SUITS = [
    # (id, display, italian, element, filestem, emblem_sing, emblem_plur, theme)
    ("coins", "Coins", "Denari", "Earth", "coins", "coin", "coins",
     "the material world — money, body, land, and the slow work of provision"),
    ("cups", "Cups", "Coppe", "Water", "cups", "cup", "cups",
     "feeling and relationship — love, devotion, and the inner life"),
    ("swords", "Swords", "Spade", "Air", "swords", "sword", "swords",
     "mind and conflict — thought, strife, decision, and the cut of judgment"),
    ("batons", "Batons", "Bastoni", "Fire", "staves", "baton", "batons",
     "will and growth — work, enterprise, and the green branch of action"),
]

# pip number -> (filename-fragment, terse meaning)
PIP_MEANING = {
    1: "the pure seed and root of the suit, its whole nature held in one",
    2: "duality and exchange — balance, pairing, the first relationship",
    3: "first increase — growth, fellowship, the suit beginning to flower",
    4: "stability and foundation — a settled square, rest, possession",
    5: "tension and loss — friction, lack, the challenge within the suit",
    6: "harmony and reciprocity — give and take in balance, ease restored",
    7: "striving — effort against resistance, partial and uncertain gain",
    8: "movement and change — energy in motion, swiftness, reordering",
    9: "near-fullness — intensity at its height, the suit almost complete",
    10: "completion — the suit in full, its plenty and its burden together",
}

# court rank -> (filename rank number, display, italian, role)
COURTS = [
    (11, "page", "Page", "Fante", "the student and messenger of the suit — its energy young, curious, not yet committed"),
    (12, "knight", "Knight", "Cavallo", "the suit in motion — questing, active, riding out to meet its element"),
    (13, "queen", "Queen", "Regina", "the inward mastery of the suit — it held, nurtured, and understood from within"),
    (14, "king", "King", "Re", "the outward authority of the suit — it commanded, ordered, and ruled in the world"),
]

# Verified available Bembo minor filenames (Commons). Anything not here = no image.
AVAILABLE_MINORS = {
    "coins-01-ace", "coins-02-deuce", "coins-03", "coins-04", "coins-05", "coins-06",
    "coins-07", "coins-08", "coins-09", "coins-10", "coins-11-knave", "coins-13-queen", "coins-14-king",
    "cups-01-ace", "cups-02-deuce", "cups-03", "cups-04", "cups-05", "cups-06", "cups-07",
    "cups-08", "cups-09", "cups-10", "cups-11-knave", "cups-12-knight", "cups-13-queen",
    "staves-01-ace", "staves-02-deuce", "staves-03", "staves-04", "staves-05", "staves-06",
    "staves-07", "staves-08", "staves-09", "staves-10", "staves-11-knave", "staves-12-knight",
    "staves-13-queen", "staves-14-king",
    "swords-01-ace", "swords-02-deuce", "swords-04", "swords-05", "swords-06", "swords-07",
    "swords-08", "swords-09", "swords-10", "swords-11-knave", "swords-12-knight",
    "swords-13-queen", "swords-14-king",
}

# The four permanently lost cards (id -> note)
LOST = {"swords-knight": "Knight of Swords",  # placeholder, recomputed below
        }


def minor_filename(filestem, ranknum, rank_token):
    """Build the Bembo filename fragment and full filename if it exists."""
    if ranknum == 1:
        frag = f"{filestem}-01-ace"
    elif ranknum == 2:
        frag = f"{filestem}-02-deuce"
    elif ranknum <= 10:
        frag = f"{filestem}-{ranknum:02d}"
    elif rank_token == "page":
        frag = f"{filestem}-11-knave"
    elif rank_token == "knight":
        frag = f"{filestem}-12-knight"
    elif rank_token == "queen":
        frag = f"{filestem}-13-queen"
    else:  # king
        frag = f"{filestem}-14-king"
    if frag in AVAILABLE_MINORS:
        return f"Bembo-Visconti-tarot-{frag}.jpg"
    return None


def ordinal_word(n):
    return {1: "Ace", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six",
            7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten"}[n]


items = []
sort_order = 0

# --- Major arcana ---
for num, slug, name, ital, fn, hand, icon, hist, reading in MAJORS:
    item = {
        "id": f"major-{num:02d}-{slug}",
        "name": f"{num} — {name}",
        "sort_order": sort_order,
        "category": "major-arcana",
        "level": 1,
        "keywords": [name.lower().replace("the ", ""), "trionfi", "major arcana", ital.lower()],
        "metadata": {
            "arcana": "major",
            "number": num,
            "italian_name": ital,
            "painter_hand": hand,
            "status": "lost" if hand == "lost" else "surviving",
            "museum": "Pierpont Morgan Library, New York / Accademia Carrara, Bergamo",
        },
        "sections": {
            "Iconography": icon,
            "History": hist,
            "Reading": reading,
        },
    }
    u = img(fn)
    if u:
        item["image_url"] = u
        item["metadata"]["illustrations"] = [{
            "url": u,
            "artist": "Bonifacio Bembo workshop" + (" (later restoration hand)" if hand == "second" else ""),
            "artist_dates": "active c. 1444–1482",
            "edition": "Pierpont Morgan-Bergamo Visconti-Sforza Tarot, c. 1451",
            "scene": f"{name} ({ital})",
            "license": "Public Domain",
            "is_primary": True,
        }]
    items.append(item)
    sort_order += 1

# --- Minor arcana: pips then courts, suit by suit ---
LOST_MINORS = {("coins", "knight"), ("swords", 3)}  # Knight of Coins, Three of Swords

for sid, sdisp, sital, element, filestem, emb_s, emb_p, theme in SUITS:
    # pips 1..10
    for n in range(1, 11):
        is_lost = (sid, n) in LOST_MINORS
        word = ordinal_word(n)
        cardname = f"{word} of {sdisp}"
        if n == 1:
            emblem_phrase = f"a single {emb_s}"
        else:
            emblem_phrase = f"{n} {emb_p}"
        icon = (f"{cardname[0].upper()}{cardname[1:]}: {emblem_phrase} arranged amid gold-leaf "
                f"scrollwork and Visconti-Sforza heraldic flourishes on a punched gold ground. "
                f"Like all early Italian pips, it is decorative rather than scenic — there is no "
                f"narrative picture, only the suit-emblems themselves made splendid.")
        if is_lost:
            hist = ("One of the four cards that never survived from this deck. Its image is "
                    "reconstructed only by inference from the suit's other pips.")
        else:
            hist = (f"A pip card of {sdisp} ({sital}), the suit of {element}. Painted in the "
                    f"Bembo workshop for the dukes of Milan, it was a playing card for the game "
                    f"of trionfi — divinatory meanings were attached only centuries later.")
        reading = f"{word} of {sdisp} — {PIP_MEANING[n]}, within {theme}."
        item = {
            "id": f"{sid}-{n:02d}" if n > 1 else f"{sid}-ace",
            "name": cardname,
            "sort_order": sort_order,
            "category": f"suit-{sid}",
            "level": 1,
            "keywords": [sdisp.lower(), element.lower(), word.lower(), "minor arcana", sital.lower()],
            "metadata": {
                "arcana": "minor", "suit": sdisp, "suit_italian": sital,
                "element": element, "rank": word,
                "status": "lost" if is_lost else "surviving",
            },
            "sections": {"Iconography": icon, "History": hist, "Reading": reading},
        }
        rank_token = "ace" if n == 1 else str(n)
        fn = None if is_lost else minor_filename(filestem, n, rank_token)
        if fn:
            u = img(fn)
            item["image_url"] = u
            item["metadata"]["illustrations"] = [{
                "url": u, "artist": "Bonifacio Bembo workshop", "artist_dates": "active c. 1444–1482",
                "edition": "Pierpont Morgan-Bergamo Visconti-Sforza Tarot, c. 1451",
                "scene": cardname, "license": "Public Domain", "is_primary": True,
            }]
        items.append(item)
        sort_order += 1
    # courts
    for ranknum, rtoken, rdisp, rital, role in COURTS:
        is_lost = (sid, "knight") in LOST_MINORS and rdisp == "Knight"
        cardname = f"{rdisp} of {sdisp}"
        icon = (f"{cardname}: a courtly {rital.lower()} figure of the house of Visconti-Sforza, "
                f"richly robed in gold brocade and bearing the {emb_s} of the suit. The court "
                f"cards are the deck's portrait gallery — idealised nobles rather than scenes.")
        if is_lost:
            hist = ("The Knight of Coins is one of the four permanently lost cards of this deck — "
                    "no surviving example is known.")
        else:
            hist = (f"A court card of {sdisp} ({sital}). In the four-court Morgan-Bergamo deck the "
                    f"ranks run Page, Knight, Queen, King — the Cary-Yale sister deck unusually "
                    f"doubled these with female knights and damsels.")
        reading = f"{cardname} — {role}, expressed through {theme}."
        item = {
            "id": f"{sid}-{rdisp.lower()}",
            "name": cardname,
            "sort_order": sort_order,
            "category": f"suit-{sid}",
            "level": 1,
            "keywords": [sdisp.lower(), element.lower(), rdisp.lower(), "court card", rital.lower()],
            "metadata": {
                "arcana": "minor", "suit": sdisp, "suit_italian": sital, "element": element,
                "rank": rdisp, "court": True,
                "status": "lost" if is_lost else "surviving",
            },
            "sections": {"Iconography": icon, "History": hist, "Reading": reading},
        }
        fn = None if is_lost else minor_filename(filestem, ranknum, rdisp.lower())
        if fn:
            u = img(fn)
            item["image_url"] = u
            item["metadata"]["illustrations"] = [{
                "url": u, "artist": "Bonifacio Bembo workshop", "artist_dates": "active c. 1444–1482",
                "edition": "Pierpont Morgan-Bergamo Visconti-Sforza Tarot, c. 1451",
                "scene": cardname, "license": "Public Domain", "is_primary": True,
            }]
        items.append(item)
        sort_order += 1

# --- Cross-reference images from the Cary-Yale sister deck ---
# Three cards have no Morgan-Bergamo image on Commons (King of Cups is not
# digitized; Knight of Coins and Three of Swords are lost). The Cary-Yale deck
# (same Bembo workshop, c. 1442) preserves all three — shown here, clearly
# labelled as the sister deck. The Devil and Tower survive in NO 15th-century
# Visconti deck, so they remain deliberate gaps.
# Each entry carries a full, self-consistent History (it REPLACES the generated
# text, which otherwise contradicts the cross-referenced image — e.g. "no
# surviving example" beside "where it survives").
CARY_YALE = {
    "cups-king": ("Cary-Yale Tarot deck - King of Cups.jpg", "King of Cups",
                  "A court card of Cups (Coppe). The Morgan-Bergamo King of Cups survives but has not "
                  "been digitized on Wikimedia Commons, so the image shown here is the King of Cups from "
                  "the Cary-Yale (Visconti di Modrone) deck — the same Bembo workshop, about a decade "
                  "earlier. In the four-court Morgan-Bergamo deck the ranks run Page, Knight, Queen, King; "
                  "the Cary-Yale deck unusually doubled these with female knights and damsels."),
    "coins-knight": ("Cary-Yale Tarot deck - Knight of Coins.jpg", "Knight of Coins",
                     "The Knight of Coins is one of the four cards lost from the Morgan-Bergamo deck — no "
                     "Morgan-Bergamo example survives. The image shown here is the Knight of Coins from "
                     "the Cary-Yale sister deck (c. 1442, same Bembo workshop), where it does survive, "
                     "standing in for the lost original."),
    "swords-03": ("Cary-Yale Tarot deck - Three of Spades.jpg", "Three of Swords (Spade)",
                  "The Three of Swords is one of the four cards lost from the Morgan-Bergamo deck. The "
                  "image shown here is the Three of Swords (Spade) from the Cary-Yale sister deck "
                  "(c. 1442, same Bembo workshop), where it survives, standing in for the lost original."),
}
for it in items:
    ref = CARY_YALE.get(it["id"])
    if not ref:
        continue
    fname, scene, history = ref
    u = img(fname)
    it["image_url"] = u
    it["metadata"]["image_source"] = "cary-yale-sister-deck"
    it["metadata"]["illustrations"] = [{
        "url": u, "artist": "Bonifacio Bembo workshop",
        "artist_dates": "active c. 1444–1482",
        "edition": "Cary-Yale (Visconti di Modrone) Tarot, c. 1442 (sister deck)",
        "scene": scene, "license": "Public Domain", "is_primary": True,
    }]
    it["sections"]["History"] = history

# --- L2 emergences ---
all_ids = {it["id"] for it in items}
major_ids = [it["id"] for it in items if it["category"] == "major-arcana"]
lost_ids = [it["id"] for it in items if it["metadata"].get("status") == "lost"]
second_hand_ids = [it["id"] for it in items if it["metadata"].get("painter_hand") == "second"]

DECK_GROUP_IMG = img("Viscontisforzatarot.jpg")
SPREAD_IMG = img("Visconti-Sforza tarot deck..jpg")

emergences = [
    ("emg-trionfi", "The Trionfi — The 22 Triumphs", "emergence", major_ids, DECK_GROUP_IMG,
     {"About the Triumphs": "The 22 trumps are the tarot's true invention — a fifth suit of allegorical "
      "'triumphs' added to an ordinary 56-card pack around 1440. They were not yet a spiritual journey; "
      "they were the high cards of a trick-taking game, a parade of estates from Fool to World. Only in "
      "the 18th century did occultists reread them as the soul's progress.",
      "How to Use": "Browse the trumps in order to see the medieval social cosmos the deck assumes: "
      "craftsman, popess, the imperial and papal powers, love, fortune, the virtues, death, the heavens, "
      "and the world entire."}),
    ("emg-suit-coins", "Suit of Coins (Denari) — Earth", "emergence",
     [it["id"] for it in items if it["category"] == "suit-coins"], img("Bembo-Visconti-tarot-coins-05.jpg"),
     {"About this Suit": "Coins (Denari) is the suit of Earth — money, body, land, and provision. In the "
      "Morgan-Bergamo deck its pips are gilded discs amid scrolling vines; the Knight of Coins is one of "
      "the deck's four lost cards.",
      "How to Use": "The suit of having and making — read it for questions of resources, work made tangible, "
      "and the slow accumulation of the material world."}),
    ("emg-suit-cups", "Suit of Cups (Coppe) — Water", "emergence",
     [it["id"] for it in items if it["category"] == "suit-cups"], img("Bembo-Visconti-tarot-cups-05.jpg"),
     {"About this Suit": "Cups (Coppe) is the suit of Water — feeling, love, and devotion. Its emblem is the "
      "chalice, and in a deck made to celebrate a marriage it carries the deck's romantic charge.",
      "How to Use": "The suit of the heart — read it for relationship, longing, and the inner life that the "
      "trumps dramatise on a cosmic scale."}),
    ("emg-suit-swords", "Suit of Swords (Spade) — Air", "emergence",
     [it["id"] for it in items if it["category"] == "suit-swords"], img("Bembo-Visconti-tarot-swords-05.jpg"),
     {"About this Suit": "Swords (Spade) is the suit of Air — mind, conflict, and decision. Its curved blades "
      "interlace across the gold; the Three of Swords is one of the deck's four lost cards.",
      "How to Use": "The suit of the cutting mind — read it for thought, strife, and the hard clarity of "
      "judgment."}),
    ("emg-suit-batons", "Suit of Batons (Bastoni) — Fire", "emergence",
     [it["id"] for it in items if it["category"] == "suit-batons"], img("Bembo-Visconti-tarot-staves-05.jpg"),
     {"About this Suit": "Batons (Bastoni), or Staves, is the suit of Fire — will, work, and growth. It is the "
      "deck's only complete minor suit, all fourteen cards surviving.",
      "How to Use": "The suit of action and enterprise — read it for ambition, labour, and the green energy "
      "of beginnings pushed into the world."}),
    ("emg-lost-cards", "The Lost Cards", "emergence", lost_ids, SPREAD_IMG,
     {"About the Lost Cards": "Four cards of this deck never survived: The Devil, The Tower, the Knight of "
      "Coins, and the Three of Swords. Whether lost to time, accident, or — in the case of the two dark "
      "trumps — possibly deliberate removal, we cannot know. Their absence is itself a historical document.",
      "Why this Matters": "The two missing trumps are precisely the deck's images of bondage and catastrophe. "
      "A deck made to glorify a dynasty has come down to us with its pictures of the Devil and the falling "
      "Tower torn out — a gap that later traditions had to imagine their way across."}),
    ("emg-second-hand", "The Restoration Hand — Six Repainted Triumphs", "emergence", second_hand_ids,
     img("Visconti-sforza-19-sun.jpg"),
     {"About these Cards": "Six trumps — Fortitude, Temperance, the Star, Moon, Sun, and World — were repainted "
      "by a later artist (c. 1480s–90s, often attributed to Antonio Cicognara) after the Bembo originals were "
      "lost. Their style, faces, and gold differ visibly from the first hand.",
      "Why this Matters": "The deck we call 'Visconti-Sforza' is already a restoration — a 15th-century object "
      "repaired within its own century. The seams between the two hands are a lesson in how every old deck is "
      "partly a reconstruction."}),
]

for eid, ename, rel, children, image_url, sections in emergences:
    children = [c for c in children if c in all_ids]
    item = {
        "id": eid,
        "name": ename,
        "sort_order": sort_order,
        "category": "emergence",
        "level": 2,
        "composite_of": children,
        "relationship_type": rel,
        "sections": sections,
        "metadata": {},
    }
    if image_url:
        item["image_url"] = image_url
    items.append(item)
    sort_order += 1


for it in items:
    if it.get("category") != "emergence":
        it["sections"]["Tradition Note"] = TRADITION_NOTE

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0",
        "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Bonifacio Bembo (workshop)", "date": "c. 1451",
             "note": "Original painter of the Pierpont Morgan-Bergamo Visconti-Sforza Tarot, Milan"},
            {"name": "Later restoration hand (attrib. Antonio Cicognara)", "date": "c. 1480s–1490s",
             "note": "Repainted six lost trumps: Fortitude, Temperance, Star, Moon, Sun, World"},
            {"name": "Wikimedia Commons", "date": "public domain",
             "note": "Card images, Category:Pierpont Morgan-Bergamo Visconti-Sforza Tarot"},
            {"name": "PlayfulProcess", "date": "2026",
             "note": "Grammar architecture, historical and iconographic summaries"},
        ],
    },
    "name": "Visconti-Sforza Tarot — The Oldest Tarot (Bonifacio Bembo, c. 1451)",
    "description": (
        "The oldest tarot tradition we can hold in our hands. Around 1451 the workshop of Bonifacio Bembo "
        "painted a deck of 78 cards in gold leaf and tempera for the ducal house of Visconti-Sforza in Milan "
        "— not for fortune-telling, which did not yet exist, but for a trick-taking card game called "
        "'trionfi' (triumphs), the ancestor of the word 'trumps'. This grammar holds the full historical "
        "deck: the 22 triumphs (major arcana) and the 56 minor cards across four suits — Coins, Cups, "
        "Swords, and Batons.\n\n"
        "It is a historical and iconographic grammar, not a modern divination deck. Each card carries an "
        "Iconography note (what Bembo actually painted), a History note (its place, condition, and story), "
        "and a light Reading. Four cards never survived — The Devil, The Tower, the Knight of Coins, and the "
        "Three of Swords — and are included here as deliberate gaps. Six trumps were repainted by a later "
        "hand after the originals were lost. The famous Popess is almost certainly Sister Maifreda da "
        "Pirovano, a Visconti kinswoman burned for heresy in 1300.\n\n"
        "Three related Bembo-workshop decks survive: the Cary-Yale (Visconti di Modrone, c. 1442), the "
        "Brera-Brambilla (c. 1442, fragmentary), and this Pierpont Morgan-Bergamo deck (c. 1451), the most "
        "complete with 74 of 78 cards. Source images: Wikimedia Commons (public domain).\n\n"
        "PUBLIC DOMAIN ILLUSTRATION REFERENCES: Bonifacio Bembo workshop, Pierpont Morgan-Bergamo "
        "Visconti-Sforza Tarot, c. 1451 (Pierpont Morgan Library, New York; Accademia Carrara, Bergamo; "
        "Colleoni collection) — gold-ground tempera on card, International Gothic style. Later restoration "
        "trumps attributed to Antonio Cicognara, c. 1480s–90s. Sister deck: Cary-Yale Visconti Tarot, "
        "c. 1442 (Beinecke Library, Yale) — the 'Damsel of Swords' and other six-court cards. All on "
        "Wikimedia Commons, Category:Visconti-Sforza tarot deck."
    ),
    "grammar_type": "tarot",
    "creator_name": "PlayfulProcess",
    "creator_link": "https://recursive.eco",
    "cover_image_url": img("Viscontisforzatarot.jpg"),
    "tags": ["tarot", "visconti-sforza", "history", "bonifacio-bembo", "trionfi",
             "milan", "15th-century", "public-domain", "major-arcana"],
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

# Summary
n_major = sum(1 for it in items if it["category"] == "major-arcana")
n_minor = sum(1 for it in items if str(it["category"]).startswith("suit-"))
n_emg = sum(1 for it in items if it["category"] == "emergence")
n_img = sum(1 for it in items if it.get("image_url"))
n_lost = sum(1 for it in items if it["metadata"].get("status") == "lost")
print(f"Wrote {out_path}")
print(f"  total items: {len(items)}  (majors {n_major}, minors {n_minor}, emergences {n_emg})")
print(f"  with image_url: {n_img}   lost cards: {n_lost}")
