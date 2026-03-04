#!/usr/bin/env python3
"""
Parse The Communist Manifesto (Marx & Engels, 1888 English edition, Gutenberg #61)
into a grammar.json.

Structure:
- L1: Individual paragraphs with chapter/section context
- L2: Preamble + 4 chapters as emergence groups, Chapter III subsections,
      and thematic groupings across chapters
- L3: "The Communist Manifesto" meta-item connecting everything
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "communist-manifesto.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "communist-manifesto")
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


def strip_front_matter(text):
    """Remove title page and table of contents, return text starting from 'A spectre'."""
    idx = text.find("A spectre is haunting Europe")
    if idx == -1:
        raise ValueError("Could not find start of preamble")
    return text[idx:].strip()


def split_into_sections(text):
    """Split the manifesto into preamble + 4 chapters.

    Chapter headers appear as:
      I.
      BOURGEOIS AND PROLETARIANS
    or
      IV.
      POSITION OF THE COMMUNISTS...
    """
    # Pattern: Roman numeral on its own line, followed by chapter title in caps
    chapter_pattern = re.compile(
        r'\n\s*\n\s*\n\s*\n*'  # multiple blank lines before
        r'(I{1,3}V?|IV|VI{0,3})\.\s*\n'  # Roman numeral + period on its own line
        r'([A-Z][A-Z\s,\-\']+(?:\n[A-Z][A-Z\s,\-\']+)*)\s*\n',  # Title in ALL CAPS (may span lines)
        re.MULTILINE
    )

    sections = []
    matches = list(chapter_pattern.finditer(text))

    if not matches:
        raise ValueError("Could not find any chapter headers")

    # Preamble is everything before the first chapter
    preamble_text = text[:matches[0].start()].strip()
    sections.append({
        'number': 0,
        'roman': '',
        'title': 'Preamble',
        'slug': 'preamble',
        'text': preamble_text
    })

    chapter_info = [
        (1, 'I', 'Bourgeois and Proletarians', 'bourgeois-and-proletarians'),
        (2, 'II', 'Proletarians and Communists', 'proletarians-and-communists'),
        (3, 'III', 'Socialist and Communist Literature', 'socialist-and-communist-literature'),
        (4, 'IV', 'Position of the Communists in Relation to the Various Existing Opposition Parties',
         'position-of-communists'),
    ]

    for i, match in enumerate(matches):
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        chapter_text = text[match.end():end_pos].strip()
        num, roman, title, slug = chapter_info[i]
        sections.append({
            'number': num,
            'roman': roman,
            'title': title,
            'slug': slug,
            'text': chapter_text
        })

    return sections


def split_paragraphs(text):
    """Split text into paragraphs on double newlines, filtering out empty ones."""
    paragraphs = re.split(r'\n\s*\n', text)
    result = []
    for p in paragraphs:
        # Join continuation lines (single newlines within a paragraph)
        cleaned = ' '.join(line.strip() for line in p.strip().split('\n') if line.strip())
        if cleaned:
            result.append(cleaned)
    return result


def merge_short_paragraphs(paragraphs, min_length=120):
    """Merge very short paragraphs with their neighbors to create more substantial items.

    Strategy:
    - If a paragraph is shorter than min_length, merge it with the next paragraph
    - The 10-point program (items starting with "1." through "10.") gets merged into one block
    - Short Q&A rhetorical pairs get merged together
    - Subsection headers are never merged (handled separately)
    """
    if not paragraphs:
        return paragraphs

    merged = []
    i = 0
    while i < len(paragraphs):
        current = paragraphs[i]

        # Detect the 10-point program: starts with "1. Abolition of property"
        if re.match(r'^1\.\s*Abolition of property in land', current):
            # Merge all numbered items until we hit a non-numbered paragraph
            program_parts = [current]
            j = i + 1
            while j < len(paragraphs):
                if re.match(r'^\d+\.', paragraphs[j]):
                    program_parts.append(paragraphs[j])
                    j += 1
                else:
                    break
            merged.append('\n\n'.join(program_parts))
            i = j
            continue

        # Skip subsection headers — don't merge them
        if is_subsection_header(current):
            merged.append(current)
            i += 1
            continue

        # If current paragraph is short, try to merge with next
        if len(current) < min_length and i + 1 < len(paragraphs):
            next_p = paragraphs[i + 1]
            # Don't merge across subsection headers
            if not is_subsection_header(next_p):
                merged.append(current + '\n\n' + next_p)
                i += 2
                continue

        merged.append(current)
        i += 1

    # Second pass: merge any remaining short paragraphs with previous
    final = []
    for p in merged:
        if is_subsection_header(p):
            final.append(p)
            continue
        if final and len(p) < min_length and not is_subsection_header(final[-1]):
            final[-1] = final[-1] + '\n\n' + p
        else:
            final.append(p)

    return final


def first_sentence(text, max_len=80):
    """Extract first sentence, truncated to max_len characters."""
    # Find sentence end
    m = re.search(r'[.!?](?:\s|$)', text)
    if m and m.end() <= max_len:
        return text[:m.end()].strip()
    # No sentence end found within limit, truncate at word boundary
    if len(text) <= max_len:
        return text
    truncated = text[:max_len]
    # Find last space
    last_space = truncated.rfind(' ')
    if last_space > 40:
        truncated = truncated[:last_space]
    return truncated + "..."


def identify_ch3_subsections(paragraphs):
    """Identify which paragraphs in Chapter III belong to which subsection.

    Subsection headers appear as paragraphs like:
    - "1. REACTIONARY SOCIALISM"
    - "_A. Feudal Socialism_"
    - "_B. Petty-Bourgeois Socialism_"
    - "_C. German, or \"True,\" Socialism_"
    - "2. CONSERVATIVE, OR BOURGEOIS, SOCIALISM"
    - "3. CRITICAL-UTOPIAN SOCIALISM AND COMMUNISM"

    Returns a list of (subsection_key, start_para_idx, end_para_idx) tuples.
    """
    # Track subsection boundaries
    subsection_markers = []

    for i, p in enumerate(paragraphs):
        text = p.strip()
        # Major subsection headers
        if re.match(r'^1\.\s*REACTIONARY SOCIALISM', text):
            subsection_markers.append(('reactionary-socialism', i))
        elif re.match(r'^2\.\s*CONSERVATIVE', text):
            subsection_markers.append(('conservative-bourgeois-socialism', i))
        elif re.match(r'^3\.\s*CRITICAL-UTOPIAN', text):
            subsection_markers.append(('critical-utopian-socialism', i))

    # Build ranges
    ranges = []
    for j, (key, start) in enumerate(subsection_markers):
        end = subsection_markers[j + 1][0] if j + 1 < len(subsection_markers) else None
        end_idx = subsection_markers[j + 1][1] if j + 1 < len(subsection_markers) else len(paragraphs)
        ranges.append((key, start, end_idx))

    return ranges


def is_subsection_header(text):
    """Check if a paragraph is a subsection header (not real content)."""
    text = text.strip()
    # Match patterns like "1. REACTIONARY SOCIALISM", "_A. Feudal Socialism_", etc.
    if re.match(r'^\d+\.\s*[A-Z][A-Z\s,\-]+$', text):
        return True
    if re.match(r'^_[A-Z]\.\s+.*_$', text):
        return True
    return False


def build_grammar():
    with open(SEED, 'r', encoding='utf-8') as f:
        raw = f.read()

    text = strip_gutenberg(raw)
    text = strip_front_matter(text)

    # Also strip the trailing "WORKING MEN OF ALL COUNTRIES, UNITE!" —
    # we'll include it as the last paragraph of chapter IV
    sections = split_into_sections(text)

    items = []
    sort_order = 0

    # Track paragraph IDs per chapter for L2 composite_of
    chapter_paragraph_ids = {}  # slug -> [ids]
    # Track Ch3 subsection paragraph IDs
    ch3_subsection_ids = {
        'reactionary-socialism': [],
        'conservative-bourgeois-socialism': [],
        'critical-utopian-socialism': [],
    }

    # IDs for thematic groupings (manually curated by paragraph ID)
    thematic_ids = {
        'class-struggle-history': [],
        'bourgeoisie-revolutionary-role': [],
        'communist-program': [],
        'critique-other-socialisms': [],
    }

    for section in sections:
        slug = section['slug']
        num = section['number']
        raw_paragraphs = split_paragraphs(section['text'])

        # Merge short paragraphs to get substantial items
        paragraphs = merge_short_paragraphs(raw_paragraphs)

        chapter_paragraph_ids[slug] = []
        prefix = 'preamble' if num == 0 else f'ch{num}'
        para_counter = 0

        # For Ch3 subsection tracking, use content-based markers
        current_ch3_subsection = None

        for i, para in enumerate(paragraphs):
            # Skip pure subsection headers
            if is_subsection_header(para):
                continue

            # Track Ch3 subsection boundaries by content
            if num == 3:
                if '1. REACTIONARY SOCIALISM' in para or 'REACTIONARY SOCIALISM' in para:
                    current_ch3_subsection = 'reactionary-socialism'
                elif '2. CONSERVATIVE' in para or 'CONSERVATIVE, OR BOURGEOIS, SOCIALISM' in para:
                    current_ch3_subsection = 'conservative-bourgeois-socialism'
                elif '3. CRITICAL-UTOPIAN' in para or 'CRITICAL-UTOPIAN SOCIALISM' in para:
                    current_ch3_subsection = 'critical-utopian-socialism'
                # Also detect subsection markers embedded in merged paragraphs
                if re.search(r'Feudal Socialism|Petty-Bourgeois Socialism|German.*True.*Socialism', para):
                    if current_ch3_subsection is None:
                        current_ch3_subsection = 'reactionary-socialism'

            para_counter += 1
            para_id = f"{prefix}-p{para_counter:02d}"
            name = first_sentence(para)

            item = {
                "id": para_id,
                "name": name,
                "sort_order": sort_order,
                "category": slug,
                "level": 1,
                "sections": {
                    "Passage": para
                },
                "keywords": [],
                "metadata": {
                    "chapter_number": num,
                    "paragraph_number": para_counter
                }
            }
            items.append(item)
            sort_order += 1
            chapter_paragraph_ids[slug].append(para_id)

            # Assign to Ch3 subsections
            if num == 3 and current_ch3_subsection:
                ch3_subsection_ids[current_ch3_subsection].append(para_id)

            # Assign to thematic groupings based on content heuristics
            lower = para.lower()

            # Class Struggle Through History — historical materialist paragraphs in Ch1
            if num == 1 and para_counter <= 5:
                # First few paragraphs of Ch1 are the famous historical materialism opening
                thematic_ids['class-struggle-history'].append(para_id)
            elif num == 0:
                # Preamble paragraphs about communism as a power
                pass
            elif num == 1 and ('history of' in lower and ('class' in lower or 'struggle' in lower)):
                thematic_ids['class-struggle-history'].append(para_id)
            elif num == 1 and ('feudal' in lower and 'bourgeois' in lower and 'epoch' in lower):
                thematic_ids['class-struggle-history'].append(para_id)

            # Bourgeoisie's Revolutionary Role — Ch1 paragraphs praising capitalism
            if num == 1 and any(phrase in lower for phrase in [
                'bourgeoisie, historically, has played a most revolutionary',
                'has put an end to all feudal',
                'has stripped of its halo',
                'has torn away from the family',
                'has disclosed how it came to pass',
                'cannot exist without constantly revolutionising',
                'need of a constantly expanding market',
                'through its exploitation of the world-market',
                'by the rapid improvement of all instruments',
                'has subjected the country to the rule',
                'keeps more and more doing away',
                'more massive and more colossal productive forces',
                'egyptian pyramids',
                'all that is solid melts into air',
            ]):
                thematic_ids['bourgeoisie-revolutionary-role'].append(para_id)

            # Communist Program — the 10 points and surrounding argument in Ch2
            if num == 2 and any(phrase in lower for phrase in [
                'abolition of private property',
                'proletariat will use its political supremacy',
                'despotic inroads',
                'following will be pretty generally applicable',
                'abolition of property in land',
                'heavy progressive',
                'abolition of all right of inheritance',
                'confiscation of the property',
                'centralisation of credit',
                'centralisation of the means of communication',
                'extension of factories',
                'equal liability of all to labour',
                'combination of agriculture',
                'free education for all children',
                'class distinctions have disappeared',
                'free development of each',
            ]):
                thematic_ids['communist-program'].append(para_id)

            # Critique of Other Socialisms — all of Ch3
            if num == 3:
                thematic_ids['critique-other-socialisms'].append(para_id)

    # Deduplicate thematic IDs
    for key in thematic_ids:
        thematic_ids[key] = list(dict.fromkeys(thematic_ids[key]))

    # === L2: Chapter emergence groups ===
    chapter_about = {
        'preamble': "The famous opening of the Manifesto, declaring that communism is already recognized as a power by all European governments. Marx and Engels announce their intention to publish their views openly, replacing the 'nursery tale of the Spectre of Communism' with a clear statement of communist aims.",
        'bourgeois-and-proletarians': "The longest and most analytically powerful chapter. It presents the Marxist theory of history as class struggle, traces the rise of the bourgeoisie from feudal society, catalogues capitalism's revolutionary achievements (globalization, urbanization, technological progress), and argues that capitalism produces its own gravediggers in the proletariat.",
        'proletarians-and-communists': "Defines the relationship of communists to the broader working-class movement and defends the communist program. Contains the famous declaration 'Abolition of private property' and the 10-point program for the transition period. Also addresses objections about the family, nationality, education, and culture.",
        'socialist-and-communist-literature': "A taxonomy of rival socialist movements, divided into three categories: Reactionary Socialism (feudal, petty-bourgeois, and German 'True' Socialism), Conservative/Bourgeois Socialism (reformism), and Critical-Utopian Socialism (Saint-Simon, Fourier, Owen). Each is analyzed and found wanting.",
        'position-of-communists': "The shortest chapter, outlining communist tactical positions in various countries (France, Switzerland, Poland, Germany) and ending with the famous call to action: 'The proletarians have nothing to lose but their chains. They have a world to win. WORKING MEN OF ALL COUNTRIES, UNITE!'"
    }

    chapter_titles = {
        'preamble': 'Preamble: A Spectre Is Haunting Europe',
        'bourgeois-and-proletarians': 'Chapter I: Bourgeois and Proletarians',
        'proletarians-and-communists': 'Chapter II: Proletarians and Communists',
        'socialist-and-communist-literature': 'Chapter III: Socialist and Communist Literature',
        'position-of-communists': 'Chapter IV: Position of the Communists',
    }

    for slug, title in chapter_titles.items():
        item = {
            "id": f"chapter-{slug}",
            "name": title,
            "sort_order": sort_order,
            "category": "chapters",
            "level": 2,
            "sections": {
                "About": chapter_about[slug],
                "How to Read": "Each paragraph is a self-contained argument or rhetorical move. Read them in sequence to follow the dialectical logic, or browse individually to find the famous passages."
            },
            "keywords": [],
            "metadata": {
                "relationship_type": "emergence"
            },
            "composite_of": chapter_paragraph_ids[slug]
        }
        items.append(item)
        sort_order += 1

    # === L2: Chapter III subsections ===
    ch3_sub_info = {
        'reactionary-socialism': {
            'name': 'Reactionary Socialism',
            'about': "Marx and Engels dissect three forms of backward-looking socialism: Feudal Socialism (aristocrats using socialist rhetoric to attack the bourgeoisie), Petty-Bourgeois Socialism (Sismondi and defenders of the old middle class), and German or 'True' Socialism (philosophers who translated French socialist ideas into abstract German philosophy, stripping them of revolutionary content)."
        },
        'conservative-bourgeois-socialism': {
            'name': 'Conservative, or Bourgeois, Socialism',
            'about': "A critique of reformist socialism — bourgeois thinkers who want to preserve capitalist society while removing its most objectionable features. Marx skewers philanthropists, humanitarians, and reformers who offer 'Free trade: for the benefit of the working class' while leaving the fundamental class relationship intact."
        },
        'critical-utopian-socialism': {
            'name': 'Critical-Utopian Socialism and Communism',
            'about': "A more respectful treatment of Saint-Simon, Fourier, and Owen, acknowledging their critical insights while arguing that their systems were necessarily utopian because they emerged before the proletariat had developed into an independent political force. Their disciples have become 'mere reactionary sects.'"
        },
    }

    for sub_key, info in ch3_sub_info.items():
        if ch3_subsection_ids[sub_key]:
            item = {
                "id": f"ch3-{sub_key}",
                "name": info['name'],
                "sort_order": sort_order,
                "category": "chapter-3-subsections",
                "level": 2,
                "sections": {
                    "About": info['about']
                },
                "keywords": [],
                "metadata": {
                    "relationship_type": "emergence"
                },
                "composite_of": ch3_subsection_ids[sub_key]
            }
            items.append(item)
            sort_order += 1

    # === L2: Thematic groupings ===
    thematic_info = {
        'class-struggle-history': {
            'name': 'Class Struggle Through History',
            'about': "Key paragraphs presenting Marx's theory of historical materialism — the argument that all history is the history of class struggles, from freeman and slave through lord and serf to bourgeois and proletarian. These passages trace how each epoch's mode of production generates the class that will overthrow it.",
            'how_to_read': "These paragraphs form the theoretical backbone of the Manifesto. They are best read as a sweeping historical narrative that tries to explain all of human history through one lens. Ask yourself: what does this framework illuminate, and what does it obscure?"
        },
        'bourgeoisie-revolutionary-role': {
            'name': "The Bourgeoisie's Revolutionary Role",
            'about': "Some of the most striking passages in all political writing — Marx's tribute to capitalism's transformative power. The bourgeoisie has 'accomplished wonders far surpassing Egyptian pyramids,' created world markets, drawn all nations into civilization, and generated productive forces beyond anything previously imaginable. 'All that is solid melts into air.'",
            'how_to_read': "These passages are remarkable for their admiration of the very system Marx seeks to overthrow. They show that Marxism is not a simple rejection of capitalism but a theory that capitalism is a necessary and revolutionary stage that creates the conditions for its own transcendence."
        },
        'communist-program': {
            'name': 'The Communist Program',
            'about': "The practical core of the Manifesto: the defense of the abolition of private property and the famous 10-point program (progressive income tax, centralization of credit, free public education, etc.). Many of these demands have since been adopted by capitalist democracies — a fact that would have both pleased and puzzled Marx.",
            'how_to_read': "Read these demands in their historical context — most were radical in 1848. Note which have been adopted (progressive taxation, free public education) and which have not (abolition of inheritance, industrial armies). This is where the Manifesto's legacy is most complex."
        },
        'critique-other-socialisms': {
            'name': 'Critique of Other Socialisms',
            'about': "Marx and Engels' taxonomy of rival socialist movements — feudal socialists, petty-bourgeois socialists, German 'True' Socialists, bourgeois reformers, and utopian socialists. Each is analyzed with characteristic wit and dismissed for failing to understand the historical dynamics of class struggle.",
            'how_to_read': "This chapter reveals Marx as a polemicist and political strategist. It maps the 1840s socialist landscape and shows how Marx positioned his 'scientific socialism' against all competitors. Many of these critiques remain relevant to debates within the left today."
        },
    }

    for theme_key, info in thematic_info.items():
        if thematic_ids[theme_key]:
            item = {
                "id": f"theme-{theme_key}",
                "name": info['name'],
                "sort_order": sort_order,
                "category": "themes",
                "level": 2,
                "sections": {
                    "About": info['about'],
                    "How to Read": info['how_to_read']
                },
                "keywords": [],
                "metadata": {
                    "relationship_type": "emergence"
                },
                "composite_of": thematic_ids[theme_key]
            }
            items.append(item)
            sort_order += 1

    # === L3: The Communist Manifesto as a whole ===
    all_l2_ids = [f"chapter-{s}" for s in chapter_titles.keys()]
    all_l2_ids += [f"ch3-{k}" for k in ch3_sub_info.keys() if ch3_subsection_ids[k]]
    all_l2_ids += [f"theme-{k}" for k in thematic_info.keys() if thematic_ids[k]]

    l3_item = {
        "id": "the-communist-manifesto",
        "name": "The Communist Manifesto",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "sections": {
            "About": "The Communist Manifesto (1848) by Karl Marx and Friedrich Engels is arguably the most influential political pamphlet ever written. In roughly 12,000 words, it lays out a theory of history as class struggle, a devastating analysis of capitalism's revolutionary dynamism, a program for communist revolution, and a polemic against rival socialisms. Its influence on the 20th century — for both liberation and oppression — is incalculable.",
            "Why It's on the 'Contested' Shelf": "This text is placed on the 'contested' shelf because intellectual honesty demands it. The Manifesto contains brilliant insights about capitalism's dynamics that remain relevant today — globalization, creative destruction, the commodification of everything. It also provided the theoretical framework for regimes that killed tens of millions. Both truths coexist. Reading it critically, with full awareness of its legacy, is more valuable than either uncritical embrace or reflexive dismissal.",
            "How to Read": "Start with Chapter I for the famous theory of history and the remarkable passages on capitalism's achievements. Chapter II contains the practical program. Chapter III is a map of 1840s socialist thought. Chapter IV is a brief call to action. The thematic groupings allow you to focus on specific arguments across the text."
        },
        "keywords": ["marxism", "class-struggle", "capitalism", "socialism", "revolution", "historical-materialism"],
        "metadata": {
            "relationship_type": "emergence"
        },
        "composite_of": all_l2_ids
    }
    items.append(l3_item)

    # === Build grammar ===
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Karl Marx", "date": "1848", "note": "Author"},
                {"name": "Friedrich Engels", "date": "1848/1888", "note": "Co-author, editor of 1888 English edition"}
            ]
        },
        "name": "The Communist Manifesto",
        "description": "The Communist Manifesto (1848) by Karl Marx and Friedrich Engels \u2014 the most influential political pamphlet in history. In four chapters, it argues that all history is the history of class struggle, analyzes the revolutionary role of the bourgeoisie, and calls for the abolition of private property. Placed on the 'contested' shelf: it is both a brilliant analysis of capitalism's dynamics AND a blueprint that was used to justify immense suffering. Both truths coexist.\n\nSource: Project Gutenberg eBook #61 (https://www.gutenberg.org/ebooks/61)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: 19th century political cartoons and broadsheets. Honor\u00e9 Daumier's lithographs of workers. Gustave Dor\u00e9's illustrations of London poverty. Soviet constructivist posters (early period, pre-Stalin).",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["philosophy", "politics", "economics", "contested", "public-domain", "full-text", "marxism", "class-struggle"],
        "roots": ["freedom-commons"],
        "shelves": ["contested"],
        "lineages": ["Kelty", "Andreotti"],
        "worldview": "dialectical",
        "items": items
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    # Print summary
    l1_items = [i for i in items if i['level'] == 1]
    l2_items = [i for i in items if i['level'] == 2]
    l3_items = [i for i in items if i['level'] == 3]

    print(f"Total items: {len(items)}")
    print(f"  L1 paragraphs: {len(l1_items)}")
    print(f"  L2 emergence: {len(l2_items)}")
    print(f"  L3 meta: {len(l3_items)}")
    print()

    # Per-chapter breakdown
    for section in ['preamble', 'bourgeois-and-proletarians', 'proletarians-and-communists',
                     'socialist-and-communist-literature', 'position-of-communists']:
        count = len(chapter_paragraph_ids.get(section, []))
        print(f"  {section}: {count} paragraphs")

    print()
    for theme_key, ids in thematic_ids.items():
        print(f"  Theme '{theme_key}': {len(ids)} paragraphs")

    print()
    for sub_key, ids in ch3_subsection_ids.items():
        print(f"  Ch3 subsection '{sub_key}': {len(ids)} paragraphs")

    print(f"\nWritten to {OUTPUT}")


if __name__ == '__main__':
    build_grammar()
