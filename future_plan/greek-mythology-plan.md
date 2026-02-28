# Greek Mythology & Astrology — Unified Grammar Build Plan

> **Status**: CHARACTERS COMPLETE (54 items). Zodiac signs and myths are future work.

## Architecture

- **One file**: `custom/greek-mythology/grammar.json`
- **grammar_type**: `"astrology"` — chart UI integration
- **English names**: match chart positions by `name` (Jupiter, Saturn, etc.)
- **Levels**: L1 Primordials → L2 Titans+Primordial Children → L3 Titan Children+Olympians → L4 Next-Gen Gods → L5 Heroes+Cupid

## Current State (54 items)

| Level | Count | Contents |
|-------|-------|----------|
| L1 | 8 | Chaos, Gaia, Uranus, Pontus, Tartarus, Erebus, Nyx, Eros |
| L2 | 15 | 11 Titans (Saturn, Rhea, Oceanus, Tethys, Hyperion, Theia, Coeus, Phoebe, Mnemosyne, Themis, Iapetus) + Aether, Nereus, Typhon, Phanes |
| L3 | 13 | Latona, Helios, Selene, Eos, Prometheus, Atlas, Venus, Jupiter, Neptune, Pluto, Juno, Ceres, Vesta |
| L4 | 8 | Sun/Apollo, Moon/Diana, Mars, Mercury, Minerva, Vulcan, Bacchus, Proserpine |
| L5 | 10 | Cupid, Heracles, Perseus, Achilles, Odysseus, Theseus, Orpheus, Jason, Atalanta, Aeneas |

## Future Work

- **Zodiac signs** (12 items): Aries through Pisces at L1 with `category: "sign"`
- **Zodiac placements** (L2): composite_of planet + sign for chart integration
- **Myths** (~30 items): Creation cycle, Trojan War, Odyssey, Metamorphoses, Hubris tales
