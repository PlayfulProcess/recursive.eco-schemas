/**
 * Merge Luiza Lian grammar sources:
 *   1. grammars/luiza-lian/grammar.json (backup) — deployed version with YouTube + PT lyrics
 *   2. schemas/tarot/luiza-lian-poetry — tarot schema with Yoruba English translations
 */
const fs = require('fs');
const path = require('path');

const deployedPath = path.join(__dirname, '..', 'grammars', 'luiza-lian', 'grammar.backup.json');
const schemaPath = path.join(__dirname, '..', 'schemas', 'tarot', 'luiza-lian-poetry');
const outputPath = path.join(__dirname, '..', 'grammars', 'luiza-lian', 'grammar.json');

// Make backup first
const originalPath = path.join(__dirname, '..', 'grammars', 'luiza-lian', 'grammar.json');
if (!fs.existsSync(deployedPath)) {
  fs.copyFileSync(originalPath, deployedPath);
  console.log('Created backup at grammar.backup.json');
}

const deployed = JSON.parse(fs.readFileSync(deployedPath, 'utf8'));
const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));

// ============================
// EXPLICIT ID-to-SchemaID mappings
// Built by comparing deployed names vs schema names
// ============================
const DEPLOYED_TO_SCHEMA = {
  // Album 1: Luiza Lian (2016)
  // Chororô, Me Tema, Protetora, Gula — NOT in schema (different songs on YouTube vs album)
  'yt-_g3IoYH3noY': 'luiza-lian-03-onibus-lotado',      // Ônibus Lotado
  'yt-XrfQrD2ED9Y': 'luiza-lian-05-coroa-de-flores',     // Coroa de Flores
  'yt-9Av_Auxb-jc': 'luiza-lian-06-falador',             // Falador
  'yt-OIOOv5SbMp4': 'luiza-lian-08-linda-linda',          // Linda Linda
  'yt-iKzPXWHm698': 'luiza-lian-09-a-luz-do-velle',       // A Luz da Vela / A Luz do Velle
  'yt-ZWEIjXv5nXA': 'luiza-lian-10-escuta-ze',            // Escuta Zé
  'yt-j32t1GLbmHk': 'luiza-lian-11-jardim',               // Jardim
  'yt-0HJLhYS9eNI': 'luiza-lian-12-mississipi-luz',       // Mississipi / Luz
  'yt-dAbBos3s5_o': 'luiza-lian-13-luna',                  // Luar / Luna

  // Album 2: Oyá Tempo (2017)
  'yt-yjj0rySbdbI': 'oya-tempo-01-tucum',                 // Tucum
  'yt-tTsUwAaWIlg': 'oya-tempo-02-tem-luz',               // Tem Luz
  'yt-J_kmvlXLy1I': 'oya-tempo-03-oya-tempo',             // Oyá
  'yt-DnHhQjdR_SU': 'oya-tempo-04-flash',                 // Flash
  'yt-ulNE5qJPtl4': 'oya-tempo-05-cadeira',               // Cadeira
  'yt-9egWeibGcHU': 'oya-tempo-06-po-de-ouro',            // Pó de Ouro
  'yt-XyNYBRGQ_e8': 'oya-tempo-07-manada',                // Manada
  'yt-J6o0ePv4h2M': 'oya-tempo-08-e-nela',                // É Nela Que Se Mora?

  // Album 3: Azul Moderno (2018)
  'yt-nPyFOtjsfUI': 'azul-moderno-01-vem-dizer-tchau',    // Vem Dizer Tchau
  'yt-yZEkeA6AxYw': 'azul-moderno-02-mil-mulheres',       // Mil Mulheres
  'yt-5wZJVun6WJo': 'azul-moderno-03-sou-yaba',           // Sou Yabá
  'yt-_eflzHsPqjA': 'azul-moderno-04-mira',               // Mira
  'yt-oFKwTpk9-vo': 'azul-moderno-05-iarinhas',           // Iarinhas
  'yt-3sbVciJBLXs': 'azul-moderno-06-pomba-gira',         // Pomba Gira do Luar
  'yt-OluAiwNlFhk': 'azul-moderno-07-geladeira',          // Geladeira
  'yt-kyT-MeBUcIU': 'azul-moderno-08-noticias-japao',     // Notícias do Japão
  'yt-pret04SXgF0': 'azul-moderno-09-santa-barbara',      // Santa Bárbara
  'yt-sH4gJp_Y4_M': 'azul-moderno-10-azul-moderno',       // Azul Moderno

  // Album 4: 7 Estrelas (2023)
  'yt-KMU2UK9i45Q': 'sete-estrelas-07-eu-estou-aqui',     // Eu Estou Aqui
};

// Also match 7 Estrelas visualizers by name pattern
const SETE_ESTRELAS_NAME_MAP = {
  'A Minha Música É': 'sete-estrelas-01-minha-musica',
  'Tecnicolor': 'sete-estrelas-02-tecnicolor',
  'Homenagem': 'sete-estrelas-03-homenagem',
  'Forca': 'sete-estrelas-04-forca',
  'Cobras na sua Mesa': 'sete-estrelas-05-cobras',
  'Viajante': 'sete-estrelas-06-viajante',
  'Eu Estou Aqui': 'sete-estrelas-07-eu-estou-aqui',
  'Desabriga': 'sete-estrelas-08-desabriga',
  '7 Estrelas': 'sete-estrelas-09-sete-estrelas',
  'Deságua': 'sete-estrelas-10-desagua',
};

// Build schema lookup by ID
const schemaById = {};
for (const item of schema.items) {
  schemaById[item.id] = item;
}

function cleanName(rawName) {
  return rawName.trim()
    .replace(/\s*-\s*#\w+/g, '')           // Remove " - #OyaTempo"
    .replace(/\s*-\s*Luiza Lian.*$/i, '')   // Remove " - Luiza Lian (Visualizer)"
    .replace(/\s*\(Clipe\)/i, '')           // Remove "(Clipe)"
    .replace(/\s*\(Visualizer\)/i, '')      // Remove "(Visualizer)"
    .replace(/\s*\(visualizer\)/i, '')
    .replace(/\s*\(feat\.?\s*.*?\)/i, '')   // Remove "(feat. ...)" but keep base name
    .replace(/^\s+/, '')
    .trim();
}

function extractLyricsAndCredits(notes) {
  if (!notes) return { lyrics: '', credits: '' };
  const lines = notes.split('\n');
  const lyricsLines = [];
  const creditsLines = [];
  let inCredits = false;
  let songTitleSeen = false;

  for (const line of lines) {
    const t = line.trim();
    // Skip URLs, hashtags
    if (t.startsWith('http') || t.startsWith('#') || t === '*' || t === '**') continue;
    // Skip header/promo lines
    if (/^(luizalian\.com|Oyá Tempo - Album|Produzido por|Mixado e Master|Lançado pelo|Faixa \d|Nas Redes|Follow|Spotify:|Twitter:|Instagram:|Facebook:|Deezer:|selo RISCO|Listen:|Escute nas plat)/i.test(t)) continue;
    // Detect credits
    if (/^(Ficha Técnica|Luiza Lian: voz|Músicos|Composição:|Co-?Produção:|Gravado no|Mixagem:|Masterização:|Produção:|Arte:|Animação|Realização:|Ass\.?\s)/i.test(t)) {
      inCredits = true;
    }
    if (inCredits) {
      if (t) creditsLines.push(t);
    } else {
      lyricsLines.push(line);
    }
  }
  return {
    lyrics: lyricsLines.join('\n').replace(/^\n+/, '').replace(/\n+$/, ''),
    credits: creditsLines.join('\n').trim(),
  };
}

// Orixá detection
const ORIXA_PATTERNS = {
  'Oxum': /oxum|odoyá|cachoeira|pó de ouro|rainha.*coração/i,
  'Yemanjá': /yemanjá|janaína|ondas do mar|sou yabá|mareia.*rainha/i,
  'Oyá/Iansã': /oyá|iansã|santa bárbara|vendaval|tempestade|temporal/i,
  'Nanã': /nanã/i,
  'Exu/Pomba Gira': /exu|pomba gira|encruzilhada/i,
  'Ogum': /ogum/i,
  'Oxóssi': /oxóssi/i,
  'Xangô': /xangô|justiça.*deus/i,
  'Caboclos': /cabocl|boiadeiro|marinheiro|juremá/i,
};

const enrichedItems = [];
const orixaIndex = {};
let merged = 0;
const unmatched = [];

for (const dItem of deployed.items) {
  if (dItem.level === 2) {
    enrichedItems.push(dItem); // Keep L2 emergences as-is
    continue;
  }
  if (dItem.level === 3) {
    continue; // Skip old L3 meta-emergences — we recreate them fresh below
  }

  // Find matching schema item
  let sItem = null;
  if (DEPLOYED_TO_SCHEMA[dItem.id]) {
    sItem = schemaById[DEPLOYED_TO_SCHEMA[dItem.id]];
  }
  // Try 7 Estrelas name match
  if (!sItem) {
    const clean = cleanName(dItem.name);
    for (const [nameKey, schemaId] of Object.entries(SETE_ESTRELAS_NAME_MAP)) {
      if (clean === nameKey || clean.startsWith(nameKey)) {
        sItem = schemaById[schemaId];
        break;
      }
    }
  }

  // Try extracting lyrics from Creator's Notes (original YouTube import format)
  const { lyrics, credits } = extractLyricsAndCredits(dItem.sections?.["Creator's Notes"]);
  const clean = cleanName(dItem.name);

  // Build sections — preserve existing Português/Credits if extractLyricsAndCredits found nothing
  const sections = {};
  const existingPT = dItem.sections?.["Português"];
  const existingCredits = dItem.sections?.["Credits"];
  if (lyrics) sections["Português"] = lyrics;
  else if (existingPT) sections["Português"] = existingPT;
  if (sItem?.sections?.["Yoruba English"]) sections["Yoruba English"] = sItem.sections["Yoruba English"];
  if (sItem?.sections?.["Reflection"]) sections["Reflection"] = sItem.sections["Reflection"];
  if (credits) sections["Credits"] = credits;
  else if (existingCredits) sections["Credits"] = existingCredits;
  // Preserve any other existing sections (About, etc.)
  for (const [key, val] of Object.entries(dItem.sections || {})) {
    if (!sections[key] && key !== "Creator's Notes") sections[key] = val;
  }

  // Detect album
  let album = 'Luiza Lian (2016)';
  const name = dItem.name;
  if (name.includes('OyaTempo') || name.includes('Oyá')) album = 'Oyá Tempo (2017)';
  if (name.includes('AzulModerno')) album = 'Azul Moderno (2018)';
  if (sItem?.category === 'Oyá Tempo') album = 'Oyá Tempo (2017)';
  if (sItem?.category === 'Azul Moderno') album = 'Azul Moderno (2018)';
  if (sItem?.category === '7 Estrelas') album = '7 Estrelas (2023)';
  // Check by composite_of in L2 emergences
  for (const em of deployed.items.filter(i => i.level === 2)) {
    if (em.composite_of?.includes(dItem.id)) {
      if (em.name.includes('Oya')) album = 'Oyá Tempo (2017)';
      if (em.name.includes('Azul')) album = 'Azul Moderno (2018)';
      if (em.name.includes('7 Estrelas')) album = '7 Estrelas (2023)';
    }
  }
  // Special 7 Estrelas items
  if (name.includes('Visualizer') || name.includes('7 Estrelas') ||
      dItem.id === 'yt-KMU2UK9i45Q' || clean === 'O Coração Batendo No Corpo Todo (Esperar o Sol)' ||
      clean === 'Alumiô') {
    if (!album.includes('Oyá') && !album.includes('Azul')) album = '7 Estrelas (2023)';
  }

  // Keywords
  const keywords = [...new Set([
    ...(sItem?.keywords || []),
    ...(dItem.keywords || []).filter(k => k !== 'Luiza Lian'),
  ])];
  if (keywords.length === 0) keywords.push(clean.split(/\s+/)[0].toLowerCase());

  // Orixá detection
  const allText = JSON.stringify(sections) + ' ' + keywords.join(' ') + ' ' + clean;
  for (const [orixa, pattern] of Object.entries(ORIXA_PATTERNS)) {
    if (pattern.test(allText)) {
      if (!orixaIndex[orixa]) orixaIndex[orixa] = [];
      orixaIndex[orixa].push(dItem.id);
    }
  }

  // Metadata
  const metadata = { ...dItem.metadata, album: album.replace(/\s*\(\d{4}\)/, '') };
  if (sItem?.metadata?.spotify_url) metadata.spotify_url = sItem.metadata.spotify_url;
  if (sItem?.metadata?.featuring) metadata.featuring = sItem.metadata.featuring;

  enrichedItems.push({
    id: dItem.id,
    name: clean,
    level: 1,
    category: album,
    sort_order: dItem.sort_order,
    origin: dItem.origin,
    keywords,
    metadata,
    sections,
    image_url: dItem.image_url,
  });

  if (sItem) merged++;
  else unmatched.push(clean);
}

// ============================
// L3 META-EMERGENCES
// ============================
const metas = [];

// 1. Yabá — Feminine Divine (ALL female orixá songs)
const yabaIds = [...new Set([
  ...(orixaIndex['Oxum'] || []),
  ...(orixaIndex['Yemanjá'] || []),
  ...(orixaIndex['Oyá/Iansã'] || []),
  ...(orixaIndex['Nanã'] || []),
  ...(orixaIndex['Exu/Pomba Gira'] || []),
])];
metas.push({
  id: 'meta-yaba',
  name: 'Yabá — The Feminine Divine',
  level: 3,
  category: 'meta-emergence',
  sort_order: 200,
  keywords: ['Yabá', 'feminine divine', 'orixá', 'queen mother'],
  metadata: {
    orixas: ['Oxum', 'Yemanjá', 'Oyá/Iansã', 'Nanã', 'Pomba Gira'],
  },
  sections: {
    'Yoruba English': 'Yabá means queen-mother in Yoruba. She is not one goddess — she is the principle of feminine sovereignty itself. When Luiza sings "Sou Yabá," she is not choosing one deity. She is claiming the throne that all the female orixás share: the power to create, to destroy, to transform, to hold, to release.\n\nOxum brings the gold. Yemanjá brings the ocean. Oyá brings the storm. Nanã brings the primordial clay. Pomba Gira brings the crossroads and desire. Together, they are not a pantheon — they are a technology of feminine power that survived slavery, colonization, and erasure.',
    'For Americans': 'Imagine if Beyoncé, Nina Simone, Billie Holiday, Aretha Franklin, and Erykah Badu were not just musicians but actual spiritual forces that people pray to, make offerings to, and receive in their bodies during ceremony. That\'s what the Yabás are. Not metaphors. Not symbols. Living presences. And Luiza channels them all.',
    'Reflection': 'Which Yabá speaks loudest in your life right now? Are you in an Oxum season (beauty, diplomacy, inner gold)? An Oyá season (destruction, transformation, letting go)? A Yemanjá season (mothering, oceanic grief, vast holding)?',
  },
  image_url: '',
  composite_of: yabaIds,
  relationship_type: 'emergence',
});

// 2. Águas Sagradas — Sacred Waters (Oxum + Yemanjá + water references)
const waterIds = [...new Set([
  ...(orixaIndex['Oxum'] || []),
  ...(orixaIndex['Yemanjá'] || []),
])];
metas.push({
  id: 'meta-sacred-waters',
  name: 'Águas Sagradas — Sacred Waters',
  level: 3,
  category: 'meta-emergence',
  sort_order: 201,
  keywords: ['Oxum', 'Yemanjá', 'water', 'ocean', 'river', 'cachoeira', 'Iara'],
  metadata: {
    orixas: ['Oxum', 'Yemanjá'],
    note: 'Iarinhas (little Iaras) are river spirits connected to Oxum\'s domain. The Iara is the Brazilian mermaid — indigenous, not European — who sings in the rivers of São Paulo that the city buried under concrete.',
  },
  sections: {
    'Yoruba English': 'Oxum rules the sweet waters — rivers, waterfalls, lakes. She is gold, honey, fertility, and the diplomacy that prevents war. Yemanjá rules the salt waters — the ocean, motherhood, the boundary between life and death.\n\nWhen Luiza sings "Iarinhas," she is singing about the Iaras — the river spirits of indigenous Brazilian mythology. But the rivers she names (Tietê, Tapajós, Tamanduateí) are São Paulo\'s buried rivers, paved over by the city. The Iarinhas are still singing underneath the concrete. This is Oxum\'s territory — fresh water, urban and wild at once.\n\nWhen she sings "Sou Yabá" and declares "eu danço nas ondas do mar" (I dance on the waves of the sea), she crosses from Oxum\'s rivers into Yemanjá\'s ocean. The movement from fresh to salt water is also the movement from life to death to rebirth.',
    'For Americans': 'For an American, think of the Mississippi — Robert Johnson\'s blues river. Now imagine that river has a goddess. And that every waterfall, every lake, every ocean has its own deity with specific songs, colors, foods, and days of the week. That\'s the Afro-Brazilian relationship to water. It\'s not metaphor. When Bahians throw flowers into the ocean on February 2nd for Yemanjá, millions of people participate. It\'s one of the largest religious celebrations in the Americas.',
    'Reflection': 'Where does your inner river meet the sea? What is the difference between your fresh-water self (intimate, golden, close) and your salt-water self (vast, deep, borderless)?',
  },
  image_url: '',
  composite_of: waterIds,
  relationship_type: 'emergence',
});

// 3. Encruzilhada — Crossroads
const crossIds = orixaIndex['Exu/Pomba Gira'] || [];
if (crossIds.length > 0) {
  metas.push({
    id: 'meta-crossroads',
    name: 'Encruzilhada — The Crossroads',
    level: 3,
    category: 'meta-emergence',
    sort_order: 202,
    keywords: ['Exu', 'Pomba Gira', 'crossroads', 'Jurema', 'desire'],
    metadata: { orixas: ['Exu', 'Pomba Gira'] },
    sections: {
      'Yoruba English': 'Exu is the messenger. Without him, no prayer is heard, no offering received. The colonizers called him devil — he is not. He is the principle of communication, of movement, of the space between.\n\nPomba Gira is his feminine counterpart. She spins at the crossroads in her red dress, laughing at what scares you. She is desire without shame, power without permission.\n\nIn "Pomba Gira do Luar," Luiza enters the Jurema (an indigenous-Afro-Brazilian spiritual tradition) and finds her at the crossroads with a moonlit king. The crossroads is where you make choices. It\'s where transformation begins.',
      'For Americans': 'Robert Johnson went to the crossroads at midnight. In Afro-Brazilian tradition, you don\'t go there to sell your soul — you go to find your path. Exu is more like Hermes than Satan: the trickster-messenger who opens and closes doors. Pomba Gira is like a divine Josephine Baker — unapologetically sexual, fiercely free, and sacred precisely because of her refusal to be tamed.',
      'Reflection': 'What crossroads are you standing at? What choice keeps presenting itself? And what would Pomba Gira do — she who never asks permission?',
    },
    image_url: '',
    composite_of: crossIds,
    relationship_type: 'emergence',
  });
}

// 4. Tempestade — Storm & Transformation (Oyá)
const stormIds = orixaIndex['Oyá/Iansã'] || [];
if (stormIds.length > 0) {
  metas.push({
    id: 'meta-storms',
    name: 'Tempestade — Storm & Transformation',
    level: 3,
    category: 'meta-emergence',
    sort_order: 203,
    keywords: ['Oyá', 'Iansã', 'storm', 'transformation', 'wind', 'death'],
    metadata: { orixas: ['Oyá', 'Iansã', 'Santa Bárbara'] },
    sections: {
      'Yoruba English': 'Oyá (Iansã) is the storm itself. She carries the dead to the other side. She sweeps the marketplace clean with her irukere (horsehair whisk). An entire album bears her name: Oyá Tempo — Oyá + Time — because transformation is not a moment, it is the weather of existence.\n\nWhen the slavers banned the orixás, the enslaved people dressed their gods in Catholic clothes. Oyá became Santa Bárbara — patron saint of lightning. The syncretism was survival technology. Luiza sings both names because both are true.',
      'For Americans': 'If Beyoncé\'s "Lemonade" is about alchemy — turning pain into art — Oyá Tempo is about learning that you ARE the storm. Not surviving it. Being it. The wind does not resist itself.',
      'Reflection': 'What storm are you — not surviving — but actually being? What transformation would happen if you stopped sheltering and started blowing?',
    },
    image_url: '',
    composite_of: stormIds,
    relationship_type: 'emergence',
  });
}

// 5. Caboclos — Indigenous Spirit Guides
const cabocloIds = orixaIndex['Caboclos'] || [];
if (cabocloIds.length > 0) {
  metas.push({
    id: 'meta-caboclos',
    name: 'Caboclos — Indigenous Spirit Guides',
    level: 3,
    category: 'meta-emergence',
    sort_order: 204,
    keywords: ['caboclo', 'boiadeiro', 'marinheiro', 'indigenous', 'Jurema'],
    metadata: { entities: ['Caboclo', 'Boiadeiro', 'Marinheiro'] },
    sections: {
      'Yoruba English': 'Caboclos are indigenous Brazilian spirit guides who work in Umbanda and Jurema traditions. They are not orixás — they are ancestors of the land itself. The Boiadeiro (cowboy spirit) teaches direction: "always walking with the herd, you cannot look at the ground." The Marinheiro (sailor spirit) teaches balance: "in the swaying of my boat I teach you to balance."\n\nLuiza channels these spirits alongside the orixás, weaving indigenous and African traditions together — as they have always been woven in Brazilian spiritual practice.',
      'For Americans': 'Imagine Native American spirit guides meeting West African deities in the body of a São Paulo electronic musician. That\'s what\'s happening. Brazil\'s spirituality braids indigenous, African, Catholic, and Kardecist spiritist traditions into something that exists nowhere else on Earth.',
      'Reflection': 'What indigenous wisdom of your own land have you forgotten? What spirits of place are singing underneath your concrete?',
    },
    image_url: '',
    composite_of: cabocloIds,
    relationship_type: 'emergence',
  });
}

enrichedItems.push(...metas);

// Build final grammar
const grammar = {
  name: 'Luiza Lian: Cartografia do Sagrado',
  description: `Luiza Lian is a São Paulo artist whose music braids MPB, electronic production, and Afro-Brazilian spirituality into a living cartography of the sacred. Across four albums — her self-titled debut (2016), Oyá Tempo (2017), Azul Moderno (2018), and 7 Estrelas | quem arrancou o céu? (2023) — she maps where the orixás live inside modern Brazilian life: in crowded buses, empty refrigerators, buried rivers, and torn skies.

She is not performing religion. She is channeling it — the way a river channels rain.

This grammar holds each song as a card. Portuguese lyrics sit beside Yoruba English translations — not word-for-word but spirit-for-spirit transmissions that carry cultural and spiritual context across languages. The meta-emergences reveal deeper constellations: the Yabás (feminine orixás), Sacred Waters (Oxum & Yemanjá), the Crossroads (Exu & Pomba Gira), and Storms of Transformation (Oyá/Iansã).

Produced by Charles Tixier. Co-produced by Tim Bernardes (O Terno). Released on selo RISCO.`,
  cover_image_url: deployed.cover_image_url,
  tags: [
    'poetry', 'music', 'brazilian', 'yoruba', 'animist', 'orixá',
    'mpb', 'electronic', 'afro-brazilian', 'candomblé', 'umbanda',
    'luiza-lian', 'são-paulo', 'feminine-divine', 'cultural-translation',
  ],
  grammar_type: 'tarot',
  attribution: {
    source_name: 'Luiza Lian — Complete Discography',
    source_author: 'Luiza Lian',
    license: 'CC-BY-SA-4.0',
    note: 'Original music and Portuguese lyrics by Luiza Lian. Yoruba English translations by PlayfulProcess. Produced by Charles Tixier, co-produced by Tim Bernardes. Released on selo RISCO.',
  },
  items: enrichedItems,
};

fs.writeFileSync(outputPath, JSON.stringify(grammar, null, 2));

console.log(`\n=== Luiza Lian Grammar Merge ===`);
console.log(`L1 songs: ${enrichedItems.filter(i => i.level === 1).length}`);
console.log(`L2 album emergences: ${enrichedItems.filter(i => i.level === 2).length}`);
console.log(`L3 meta-emergences: ${enrichedItems.filter(i => i.level === 3).length}`);
console.log(`Merged with Yoruba English: ${merged}/${enrichedItems.filter(i => i.level === 1).length}`);
if (unmatched.length > 0) {
  console.log(`Without translations: ${unmatched.join(', ')}`);
}
console.log(`\nOrixá constellations:`);
for (const [o, ids] of Object.entries(orixaIndex)) {
  console.log(`  ${o}: ${ids.length} songs`);
}
console.log(`\n✓ Written to ${outputPath}`);
