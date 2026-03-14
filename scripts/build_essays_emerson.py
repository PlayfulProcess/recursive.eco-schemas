#!/usr/bin/env python3
"""
Parse Essays: First Series by Ralph Waldo Emerson (Gutenberg #2944, 1841)
into a grammar.json.

Structure:
- L1: Paragraphs within each of the 12 essays
- L2: Essay emergence groups + thematic groups
- L3: Meta-category connecting all

The 12 essays: History, Self-Reliance, Compensation, Spiritual Laws, Love,
Friendship, Prudence, Heroism, The Over-Soul, Circles, Intellect, Art.
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "essays-emerson.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "essays-emerson")
OUTPUT = os.path.join(OUTPUT_DIR, "grammar.json")


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    if start != -1:
        text = text[text.index("\n", start) + 1:]
    if end != -1:
        text = text[:end]
    return text.strip()


ESSAYS = [
    {
        "slug": "history",
        "prefix": "history-para",
        "title": "History",
        "num": "I",
        "header": "HISTORY",
    },
    {
        "slug": "self-reliance",
        "prefix": "self-reliance-para",
        "title": "Self-Reliance",
        "num": "II",
        "header": "SELF-RELIANCE",
    },
    {
        "slug": "compensation",
        "prefix": "compensation-para",
        "title": "Compensation",
        "num": "III",
        "header": "COMPENSATION",
    },
    {
        "slug": "spiritual-laws",
        "prefix": "spiritual-laws-para",
        "title": "Spiritual Laws",
        "num": "IV",
        "header": "SPIRITUAL LAWS",
    },
    {
        "slug": "love",
        "prefix": "love-para",
        "title": "Love",
        "num": "V",
        "header": "LOVE",
    },
    {
        "slug": "friendship",
        "prefix": "friendship-para",
        "title": "Friendship",
        "num": "VI",
        "header": "FRIENDSHIP",
    },
    {
        "slug": "prudence",
        "prefix": "prudence-para",
        "title": "Prudence",
        "num": "VII",
        "header": "PRUDENCE",
    },
    {
        "slug": "heroism",
        "prefix": "heroism-para",
        "title": "Heroism",
        "num": "VIII",
        "header": "HEROISM",
    },
    {
        "slug": "the-over-soul",
        "prefix": "over-soul-para",
        "title": "The Over-Soul",
        "num": "IX",
        "header": "THE OVER-SOUL",
    },
    {
        "slug": "circles",
        "prefix": "circles-para",
        "title": "Circles",
        "num": "X",
        "header": "CIRCLES",
    },
    {
        "slug": "intellect",
        "prefix": "intellect-para",
        "title": "Intellect",
        "num": "XI",
        "header": "INTELLECT",
    },
    {
        "slug": "art",
        "prefix": "art-para",
        "title": "Art",
        "num": "XII",
        "header": "ART",
    },
]


def find_essay_boundaries(text):
    """Find the start of each essay.

    Each essay is preceded by its Roman numeral on its own line, then the
    title in ALL CAPS, then epigraph/poetry, then the title again in ALL CAPS,
    then the essay body. We want to find the SECOND occurrence of each title
    (the one that precedes the actual body text).
    """
    lines = text.split('\n')
    boundaries = []

    # Skip the table of contents (first ~55 lines of stripped text)
    # Find "Next Volume" marker which ends the TOC
    toc_end = 0
    for i, line in enumerate(lines):
        if 'Next Volume' in line:
            toc_end = i
            break

    for essay in ESSAYS:
        # Find the Roman numeral line for this essay
        numeral_line = None
        for i in range(toc_end, len(lines)):
            stripped = lines[i].strip()
            if stripped == f"{essay['num']}.":
                numeral_line = i
                break

        if numeral_line is None:
            continue

        # After the numeral, find the second occurrence of the title
        # (first is right after numeral, second is after the epigraph)
        title_count = 0
        essay_start = None
        for i in range(numeral_line + 1, min(numeral_line + 50, len(lines))):
            stripped = lines[i].strip()
            if stripped == essay["header"]:
                title_count += 1
                if title_count == 2:
                    essay_start = i
                    break

        if essay_start is not None:
            boundaries.append((essay_start, essay))
        elif numeral_line is not None:
            # Fallback: use the numeral line
            boundaries.append((numeral_line, essay))

    boundaries.sort(key=lambda x: x[0])
    return boundaries, lines


def extract_essay_text(boundaries, lines):
    """Extract text for each essay."""
    essays = []
    for idx, (start_line, essay) in enumerate(boundaries):
        # Skip the title line and any blank lines
        content_start = start_line + 1
        while content_start < len(lines):
            stripped = lines[content_start].strip()
            if not stripped:
                content_start += 1
                continue
            break

        if idx + 1 < len(boundaries):
            # End at the Roman numeral line of the next essay
            # Go back from next boundary to find the numeral line
            end_line = boundaries[idx + 1][0]
            # Search backwards for the numeral line
            for i in range(end_line, max(end_line - 50, 0), -1):
                stripped = lines[i].strip()
                if stripped == f"{boundaries[idx + 1][1]['num']}.":
                    end_line = i
                    break
        else:
            end_line = len(lines)

        essay_text = '\n'.join(lines[content_start:end_line]).strip()

        # Remove trailing "Next Volume" and similar
        for marker in ['Next Volume', 'End of Project Gutenberg']:
            idx_marker = essay_text.find(marker)
            if idx_marker != -1:
                essay_text = essay_text[:idx_marker].strip()

        essays.append({
            "slug": essay["slug"],
            "prefix": essay["prefix"],
            "title": essay["title"],
            "text": essay_text,
        })

    return essays


def split_into_paragraphs(text):
    """Split text into paragraphs."""
    raw_paragraphs = re.split(r'\n\s*\n', text)
    paragraphs = []

    for p in raw_paragraphs:
        cleaned = p.strip()
        if not cleaned:
            continue
        if len(cleaned) < 20:
            continue
        # Normalize internal whitespace
        cleaned = re.sub(r'\n\s*', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        paragraphs.append(cleaned)

    return paragraphs


def first_sentence_name(text, max_len=80):
    """Extract first sentence, truncated to max_len chars."""
    match = re.search(r'[.;!?]', text)
    if match and match.end() <= max_len:
        return text[:match.end()].strip()
    if len(text) <= max_len:
        return text
    truncated = text[:max_len]
    last_space = truncated.rfind(' ')
    if last_space > 40:
        truncated = truncated[:last_space]
    return truncated + "..."


ESSAY_ABOUTS = {
    "history": {
        "about": "Emerson's argument that all of history is biography -- that the universal mind expresses itself through every individual. There is one mind common to all; what Plato thought, any person may think. History is not a catalogue of dead facts but a living resource through which we understand ourselves. Every revolution was first a thought in one person's mind.",
        "for_readers": "The opening essay establishes Emerson's central theme: the unity of the individual soul with the universal mind. His claim that 'there is properly no history, only biography' challenges us to read history not as spectators but as participants. Every historical event is a mirror in which we can recognize our own experience.",
    },
    "self-reliance": {
        "about": "Emerson's most famous and most radical essay. Trust thyself. Society everywhere is in conspiracy against the manhood of every one of its members. Whoso would be a man must be a nonconformist. A foolish consistency is the hobgoblin of little minds. To be great is to be misunderstood. These aphorisms have entered the American bloodstream, but the essay's full argument -- that conformity is spiritual death and self-trust is the only path to greatness -- remains as challenging as ever.",
        "for_readers": "Self-Reliance is the essay that made Emerson dangerous. He does not merely encourage independence; he demands it as a spiritual obligation. His argument that 'imitation is suicide' -- that every person has a unique contribution that can only be made by trusting their own deepest intuitions -- challenges every institution, every tradition, every authority. The essay is the manifesto of American individualism, for better and worse.",
    },
    "compensation": {
        "about": "Emerson's meditation on cosmic justice. Every action has its equal reaction; every excess produces its own correction; every evil carries its own punishment and every good its own reward. The universe is self-balancing. This is not conventional moralism but a metaphysical claim: the structure of reality itself ensures that nothing is gained without something lost, and nothing lost without something gained.",
        "for_readers": "Compensation explores the idea that the universe is inherently just -- not through divine intervention but through the nature of things themselves. Emerson's examples range from physics to ethics: action and reaction, crime and punishment, gift and loss. The essay's most radical claim is that suffering has its compensations and success its penalties -- that every condition of life carries both burden and blessing.",
    },
    "spiritual-laws": {
        "about": "Emerson's argument that the soul has its own laws, deeper than any convention. We do not choose our callings; they choose us. The soul draws to itself what belongs to it. Effort and will are less important than receptivity and trust. The essay counsels a radical passivity -- not laziness but attentiveness to the soul's own direction, which is wiser than any plan.",
        "for_readers": "Spiritual Laws is Emerson at his most mystical and his most practical. His argument that 'a man's genius is always telling him things' -- that each person has an inner guidance system more reliable than external authority -- anticipates modern ideas about intuition, flow, and authentic vocation. The essay's counsel to 'do your work, and you shall reinforce yourself' is both spiritual advice and career guidance.",
    },
    "love": {
        "about": "Emerson's meditation on romantic love as a portal to the divine. Love begins with the beauty of one person but, if followed deeply enough, leads to the beauty of the universe. The lover sees in the beloved a symbol of infinite beauty and goodness. But the essay also acknowledges love's illusions and its tendency toward disenchantment -- the beloved is always more than and less than the lover imagines.",
        "for_readers": "The Love essay reveals Emerson's Platonism. He sees romantic love not as an end in itself but as a path toward the perception of universal beauty. The essay moves from the intoxication of first love through its inevitable disillusionment to a higher love that embraces the beloved's imperfections. His treatment of love's illusions is tender rather than cynical.",
    },
    "friendship": {
        "about": "Emerson's ideal of friendship: rare, demanding, and ultimately grounded in shared commitment to truth. A friend is a person with whom I may be sincere; before them I may think aloud. But friendship requires both tenderness and honesty -- the courage to speak truth even when it wounds. Emerson's friendships are not comfortable but bracing, not relaxing but elevating.",
        "for_readers": "The Friendship essay sets impossibly high standards -- and that is its point. Emerson demands that friendship be a meeting of equals, each challenging the other to be more fully themselves. His requirement of absolute sincerity ('a friend is a person with whom I may be sincere') is both beautiful and terrifying. The essay explains why Emerson had so few close friends.",
    },
    "prudence": {
        "about": "Emerson's surprising defense of practical wisdom. The Transcendentalist sage argues for attention to health, money, and worldly affairs -- not as ends in themselves but as the material foundation of spiritual life. The body is the temple; neglect it and the spirit suffers. Prudence is not materialism but the recognition that spirit must work through matter.",
        "for_readers": "Prudence is the essay that surprises readers who think of Emerson as purely otherworldly. He advocates for bodily health, financial responsibility, and practical attention to the details of daily life. His argument is that the spiritual and the practical are not opposed: a person who cannot manage their material affairs will find their spiritual life equally disordered.",
    },
    "heroism": {
        "about": "Emerson's celebration of moral courage -- the willingness to act on principle regardless of consequences. The hero is not the warrior but the person who speaks truth, who stands alone against the crowd, who chooses conscience over comfort. Heroism is available to everyone: it is not a matter of circumstances but of character, not of great events but of daily choices.",
        "for_readers": "Heroism democratizes courage. Emerson argues that the heroic is not confined to battlefields and great crises but is available in every moment of moral choice. His hero is the person who tells the truth when lying would be easier, who stands by principle when conformity would be safer. The essay channels the Stoic tradition -- Marcus Aurelius and Epictetus -- into American Transcendentalism.",
    },
    "the-over-soul": {
        "about": "Emerson's most mystical essay: his account of the universal soul that underlies and connects all individual souls. The Over-Soul is not a personal God but an impersonal divine presence in which all beings participate. In moments of insight, prayer, or communion with nature, the individual soul recognizes its unity with this larger reality. Revelation is not historical but perpetual.",
        "for_readers": "The Over-Soul is Emerson's theology -- or anti-theology. He replaces the personal God of Christianity with an impersonal divine presence that speaks through every soul. His claim that 'the soul's advances are not made by graduation, but by ascension' -- that insight comes not through study but through sudden illumination -- aligns him with the mystic traditions of every religion. This essay influenced William James, the Vedanta movement, and the entire New Thought tradition.",
    },
    "circles": {
        "about": "Emerson's meditation on perpetual growth. Every truth is temporary; every achievement is a platform for the next. The eye is the first circle, the horizon the second -- and there is always a wider circle beyond. No fact is sacred; no institution is permanent; no boundary is final. The essay celebrates restlessness, experimentation, and the refusal to settle into any fixed position.",
        "for_readers": "Circles is the most exhilarating and most unsettling of Emerson's essays. Its message -- that every truth will be superseded, every achievement outgrown, every certainty dissolved -- is both liberating and terrifying. The essay's energy is centrifugal: it spins outward from every center, refusing to rest. Emerson's image of ever-expanding circles anticipates Nietzsche's eternal return and the postmodern suspicion of all fixed truths.",
    },
    "intellect": {
        "about": "Emerson's account of the intellect as a faculty distinct from talent or learning. True intellect is receptive, not aggressive; it waits for truth to reveal itself rather than pursuing it by force. The intellect sees universals where the understanding sees particulars. It operates by intuition, not logic, and its truths come as gifts rather than conquests.",
        "for_readers": "The Intellect essay distinguishes between knowing and understanding, between information and insight. Emerson argues that the deepest truths cannot be reached by effort but only by receptivity -- a kind of intellectual meditation. His distinction between the 'constructive intellect' (which builds systems) and the 'receptive intellect' (which receives truth) anticipates modern discussions of creativity, flow, and the role of the unconscious in thought.",
    },
    "art": {
        "about": "Emerson's theory of art: true art is not imitation but expression of the universal through the particular. The artist does not copy nature but reveals the spiritual meaning hidden within natural forms. Art is great not when it is beautiful but when it is true -- when it expresses the deepest laws of the universe in sensible form. But art must also serve life: art for art's sake is a dead end.",
        "for_readers": "The final essay brings the collection full circle. Art, like history, is a way of seeing the universal in the particular. Emerson's requirement that art serve truth rather than beauty, and life rather than itself, places him at odds with aestheticism but in sympathy with every tradition that sees art as a vehicle for spiritual insight. His vision of art as 'nature passed through the alembic of man' is both Romantic and Transcendentalist.",
    },
}


THEMATIC_GROUPS = [
    {
        "id": "theme-self-trust",
        "name": "Self-Trust and Nonconformity",
        "about": "The thread that runs through all of Emerson's essays: the imperative to trust one's own deepest intuitions over every external authority -- tradition, institution, opinion, even consistency with one's own past. Self-trust is not selfishness but fidelity to the divine spark within. Conformity is spiritual suicide. These passages are the manifesto of American individualism.",
        "for_readers": "Self-trust is Emerson's deepest theme. He argues that each person has access to the universal mind, and that trusting this inner voice is not arrogance but obedience to the highest authority. The implications are radical: no church, no state, no tradition has more authority than the individual soul. These passages explain both the liberating and the dangerous sides of American individualism.",
        "patterns": [
            "trust thyself",
            "self-reliance",
            "nonconformist",
            "foolish consistency",
            "hobgoblin",
            "imitation is suicide",
            "envy is ignorance",
            "your own thought",
            "believe your own thought",
            "the great man is he who in the midst of the crowd",
            "whoso would be a man must be a nonconformist",
        ],
    },
    {
        "id": "theme-universal-mind",
        "name": "The Universal Mind and Over-Soul",
        "about": "Emerson's metaphysics: there is one mind common to all individual minds, one soul underlying all individual souls. This Over-Soul is not a personal God but an impersonal divine presence in which all beings participate. History, nature, and art are all expressions of this universal mind. In moments of insight, the individual recognizes their unity with the whole.",
        "for_readers": "The Over-Soul is Emerson's answer to the question of meaning. He does not argue for its existence; he testifies to the experience of it -- moments when the boundaries of the self dissolve and one feels connected to something infinitely larger. These passages draw on Neoplatonism, Hindu philosophy, and Quaker inner light doctrine, fused into something uniquely Emersonian.",
        "patterns": [
            "over-soul",
            "universal mind",
            "one mind common",
            "universal soul",
            "divine",
            "revelation",
            "the soul",
            "unity",
            "transcendent",
            "eternal",
            "infinite",
        ],
    },
    {
        "id": "theme-nature-and-law",
        "name": "Nature, Compensation, and Cosmic Law",
        "about": "Emerson's conviction that the universe is governed by moral laws as exact as physical ones. Compensation, polarity, balance -- these are not metaphors but descriptions of how reality works. Every action produces its reaction; every excess its correction; every gift its price. Nature is the visible expression of invisible spiritual law.",
        "for_readers": "These passages reveal Emerson's faith in cosmic justice. He believes that the universe is fundamentally fair -- not through divine intervention but through the structure of reality itself. His examples range from physics (action and reaction) to ethics (crime and punishment) to nature (winter and spring). The implications are simultaneously comforting and challenging: nothing is free, but nothing is lost.",
        "patterns": [
            "compensation",
            "polarity",
            "action and reaction",
            "balance",
            "nature",
            "law",
            "cause and effect",
            "every excess causes a defect",
            "retribution",
            "the dice of god are always loaded",
        ],
    },
    {
        "id": "theme-growth-and-circles",
        "name": "Growth, Circles, and Perpetual Becoming",
        "about": "Emerson's philosophy of perpetual growth. No truth is final; no achievement is permanent; every circle is contained within a larger circle. The healthy soul is always outgrowing its previous forms. Stagnation is death; growth is the only evidence of life. These passages celebrate restlessness, experimentation, and the courage to abandon what has been achieved for what has not yet been imagined.",
        "for_readers": "Growth is Emerson's ethical imperative. He demands that we never settle into comfortable certainties but always push toward the next circle of understanding. This is exhilarating but also exhausting -- Emerson offers no rest, no final destination, only perpetual becoming. His philosophy anticipates pragmatism, process philosophy, and the modern emphasis on growth mindset.",
        "patterns": [
            "circle",
            "horizon",
            "new prospect",
            "outgrow",
            "growth",
            "becoming",
            "transition",
            "abandonment",
            "new thought",
            "leave all",
        ],
    },
]


def build_grammar(essays_data):
    items = []
    sort_order = 0
    essay_item_ids = {}

    for essay in essays_data:
        paragraphs = split_into_paragraphs(essay["text"])
        essay_item_ids[essay["slug"]] = []

        for i, para in enumerate(paragraphs):
            sort_order += 1
            para_id = f"{essay['prefix']}-{i+1:02d}"
            name = first_sentence_name(para)

            items.append({
                "id": para_id,
                "name": name,
                "level": 1,
                "category": essay["slug"],
                "sort_order": sort_order,
                "sections": {
                    "Passage": para,
                },
                "keywords": [],
                "metadata": {
                    "essay": essay["title"],
                    "paragraph_number": i + 1,
                },
            })
            essay_item_ids[essay["slug"]].append(para_id)

    # L2: Essay groups
    for essay in essays_data:
        sort_order += 1
        ids = essay_item_ids[essay["slug"]]
        about_data = ESSAY_ABOUTS.get(essay["slug"], {})

        items.append({
            "id": f"essay-{essay['slug']}",
            "name": essay["title"],
            "level": 2,
            "category": "essay",
            "relationship_type": "emergence",
            "composite_of": ids,
            "sort_order": sort_order,
            "sections": {
                "About": about_data.get("about", f"Essay: {essay['title']}"),
                "For Readers": about_data.get("for_readers", ""),
            },
            "keywords": [],
            "metadata": {
                "paragraph_count": len(ids),
            },
        })

    # L2: Thematic groups
    all_l1 = [item for item in items if item["level"] == 1]

    def find_paragraphs_matching(patterns):
        matched = []
        for item in all_l1:
            text = item["sections"]["Passage"].lower()
            for pat in patterns:
                if pat.lower() in text:
                    if item["id"] not in matched:
                        matched.append(item["id"])
                    break
        return matched

    for theme in THEMATIC_GROUPS:
        sort_order += 1
        composite = find_paragraphs_matching(theme["patterns"])

        items.append({
            "id": theme["id"],
            "name": theme["name"],
            "level": 2,
            "category": "theme",
            "relationship_type": "emergence",
            "composite_of": composite,
            "sort_order": sort_order,
            "sections": {
                "About": theme["about"],
                "For Readers": theme["for_readers"],
            },
            "keywords": [],
            "metadata": {
                "passage_count": len(composite),
            },
        })

    # L3: Meta
    sort_order += 1
    all_l2_ids = [item["id"] for item in items if item["level"] == 2]
    items.append({
        "id": "meta-essays-emerson",
        "name": "Essays: First Series",
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_l2_ids,
        "sort_order": sort_order,
        "sections": {
            "About": "Ralph Waldo Emerson's Essays: First Series (1841) is the founding document of American Transcendentalism and one of the most influential works of philosophy in the English language. Across twelve essays -- from the famous Self-Reliance to the mystical Over-Soul to the restless Circles -- Emerson develops his vision of the individual soul as a direct channel to the universal mind. His message is at once simple and radical: trust yourself, for what is true for you is true for all. No institution, no tradition, no authority is higher than the individual's own deepest intuition. The essays move between practical counsel (Prudence), moral philosophy (Compensation, Heroism), metaphysics (The Over-Soul, Circles), and aesthetics (Art), united by Emerson's conviction that the universe is fundamentally spiritual, fundamentally just, and fundamentally knowable through the individual soul.",
        },
        "keywords": [],
        "metadata": {
            "essay_count": len(essays_data),
            "theme_count": len(THEMATIC_GROUPS),
        },
    })

    return items


def main():
    with open(SEED, "r", encoding="utf-8") as f:
        raw = f.read()

    text = strip_gutenberg(raw)

    boundaries, lines = find_essay_boundaries(text)
    print(f"Found {len(boundaries)} essays:")
    for line_num, essay in boundaries:
        print(f"  Line {line_num}: {essay['title']}")

    essays_data = extract_essay_text(boundaries, lines)

    total_paragraphs = 0
    for essay in essays_data:
        paras = split_into_paragraphs(essay["text"])
        total_paragraphs += len(paras)
        print(f"  {essay['title']}: {len(paras)} paragraphs")

    print(f"Total paragraphs: {total_paragraphs}")

    items = build_grammar(essays_data)

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Ralph Waldo Emerson", "date": "1841", "note": "Author"},
            ]
        },
        "name": "Essays: First Series",
        "description": "Ralph Waldo Emerson's Essays: First Series (1841) -- the founding text of American Transcendentalism. Twelve essays that redefined the relationship between the individual and the universe. From the famous Self-Reliance ('Trust thyself: every heart vibrates to that iron string') to the mystical Over-Soul ('Within man is the soul of the whole') to the restless Circles ('every action admits of being outdone'), Emerson argues that each person has direct access to the divine mind and owes allegiance to no authority but their own deepest intuition. These essays shaped Thoreau, Whitman, Nietzsche, William James, and the entire tradition of American individualism.\n\nSource: Project Gutenberg eBook #2944 (https://www.gutenberg.org/ebooks/2944)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Photographs and daguerreotypes of Emerson by various artists. Illustrations of the Concord landscape. Pre-Raphaelite art (Emerson's aesthetic contemporaries).",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["philosophy", "transcendentalism", "self-knowledge", "individualism", "spirituality", "public-domain", "full-text"],
        "roots": ["self-knowledge"],
        "shelves": ["mirror"],
        "lineages": ["Linehan"],
        "worldview": "non-dual",
        "items": items,
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    l1 = sum(1 for i in items if i["level"] == 1)
    l2 = sum(1 for i in items if i["level"] == 2)
    l3 = sum(1 for i in items if i["level"] == 3)
    print(f"\nGrammar written to {OUTPUT}")
    print(f"  L1: {l1} paragraphs, L2: {l2} groups, L3: {l3} meta")
    print(f"  Total items: {len(items)}")

    all_ids = {item["id"] for item in items}
    errors = 0
    for item in items:
        if "composite_of" in item:
            for ref in item["composite_of"]:
                if ref not in all_ids:
                    print(f"  ERROR: {item['id']} references non-existent {ref}")
                    errors += 1
    if errors == 0:
        print("  All composite_of references valid.")
    else:
        print(f"  {errors} reference errors found!")

    print("\nThematic group sizes:")
    for item in items:
        if item["level"] == 2 and item["category"] == "theme":
            print(f"  {item['name']}: {len(item['composite_of'])} passages")


if __name__ == "__main__":
    main()
