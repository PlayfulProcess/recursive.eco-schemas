#!/usr/bin/env python3
"""
Parse Areopagitica by John Milton (Gutenberg #608, 1644)
into a grammar.json.

Structure:
- L1: Paragraphs of the single essay
- L2: Thematic groups (since there are no chapters, we create thematic groupings)
- L3: Meta-category connecting all

Areopagitica is a single continuous essay (a speech to Parliament against
the Licensing Order of 1643). We divide it into paragraphs at L1 and
create thematic groupings at L2.
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(SCRIPT_DIR, "..", "seeds", "areopagitica.txt")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "grammars", "areopagitica")
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


def strip_header(text):
    """Remove the title page and epigraph, keeping only the essay body."""
    lines = text.split('\n')
    # Find the start of the actual essay text
    # The essay begins with "They, who to states and governors..."
    for i, line in enumerate(lines):
        if line.strip().startswith("They, who to states and governors"):
            return '\n'.join(lines[i:]).strip()
    # Fallback: skip title and epigraph (first ~50 lines)
    return '\n'.join(lines[30:]).strip()


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


THEMATIC_GROUPS = [
    {
        "id": "theme-address-to-parliament",
        "name": "Address to Parliament",
        "about": "Milton's opening address to the Lords and Commons, establishing his right to petition and his loyalty to Parliament. He praises Parliament's openness to counsel while positioning himself as a citizen exercising the ancient right of free speech. The rhetorical strategy is masterful: by praising Parliament's tolerance, he makes it harder for them to suppress his argument.",
        "for_readers": "The opening paragraphs reveal Milton's rhetorical genius. He cannot simply demand free speech -- he must persuade the very body that passed the Licensing Order to repeal it. So he begins with praise, establishes his credibility, and invokes the classical precedent of Isocrates addressing the Athenian assembly. Every compliment is also a trap: having praised Parliament's openness, he can now argue that censorship contradicts their own principles.",
        "patterns": [
            "lords and commons",
            "parliament",
            "high court",
            "your published order",
            "your laudable deeds",
            "civil liberty",
            "praise ye",
            "covenant of his fidelity",
        ],
    },
    {
        "id": "theme-history-of-censorship",
        "name": "History of Censorship",
        "about": "Milton traces the history of book licensing from ancient Athens through the Roman Inquisition, showing that censorship has always been the tool of tyrants and the Catholic Church. The Greeks and Romans censored only blasphemous and libellous books; systematic pre-publication censorship was invented by the Inquisition. Parliament's Licensing Order thus imitates the worst practices of popery, not the best traditions of classical liberty.",
        "for_readers": "Milton's historical argument is devastatingly effective. He shows that the very institution Parliament is defending -- pre-publication licensing -- was invented by the Spanish Inquisition and the Council of Trent. Protestant England is imitating Catholic tyranny. The implicit argument: you fought a civil war against popish tyranny; why are you now adopting the Pope's methods?",
        "patterns": [
            "inquisition",
            "licensing",
            "index",
            "imprimatur",
            "council of trent",
            "papist",
            "bishops",
            "censor",
            "rome",
            "plato",
            "prohibit",
        ],
    },
    {
        "id": "theme-virtue-of-books",
        "name": "The Virtue of Books",
        "about": "Milton's passionate defense of the value of books and reading. 'A good book is the precious life-blood of a master spirit, embalmed and treasured up on purpose to a life beyond life.' To destroy a book is to destroy reason itself. And censorship before publication is worse than burning: it kills ideas before they are born. Books are not mere paper but living things, and licensing treats them as guilty until proven innocent.",
        "for_readers": "These passages contain Milton's most quoted lines. His argument that 'who kills a man kills a reasonable creature, God's image; but he who destroys a good book, kills reason itself' elevates the book to sacred status. His distinction between pre-publication censorship (which prevents ideas from being born) and post-publication punishment (which at least allows ideas to be heard) is the foundation of modern free press doctrine.",
        "patterns": [
            "good book",
            "life-blood",
            "master spirit",
            "reason itself",
            "kills a man",
            "destroy a good book",
            "precious",
            "reading",
            "truth",
            "learning",
        ],
    },
    {
        "id": "theme-knowledge-and-virtue",
        "name": "Knowledge, Temptation, and Virtue",
        "about": "Milton's most profound argument: virtue that has never been tested is not true virtue. To censor evil books is to create a 'cloistered virtue' that cannot withstand real temptation. True goodness requires knowledge of evil -- the capacity to choose good when evil is available. Adam fell because he was innocent, not because he was wise. A censored society is a society of children, not of virtuous adults.",
        "for_readers": "This is Milton the Puritan theologian at his most radical. His argument that virtue requires the knowledge of evil directly challenges the logic of censorship: if we remove all bad books, we do not create good people -- we create ignorant ones. 'I cannot praise a fugitive and cloistered virtue, unexercised and unbreathed, that never sallies out and sees her adversary.' This sentence is the seed of every subsequent argument for trusting adults to make their own moral choices.",
        "patterns": [
            "virtue",
            "knowledge of good and evil",
            "temptation",
            "cloistered",
            "trial",
            "temperance",
            "choose",
            "innocence",
            "fugitive",
            "sallies out",
        ],
    },
    {
        "id": "theme-truth-will-prevail",
        "name": "Truth Will Prevail",
        "about": "Milton's faith that truth, freely published, will defeat falsehood in open encounter. 'Let her and Falsehood grapple; who ever knew Truth put to the worse, in a free and open encounter?' This confidence in the self-correcting power of free debate is the foundation of the 'marketplace of ideas' that underlies modern free speech doctrine. Censorship is not merely unjust but unnecessary: truth does not need the protection of the censor.",
        "for_readers": "Milton's argument for truth's power is both theological and practical. He compares truth to the scattered body of Osiris -- broken into pieces that must be gathered by free inquiry. Censorship does not protect truth; it prevents the gathering of truth's fragments. His vision of truth and falsehood in open combat became the intellectual foundation for Mill's On Liberty, Holmes's 'marketplace of ideas,' and the First Amendment tradition.",
        "patterns": [
            "truth",
            "falsehood",
            "grapple",
            "free and open encounter",
            "marketplace",
            "prevail",
            "osiris",
            "scattered",
            "gather",
            "light",
        ],
    },
    {
        "id": "theme-impracticality-of-censorship",
        "name": "The Impracticality of Censorship",
        "about": "Milton's practical argument: even if censorship were desirable, it would be impossible to implement. To censor books, you would need to censor sermons, lectures, songs, conversations, and private letters. You would need an army of licensers -- and who will censor the censors? The licensing system is not merely tyrannical but absurd: it cannot achieve its own goals, and it insults the licensers (forced to read tedious books) as much as the authors.",
        "for_readers": "Milton shifts from philosophy to practicality. His argument that censorship is impossible to enforce without censoring all human communication anticipates the 'information wants to be free' arguments of the digital age. His observation that the licenser's job is unbearable -- reading every bad book submitted -- adds humor to the argument. And his point that licensed books carry the imprimatur of the state, making the state responsible for their contents, is shrewdly ironic.",
        "patterns": [
            "licenser",
            "imprimatur",
            "impossible",
            "enforce",
            "regulate",
            "unlearned",
            "tedious",
            "monopoly",
            "company of stationers",
            "twenty licensers",
        ],
    },
]


def build_grammar(paragraphs):
    items = []
    sort_order = 0

    # L1: Paragraphs
    para_ids = []
    for i, para in enumerate(paragraphs):
        sort_order += 1
        para_id = f"para-{i+1:02d}"
        name = first_sentence_name(para)

        items.append({
            "id": para_id,
            "name": name,
            "level": 1,
            "category": "essay",
            "sort_order": sort_order,
            "sections": {
                "Passage": para,
            },
            "keywords": [],
            "metadata": {
                "paragraph_number": i + 1,
            },
        })
        para_ids.append(para_id)

    # L2: Whole-essay group
    sort_order += 1
    items.append({
        "id": "essay-areopagitica",
        "name": "Areopagitica: The Complete Essay",
        "level": 2,
        "category": "essay-whole",
        "relationship_type": "emergence",
        "composite_of": para_ids,
        "sort_order": sort_order,
        "sections": {
            "About": "John Milton's Areopagitica (1644) as a continuous argument. The essay moves from an address to Parliament, through a history of censorship, a defense of books and learning, a theological argument for tested virtue, a practical case against licensing, to a prophetic vision of England as a nation of free inquiry. Each section builds on the last: censorship has ignoble origins, destroys precious things, prevents true virtue, cannot achieve its goals, and betrays England's revolutionary promise.",
            "For Readers": "Reading Areopagitica straight through reveals Milton's argumentative architecture. He begins with praise (establishing goodwill), moves to history (showing censorship's corrupt pedigree), rises to philosophy (virtue requires choice), descends to practicality (licensing cannot work), and ends with prophecy (England is destined for intellectual greatness). The essay is a masterclass in persuasion.",
        },
        "keywords": [],
        "metadata": {
            "paragraph_count": len(para_ids),
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
        "id": "meta-areopagitica",
        "name": "Areopagitica",
        "level": 3,
        "category": "meta",
        "relationship_type": "emergence",
        "composite_of": all_l2_ids,
        "sort_order": sort_order,
        "sections": {
            "About": "John Milton's Areopagitica (1644) is the foundational text of free press doctrine. Written as an unlicensed pamphlet addressed to the English Parliament, it argues against the Licensing Order of 1643 that required all books to be approved by a government censor before publication. Milton's argument moves through multiple registers: historical (censorship was invented by the Inquisition), philosophical (virtue requires the knowledge of evil), practical (licensing is impossible to enforce), and prophetic (England is destined for intellectual greatness). His most famous passages -- 'a good book is the precious life-blood of a master spirit'; 'I cannot praise a fugitive and cloistered virtue'; 'Let Truth and Falsehood grapple' -- established the intellectual framework that underlies the First Amendment, Mill's On Liberty, and every subsequent argument for freedom of the press.",
        },
        "keywords": [],
        "metadata": {
            "theme_count": len(THEMATIC_GROUPS),
        },
    })

    return items


def main():
    with open(SEED, "r", encoding="utf-8") as f:
        raw = f.read()

    text = strip_gutenberg(raw)
    text = strip_header(text)

    paragraphs = split_into_paragraphs(text)
    print(f"Found {len(paragraphs)} paragraphs")

    items = build_grammar(paragraphs)

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "John Milton", "date": "1644", "note": "Author"},
            ]
        },
        "name": "Areopagitica",
        "description": "John Milton's Areopagitica (1644) -- the foundational argument for freedom of the press. Written as an unlicensed pamphlet defying the very law it opposed, it argues against Parliament's Licensing Order with a force that echoes across four centuries. Milton marshals history (censorship was invented by the Inquisition), theology (virtue requires the knowledge of evil), and practical sense (licensing is impossible to enforce) into the most eloquent case ever made for the free circulation of ideas. 'Who kills a man kills a reasonable creature, God's image; but he who destroys a good book, kills reason itself.'\n\nSource: Project Gutenberg eBook #608 (https://www.gutenberg.org/ebooks/608)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: 17th century English Civil War engravings. William Faithorne's portrait of Milton. Title pages of original 1644 pamphlet editions.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["politics", "philosophy", "free-press", "censorship", "freedom", "rhetoric", "public-domain", "full-text"],
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
