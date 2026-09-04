# -*- coding: utf-8 -*-
"""Stamp canonical archetype hashtags onto every tarot card across the built decks.

This is the "second axis" unlock: it lets the viewer group ONE archetype (e.g.
Death) across EVERY deck that has it — orthogonal to the genealogy tree. It writes,
per L1 card item:
  * canonical hashtags into `keywords[]` using a `namespace:value` convention
    (e.g. "arcana:death", "suit:cups", "rank:king", "card:king-of-cups",
    "element:fire", "zodiac:scorpio", "virtue:prudence", "etteilla:cosmogony").
  * `metadata.archetype` — the single primary canonical key (or null).
  * `metadata.mapping_confidence` — "exact" | "loose" | "none".

The hard part is that you CANNOT join on number or local name: Etteilla renumbered
Death to 17; the Golden Dawn swapped Strength<->Justice; Minchiate has 20 cards with
no standard equivalent; Sola Busca only loosely maps. So this resolves by MEANING,
handles the exceptions explicitly, and refuses to force false equivalences (those get
their own namespace or a null archetype).

Run AFTER the deck generators (it rewrites grammars/*/grammar.json in place).
See plan/tarot-roadmap-and-supabase-log.md §6.
"""
import json
import os
import re

GRAMMARS = os.path.join(os.path.dirname(__file__), "..", "grammars")

DECKS = [
    "visconti-sforza-tarot", "cary-yale-visconti-tarot", "charles-vi-tarot",
    "minchiate-florence-tarot", "tarot-de-marseille-conver", "oswald-wirth-tarot",
    "golden-dawn-book-t-tarot", "court-de-gebelin-tarot",
    "etteilla-i-livre-de-thot", "etteilla-ii-egyptian", "etteilla-iii-oracle-des-dames",
    "tarocchino-bologna", "tarot-de-besancon",
]

# --- Major archetype resolver (by meaning; order matters) -------------------
# Tower patterns MUST precede Devil; High-Priestess MUST precede Pope.
MAJOR_PATTERNS = [
    (r"high priestess|papess|popess|priestess|papessa", "the-high-priestess"),
    (r"hierophant|grand pr[eê]tre|grand pretre|\ble pape\b|il papa|the pope|\bpope\b", "the-hierophant"),
    (r"empress|imp[eé]ratrice|imperatrice", "the-empress"),
    (r"emperor|empereur|imperatore|despote|despot", "the-emperor"),
    (r"magician|bateleur|bagatt|magus|juggler|bagatto", "the-magician"),
    (r"\bfool\b|\ble mat\b|\bil matto\b|\bmatto\b|folie|folly", "the-fool"),
    (r"lovers|amoureux|amour|amore|\blove\b", "the-lovers"),
    (r"chariot|\bcarro\b", "the-chariot"),
    (r"strength|\bforce\b|forza|fortezza|fortitude", "strength"),
    (r"justice|giustizia", "justice"),
    (r"hermit|ermit|vecchio|tempo|gobbo|hunchback|capucin|capuchin|old man", "the-hermit"),
    (r"wheel|\broue\b|ruota|fortune", "wheel-of-fortune"),
    (r"hanged|pendu|impiccato|traditore|appeso|traitor", "the-hanged-man"),
    (r"death|\bmort\b|morte", "death"),
    (r"temperance|temperanza|temp[eé]rance", "temperance"),
    # Tower BEFORE Devil:
    (r"tower|maison.?dieu|maison de dieu|casa del diavolo|house of the devil|temple foudroy|feu du ciel|struck temple", "the-tower"),
    (r"devil|diable|diavolo", "the-devil"),
    (r"\bstar\b|[eé]toile|stella", "the-star"),
    (r"moon|\blune\b|luna", "the-moon"),
    (r"\bsun\b|soleil|\bsole\b", "the-sun"),
    (r"judgement|judgment|jugement|giudizio|trumpet|trombe", "judgement"),
    (r"world|monde|mondo", "the-world"),
]


def resolve_major(name):
    n = name.lower()
    for pat, slug in MAJOR_PATTERNS:
        if re.search(pat, n):
            return slug
    return None


SUIT_MAP = {
    "coins": "coins", "coin": "coins", "denari": "coins", "deniers": "coins", "denier": "coins",
    "pentacles": "coins", "pentacle": "coins", "disks": "coins",
    "cups": "cups", "cup": "cups", "coppe": "cups", "coupes": "cups", "coupe": "cups",
    "swords": "swords", "sword": "swords", "spade": "swords", "spada": "swords",
    "epees": "swords", "épées": "swords", "epée": "swords", "épée": "swords", "epee": "swords",
    "batons": "wands", "baton": "wands", "bastoni": "wands", "wands": "wands", "wand": "wands",
    "staves": "wands", "arrows": "wands", "stave": "wands",
}
RANK_MAP = {
    "ace": "ace", "one": "ace", "two": "two", "three": "three", "four": "four", "five": "five",
    "six": "six", "seven": "seven", "eight": "eight", "nine": "nine", "ten": "ten",
    "page": "page", "valet": "page", "knave": "page", "fante": "page", "damsel": "page",
    "knight": "knight", "chevalier": "knight", "cavallo": "knight", "cavalier": "knight",
    "horsewoman": "knight", "queen": "queen", "reine": "queen", "regina": "queen",
    "king": "king", "roi": "king", "re": "king",
}
NUM_TO_RANK = {1: "ace", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
               7: "seven", 8: "eight", 9: "nine", 10: "ten"}

# Etteilla number -> (archetype, confidence, extra_hashtag)
ETTEILLA_MAJORS = {
    1: (None, "none", "etteilla:significator-male"),
    2: (None, "none", "etteilla:cosmogony"), 3: (None, "none", "etteilla:cosmogony"),
    4: (None, "none", "etteilla:cosmogony"), 5: (None, "none", "etteilla:cosmogony"),
    6: (None, "none", "etteilla:cosmogony"), 7: (None, "none", "etteilla:cosmogony"),
    8: (None, "none", "etteilla:cosmogony"),
    9: ("arcana:justice", "exact", None), 10: ("arcana:temperance", "exact", None),
    11: ("arcana:strength", "exact", None), 12: ("virtue:prudence", "loose", None),
    13: ("arcana:the-hierophant", "exact", None), 14: ("arcana:the-devil", "exact", None),
    15: ("arcana:the-magician", "exact", None), 16: ("arcana:judgement", "exact", None),
    17: ("arcana:death", "exact", None), 18: ("arcana:the-hermit", "exact", None),
    19: ("arcana:the-tower", "exact", None), 20: ("arcana:wheel-of-fortune", "exact", None),
    21: ("arcana:the-emperor", "loose", None),
    0: (None, "none", "etteilla:significator-female"),  # La Folie, number 0
}
ETTEILLA_BASE = {"batons": 22, "coupes": 36, "epees": 50, "deniers": 64}


def add_kw(item, *tags):
    kws = item.get("keywords") or []
    for t in tags:
        if t and t not in kws:
            kws.append(t)
    item["keywords"] = kws


def set_arch(item, archetype, confidence):
    md = item.setdefault("metadata", {})
    md["archetype"] = archetype
    md["mapping_confidence"] = confidence
    if archetype:
        add_kw(item, archetype)


def stamp_minor(item, suit_raw, rank_raw=None, number=None):
    suit = SUIT_MAP.get((suit_raw or "").lower().strip())
    rank = None
    if rank_raw:
        rank = RANK_MAP.get(rank_raw.lower().strip())
    if rank is None and number is not None:
        rank = NUM_TO_RANK.get(int(number))
    if not suit or not rank:
        set_arch(item, None, "none")
        return
    arche = f"card:{rank}-of-{suit}"
    add_kw(item, f"suit:{suit}", f"rank:{rank}")
    set_arch(item, arche, "exact")


def stamp_deck(slug):
    path = os.path.join(GRAMMARS, slug, "grammar.json")
    g = json.load(open(path, encoding="utf-8"))
    n = 0
    for it in g["items"]:
        cat = str(it.get("category", ""))
        md = it.get("metadata", {})
        if cat == "emergence" or it.get("level", 1) >= 2 or it.get("composite_of"):
            continue
        n += 1
        # ---- Etteilla decks: resolve by Etteilla number ----
        if slug.startswith("etteilla-"):
            num = md.get("number")
            try:
                num = int(num)
            except (TypeError, ValueError):
                num = None
            if md.get("arcana") == "major" or md.get("suit") in (None, ""):
                arche, conf, extra = ETTEILLA_MAJORS.get(num, (None, "none", None))
                add_kw(it, extra)
                set_arch(it, arche, conf)
            else:
                suit = md.get("suit")
                base = ETTEILLA_BASE.get(suit)
                if base is not None and num is not None:
                    off = num - base  # 0=king,1=queen,2=knight,3=page,4..13 = 10..ace
                    if off in (0, 1, 2, 3):
                        rank = {0: "king", 1: "queen", 2: "knight", 3: "page"}[off]
                        stamp_minor(it, suit, rank_raw=rank)
                    else:
                        stamp_minor(it, suit, number=14 - off)
                else:
                    stamp_minor(it, suit)
            continue
        # ---- Minchiate: use trump_group ----
        if slug == "minchiate-florence-tarot" and md.get("arcana") == "trump":
            grp = md.get("trump_group")
            name = it["name"].lower()
            if grp == "fool":
                set_arch(it, "arcana:the-fool", "exact")
            elif grp == "papi":
                add_kw(it, "minchiate:papi")
                set_arch(it, None, "none")
            elif grp == "element":
                el = next((e for e in ("fire", "water", "earth", "air") if e in name
                           or e in (it["sections"].get("Meaning", "").lower())), None)
                ital = {"fuoco": "fire", "acqua": "water", "terra": "earth", "aria": "air"}
                for k, v in ital.items():
                    if k in name:
                        el = v
                set_arch(it, f"element:{el}" if el else None, "exact" if el else "none")
            elif grp == "zodiac":
                sign = next((s for s in ("aries", "taurus", "gemini", "cancer", "leo", "virgo",
                            "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces")
                            if s in name), None)
                set_arch(it, f"zodiac:{sign}" if sign else None, "exact" if sign else "none")
            elif grp == "arie":
                m = resolve_major(name)
                set_arch(it, f"arcana:{m}" if m else None, "loose" if m == "judgement" else "exact" if m else "none")
            elif grp == "virtue":
                # Temperance/Fortitude/Justice = standard majors; Hope/Prudence/Faith/Charity = theological
                m = resolve_major(name)
                if m in ("temperance", "justice", "strength"):
                    set_arch(it, f"arcana:{m}", "exact")
                else:
                    v = next((v for v in ("hope", "prudence", "faith", "charity") if v in name), None)
                    ital = {"speranza": "hope", "prudenza": "prudence", "fede": "faith", "carità": "charity", "carita": "charity"}
                    for k, val in ital.items():
                        if k in name:
                            v = val
                    set_arch(it, f"virtue:{v}" if v else None, "exact" if v else "none")
            else:  # group 'trump'
                m = resolve_major(name)
                set_arch(it, f"arcana:{m}" if m else None, "exact" if m else "none")
            continue
        # ---- Besançon: Juno replaces Popess, Jupiter replaces Pope (loose) ----
        if slug == "tarot-de-besancon" and md.get("arcana") == "trump":
            name = it["name"].lower()
            if "juno" in name or "junon" in name:
                set_arch(it, "arcana:the-high-priestess", "loose")
            elif "jupiter" in name:
                set_arch(it, "arcana:the-hierophant", "loose")
            else:
                m = resolve_major(it["name"])
                set_arch(it, f"arcana:{m}" if m else None, "exact" if m else "none")
            continue
        # ---- Cary-Yale theological virtues (Faith/Hope/Charity trumps) ----
        if cat == "virtue":
            name = it["name"].lower()
            v = next((v for v in ("hope", "prudence", "faith", "charity") if v in name), None)
            set_arch(it, f"virtue:{v}" if v else None, "exact" if v else "none")
            continue
        # ---- Generic majors / trumps ----
        if md.get("arcana") in ("major", "trump") or cat in ("major-arcana", "trump"):
            m = resolve_major(it["name"])
            set_arch(it, f"arcana:{m}" if m else None, "exact" if m else "none")
            continue
        # ---- Generic minors ----
        if md.get("arcana") == "minor" or cat.startswith("suit-") or cat == "court":
            stamp_minor(it, md.get("suit"), rank_raw=md.get("rank"), number=md.get("number"))
            continue
        # fallback
        set_arch(it, None, "none")

    json.dump(g, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    return n


if __name__ == "__main__":
    total = 0
    for slug in DECKS:
        c = stamp_deck(slug)
        total += c
        print(f"  stamped {c:>3} cards in {slug}")
    print(f"Done. {total} cards stamped across {len(DECKS)} decks.")
