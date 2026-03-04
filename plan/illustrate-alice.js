const fs = require('fs');
const path = require('path');

const grammarPath = path.join(__dirname, '..', 'literature', 'alice-in-wonderland-chapter-book', 'grammar.json');
const g = JSON.parse(fs.readFileSync(grammarPath, 'utf8'));

const IMG = (id) => 'https://drive.google.com/uc?export=view&id=' + id;

const imageMap = {
  // Chapter 1: Down the Rabbit-Hole
  'ch01-bored-by-the-river':       { url: IMG('1HbJysHMeVJuoPid1ykob9vVIym3ZLqF6'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #1' },
  'ch01-the-white-rabbit-appears':  { url: IMG('1DjF69qfmVBFz0s8SbBQ3bsEpWQvwJww4'), artist: 'Arthur Rackham, 1907', desc: 'White Rabbit' },
  'ch01-falling-down':             { url: IMG('1EUcRWX8qmtpKAv6ahb3Gj5Dju9-odTbn'), artist: 'Chapter illustration', desc: 'Chapter 1 - Down the Rabbit-Hole' },
  'ch01-the-hall-of-doors':        { url: IMG('1efYI57mJw_lPnGTworQXqsyi94-t5ta4'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #4 - Hall of Doors' },
  'ch01-drink-me':                 { url: IMG('1mVpgRq8pspFHgCWHpDGDD6G7cB3lMd_C'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #5 - Drink Me' },
  'ch01-eat-me':                   { url: IMG('18qQvIFiGNkppSk57EgcdXrh6rqG5hVLp'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #6 - Eat Me' },
  'chapter-01-down-the-rabbit-hole': { url: IMG('1d2Mw4qrzjOR6JL8Dup3Va9TBS08d-4di'), artist: 'Arthur Rackham, 1907', desc: 'Alice portrait' },

  // Chapter 2: Pool of Tears
  'ch02-curiouser-and-curiouser':   { url: IMG('1xWwFnZFOFN5t0gaAre_tJ4uSRIgstYsU'), artist: 'Bessie Pease Gutmann, 1933', desc: 'Hope I shan\'t grow more' },
  'ch02-the-white-rabbit-returns':  { url: IMG('1quxdD-bwPfuNUIlFLbKZ4nxFjXbUIrSV'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #7 - White Rabbit returns' },
  'ch02-the-pool-of-tears':        { url: IMG('1Fan7-lXui1m7Z9onJq2Shel_e89061ny'), artist: 'Arthur Rackham, 1907', desc: 'Pool of tears' },
  'ch02-meeting-the-mouse':        { url: IMG('1Hzl_7jA8nOo-uRn98na4VraIh09bd-Gv'), artist: 'Chapter illustration', desc: 'Chapter 2 - Pool of Tears' },
  'chapter-02-the-pool-of-tears':   { url: IMG('1Fan7-lXui1m7Z9onJq2Shel_e89061ny'), artist: 'Arthur Rackham, 1907', desc: 'Pool of tears' },

  // Chapter 3: Caucus-Race
  'ch03-the-driest-thing':          { url: IMG('1iCHo_J6YFhU6MoFjbedcO-SfvoaUC33J'), artist: 'Chapter illustration', desc: 'Chapter 3 - Caucus-Race' },
  'ch03-the-caucus-race':           { url: IMG('1gzgt8Ers4hN15kmvjiGAj2iDpb53BUsV'), artist: 'Arthur Rackham, 1907', desc: 'Who has won the race' },
  'ch03-a-long-sad-tale':           { url: IMG('1rouNf6wuEkebQGRn3wfxhq8AJBYk0fWk'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #10 - A long tale' },
  'chapter-03-a-caucus-race-and-a-long-tale': { url: IMG('1gzgt8Ers4hN15kmvjiGAj2iDpb53BUsV'), artist: 'Arthur Rackham, 1907', desc: 'Who has won' },

  // Chapter 4: Rabbit Sends in a Little Bill
  'ch04-mistaken-for-mary-ann':     { url: IMG('17Sald-2G_QuvOzfHpeNVDEP0zNB74lKA'), artist: 'Chapter illustration', desc: 'Chapter 4 - The Rabbit Sends in a Little Bill' },
  'ch04-stuck-in-the-house':        { url: IMG('1FGGzGt6sSSvqqVCUpR5FShFKhDhwnFDb'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #8 - Stuck in the house' },
  'ch04-bill-the-lizard':           { url: IMG('1tOj_GfAYEWIFQXJImZIz7J-GSYtH5rIp'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #9 - Bill the Lizard' },
  'ch04-the-great-puppy':           { url: IMG('1PMOVdYDHfuIiGHVVsLhKvHnyjsmUKdcn'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #12 - The great puppy' },
  'chapter-04-the-rabbit-sends-in-a-little-bill': { url: IMG('1tOj_GfAYEWIFQXJImZIz7J-GSYtH5rIp'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Bill the Lizard' },

  // Chapter 5: Advice from a Caterpillar
  'ch05-who-are-you':               { url: IMG('1VnffYIn0Kpj1_gRVc5ngHfzLjjL9R0eh'), artist: 'Arthur Rackham, 1907', desc: 'Advice from a Caterpillar' },
  'ch05-father-william':            { url: IMG('1_IOLMFVxQodFyKU4bHLeyM3ViI_nh-lZ'), artist: 'Bessie Pease Gutmann, 1933', desc: 'Caterpillar' },
  'ch05-the-mushrooms-magic':       { url: IMG('1aksQD_loEJKGtYT0vomRebN7MheYMkZi'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #13 - Mushroom magic' },
  'ch05-serpent':                    { url: IMG('1TDYv4rptASsohX49mpQKI5tRxKtEBKnm'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #14 - Serpent' },
  'chapter-05-advice-from-a-caterpillar': { url: IMG('1VnffYIn0Kpj1_gRVc5ngHfzLjjL9R0eh'), artist: 'Arthur Rackham, 1907', desc: 'Caterpillar on mushroom' },

  // Chapter 6: Pig and Pepper
  'ch06-the-fish-footman':          { url: IMG('1EovMSufLg-H-uSUhTv6V95MAJDjtyaML'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #15 - Fish footman' },
  'ch06-the-duchesss-kitchen':      { url: IMG('1OZXQmPHJ8-BO944fwGuaTEm1RtaYe5Qj'), artist: 'Arthur Rackham, 1907', desc: 'Saucepan flew close to his nose' },
  'ch06-the-baby-turns-into-a-pig': { url: IMG('1KKR-xQtCzzzNI8XhS_7WwNjkvcGf-k9Y'), artist: 'Arthur Rackham, 1907', desc: 'Pig baby' },
  'ch06-the-cheshire-cat':          { url: IMG('11CX9xtpCESvZV3H-7AvToQaohnEWwRlg'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #16 - Cheshire Cat' },
  'chapter-06-pig-and-pepper':       { url: IMG('1KKR-xQtCzzzNI8XhS_7WwNjkvcGf-k9Y'), artist: 'Arthur Rackham, 1907', desc: 'Pig baby' },

  // Chapter 7: A Mad Tea-Party
  'ch07-no-room':                    { url: IMG('1JV1jv7pen2HCdu1jhdLgUi8ULxASx8Yi'), artist: 'Arthur Rackham, 1907', desc: 'Mad Hatter\'s tea party' },
  'ch07-the-hatters-watch':          { url: IMG('1TLTm8Ux9bjf-0hgpm61aZ8T9tv_Nj4N7'), artist: 'Sir John Tenniel, 1865', desc: 'Mad Hatter\'s Tea Party' },
  'ch07-time-is-frozen':             { url: IMG('1J3RUA9U4p24pog6HC7gO-NcFlsbjwSdS'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #17 - Tea party' },
  'ch07-the-dormouses-story':        { url: IMG('1S4m2_zcHXWdxFHDvMs-JlibhNQTq06-d'), artist: 'Bessie Pease Gutmann, 1933', desc: 'Don\'t see how he\'ll finish' },
  'ch07-alice-leaves-the-tea-party': { url: IMG('1J25rcwcMihJyE2hkqPAKFhsb44RVLAlS'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #18 - Leaving the tea party' },
  'chapter-07-a-mad-tea-party':      { url: IMG('1JV1jv7pen2HCdu1jhdLgUi8ULxASx8Yi'), artist: 'Arthur Rackham, 1907', desc: 'Mad Hatter\'s tea party' },

  // Chapter 8: Queen's Croquet-Ground
  'ch08-painting-the-roses-red':     { url: IMG('1DjuOwQR9zogmdgYUpcfuSinqYtk2FVeX'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #19 - Painting roses red' },
  'ch08-the-royal-procession':       { url: IMG('1YJmbCYeSOqjjZrERTq6dmS9frEOQGE7H'), artist: 'Arthur Rackham, 1907', desc: 'Queen of Hearts' },
  'ch08-croquet-with-flamingos':     { url: IMG('1joz7MmkAQ8Fe3rcPqpbnY1f4OpzF5Euy'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #20 - Croquet with flamingos' },
  'ch08-the-cheshire-cats-head':     { url: IMG('1kVMO42Bpfsu_deoePbAh9mdS_87Jz7IZ'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #24 - Cheshire Cat head' },
  'chapter-08-the-queens-croquet-ground': { url: IMG('1YJmbCYeSOqjjZrERTq6dmS9frEOQGE7H'), artist: 'Arthur Rackham, 1907', desc: 'Queen of Hearts' },

  // Chapter 9: Mock Turtle's Story
  'ch09-the-duchess-and-her-morals': { url: IMG('1GnibabGom4BfwgAAkFce7URWrALGSUzU'), artist: 'Bessie Pease Gutmann, 1933', desc: 'Beg your acceptance' },
  'ch09-meeting-the-gryphon':       { url: IMG('18rehpiJYvoOlPZ-X9igZIXqlaSJdXw_F'), artist: 'Bessie Pease Gutmann, 1933', desc: 'Gryphon' },
  'ch09-the-mock-turtles-school':   { url: IMG('14z4lpLEHvJtRUOFRRnXmA1Uy55d9W8WD'), artist: 'Arthur Rackham, 1907', desc: 'Gryphon & Mock Turtle' },
  'chapter-09-the-mock-turtles-story': { url: IMG('14z4lpLEHvJtRUOFRRnXmA1Uy55d9W8WD'), artist: 'Arthur Rackham, 1907', desc: 'Gryphon & Mock Turtle' },

  // Chapter 10: Lobster Quadrille
  'ch10-the-lobster-quadrille':     { url: IMG('1fpQOphCVGX9QG2RmnBgWM1MGzPAgPNYz'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #24b - Lobster Quadrille' },
  'ch10-the-lobster-and-the-owl':   { url: IMG('1T9fZRj503BjF_Q9aNXrK84o_yH9a4ajC'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #25 - Voice of the Lobster' },
  'ch10-beautiful-soup':            { url: IMG('1GIHmyQ-NmZG3O-7IT0jYUA3MLYLIUCiT'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #26 - Beautiful Soup' },
  'chapter-10-the-lobster-quadrille': { url: IMG('1fpQOphCVGX9QG2RmnBgWM1MGzPAgPNYz'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Lobster Quadrille' },

  // Chapter 11: Who Stole the Tarts?
  'ch11-the-court-assembles':       { url: IMG('1UDxSeCTUTzl2xwfhZpagRuFeRbyU9HOi'), artist: 'Arthur Rackham, 1907', desc: 'Trial of the Knave of Hearts' },
  'ch11-the-hatters-evidence':      { url: IMG('18wGoF800uk8T_xZ60EXaMlYqlk5cU3kq'), artist: 'Arthur Rackham, 1907', desc: 'Knave of Spades' },
  'ch11-the-cooks-evidence':        { url: IMG('1jL39fdeRIQ50SNDaB56CRLNv-ZyXCRHk'), artist: 'Bessie Pease Gutmann, 1933', desc: 'Shan\'t be beheaded' },
  'chapter-11-who-stole-the-tarts': { url: IMG('1UDxSeCTUTzl2xwfhZpagRuFeRbyU9HOi'), artist: 'Arthur Rackham, 1907', desc: 'Trial of the Knave of Hearts' },

  // Chapter 12: Alice's Evidence
  'ch12-alice-tips-the-jury':       { url: IMG('1MTle8gV8St4NiL9a7viUe-41nyeJW20K'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #31 - Tipping the jury' },
  'ch12-the-mysterious-letter':     { url: IMG('1vvfcBp3RYczY5NZJVqJ2euFIdOtNasVx'), artist: 'Lewis Carroll (manuscript, 1864)', desc: 'Alice Under Ground #32 - The letter' },
  'ch12-sentence-first':            { url: IMG('1vwKtbajQP49qAsrKUQ2o6S8eO--PBQCb'), artist: 'Arthur Rackham, 1907', desc: 'Pack rose in the air' },
  'ch12-waking-up':                 { url: IMG('1AmB2NFrFMkw8OBhSqh40meUrHvU7juLh'), artist: 'Charles F.A. Voysey, c.1930', desc: 'Alice in Wonderland textile design' },
  'chapter-12-alices-evidence':      { url: IMG('1vwKtbajQP49qAsrKUQ2o6S8eO--PBQCb'), artist: 'Arthur Rackham, 1907', desc: 'Pack rose in the air' },
};

// Apply images
let mapped = 0;
let unmapped = [];
g.items.forEach(item => {
  const img = imageMap[item.id];
  if (img) {
    item.image_url = img.url;
    if (!item.metadata) item.metadata = {};
    item.metadata.illustration_artist = img.artist;
    item.metadata.illustration_description = img.desc;
    mapped++;
  } else {
    unmapped.push(item.id);
  }
});

// Update description
g.description = "Lewis Carroll's beloved classic broken into scenes for multi-level reading. Level 2 chapters are emergent summaries (perfect for the littlest readers). Level 1 scenes contain the COMPLETE ORIGINAL TEXT alongside age-adapted retellings. Illustrated with public domain artwork from 5 artists: Lewis Carroll's own manuscript drawings (1864), Arthur Rackham (1907), Bessie Pease Gutmann (1933), Sir John Tenniel (1865), and Charles F.A. Voysey textile design (c.1930).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES:\n- Lewis Carroll original manuscript drawings (1864, British Library) - 42 pen-and-ink illustrations drawn by Carroll himself for Alice Liddell\n- Arthur Rackham (1907, William Heinemann) - 13 color plates, art nouveau style\n- Bessie Pease Gutmann (1933, Dodge Publishing) - 6 soft pastel illustrations\n- Sir John Tenniel (1865, Macmillan) - the iconic original illustrations\n- Charles F.A. Voysey (c.1930) - Arts & Crafts textile design featuring Alice characters";

// Update attribution
g.attribution.note = "Complete original text from Project Gutenberg eBook #11. Illustrated with public domain images from multiple editions: Lewis Carroll's manuscript drawings (1864, British Library), Arthur Rackham (1907), Bessie Pease Gutmann (1933), Sir John Tenniel (1865), Charles F.A. Voysey textile design (c.1930). All illustrations are public domain. Images from Julia's curated collection on Google Drive.";

g.cover_image_url = 'https://drive.google.com/uc?export=view&id=1d2Mw4qrzjOR6JL8Dup3Va9TBS08d-4di';

console.log('Mapped:', mapped, 'of', g.items.length);
if (unmapped.length) console.log('Unmapped:', unmapped);

fs.writeFileSync(grammarPath, JSON.stringify(g, null, 2));
console.log('Saved to', grammarPath);
