# Plan: Move Grimm's Fairy Tales to Compost

## The Argument

The Brothers Grimm's *Kinder- und Hausmärchen* (1812–1857) is not a folklore collection. It is a **nationalist editorial project** — a deliberate construction of "German-ness" through curated, rewritten, and sanitized oral tales.

### What the Grimms Actually Did

1. **Collected from literate middle-class informants**, not peasants. Their primary sources (the Hassenpflug and Wild families) were educated, French-speaking Huguenot descendants. The "authentic German peasant voice" was a fiction.

2. **Rewrote extensively across seven editions** (1812–1857). Wilhelm Grimm systematically:
   - Added Christian morality (punishing wickedness, rewarding piety)
   - Removed sexual content and replaced biological mothers with stepmothers
   - Germanified tales that were actually French, Italian, or pan-European (Cinderella = Perrault, Sleeping Beauty = Basile)
   - Added nationalist framing — the tales were presented as evidence of an ancient, continuous "German spirit"

3. **Served an explicit political agenda.** The Grimms were philologists working during German unification (1815–1871). Their fairy tale project, their German dictionary, and their German grammar were all part of the same nationalist enterprise: proving that a unified Germany had deep cultural roots.

4. **Obscured actual folk tradition.** By smoothing, Christianizing, and Germanifying the tales, the Grimms buried the real oral traditions — which were messy, sexual, violent, cross-cultural, regionally specific, and often told by women whose names we'll never know. The Grimm version replaced the real thing.

### Why This Is Compost, Not Just "Old"

The Grimm project is specifically **composting material** because:

- It presents **manufactured national identity as authentic folklore** — the original colonial move
- It erases the actual women and storytellers who carried these tales
- It claims pan-European (and often Middle Eastern/Asian) tales as "German"
- It naturalizes a hierarchy of "civilized" (Christian, German, patriarchal) vs. "primitive"
- Its structure has been weaponized: the Nazis used Grimm's tales extensively in propaganda and education
- Disney's adaptations (Snow White, Cinderella, Sleeping Beauty) further laundered the nationalist project into "universal" children's culture

The tales themselves aren't the problem. "Cinderella" existed in China (Ye Xian, 850 CE) and Egypt and Italy long before the Grimms. The problem is the **editorial project** that claimed these stories for one nation and one worldview.

## What Changes

### 1. Move grammar to compost shelf

Update `grammars/grimms-fairy-tales/grammar.json`:
- Add `"shelves": ["composting"]`
- Add `"roots": ["european-philosophy"]`
- Add `"worldview": "dialectical"`
- Add `"lineages": ["Andreotti"]` (Vanessa Andreotti's work on "hospicing modernity" directly addresses this kind of colonial knowledge production)
- Add composting-related tags: `"nationalist-project"`, `"editorial-folklore"`, `"composting"`
- Update `description` to include a composting note explaining WHY this is on the composting shelf

### 2. Add decomposer metadata

Add a new top-level field `"composting_context"` with:
- What needs composting (the nationalist editorial project, not the tales themselves)
- Who decomposes it (Jack Zipes, Marina Warner, Ruth Bottigheimer — scholars who exposed the Grimm myth)
- What grows from the compost (the Roots grammars — Moana, Frozen II — that reconnect fairy tales to living cultural traditions rather than nationalist projects)

### 3. Update WHAT_IS_COMPOST.md

Add Grimm's Fairy Tales to the compost table:

| Source | What Needs Composting | Decomposer |
|--------|----------------------|------------|
| Brothers Grimm — Kinder- und Hausmärchen | Nationalist editorial project disguised as authentic folklore; erasure of actual storytellers; Germanification of pan-European tales; manufactured cultural purity | Jack Zipes, Marina Warner, Ruth Bottigheimer; the actual folk traditions (Polynesian, Sámi, West African) that demonstrate what living oral culture looks like |

### 4. Delete empty storyboard folder

`grammars/grimms-fairy-tales-storyboard/` is empty — remove it.

### 5. Regenerate manifest

Run `python3 scripts/generate_manifest.py` to reflect the shelf change.

## What Does NOT Change

- The grammar stays in `grammars/grimms-fairy-tales/` (grammars are flat, compost is a shelf tag, not a folder move)
- The tales themselves remain intact — compost is not deletion
- The grammar remains fully functional in the viewer
- No tales are removed or altered

## The Composting Gesture

The Grimm grammar sits on the `composting` shelf alongside Kipling, Lobato, and Gobineau — not because fairy tales are bad, but because the **editorial project** that packaged them is a colonial technology.

The decomposers are:
- **Scholars** (Zipes, Warner, Bottigheimer) who documented what the Grimms actually did
- **Living traditions** (Polynesian wayfinding, Sámi joik, West African Anansi) that show what real oral culture looks like — messy, multilingual, female-voiced, regionally specific, and connected to land rather than nation
- **The ATU Index** itself — which reveals that "Grimm's tales" are pan-human stories the Grimms merely branded

The new growth is already happening: the Roots of Moana and Roots of Frozen II grammars connect children to the REAL cultural traditions behind their favorite stories, rather than passing off a 19th-century editorial project as timeless folklore.
