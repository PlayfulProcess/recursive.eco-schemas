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

3. **Example Schema Structure**
   ```json
   {
     "id": "major_arcana_0",
     "name": "The Fool",
     "number": 0,
     "tradition": "Rider-Waite-Smith",
     "keywords": ["new beginnings", "innocence", "spontaneity"],
     "interpretation": {
       "upright": "...",
       "reversed": "..."
     },
     "source": "community",
     "contributors": ["username"]
   }
   ```

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
