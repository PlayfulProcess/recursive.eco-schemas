-- ============================================================================
-- rebuild-all-decks-meta.sql
-- ----------------------------------------------------------------------------
-- Regenerates the meta-grammar "The Tarot — All Decks, Many Lenses"
--   Supabase user_documents id = b03937bf-92be-414b-bd23-a85fe9be39eb
--   (recursive-eco project xtviwcznhbrsvkitepvm)
--
-- WHY THIS FILE EXISTS (drift control):
--   This meta INLINES a copy of every card (name, deck, suit, number, image_url,
--   per-deck editorial provenance, ref back to the source deck) from 12 source
--   decks. An inlined snapshot DRIFTS when a source deck changes. So the meta is
--   a *generated artifact*, not hand-maintained data. Never hand-edit it — fix
--   the source decks (or this script) and RE-RUN. It is idempotent: it fully
--   replaces document_data->'items' each run.
--
-- ORDER MATTERS: rehost a deck's Wikimedia images to R2 (scripts/r2-rehost.mjs)
--   BEFORE rebuilding, so the meta inherits R2 URLs, not 429-prone Wikimedia.
--
-- STRUCTURE (the canonical tarot taxonomy — nested, ~1001 items):
--   root-arcana "The Tarot — by Arcana · Suit · Number"
--     ├─ Major Arcana ─ 22 archetype nodes (0–21) ─ cards (that major across decks)
--     └─ Minor Arcana ─ 4 suits ─ 14 within-suit ranks ─ cards (e.g. Ace of Cups across decks)
--   axis-deck   "By Deck"               ─ 12 deck nodes ─ cards   (orthogonal lens)
--   axis-age    "By Age"                ─ 5 era nodes  ─ cards    (orthogonal lens)
--   axis-number "By Rank — across all suits" ─ 14 cross-suit rank nodes ─ cards
--                                       (numerology: every Ace/Two/…/King across suits)
--   Depth is computed by the tree-viewer from composite_of (computeLevel), so a
--   card legitimately appears under several parents (its within-suit rank, its
--   cross-suit rank, its deck, its era).
--
--   NOTE: augmented trumps (number > 21, e.g. Arlecchino) and suitless customs
--   have no archetype/rank node, so they appear only under By Deck / By Age.
--
-- EACH CARD CARRIES: ref_document_id/ref_item_id/ref_preview (click through to the
--   source deck for full meaning), metadata.editorial {date,maker,patron,context,
--   print,orientation}, metadata.source_deck_id/source_item_id, and readable
--   sections.Origin + "Find the meaning" (so the Journal AI can narrate origin).
--   Click-through resolves only for PUBLIC source decks (or the owner).
--
-- EDITORIAL lives in ed(...) keyed per deck (provenance is a deck property).
--   Historical decks sourced from the tarot lineage; modern decks kept general.
--
-- DERIVATIONS: suit names normalized to 4 canonical suits; minor rank parsed from
--   the card NAME (English rank word, direct or in parens) with a "<n> of <suit>"
--   digit fallback (schemes differ: Marseille/RWS 1..14, Etteilla global 1..78,
--   Tarocchino offset, Visconti non-numeric). era assigned per deck.
--
-- BACKUP FIRST: CREATE TABLE _backup_meta_<date> AS SELECT * FROM user_documents
--   WHERE id='b03937bf-92be-414b-bd23-a85fe9be39eb';
-- TO ADD/REMOVE A DECK: edit decks(...) and ed(...) and re-run.
-- ============================================================================
WITH decks(deck_id,label,era,era_sort) AS (
  VALUES
   ('58f8e047-417a-4a9f-bc1c-ea7fd43ecae2'::uuid,'Anecdotes Tarot','21st c · Contemporary',5),
   ('67314102-eeff-4ccb-a155-e022378ccb03'::uuid,'Arlecchino''s Augmented Arcana','21st c · Contemporary',5),
   ('bc1953b2-9e07-4f31-9635-d3968af49625'::uuid,'Clown Town Tarot','21st c · Contemporary',5),
   ('3a562b9a-50ff-4455-9579-edc080b9f4a2'::uuid,'Etteilla II','18th–19th c · Etteilla cartomancy',3),
   ('751cd7a0-3ec7-4fee-950e-9dc0a1c1bab7'::uuid,'Etteilla III','18th–19th c · Etteilla cartomancy',3),
   ('06286025-703b-4e9d-972c-3d85a8dde0a4'::uuid,'Path of the Ontoject','21st c · Contemporary',5),
   ('511521a4-2282-4797-aaaa-9b8088c40c65'::uuid,'Rider–Waite–Smith','20th c · Golden Dawn / RWS',4),
   ('6e4394c2-cbd7-4b8c-8917-d8594daf2814'::uuid,'Sola Busca','15th c · Renaissance Italy',1),
   ('36e33662-592a-485c-baba-e0c7896ea4ab'::uuid,'Tarot de Marseille','18th c · Tarot de Marseille',2),
   ('a8c5ad8e-5c0d-4679-ad08-8469fde639c9'::uuid,'The Recursive Tarot','21st c · Contemporary',5),
   ('b757c293-3c3b-44de-aa97-8a011ddea50a'::uuid,'Visconti-Sforza','15th c · Renaissance Italy',1),
   ('7ea72ae9-989c-4c2a-9d85-6b07fe08a70d'::uuid,'Tarocchino Arlecchino','21st c · Contemporary',5)
),
ed(deck_id,ed_date,ed_maker,ed_patron,ed_context,ed_print,ed_orient) AS (
  VALUES
   ('b757c293-3c3b-44de-aa97-8a011ddea50a'::uuid,'c. 1451','Bonifacio Bembo workshop (attrib.; some trumps later repainted, attrib. Antonio Cicognara)','House of Visconti–Sforza, Milan','Hand-painted ducal luxury deck, among the oldest surviving tarot','Hand-painted, gold leaf & tempera','Game (trionfi) — pre-divinatory'),
   ('6e4394c2-cbd7-4b8c-8917-d8594daf2814'::uuid,'c. 1491','Engraver unknown (Northern Italy)','Venetian / Ferrarese commission','Earliest complete 78-card deck with fully illustrated pips; humanist & alchemical imagery','Copper-plate engraving, hand-coloured','Game (esoteric imagery)'),
   ('36e33662-592a-485c-baba-e0c7896ea4ab'::uuid,'1760','Nicolas Conver, master cardmaker, Marseille','Commercial cardmaking trade','The canonical Tarot de Marseille woodblock pattern; later the occult era''s reference image','Woodcut with stencil colouring','Game (later adopted for divination)'),
   ('3a562b9a-50ff-4455-9579-edc080b9f4a2'::uuid,'1780s–1790s','Jean-Baptiste Alliette (Etteilla) & workshop','Parisian cartomancy public','Among the first decks purpose-built for fortune-telling','Engraving / woodcut, hand-coloured','Divination (purpose-built)'),
   ('751cd7a0-3ec7-4fee-950e-9dc0a1c1bab7'::uuid,'19th century','Etteilla tradition; later Grand Etteilla editors','Commercial esoteric publishers','A later Grand Etteilla edition continuing Alliette''s cartomantic system','Lithograph / engraving, coloured','Divination'),
   ('511521a4-2282-4797-aaaa-9b8088c40c65'::uuid,'1909','Pamela Colman Smith, directed by A. E. Waite','Published by William Rider & Son, London','Golden Dawn–derived; first mass-market deck with fully scene-illustrated minors','Lithograph (line & flat colour)','Divination'),
   ('58f8e047-417a-4a9f-bc1c-ea7fd43ecae2'::uuid,'Contemporary','recursive.eco community deck','—','A modern deck built on recursive.eco','Digital','Divination / journaling'),
   ('67314102-eeff-4ccb-a155-e022378ccb03'::uuid,'Contemporary','recursive.eco','—','A modern commedia-themed deck with an augmented (28-trump) major arcana','Digital','Game / divination'),
   ('bc1953b2-9e07-4f31-9635-d3968af49625'::uuid,'Contemporary','recursive.eco','—','A modern custom deck built on recursive.eco','Digital','Divination / play'),
   ('06286025-703b-4e9d-972c-3d85a8dde0a4'::uuid,'Contemporary','PlayfulProcess','—','A modern philosophical deck (Tillich-inflected) built on recursive.eco','Digital','Reflection / divination'),
   ('a8c5ad8e-5c0d-4679-ad08-8469fde639c9'::uuid,'Contemporary','PlayfulProcess / recursive.eco','—','A modern deck for meaning-makers and gateway-builders','Digital','Divination / meaning-making'),
   ('7ea72ae9-989c-4c2a-9d85-6b07fe08a70d'::uuid,'Contemporary','recursive.eco','—','A modern take on the Bolognese Tarocchino, a 62-card trick-taking game','Digital','Game (Bolognese tradition)')
),
suit_ord(suit_norm,sord) AS (VALUES ('Wands',1),('Cups',2),('Swords',3),('Coins',4)),
majnames(n,cname) AS (VALUES (0,'The Fool'),(1,'The Magician'),(2,'The High Priestess'),(3,'The Empress'),(4,'The Emperor'),(5,'The Hierophant'),(6,'The Lovers'),(7,'The Chariot'),(8,'Strength'),(9,'The Hermit'),(10,'Wheel of Fortune'),(11,'Justice'),(12,'The Hanged Man'),(13,'Death'),(14,'Temperance'),(15,'The Devil'),(16,'The Tower'),(17,'The Star'),(18,'The Moon'),(19,'The Sun'),(20,'Judgement'),(21,'The World')),
ranknames(r,rname) AS (VALUES (1,'Ace'),(2,'Two'),(3,'Three'),(4,'Four'),(5,'Five'),(6,'Six'),(7,'Seven'),(8,'Eight'),(9,'Nine'),(10,'Ten'),(11,'Page'),(12,'Knight'),(13,'Queen'),(14,'King')),
src AS (
  SELECT d.deck_id, d.label, d.era, d.era_sort, t.ord, it->>'id' AS src_item_id,
    it->'metadata'->>'arcana' AS arcana, lower(coalesce(it->'metadata'->>'suit','')) AS suit_raw,
    it->>'name' AS cname, it->>'image_url' AS image_url, it->'metadata'->>'number' AS num_raw,
    e.ed_date,e.ed_maker,e.ed_patron,e.ed_context,e.ed_print,e.ed_orient
  FROM decks d JOIN user_documents ud ON ud.id=d.deck_id LEFT JOIN ed e ON e.deck_id=d.deck_id
  CROSS JOIN LATERAL jsonb_array_elements(ud.document_data->'items') WITH ORDINALITY AS t(it,ord)
),
cards AS (
  SELECT 'card-'||replace(deck_id::text,'-','')||'-'||ord AS card_id,
    deck_id,label,era,era_sort,arcana,image_url,cname,ord,src_item_id,
    ed_date,ed_maker,ed_patron,ed_context,ed_print,ed_orient,
    CASE WHEN suit_raw ~ 'wand|baton|bastoni' THEN 'Wands' WHEN suit_raw ~ 'cup|coupe|coppe' THEN 'Cups'
         WHEN suit_raw ~ 'sword|epee|épée|spade' THEN 'Swords' WHEN suit_raw ~ 'coin|pentacl|denier|denari' THEN 'Coins' ELSE NULL END AS suit_norm,
    CASE WHEN arcana='major' AND num_raw ~ '^[0-9]+$' AND num_raw::int BETWEEN 0 AND 21 THEN num_raw::int ELSE NULL END AS major_num,
    CASE WHEN arcana='minor' THEN CASE
      WHEN lower(cname) ~ '\mace\M' THEN 1 WHEN lower(cname) ~ '\mtwo\M' THEN 2 WHEN lower(cname) ~ '\mthree\M' THEN 3
      WHEN lower(cname) ~ '\mfour\M' THEN 4 WHEN lower(cname) ~ '\mfive\M' THEN 5 WHEN lower(cname) ~ '\msix\M' THEN 6
      WHEN lower(cname) ~ '\mseven\M' THEN 7 WHEN lower(cname) ~ '\meight\M' THEN 8 WHEN lower(cname) ~ '\mnine\M' THEN 9
      WHEN lower(cname) ~ '\mten\M' THEN 10 WHEN lower(cname) ~ 'page|knave|valet|fante|maid|servante' THEN 11
      WHEN lower(cname) ~ 'knight|chevalier|cavall' THEN 12 WHEN lower(cname) ~ 'queen|reine|regina' THEN 13
      WHEN lower(cname) ~ 'king|\mroi\M|\mre\M' THEN 14
      WHEN cname ~ '^\s*\d+\s+of\s' THEN (substring(cname from '^\s*(\d+)\s+of\s'))::int ELSE NULL END ELSE NULL END AS rank_num
  FROM src
),
card_items AS (
  SELECT 0 grp, ord::int so, jsonb_build_object('id',card_id,'name',cname||' — '||label,'level',1,'category','card',
    'ref_document_id',deck_id::text,'ref_item_id',src_item_id,'ref_preview','study',
    'metadata',jsonb_strip_nulls(jsonb_build_object('deck',label,'arcana',arcana,'suit',suit_norm,'number',coalesce(major_num,rank_num),
      'source_deck_id',deck_id::text,'source_item_id',src_item_id,
      'editorial',jsonb_strip_nulls(jsonb_build_object('date',ed_date,'maker',ed_maker,'patron',NULLIF(ed_patron,'—'),'context',ed_context,'print',ed_print,'orientation',ed_orient)))),
    'sections',jsonb_build_object('Origin',coalesce(label||' · '||ed_date||' · '||ed_maker||'. '||ed_context||'. Print: '||ed_print||'. Made for: '||ed_orient||'.',label),
      'Find the meaning','From '||label||'. Click through to the source deck for this card''s full interpretation.'),
    'image_url',image_url,'sort_order',ord) item FROM cards
),
deck_nodes AS (
  SELECT 1 grp, era_sort*100 so, jsonb_build_object('id','deck-'||replace(deck_id::text,'-',''),'name',label,'level',2,'category','deck',
    'ref_document_id',deck_id::text,'ref_preview','cards','sections',jsonb_build_object('What it is',label||' — '||coalesce(max(ed_date),'')||'. Every card in this deck.'),
    'sort_order',1000+era_sort*20,'composite_of',jsonb_agg(card_id ORDER BY ord)) item FROM cards GROUP BY deck_id,label,era_sort
),
era_nodes AS (
  SELECT 2 grp, era_sort so, jsonb_build_object('id','era-'||era_sort,'name',era,'level',2,'category','era',
    'sections',jsonb_build_object('What it is','All cards from decks of this era: '||era||'.'),'sort_order',6000+era_sort,
    'composite_of',jsonb_agg(card_id ORDER BY card_id)) item FROM cards GROUP BY era,era_sort
),
wsr_nodes AS (
  SELECT 3 grp, 0 so, jsonb_build_object('id','wsr-'||lower(c.suit_norm)||'-'||c.rank_num,'name',rn.rname||' of '||c.suit_norm||' (all decks)','level',2,'category','rank',
    'sections',jsonb_build_object('What it is','The '||rn.rname||' of '||c.suit_norm||' across every deck.'),'sort_order',3000+so2.sord*20+c.rank_num,
    'composite_of',jsonb_agg(c.card_id ORDER BY c.card_id)) item
  FROM cards c JOIN ranknames rn ON rn.r=c.rank_num JOIN suit_ord so2 ON so2.suit_norm=c.suit_norm
  WHERE c.suit_norm IS NOT NULL AND c.rank_num IS NOT NULL GROUP BY c.suit_norm, c.rank_num, rn.rname, so2.sord
),
suit_ranks AS (SELECT DISTINCT suit_norm, rank_num FROM cards WHERE suit_norm IS NOT NULL AND rank_num IS NOT NULL),
suit_nodes AS (
  SELECT 4 grp, so2.sord so, jsonb_build_object('id','suit-'||lower(so2.suit_norm),'name',so2.suit_norm,'level',3,'category','suit',
    'sections',jsonb_build_object('What it is','The suit of '||so2.suit_norm||' (names normalized: Wands=Batons=Bastoni, Coins=Pentacles=Deniers, Cups=Coupes, Swords=Épées) — Ace through King across every deck.'),
    'sort_order',2900+so2.sord,'composite_of',(SELECT jsonb_agg('wsr-'||lower(sr.suit_norm)||'-'||sr.rank_num ORDER BY sr.rank_num) FROM suit_ranks sr WHERE sr.suit_norm=so2.suit_norm)) item
  FROM suit_ord so2 WHERE EXISTS (SELECT 1 FROM suit_ranks sr WHERE sr.suit_norm=so2.suit_norm)
),
majnum_nodes AS (
  SELECT 5 grp, m.n so, jsonb_build_object('id','num-major-'||m.n,'name',m.n||' — '||m.cname,'level',2,'category','archetype',
    'sections',jsonb_build_object('What it is',m.cname||' — Arcanum '||m.n||' — across the decks.'),'sort_order',4000+m.n,
    'composite_of',jsonb_agg(c.card_id ORDER BY c.card_id)) item FROM majnames m JOIN cards c ON c.major_num=m.n GROUP BY m.n,m.cname
),
xrank_nodes AS (
  SELECT 6 grp, r.r so, jsonb_build_object('id','num-rank-'||r.r,'name',r.rname||'s (every suit, all decks)','level',2,'category','rank-cross',
    'sections',jsonb_build_object('What it is','Every '||r.rname||' across all four suits and every deck — cross-suit numerology.'),'sort_order',7000+r.r,
    'composite_of',jsonb_agg(c.card_id ORDER BY c.card_id)) item
  FROM ranknames r JOIN cards c ON c.rank_num=r.r AND c.suit_norm IS NOT NULL GROUP BY r.r,r.rname
),
arcana_nodes AS (
  SELECT 7 grp, 1 so, jsonb_build_object('id','arc-major','name','Major Arcana','level',3,'category','arcana',
    'sections',jsonb_build_object('What it is','The 22 trumps (0–21), each composed of that archetype across every deck.'),'sort_order',2801,
    'composite_of',(SELECT jsonb_agg('num-major-'||n ORDER BY n) FROM (SELECT DISTINCT major_num n FROM cards WHERE major_num IS NOT NULL) a)) item
  UNION ALL SELECT 7,2, jsonb_build_object('id','arc-minor','name','Minor Arcana','level',4,'category','arcana',
    'sections',jsonb_build_object('What it is','The four suits, each composed of its ranks Ace–King across every deck.'),'sort_order',2802,
    'composite_of',(SELECT jsonb_agg('suit-'||lower(suit_norm) ORDER BY sord) FROM suit_ord so2 WHERE EXISTS (SELECT 1 FROM suit_ranks sr WHERE sr.suit_norm=so2.suit_norm)))
),
root_nodes AS (
  SELECT 8 grp, 1 so, jsonb_build_object('id','root-arcana','name','The Tarot — by Arcana · Suit · Number','level',5,'category','root',
    'sections',jsonb_build_object('What it is','The canonical tarot tree: Major Arcana by number, and Minor Arcana decomposing into four suits, each into its ranks Ace–King — every leaf gathered across all decks.'),'sort_order',9000,
    'composite_of',jsonb_build_array('arc-major','arc-minor')) item
  UNION ALL SELECT 8,2, jsonb_build_object('id','axis-deck','name','By Deck','level',3,'category','axis','render_as','pill-group','sort_order',9010,
    'sections',jsonb_build_object('What it is','Browse every card grouped by its source deck.'),
    'composite_of',(SELECT jsonb_agg('deck-'||replace(deck_id::text,'-','') ORDER BY era_sort,label) FROM decks))
  UNION ALL SELECT 8,3, jsonb_build_object('id','axis-age','name','By Age','level',3,'category','axis','render_as','pill-group','sort_order',9020,
    'sections',jsonb_build_object('What it is','Five centuries of decks, grouped by era.'),
    'composite_of',(SELECT jsonb_agg('era-'||era_sort ORDER BY era_sort) FROM (SELECT DISTINCT era_sort FROM decks) e))
  UNION ALL SELECT 8,4, jsonb_build_object('id','axis-number','name','By Rank — across all suits','level',3,'category','axis','render_as','pill-group','sort_order',9030,
    'sections',jsonb_build_object('What it is','Cross-suit numerology: every Ace, every Two … every King, gathered across all four suits and every deck.'),
    'composite_of',(SELECT jsonb_agg('num-rank-'||r ORDER BY r) FROM (SELECT DISTINCT rank_num r FROM cards WHERE rank_num IS NOT NULL AND suit_norm IS NOT NULL) a))
),
all_items AS (
  SELECT * FROM card_items UNION ALL SELECT * FROM deck_nodes UNION ALL SELECT * FROM era_nodes
  UNION ALL SELECT * FROM wsr_nodes UNION ALL SELECT * FROM suit_nodes UNION ALL SELECT * FROM majnum_nodes
  UNION ALL SELECT * FROM xrank_nodes UNION ALL SELECT * FROM arcana_nodes UNION ALL SELECT * FROM root_nodes
),
agg AS (SELECT jsonb_agg(item ORDER BY grp,so) items, count(*) n FROM all_items)
UPDATE user_documents ud
SET document_data = jsonb_strip_nulls(ud.document_data || jsonb_build_object('items',agg.items)
  || jsonb_build_object('name','The Tarot — All Decks, Many Lenses (meta)','default_view','tree','default_preview','tree',
       '_generated',true,'_do_not_hand_edit',true,'_rebuilt_at',now()::text,
       '_rebuild_note','Nested taxonomy: root-arcana -> Major/Minor -> Suit -> Rank -> card; plus By Deck and By Age. Generated by scripts/rebuild-all-decks-meta.sql.'))
FROM agg WHERE ud.id='b03937bf-92be-414b-bd23-a85fe9be39eb'
RETURNING agg.n AS total_items;

-- Post-run sanity (optional): expect dangling_refs=0, top-level = root-arcana/axis-deck/axis-age
-- WITH it AS (SELECT jsonb_array_elements(document_data->'items') i FROM user_documents WHERE id='b03937bf-92be-414b-bd23-a85fe9be39eb'),
--   ids AS (SELECT i->>'id' id FROM it),
--   refs AS (SELECT jsonb_array_elements_text(i->'composite_of') r FROM it WHERE i ? 'composite_of')
-- SELECT (SELECT count(*) FROM refs r LEFT JOIN ids ON ids.id=r.r WHERE ids.id IS NULL) dangling_refs;
