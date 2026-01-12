# recursive.eco-schemas

Where community's schemas of interpretation for tarot, I Ching, Astrology and Others live and nurture the recursive public.

## Purpose

This repository serves as a collaborative space for the recursive.eco community to share and maintain JSON-formatted interpretation schemas for various divination and symbolic systems. These schemas are published on the recursive.eco website and are meant to be freely shared, adapted, and improved by the community.

## Structure

The repository is organized by divination system:

```
├── tarot/
│   ├── rider-waite-smith/
│   │   ├── grammar.json      # Card definitions, meanings
│   │   ├── LICENSE           # CC-BY-SA-4.0
│   │   └── README.md         # Description, attribution chain
│   └── thoth/
│       └── README.md         # Placeholder for contributions
├── iching/
│   └── README.md             # Placeholder for contributions
└── SCHEMA.md                 # Format specification
```

## Getting Started

### Using the Schemas

All schemas are available in JSON format and can be freely used in your applications. Each schema includes:
- **Structured data** for programmatic access
- **Interpretations** based on traditional sources
- **Attribution** to honor the sources and contributors
- **Open licenses** (typically CC-BY-SA-4.0) for collaboration

### Contributing

We welcome contributions! To add a new deck, tradition, or system:

1. **Choose your system** - Navigate to the appropriate directory (tarot, iching, etc.)
2. **Create a subdirectory** - Name it after your deck/tradition
3. **Add required files**:
   - `grammar.json` - Your interpretation data (see SCHEMA.md for format)
   - `LICENSE` - License information (we recommend CC-BY-SA-4.0)
   - `README.md` - Description and attribution chain
4. **Submit a pull request** - Share your contribution with the community

Please read [SCHEMA.md](SCHEMA.md) for detailed format specifications.

## Available Systems

### Tarot
- **Rider-Waite-Smith** - The classic tarot deck (partial implementation, contributions welcome!)
- **Thoth** - Placeholder, contributions needed

### I Ching
- Contributions needed for various traditions

### Future Systems
- Astrology
- Runes
- Oracle decks
- And more...

## License

Individual schemas have their own licenses (see LICENSE file in each directory). We encourage using open licenses like CC-BY-SA-4.0 to foster collaboration.

The repository structure and documentation are released under CC0 (Public Domain).

## Community

This project is part of the recursive.eco ecosystem. Join us in building a collaborative, open resource for divination and symbolic interpretation systems.

## Support

For questions or discussions, please open an issue or join the recursive.eco community. 
