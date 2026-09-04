#!/usr/bin/env python3
"""
Build grammar.json for Ovid's Art of Love (Ars Amatoria) from seed text.

Source: Project Gutenberg eBook #47677
Author: Ovid (43 BCE - 17/18 CE)
Translator: Henry T. Riley (1885)

Structure:
- 3 Books of verse in prose translation
- Book 1: How to find a woman (addressed to men)
- Book 2: How to keep her love
- Book 3: Advice to women (how to attract and keep men)
- Footnotes at end (stripped)
- Inline footnote references [701], [813], etc. (stripped)

L1: Thematic passages within each book
L2: The three books
L3: Meta-categories
"""

import json
import re
from pathlib import Path

SEED_PATH = Path(__file__).parent.parent / "seeds" / "art-of-love-ovid.txt"
OUTPUT_DIR = Path(__file__).parent.parent / "grammars" / "art-of-love-ovid"
OUTPUT_PATH = OUTPUT_DIR / "grammar.json"


def read_and_clean():
    """Read seed text, strip Gutenberg header/footer and footnotes."""
    with open(SEED_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    # Extract between Gutenberg markers
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    if start == -1 or end == -1:
        raise ValueError("Could not find Gutenberg markers")

    text = text[start:end]
    # Skip past the start marker line
    text = text[text.find('\n') + 1:]

    # Remove everything from FOOTNOTES onward
    fn_start = text.find("\nFOOTNOTES BOOK ONE")
    if fn_start == -1:
        fn_start = text.find("\nFOOTNOTES")
    if fn_start == -1:
        fn_start = text.find("\n[Footnote")
    if fn_start != -1:
        text = text[:fn_start]

    # Also check for "END" marker before footnotes
    end_marker = text.find("\nEND\n")
    if end_marker != -1:
        text = text[:end_marker]

    return text.strip()


def clean_text(text):
    """Clean inline footnote refs, pipe characters, normalize whitespace."""
    if not text:
        return ""
    # Remove inline footnote references like [701], [813]
    text = re.sub(r'\s*\[\d{3,4}\]', '', text)
    # Remove leading pipe characters (paragraph starters in this edition)
    text = re.sub(r'^\|', '', text, flags=re.MULTILINE)
    # Remove italic markers
    text = text.replace('_', '')
    # Normalize whitespace
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


def extract_books(text):
    """Split the text into three books."""
    book1_start = text.find("BOOK THE FIRST.")
    book2_start = text.find("BOOK THE SECOND.")
    book3_start = text.find("BOOK THE THIRD.")

    if book1_start == -1 or book2_start == -1 or book3_start == -1:
        raise ValueError("Could not find all three book markers")

    book1 = text[book1_start:book2_start].strip()
    book2 = text[book2_start:book3_start].strip()
    book3 = text[book3_start:].strip()

    # Remove the "BOOK THE X." header from each
    book1 = book1[len("BOOK THE FIRST."):].strip()
    book2 = book2[len("BOOK THE SECOND."):].strip()
    book3 = book3[len("BOOK THE THIRD."):].strip()

    return book1, book2, book3


def split_into_passages(book_text, num_passages):
    """Split a book into roughly equal thematic passages by paragraph breaks."""
    paragraphs = re.split(r'\n\n+', book_text.strip())
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    if len(paragraphs) <= num_passages:
        return ['\n\n'.join([p]) for p in paragraphs]

    per_passage = len(paragraphs) // num_passages
    remainder = len(paragraphs) % num_passages

    passages = []
    idx = 0
    for i in range(num_passages):
        count = per_passage + (1 if i < remainder else 0)
        chunk = paragraphs[idx:idx + count]
        passages.append('\n\n'.join(chunk))
        idx += count

    return passages


def build_grammar():
    raw_text = read_and_clean()
    book1_raw, book2_raw, book3_raw = extract_books(raw_text)

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
    # Book 1: How to Find a Woman
    # =========================================================================
    b1_passages = split_into_passages(book1_raw, 6)

    b1_titles = [
        "The Art Begins: Venus Appoints Her Poet",
        "Where to Find Her: Theatres, Temples, and Feasts",
        "The Rape of the Sabines and the Art of the Races",
        "Winning Her Favor: Promises, Tears, and Persistence",
        "The Banquet: Wine, Song, and Stolen Kisses",
        "A Thousand Dispositions, A Thousand Ways"
    ]
    b1_abouts = [
        "Ovid declares himself Love's chosen instructor. As Chiron trained Achilles, so Ovid will train lovers. He announces his three-part plan: find the beloved, win her, and keep her love. The muses of poetry and the authority of experience guide him.",
        "Rome is a paradise for lovers. Ovid catalogs the city's best hunting grounds: Pompey's Portico, the temples of Venus and Isis, the law courts where advocates lose their own cases to love, and especially the theatres where fashionable women come to see and be seen.",
        "Ovid retells the founding myth of Roman love: Romulus' soldiers seizing the Sabine women at the games. The races too are prime territory -- sit close, brush her knee, pick up her dropped handkerchief. The mock naval battles provide spectacle and opportunity.",
        "Make promises freely (the gods forgive lovers' oaths). Use tears, kisses stolen boldly, and the services of her maidservant as intermediary. Write letters on wax tablets. Be persistent but not heavy-handed. Above all, know her character before you begin.",
        "The dinner party is Love's battlefield. Arrive late, look your best, drink just enough. Write sweet nothings on the table in wine. Praise her beauty. When the party breaks up, press close in the crowd. But beware: the same arts that win her can be turned against you.",
        "There are as many characters in women as forms in the world. The wise lover adapts like Proteus -- flowing water, then a lion, then a tree. What works on the shy will fail on the bold. Study her nature first."
    ]
    b1_keywords = [
        ["invocation", "venus", "cupid", "art", "instruction"],
        ["rome", "theatre", "temple", "portico", "spectacle"],
        ["sabines", "races", "romulus", "boldness", "opportunity"],
        ["persuasion", "letters", "tears", "persistence", "servants"],
        ["banquet", "wine", "flattery", "beauty", "dinner"],
        ["character", "proteus", "adaptation", "wisdom", "variety"]
    ]

    b1_ids = []
    for i, passage in enumerate(b1_passages):
        item_id = f"book1-{i+1}"
        b1_ids.append(item_id)
        add_item({
            "id": item_id,
            "name": b1_titles[i],
            "level": 1,
            "category": "book-1-finding",
            "sections": {
                "Verse": ct(passage),
                "About": b1_abouts[i],
                "Reflection": "What does Ovid's playful worldliness reveal about the Roman attitude toward love? Where do you see genuine insight beneath the wit?"
            },
            "keywords": b1_keywords[i],
            "metadata": {"book": 1}
        })

    # =========================================================================
    # Book 2: How to Keep Her Love
    # =========================================================================
    b2_passages = split_into_passages(book2_raw, 6)

    b2_titles = [
        "The Prey Is Won: Now Learn to Keep Her",
        "Daedalus and the Art of Flight",
        "Be Yielding: The Gentle Arts of Submission",
        "Bear with Her Faults and Humor Her Moods",
        "The Rival and the Gift of Jealousy",
        "Love's Eternal Renewal"
    ]
    b2_abouts = [
        "Triumph! But the harder art begins now. Keeping love requires more skill than winning it. Ovid invokes Cupid and Erato, muse of love poetry, for this second campaign.",
        "The myth of Daedalus and Icarus illustrates the perils of excess. Like Daedalus, the lover must find the middle way -- too little effort loses her, too much smothers. Wings of wax melt in the sun of passion.",
        "Be agreeable. Yield in quarrels. Let her win arguments. Praise her singing even if it's terrible. Carry her parasol. Be her mirror. These small submissions are not weakness but the arts of sustained affection.",
        "Every woman has flaws; love them as part of the whole. Call the dark one 'dusky,' the thin one 'slender,' the plump one 'bountiful.' Make her faults into virtues through the alchemy of devoted attention.",
        "A little jealousy keeps love alive. Let her know she has rivals, but not too many. The art is to stir anxiety without provoking despair. Ovid navigates the dangerous waters between complacency and crisis.",
        "Love must be continually renewed through attention, surprise, and shared pleasure. The lover who rests on past conquests will lose everything. The art of love is the art of perpetual beginning."
    ]
    b2_keywords = [
        ["triumph", "keeping", "art", "difficulty", "cupid"],
        ["daedalus", "icarus", "moderation", "excess", "myth"],
        ["yielding", "submission", "praise", "gentleness", "service"],
        ["faults", "acceptance", "alchemy", "devotion", "forgiveness"],
        ["jealousy", "rivalry", "anxiety", "passion", "danger"],
        ["renewal", "attention", "surprise", "persistence", "beginning"]
    ]

    b2_ids = []
    for i, passage in enumerate(b2_passages):
        item_id = f"book2-{i+1}"
        b2_ids.append(item_id)
        add_item({
            "id": item_id,
            "name": b2_titles[i],
            "level": 1,
            "category": "book-2-keeping",
            "sections": {
                "Verse": ct(passage),
                "About": b2_abouts[i],
                "Reflection": "What genuine relationship wisdom hides in Ovid's playful advice? Where does strategy end and real tenderness begin?"
            },
            "keywords": b2_keywords[i],
            "metadata": {"book": 2}
        })

    # =========================================================================
    # Book 3: Advice to Women
    # =========================================================================
    b3_passages = split_into_passages(book3_raw, 6)

    b3_titles = [
        "Arming the Amazons: Now Women Get Their Turn",
        "The Art of Appearance: Hair, Dress, and Grace",
        "Cultivate Your Mind: Song, Dance, and Letters",
        "Where to Be Seen and How to Attract",
        "The Arts of Intimacy: Timing, Tenderness, and Tears",
        "The Final Lesson: Shared Pleasure"
    ]
    b3_abouts = [
        "Having armed the men, Ovid now arms the women. Penthesilea's Amazons deserve equal instruction. He addresses the double standard head-on: if men are taught to pursue, women should be taught to respond with equal art. Not all women are Helens or Penelopes -- each has her own story.",
        "Beauty is partly nature, partly art. Ovid gives detailed advice on hairstyles, clothing, and cosmetics. Choose colors that suit your complexion. Don't let him see the workshop -- only the finished portrait. But above all, cultivate grace: an ungraceful beauty loses half her power.",
        "Learn to sing, to play the lyre, to dance. Read the poets -- especially Ovid. Write letters with feeling and wit. Intelligence and cultivation are more enduring attractions than physical beauty alone.",
        "Be seen at the right places. The theatre, the races, the temples. Walk with grace. Laugh sweetly but not loudly. Let your glance linger, then look away. The art of attraction is the art of attention -- giving it and withdrawing it in rhythm.",
        "Know when to yield and when to resist. Tears can be weapons, but use them sparingly. Jealousy, artfully deployed, keeps his attention. But cruelty destroys love -- the art is to seem difficult, not impossible.",
        "Love's final art is mutual pleasure. Ovid insists that both partners should find fulfillment. The greatest lovers are not the most beautiful but the most attentive. Nature made love to be shared, and the art of love is ultimately the art of generous attention."
    ]
    b3_keywords = [
        ["women", "amazons", "equality", "instruction", "fairness"],
        ["beauty", "appearance", "hair", "dress", "grace"],
        ["mind", "song", "dance", "letters", "cultivation"],
        ["attraction", "spectacle", "presence", "glance", "rhythm"],
        ["intimacy", "timing", "tears", "jealousy", "resistance"],
        ["pleasure", "mutuality", "attention", "generosity", "fulfillment"]
    ]

    b3_ids = []
    for i, passage in enumerate(b3_passages):
        item_id = f"book3-{i+1}"
        b3_ids.append(item_id)
        add_item({
            "id": item_id,
            "name": b3_titles[i],
            "level": 1,
            "category": "book-3-women",
            "sections": {
                "Verse": ct(passage),
                "About": b3_abouts[i],
                "Reflection": "How does Ovid's advice to women compare with his advice to men? Where does he subvert or reinforce the gender norms of his time?"
            },
            "keywords": b3_keywords[i],
            "metadata": {"book": 3}
        })

    # =========================================================================
    # L2 ITEMS - The Three Books
    # =========================================================================

    add_item({
        "id": "book-1-the-hunt",
        "name": "Book I: The Hunt -- Finding Love in Rome",
        "level": 2,
        "category": "book-grouping",
        "sections": {
            "About": "The first book addresses young men and maps the geography of desire across Augustan Rome. Ovid treats the city as a vast theatre of erotic possibility -- every temple, portico, racecourse, and banquet is a potential scene of encounter. His advice is pragmatic, witty, and subversively democratic: love is an art anyone can learn.",
            "For Readers": "Read Book I as both a guide to Roman social life and a meditation on desire as performance. Ovid's Rome is a city where everyone is both actor and audience, hunter and hunted."
        },
        "keywords": ["rome", "finding", "pursuit", "spectacle", "men"],
        "metadata": {},
        "composite_of": b1_ids
    })

    add_item({
        "id": "book-2-the-garden",
        "name": "Book II: The Garden -- Cultivating Lasting Love",
        "level": 2,
        "category": "book-grouping",
        "sections": {
            "About": "Book II shifts from conquest to cultivation. Love, once won, must be tended like a garden -- with patience, skill, and willingness to adapt. The myth of Daedalus frames the central lesson: find the middle way between too much and too little. Ovid's advice here is surprisingly modern: listen, adapt, forgive, and never stop paying attention.",
            "For Readers": "Beneath the playful surface, Book II contains genuine relationship wisdom about acceptance, flexibility, and the ongoing work of love. Compare Ovid's advice with modern relationship science."
        },
        "keywords": ["keeping", "cultivation", "patience", "adaptation", "moderation"],
        "metadata": {},
        "composite_of": b2_ids
    })

    add_item({
        "id": "book-3-the-mirror",
        "name": "Book III: The Mirror -- A Woman's Art of Love",
        "level": 2,
        "category": "book-grouping",
        "sections": {
            "About": "The boldest book: Ovid arms the other side. In a culture that prescribed passivity for women, he teaches them active artistry in love. While much of his advice concerns appearance, he also champions intellectual cultivation -- reading, music, conversation. The final lesson on mutual pleasure is remarkably egalitarian for its era.",
            "For Readers": "Book III is where Ovid is most subversive. By teaching women the same arts he taught men, he implicitly argues for a kind of erotic equality. Notice where his advice transcends its patriarchal context and where it remains bound by it."
        },
        "keywords": ["women", "equality", "cultivation", "pleasure", "subversion"],
        "metadata": {},
        "composite_of": b3_ids
    })

    # =========================================================================
    # L3 ITEMS - Meta-categories
    # =========================================================================

    add_item({
        "id": "meta-art-of-love",
        "name": "The Art of Love: Wit, Wisdom, and Subversion",
        "level": 3,
        "category": "meta-category",
        "sections": {
            "About": "Ovid's Ars Amatoria is at once a handbook, a comedy, a social satire, and a meditation on the nature of desire. Written in the last years of the Roman Republic's cultural flowering, it treats love as a learnable art -- democratic, playful, and endlessly renewable. Its frank celebration of pleasure and its egalitarian spirit ultimately got Ovid exiled from Rome, but the poem survived to influence troubadour poetry, Renaissance literature, and the entire Western tradition of writing about love.",
            "For Readers": "Read the Ars Amatoria as you would a witty friend's advice: some of it is timeless, some of it is bound to its era, and all of it reveals as much about the speaker as the subject. Ovid's greatest insight may be that love is an art not because it requires manipulation, but because it requires attention, adaptation, and the courage to be genuinely present."
        },
        "keywords": ["ovid", "art", "love", "rome", "wit", "wisdom", "subversion", "exile"],
        "metadata": {},
        "composite_of": ["book-1-the-hunt", "book-2-the-garden", "book-3-the-mirror"]
    })

    # =========================================================================
    # BUILD GRAMMAR
    # =========================================================================

    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {"name": "Ovid (Publius Ovidius Naso)", "date": "c. 2 CE", "note": "Author"},
                {"name": "Henry T. Riley", "date": "1885", "note": "Translator (literal English prose)"},
                {"name": "Project Gutenberg", "date": "2014", "note": "Source: eBook #47677 (https://www.gutenberg.org/ebooks/47677)"}
            ]
        },
        "name": "The Art of Love (Ars Amatoria)",
        "description": "Ovid's scandalous and brilliant verse manual on the art of love, in three books: finding love, keeping love, and a woman's guide to love. Written around 2 CE, it earned Ovid exile from Rome but became one of the most influential poems in Western literature. This prose translation by Henry T. Riley preserves the wit and structure of the original.\n\nSource: Project Gutenberg eBook #47677 (https://www.gutenberg.org/ebooks/47677)\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: John William Waterhouse's classical paintings of Roman love scenes (1890s-1900s); Sir Lawrence Alma-Tadema's paintings of Roman daily life and leisure (1870s-1900s); illustrations from 18th-century French editions of the Ars Amatoria.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": ["poetry", "love", "rome", "ovid", "instruction", "wit", "ancient-world", "desire", "gender", "relationships"],
        "roots": ["emotion-love"],
        "shelves": ["mirror"],
        "lineages": ["Gottman"],
        "worldview": "dialectical",
        "items": items
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    print(f"Built Art of Love grammar: {len(items)} items")
    for item in items:
        verse = item["sections"].get("Verse", "")
        print(f"  L{item['level']}: {item['id']} - {item['name']} ({len(verse)} chars)")


if __name__ == "__main__":
    build_grammar()
