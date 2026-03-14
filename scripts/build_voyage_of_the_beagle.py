#!/usr/bin/env python3
"""
Build grammar.json for The Voyage of the Beagle by Charles Darwin.

Source: Project Gutenberg eBook #944
Author: Charles Darwin (1839, revised 1845)

Structure:
- L1: 21 chapters (each covering a geographical location/leg of the voyage)
- L2: Regional groupings (5 regions) + thematic groupings
- L3: Meta-categories
"""

import json
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SEED_PATH = PROJECT_ROOT / "seeds" / "voyage-of-the-beagle.txt"
OUTPUT_DIR = PROJECT_ROOT / "grammars" / "voyage-of-the-beagle"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"

# Chapter definitions
CHAPTER_TITLES = [
    "St. Jago -- Cape de Verd Islands",
    "Rio de Janeiro",
    "Maldonado",
    "Rio Negro to Bahia Blanca",
    "Bahia Blanca",
    "Bahia Blanca to Buenos Ayres",
    "Buenos Ayres and St. Fe",
    "Banda Oriental and Patagonia",
    "Santa Cruz, Patagonia, and the Falkland Islands",
    "Tierra del Fuego",
    "Strait of Magellan -- Climate of the Southern Coasts",
    "Central Chile",
    "Chiloe and Chonos Islands",
    "Chiloe and Concepcion: Great Earthquake",
    "Passage of the Cordillera",
    "Northern Chile and Peru",
    "Galapagos Archipelago",
    "Tahiti and New Zealand",
    "Australia",
    "Keeling Island -- Coral Formations",
    "Mauritius to England",
]

CHAPTER_IDS = [
    "st-jago-cape-de-verd",
    "rio-de-janeiro",
    "maldonado",
    "rio-negro-to-bahia-blanca",
    "bahia-blanca",
    "bahia-blanca-to-buenos-ayres",
    "buenos-ayres-and-st-fe",
    "banda-oriental-and-patagonia",
    "santa-cruz-patagonia-falklands",
    "tierra-del-fuego",
    "strait-of-magellan",
    "central-chile",
    "chiloe-and-chonos-islands",
    "chiloe-and-concepcion-earthquake",
    "passage-of-the-cordillera",
    "northern-chile-and-peru",
    "galapagos-archipelago",
    "tahiti-and-new-zealand",
    "australia",
    "keeling-island-coral-formations",
    "mauritius-to-england",
]

CHAPTER_KEYWORDS = [
    ["cape-verde", "volcanic", "sea-life", "tropics", "sailing"],
    ["brazil", "tropics", "forest", "slavery", "insects"],
    ["uruguay", "birds", "mammals", "hunting", "gauchos"],
    ["argentina", "indians", "pampas", "salt-lakes", "flamingoes"],
    ["fossils", "megatheria", "extinction", "geology", "quadrupeds"],
    ["argentina", "gauchos", "pampas", "revolution", "journey"],
    ["argentina", "geology", "estancias", "fossils", "rivers"],
    ["uruguay", "patagonia", "guanaco", "geology", "zoology"],
    ["patagonia", "falklands", "condor", "geology", "river"],
    ["fuegians", "indigenous", "beagle-channel", "glaciers", "survival"],
    ["magellan", "climate", "forests", "glaciers", "kelp"],
    ["chile", "mining", "earthquakes", "andes", "geology"],
    ["chiloe", "forests", "rain", "islands", "potatoes"],
    ["earthquake", "concepcion", "tsunami", "geology", "destruction"],
    ["andes", "cordillera", "fossils", "geology", "altitude"],
    ["chile", "peru", "desert", "mining", "nitrate"],
    ["galapagos", "tortoises", "finches", "iguanas", "species"],
    ["tahiti", "coral-reefs", "missionaries", "new-zealand", "maori"],
    ["australia", "aborigines", "kangaroo", "platypus", "sydney"],
    ["coral", "atoll", "reef-formation", "subsidence", "coconut"],
    ["mauritius", "st-helena", "brazil", "return", "homecoming"],
]


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    start_idx = text.find(start_marker)
    if start_idx >= 0:
        start_idx = text.index("\n", start_idx) + 1
    else:
        start_idx = 0
    end_idx = text.find(end_marker)
    if end_idx < 0:
        end_idx = len(text)
    return text[start_idx:end_idx]


def strip_front_matter(text):
    """Remove title page, preface, and about the online edition.

    The actual text begins at CHAPTER I.
    """
    match = re.search(r'^CHAPTER I\s*$', text, re.MULTILINE)
    if match:
        return text[match.start():]
    return text


def strip_footnotes(text):
    """Remove footnote references [1], [2] etc. from the text body.

    Note: Footnotes in the Beagle are collected at chapter ends.
    We keep them as they are part of Darwin's supplementary observations.
    We only clean up the inline reference markers.
    """
    # Remove inline [N] references
    text = re.sub(r'\s*\[(\d+)\]', '', text)
    return text


def parse_chapters(text):
    """Parse the Voyage into 21 chapters."""
    chapters = []

    # Find all chapter headings
    chapter_pattern = re.compile(r'^CHAPTER\s+([IVXLC]+)\s*$', re.MULTILINE)
    matches = list(chapter_pattern.finditer(text))

    for i, match in enumerate(matches):
        start = match.start()
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        chunk = text[start:end].strip()
        lines = chunk.split('\n')

        # Skip the "CHAPTER X" line, blank line, and title line
        # Then skip the synopsis/topic line(s) and blank lines
        text_start = 0
        found_title = False
        blank_after_title = 0
        for j, line in enumerate(lines):
            if j == 0:
                continue  # "CHAPTER X"
            if not found_title and line.strip():
                found_title = True
                continue  # title line
            if found_title and not line.strip():
                blank_after_title += 1
                continue
            if found_title and blank_after_title >= 1 and line.strip():
                # Check if this looks like a synopsis line (topics separated by --)
                # Synopsis lines typically have many -- separators or are in a specific format
                if '--' in line or (j < 10 and not line[0].isupper()):
                    continue
                text_start = j
                break

        # More robust: find the first paragraph that starts with a capital letter
        # after at least one blank line following the synopsis
        found_synopsis_end = False
        for j, line in enumerate(lines):
            if j < 3:
                continue
            stripped = line.strip()
            if not stripped:
                if found_synopsis_end:
                    continue
                # Check if previous non-blank lines looked like synopsis
                found_synopsis_end = True
                continue
            if found_synopsis_end and stripped and stripped[0].isupper():
                text_start = j
                break

        chapter_text = '\n'.join(lines[text_start:]).strip()
        # Clean up multiple blank lines
        chapter_text = re.sub(r'\n{3,}', '\n\n', chapter_text)
        # Remove [Illustration] markers if any
        chapter_text = re.sub(r'\[Illustration[^\]]*\]', '', chapter_text)
        chapter_text = re.sub(r'\n{3,}', '\n\n', chapter_text)

        chapters.append({
            'index': i,
            'text': chapter_text,
        })

    return chapters


# Regional groupings for L2
REGIONS = [
    {
        "id": "region-atlantic-islands",
        "name": "Atlantic Islands and Brazil",
        "chapters": ["st-jago-cape-de-verd", "rio-de-janeiro"],
        "about": "The Beagle's first landfall and Darwin's introduction to tropical natural history. At St. Jago in the Cape Verde Islands, Darwin sees his first volcanic geology and tropical marine life. In Brazil, he encounters the overwhelming richness of tropical forests — and the horror of slavery, which marks him for life.",
        "for_readers": "These opening chapters show Darwin learning to see. His wonder at the tropical forest is infectious, and his revulsion at slavery is one of the book's most powerful moral moments.",
    },
    {
        "id": "region-argentina-uruguay",
        "name": "Argentina and Uruguay",
        "chapters": [
            "maldonado", "rio-negro-to-bahia-blanca", "bahia-blanca",
            "bahia-blanca-to-buenos-ayres", "buenos-ayres-and-st-fe",
            "banda-oriental-and-patagonia",
        ],
        "about": "Darwin's long exploration of the Argentine pampas and Patagonian coast. He rides with gauchos, discovers enormous fossils of extinct mammals (Megatherium, Mylodon, Toxodon), witnesses the aftermath of General Rosas's war against indigenous peoples, and begins to think deeply about extinction and the relationship between living and fossil species.",
        "for_readers": "The Argentine chapters are adventure writing at its finest — Darwin on horseback with gauchos, sleeping under the stars, discovering giant fossils. Bahia Blanca (Chapter V) is where the fossil discoveries begin to reshape his thinking about species.",
    },
    {
        "id": "region-patagonia-tierra-del-fuego",
        "name": "Patagonia and Tierra del Fuego",
        "chapters": [
            "santa-cruz-patagonia-falklands",
            "tierra-del-fuego",
            "strait-of-magellan",
        ],
        "about": "The wild southern tip of South America — glaciers, storms, the Fuegians, and the strange ecology of the subantarctic. Darwin's encounters with the indigenous Fuegians raise profound questions about human nature and civilization. The Beagle Channel and Strait of Magellan provide some of the voyage's most dramatic scenery.",
        "for_readers": "Tierra del Fuego (Chapter X) is among the most remarkable chapters, describing Darwin's encounter with people living at the extreme edge of human habitation. His complex, often contradictory responses to the Fuegians make for fascinating reading.",
    },
    {
        "id": "region-chile-andes",
        "name": "Chile and the Andes",
        "chapters": [
            "central-chile", "chiloe-and-chonos-islands",
            "chiloe-and-concepcion-earthquake", "passage-of-the-cordillera",
            "northern-chile-and-peru",
        ],
        "about": "Darwin witnesses one of the great earthquakes of the 19th century at Concepcion, crosses the Andes on mule-back, and finds marine fossils at 14,000 feet — proof that the mountains were once beneath the sea. These chapters transform his understanding of geological time and the dynamic nature of the Earth's surface.",
        "for_readers": "The earthquake chapter (XIV) is unforgettable eyewitness journalism. The Cordillera crossing (XV) shows Darwin as mountaineer-geologist, reading the story of continental uplift in the rocks. These chapters are where Darwin the geologist is at his most brilliant.",
    },
    {
        "id": "region-pacific-and-homeward",
        "name": "Pacific Islands and Homeward",
        "chapters": [
            "galapagos-archipelago", "tahiti-and-new-zealand",
            "australia", "keeling-island-coral-formations",
            "mauritius-to-england",
        ],
        "about": "The most famous leg of the voyage: the Galapagos, where Darwin observes the unique tortoises, iguanas, and finches that will later crystallize his theory of evolution. Then onward through Tahiti, New Zealand, Australia, and the coral atolls of Keeling Island (where he develops his theory of reef formation), before the long journey home.",
        "for_readers": "The Galapagos chapter (XVII) is the one everyone knows, and it lives up to its reputation — the tortoises, the marine iguanas, the mockingbirds that differ island to island. But don't skip Keeling Island (XX), where Darwin's theory of coral reef formation by subsidence is a masterpiece of geological reasoning.",
    },
]


def build_grammar():
    raw = SEED_PATH.read_text(encoding="utf-8")
    text = strip_gutenberg(raw)
    text = strip_front_matter(text)
    # Don't strip footnotes entirely — they contain valuable Darwin observations
    # Just remove inline [N] markers
    text = strip_footnotes(text)

    chapters = parse_chapters(text)
    print(f"Parsed {len(chapters)} chapters (expected 21)")

    items = []
    sort_order = 0

    # L1: Individual chapters
    for i, ch in enumerate(chapters):
        sort_order += 1
        chapter_id = CHAPTER_IDS[i]
        chapter_name = CHAPTER_TITLES[i]
        keywords = CHAPTER_KEYWORDS[i]

        items.append({
            "id": chapter_id,
            "name": chapter_name,
            "sort_order": sort_order,
            "level": 1,
            "category": "chapter",
            "sections": {
                "Text": ch['text'],
            },
            "keywords": keywords,
            "metadata": {
                "chapter_number": i + 1,
            }
        })
        print(f"  Ch {i+1:2d}: {chapter_name} ({len(ch['text'])} chars)")

    # L2: Regional groupings
    all_region_ids = []
    for region in REGIONS:
        sort_order += 1
        region_id = region["id"]
        all_region_ids.append(region_id)

        items.append({
            "id": region_id,
            "name": region["name"],
            "sort_order": sort_order,
            "level": 2,
            "category": "region",
            "relationship_type": "emergence",
            "composite_of": region["chapters"],
            "sections": {
                "About": region["about"],
                "For Readers": region["for_readers"],
            },
            "keywords": [],
            "metadata": {
                "chapter_count": len(region["chapters"]),
            }
        })

    # L3: The complete voyage
    sort_order += 1
    items.append({
        "id": "voyage-of-the-beagle-complete",
        "name": "The Voyage of the Beagle",
        "sort_order": sort_order,
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_region_ids,
        "sections": {
            "About": "Charles Darwin's Voyage of the Beagle (1839, revised 1845) is the journal of a five-year circumnavigation that changed the course of science. As naturalist aboard HMS Beagle (1831-1836), the 22-year-old Darwin observed the geology, flora, fauna, and peoples of South America, the Galapagos, the Pacific islands, and beyond. The book is at once a travel adventure, a work of natural history, a geological treatise, and the intellectual autobiography of a young man whose observations would lead to the theory of evolution. Every chapter brims with wonder, meticulous observation, and the dawning realization that the living world is not fixed but mutable.",
            "For Readers": "The Voyage is Darwin's most readable book — vivid, adventurous, and full of personality. Read it chronologically to follow the journey, or browse by region. The Argentine chapters for gaucho adventure and giant fossils. Tierra del Fuego for human drama. The Galapagos for the seeds of evolution. The earthquake at Concepcion for geological dynamism. The coral atolls for elegant theory. Darwin's prose is clear and often beautiful, and his sense of wonder never flags across 21 chapters and five years of exploration.",
        },
        "keywords": ["voyage", "beagle", "darwin", "travel", "natural-history", "exploration"],
        "metadata": {}
    })

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "Charles Darwin",
                    "date": "1839",
                    "note": "Author (revised 1845)"
                }
            ]
        },
        "name": "The Voyage of the Beagle",
        "description": "Charles Darwin's journal of his five-year circumnavigation aboard HMS Beagle (1831-1836) — one of the greatest travel and natural history books ever written. In 21 chapters following the voyage from the Cape Verde Islands through South America, the Galapagos, the Pacific, and home, Darwin records the geology, wildlife, and peoples he encountered. These observations laid the groundwork for the theory of evolution by natural selection.\n\nSource: Project Gutenberg eBook #944 (https://www.gutenberg.org/ebooks/944)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: Conrad Martens' watercolors and sketches from the Beagle voyage. John Gould's ornithological illustrations from The Zoology of the Voyage of H.M.S. Beagle (1838-1843). Robert FitzRoy's charts and coastal profiles. Period maps of the Beagle's route.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["travel", "natural-history", "science", "exploration", "ecology", "geology", "public-domain", "full-text"],
        "roots": ["ecology-nature"],
        "shelves": ["earth"],
        "lineages": ["Shrei"],
        "worldview": "naturalist",
        "items": items,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    l1 = sum(1 for i in items if i["level"] == 1)
    l2 = sum(1 for i in items if i["level"] == 2)
    l3 = sum(1 for i in items if i["level"] == 3)
    print(f"\nGrammar written to {OUTPUT_PATH}")
    print(f"  L1: {l1} chapters, L2: {l2} regions, L3: {l3} meta")
    print(f"  Total items: {len(items)}")


if __name__ == "__main__":
    build_grammar()
