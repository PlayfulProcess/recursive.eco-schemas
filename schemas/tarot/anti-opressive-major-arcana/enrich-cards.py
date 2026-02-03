#!/usr/bin/env python3
"""
Systematic enrichment of tarot cards with source book context.

This script:
1. Reads grammar.json cards
2. Searches outline.md for relevant quotes
3. Outputs enriched content with page numbers and quotes

Usage:
    python enrich-cards.py [--card-id <id>] [--all] [--output json|markdown]
"""

import json
import re
import argparse
from pathlib import Path

# Card ID to search terms mapping
# Add more cards here as needed
CARD_SEARCH_CONFIG = {
    "rosa-parks": {
        "search_terms": ["Rosa Parks", "Montgomery", "bus boycott", "trained organizer"],
        "key_themes": ["organizing infrastructure", "not spontaneous", "strategic choice"],
        "page_refs": ["73-75"]
    },
    "claudette-colvin": {
        "search_terms": ["Claudette Colvin", "nine months before", "not the right person"],
        "key_themes": ["erased from history", "respectability politics", "movement strategy"],
        "page_refs": ["73-74"]
    },
    "jane-addams": {
        "search_terms": ["Jane Addams", "Hull-House", "eugenics", "health certificates", "feebleminded"],
        "key_themes": ["neither demonize nor romanticize", "both radical AND complicit"],
        "page_refs": ["40-51"]
    },
    "mary-richmond": {
        "search_terms": ["Mary Richmond", "casework", "friendly visiting", "married vagabond"],
        "key_themes": ["scientific charity", "moral regulation", "professionalization"],
        "page_refs": ["31-32"]
    },
    "ida-b-wells": {
        "search_terms": ["Ida B. Wells", "anti-lynching", "Southern Horrors", "1892"],
        "key_themes": ["parallel social work", "excluded from canon", "radical activism"],
        "page_refs": ["60"]
    },
    "albert-rose": {
        "search_terms": ["Albert Rose", "Africville", "two hours", "relocation", "Regent Park"],
        "key_themes": ["expert knowledge", "community destruction", "urban renewal"],
        "page_refs": ["62-70"]
    },
    "aaron-pa-carvery": {
        "search_terms": ["Pa Carvery", "Carvery", "final holdout", "1970"],
        "key_themes": ["resistance", "community", "last to leave"],
        "page_refs": ["70"]
    },
    "richard-henry-pratt": {
        "search_terms": ["Richard Henry Pratt", "Carlisle", "Kill the Indian", "1892 Conference"],
        "key_themes": ["boarding schools", "cultural genocide", "social work origins"],
        "page_refs": ["60-61"]
    },
    "oscar-mcculloch": {
        "search_terms": ["Oscar McCulloch", "Tribe of Ishmael", "parasite", "1888"],
        "key_themes": ["eugenic doctrine", "indiscriminate relief", "get hold of the children"],
        "page_refs": ["35"]
    },
    "emma-goldman": {
        "search_terms": ["Emma Goldman", "anarchist", "eugenics", "radical complicity"],
        "key_themes": ["radicals were eugenicists too", "not always on side of justice"],
        "page_refs": ["28-29, 38"]
    },
    "viola-desmond": {
        "search_terms": ["Viola Desmond", "Canada's Rosa Parks", "Roseland", "decade before"],
        "key_themes": ["Canadian racism", "earlier resistance", "national mythology"],
        "page_refs": ["67, 74"]
    },
    "booker-t-washington": {
        "search_terms": ["Booker T. Washington", "assimilative measures", "Du Bois", "Wells"],
        "key_themes": ["accommodation vs. resistance", "critiqued by radicals"],
        "page_refs": ["48"]
    },
    "martin-luther-king-jr": {
        "search_terms": ["Martin Luther King", "I Have a Dream", "1963", "Malcolm X"],
        "key_themes": ["sanitized legacy", "radical reality", "anti-racist poles"],
        "page_refs": ["68"]
    },
    "malcolm-x": {
        "search_terms": ["Malcolm X", "King", "Africville", "1965"],
        "key_themes": ["killed before Africville emptied", "integration debate"],
        "page_refs": ["68"]
    },
    # Add more cards...
}

def load_outline(path: Path) -> str:
    """Load the outline.md source text."""
    return path.read_text(encoding='utf-8')

def load_grammar(path: Path) -> dict:
    """Load the grammar.json."""
    return json.loads(path.read_text(encoding='utf-8'))

def find_quotes(text: str, search_terms: list, context_lines: int = 3) -> list:
    """Find relevant quotes containing search terms."""
    lines = text.split('\n')
    quotes = []

    for i, line in enumerate(lines):
        for term in search_terms:
            if term.lower() in line.lower():
                # Get context
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                context = '\n'.join(lines[start:end])

                # Try to extract page number
                page_match = re.search(r'(\d{1,3})\s+Deconstructing|page[s]?\s*(\d+)', context, re.I)
                page = page_match.group(1) or page_match.group(2) if page_match else "?"

                quotes.append({
                    "term": term,
                    "context": context.strip(),
                    "page": page,
                    "line": i
                })
                break  # Only one match per line

    return quotes

def extract_direct_quotes(text: str) -> list:
    """Extract direct quotes (text in quotation marks)."""
    # Match text in various quote styles
    patterns = [
        r'"([^"]{20,300})"',  # Standard quotes
        r'"([^"]{20,300})"',  # Smart quotes
        r"'([^']{20,300})'"   # Single quotes (for quotes within quotes)
    ]

    quotes = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        quotes.extend(matches)

    return quotes

def enrich_card(card_id: str, outline_text: str, config: dict) -> dict:
    """Generate enriched content for a card."""
    if card_id not in config:
        return {"error": f"No config for {card_id}"}

    card_config = config[card_id]
    quotes = find_quotes(outline_text, card_config["search_terms"])

    # Extract the most relevant direct quotes
    all_context = '\n'.join([q["context"] for q in quotes])
    direct_quotes = extract_direct_quotes(all_context)

    return {
        "card_id": card_id,
        "search_terms": card_config["search_terms"],
        "key_themes": card_config["key_themes"],
        "page_refs": card_config["page_refs"],
        "found_quotes": quotes[:5],  # Top 5 matches
        "direct_quotes": direct_quotes[:3],  # Top 3 direct quotes
        "suggested_enrichment": {
            "Context": f"[Enrich with specific details from pages {', '.join(card_config['page_refs'])}]",
            "Source": f"Chapman & Withers ({', '.join(card_config['page_refs'])}): [Add key quote here]",
            "Key Insight": card_config["key_themes"][0] if card_config["key_themes"] else ""
        }
    }

def main():
    parser = argparse.ArgumentParser(description="Enrich tarot cards with book context")
    parser.add_argument("--card-id", help="Specific card ID to enrich")
    parser.add_argument("--all", action="store_true", help="Process all configured cards")
    parser.add_argument("--list", action="store_true", help="List all configured cards")
    parser.add_argument("--output", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()

    base_path = Path(__file__).parent
    outline_path = base_path / "outline.md"
    grammar_path = base_path / "grammar.json"

    if args.list:
        print("Configured cards:")
        for card_id in CARD_SEARCH_CONFIG:
            print(f"  - {card_id}")
        return

    outline_text = load_outline(outline_path)

    if args.card_id:
        result = enrich_card(args.card_id, outline_text, CARD_SEARCH_CONFIG)
        if args.output == "json":
            print(json.dumps(result, indent=2))
        else:
            print(f"\n## {args.card_id}\n")
            print(f"**Pages**: {', '.join(result.get('page_refs', []))}")
            print(f"**Key themes**: {', '.join(result.get('key_themes', []))}")
            print("\n**Direct quotes found:**")
            for q in result.get("direct_quotes", []):
                print(f"  > \"{q[:100]}...\"")

    elif args.all:
        results = {}
        for card_id in CARD_SEARCH_CONFIG:
            results[card_id] = enrich_card(card_id, outline_text, CARD_SEARCH_CONFIG)

        if args.output == "json":
            print(json.dumps(results, indent=2))
        else:
            for card_id, result in results.items():
                print(f"\n## {card_id}")
                print(f"Pages: {', '.join(result.get('page_refs', []))}")

if __name__ == "__main__":
    main()
