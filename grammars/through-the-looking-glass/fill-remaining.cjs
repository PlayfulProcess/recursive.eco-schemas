/**
 * Fill ALL remaining Looking Glass items with illustrations.
 * Uses non-primary illustrations from sibling L1 items for L2 chapters,
 * and thematically appropriate ones for themes/meta items.
 * No new R2 uploads needed — just references existing URLs.
 */
const fs = require('fs');
const grammar = JSON.parse(fs.readFileSync(__dirname + '/grammar.json', 'utf8'));
const r2 = JSON.parse(fs.readFileSync(__dirname + '/r2-illustrations.json', 'utf8'));

// Build a lookup of all existing illustration objects by URL
const allIllsByUrl = {};
for (const arr of Object.values(r2)) {
  arr.forEach(i => { allIllsByUrl[i.url] = i; });
}

// Helper: get an illustration from an item's R2 data, preferring non-primary
function getIll(itemId, preferNonPrimary = true) {
  const ills = r2[itemId];
  if (!ills || ills.length === 0) return null;
  if (preferNonPrimary) {
    const nonPri = ills.find(i => !i.is_primary);
    if (nonPri) return { ...nonPri, is_primary: false };
  }
  return { ...ills[0], is_primary: false };
}

// Helper: get a specific illustration by scene substring
function getByScene(itemId, sceneFragment) {
  const ills = r2[itemId];
  if (!ills) return null;
  const match = ills.find(i => i.scene.toLowerCase().includes(sceneFragment.toLowerCase()));
  return match ? { ...match, is_primary: false } : null;
}

// ============================================================
// MAPPING: Missing items → illustration source
// ============================================================
const assignments = {
  // === L2 Chapter items (use non-primary from child L1s, all unique!) ===
  'chapter-1':  getByScene('ch1-alice-and-the-kittens', 'talking to Kitty')     // Tenniel/Theaker
             || getIll('ch1-through-the-glass', true),
  'chapter-2':  getByScene('ch2-the-garden-of-live-flowers', 'Talking Tiger')   // Tenniel/Theaker
             || getIll('ch2-the-contrary-path', true),
  'chapter-3':  getByScene('ch3-looking-glass-insects', 'gnat')                 // Newell gnat
             || getIll('ch3-the-wood-where-things-have-no-names'),
  'chapter-4':  getByScene('ch4-the-walrus-and-the-carpenter', 'Walrus')       // Newell Walrus
             || getIll('ch4-the-battle-of-the-brothers'),
  'chapter-5':  getByScene('ch5-the-sheeps-shop', 'Sheep knitting')            // Tenniel/Theaker
             || getIll('ch5-the-white-queens-shawl'),
  'chapter-6':  getByScene('ch6-meeting-humpty-dumpty', 'Alice meets')          // Tenniel/Theaker
             || getIll('ch6-explaining-jabberwocky'),
  'chapter-7':  getByScene('ch7-the-kings-men', 'You alarm me')                // Newell
             || getIll('ch7-the-lion-and-the-unicorn'),
  'chapter-8':  getByScene('ch8-the-white-knights-inventions', 'White Knight')  // Tenniel/Theaker
             || getIll('ch8-the-battle-of-the-knights', true),
  'chapter-9':  getByScene('ch9-alice-seizes-the-tablecloth', 'Plates crashing')// Tenniel/Theaker
             || getIll('ch9-the-dinner-party'),
  'chapter-10': getIll('ch10-shaking'),                                         // Only option
  'chapter-11': getByScene('ch9-alice-seizes-the-tablecloth', 'Everything')     // Newell chaos
             || getIll('ch10-shaking'),
  'chapter-12': getByScene('ch1-alice-and-the-kittens', 'Now kitty')           // Full circle - kittens
             || getIll('ch1-through-the-glass'),

  // === Missing L1 items (use sibling illustrations from same chapter) ===
  'ch1-lets-pretend':       getByScene('ch1-through-the-glass', 'Through the glass')
                         || getIll('ch1-the-living-chess-pieces'),
  'ch3-the-railway-carriage': getByScene('ch3-looking-glass-insects', 'Elephant')
                           || getIll('ch3-looking-glass-insects'),
  'ch4-meeting-the-twins':  getByScene('ch4-the-battle-of-the-brothers', 'Dancing')
                         || getIll('ch4-the-red-kings-dream'),
  'ch5-living-backwards':   getIll('ch5-the-white-queens-shawl'),               // White Queen
  'ch5-rowing-and-rushes':  getByScene('ch5-the-sheeps-shop', 'Old sheep')
                         || getIll('ch5-the-sheeps-shop'),
  'ch6-the-meaning-of-words': getByScene('ch6-meeting-humpty-dumpty', 'Humpty Dumpty')
                            || getIll('ch6-humpty-dumptys-song-and-fall'),
  'ch8-the-aged-aged-man':  getByScene('ch8-the-white-knights-inventions', 'Head downward')
                         || getIll('ch8-becoming-a-queen'),
  'ch11-waking':            getIll('ch10-shaking'),                              // Shaking→Waking
  'ch12-which-dreamed-it':  getByScene('ch4-the-red-kings-dream', 'Red King')   // "Am I dreaming?"
                         || getIll('ch1-alice-and-the-kittens'),

  // === Theme items (thematically representative) ===
  'theme-language-wordplay': getByScene('ch6-explaining-jabberwocky', 'brillig') // "Twas brillig..."
                          || getIll('ch6-meeting-humpty-dumpty'),
  'theme-chess-game':       getByScene('ch1-the-living-chess-pieces', 'Chessmen')
                         || getByScene('ch2-the-contrary-path', 'chess-board'),
  'theme-identity':         getByScene('ch4-the-red-kings-dream', 'Red King')    // "Am I his dream?"
                         || getIll('ch3-the-wood-where-things-have-no-names'),
  'theme-mirrors-reversal': getByScene('ch1-through-the-glass', 'Little arms')   // Going through mirror
                         || getIll('ch1-through-the-glass'),
  'theme-authority-rules':  getByScene('ch2-meeting-the-red-queen', 'Red Queen')
                         || getIll('ch8-becoming-a-queen'),
  'theme-poetry-songs':     getByScene('ch1-jabberwocky', 'Jabberwock')          // Tenniel Jabberwock
                         || getIll('ch6-humpty-dumptys-song-and-fall'),

  // === Meta items ===
  'meta-narrative-journey':  getByScene('ch8-becoming-a-queen', 'Alice with crown') // Pawn→Queen
                          || getIll('ch2-running-to-stay-in-place'),
  'meta-themes-ideas':      getByScene('ch3-the-wood-where-things-have-no-names', 'fawn')
                         || getIll('ch7-the-lion-and-the-unicorn'),
};

// Apply assignments
let updated = 0;
for (const item of grammar.items) {
  if (item.image_url) continue; // Already has illustration

  const ill = assignments[item.id];
  if (!ill) {
    console.log('WARNING: No assignment for', item.id);
    continue;
  }

  const meta = item.metadata || {};
  meta.illustrations = [{ ...ill, is_primary: true }];
  item.metadata = meta;
  item.image_url = ill.url;
  updated++;
}

fs.writeFileSync(__dirname + '/grammar.json', JSON.stringify(grammar, null, 2));
console.log('Updated', updated, 'items');

const withIlls = grammar.items.filter(i => i.metadata && i.metadata.illustrations && i.metadata.illustrations.length > 0);
const withImg = grammar.items.filter(i => i.image_url);
const totalIlls = withIlls.reduce((sum, i) => sum + i.metadata.illustrations.length, 0);
console.log('Items with illustrations:', withIlls.length, '/', grammar.items.length);
console.log('Items with image_url:', withImg.length, '/', grammar.items.length);
console.log('Total illustration entries:', totalIlls);

const noIll = grammar.items.filter(i => !i.image_url);
if (noIll.length > 0) {
  console.log('\nStill missing:');
  noIll.forEach(i => console.log('  ' + i.id));
} else {
  console.log('\n✓ ALL items have illustrations!');
}
