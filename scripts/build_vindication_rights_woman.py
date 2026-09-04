#!/usr/bin/env python3
"""
Build grammar.json for Wollstonecraft's A Vindication of the Rights of Woman.

Source: Project Gutenberg eBook #3420
Author: Mary Wollstonecraft (1792)

Structure:
- Biographical sketch (stripped)
- Dedication to Talleyrand (stripped)
- Introduction + 13 chapters
- L1: Introduction + 13 chapters
- L2: Thematic groupings
- L3: Meta-category
"""

import json
import re
from pathlib import Path

SEED_PATH = Path(__file__).parent.parent / "seeds" / "vindication-rights-woman.txt"
OUTPUT_DIR = Path(__file__).parent.parent / "grammars" / "vindication-rights-woman"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"

# Chapter definitions with their text markers and metadata
CHAPTERS = [
    {
        "marker": "INTRODUCTION.\n\nAfter considering the historic page",
        "next_marker": "CHAPTER 1.",
        "title": "Introduction",
        "id": "introduction",
        "subtitle": "A Call to Reason",
        "keywords": ["introduction", "education", "reason", "equality", "women", "nature"],
        "about": "Wollstonecraft opens with a challenge: women have been rendered weak not by nature but by miseducation. Trained to please rather than to think, women become ornamental creatures -- 'flowers planted in too rich a soil.' She proposes to show that the same rational faculties belong to both sexes, and that only equal education can produce virtuous citizens."
    },
    {
        "marker": "CHAPTER 1.\n\nTHE RIGHTS AND INVOLVED DUTIES OF MANKIND CONSIDERED.",
        "next_marker": "CHAPTER 2.",
        "title": "The Rights and Involved Duties of Mankind Considered",
        "id": "chapter-1-rights-duties",
        "subtitle": "Reason as the Foundation of Rights",
        "keywords": ["rights", "duties", "reason", "virtue", "knowledge", "first-principles"],
        "about": "Wollstonecraft establishes her philosophical foundation: reason is what distinguishes humans from animals, virtue comes from the exercise of reason, and therefore any system that prevents women from developing reason prevents them from becoming virtuous. Rights and duties are inseparable -- to deny rights is to deny the capacity for moral responsibility."
    },
    {
        "marker": "CHAPTER 2.\n\nTHE PREVAILING OPINION OF A SEXUAL CHARACTER DISCUSSED.",
        "next_marker": "CHAPTER 3.",
        "title": "The Prevailing Opinion of a Sexual Character Discussed",
        "id": "chapter-2-sexual-character",
        "subtitle": "Against the Myth of Female Nature",
        "keywords": ["sexual-character", "rousseau", "nature", "education", "dependence", "submission"],
        "about": "Wollstonecraft takes on Rousseau, Milton, and the entire tradition that defines women by a distinct 'sexual character' -- gentle, submissive, designed to please men. She argues that these traits are not natural but manufactured by an education designed to produce ornamental dependence rather than rational independence."
    },
    {
        "marker": "CHAPTER 3.\n\nTHE SAME SUBJECT CONTINUED.",
        "next_marker": "CHAPTER 4.",
        "title": "The Same Subject Continued",
        "id": "chapter-3-same-continued",
        "subtitle": "Strength, Virtue, and the Body",
        "keywords": ["strength", "body", "virtue", "exercise", "mind-body", "education"],
        "about": "Bodily strength, Wollstonecraft argues, has been wrongly used to justify women's subordination. She insists that women should exercise their bodies as well as their minds. Physical weakness is not a feminine virtue but a form of degradation. The chapter extends the argument to show how mental and physical strength are connected."
    },
    {
        "marker": "CHAPTER 4.\n\nOBSERVATIONS ON THE STATE OF DEGRADATION",
        "next_marker": "CHAPTER 5.",
        "title": "Observations on the State of Degradation to Which Woman Is Reduced",
        "id": "chapter-4-degradation",
        "subtitle": "The Causes of Women's Degradation",
        "keywords": ["degradation", "ignorance", "cunning", "sensibility", "dependence", "marriage"],
        "about": "Wollstonecraft catalogs the ways women are degraded: denied education, confined to domestic concerns, encouraged in sensibility over reason, taught cunning rather than honesty. Women are made into perpetual children, and then blamed for childish behavior. Marriage under these conditions is not partnership but servitude."
    },
    {
        "marker": "CHAPTER 5.\n\nANIMADVERSIONS ON SOME OF THE WRITERS",
        "next_marker": "CHAPTER 6.",
        "title": "Animadversions on Some Writers Who Have Rendered Women Objects of Pity",
        "id": "chapter-5-writers",
        "subtitle": "Critiquing the Masters: Rousseau, Gregory, Fordyce",
        "keywords": ["rousseau", "gregory", "fordyce", "education", "conduct-books", "critique"],
        "about": "Wollstonecraft systematically dismantles the most influential writers on female education: Rousseau's Sophie (trained to be Emile's complement), Dr. Gregory's 'A Father's Legacy' (teaching daughters to conceal their intelligence), and Fordyce's sermons (idealizing female weakness). Each writer, she shows, mistakes the effects of oppression for the nature of women."
    },
    {
        "marker": "CHAPTER 6.\n\nTHE EFFECT WHICH AN EARLY ASSOCIATION OF IDEAS",
        "next_marker": "CHAPTER 7.",
        "title": "The Effect Which an Early Association of Ideas Has Upon the Character",
        "id": "chapter-6-association",
        "subtitle": "How Childhood Forms (and Deforms) Character",
        "keywords": ["association", "childhood", "ideas", "character", "formation", "habit"],
        "about": "Drawing on Lockean psychology, Wollstonecraft shows how early associations of ideas shape character. Women taught from infancy to value appearance over substance, charm over competence, develop habits of mind that become virtually impossible to break. The chapter is both psychological analysis and urgent plea for childhood education reform."
    },
    {
        "marker": "CHAPTER 7.\n\nMODESTY",
        "next_marker": "CHAPTER 8.",
        "title": "Modesty Comprehensively Considered, and Not as a Sexual Virtue",
        "id": "chapter-7-modesty",
        "subtitle": "Redefining Modesty Beyond Sexuality",
        "keywords": ["modesty", "virtue", "sexuality", "propriety", "knowledge", "innocence"],
        "about": "Wollstonecraft reclaims modesty from its reduction to sexual purity. True modesty is 'that soberness of mind which teaches a man not to think more highly of himself than he ought to think' -- it belongs to both sexes and consists not in ignorance but in self-knowledge. The false modesty imposed on women (don't know, don't ask, don't look) is the enemy of genuine virtue."
    },
    {
        "marker": "CHAPTER 8.\n\nMORALITY UNDERMINED",
        "next_marker": "CHAPTER 9.",
        "title": "Morality Undermined by Sexual Notions of the Importance of a Good Reputation",
        "id": "chapter-8-reputation",
        "subtitle": "When Reputation Replaces Character",
        "keywords": ["morality", "reputation", "character", "appearance", "hypocrisy", "double-standard"],
        "about": "Women are taught that reputation matters more than character -- seeming virtuous is more important than being virtuous. This produces hypocrisy, cunning, and moral corruption. Wollstonecraft argues that a woman's honor should rest on the same foundation as a man's: actual conduct, not appearances."
    },
    {
        "marker": "CHAPTER 9.\n\nOF THE PERNICIOUS EFFECTS",
        "next_marker": "CHAPTER 10.",
        "title": "Of the Pernicious Effects Which Arise from Unnatural Distinctions in Society",
        "id": "chapter-9-unnatural-distinctions",
        "subtitle": "Class, Gender, and Social Corruption",
        "keywords": ["class", "distinctions", "society", "wealth", "property", "corruption"],
        "about": "Wollstonecraft extends her argument from gender to class: all artificial distinctions -- whether based on sex, birth, or wealth -- corrupt both the powerful and the powerless. Women of the upper classes are especially degraded, reduced to decorative dependence. She calls for women to be able to earn their own livelihood."
    },
    {
        "marker": "CHAPTER 10.\n\nPARENTAL AFFECTION.",
        "next_marker": "CHAPTER 11.",
        "title": "Parental Affection",
        "id": "chapter-10-parental-affection",
        "subtitle": "The Blind Love of Unequal Parents",
        "keywords": ["parents", "affection", "children", "tyranny", "blindness", "favoritism"],
        "about": "Parental affection, Wollstonecraft argues, is perhaps the blindest modification of self-love. Parents who are themselves uneducated and unfree cannot properly educate their children. The tyranny of fathers and the sentimental indulgence of mothers both produce damaged souls. True parental love requires the parent's own moral and intellectual development."
    },
    {
        "marker": "CHAPTER 11.\n\nDUTY TO PARENTS.",
        "next_marker": "CHAPTER 12.",
        "title": "Duty to Parents",
        "id": "chapter-11-duty-parents",
        "subtitle": "Obedience, Authority, and Moral Autonomy",
        "keywords": ["duty", "parents", "obedience", "authority", "autonomy", "reason"],
        "about": "Wollstonecraft challenges blind filial obedience. Children owe respect and gratitude to parents, but not the surrender of reason. When parental authority is exercised tyrannically, submission becomes vice rather than virtue. The capacity for independent moral judgment must be cultivated, not crushed."
    },
    {
        "marker": "CHAPTER 12.\n\nON NATIONAL EDUCATION.",
        "next_marker": "CHAPTER 13.",
        "title": "On National Education",
        "id": "chapter-12-national-education",
        "subtitle": "A Plan for Equal Public Schooling",
        "keywords": ["education", "national", "co-education", "schools", "reform", "equality"],
        "about": "Wollstonecraft's most constructive chapter: a detailed plan for national education. Boys and girls should be educated together in public day schools. The curriculum should include exercise, science, history, and moral reasoning. Private education produces either pampered weaklings or narrow specialists. Only public, co-educational schooling can produce citizens worthy of a republic."
    },
    {
        "marker": "CHAPTER 13.\n\nSOME INSTANCES OF THE FOLLY",
        "next_marker": None,
        "title": "Some Instances of the Folly Which the Ignorance of Women Generates",
        "id": "chapter-13-folly-ignorance",
        "subtitle": "The Consequences of Ignorance",
        "keywords": ["folly", "ignorance", "superstition", "sentimentality", "revolution", "conclusion"],
        "about": "Wollstonecraft's conclusion catalogues the follies produced by women's ignorance: superstition, sentimentality, vanity, cunning, and moral cowardice. But these are not women's nature -- they are the products of oppression. She ends with a vision of revolution: when women's manners are reformed through equal education, the whole of society will be transformed."
    }
]


def read_and_extract():
    """Read seed text, strip Gutenberg header/footer, biographical sketch."""
    with open(SEED_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    if start == -1 or end == -1:
        raise ValueError("Could not find Gutenberg markers")

    text = text[start:end]
    text = text[text.find('\n') + 1:]

    return text.strip()


def clean_text(text):
    """Normalize whitespace, clean up formatting."""
    if not text:
        return ""
    text = re.sub(r'  +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def normalize(text):
    """Join lines within paragraphs, preserve paragraph breaks."""
    if not text:
        return ""
    text = text.strip()
    paragraphs = re.split(r'\n\n+', text)
    result = []
    for p in paragraphs:
        joined = ' '.join(line.strip() for line in p.split('\n') if line.strip())
        if joined:
            result.append(joined)
    return '\n\n'.join(result)


def build_grammar():
    full_text = read_and_extract()

    items = []
    so = 0

    def add_item(item):
        nonlocal so
        item["sort_order"] = so
        items.append(item)
        so += 1

    def ct(text):
        return normalize(clean_text(text))

    # =========================================================================
    # L1 ITEMS - Chapters
    # =========================================================================

    chapter_ids = []
    for i, ch in enumerate(CHAPTERS):
        start_idx = full_text.find(ch["marker"])
        if start_idx == -1:
            print(f"WARNING: Could not find marker for {ch['title']}: '{ch['marker'][:50]}'")
            continue

        if ch["next_marker"]:
            # Find the BODY version of the next chapter (not the TOC version)
            # Search for the next marker after the current chapter start
            end_idx = full_text.find(ch["next_marker"], start_idx + len(ch["marker"]))
            # Verify this is the body version (should be far from current start)
            if end_idx != -1 and (end_idx - start_idx) < 500:
                # This might be a TOC reference; skip ahead
                end_idx = full_text.find(ch["next_marker"], end_idx + 100)
            if end_idx == -1:
                chapter_text = full_text[start_idx:]
            else:
                chapter_text = full_text[start_idx:end_idx]
        else:
            chapter_text = full_text[start_idx:]

        chapter_text = chapter_text.strip()
        chapter_ids.append(ch["id"])

        add_item({
            "id": ch["id"],
            "name": f"{ch['title']}",
            "level": 1,
            "category": "chapter",
            "sections": {
                "Text": ct(chapter_text),
                "About": ch["about"],
                "Reflection": "How does Wollstonecraft's argument speak to our own time? What has changed, and what remains the same, in the relationship between education, gender, and freedom?"
            },
            "keywords": ch["keywords"],
            "metadata": {"chapter": i, "subtitle": ch["subtitle"]}
        })

    # =========================================================================
    # L2 ITEMS - Thematic groupings
    # =========================================================================

    add_item({
        "id": "theme-philosophical-foundations",
        "name": "Philosophical Foundations: Reason, Rights, and the Nature Argument",
        "level": 2,
        "category": "thematic-grouping",
        "sections": {
            "About": "The first three chapters establish Wollstonecraft's philosophical framework. Drawing on Enlightenment rationalism, she argues that reason is the common inheritance of all humans, that rights derive from rational capacity, and that the entire tradition of 'feminine nature' is a construct designed to maintain male power. Her targets are formidable -- Rousseau, Milton, the Bible as interpreted by patriarchy -- and her weapon is rigorous logic.",
            "For Readers": "These chapters are the intellectual core of the book. Wollstonecraft is doing philosophy, not merely polemics. Notice how she turns the Enlightenment's own principles against its blind spots: if reason is what makes us human, then denying women reason is denying their humanity."
        },
        "keywords": ["reason", "rights", "nature", "philosophy", "enlightenment", "rousseau"],
        "metadata": {},
        "composite_of": ["introduction", "chapter-1-rights-duties", "chapter-2-sexual-character", "chapter-3-same-continued"]
    })

    add_item({
        "id": "theme-critique-of-culture",
        "name": "Critique of Culture: Education, Writers, and the Degradation of Women",
        "level": 2,
        "category": "thematic-grouping",
        "sections": {
            "About": "Chapters 4 through 8 analyze how culture systematically degrades women: through miseducation, through conduct books that teach cunning over honesty, through the association of modesty with ignorance, and through a moral system that values reputation over character. Wollstonecraft reads the entire culture as a machine for producing decorative incompetence.",
            "For Readers": "These chapters are Wollstonecraft at her most incisive and her most angry. Her close readings of Rousseau's Sophie and Gregory's conduct advice remain devastating. Notice how she consistently shows that what appears as women's nature is actually the product of a specific educational system."
        },
        "keywords": ["culture", "education", "writers", "degradation", "conduct", "critique"],
        "metadata": {},
        "composite_of": ["chapter-4-degradation", "chapter-5-writers", "chapter-6-association", "chapter-7-modesty", "chapter-8-reputation"]
    })

    add_item({
        "id": "theme-vision-of-reform",
        "name": "Vision of Reform: Society, Family, and National Education",
        "level": 2,
        "category": "thematic-grouping",
        "sections": {
            "About": "The final five chapters turn from critique to construction. Wollstonecraft examines the institutions that need reform -- class structure, family, parental authority, and above all education. Her plan for co-educational public schooling is remarkably detailed and forward-looking. The book ends with a call to revolution: reform women's education and you transform society.",
            "For Readers": "These chapters show Wollstonecraft as a practical reformer, not just a philosopher. Her proposals for national education anticipate developments that would not arrive for over a century. Her analysis of how inequality corrupts both the powerful and the powerless remains urgent today."
        },
        "keywords": ["reform", "education", "society", "family", "co-education", "revolution"],
        "metadata": {},
        "composite_of": ["chapter-9-unnatural-distinctions", "chapter-10-parental-affection", "chapter-11-duty-parents", "chapter-12-national-education", "chapter-13-folly-ignorance"]
    })

    # =========================================================================
    # L3 ITEMS - Meta-category
    # =========================================================================

    add_item({
        "id": "meta-vindication",
        "name": "A Vindication of the Rights of Woman: The Founding Text of Feminism",
        "level": 3,
        "category": "meta-category",
        "sections": {
            "About": "Published in 1792, A Vindication of the Rights of Woman is the foundational text of feminist philosophy. Writing in the white heat of the French Revolution, Wollstonecraft applied Enlightenment principles of reason, rights, and equality to the situation of women with devastating force. Her central argument -- that women appear inferior only because they are denied equal education -- remains the bedrock of feminist thought. The book is at once a philosophical treatise, a work of cultural criticism, an educational manifesto, and a passionate plea for human dignity.",
            "For Readers": "This book is not easy or comfortable reading. Wollstonecraft writes with the urgency of someone who knows she may not be heard. Her prose can be dense, her sentences long, her anger barely contained. But within these pages is a vision of human flourishing that remains revolutionary: a world in which both sexes develop their rational capacities, share the duties of citizenship, and meet each other as equals in love, work, and moral life."
        },
        "keywords": ["feminism", "wollstonecraft", "rights", "reason", "education", "equality", "revolution", "enlightenment"],
        "metadata": {},
        "composite_of": ["theme-philosophical-foundations", "theme-critique-of-culture", "theme-vision-of-reform"]
    })

    # =========================================================================
    # BUILD GRAMMAR
    # =========================================================================

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Mary Wollstonecraft", "date": "1792", "note": "Author"},
                {"name": "Project Gutenberg", "date": "2002", "note": "Source: eBook #3420 (https://www.gutenberg.org/ebooks/3420)"}
            ]
        },
        "name": "A Vindication of the Rights of Woman",
        "description": "Mary Wollstonecraft's revolutionary treatise on women's education and rights (1792) -- the founding text of feminist philosophy. In thirteen chapters, Wollstonecraft argues that women are not naturally inferior but are made so by an education designed to produce ornamental dependence. She calls for equal education, co-educational public schooling, and the recognition of women as rational beings capable of virtue and citizenship.\n\nSource: Project Gutenberg eBook #3420 (https://www.gutenberg.org/ebooks/3420)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: John Opie's portrait of Mary Wollstonecraft (c. 1797, National Portrait Gallery); William Blake's engravings for Wollstonecraft's 'Original Stories from Real Life' (1791); James Gillray's political caricatures of 1790s radical intellectuals.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["feminism", "philosophy", "education", "rights", "equality", "enlightenment", "wollstonecraft", "reason", "virtue", "revolution"],
        "roots": ["emotion-love"],
        "shelves": ["mirror"],
        "lineages": ["Gottman", "Andreotti"],
        "worldview": "rationalist",
        "items": items
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    print(f"Built Vindication grammar: {len(items)} items")
    for item in items:
        text_len = len(item["sections"].get("Text", ""))
        print(f"  L{item['level']}: {item['id']} - {item['name']} ({text_len} chars)")


if __name__ == "__main__":
    build_grammar()
