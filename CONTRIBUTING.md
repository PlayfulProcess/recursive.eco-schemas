# Contributing to recursive.eco-schemas

Welcome! This repository is a commons for interpretive schemas used in divination and self-reflection practices. Your contributions help nurture the recursive public.

## How to Contribute

### Adding New Schemas

1. **Choose the Right Location**
   - Tarot interpretations → `/schemas/tarot/`
   - I Ching hexagrams → `/schemas/iching/`
   - Astrological data → `/schemas/astrology/`
   - Other systems → `/schemas/other/`

2. **Use Consistent Formats**
   - Prefer JSON or YAML for structured data
   - Include metadata: `source`, `tradition`, `contributor`
   - Add `description` fields to make schemas accessible

3. **Use the Unified Items Format**

   All grammars use the unified `items[]` array with flexible `sections: Record<string, string>`. This is the current standard — the editor always saves in this format.

   ```json
   {
     "id": "major-00-fool",
     "name": "The Fool",
     "sort_order": 0,
     "category": "major_arcana",
     "sections": {
       "Interpretation": "The beginning of all journeys...",
       "Reversed": "Fear of the unknown...",
       "Summary": "Innocence, new beginnings"
     },
     "keywords": ["new beginnings", "innocence", "spontaneity"],
     "image_url": "https://upload.wikimedia.org/..."
   }
   ```

   Section keys are flexible — use whatever makes sense for your content (`Story`, `Light`, `Shadow`, `For Young Readers`, `Karakatvas`, etc.). The viewer displays all sections.

### Grammar Type Must Match Content

Set `grammar_type` to match what your grammar actually contains. All types use the same unified `items[]` format:

- `"tarot"` — Must have card-style items with Interpretation/Reversed sections
- `"iching"` — Must have 64 hexagrams with line data (use the `lines` property)
- `"astrology"` — Must have items with planet/sign/house categories
- `"custom"` — Fully supported for everything else (chapter books, sequences, poetry, courses, folk tales, etc.)

Mismatched types (e.g., `"iching"` with only 10 items) will cause broken rendering in Flow. Legacy `interpretations[]` arrays still work but `items[]` is the way forward.

### Adding Templates

Templates go in `/templates/` and should:
- Be reusable across different contexts
- Include clear instructions or comments
- Specify any required variables or parameters

### Adding Data

Community data and examples go in `/data/`:
- Anonymize personal readings
- Include context about the reading
- Respect privacy and consent

## Guidelines

### Commons Principles

- **Share Generously**: Contribute knowledge freely
- **Credit Sources**: Honor traditions and teachers
- **Be Inclusive**: Welcome diverse interpretations
- **Stay Grounded**: Balance mysticism with accessibility

### Technical Standards

- Use UTF-8 encoding
- Follow existing file naming conventions
- Test JSON/YAML validity before committing
- Keep file sizes reasonable (< 1MB per file)

### Review Process

1. Submit a pull request with your changes
2. Provide context about your contribution
3. Engage with feedback constructively
4. Celebrate merged contributions!

## Questions?

Open an issue or reach out to the community. We're here to help!

## License

By contributing, you agree to share your contributions under the same license as the repository, making them part of the commons.
