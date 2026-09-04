# Plan — Public, GitHub-Backed, Contributable Tarot (and one-click branched import)

**Status: PLAN ONLY (no code yet).** Revised after investigating recursive-eco's
actual infrastructure (the `grammar-backup` and `github-grammar` API routes,
`lib/grammar/community.ts`). The short version: **most of what we want already
exists** — it's the "Community grammar" layer, and it is already backed by the
PUBLIC `recursive.eco-schemas` repo, not the private `grammar-vault`.

Companion docs: `tarot-of-all-tarots-master-plan.md`, `tarot-roadmap-and-supabase-log.md`.

---

## 1. Investigation findings — there are TWO GitHub layers already

| | **grammar-vault** (private) | **recursive.eco-schemas** (PUBLIC) |
|---|---|---|
| Route | `/api/grammar-backup` | `/api/github-grammar` |
| Env | `GITHUB_BACKUP_REPO=grammar-vault`, `GITHUB_GRAMMAR_VAULT_TOKEN` | `GITHUB_GRAMMAR_REPO=recursive.eco-schemas`, `GITHUB_GRAMMAR_TOKEN` |
| Path | `{user_id}/{document_id}.json` | `{folder}/{slug}/grammar.json` (folders: **tarot**, iching, sequences, astrology, custom, classics) |
| Who writes | owner + invited editors (pending→merge workflow) | **any authenticated user** (`save-community`) |
| Visibility | **private** | **public** (it's a public repo) |
| Features | per-save auto backup, version history, restore, editor pending/merge/reject | version history, **conflict detection (SHA 409)**, `_original_creator` + `editors[]`, **contribution tracking** (`grammar_contributions`) + **notifications** to creator, GitHub raw URL |
| Grammar state | Draft / Published | **Community** ("public + GitHub-backed, anyone-can-edit") |

**So the thing you described — "back it up in *this* github instead of the private
vault, get all community features, hold a link people can see / pull latest /
contribute to" — is exactly the existing _Community grammar_ state, and its repo is
already `recursive.eco-schemas` (the very repo where the decks were built).**

The grammar-vault is a *different thing*: it's your personal, private, per-save
version backup of YOUR grammars (any state). It is not where public collaboration
happens. Public collaboration = the Community layer above.

### The one concrete gap
The app's Community layer reads/writes the **top-level `tarot/` folder**
(`tarot/<slug>/grammar.json`) — but the 15 new decks were built in **`grammars/<slug>/`**.
So today they are public *files in a public repo*, but the app does NOT yet treat them
as Community grammars (wrong folder). Fixing that is the crux (see §3).

---

## 2. What this means (revised recommendation)

**Do NOT build a separate independent repo + a parallel importer.** Instead, use the
infrastructure that already exists:

- `recursive.eco-schemas` IS the public, contributable, GitHub-backed home. Keep it.
- Put the tarot decks in the **`tarot/` community folder** so the app recognises them
  as Community grammars → public, GitHub-linked, **anyone-can-edit**, version history,
  conflict detection, contribution tracking + creator notifications. And because the
  repo is public, people can ALSO fork / open PRs on GitHub directly.
- The private `grammar-vault` keeps doing its job for personal drafts. Untouched.
- A standalone `recursive-tarot` repo is then **optional** (a curated public mirror for
  forum collaborators / releases) — nice-to-have, not the mechanism. (Earlier draft of
  this doc over-rotated on it.)

> "Hold a link to that exclusive repo so anybody can see / push latest / contribute"
> is already provided: each community grammar carries `_community_folder` + `_community_slug`,
> the app builds the raw GitHub URL (`buildGitHubUrl`, default repo `recursive.eco-schemas`),
> and exposes `?community=<url>` (edit) and `?copyFrom=<url>` (fork) entry points.
> We should also surface a plain "View / contribute on GitHub" link in the reader.

---

## 3. The crux: get the 15 decks into the Community layer

Decision needed — how the `grammars/` build output becomes `tarot/` community grammars:

- **Option A (recommended): generators output to `tarot/`.** Point the deck generators
  + `stamp_archetypes.py` + the tree generator at `tarot/<slug>/grammar.json`, and add the
  community metadata the app expects (`_community_folder:"tarot"`, `_community_slug`,
  `_original_creator`, `editors[]`). One home, app-native.
- **Option B: a sync step** copies `grammars/*tarot*` → `tarot/` and injects community
  metadata. Keeps the `grammars/` library convention; adds a build step.
- Either way: **add `_original_creator` (PlayfulProcess user id) + `_community_slug`** so
  the contribution/notification machinery and conflict detection work.

(Also reconcile with repo CLAUDE.md, which currently documents `grammars/` as the home;
the app's truth is the `tarot/` community folder.)

---

## 4. "One-click import as several branched grammars" — thin layer on top

With the decks as community grammars, the collection import is small:

- Each deck is loaded/copied via the EXISTING community path (`?community=<rawUrl>` to
  edit-in-place as the public grammar, or `?copyFrom=<rawUrl>` to fork a private copy).
- A **collection manifest** in the repo (`tarot/_collection.json`) lists the deck slugs,
  their branch (Dummett A/B/C / occult / sui-generis), and the meta-tree's reference
  edges (which `tree-of-tarot` leaf points to which deck slug).
- A small **"Import the Tarot Collection" action** in recursive-eco loops the manifest:
  for each slug, upsert the community grammar into `user_documents` (idempotent on
  `_community_slug`); collect new Supabase ids; then set the `tree-of-tarot` leaves'
  `ref_document_id` from that map (the wiring step). Decks first, meta last.
- **Branch selector**: the manifest's branch field lets the UI offer "import all" or a
  subset (e.g. just the occult branch) — the "several different branched grammars."

This reuses the community load/save/copy code; the only *new* surface is the batch loop
+ the meta-tree id-wiring. (Per-deck import, version history, conflict detection,
contribution tracking all come for free from the Community layer.)

---

## 5. Images
Unchanged from before: for a robust public collection, mirror Wikimedia images to R2
once (`mirror_images_to_r2.py`) and rewrite `image_url`/`illustrations[].url` to R2, so
the public grammars don't depend on Wikimedia hotlinks. (Today they hotlink Commons,
some via `Special:FilePath?width=` to render TIFs.)

---

## 6. Open decisions (for you)

1. **Move decks to `tarot/` (Option A) or sync (Option B)?** A is cleaner/app-native.
2. **Add `_original_creator` + community metadata to the 15 decks now?** (cheap, unblocks
   everything; makes them real Community grammars.)
3. **Surface a "View / contribute on GitHub" link in the reader** for community grammars?
   (Probably yes — directly answers "anybody could see / push / contribute.")
4. **Collection import**: build the batch action in recursive-eco, or keep importing
   decks one at a time via the existing community flow at first?
5. **Standalone `recursive-tarot` mirror repo** — still want it as a curated forum-facing
   artifact, or is the public `tarot/` folder in schemas enough? (Likely enough.)
6. **Images → R2** before public seed (recommended) or hotlink Wikimedia to start?

---

## 7. Phases

- **P0:** add community metadata (`_community_folder`, `_community_slug`,
  `_original_creator`, `editors[]`) to the 15 decks + meta-tree; place/sync them into
  `tarot/`. Now they're real Community grammars (public, contributable, version-controlled).
- **P1:** write `tarot/_collection.json` (slugs + branches + reference edges).
- **P2:** recursive-eco — a "View/contribute on GitHub" link on community grammars (small),
  then the batch "Import the Tarot Collection" action (loop manifest → upsert → wire tree).
- **P3:** image mirror to R2; optional standalone `recursive-tarot` mirror + release.

---

## 8. One-line summary

What you want already exists as the **Community grammar** layer, backed by the **public
`recursive.eco-schemas` repo** (not the private grammar-vault): public, GitHub-linked,
anyone-can-edit, versioned, contribution-tracked. The only real work is **moving the 15
decks into the `tarot/` community folder with community metadata**, then a **thin batch
importer** (reusing the existing community load + a meta-tree id-wiring step) to bring
them in as several branch-linked grammars in one click.

---

## 9. Repo-local previews + branch-aware sync (Layers A & B)

Goal: let a contributor work entirely on **their own computer / GitHub** — edit a grammar
file, **see it render** (cards / tree / study) without the app, push a branch, then
optionally **pull that branch into recursive.eco and render the whole tree**. This is the
"GitHub is the backend, viewers are thin" vision made real.

**Key enabler (already exists):** recursive.eco's shared `GrammarLoader`
(`apps/landing/assets/js/components/grammar-loader.js`) is already source-abstracted —
`loadFromSupabase(id)` AND `loadFromGitHub(path)` (default repo `recursive.eco-schemas`).
The static viewers (`grammar-viewer.html`, `tree-viewer.html`, `study-viewer.html`) run
through it. So the previews are mostly **reuse**, not new code.

### Layer A — repo-local static previews (do first; cheap, high value)
- Add `site/` (or `previews/`) to the repo containing **copies of the shared loader +
  the cards / tree / study viewers**, with two added source modes:
  - **local file:** `cards.html?file=tarot/visconti-sforza-tarot/grammar.json`
    (served by a tiny local server — document `python -m http.server` / `npx serve` — or
    drag-drop the JSON; browsers can't `fetch()` `file://` directly).
  - **branch:** `tree.html?path=tarot/visconti-sforza-tarot&ref=<branch>` → loads from
    `raw.githubusercontent.com/.../<branch>/...` (the loader's GitHub mode + a branch param).
- **Tree across files:** the tree viewer resolves the meta-grammar's leaf references by
  **slug/path locally** (and by Supabase id in the app) — the slug-based `reference_edges`
  in §3/§4 already support both.
- **GitHub Pages:** deploy `site/` so the previews are live URLs (no clone needed) — the
  basis for `tarot.recursive.eco` (§10).
- **Anti-drift rule:** keep the repo's loader/viewers as **verbatim copies** of the app's
  (or have the app's build copy them out) so there's one source of truth for the format.

### Layer B — branch-aware app integration (later, in recursive-eco)
- **Branch-aware version history in Create:** the history panel today reads `main`; add a
  branch ref so a contributor's pushed branch shows up.
- **Pull-a-branch-render-the-whole-tree:** extend the batch importer (§4) with a branch
  param — pull a branch's whole collection into Supabase and render the tree. Reuse the
  community-save **SHA/conflict** logic so a branch pull and an app edit don't clobber.
- This is the bigger piece; Layer A delivers most of the value without it.

---

## 10. The course + `tarot.recursive.eco` static site

Ship the whole thing as a **self-contained public site** on GitHub Pages — decks + the
genealogy tree + repo-local previews (§9) + a **course** teaching the Claude-Code workflow.

- **Course:** `course/build-a-tarot-deck-with-claude.mdx` — recursive.eco course style
  (MDX frontmatter: id/title/description/duration/author/date), teaching "how to work like
  the maintainer works with Claude Code": clone → pick a public-domain deck → build it as a
  grammar with Claude Code (generators-as-research) → source PD images from Wikimedia
  Commons (the API + `?width=` TIF tricks) → honest scholarship (game-not-divination,
  no forced equivalences, the archetype tags) → preview locally → push / PR → render in app.
  *(Written alongside this plan.)*
- **Course viewer:** copy recursive.eco's `course-viewer.html` (+ the MDX loader) into
  `site/` so the course renders as a page — same reuse pattern as the grammar viewers.
- **`tarot.recursive.eco`:** point this subdomain at the GitHub Pages deploy of `site/`.
  Result: one public URL where anyone can **read the decks, walk the tree, take the course,
  and preview their own edits** — entirely from the public repo, no app account needed.
- This is the forum-facing artifact that earlier drafts wanted a separate repo for — but it
  rides on the existing public repo, so no second source of truth.

### Revised phases (supersedes §7 tail)
- **P0:** community metadata on the 15 decks + meta-tree; place into `tarot/`.
- **P1:** `tarot/_collection.json` (slugs + branches + reference edges).
- **P2 (Layer A + course):** `site/` with copied loader/viewers (local-file + branch modes)
  + the course + course-viewer; GitHub Pages → `tarot.recursive.eco`.
- **P3 (recursive-eco):** "View/contribute on GitHub" link; the batch "Import the Tarot
  Collection" action; then **Layer B** (branch-aware history + branch pull).
- **P4:** image mirror to R2; optional vault-skip gate for community grammars.
