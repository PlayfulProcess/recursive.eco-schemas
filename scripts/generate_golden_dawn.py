# -*- coding: utf-8 -*-
"""Generate grammars/golden-dawn-book-t-tarot/grammar.json.

"The Golden Dawn version of Rider-Waite" — Pamela Colman Smith's public-domain
imagery carried by the FULL Hermetic Order of the Golden Dawn correspondence
system (Book T / Liber T, S.L. MacGregor Mathers, 1888; all PD).

Built precisely within the tradition:
  * Majors: Hebrew letter + Tree-of-Life path + astrological attribution + the
    Book T esoteric title.
  * Pips 2-10: the 36 decans (Planet in Sign) + Sephirah-in-World + Book T
    "Lord of ..." title.
  * Aces: Root of the Powers of the element (Kether).
  * Courts: the Golden Dawn rank (Knight/Queen/Prince/Princess) and
    element-in-element, mapped to the RWS King/Queen/Knight/Page.

Images are reused from the repo's existing rider-waite-smith-tarot grammar
(public domain RWS scans on Wikimedia Commons).
"""
import json
import os

HERE = os.path.dirname(__file__)
OUT_DIR = os.path.join(HERE, "..", "grammars", "golden-dawn-book-t-tarot")
RWS_PATH = os.path.join(HERE, "..", "grammars", "rider-waite-smith-tarot", "grammar.json")

# ---- Reuse RWS public-domain images ----------------------------------------
rws = json.load(open(RWS_PATH, encoding="utf-8"))
IMG_MAJOR = {}   # number -> url
IMG_MINOR = {}   # (suit, number) -> url
for it in rws["items"]:
    m = it.get("metadata", {})
    u = it.get("image_url")
    if not u:
        continue
    if m.get("arcana") == "major":
        IMG_MAJOR[m.get("number")] = u
    else:
        IMG_MINOR[(m.get("suit"), m.get("number"))] = u

# ---- Major arcana: Hebrew letter, path, astro, Book T title ----------------
# (num, slug, name, (letter, translit, meaning), path, astro, gd_title, upright, reversed)
MAJORS = [
    (0, "the-fool", "The Fool", ("א", "Aleph", "ox"), 11, "Air",
     "The Spirit of Æther",
     "Boundless potential, the divine spark stepping into incarnation; freedom, beginnings, holy folly.",
     "Recklessness, dispersion of force, a leap taken in ignorance rather than trust."),
    (1, "the-magician", "The Magician", ("ב", "Beth", "house"), 12, "Mercury",
     "The Magus of Power",
     "Will and skill uniting the four elements; conscious direction of force, the word made act.",
     "Trickery, cunning misused, willpower turned to manipulation or scattered."),
    (2, "the-high-priestess", "The High Priestess", ("ג", "Gimel", "camel"), 13, "the Moon",
     "The Priestess of the Silver Star",
     "Hidden wisdom, the unmanifest, intuition and the lunar current; the veil before the sanctuary.",
     "Secrets withheld, surface knowledge, intuition ignored or clouded."),
    (3, "the-empress", "The Empress", ("ד", "Daleth", "door"), 14, "Venus",
     "The Daughter of the Mighty Ones",
     "Generative love, fertility, the creative imagination clothing spirit in form.",
     "Sterility, indulgence, creative power blocked or squandered in excess."),
    (4, "the-emperor", "The Emperor", ("ה", "Heh", "window"), 15, "Aries",
     "Sun of the Morning, Chief among the Mighty",
     "Sovereign order, structure, the ordering reason that gives the world its law.",
     "Tyranny, rigidity, authority hardened into domination."),
    (5, "the-hierophant", "The Hierophant", ("ו", "Vau", "nail"), 16, "Taurus",
     "The Magus of the Eternal Gods",
     "Revelation through tradition, the teacher and the bridge between heaven and the seeker.",
     "Dogma, hollow orthodoxy, the letter of the teaching without its spirit."),
    (6, "the-lovers", "The Lovers", ("ז", "Zain", "sword"), 17, "Gemini",
     "The Children of the Voice; the Oracle of the Mighty Gods",
     "Union, the analysis that leads to synthesis, and the moral choice at the crossroads.",
     "Indecision, a union founded on weakness, temptation, choice avoided."),
    (7, "the-chariot", "The Chariot", ("ח", "Cheth", "fence"), 18, "Cancer",
     "The Child of the Powers of the Waters; the Lord of the Triumph of Light",
     "Triumph through the holding of opposing forces, the will armoured and advancing.",
     "Loss of control, conflict of forces, a triumph undone by pride."),
    (8, "strength", "Strength", ("ט", "Teth", "serpent"), 19, "Leo",
     "Daughter of the Flaming Sword",
     "The gentle mastery of instinct, spiritual force quietly governing the lion of passion.",
     "Brute force, domination by appetite, weakness disguised as control."),
    (9, "the-hermit", "The Hermit", ("י", "Yod", "hand"), 20, "Virgo",
     "The Magus of the Voice of Power, the Prophet of the Eternal",
     "The inner light carried into solitude, prudence, the patient and secret search.",
     "Isolation that avoids, a lamp hoarded, withdrawal mistaken for wisdom."),
    (10, "wheel-of-fortune", "Wheel of Fortune", ("כ", "Kaph", "palm"), 21, "Jupiter",
     "The Lord of the Forces of Life",
     "The turning of cycles, destiny in motion, the rhythm that raises and lowers.",
     "Resistance to change, ill fortune, being dragged by the wheel."),
    (11, "justice", "Justice", ("ל", "Lamed", "ox-goad"), 22, "Libra",
     "Daughter of the Lords of Truth; the Ruler of the Balance",
     "Equilibrium, the exact adjustment of forces, consequence and the law of the balance.",
     "Injustice, imbalance, severity without mercy, the scales falsified."),
    (12, "the-hanged-man", "The Hanged Man", ("מ", "Mem", "water"), 23, "Water",
     "The Spirit of the Mighty Waters",
     "Willing reversal and sacrifice, the world seen anew, redemption through surrender.",
     "Useless sacrifice, stagnation, attachment refusing to let go."),
    (13, "death", "Death", ("נ", "Nun", "fish"), 24, "Scorpio",
     "The Child of the Great Transformers; Lord of the Gate of Death",
     "Transformation, the necessary dissolution that clears the ground for new life.",
     "Stagnation, fear of change, decay resisted instead of released."),
    (14, "temperance", "Temperance", ("ס", "Samekh", "prop"), 25, "Sagittarius",
     "Daughter of the Reconcilers; the Bringer Forth of Life",
     "The reconciling flow, the tempering of opposites, the alchemy of the middle way.",
     "Imbalance, impatience, dissipation, the vital stream spilled."),
    (15, "the-devil", "The Devil", ("ע", "Ayin", "eye"), 26, "Capricorn",
     "The Lord of the Gates of Matter; the Child of the Forces of Time",
     "The magnetic force of matter and instinct; mirth, materiality, energy that binds when unconscious.",
     "Release from bondage, or a deeper enslavement to appetite and obsession."),
    (16, "the-tower", "The Tower", ("פ", "Peh", "mouth"), 27, "Mars",
     "The Lord of the Hosts of the Mighty",
     "Sudden upheaval, the lightning that breaks false structures and frees what they caged.",
     "Catastrophe resisted, a collapse delayed but coming, clinging to ruins."),
    (17, "the-star", "The Star", ("צ", "Tzaddi", "fish-hook"), 28, "Aquarius",
     "The Daughter of the Firmament; the Dweller between the Waters",
     "Hope and renewal, the waters of life freely poured, the star that orients after the dark.",
     "Despair, disillusion, hope clouded, the gift withheld."),
    (18, "the-moon", "The Moon", ("ק", "Qoph", "back of head"), 29, "Pisces",
     "The Ruler of Flux and Reflux; the Child of the Sons of the Mighty",
     "The realm of dream and instinct, illusion, the perilous nocturnal path of the soul.",
     "Deception conquering, fear, illusions taken for truth."),
    (19, "the-sun", "The Sun", ("ר", "Resh", "head"), 30, "the Sun",
     "The Lord of the Fire of the World",
     "Conscious life, clarity, vitality, the restored innocence of the lit world.",
     "Vanity, a clouded sun, false brilliance, joy only on the surface."),
    (20, "judgement", "Judgement", ("ש", "Shin", "tooth"), 31, "Fire / Spirit",
     "The Spirit of the Primal Fire",
     "The call to awaken, regeneration, the summons answered and the self reborn.",
     "Stagnation, a call refused, fear of decision, the trumpet unheard."),
    (21, "the-world", "The World", ("ת", "Tau", "cross"), 32, "Saturn",
     "The Great One of the Night of Time",
     "Completion, the Great Work accomplished, the cosmos harmonised and the journey closed.",
     "Incompletion, a goal almost reached, a cycle that fails to close."),
]

# ---- Suits, sephirot, worlds -----------------------------------------------
SUITS = [
    ("wands", "Wands", "Fire", "Atziluth (the Archetypal World)"),
    ("cups", "Cups", "Water", "Briah (the Creative World)"),
    ("swords", "Swords", "Air", "Yetzirah (the Formative World)"),
    ("pentacles", "Pentacles", "Earth", "Assiah (the Material World)"),
]
SEPHIRA = {2: "Chokmah", 3: "Binah", 4: "Chesed", 5: "Geburah", 6: "Tiphareth",
           7: "Netzach", 8: "Hod", 9: "Yesod", 10: "Malkuth"}
ACE_TITLE = {"Wands": "Root of the Powers of Fire", "Cups": "Root of the Powers of Water",
             "Swords": "Root of the Powers of Air", "Pentacles": "Root of the Powers of Earth"}
ACE_MEAN = {
    "Wands": ("The seed of all fire — pure energy, the spark of creation and will at its origin.",
              "Force misapplied, a beginning without direction."),
    "Cups": ("The seed of all water — the wellspring of love, joy, and the fertilising emotions.",
             "Feeling blocked at the source, an empty or overflowing cup."),
    "Swords": ("The seed of all air — the sword of mind and truth, force invoked for good or ill.",
               "The double-edged blade turned the wrong way; reason used to wound."),
    "Pentacles": ("The seed of all earth — the root of wealth, body, and material beginnings.",
                  "Materialism, a foundation laid on the wrong ground."),
}

# pip -> (suit -> (Lord-title, decan)); built from Book T
PIPS = {
    "Wands": {
        2: ("Lord of Dominion", "Mars in Aries", "Bold dominion and influence over others; authority established by will.", "Restlessness, a domineering edge, pride overreaching."),
        3: ("Lord of Established Strength", "Sun in Aries", "Established strength, enterprise realised, pride in work, help from others.", "Conceit, arrogance, strength resting on its laurels."),
        4: ("Lord of Perfected Work", "Venus in Aries", "Completion and rest after labour, harmony, the perfected work celebrated.", "Work unfinished, a foundation not yet stable."),
        5: ("Lord of Strife", "Saturn in Leo", "Competition, struggle, quarrels — the friction that sharpens.", "Pointless contradiction, complications, conflict for its own sake."),
        6: ("Lord of Victory", "Jupiter in Leo", "Victory after strife, success, recognition, good news arriving.", "Delay, apprehension, a triumph that breeds complacency."),
        7: ("Lord of Valour", "Mars in Leo", "Courage against the odds, holding one's ground from a position of advantage.", "Anxiety, yielding ground, valour spent on the wrong fight."),
        8: ("Lord of Swiftness", "Mercury in Sagittarius", "Swift action and messages, energy rushing toward its aim.", "Haste scattering force, stagnation, arrows loosed too soon."),
        9: ("Lord of Great Strength", "Moon in Sagittarius", "Strength held in reserve, resilience, recovery, readiness for one more stand.", "Obstinacy, exhaustion, defence become rigidity."),
        10: ("Lord of Oppression", "Saturn in Sagittarius", "Overload, burden, force used cruelly, the weight of too much carried.", "A burden set down, but treachery or collapse may follow."),
    },
    "Cups": {
        2: ("Lord of Love", "Venus in Cancer", "Love, harmony, union, mutual attraction freely given.", "False love, disunion, a bond cooling."),
        3: ("Lord of Abundance", "Mercury in Cancer", "Plenty, joy, celebration, the overflow shared among friends.", "Excess, a pleasure that cannot last."),
        4: ("Lord of Blended Pleasure", "Moon in Cancer", "Pleasure mixed with weariness, satiety, the apathy of having enough.", "A new feeling stirring, restlessness breaking the spell."),
        5: ("Lord of Loss in Pleasure", "Mars in Scorpio", "Disappointment within plenty, sorrow, the cup spilled.", "Hope returning, what remains gathered up."),
        6: ("Lord of Pleasure", "Sun in Scorpio", "Well-being, harmony, the sweet pleasure of memory and the past.", "Living in the past, nostalgia that holds one back."),
        7: ("Lord of Illusionary Success", "Venus in Scorpio", "Illusion, fantasy, deceptive success, intoxication with one's own visions.", "Clarity returning, will reasserted over fantasy."),
        8: ("Lord of Abandoned Success", "Saturn in Pisces", "Leaving behind what was won to seek a deeper meaning; withdrawal.", "Aimless drifting, abandonment without purpose."),
        9: ("Lord of Material Happiness", "Jupiter in Pisces", "The 'wish' card — contentment, physical well-being, fulfilment.", "Smugness, excess, satisfaction grown complacent."),
        10: ("Lord of Perfected Success", "Mars in Pisces", "Lasting happiness, harmony, the suit fulfilled in shared joy.", "Discord beneath a calm surface, a peace not quite real."),
    },
    "Swords": {
        2: ("Lord of Peace Restored", "Moon in Libra", "Truce, a balance held by tension, peace restored after conflict.", "Duplicity, the stalemate broken the wrong way."),
        3: ("Lord of Sorrow", "Saturn in Libra", "Heartbreak, grief, separation — sorrow that clears the air.", "Pain that lingers, a slow and grudging recovery."),
        4: ("Lord of Rest from Strife", "Jupiter in Libra", "Repose, recovery, retreat, the rest that heals.", "Restlessness, a return to the fray too soon."),
        5: ("Lord of Defeat", "Venus in Aquarius", "Defeat, loss, dishonour, the costs of winning at any price.", "An empty victory, resentment that outlives the fight."),
        6: ("Lord of Earned Success", "Mercury in Aquarius", "Passage from trouble toward calmer water, progress earned.", "A transition stalled, the far shore not yet reached."),
        7: ("Lord of Unstable Effort", "Moon in Aquarius", "Cunning, a partial and unreliable success, slipping away with the prize.", "Exposure, the plan undone, what was taken returned."),
        8: ("Lord of Shortened Force", "Jupiter in Gemini", "Restriction, constraint, force turned against itself, indecision.", "Release, the bonds loosened, freedom found within limits."),
        9: ("Lord of Despair and Cruelty", "Mars in Gemini", "Anguish, nightmare, cruelty, the long night of despair.", "The worst passing, a first grey light of dawn."),
        10: ("Lord of Ruin", "Sun in Gemini", "Ruin, the end of an illusion, the failure of force, rock bottom.", "Recovery — from here the only way is up."),
    },
    "Pentacles": {
        2: ("Lord of Harmonious Change", "Jupiter in Capricorn", "Balancing flux, juggling demands, graceful adaptation to change.", "Imbalance, disorder, too many things in the air."),
        3: ("Lord of Material Works", "Mars in Capricorn", "Skilled work, craft, building, recognition of one's ability.", "Mediocrity, careless work, skill not yet earned."),
        4: ("Lord of Earthly Power", "Sun in Capricorn", "Security, holding, possession, the consolidation of gains.", "Hoarding, blockage, holding so tight nothing moves."),
        5: ("Lord of Material Trouble", "Mercury in Taurus", "Hardship, want, loss, the cold outside the lit window.", "Recovery beginning, help arriving, the worst behind."),
        6: ("Lord of Material Success", "Moon in Taurus", "Generosity, fair exchange, success that is shared.", "Strings attached, an unequal gift, charity that controls."),
        7: ("Lord of Success Unfulfilled", "Saturn in Taurus", "Patience, the pause before harvest, growth not yet realised.", "Impatience, wasted effort, a crop abandoned too soon."),
        8: ("Lord of Prudence", "Sun in Virgo", "Diligence, skill cultivated, the careful work of the apprentice.", "Hollow effort, perfectionism, skill without soul."),
        9: ("Lord of Material Gain", "Venus in Virgo", "Solitary plenty, refinement, material gain quietly enjoyed.", "Dependence, hollow luxury, gain that isolates."),
        10: ("Lord of Wealth", "Mercury in Virgo", "Lasting wealth, family, inheritance, completion in the world of matter.", "Stagnation, the burden of riches, a legacy that weighs."),
    },
}

# Courts: RWS rank (number) -> GD rank, element-of, ruling span per suit
# 11 Page->Princess(Earth), 12 Knight->Knight(Fire), 13 Queen->Queen(Water), 14 King->Prince(Air)
COURT_MAP = {
    11: ("Page", "Princess", "Earth", None),
    12: ("Knight", "Knight", "Fire", {"Wands": "21° Scorpio – 20° Sagittarius", "Cups": "21° Aquarius – 20° Pisces",
                                       "Swords": "21° Taurus – 20° Gemini", "Pentacles": "21° Leo – 20° Virgo"}),
    13: ("Queen", "Queen", "Water", {"Wands": "21° Pisces – 20° Aries", "Cups": "21° Gemini – 20° Cancer",
                                      "Swords": "21° Virgo – 20° Libra", "Pentacles": "21° Sagittarius – 20° Capricorn"}),
    14: ("King", "Prince", "Air", {"Wands": "21° Cancer – 20° Leo", "Cups": "21° Libra – 20° Scorpio",
                                   "Swords": "21° Capricorn – 20° Aquarius", "Pentacles": "21° Aries – 20° Taurus"}),
}
SUIT_TEMPER = {"Wands": "ardent and swift", "Cups": "tender and dreaming",
               "Swords": "keen and restless", "Pentacles": "steady and enduring"}
RANK_ROLE = {
    "Knight": "headlong, active, the mounted warrior who charges and is gone",
    "Queen": "receptive mastery, magnetic and deep, the power held within",
    "Prince": "the intellect of the suit in action — swift, reasoning, decisive",
    "Princess": "the suit made earth — daring, brilliant, the herald and the throne",
}


def heb_block(letter, translit, meaning, path, astro):
    return (f"**Hebrew letter:** {letter} ({translit}, '{meaning}') — path {path} on the Tree of Life.\n\n"
            f"**Attribution:** {astro}.\n\n"
            f"*(Classical Golden Dawn / Book T attribution. Modern decks add an outer planet — "
            f"Uranus, Neptune, or Pluto — to the three elemental trumps.)*")


items = []
so = 0
for num, slug, name, (lt, tr, mn), path, astro, gdt, up, rev in MAJORS:
    u = IMG_MAJOR.get(num)
    items.append({
        "id": f"major-{num:02d}-{slug}", "name": f"{num} — {name}", "sort_order": so,
        "category": "major-arcana", "level": 1,
        "keywords": [name.lower().replace("the ", ""), "major arcana", "golden dawn", tr.lower(), astro.lower()],
        "image_url": u,
        "metadata": {
            "arcana": "major", "number": num, "hebrew_letter": lt, "hebrew_translit": tr,
            "tree_path": path, "attribution": astro, "golden_dawn_title": gdt,
            "illustrations": [{"url": u, "artist": "Pamela Colman Smith", "artist_dates": "1878–1951",
                               "edition": "Rider-Waite-Smith, 1909 (public domain imagery)",
                               "scene": name, "license": "Public Domain", "is_primary": True}] if u else [],
        },
        "sections": {
            "Golden Dawn Title": f"*{gdt}*",
            "Correspondences": heb_block(lt, tr, mn, path, astro),
            "Divinatory Meaning": up,
            "Reversed / Ill-Dignified": rev,
        },
    })
    so += 1

for sid, sdisp, element, world in SUITS:
    # Ace
    u = IMG_MINOR.get((sid, 1))
    up, rev = ACE_MEAN[sdisp]
    items.append({
        "id": f"{sid}-ace", "name": f"Ace of {sdisp}", "sort_order": so,
        "category": f"suit-{sid}", "level": 1,
        "keywords": [sdisp.lower(), element.lower(), "ace", "minor arcana", "golden dawn"],
        "image_url": u,
        "metadata": {"arcana": "minor", "suit": sdisp, "element": element, "rank": "Ace",
                     "golden_dawn_title": ACE_TITLE[sdisp], "sephirah": "Kether", "world": world,
                     "illustrations": [{"url": u, "artist": "Pamela Colman Smith", "artist_dates": "1878–1951",
                                        "edition": "Rider-Waite-Smith, 1909 (public domain imagery)",
                                        "scene": f"Ace of {sdisp}", "license": "Public Domain", "is_primary": True}] if u else []},
        "sections": {
            "Golden Dawn Title": f"*{ACE_TITLE[sdisp]}*",
            "Correspondences": f"**Kether** in {world}. The Ace is the root and seed of the whole suit, "
                               f"the pure power of {element} before it divides. It rules, with its court, "
                               f"one quadrant of the heavens.",
            "Divinatory Meaning": up,
            "Reversed / Ill-Dignified": rev,
        },
    })
    so += 1
    # Pips 2-10
    for n in range(2, 11):
        title, decan, up, rev = PIPS[sdisp][n]
        u = IMG_MINOR.get((sid, n))
        items.append({
            "id": f"{sid}-{n:02d}", "name": f"{['','','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten'][n]} of {sdisp}",
            "sort_order": so, "category": f"suit-{sid}", "level": 1,
            "keywords": [sdisp.lower(), element.lower(), decan.lower(), "minor arcana", "decan", "golden dawn"],
            "image_url": u,
            "metadata": {"arcana": "minor", "suit": sdisp, "element": element, "number": n,
                         "golden_dawn_title": title, "decan": decan, "sephirah": SEPHIRA[n], "world": world,
                         "illustrations": [{"url": u, "artist": "Pamela Colman Smith", "artist_dates": "1878–1951",
                                            "edition": "Rider-Waite-Smith, 1909 (public domain imagery)",
                                            "scene": f"{n} of {sdisp}", "license": "Public Domain", "is_primary": True}] if u else []},
            "sections": {
                "Golden Dawn Title": f"*{title}*",
                "Correspondences": f"**Decan:** {decan} (the {['','','1st','2nd','3rd','1st','2nd','3rd','1st','2nd','3rd'][n]} "
                                   f"decanate of its sign).\n\n**Sephirah:** {SEPHIRA[n]} in {world}.",
                "Divinatory Meaning": up,
                "Reversed / Ill-Dignified": rev,
            },
        })
        so += 1
    # Courts
    for rws_num in (12, 13, 14, 11):  # Knight, Queen, King(Prince), Page(Princess) — image order flexible
        rws_rank, gd_rank, court_elem, spans = COURT_MAP[rws_num]
        u = IMG_MINOR.get((sid, rws_num))
        span = spans[sdisp] if spans else "one quadrant of the heavens around the North Pole (with the Ace)"
        eie = f"{court_elem} of {element}"
        role = RANK_ROLE[gd_rank]
        items.append({
            "id": f"{sid}-{rws_rank.lower()}", "name": f"{rws_rank} of {sdisp}",
            "sort_order": so, "category": f"suit-{sid}", "level": 1,
            "keywords": [sdisp.lower(), element.lower(), rws_rank.lower(), gd_rank.lower(), "court card", "golden dawn"],
            "image_url": u,
            "metadata": {"arcana": "minor", "suit": sdisp, "element": element, "rank": rws_rank,
                         "golden_dawn_rank": gd_rank, "element_in_element": eie, "rules": span, "court": True,
                         "illustrations": [{"url": u, "artist": "Pamela Colman Smith", "artist_dates": "1878–1951",
                                            "edition": "Rider-Waite-Smith, 1909 (public domain imagery)",
                                            "scene": f"{rws_rank} of {sdisp}", "license": "Public Domain", "is_primary": True}] if u else []},
            "sections": {
                "Golden Dawn Rank": f"RWS **{rws_rank} of {sdisp}** = Golden Dawn **{gd_rank} of {sdisp}** — "
                                    f"**{eie}**.",
                "Correspondences": f"Rules {span}. As {eie}, this court is the {court_elem.lower()} aspect of "
                                   f"a {SUIT_TEMPER[sdisp]} suit.",
                "Divinatory Meaning": f"{role.capitalize()}, coloured by the {SUIT_TEMPER[sdisp]} nature of "
                                      f"{sdisp}. A person or force of this temperament, or the call to embody it.",
                "Reversed / Ill-Dignified": f"The {eie} energy turned excessive, immature, or against itself.",
            },
        })
        so += 1

# ---- Emergences -------------------------------------------------------------
all_ids = {it["id"] for it in items}
emgs = [
    ("emg-majors", "The 22 Keys — The Paths of the Tree", [it["id"] for it in items if it["category"] == "major-arcana"],
     IMG_MAJOR.get(21),
     {"About the Keys": "In the Golden Dawn the 22 trumps are the 22 paths joining the ten Sephiroth on the "
      "Tree of Life, each carrying a Hebrew letter and an astrological force. This is the heart of the "
      "tradition: the tarot as a map of the descent and return of spirit. Note the Golden Dawn order — "
      "Strength at VIII (Leo), Justice at XI (Libra) — the swap from the Marseille that Waite and Smith kept.",
      "How to Use": "Read the trumps as paths, not just pictures: each is a stage and a doorway on the Tree."}),
    ("emg-decans", "The 36 Decans — Lords of the Minor Arcana",
     [it["id"] for it in items if it["category"].startswith("suit-") and it["metadata"].get("number")],
     IMG_MINOR.get(("wands", 2)),
     {"About the Decans": "The small cards 2–10 map to the 36 decans — the ten-degree divisions of the "
      "zodiac — each ruled by a planet and bearing a Book T title (the 'Lord of ...'). The number gives the "
      "Sephirah, the suit gives the World. This is what lets a Golden Dawn reader date and place a card in "
      "the wheel of the year.",
      "How to Use": "Read each pip as Planet-in-Sign within a Sephirah: the decan is the weather, the "
      "Sephirah the depth, the suit the world."}),
]
for sid, sdisp, element, world in SUITS:
    kids = [it["id"] for it in items if it["category"] == f"suit-{sid}"]
    emgs.append((f"emg-suit-{sid}", f"Suit of {sdisp} — {element} ({world.split(' ')[0]})", kids,
                 IMG_MINOR.get((sid, 5)),
                 {"About this Suit": f"The {sdisp}, suit of {element}, unfolding through the Sephiroth in "
                  f"{world}. From the Ace (Kether, the root) down to the Ten (Malkuth, the suit made fully "
                  f"manifest), with the four courts as {element}'s inner elements.",
                  "How to Use": f"Follow the suit from Ace to Ten to watch {element} descend from pure "
                  f"potential into the fully realised world."}))
for eid, ename, kids, image_url, sections in emgs:
    kids = [k for k in kids if k in all_ids]
    items.append({"id": eid, "name": ename, "sort_order": so, "category": "emergence", "level": 2,
                  "composite_of": kids, "relationship_type": "emergence",
                  "image_url": image_url, "metadata": {}, "sections": sections})
    so += 1

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0", "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "S.L. MacGregor Mathers / Hermetic Order of the Golden Dawn", "date": "1888",
             "note": "Book T (Liber T) — the correspondence system: paths, decans, Sephiroth, titles"},
            {"name": "Pamela Colman Smith & A.E. Waite", "date": "1909",
             "note": "Rider-Waite-Smith imagery (public domain), the most famous Golden-Dawn-derived deck"},
            {"name": "Wikimedia Commons", "date": "public domain", "note": "RWS card scans"},
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar architecture; correspondences compiled from Book T"},
        ],
    },
    "name": "Golden Dawn Tarot — Book T with Rider-Waite-Smith Imagery",
    "description": (
        "The Golden Dawn version of the Rider-Waite tarot — Pamela Colman Smith's familiar imagery carried "
        "by the full correspondence system of the Hermetic Order of the Golden Dawn, set down in Book T "
        "(Liber T) by S.L. MacGregor Mathers in 1888. Waite and Smith were both Golden Dawn initiates; their "
        "1909 deck is the tradition's most famous visual expression, but the published deck strips out the "
        "esoteric scaffolding. This grammar puts it back.\n\n"
        "Every card is built precisely within the tradition. The 22 trumps carry their Hebrew letter, their "
        "path on the Tree of Life, their astrological attribution, and their Book T title (the Fool is 'The "
        "Spirit of Æther'; Strength is 'Daughter of the Flaming Sword'). The small cards 2–10 carry the 36 "
        "decans — Planet in Sign — their Sephirah and World, and their 'Lord of ...' titles (Two of Wands is "
        "the 'Lord of Dominion', Mars in Aries). The Aces are the Roots of the Powers of the elements; the "
        "courts are mapped to the Golden Dawn's Knight / Queen / Prince / Princess and their "
        "element-in-element nature.\n\n"
        "Note the Golden Dawn order, which Waite kept: Strength at VIII (Leo) and Justice at XI (Libra), "
        "swapped from the older Marseille. Where modern writers add an outer planet (Uranus, Neptune, Pluto) "
        "to the three elemental trumps, the classical Book T attribution is given and the overlay noted.\n\n"
        "PUBLIC DOMAIN ILLUSTRATION REFERENCES: Pamela Colman Smith, Rider-Waite-Smith Tarot, 1909 "
        "(Wikimedia Commons) — the canonical illustrated minors. Correspondence text compiled from the "
        "public-domain Book T / Liber T (Mathers; pub. Regardie, 'The Golden Dawn')."
    ),
    "grammar_type": "tarot",
    "creator_name": "PlayfulProcess",
    "creator_link": "https://recursive.eco",
    "cover_image_url": IMG_MAJOR.get(0),
    "tags": ["tarot", "golden-dawn", "book-t", "rider-waite-smith", "kabbalah", "decans",
             "astrology", "esoteric", "public-domain", "tree-of-life"],
    "roots": ["western-esoteric", "mysticism"],
    "shelves": ["wonder", "mirror"],
    "lineages": ["Andreotti"],
    "worldview": "esoteric",
    "is_published": False,
    "items": items,
}

os.makedirs(OUT_DIR, exist_ok=True)
out_path = os.path.join(OUT_DIR, "grammar.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)
print(f"Wrote {out_path}")
print(f"  items: {len(items)}  with image_url: {sum(1 for it in items if it.get('image_url'))}")
