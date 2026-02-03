#!/usr/bin/env python3
"""
Apply enrichment data to grammar.json cards.

This script reads enrichment-data.json and updates grammar.json
with book quotes, page numbers, and key insights.
"""

import json
import re
from pathlib import Path

def extract_best_quote(found_quotes, max_length=400):
    """Extract the most relevant quote from found_quotes."""
    if not found_quotes:
        return None, None

    # Prefer quotes with page numbers
    for quote in found_quotes:
        page = quote.get('page', '?')
        context = quote.get('context', '')

        # Skip if it's just metadata/noise
        if 'Complicit Figures' in context or 'schema' in context.lower():
            continue

        # Look for actual book content
        if 'Chapman' in context or 'Deconstructing' in context:
            # Extract a clean quote - look for quoted text
            quoted = re.findall(r'"([^"]{30,300})"', context)
            if quoted:
                return quoted[0], page

            # Otherwise extract a meaningful sentence
            sentences = re.split(r'(?<=[.!?])\s+', context)
            for sent in sentences:
                if len(sent) > 50 and len(sent) < max_length:
                    # Skip metadata sentences
                    if 'Copyright' not in sent and 'Created from' not in sent:
                        return sent.strip(), page

    return None, None

def update_card(card, enrichment):
    """Update a card with enrichment data."""
    if not enrichment:
        return card

    key_themes = enrichment.get('key_themes', [])
    page_refs = enrichment.get('page_refs', [])
    found_quotes = enrichment.get('found_quotes', [])

    # Extract best quote
    quote, page = extract_best_quote(found_quotes)

    # Get or create sections
    sections = card.get('sections', {})

    # Only update if we have meaningful new content
    if quote and 'Source' not in sections:
        page_str = page if page and page != '?' else ', '.join(page_refs)
        sections['Source'] = f"Chapman & Withers ({page_str}): \"{quote[:300]}...\""

    if key_themes and 'Key Insight' not in sections:
        sections['Key Insight'] = key_themes[0].replace('_', ' ').title()

    card['sections'] = sections
    return card

def main():
    base_path = Path(__file__).parent.parent
    enrichment_path = base_path / "data" / "enrichment-data.json"
    grammar_path = base_path / "grammar.json"

    # Load files
    with open(enrichment_path) as f:
        enrichment_data = json.load(f)

    with open(grammar_path) as f:
        grammar = json.load(f)

    # Track updates
    updated = 0

    # Update each card
    for item in grammar['items']:
        card_id = item.get('id', '')

        if card_id in enrichment_data:
            enrichment = enrichment_data[card_id]

            # Check if card needs updating (no Source section yet)
            sections = item.get('sections', {})
            if 'Source' not in sections or len(sections.get('Source', '')) < 50:
                item = update_card(item, enrichment)
                updated += 1
                print(f"Updated: {card_id}")

    # Save updated grammar
    with open(grammar_path, 'w') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    print(f"\nTotal cards updated: {updated}")

if __name__ == "__main__":
    main()
