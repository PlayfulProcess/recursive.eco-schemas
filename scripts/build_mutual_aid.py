#!/usr/bin/env python3
"""
Parse Mutual Aid: A Factor of Evolution by Peter Kropotkin (Gutenberg #4341, 1902)
into a grammar.json.

Structure:
- L1: Paragraphs within each chapter (id like "intro-para-01", "ch1-para-01", etc.)
- L2: Chapter emergence groups + thematic groups
- L3: Meta-category connecting all
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "mutual-aid.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "mutual-aid")
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


CHAPTERS = [
    {
        "slug": "introduction",
        "prefix": "intro-para",
        "title": "Introduction",
        "header_pattern": r"^INTRODUCTION$",
    },
    {
        "slug": "ch1-animals",
        "prefix": "ch1-para",
        "title": "Mutual Aid Among Animals",
        "header_pattern": r"^CHAPTER I$",
    },
    {
        "slug": "ch2-animals-continued",
        "prefix": "ch2-para",
        "title": "Mutual Aid Among Animals (continued)",
        "header_pattern": r"^CHAPTER II$",
    },
    {
        "slug": "ch3-savages",
        "prefix": "ch3-para",
        "title": "Mutual Aid Among Savages",
        "header_pattern": r"^CHAPTER III$",
    },
    {
        "slug": "ch4-barbarians",
        "prefix": "ch4-para",
        "title": "Mutual Aid Among the Barbarians",
        "header_pattern": r"^CHAPTER IV$",
    },
    {
        "slug": "ch5-medieval-city",
        "prefix": "ch5-para",
        "title": "Mutual Aid in the Mediaeval City",
        "header_pattern": r"^CHAPTER V$",
    },
    {
        "slug": "ch6-medieval-city-continued",
        "prefix": "ch6-para",
        "title": "Mutual Aid in the Mediaeval City (continued)",
        "header_pattern": r"^CHAPTER VI$",
    },
    {
        "slug": "ch7-ourselves",
        "prefix": "ch7-para",
        "title": "Mutual Aid Amongst Ourselves",
        "header_pattern": r"^CHAPTER VII$",
    },
    {
        "slug": "ch8-ourselves-continued",
        "prefix": "ch8-para",
        "title": "Mutual Aid Amongst Ourselves (continued)",
        "header_pattern": r"^CHAPTER VIII$",
    },
    {
        "slug": "conclusion",
        "prefix": "conclusion-para",
        "title": "Conclusion",
        "header_pattern": r"^CONCLUSION$",
    },
]


def find_chapter_boundaries(text):
    """Find chapter start lines."""
    lines = text.split('\n')
    boundaries = []

    for ch in CHAPTERS:
        pattern = re.compile(ch["header_pattern"])
        for i, line in enumerate(lines):
            stripped = line.strip()
            if pattern.match(stripped):
                boundaries.append((i, ch))
                break

    boundaries.sort(key=lambda x: x[0])
    return boundaries, lines


def extract_chapter_text(boundaries, lines):
    """Extract text for each chapter."""
    chapters = []
    for idx, (start_line, ch) in enumerate(boundaries):
        # Skip header lines: chapter number, subtitle, synopsis lines
        content_start = start_line + 1
        # Skip blank lines, ALL-CAPS subtitle lines, and synopsis lines
        while content_start < len(lines):
            stripped = lines[content_start].strip()
            if not stripped:
                content_start += 1
                continue
            # Skip MUTUAL AID AMONG... subtitle
            if stripped.startswith("MUTUAL AID") and stripped == stripped.upper():
                content_start += 1
                continue
            # Skip CONCLUSION header continuation
            if stripped == stripped.upper() and len(stripped) > 3 and not any(c.islower() for c in stripped):
                content_start += 1
                continue
            # Skip synopsis lines (short italic-style summaries with periods and dashes)
            # These appear right after chapter subtitles, listing topics
            if content_start < start_line + 10 and ('--' in stripped or stripped.count('.') > 2) and len(stripped) < 300:
                # Check if it looks like a synopsis (multiple topic phrases separated by periods/dashes)
                content_start += 1
                continue
            break

        if idx + 1 < len(boundaries):
            end_line = boundaries[idx + 1][0]
        else:
            end_line = len(lines)

        chapter_text = '\n'.join(lines[content_start:end_line]).strip()
        chapters.append({
            "slug": ch["slug"],
            "prefix": ch["prefix"],
            "title": ch["title"],
            "text": chapter_text,
        })

    return chapters


def split_into_paragraphs(text):
    """Split text into paragraphs."""
    raw_paragraphs = re.split(r'\n\s*\n', text)
    paragraphs = []

    for p in raw_paragraphs:
        cleaned = p.strip()
        if not cleaned:
            continue
        # Skip footnote markers and very short fragments
        if len(cleaned) < 20:
            continue
        # Skip lines that are just footnote references like [1], [2]
        if re.match(r'^\[\d+\]$', cleaned):
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


THEMATIC_GROUPS = [
    {
        "id": "theme-cooperation-in-nature",
        "name": "Cooperation in Nature",
        "about": "Kropotkin's evidence for cooperation as a fundamental force in the animal kingdom. From ants and bees to eagles and pelicans, species survive not primarily through competition but through mutual support. These passages challenge the Social Darwinist misreading of evolution as pure competition, showing that sociability is itself a survival advantage -- the fittest are often those who cooperate best.",
        "for_readers": "These passages reframe evolution itself. Where Social Darwinists saw nature as 'red in tooth and claw,' Kropotkin saw cooperative hunting, shared nesting, collective migration, and mutual warning systems. His observations from Siberia carry the authority of direct field experience. The implications are radical: if cooperation is natural, then competitive individualism is not inevitable.",
        "patterns": [
            "mutual aid among animals",
            "sociability is as much a law of nature",
            "mutual support",
            "struggle for existence",
            "survival of the fittest",
            "ants and bees",
            "colonies of birds",
            "migration",
            "species which live solitarily",
            "sociable species",
            "hunting in common",
            "nesting colonies",
        ],
    },
    {
        "id": "theme-human-solidarity",
        "name": "Human Solidarity Through History",
        "about": "Kropotkin traces mutual aid through human history -- from tribal societies through barbarian villages to medieval guilds. At every stage, humans organized cooperatively: the clan, the village commune, the guild, the free city. These institutions were not imposed from above but grew from the instinct of mutual support. Their destruction by the centralizing state was not progress but loss.",
        "for_readers": "Kropotkin's historical argument is deeply subversive. Where liberal history sees the rise of the individual, and Marxist history sees class struggle, Kropotkin sees the repeated creation and destruction of cooperative institutions. The medieval guild was not a restraint on trade but a mutual aid society. The village commune was not primitive but sophisticated. The state did not create order; it destroyed it.",
        "patterns": [
            "village commune",
            "barbarian",
            "savage",
            "clan",
            "tribe",
            "guild",
            "mediaeval city",
            "free cities",
            "common law",
            "folk-moot",
            "mutual support among",
        ],
    },
    {
        "id": "theme-against-the-state",
        "name": "Against the State",
        "about": "Kropotkin's argument that the centralized state systematically destroyed the organic institutions of mutual aid -- the village commune, the guild, the free city -- and replaced them with atomized individuals dependent on state power. The state did not bring order out of chaos; it brought chaos by destroying the self-governing communities that maintained social cohesion through voluntary cooperation.",
        "for_readers": "This is Kropotkin the anarchist at his most pointed. He argues that every advance of state power came at the expense of cooperative self-governance. The Reformation, the absolute monarchies, the Jacobin state -- each centralized control while claiming to liberate. His critique anticipates modern arguments about the destruction of 'social capital' and the hollowing-out of civil society by both market and state.",
        "patterns": [
            "the state",
            "centralization",
            "roman empire",
            "absorbed all social functions",
            "destroy",
            "legislation",
            "individual submitted",
            "military authority",
            "absorption",
        ],
    },
    {
        "id": "theme-modern-mutual-aid",
        "name": "Modern Mutual Aid",
        "about": "Despite the state's efforts to atomize society, mutual aid persists in modern life -- in trade unions, cooperatives, friendly societies, lifeboat associations, and countless informal networks of neighborly help. Kropotkin argues that these are not charming survivals but the essential fabric of civilization, without which no society could function for a single day.",
        "for_readers": "These passages are Kropotkin at his most optimistic. He catalogues the astonishing variety of cooperative institutions that thrive despite hostility from both state and market: workers' unions, cooperative stores, mutual insurance societies, volunteer lifeboats, scientific associations. His point is that cooperation is not utopian but ordinary -- the most common, most essential, and least noticed feature of daily life.",
        "patterns": [
            "trade union",
            "cooperative",
            "friendly societ",
            "lifeboat",
            "labour",
            "working men",
            "strike",
            "association",
            "voluntary",
            "among ourselves",
        ],
    },
]


CHAPTER_ABOUTS = {
    "introduction": {
        "about": "Kropotkin's personal and intellectual genesis. Traveling through Siberia and Manchuria, he observed that animals survived not through competition but through cooperation. Kessler's lecture on the 'Law of Mutual Aid' confirmed his intuition: beside the law of mutual struggle, there is in nature a law of mutual support, far more important for progressive evolution. This introduction sets up the entire book's argument against Social Darwinism.",
        "for_readers": "The Introduction reveals Kropotkin as both scientist and radical. His argument begins not with theory but with observation: the frozen steppes of Siberia, the migrating deer, the cooperating birds. He positions himself against Huxley's 'gladiators' show' view of nature -- not to deny struggle, but to insist that cooperation is the more important factor in evolution and survival.",
    },
    "ch1-animals": {
        "about": "The evidence from the animal kingdom, Part I. Kropotkin surveys ants, bees, beetles, birds, and mammals, documenting cooperative behavior: shared nesting, collective hunting, mutual warning, cooperative child-rearing. He argues that sociable species are far more numerous and successful than solitary ones. Competition within species is the exception, not the rule; mutual aid is the norm.",
        "for_readers": "Kropotkin marshals an enormous catalogue of zoological evidence. Ants that share food, bees that sacrifice for the hive, eagles that hunt in pairs, parrots that post sentinels -- each example challenges the 'nature red in tooth and claw' narrative. His distinction between inter-species competition (real but limited) and intra-species cooperation (constant and vital) is the book's foundational insight.",
    },
    "ch2-animals-continued": {
        "about": "The evidence from the animal kingdom, Part II. Continuing through mammals and higher animals, Kropotkin shows that mutual aid extends to wolves, horses, elephants, monkeys, and many others. He addresses Darwin's own recognition that social instincts are among the most important factors in evolution, and argues that natural selection favors cooperative groups over competitive individuals.",
        "for_readers": "The second animal chapter moves to larger and more complex species. Wolves hunt in packs, horses defend their young collectively, elephants never abandon a wounded companion. Kropotkin's key argument: species that cooperate survive glaciation, drought, and predation better than those that compete internally. Evolution selects for sociability.",
    },
    "ch3-savages": {
        "about": "Mutual aid in early human societies. Kropotkin examines tribal peoples -- Bushmen, Hottentots, Eskimos, Aboriginal Australians, and others -- documenting their elaborate systems of sharing, collective decision-making, and mutual support. He challenges the Hobbesian myth of primitive savagery: early humans were not isolated brutes but deeply cooperative beings whose survival depended on mutual aid.",
        "for_readers": "Kropotkin's anthropological chapter overturns the 'nasty, brutish, and short' narrative. Tribal societies share food, adopt orphans, care for the elderly, and make decisions by consensus. His evidence, drawn from explorers and ethnographers, shows that the 'war of all against all' was a European projection onto peoples whose actual social life was far more cooperative than that of industrial Europe.",
    },
    "ch4-barbarians": {
        "about": "Mutual aid among the 'barbarian' peoples who built early civilizations. The village commune -- shared land, collective labor, mutual insurance against misfortune -- was the fundamental unit of social organization from ancient Germania to medieval Russia. Kropotkin shows how customary law, folk assemblies, and communal land tenure created stable, self-governing societies without centralized authority.",
        "for_readers": "The barbarian chapter is Kropotkin's counter-history of civilization. Where conventional history celebrates kings and conquerors, he celebrates the village commune: the Germanic mark, the Russian mir, the Swiss Allmend. These were not anarchic wastelands but highly organized cooperative societies with customary law, elected judges, and collective land management.",
    },
    "ch5-medieval-city": {
        "about": "The medieval free city as the apex of mutual aid in European history. Kropotkin argues that the guilds, communes, and free cities of the Middle Ages represented a flourishing of cooperative self-governance. Artisans organized in guilds, cities governed themselves through assemblies, and social insurance was provided through confraternities. The medieval city was not a stepping stone to modernity but a high point of human cooperation.",
        "for_readers": "This is perhaps Kropotkin's most original chapter. He rehabilitates the medieval guild not as a monopolistic restraint on trade but as a mutual aid society: caring for sick members, educating apprentices, maintaining quality, and providing a social safety net. The free city -- Florence, Bruges, Novgorod -- was a self-governing cooperative that produced cathedrals, universities, and great art.",
    },
    "ch6-medieval-city-continued": {
        "about": "The destruction of medieval mutual aid by the rising centralized state. Kings, aided by Roman-trained lawyers, systematically dismantled the guilds, communes, and free cities, replacing cooperative self-governance with bureaucratic control. The Reformation furthered this process by destroying the confraternities and communal institutions of the medieval church. What was called 'progress' was actually the destruction of cooperative institutions.",
        "for_readers": "The second medieval chapter tells the tragic side of the story. The free cities fell not because they were weak but because centralized states were more militarily powerful. Kings and emperors destroyed guilds, revoked city charters, and imposed royal courts. Kropotkin's argument is that the modern state was built on the ruins of cooperative institutions -- and that this was a catastrophic loss for human freedom.",
    },
    "ch7-ourselves": {
        "about": "Mutual aid in modern industrial society, Part I. Despite the state's efforts to atomize society and the economists' celebration of individualism, mutual aid persists everywhere: in trade unions, cooperatives, friendly societies, scientific associations, and countless informal networks. Kropotkin catalogues the astonishing variety of cooperative institutions that thrive in the hostile environment of modern capitalism.",
        "for_readers": "Kropotkin answers the objection that mutual aid is a thing of the past. Trade unions, cooperatives, mutual insurance societies, volunteer lifeboats, cycling clubs, scientific associations -- the modern world teems with cooperative institutions. His point is devastating: the very economists who preach individualism depend on mutual aid for their daily bread, their scientific knowledge, and their personal safety.",
    },
    "ch8-ourselves-continued": {
        "about": "Mutual aid in modern society, Part II. Kropotkin examines the growth of cooperatives, the labor movement, and voluntary associations, arguing that these represent not nostalgia for the past but the seeds of a future society organized on cooperative principles. The instinct of mutual aid is indestructible; crushed in one form, it reappears in another.",
        "for_readers": "The final substantive chapter is Kropotkin at his most prophetic. He sees in trade unions, consumer cooperatives, and voluntary associations the embryo of a new social order -- not imposed by revolution but growing organically from the human instinct for mutual support. His vision anticipates the cooperative movement, mutual aid networks, and commons-based peer production of our own time.",
    },
    "conclusion": {
        "about": "Kropotkin's summation. Mutual aid is not a sentimental ideal but a hard biological and historical fact. From ants to medieval guilds to modern trade unions, cooperation has been the decisive factor in evolution and civilization. The competitive individualism celebrated by Social Darwinists and laissez-faire economists is a temporary aberration, not the natural state of humanity. The instinct of mutual aid is the strongest guarantee of further evolution.",
        "for_readers": "The Conclusion brings together all of Kropotkin's evidence into a single argument: mutual aid is the main factor in progressive evolution, and those periods of history when cooperative institutions flourished were also the periods of greatest cultural and material advance. His final message is one of grounded hope: the instinct of mutual aid cannot be destroyed, only temporarily suppressed.",
    },
}


def build_grammar(chapters):
    items = []
    sort_order = 0
    chapter_item_ids = {}

    # L1: Paragraphs
    for ch in chapters:
        paragraphs = split_into_paragraphs(ch["text"])
        chapter_item_ids[ch["slug"]] = []

        for i, para in enumerate(paragraphs):
            sort_order += 1
            para_id = f"{ch['prefix']}-{i+1:02d}"
            name = first_sentence_name(para)

            items.append({
                "id": para_id,
                "name": name,
                "level": 1,
                "category": ch["slug"],
                "sort_order": sort_order,
                "sections": {
                    "Passage": para,
                },
                "keywords": [],
                "metadata": {
                    "chapter": ch["title"],
                    "paragraph_number": i + 1,
                },
            })
            chapter_item_ids[ch["slug"]].append(para_id)

    # L2: Chapter groups
    for ch in chapters:
        sort_order += 1
        ids = chapter_item_ids[ch["slug"]]
        about_data = CHAPTER_ABOUTS.get(ch["slug"], {})

        items.append({
            "id": f"chapter-{ch['slug']}",
            "name": ch["title"],
            "level": 2,
            "category": "chapter",
            "relationship_type": "emergence",
            "composite_of": ids,
            "sort_order": sort_order,
            "sections": {
                "About": about_data.get("about", f"Chapter: {ch['title']}"),
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
        "id": "meta-mutual-aid",
        "name": "Mutual Aid: A Factor of Evolution",
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_l2_ids,
        "sort_order": sort_order,
        "sections": {
            "About": "Peter Kropotkin's Mutual Aid: A Factor of Evolution (1902) is the great counter-argument to Social Darwinism. Drawing on his own field observations in Siberia and an enormous range of zoological, anthropological, and historical evidence, Kropotkin argues that cooperation -- not competition -- is the dominant factor in both biological evolution and human civilization. From ants and bees through tribal societies, medieval guilds, and modern trade unions, mutual aid has been the foundation of survival and progress. The book moves through three great domains: the animal kingdom (Chapters I-II), human history from tribal to medieval (Chapters III-VI), and modern society (Chapters VII-VIII), building a cumulative case that the competitive individualism celebrated by laissez-faire economists is a temporary aberration, not the natural state of life.",
        },
        "keywords": [],
        "metadata": {
            "chapter_count": len(chapters),
            "theme_count": len(THEMATIC_GROUPS),
        },
    })

    return items


def main():
    with open(SEED, "r", encoding="utf-8") as f:
        raw = f.read()

    text = strip_gutenberg(raw)

    boundaries, lines = find_chapter_boundaries(text)
    print(f"Found {len(boundaries)} chapters:")
    for line_num, ch in boundaries:
        print(f"  Line {line_num}: {ch['title']}")

    chapters = extract_chapter_text(boundaries, lines)

    total_paragraphs = 0
    for ch in chapters:
        paras = split_into_paragraphs(ch["text"])
        total_paragraphs += len(paras)
        print(f"  {ch['title']}: {len(paras)} paragraphs")

    print(f"Total paragraphs: {total_paragraphs}")

    items = build_grammar(chapters)

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Peter Kropotkin", "date": "1902", "note": "Author"},
            ]
        },
        "name": "Mutual Aid: A Factor of Evolution",
        "description": "Peter Kropotkin's Mutual Aid: A Factor of Evolution (1902) -- the foundational text of cooperative evolutionary theory. Against Social Darwinism's 'survival of the fittest' as justification for competitive individualism, Kropotkin marshals evidence from zoology, anthropology, and history to show that mutual aid -- not mutual struggle -- is the chief factor in evolution and civilization. From Siberian field observations to medieval guild records, this is the scientific case for cooperation as the natural state of life.\n\nSource: Project Gutenberg eBook #4341 (https://www.gutenberg.org/ebooks/4341)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Natural history illustrations from the 19th century. Ernst Haeckel's Art Forms in Nature. Medieval guild and city illustrations from illuminated manuscripts.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["politics", "philosophy", "science", "evolution", "cooperation", "anarchism", "public-domain", "full-text"],
        "roots": ["freedom-commons"],
        "shelves": ["resilience"],
        "lineages": ["Kelty"],
        "worldview": "rationalist",
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

    # Validate references
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
