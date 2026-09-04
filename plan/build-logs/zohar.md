# Build Log: Zohar

**Grammar**: NOT BUILT
**Source**: `sources/zohar` (11KB, JSON)
**Type**: from-source-text (attempted)
**Status**: SKIPPED — source file is 95% empty

---

## Source Analysis

- JSON format with 53 Torah portion names as section keys
- Only `Bereshit[85]` has actual text — 7 short passages about flame meditation / mystical unity
- 52 out of 53 sections are completely empty arrays
- The "Addenda" section has a dict with 3 empty volumes (all empty)
- This appears to be a **skeleton/schema** from Sefaria's API, not actual content

## Why It Failed

The source file is essentially metadata without text. You cannot build a meaningful grammar from 7 passages. The file gives us the structure (53 parashot) but none of the actual Kabbalistic commentary.

## What's Needed

| Option | Source | Notes |
|--------|--------|-------|
| Sefaria API | `https://www.sefaria.org/api/texts/Zohar` | Need to paginate through all 53 sections |
| Sefaria website | `https://www.sefaria.org/Zohar` | Full Pritzker Edition (Daniel Matt translation) |
| Sacred-texts.com | `https://www.sacred-texts.com/jud/zdm/` | Older Sperling/Simon translation, public domain |
| Manual upload | User provides complete text file | Replace `sources/zohar` |

## Recommended Approach

1. User runs: `curl` or `WebFetch` against Sefaria API to pull all 53 sections
2. Or: user downloads from sacred-texts.com (public domain, no API needed)
3. Once text is available, parse like Confucius — split on structural delimiters within each parasha
4. Expected structure: L1 = individual passages/zoharic fragments, L2 = parashot (Torah portions), L3 = the 5 Books of Moses

## Prompt for When Source is Available

```
Parse the Zohar text organized by Torah portions (parashot).
The Zohar has 53+ sections corresponding to the weekly Torah readings.
Group passages by parasha (L1), group parashot by the 5 Books (L2).
The text is Aramaic/Hebrew commentary — expect mystical/allegorical language.
Section names: Bereshit, Noach, Lech Lecha, Vayera, Chayei Sarah, etc.
```
