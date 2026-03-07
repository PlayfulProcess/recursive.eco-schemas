#!/usr/bin/env python3
"""
Parse four Greek religion/ritual seed files into grammars:
1. Five Stages of Greek Religion (Gilbert Murray, Gutenberg #30250)
2. The Eleusinian Mysteries and Rites (Dudley Wright, Gutenberg #35087)
3. Ancient Art and Ritual (Jane Ellen Harrison, Gutenberg #17087)
4. Myths of Greece and Rome (Otto Seemann, Gutenberg #61901)
"""
import json, re, os

def read_seed(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    start = text.find("\n", start) + 1
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    return text[start:end].strip()

def truncate(text, limit=2800):
    if len(text) <= limit:
        return text
    bp = text.rfind(".", 0, limit - 100)
    if bp == -1:
        bp = limit - 100
    remaining = len(text[bp:].split())
    return text[:bp+1] + f"\n\n[Text continues for approximately {remaining} more words...]"

def strip_footnotes(text):
    """Remove [123:1] style footnote markers and footnote blocks."""
    text = re.sub(r'\[\d+:\d+\]', '', text)
    text = re.sub(r'\[Illustration[^\]]*\]', '', text)
    return text

def clean_text(text):
    """Clean up text: strip footnotes, normalize whitespace."""
    text = strip_footnotes(text)
    # Remove _italic_ markers
    text = re.sub(r'_([^_]+)_', r'\1', text)
    # Remove =bold= markers
    text = re.sub(r'=([^=]+)=', r'\1', text)
    # Collapse excessive blank lines
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    return text.strip()

def write_grammar(grammar, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)
    items = grammar['items']
    ids = [i['id'] for i in items]
    dupes = [x for x in ids if ids.count(x) > 1]
    bad_refs = [(i['id'], r) for i in items for r in i.get('composite_of', []) if r not in ids]
    orders = [i['sort_order'] for i in items]
    print(f"\n{path}:")
    print(f"  Items: {len(items)}, L1: {sum(1 for i in items if i['level']==1)}, L2: {sum(1 for i in items if i['level']==2)}, L3: {sum(1 for i in items if i['level']==3)}")
    print(f"  Sections: {sum(len(i.get('sections',{})) for i in items)}")
    print(f"  Duplicate IDs: {dupes}")
    print(f"  Bad refs: {bad_refs}")
    print(f"  Sort orders sequential: {orders == list(range(1, len(items)+1))}")

def base_commons():
    return {
        "schema_version": "1.0",
        "license": "CC-BY-SA-4.0"
    }

def base_meta():
    return {
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "roots": ["western-philosophy", "classical-antiquity"],
        "shelves": ["wisdom"],
        "lineages": ["Shrei"],
        "worldview": "animist"
    }

# ═══════════════════════════════════════════════════════════════════
# 1. FIVE STAGES OF GREEK RELIGION
# ═══════════════════════════════════════════════════════════════════

def parse_five_stages():
    body = read_seed("seeds/five-stages-greek-religion.txt")
    lines = body.split("\n")

    # Chapter definitions: (roman, title, id, name)
    chapters = [
        ("I", "SATURNIA REGNA", "ch1-saturnia-regna", "I. Saturnia Regna"),
        ("II", "THE OLYMPIAN CONQUEST", "ch2-olympian-conquest", "II. The Olympian Conquest"),
        ("III", "THE GREAT SCHOOLS OF THE FOURTH CENTURY, B. C.", "ch3-great-schools", "III. The Great Schools of the Fourth Century B.C."),
        ("IV", "THE FAILURE OF NERVE", "ch4-failure-of-nerve", "IV. The Failure of Nerve"),
        ("V", "THE LAST PROTEST", "ch5-last-protest", "V. The Last Protest"),
    ]

    # Also parse prefaces and appendix
    preface_sections = [
        ("PREFACE TO THE THIRD EDITION", "preface-third", "Preface to the Third Edition"),
        ("PREFACE TO THE SECOND EDITION", "preface-second", "Preface to the Second Edition"),
        ("PREFACE TO THE FIRST EDITION", "preface-first", "Preface to the First Edition"),
    ]

    # Find line numbers for each section
    def find_line(heading):
        for i, line in enumerate(lines):
            if line.strip() == heading:
                return i
        return -1

    # Build items
    items = []
    sort_order = 1

    # Parse prefaces
    pref_ids = []
    for heading, sid, name in preface_sections:
        start = find_line(heading)
        if start == -1:
            continue
        # Find end: next preface or chapter I
        end = len(lines)
        for h2, _, _ in preface_sections:
            ln = find_line(h2)
            if ln > start:
                end = min(end, ln)
                break
        # Also check for chapter I marker
        ch1_line = find_line("SATURNIA REGNA")
        if ch1_line > start:
            end = min(end, ch1_line - 5)

        content = "\n".join(lines[start+1:end]).strip()
        content = clean_text(content)
        content = truncate(content)

        items.append({
            "id": sid,
            "name": name,
            "sort_order": sort_order,
            "category": "preface",
            "level": 1,
            "sections": {"Preface": content},
            "keywords": ["preface", "introduction"],
            "metadata": {}
        })
        pref_ids.append(sid)
        sort_order += 1

    # Parse chapters
    ch_ids = []
    for i, (roman, title, sid, name) in enumerate(chapters):
        # Find the roman numeral line, then the title line
        title_line = find_line(title)
        if title_line == -1:
            print(f"  WARNING: Could not find chapter '{title}'")
            continue

        start = title_line
        # Find end: next chapter title or Sallustius appendix or end
        end = len(lines)
        for j in range(i + 1, len(chapters)):
            next_title_line = find_line(chapters[j][1])
            if next_title_line > 0:
                end = next_title_line - 5
                break

        # Check for BIBLIOGRAPHICAL NOTE or SALLUSTIUS
        for marker in ["BIBLIOGRAPHICAL NOTE", "     SALLUSTIUS"]:
            ml = find_line(marker) if marker.strip() == marker else -1
            if ml == -1:
                for k, line in enumerate(lines):
                    if marker in line and k > start:
                        ml = k
                        break
            if ml > start and ml < end:
                end = ml - 2

        content = "\n".join(lines[start+1:end]).strip()
        content = clean_text(content)
        content = truncate(content)

        items.append({
            "id": sid,
            "name": name,
            "sort_order": sort_order,
            "category": "chapter",
            "level": 1,
            "sections": {"Chapter": content},
            "keywords": [w.lower() for w in title.split() if len(w) > 3],
            "metadata": {}
        })
        ch_ids.append(sid)
        sort_order += 1

    # Parse Sallustius appendix
    sall_start = -1
    for i, line in enumerate(lines):
        if "SALLUSTIUS" in line and i > 5000:
            sall_start = i
            break

    if sall_start > 0:
        # Find end of Sallustius (before footnotes or end)
        sall_end = len(lines)
        for i in range(sall_start + 10, len(lines)):
            if "Footnote" in lines[i] and i > sall_start + 100:
                sall_end = i
                break
            # End at the last numbered section
            if lines[i].strip().startswith("XXI.") or "End of the Project" in lines[i]:
                sall_end = i + 20
                break

        sall_text = "\n".join(lines[sall_start:sall_end]).strip()
        sall_text = clean_text(sall_text)
        sall_text = truncate(sall_text)

        items.append({
            "id": "appendix-sallustius",
            "name": "Appendix: Sallustius - On the Gods and the World",
            "sort_order": sort_order,
            "category": "appendix",
            "level": 1,
            "sections": {"Text": sall_text},
            "keywords": ["sallustius", "neoplatonism", "theology", "gods", "appendix"],
            "metadata": {}
        })
        ch_ids.append("appendix-sallustius")
        sort_order += 1

    # L2: Thematic groupings
    l2_groups = [
        ("theme-primitive-religion", "Primitive and Pre-Olympian Religion",
         "The earliest layers of Greek religion: the worship of Themis, the Year-Spirit, fertility rites, and the tribal customs that preceded the Olympian gods. These practices survived beneath the official religion throughout antiquity.",
         [sid for sid in ch_ids if "saturnia" in sid or "preface" in sid],
         ["primitive", "fertility", "ritual", "year-spirit"]),
        ("theme-olympian-era", "The Olympian Achievement",
         "The emergence of the Olympian gods as moral and aesthetic ideals, and the philosophical schools that refined Greek religious thought into systematic ethics and metaphysics.",
         [sid for sid in ch_ids if "olympian" in sid or "great-schools" in sid],
         ["olympian", "philosophy", "ethics", "classical"]),
        ("theme-decline-transformation", "Decline and Transformation",
         "The loss of nerve in the Hellenistic age, the rise of astrology, mystery religions, and salvation cults, and the final pagan protest against Christianity.",
         [sid for sid in ch_ids if "failure" in sid or "last-protest" in sid or "sallustius" in sid],
         ["hellenistic", "mystery-religions", "gnosticism", "christianity"]),
    ]

    for gid, gname, about, refs, kws in l2_groups:
        valid_refs = [r for r in refs if r in [it['id'] for it in items]]
        if not valid_refs:
            # Use chapter refs
            valid_refs = [r for r in ch_ids if r in [it['id'] for it in items]][:2]
        items.append({
            "id": gid,
            "name": gname,
            "sort_order": sort_order,
            "category": "theme",
            "level": 2,
            "composite_of": valid_refs,
            "relationship_type": "emergence",
            "sections": {
                "About": about,
                "For Readers": "Read these chapters together to trace how Greek religion evolved from earth-bound fertility cults through the clarity of Olympian theology to the anxious spirituality of the Hellenistic world."
            },
            "keywords": kws,
            "metadata": {}
        })
        sort_order += 1

    # L3: Meta
    items.append({
        "id": "meta-evolution-of-religion",
        "name": "The Evolution of Greek Religious Consciousness",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "composite_of": [g[0] for g in l2_groups],
        "relationship_type": "emergence",
        "sections": {
            "About": "Murray's central thesis: Greek religion was not a fixed system but a living organism that evolved through five distinct stages, from primitive earth-worship through Olympian rationalism to Hellenistic mysticism. Each stage preserved elements of the previous ones, creating layers of belief that coexisted uneasily. The final stage saw Christianity absorb and transform the Greek religious inheritance.",
            "For Readers": "This grammar traces the full arc of Western religious evolution from animism to monotheism. Murray's sympathetic treatment of each stage invites readers to see religion not as truth vs. superstition, but as humanity's ongoing attempt to make sense of existence."
        },
        "keywords": ["evolution", "religion", "consciousness", "western-thought"],
        "metadata": {}
    })
    sort_order += 1

    grammar = {
        "_grammar_commons": {
            **base_commons(),
            "attribution": [
                {"name": "Gilbert Murray", "date": "1925", "note": "Five Stages of Greek Religion, third edition"},
                {"name": "Project Gutenberg", "date": "2009", "note": "eBook #30250"}
            ]
        },
        "name": "Five Stages of Greek Religion",
        "description": "Gilbert Murray's classic study of the evolution of Greek religious thought, from primitive fertility rites through Olympian theology, classical philosophy, Hellenistic mysticism, and the final pagan resistance to Christianity. A foundational text in the history of religion.\n\nSource: Project Gutenberg eBook #30250 (https://www.gutenberg.org/ebooks/30250)",
        **base_meta(),
        "tags": ["greek-religion", "philosophy", "ritual", "paganism", "history-of-religion"],
        "items": items
    }

    write_grammar(grammar, "grammars/five-stages-greek-religion/grammar.json")

# ═══════════════════════════════════════════════════════════════════
# 2. THE ELEUSINIAN MYSTERIES AND RITES
# ═══════════════════════════════════════════════════════════════════

def parse_eleusinian():
    body = read_seed("seeds/eleusinian-mysteries.txt")
    lines = body.split("\n")

    def find_line(heading):
        for i, line in enumerate(lines):
            if line.strip() == heading:
                return i
        return -1

    # Sections to extract
    sections_def = [
        ("PREFACE", "preface", "Preface", "preface"),
        ("INTRODUCTION BY THE REV. J. FORT NEWTON, D.LITT., D.D.,", "introduction", "Introduction", "introduction"),
        ("THE ELEUSINIAN LEGEND", "ch1-eleusinian-legend", "I. The Eleusinian Legend", "chapter"),
        ("THE RITUAL OF THE MYSTERIES", "ch2-ritual-of-mysteries", "II. The Ritual of the Mysteries", "chapter"),
        ("PROGRAMME OF THE GREATER MYSTERIES", "ch3-greater-mysteries", "III. Programme of the Greater Mysteries", "chapter"),
        ("THE INITIATORY RITES", "ch4-initiatory-rites", "IV. The Initiatory Rites", "chapter"),
        ("THEIR MYSTICAL SIGNIFICANCE", "ch5-mystical-significance", "V. Their Mystical Significance", "chapter"),
        ("BIBLIOGRAPHY", "bibliography", "Bibliography", "appendix"),
    ]

    items = []
    sort_order = 1

    for idx, (heading, sid, name, cat) in enumerate(sections_def):
        start = find_line(heading)
        if start == -1:
            # Try partial match
            for i, line in enumerate(lines):
                if heading[:20] in line and i > 50:
                    start = i
                    break
        if start == -1:
            print(f"  WARNING: Could not find '{heading}'")
            continue

        # Find end
        end = len(lines)
        for j in range(idx + 1, len(sections_def)):
            next_start = find_line(sections_def[j][0])
            if next_start == -1:
                for k, line in enumerate(lines):
                    if sections_def[j][0][:20] in line and k > start:
                        next_start = k
                        break
            if next_start > start:
                end = next_start - 2
                break

        content = "\n".join(lines[start+1:end]).strip()
        content = clean_text(content)
        content = truncate(content)

        section_name = "Chapter" if cat == "chapter" else cat.title()
        items.append({
            "id": sid,
            "name": name,
            "sort_order": sort_order,
            "category": cat,
            "level": 1,
            "sections": {section_name: content},
            "keywords": [w.lower() for w in name.split() if len(w) > 3 and w not in ("The", "Their")],
            "metadata": {}
        })
        sort_order += 1

    # L2: Thematic groups
    ch_ids = [i['id'] for i in items]
    l2_groups = [
        ("theme-myth-and-history", "Myth and Historical Context",
         "The mythological foundation of the Eleusinian Mysteries in the story of Demeter and Persephone, and the historical development of the ritual practices over centuries.",
         [sid for sid in ch_ids if "legend" in sid or "preface" in sid or "introduction" in sid],
         ["demeter", "persephone", "myth", "history"]),
        ("theme-ritual-practice", "Ritual Practice and Ceremony",
         "The detailed programme of the Greater Mysteries: the processions, purifications, sacrifices, and dramatic performances that initiates experienced over ten days of sacred time.",
         [sid for sid in ch_ids if "ritual" in sid or "greater" in sid or "initiatory" in sid],
         ["ritual", "initiation", "ceremony", "procession"]),
        ("theme-inner-meaning", "Inner Meaning and Spiritual Teaching",
         "The deeper mystical significance of the Mysteries: the soul's descent and return, death as initiation, and the promise of a blessed afterlife for those who had seen the sacred things.",
         [sid for sid in ch_ids if "mystical" in sid or "initiatory" in sid],
         ["mysticism", "soul", "death", "rebirth", "afterlife"]),
    ]

    for gid, gname, about, refs, kws in l2_groups:
        valid_refs = [r for r in refs if r in ch_ids]
        items.append({
            "id": gid,
            "name": gname,
            "sort_order": sort_order,
            "category": "theme",
            "level": 2,
            "composite_of": valid_refs,
            "relationship_type": "emergence",
            "sections": {
                "About": about,
                "For Readers": "These chapters illuminate different facets of the most famous mystery cult in the ancient world. Read them to understand how outer ritual and inner transformation were woven together."
            },
            "keywords": kws,
            "metadata": {}
        })
        sort_order += 1

    # L3
    items.append({
        "id": "meta-mysteries",
        "name": "The Sacred Secret: Death and Rebirth at Eleusis",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "composite_of": [g[0] for g in l2_groups],
        "relationship_type": "emergence",
        "sections": {
            "About": "For nearly two thousand years, the Eleusinian Mysteries offered initiates a direct experience of the cycle of death and rebirth. Rooted in the myth of Demeter's grief and Persephone's return, the rites transformed participants through fasting, procession, darkness, terror, and final revelation. The secret was never betrayed; what remains is the testimony of those who emerged changed. Wright's study reconstructs what can be known of this transformative tradition.",
            "For Readers": "The Eleusinian Mysteries stand at the root of Western esoteric tradition. This grammar offers a window into a religious experience that shaped Plato, Cicero, and Marcus Aurelius, and whose echoes persist in every tradition that promises illumination through ordeal."
        },
        "keywords": ["eleusis", "initiation", "death-rebirth", "mystery-tradition"],
        "metadata": {}
    })

    grammar = {
        "_grammar_commons": {
            **base_commons(),
            "attribution": [
                {"name": "Dudley Wright", "date": "1919", "note": "The Eleusinian Mysteries and Rites"},
                {"name": "Project Gutenberg", "date": "2011", "note": "eBook #35087"}
            ]
        },
        "name": "The Eleusinian Mysteries and Rites",
        "description": "Dudley Wright's study of the most famous mystery cult of the ancient world: the Eleusinian Mysteries sacred to Demeter and Persephone. Covers the founding myth, ritual programme, initiatory rites, and mystical significance of a tradition that endured for nearly two millennia.\n\nSource: Project Gutenberg eBook #35087 (https://www.gutenberg.org/ebooks/35087)",
        **base_meta(),
        "tags": ["mysteries", "greek-religion", "ritual", "initiation", "esoteric"],
        "items": items
    }

    write_grammar(grammar, "grammars/eleusinian-mysteries/grammar.json")

# ═══════════════════════════════════════════════════════════════════
# 3. ANCIENT ART AND RITUAL
# ═══════════════════════════════════════════════════════════════════

def parse_ancient_art():
    body = read_seed("seeds/ancient-art-ritual.txt")
    lines = body.split("\n")

    def find_line(heading):
        for i, line in enumerate(lines):
            if line.strip() == heading:
                return i
        return -1

    # Chapters from the TOC
    chapter_defs = [
        ("CHAPTER I", "ART AND RITUAL", "ch1-art-and-ritual", "I. Art and Ritual"),
        ("CHAPTER II", "PRIMITIVE RITUAL: PANTOMIMIC DANCES", "ch2-pantomimic-dances", "II. Primitive Ritual: Pantomimic Dances"),
        ("CHAPTER III", "SEASONAL RITES: THE SPRING FESTIVAL", "ch3-spring-festival", "III. Seasonal Rites: The Spring Festival"),
        ("CHAPTER IV", "THE SPRING FESTIVAL IN GREECE", "ch4-spring-festival-greece", "IV. The Spring Festival in Greece"),
        ("CHAPTER V", "TRANSITION FROM RITUAL TO ART: THE DROMENON (\"THING DONE\") AND THE DRAMA", "ch5-dromenon-and-drama", "V. Transition from Ritual to Art"),
        ("CHAPTER VI", "GREEK SCULPTURE: THE PANATHENAIC FRIEZE AND THE APOLLO BELVEDERE", "ch6-greek-sculpture", "VI. Greek Sculpture"),
        ("CHAPTER VII", "RITUAL, ART AND LIFE", "ch7-ritual-art-life", "VII. Ritual, Art and Life"),
    ]

    items = []
    sort_order = 1

    # Parse prefatory note
    pref_start = find_line("PREFATORY NOTE")
    if pref_start > 0:
        ch1_start = find_line("CHAPTER I")
        content = "\n".join(lines[pref_start+1:ch1_start-3]).strip()
        content = clean_text(content)
        content = truncate(content)
        items.append({
            "id": "prefatory-note",
            "name": "Prefatory Note",
            "sort_order": sort_order,
            "category": "preface",
            "level": 1,
            "sections": {"Preface": content},
            "keywords": ["preface", "introduction", "ritual", "art"],
            "metadata": {}
        })
        sort_order += 1

    # Parse chapters
    ch_ids = []
    for idx, (ch_marker, title, sid, name) in enumerate(chapter_defs):
        start = find_line(ch_marker)
        if start == -1:
            print(f"  WARNING: Could not find '{ch_marker}'")
            continue

        # Find end
        end = len(lines)
        for j in range(idx + 1, len(chapter_defs)):
            next_start = find_line(chapter_defs[j][0])
            if next_start > start:
                end = next_start - 3
                break

        # Also check for BIBLIOGRAPHY or INDEX
        for marker in ["BIBLIOGRAPHY", "INDEX"]:
            ml = find_line(marker)
            if ml > start and ml < end:
                end = ml - 2

        # Skip the chapter marker and title lines
        content_start = start + 1
        # Find the title line after CHAPTER X
        for k in range(start + 1, min(start + 5, len(lines))):
            if lines[k].strip() and lines[k].strip() != ch_marker:
                content_start = k + 1
                break

        content = "\n".join(lines[content_start:end]).strip()
        content = clean_text(content)
        content = truncate(content)

        items.append({
            "id": sid,
            "name": name,
            "sort_order": sort_order,
            "category": "chapter",
            "level": 1,
            "sections": {"Chapter": content},
            "keywords": [w.lower() for w in title.split() if len(w) > 3],
            "metadata": {}
        })
        ch_ids.append(sid)
        sort_order += 1

    # L2: Thematic groups
    l2_groups = [
        ("theme-ritual-origins", "The Ritual Origins of Art",
         "Harrison's argument that art emerges from ritual: from mimetic hunting dances through seasonal festivals to the Greek spring rites that gave birth to drama. The dromenon (thing done) precedes the drama (thing watched).",
         [sid for sid in ch_ids if any(x in sid for x in ["art-and-ritual", "pantomimic", "spring-festival"])],
         ["ritual", "origins", "dance", "mimesis"]),
        ("theme-greek-transformation", "The Greek Transformation",
         "How Greek culture specifically transformed ritual into art: the dithyramb becoming tragedy, the sacred procession becoming sculptural form, and the critical moment when the spectator separates from the participant.",
         [sid for sid in ch_ids if any(x in sid for x in ["greece", "dromenon", "sculpture"])],
         ["greece", "drama", "sculpture", "transformation"]),
        ("theme-art-and-life", "Art, Ritual, and Modern Life",
         "Harrison's concluding meditation on the relationship between ritual, art, and life. Art is not mere imitation of nature but a mode of heightened experience; ritual is not mere superstition but a communal expression of emotion that art inherits and transforms.",
         [sid for sid in ch_ids if "life" in sid],
         ["modern", "aesthetics", "emotion", "community"]),
    ]

    for gid, gname, about, refs, kws in l2_groups:
        valid_refs = [r for r in refs if r in ch_ids]
        items.append({
            "id": gid,
            "name": gname,
            "sort_order": sort_order,
            "category": "theme",
            "level": 2,
            "composite_of": valid_refs,
            "relationship_type": "emergence",
            "sections": {
                "About": about,
                "For Readers": "Harrison's insight that art and ritual share a common root in human emotional expression remains profoundly relevant. These groupings trace her argument from primitive dance to modern aesthetics."
            },
            "keywords": kws,
            "metadata": {}
        })
        sort_order += 1

    # L3
    items.append({
        "id": "meta-art-from-ritual",
        "name": "From Dromenon to Drama: The Birth of Art",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "composite_of": [g[0] for g in l2_groups],
        "relationship_type": "emergence",
        "sections": {
            "About": "Jane Ellen Harrison's central insight: art is not born from aesthetic contemplation but from the urgency of ritual action. Before there were spectators, there were participants. Before there was drama, there was the dromenon — the thing done, the sacred act. Greek tragedy emerged when the chorus stepped back and someone stepped forward to speak, transforming collective ritual into individual art. This grammar traces that revolutionary transition.",
            "For Readers": "Harrison was one of the Cambridge Ritualists who transformed our understanding of Greek culture. This text connects primitive ritual, Greek drama, and modern art theory in a single luminous argument."
        },
        "keywords": ["dromenon", "drama", "ritual-to-art", "harrison", "cambridge-ritualists"],
        "metadata": {}
    })

    grammar = {
        "_grammar_commons": {
            **base_commons(),
            "attribution": [
                {"name": "Jane Ellen Harrison", "date": "1913", "note": "Ancient Art and Ritual"},
                {"name": "Project Gutenberg", "date": "2005", "note": "eBook #17087"}
            ]
        },
        "name": "Ancient Art and Ritual",
        "description": "Jane Ellen Harrison's groundbreaking study of the connection between ritual and art, tracing how Greek drama emerged from primitive seasonal rites. A founding text of the Cambridge Ritualist school that transformed classical studies.\n\nSource: Project Gutenberg eBook #17087 (https://www.gutenberg.org/ebooks/17087)",
        **base_meta(),
        "tags": ["ritual", "art", "greek-religion", "anthropology", "origins-of-art"],
        "items": items
    }

    write_grammar(grammar, "grammars/ancient-art-ritual/grammar.json")

# ═══════════════════════════════════════════════════════════════════
# 4. MYTHS OF GREECE AND ROME
# ═══════════════════════════════════════════════════════════════════

def parse_myths_greece_rome():
    body = read_seed("seeds/myth-greece-rome.txt")
    lines = body.split("\n")

    def find_centered(heading):
        """Find centered heading (lots of leading spaces)."""
        target = heading.strip()
        for i, line in enumerate(lines):
            if line.strip() == target:
                return i
        return -1

    def find_bold(pattern):
        """Find =N. Name= bold heading."""
        for i, line in enumerate(lines):
            if line.startswith(pattern):
                return i
        return -1

    # Define all sections to extract
    # Format: (search_pattern, id, name, category, keywords)
    section_defs = [
        # Introduction
        ("intro-subjects", "I.\u2014SUBJECTS OF GREEK AND ROMAN MYTHOLOGY.", "intro-subjects", "Introduction: Subjects of Mythology", "introduction", ["mythology", "subjects", "nature-myths"]),
        ("intro-popular", "II.\u2014POPULAR IDEAS CONCERNING THE GODS.", "intro-popular-ideas", "Introduction: Popular Ideas Concerning the Gods", "introduction", ["gods", "anthropomorphism", "worship"]),

        # Part I
        ("cosmogony", "PART I.\u2014COSMOGONY AND THEOGONY.", "cosmogony-theogony", "Cosmogony and Theogony", "cosmogony", ["chaos", "titans", "creation", "cronus", "zeus"]),

        # Part II - Superior Deities
        ("zeus", "=1. Zeus (Jupiter).=", "zeus-jupiter", "Zeus (Jupiter)", "olympian-gods", ["zeus", "jupiter", "sky-father", "thunder"]),
        ("hera", "=2. Hera (Juno).=", "hera-juno", "Hera (Juno)", "olympian-gods", ["hera", "juno", "marriage", "queen"]),
        ("athene", "=3. Pallas Athene (Minerva).=", "athene-minerva", "Pallas Athene (Minerva)", "olympian-gods", ["athene", "minerva", "wisdom", "war"]),
        ("apollo", "=4. Apollo.=", "apollo", "Apollo", "olympian-gods", ["apollo", "sun", "music", "prophecy"]),
        ("artemis", "=5. Artemis (Diana).=", "artemis-diana", "Artemis (Diana)", "olympian-gods", ["artemis", "diana", "hunt", "moon"]),
        ("ares", "=6. Ares (Mars).=", "ares-mars", "Ares (Mars)", "olympian-gods", ["ares", "mars", "war", "battle"]),
        ("aphrodite", "=7. Aphrodite (Venus).=", "aphrodite-venus", "Aphrodite (Venus)", "olympian-gods", ["aphrodite", "venus", "love", "beauty"]),
        ("hermes", "=8. Hermes (Mercurius).=", "hermes-mercury", "Hermes (Mercury)", "olympian-gods", ["hermes", "mercury", "messenger", "trickster"]),
        ("hephaestus", "=9. Heph\u00e6stus (Vulcan).=", "hephaestus-vulcan", "Hephaestus (Vulcan)", "olympian-gods", ["hephaestus", "vulcan", "forge", "fire"]),
        ("hestia", "=10. Hestia (Vesta).=", "hestia-vesta", "Hestia (Vesta)", "olympian-gods", ["hestia", "vesta", "hearth", "home"]),
        ("janus", "=11. Janus.=", "janus", "Janus", "roman-gods", ["janus", "doors", "beginnings", "roman"]),
        ("quirinus", "=12. Quirinus.=", "quirinus", "Quirinus", "roman-gods", ["quirinus", "romulus", "roman"]),
    ]

    # Secondary deities
    secondary_defs = [
        ("=1. Eros (Amor).=", "eros-amor", "Eros (Amor)", "secondary-gods", ["eros", "amor", "love", "cupid"]),
        ("=2. The Muses.=", "the-muses", "The Muses", "secondary-gods", ["muses", "poetry", "arts", "inspiration"]),
        ("=3. The Charites", "charites-gratiae", "The Charites (Gratiae)", "secondary-gods", ["charites", "graces", "beauty"]),
        ("=4. Themis and the Hor", "themis-horae", "Themis and the Horae", "secondary-gods", ["themis", "seasons", "order", "justice"]),
        ("=5. Nice (Victoria).=", "nice-victoria", "Nice (Victoria)", "secondary-gods", ["nike", "victory"]),
        ("=6. Iris.=", "iris", "Iris", "secondary-gods", ["iris", "rainbow", "messenger"]),
        ("=7. Hebe (Juventas).=", "hebe-juventas", "Hebe (Juventas)", "secondary-gods", ["hebe", "youth"]),
        ("=8. Ganymedes.=", "ganymedes", "Ganymedes", "secondary-gods", ["ganymede", "cupbearer", "zeus"]),
    ]

    # Celestial phenomena
    celestial_defs = [
        ("=1. Helios (Sol).=", "helios-sol", "Helios (Sol)", "celestial-gods", ["helios", "sol", "sun"]),
        ("=2. Selene (Luna).=", "selene-luna", "Selene (Luna)", "celestial-gods", ["selene", "luna", "moon"]),
        ("=3. Eos (Aurora).=", "eos-aurora", "Eos (Aurora)", "celestial-gods", ["eos", "aurora", "dawn"]),
        ("=4. The Stars.=", "the-stars", "The Stars", "celestial-gods", ["stars", "constellations"]),
        ("=5. The Winds.=", "the-winds", "The Winds", "celestial-gods", ["winds", "aeolus", "boreas"]),
    ]

    # Healing gods
    healing_defs = [
        ("=1. Asclepius", "asclepius", "Asclepius (Aesculapius)", "healing-gods", ["asclepius", "healing", "medicine"]),
        ("=2. Inferior Deities of Birth", "inferior-healing", "Inferior Deities of Birth and Healing", "healing-gods", ["birth", "healing"]),
    ]

    # Fate deities
    fate_defs = [
        ("=1. M\u0153r\u00e6 (Parc\u00e6).=", "moirae-parcae", "The Moirae (Parcae)", "fate-gods", ["moirae", "fates", "destiny"]),
        ("=2. Nemesis, Tyche", "nemesis-tyche", "Nemesis, Tyche, and Agathodaemon", "fate-gods", ["nemesis", "fortune", "fate"]),
    ]

    # Sea gods
    sea_defs = [
        ("=1. Poseidon (Neptunus).=", "poseidon-neptune", "Poseidon (Neptune)", "sea-gods", ["poseidon", "neptune", "sea", "earthquakes"]),
        ("=2. Amphitrite.=", "amphitrite", "Amphitrite", "sea-gods", ["amphitrite", "sea-queen"]),
        ("=3. Triton and the Tritons.=", "triton", "Triton and the Tritons", "sea-gods", ["triton", "sea"]),
        ("=4. Pontus and his Descendants.=", "pontus", "Pontus and his Descendants", "sea-gods", ["pontus", "nereus", "nereids"]),
        ("=5. Proteus.=", "proteus", "Proteus", "sea-gods", ["proteus", "shapeshifter"]),
        ("=6. Glaucus.=", "glaucus-sea", "Glaucus", "sea-gods", ["glaucus", "sea"]),
        ("=7. Ino Leucothea", "ino-leucothea", "Ino Leucothea and Melicertes", "sea-gods", ["ino", "leucothea"]),
        ("=8. The Sirens.=", "the-sirens", "The Sirens", "sea-gods", ["sirens", "song", "danger"]),
        ("=9. The Race of Oceanus.=", "race-of-oceanus", "The Race of Oceanus", "sea-gods", ["oceanus", "river-gods"]),
    ]

    # Earth and Lower World gods
    earth_defs = [
        ("=1. G\u00e6a (Tellus).=", "gaea-tellus", "Gaea (Tellus)", "earth-gods", ["gaea", "earth-mother"]),
        ("=2. Rhea Cybele", "rhea-cybele", "Rhea Cybele", "earth-gods", ["rhea", "cybele", "mother-goddess"]),
        ("=3. Dionysus, or Bacchus", "dionysus-bacchus", "Dionysus (Bacchus)", "earth-gods", ["dionysus", "bacchus", "wine", "ecstasy"]),
        ("=4. The Nymphs.=", "the-nymphs", "The Nymphs", "earth-gods", ["nymphs", "nature-spirits"]),
        ("=5. The Satyrs.=", "the-satyrs", "The Satyrs", "earth-gods", ["satyrs", "wild"]),
        ("=6. Silenus.=", "silenus", "Silenus", "earth-gods", ["silenus", "wisdom", "dionysus"]),
        ("=7. Greek and Roman Wood-Spirits.=", "wood-spirits", "Greek and Roman Wood-Spirits", "earth-gods", ["pan", "silvanus", "faunus", "woods"]),
        ("=8. Priapus.=", "priapus", "Priapus", "earth-gods", ["priapus", "fertility", "gardens"]),
        ("=9. Saturnus and Ops.=", "saturnus-ops", "Saturnus and Ops", "earth-gods", ["saturn", "ops", "golden-age"]),
        ("=10. Vertumnus and Pomona.=", "vertumnus-pomona", "Vertumnus and Pomona", "earth-gods", ["vertumnus", "pomona", "seasons"]),
        ("=11. Flora.=", "flora", "Flora", "earth-gods", ["flora", "flowers", "spring"]),
        ("=12. Pales.=", "pales", "Pales", "earth-gods", ["pales", "pastoral"]),
        ("=13. Terminus.=", "terminus", "Terminus", "earth-gods", ["terminus", "boundaries"]),
        ("=14. Demeter (Ceres).=", "demeter-ceres", "Demeter (Ceres)", "earth-gods", ["demeter", "ceres", "grain", "harvest"]),
        ("=15. Persephone (Proserpina).=", "persephone", "Persephone (Proserpina)", "underworld-gods", ["persephone", "proserpina", "underworld"]),
        ("=16. Hades (Pluto).=", "hades-pluto", "Hades (Pluto)", "underworld-gods", ["hades", "pluto", "underworld", "death"]),
        ("=17. The Lower World.=", "lower-world", "The Lower World", "underworld-gods", ["underworld", "tartarus", "elysium"]),
        ("=18. The Erinyes", "erinyes-furiae", "The Erinyes (Furiae)", "underworld-gods", ["erinyes", "furies", "vengeance"]),
        ("=19. Hecate.=", "hecate", "Hecate", "underworld-gods", ["hecate", "crossroads", "magic"]),
        ("=20. Sleep and Death.=", "sleep-and-death", "Sleep and Death", "underworld-gods", ["hypnos", "thanatos", "sleep", "death"]),
    ]

    # Roman house gods
    roman_defs = [
        ("=1. The Penates.=", "the-penates", "The Penates", "roman-household", ["penates", "household", "roman"]),
        ("=2. The Lares.=", "the-lares", "The Lares", "roman-household", ["lares", "ancestors", "roman"]),
        ("=3. Larv\u00e6, Lemures", "larvae-lemures", "Larvae, Lemures, and Manes", "roman-household", ["larvae", "lemures", "ghosts", "roman"]),
    ]

    # Heroes
    hero_defs = [
        # Introductory
        ("hero-intro", "I.\u2014INTRODUCTORY.", "heroes-introductory", "Heroes: Introduction", "heroes-intro", ["heroes", "demigods"]),
        ("hero-creation", "II.\u2014THE CREATION AND PRIMITIVE CONDITION OF MANKIND.", "heroes-creation", "The Creation and Primitive Condition of Mankind", "heroes-intro", ["creation", "prometheus", "deucalion"]),
        # Provincial legends
        ("hero-lapithae", "=1. The Lapith\u00e6 and the Centaurs.=", "lapithae-centaurs", "The Lapithae and the Centaurs", "heroes-thessaly", ["lapithae", "centaurs", "thessaly"]),
        ("hero-theban", "=2. Theban Legend.=", "theban-legend", "Theban Legend", "heroes-thebes", ["cadmus", "thebes", "actaeon", "amphion"]),
        ("hero-corinth", "=3. Corinthian Legend.=", "corinthian-legend", "Corinthian Legend", "heroes-corinth", ["sisyphus", "bellerophon", "corinth"]),
        ("hero-argive", "=4. Argive Legend.=", "argive-legend", "Argive Legend", "heroes-argos", ["io", "danaus", "perseus", "argos"]),
        ("hero-dioscuri", "=5. The Dioscuri.=", "the-dioscuri", "The Dioscuri", "heroes-sparta", ["castor", "pollux", "dioscuri", "sparta"]),
        ("hero-heracles", "=6. Heracles (Hercules).=", "heracles", "Heracles (Hercules)", "heroes-heracles", ["heracles", "hercules", "twelve-labours"]),
        ("hero-attic", "=7. Attic Legend.=", "attic-legend", "Attic Legend", "heroes-athens", ["cecrops", "theseus", "athens"]),
        ("hero-cretan", "=8. Cretan Legend.=", "cretan-legend", "Cretan Legend", "heroes-crete", ["minos", "minotaur", "crete"]),
        # Combined undertakings
        ("hero-calydonian", "=1. The Calydonian Hunt.=", "calydonian-hunt", "The Calydonian Hunt", "heroes-combined", ["meleager", "calydonian-boar", "hunt"]),
        ("hero-argonauts", "=2. The Argonauts.=", "the-argonauts", "The Argonauts", "heroes-combined", ["jason", "argonauts", "golden-fleece"]),
        ("hero-theban-cycle", "=3. The Theban Cycle.=", "theban-cycle", "The Theban Cycle", "heroes-combined", ["oedipus", "antigone", "seven-against-thebes"]),
        ("hero-trojan", "=4. The Trojan Cycle.=", "trojan-cycle", "The Trojan Cycle", "heroes-combined", ["troy", "iliad", "achilles", "odysseus"]),
    ]

    # Mythic seers
    seer_defs = [
        ("seers", "V.\u2014MYTHIC SEERS AND BARDS.", "mythic-seers-bards", "Mythic Seers and Bards", "seers", ["orpheus", "musaeus", "seers", "bards"]),
    ]

    # Now parse all sections using a unified approach
    all_defs = []

    # Collect all bold-heading sections in order
    bold_sections = []
    for i, line in enumerate(lines):
        if re.match(r'^=\d+\.', line):
            bold_sections.append((i, line))

    # Also find centered headings
    centered_sections = []
    centered_patterns = [
        "I.\u2014SUBJECTS OF GREEK AND ROMAN MYTHOLOGY.",
        "II.\u2014POPULAR IDEAS CONCERNING THE GODS.",
        "PART I.\u2014COSMOGONY AND THEOGONY.",
        "I.\u2014INTRODUCTORY.",
        "II.\u2014THE CREATION AND PRIMITIVE CONDITION OF MANKIND.",
        "V.\u2014MYTHIC SEERS AND BARDS.",
    ]
    for pat in centered_patterns:
        for i, line in enumerate(lines):
            if line.strip() == pat:
                centered_sections.append((i, line.strip()))
                break

    # Build a unified ordered list of all section starts
    all_section_starts = sorted(
        [(ln, text.strip()) for ln, text in bold_sections] +
        [(ln, text) for ln, text in centered_sections],
        key=lambda x: x[0]
    )

    # Map from heading text prefix -> section def
    # We'll build items by iterating through all_section_starts
    items = []
    sort_order = 1

    # Build a mapping of section defs
    all_section_defs = []

    # Introduction sections
    all_section_defs.append(("I.\u2014SUBJECTS OF GREEK AND ROMAN MYTHOLOGY.", "intro-subjects", "Introduction: Subjects of Mythology", "introduction", ["mythology", "nature-myths"]))
    all_section_defs.append(("II.\u2014POPULAR IDEAS CONCERNING THE GODS.", "intro-popular-ideas", "Introduction: Popular Ideas Concerning the Gods", "introduction", ["gods", "anthropomorphism"]))

    # Cosmogony
    all_section_defs.append(("PART I.\u2014COSMOGONY AND THEOGONY.", "cosmogony-theogony", "Cosmogony and Theogony", "cosmogony", ["chaos", "titans", "creation"]))

    # Superior deities (from bold headings)
    sup_deity_map = {
        "=1. Zeus (Jupiter).=": ("zeus-jupiter", "Zeus (Jupiter)", "olympian-gods", ["zeus", "jupiter", "sky-father"]),
        "=2. Hera (Juno).=": ("hera-juno", "Hera (Juno)", "olympian-gods", ["hera", "juno", "marriage"]),
        "=3. Pallas Athene (Minerva).=": ("athene-minerva", "Pallas Athene (Minerva)", "olympian-gods", ["athene", "minerva", "wisdom"]),
        "=4. Apollo.=": ("apollo", "Apollo", "olympian-gods", ["apollo", "sun", "music"]),
        "=5. Artemis (Diana).=": ("artemis-diana", "Artemis (Diana)", "olympian-gods", ["artemis", "diana", "hunt"]),
        "=6. Ares (Mars).=": ("ares-mars", "Ares (Mars)", "olympian-gods", ["ares", "mars", "war"]),
        "=7. Aphrodite (Venus).=": ("aphrodite-venus", "Aphrodite (Venus)", "olympian-gods", ["aphrodite", "venus", "love"]),
        "=8. Hermes (Mercurius).=": ("hermes-mercury", "Hermes (Mercury)", "olympian-gods", ["hermes", "mercury", "messenger"]),
    }

    # We need a simpler approach: just find each heading and extract text until the next heading
    # Build one big ordered list of (line_num, id, name, category, keywords)

    master_sections = []

    # Helper to find a heading
    def find_heading(text, after=0):
        for i, line in enumerate(lines):
            if i <= after:
                continue
            if line.strip() == text or line.startswith(text):
                return i
        return -1

    # Define ALL sections in order with their search patterns
    ordered_sections = [
        ("I.\u2014SUBJECTS OF GREEK AND ROMAN MYTHOLOGY.", "intro-subjects", "Introduction: Subjects of Mythology", "introduction", ["mythology", "nature-myths"]),
        ("II.\u2014POPULAR IDEAS CONCERNING THE GODS.", "intro-popular-ideas", "Introduction: Popular Ideas Concerning the Gods", "introduction", ["gods", "anthropomorphism"]),
        ("PART I.\u2014COSMOGONY AND THEOGONY.", "cosmogony-theogony", "Cosmogony and Theogony", "cosmogony", ["chaos", "titans", "creation", "cronus"]),
        ("=1. Zeus (Jupiter).=", "zeus-jupiter", "Zeus (Jupiter)", "olympian-gods", ["zeus", "jupiter", "sky-father", "thunder"]),
        ("=2. Hera (Juno).=", "hera-juno", "Hera (Juno)", "olympian-gods", ["hera", "juno", "marriage"]),
        ("=3. Pallas Athene (Minerva).=", "athene-minerva", "Pallas Athene (Minerva)", "olympian-gods", ["athene", "minerva", "wisdom"]),
        ("=4. Apollo.=", "apollo", "Apollo", "olympian-gods", ["apollo", "sun", "music", "prophecy"]),
        ("=5. Artemis (Diana).=", "artemis-diana", "Artemis (Diana)", "olympian-gods", ["artemis", "diana", "hunt", "moon"]),
        ("=6. Ares (Mars).=", "ares-mars", "Ares (Mars)", "olympian-gods", ["ares", "mars", "war"]),
        ("=7. Aphrodite (Venus).=", "aphrodite-venus", "Aphrodite (Venus)", "olympian-gods", ["aphrodite", "venus", "love", "beauty"]),
        ("=8. Hermes (Mercurius).=", "hermes-mercury", "Hermes (Mercury)", "olympian-gods", ["hermes", "mercury", "messenger"]),
        ("=9. Heph\u00e6stus (Vulcan).=", "hephaestus-vulcan", "Hephaestus (Vulcan)", "olympian-gods", ["hephaestus", "vulcan", "forge"]),
        ("=10. Hestia (Vesta).=", "hestia-vesta", "Hestia (Vesta)", "olympian-gods", ["hestia", "vesta", "hearth"]),
        ("=11. Janus.=", "janus", "Janus", "roman-gods", ["janus", "doors", "beginnings"]),
        ("=12. Quirinus.=", "quirinus", "Quirinus", "roman-gods", ["quirinus", "romulus"]),
        ("=1. Eros (Amor).=", "eros-amor", "Eros (Amor)", "secondary-gods", ["eros", "amor", "cupid"]),
        ("=2. The Muses.=", "the-muses", "The Muses", "secondary-gods", ["muses", "poetry", "inspiration"]),
        ("=3. The Charites", "charites-gratiae", "The Charites (Gratiae)", "secondary-gods", ["charites", "graces"]),
        ("=4. Themis and the Hor", "themis-horae", "Themis and the Horae", "secondary-gods", ["themis", "seasons"]),
        ("=5. Nice (Victoria).=", "nice-victoria", "Nice (Victoria)", "secondary-gods", ["nike", "victory"]),
        ("=6. Iris.=", "iris", "Iris", "secondary-gods", ["iris", "rainbow"]),
        ("=7. Hebe (Juventas).=", "hebe-juventas", "Hebe (Juventas)", "secondary-gods", ["hebe", "youth"]),
        ("=8. Ganymedes.=", "ganymedes", "Ganymedes", "secondary-gods", ["ganymede", "cupbearer"]),
        ("=1. Helios (Sol).=", "helios-sol", "Helios (Sol)", "celestial-gods", ["helios", "sol", "sun"]),
        ("=2. Selene (Luna).=", "selene-luna", "Selene (Luna)", "celestial-gods", ["selene", "moon"]),
        ("=3. Eos (Aurora).=", "eos-aurora", "Eos (Aurora)", "celestial-gods", ["eos", "dawn"]),
        ("=4. The Stars.=", "the-stars", "The Stars", "celestial-gods", ["stars", "constellations"]),
        ("=5. The Winds.=", "the-winds", "The Winds", "celestial-gods", ["winds", "boreas"]),
        ("=1. Asclepius", "asclepius", "Asclepius (Aesculapius)", "healing-gods", ["asclepius", "healing"]),
        ("=2. Inferior Deities of Birth", "inferior-healing", "Inferior Deities of Birth and Healing", "healing-gods", ["birth", "healing"]),
        ("=1. M", "moirae-parcae", "The Moirae (Parcae)", "fate-gods", ["moirae", "fates"]),
        ("=2. Nemesis, Tyche", "nemesis-tyche", "Nemesis, Tyche, and Agathodaemon", "fate-gods", ["nemesis", "fortune"]),
        ("=1. Poseidon (Neptunus).=", "poseidon-neptune", "Poseidon (Neptune)", "sea-gods", ["poseidon", "neptune", "sea"]),
        ("=2. Amphitrite.=", "amphitrite", "Amphitrite", "sea-gods", ["amphitrite"]),
        ("=3. Triton and the Tritons.=", "triton", "Triton and the Tritons", "sea-gods", ["triton"]),
        ("=4. Pontus and his Descendants.=", "pontus", "Pontus and his Descendants", "sea-gods", ["pontus", "nereus"]),
        ("=5. Proteus.=", "proteus", "Proteus", "sea-gods", ["proteus"]),
        ("=6. Glaucus.=", "glaucus-sea", "Glaucus", "sea-gods", ["glaucus"]),
        ("=7. Ino Leucothea", "ino-leucothea", "Ino Leucothea and Melicertes", "sea-gods", ["ino"]),
        ("=8. The Sirens.=", "the-sirens", "The Sirens", "sea-gods", ["sirens"]),
        ("=9. The Race of Oceanus.=", "race-of-oceanus", "The Race of Oceanus", "sea-gods", ["oceanus"]),
        ("=1. G", "gaea-tellus", "Gaea (Tellus)", "earth-gods", ["gaea", "earth-mother"]),
        ("=2. Rhea Cybele", "rhea-cybele", "Rhea Cybele", "earth-gods", ["rhea", "cybele"]),
        ("=3. Dionysus, or Bacchus", "dionysus-bacchus", "Dionysus (Bacchus)", "earth-gods", ["dionysus", "wine", "ecstasy"]),
        ("=4. The Nymphs.=", "the-nymphs", "The Nymphs", "earth-gods", ["nymphs"]),
        ("=5. The Satyrs.=", "the-satyrs", "The Satyrs", "earth-gods", ["satyrs"]),
        ("=6. Silenus.=", "silenus", "Silenus", "earth-gods", ["silenus", "wisdom"]),
        ("=7. Greek and Roman Wood-Spirits.=", "wood-spirits", "Greek and Roman Wood-Spirits", "earth-gods", ["pan", "faunus"]),
        ("=8. Priapus.=", "priapus", "Priapus", "earth-gods", ["priapus", "fertility"]),
        ("=9. Saturnus and Ops.=", "saturnus-ops", "Saturnus and Ops", "earth-gods", ["saturn", "golden-age"]),
        ("=10. Vertumnus and Pomona.=", "vertumnus-pomona", "Vertumnus and Pomona", "earth-gods", ["vertumnus", "pomona"]),
        ("=11. Flora.=", "flora", "Flora", "earth-gods", ["flora", "flowers"]),
        ("=12. Pales.=", "pales", "Pales", "earth-gods", ["pales"]),
        ("=13. Terminus.=", "terminus", "Terminus", "earth-gods", ["terminus"]),
        ("=14. Demeter (Ceres).=", "demeter-ceres", "Demeter (Ceres)", "earth-gods", ["demeter", "ceres", "grain"]),
        ("=15. Persephone (Proserpina).=", "persephone", "Persephone (Proserpina)", "underworld-gods", ["persephone", "underworld"]),
        ("=16. Hades (Pluto).=", "hades-pluto", "Hades (Pluto)", "underworld-gods", ["hades", "pluto"]),
        ("=17. The Lower World.=", "lower-world", "The Lower World", "underworld-gods", ["underworld", "tartarus"]),
        ("=18. The Erinyes", "erinyes-furiae", "The Erinyes (Furiae)", "underworld-gods", ["erinyes", "furies"]),
        ("=19. Hecate.=", "hecate", "Hecate", "underworld-gods", ["hecate", "crossroads"]),
        ("=20. Sleep and Death.=", "sleep-and-death", "Sleep and Death", "underworld-gods", ["hypnos", "thanatos"]),
        ("=1. The Penates.=", "the-penates", "The Penates", "roman-household", ["penates", "household"]),
        ("=2. The Lares.=", "the-lares", "The Lares", "roman-household", ["lares", "ancestors"]),
        ("=3. Larv", "larvae-lemures", "Larvae, Lemures, and Manes", "roman-household", ["larvae", "ghosts"]),
        ("I.\u2014INTRODUCTORY.", "heroes-introductory", "Heroes: Introduction", "heroes-intro", ["heroes", "demigods"]),
        ("II.\u2014THE CREATION AND PRIMITIVE CONDITION OF MANKIND.", "heroes-creation", "The Creation and Primitive Condition of Mankind", "heroes-intro", ["creation", "prometheus"]),
        ("=1. The Lapith", "lapithae-centaurs", "The Lapithae and the Centaurs", "heroes-regional", ["lapithae", "centaurs"]),
        ("=2. Theban Legend.=", "theban-legend", "Theban Legend", "heroes-regional", ["cadmus", "thebes"]),
        ("=3. Corinthian Legend.=", "corinthian-legend", "Corinthian Legend", "heroes-regional", ["sisyphus", "bellerophon"]),
        ("=4. Argive Legend.=", "argive-legend", "Argive Legend", "heroes-regional", ["io", "perseus"]),
        ("=5. The Dioscuri.=", "the-dioscuri", "The Dioscuri", "heroes-regional", ["castor", "pollux"]),
        ("=6. Heracles (Hercules).=", "heracles", "Heracles (Hercules)", "heroes-heracles", ["heracles", "hercules"]),
        ("=7. Attic Legend.=", "attic-legend", "Attic Legend", "heroes-regional", ["theseus", "cecrops"]),
        ("=8. Cretan Legend.=", "cretan-legend", "Cretan Legend", "heroes-regional", ["minos", "minotaur"]),
        ("=1. The Calydonian Hunt.=", "calydonian-hunt", "The Calydonian Hunt", "heroes-combined", ["meleager", "hunt"]),
        ("=2. The Argonauts.=", "the-argonauts", "The Argonauts", "heroes-combined", ["jason", "golden-fleece"]),
        ("=3. The Theban Cycle.=", "theban-cycle", "The Theban Cycle", "heroes-combined", ["oedipus", "antigone"]),
        ("=4. The Trojan Cycle.=", "trojan-cycle", "The Trojan Cycle", "heroes-combined", ["troy", "achilles"]),
        ("V.\u2014MYTHIC SEERS AND BARDS.", "mythic-seers-bards", "Mythic Seers and Bards", "seers", ["orpheus", "musaeus"]),
    ]

    # Now find each heading and extract text
    items = []
    sort_order = 1
    found_positions = []
    last_search_pos = 0

    for pattern, sid, name, cat, kws in ordered_sections:
        # Find this heading after the last found position
        found = -1
        for i in range(last_search_pos, len(lines)):
            line = lines[i].strip()
            # Handle centered headings (with leading spaces)
            if line == pattern or line.startswith(pattern):
                found = i
                break
            # Also try with the raw line for = patterns
            if lines[i].startswith(pattern):
                found = i
                break
        if found == -1:
            print(f"  WARNING: Could not find '{pattern}' for {sid}")
            continue

        found_positions.append((found, sid, name, cat, kws))
        last_search_pos = found + 1

    # Now extract text between consecutive found positions
    for idx, (line_num, sid, name, cat, kws) in enumerate(found_positions):
        # End is start of next section or end of text
        if idx + 1 < len(found_positions):
            end_line = found_positions[idx + 1][0]
        else:
            # Last section - go to INDEX or end
            end_line = len(lines)
            for i, line in enumerate(lines):
                if line.strip() == "INDEX." and i > line_num:
                    end_line = i
                    break

        content = "\n".join(lines[line_num:end_line]).strip()
        content = clean_text(content)
        # Remove Footnote blocks at end
        fn_match = re.search(r'\nFootnote \d+:', content)
        if fn_match:
            content = content[:fn_match.start()].strip()
        content = truncate(content)

        items.append({
            "id": sid,
            "name": name,
            "sort_order": sort_order,
            "category": cat,
            "level": 1,
            "sections": {"Text": content},
            "keywords": kws,
            "metadata": {}
        })
        sort_order += 1

    # L2: Thematic groups
    all_ids = [i['id'] for i in items]

    l2_groups = [
        ("group-olympian-gods", "The Olympian Gods",
         "The twelve great deities of Mount Olympus: Zeus, Hera, Athene, Apollo, Artemis, Ares, Aphrodite, Hermes, Hephaestus, and Hestia, plus the Roman Janus and Quirinus. These are the ruling powers of the Greek and Roman world.",
         [sid for sid in all_ids if any(i['category'] == 'olympian-gods' for i in items if i['id'] == sid)],
         ["olympian", "gods", "twelve"]),
        ("group-secondary-celestial", "Secondary and Celestial Deities",
         "The attendant gods, muses, and celestial phenomena: Eros, the Muses, the Charites, the Hours, Nike, Iris, Hebe, Ganymede, Helios, Selene, Eos, the Stars, and the Winds.",
         [sid for sid in all_ids if any(i['category'] in ('secondary-gods', 'celestial-gods') for i in items if i['id'] == sid)],
         ["secondary", "celestial", "muses"]),
        ("group-sea-gods", "Gods of the Sea",
         "Poseidon and his watery kingdom: Amphitrite, Triton, the Nereids, Proteus, Glaucus, the Sirens, and the race of Oceanus. The sea was a realm of mystery, danger, and divine power.",
         [sid for sid in all_ids if any(i['category'] == 'sea-gods' for i in items if i['id'] == sid)],
         ["sea", "poseidon", "ocean"]),
        ("group-earth-underworld", "Gods of Earth, Nature, and the Underworld",
         "The chthonic and terrestrial deities: Gaea, Dionysus, Demeter, Pan, the Nymphs and Satyrs, and the dark rulers of the underworld — Hades, Persephone, Hecate, and the Erinyes.",
         [sid for sid in all_ids if any(i['category'] in ('earth-gods', 'underworld-gods') for i in items if i['id'] == sid)],
         ["earth", "underworld", "nature", "chthonic"]),
        ("group-heroes-regional", "Regional Heroic Legends",
         "The great heroes of the Greek city-states: Heracles of Thebes, Theseus of Athens, Perseus of Argos, Bellerophon of Corinth, and Minos of Crete. Each hero embodies the pride and values of his homeland.",
         [sid for sid in all_ids if any(i['category'] in ('heroes-regional', 'heroes-heracles', 'heroes-intro') for i in items if i['id'] == sid)],
         ["heroes", "city-states", "quests"]),
        ("group-heroes-combined", "The Great Combined Adventures",
         "The grand enterprises of the heroic age: the Calydonian Hunt, the voyage of the Argonauts, the Theban cycle of Oedipus, and the Trojan War — stories that united heroes from across the Greek world.",
         [sid for sid in all_ids if any(i['category'] == 'heroes-combined' for i in items if i['id'] == sid)],
         ["trojan-war", "argonauts", "oedipus", "epic"]),
    ]

    for gid, gname, about, refs, kws in l2_groups:
        valid_refs = [r for r in refs if r in all_ids]
        if not valid_refs:
            continue
        items.append({
            "id": gid,
            "name": gname,
            "sort_order": sort_order,
            "category": "theme",
            "level": 2,
            "composite_of": valid_refs,
            "relationship_type": "emergence",
            "sections": {
                "About": about,
                "For Readers": "Seemann's treatment emphasizes the artistic representation of each deity and hero, making this grammar especially useful for understanding classical art and its mythological subjects."
            },
            "keywords": kws,
            "metadata": {}
        })
        sort_order += 1

    # L3
    l3_groups = [
        ("meta-gods", "The Divine Order: Gods of Greece and Rome",
         [gid for gid, _, _, _, _ in l2_groups if "god" in gid or "celestial" in gid or "sea" in gid or "earth" in gid],
         "The complete pantheon of Greek and Roman religion, from the ruling Olympians through the secondary attendants, sea powers, earth spirits, and underworld rulers. Seemann shows how the Greeks transformed crude nature-worship into the most beautiful and human religion the ancient world produced.",
         ["pantheon", "greek-religion", "roman-religion"]),
        ("meta-heroes", "The Heroic Age: Mortals Who Challenged the Gods",
         [gid for gid, _, _, _, _ in l2_groups if "hero" in gid],
         "The great heroes of myth — part human, part divine — who pushed against the boundaries of mortality. From Heracles' twelve labours to the fall of Troy, these legends explore the tragic grandeur of human striving against fate.",
         ["heroes", "mortality", "fate", "glory"]),
    ]

    for gid, gname, refs, about, kws in l3_groups:
        valid_refs = [r for r in refs if r in [i['id'] for i in items]]
        if not valid_refs:
            continue
        items.append({
            "id": gid,
            "name": gname,
            "sort_order": sort_order,
            "category": "meta",
            "level": 3,
            "composite_of": valid_refs,
            "relationship_type": "emergence",
            "sections": {
                "About": about,
                "For Readers": "This comprehensive mythology covers the full sweep of Greek and Roman divine and heroic legend, with special attention to how each figure was represented in art."
            },
            "keywords": kws,
            "metadata": {}
        })
        sort_order += 1

    grammar = {
        "_grammar_commons": {
            **base_commons(),
            "attribution": [
                {"name": "Otto Seemann", "date": "1882", "note": "The Mythology of Greece and Rome, edited by G. H. Bianchi"},
                {"name": "Project Gutenberg", "date": "2020", "note": "eBook #61901"}
            ]
        },
        "name": "Myths of Greece and Rome",
        "description": "Otto Seemann's comprehensive guide to the mythology of Greece and Rome, with special reference to its use in art. Covers the entire pantheon from the Olympian gods through sea deities, earth spirits, and underworld powers, plus the great heroic legends from Heracles to the Trojan War.\n\nSource: Project Gutenberg eBook #61901 (https://www.gutenberg.org/ebooks/61901)",
        **base_meta(),
        "tags": ["greek-mythology", "roman-mythology", "gods", "heroes", "classical-art"],
        "items": items
    }

    write_grammar(grammar, "grammars/myth-greece-rome/grammar.json")

# ═══════════════════════════════════════════════════════════════════
# RUN ALL PARSERS
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("Parsing Four Greek Religion Grammars")
    print("=" * 60)

    print("\n1. Five Stages of Greek Religion...")
    parse_five_stages()

    print("\n2. Eleusinian Mysteries...")
    parse_eleusinian()

    print("\n3. Ancient Art and Ritual...")
    parse_ancient_art()

    print("\n4. Myths of Greece and Rome...")
    parse_myths_greece_rome()

    print("\n" + "=" * 60)
    print("Done!")
