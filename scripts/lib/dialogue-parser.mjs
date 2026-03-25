/**
 * Dialogue Parser for Carroll's Alice in Wonderland
 *
 * Parses the original text into segments for multi-voice TTS generation.
 * Each segment is tagged with a voice role (narrator, alice, male, female, quirky)
 * and character attribution for voice switching.
 *
 * Design: Reusable for any classic literature with quoted dialogue.
 *
 * Usage:
 *   import { parseChapterDialogue, CHARACTER_VOICES } from './dialogue-parser.mjs';
 *   const { cleanText, segments, stats } = parseChapterDialogue(rawText);
 */

// ── Voice Role Mapping ─────────────────────────────────────────────────
// Maps character names (lowercase) to voice roles for TTS.
// 5 voices: narrator, alice, male, female, quirky

export const CHARACTER_VOICES = {
  // Protagonist
  'alice':            'alice',

  // Male characters → one male voice (varied via ElevenLabs settings)
  'white rabbit':     'male',
  'rabbit':           'male',
  'hatter':           'male',
  'mad hatter':       'male',
  'march hare':       'male',
  'king':             'male',
  'gryphon':          'male',
  'mouse':            'male',
  'dodo':             'male',
  'bill':             'male',
  'bill the lizard':  'male',
  'pat':              'male',
  'frog-footman':     'male',
  'fish-footman':     'male',
  'knave':            'male',
  'father william':   'male',
  'young man':        'male',
  'five':             'male',
  'seven':            'male',
  'two':              'male',

  // Female characters
  'queen':            'female',
  'duchess':          'female',
  'cook':             'female',
  'pigeon':           'female',
  'lory':             'female',
  'eaglet':           'female',
  'rose':             'female',

  // Quirky/distinctive characters
  'cheshire cat':     'quirky',
  'cat':              'quirky',
  'caterpillar':      'quirky',
  'mock turtle':      'quirky',
  'dormouse':         'quirky',
};

// ── Attribution Verbs ──────────────────────────────────────────────────
const SPEECH_VERBS = new Set([
  'said', 'says', 'thought', 'cried', 'asked', 'replied', 'exclaimed',
  'remarked', 'whispered', 'shouted', 'continued', 'added', 'muttered',
  'began', 'answered', 'observed', 'repeated', 'returned', 'suggested',
  'grumbled', 'growled', 'sighed', 'sobbed', 'shrieked', 'screamed',
  'panted', 'interrupted', 'went', 'called', 'sang', 'recited', 'read',
  'roared', 'declared', 'demanded', 'inquired', 'protested', 'pleaded',
  'moaned', 'groaned', 'snapped', 'retorted', 'echoed', 'murmured',
]);

// Characters as they appear in attribution (with "the" prefix patterns)
const CHARACTER_PATTERNS = [
  // Multi-word characters first (greedy match)
  { pattern: /\b(?:the\s+)?white\s+rabbit\b/i, name: 'White Rabbit' },
  { pattern: /\b(?:the\s+)?march\s+hare\b/i, name: 'March Hare' },
  { pattern: /\b(?:the\s+)?mock\s+turtle\b/i, name: 'Mock Turtle' },
  { pattern: /\b(?:the\s+)?cheshire[\s-]+cat\b/i, name: 'Cheshire Cat' },
  { pattern: /\b(?:the\s+)?mad\s+hatter\b/i, name: 'Mad Hatter' },
  { pattern: /\bbill\s+the\s+lizard\b/i, name: 'Bill' },
  { pattern: /\bfather\s+william\b/i, name: 'Father William' },
  { pattern: /\bfrog[\s-]+footman\b/i, name: 'Frog-Footman' },
  { pattern: /\bfish[\s-]+footman\b/i, name: 'Fish-Footman' },
  // Single-word characters
  { pattern: /\balice\b/i, name: 'Alice' },
  { pattern: /\b(?:the\s+)?hatter\b/i, name: 'Hatter' },
  { pattern: /\b(?:the\s+)?caterpillar\b/i, name: 'Caterpillar' },
  { pattern: /\b(?:the\s+)?dormouse\b/i, name: 'Dormouse' },
  { pattern: /\b(?:the\s+)?queen\b/i, name: 'Queen' },
  { pattern: /\b(?:the\s+)?king\b/i, name: 'King' },
  { pattern: /\b(?:the\s+)?duchess\b/i, name: 'Duchess' },
  { pattern: /\b(?:the\s+)?gryphon\b/i, name: 'Gryphon' },
  { pattern: /\b(?:the\s+)?pigeon\b/i, name: 'Pigeon' },
  { pattern: /\b(?:the\s+)?mouse\b/i, name: 'Mouse' },
  { pattern: /\b(?:the\s+)?dodo\b/i, name: 'Dodo' },
  { pattern: /\b(?:the\s+)?lory\b/i, name: 'Lory' },
  { pattern: /\b(?:the\s+)?cook\b/i, name: 'Cook' },
  { pattern: /\b(?:the\s+)?knave\b/i, name: 'Knave' },
  { pattern: /\bpat\b/i, name: 'Pat' },
  { pattern: /\bbill\b/i, name: 'Bill' },
];

// Pronoun → gender mapping for fallback
const PRONOUN_GENDER = {
  'she': 'female',
  'her': 'female',
  'he': 'male',
  'his': 'male',
  'it': 'neutral',
  'they': 'neutral',
};

// ── Text Normalization ─────────────────────────────────────────────────

/**
 * Clean raw grammar text for TTS:
 * - Unwrap hard line breaks (preserve paragraph breaks)
 * - Strip _emphasis_ markers (italics don't affect speech)
 * - Normalize whitespace
 * - Normalize quote characters to standard ASCII
 */
export function normalizeForTTS(raw) {
  let text = raw;

  // Normalize curly quotes to straight quotes for consistent parsing
  text = text.replace(/[\u201c\u201e\u201f]/g, '"');  // opening "
  text = text.replace(/[\u201d]/g, '"');                // closing "
  text = text.replace(/[\u2018\u201b]/g, "'");          // opening '
  text = text.replace(/[\u2019]/g, "'");                // closing '

  // Preserve paragraph breaks, unwrap hard line breaks
  text = text.replace(/\r\n/g, '\n');
  // Mark paragraph breaks
  text = text.replace(/\n\n+/g, '\u00B6\u00B6');  // pilcrow placeholder
  // Join remaining line breaks (hard wraps)
  text = text.replace(/\n/g, ' ');
  // Restore paragraph breaks
  text = text.replace(/\u00B6\u00B6/g, '\n\n');

  // Strip emphasis markers: _word_ → word
  text = text.replace(/_([^_]+)_/g, '$1');
  text = text.replace(/\*([^*]+)\*/g, '$1');

  // Normalize whitespace (but keep paragraph breaks)
  text = text.replace(/[ \t]+/g, ' ');
  text = text.replace(/\n +/g, '\n');

  return text.trim();
}

// ── Quote Finding ──────────────────────────────────────────────────────

/**
 * Find all quoted dialogue spans in the text.
 * Handles:
 *   - Standard: "Hello," said Alice.
 *   - Mid-speech attribution: "Start," said Alice, "continuation."
 *   - Nested single quotes: "I said 'hello' to them."
 *   - Parenthetical within quotes: (he thought)
 *
 * Returns array of { start, end } indices (inclusive of quotes).
 */
function findDialogueSpans(text) {
  const spans = [];
  let i = 0;

  while (i < text.length) {
    if (text[i] === '"') {
      const start = i;
      let j = i + 1;
      let depth = 1;

      // Find matching closing quote
      while (j < text.length && depth > 0) {
        if (text[j] === '"' && depth === 1) {
          // Check if this is a real close or a nested open
          // Real close: preceded by letter/punctuation, followed by space/punct/verb
          depth = 0;
        } else if (text[j] === '"' && j > start + 1) {
          // Another opening quote — could be continuation after attribution
          // Check if there's attribution between previous close and this open
          depth = 0;
          j--; // Back up to let the outer loop handle this
          break;
        }
        j++;
      }

      if (j <= text.length) {
        spans.push({ start, end: j - 1 }); // end is index of closing quote
      }
      i = j;
    } else {
      i++;
    }
  }

  return spans;
}

/**
 * Improved dialogue span finder using a state machine.
 * More robust than regex for nested quotes and multi-turn dialogue.
 */
function findDialogueSpansRobust(text) {
  const spans = [];
  let i = 0;

  while (i < text.length) {
    // Look for opening double quote
    if (text[i] === '"') {
      const start = i;
      let j = i + 1;
      let foundClose = false;

      while (j < text.length) {
        if (text[j] === '"') {
          // Check: is this a closing quote or an opening quote for next dialogue?
          // Closing quote is followed by: space+verb, comma, period, !, ?, end
          // Opening quote is preceded by: space (new dialogue)

          const afterQuote = text.slice(j + 1, j + 3);
          const beforeQuote = j > 0 ? text[j - 1] : '';

          // If preceded by space or newline, this might be an opening quote
          // for new dialogue. But first check if it closes the current one.
          if (/[a-zA-Z,!?.\-;:\)]/.test(beforeQuote) || beforeQuote === ' ') {
            // Likely a closing quote
            spans.push({ start, end: j });
            i = j + 1;
            foundClose = true;
            break;
          }
        }
        j++;
      }

      if (!foundClose) {
        // Unclosed quote — include to end of paragraph
        const paraEnd = text.indexOf('\n\n', start);
        const end = paraEnd !== -1 ? paraEnd : text.length;
        spans.push({ start, end: end - 1 });
        i = end;
      }
    } else {
      i++;
    }
  }

  return spans;
}

// ── Character Detection ────────────────────────────────────────────────

/**
 * Detect which character is speaking based on attribution near the quote.
 * Searches both after the closing quote (most common) and before the opening quote.
 *
 * Patterns:
 *   - "quote," said Alice.              → after, verb-first
 *   - "quote," Alice said.              → after, character-first
 *   - Alice said, "quote"               → before, character-first
 *   - "quote," she said.                → pronoun, resolved via lastSpeakers
 *
 * @param {string} text - Full chapter text
 * @param {number} quoteStart - Index of opening quote
 * @param {number} quoteEnd - Index of closing quote
 * @param {Object} lastSpeakers - { female, male, neutral } tracking for pronoun resolution
 * @returns {{ character: string|null, role: string }}
 */
function detectSpeaker(text, quoteStart, quoteEnd, lastSpeakers) {
  // Search window: up to 150 chars after the quote, 100 chars before
  const afterText = text.slice(quoteEnd + 1, quoteEnd + 151);
  const beforeText = text.slice(Math.max(0, quoteStart - 100), quoteStart);

  // ── Try after-quote attribution first (most common pattern) ──
  // Pattern 1: "quote," [verb] [character]
  // Pattern 2: "quote," [character] [verb]

  // Extract the attribution clause (up to next quote, period, or paragraph break)
  const attrMatch = afterText.match(/^[,;:]?\s*(.+?)(?=["\n\n]|$)/s);
  const attrClause = attrMatch ? attrMatch[1] : '';

  if (attrClause) {
    // Check for character names in the attribution
    for (const { pattern, name } of CHARACTER_PATTERNS) {
      if (pattern.test(attrClause)) {
        // Verify there's a speech verb nearby (to confirm it's attribution)
        const words = attrClause.toLowerCase().split(/\s+/);
        const hasVerb = words.some(w => SPEECH_VERBS.has(w));
        if (hasVerb || attrClause.length < 30) {
          updateLastSpeakers(lastSpeakers, name);
          return { character: name, role: getRole(name) };
        }
      }
    }

    // Check for pronoun attribution: "she said", "he replied"
    const pronounMatch = attrClause.match(/\b(she|he|it|they)\s+(\w+)/i);
    if (pronounMatch) {
      const pronoun = pronounMatch[1].toLowerCase();
      const verb = pronounMatch[2].toLowerCase();
      if (SPEECH_VERBS.has(verb)) {
        const gender = PRONOUN_GENDER[pronoun] || 'neutral';
        const resolvedChar = lastSpeakers[gender];
        if (resolvedChar) {
          return { character: resolvedChar, role: getRole(resolvedChar) };
        }
        // Can't resolve pronoun — use gender-based default
        if (gender === 'female') return { character: 'Alice', role: 'alice' };
        return { character: null, role: gender === 'male' ? 'male' : 'narrator' };
      }
    }

    // Verb-first pattern: "said she", "thought she"
    const verbFirstPronoun = attrClause.match(/\b(\w+)\s+(she|he|it|they)\b/i);
    if (verbFirstPronoun && SPEECH_VERBS.has(verbFirstPronoun[1].toLowerCase())) {
      const pronoun = verbFirstPronoun[2].toLowerCase();
      const gender = PRONOUN_GENDER[pronoun] || 'neutral';
      const resolvedChar = lastSpeakers[gender];
      if (resolvedChar) {
        return { character: resolvedChar, role: getRole(resolvedChar) };
      }
    }
  }

  // ── Try before-quote attribution ──
  // Pattern: Alice said, "quote" or Alice thought, "quote"
  const beforeWords = beforeText.trim().split(/\s+/).slice(-5);
  for (const { pattern, name } of CHARACTER_PATTERNS) {
    const beforeSnippet = beforeWords.join(' ');
    if (pattern.test(beforeSnippet)) {
      const hasVerb = beforeWords.some(w => SPEECH_VERBS.has(w.toLowerCase().replace(/[,.:]/g, '')));
      if (hasVerb) {
        updateLastSpeakers(lastSpeakers, name);
        return { character: name, role: getRole(name) };
      }
    }
  }

  // ── Fallback: "thought Alice" pattern (common for internal monologue) ──
  const thoughtMatch = afterText.match(/^\s*thought\s+(\w+)/i);
  if (thoughtMatch) {
    const name = thoughtMatch[1];
    if (name.toLowerCase() === 'alice') {
      updateLastSpeakers(lastSpeakers, 'Alice');
      return { character: 'Alice', role: 'alice' };
    }
  }

  // ── No attribution found — return unattributed ──
  return { character: null, role: 'narrator' };
}

function getRole(characterName) {
  if (!characterName) return 'narrator';
  const key = characterName.toLowerCase();
  return CHARACTER_VOICES[key] || 'narrator';
}

// Characters that use "he/it" pronouns (for pronoun resolution)
const MALE_PRONOUN_CHARS = new Set([
  'white rabbit', 'rabbit', 'hatter', 'mad hatter', 'march hare',
  'king', 'gryphon', 'mouse', 'dodo', 'bill', 'pat', 'knave',
  'caterpillar', 'mock turtle', 'dormouse', 'frog-footman', 'fish-footman',
  'father william', 'young man', 'five', 'seven', 'two',
]);

function updateLastSpeakers(lastSpeakers, characterName) {
  if (!characterName) return;
  const key = characterName.toLowerCase();
  // Alice is female
  if (key === 'alice') {
    lastSpeakers.female = characterName;
  } else if (MALE_PRONOUN_CHARS.has(key)) {
    lastSpeakers.male = characterName;
  } else {
    // Female characters or unknown
    const role = CHARACTER_VOICES[key];
    if (role === 'female') {
      lastSpeakers.female = characterName;
    } else {
      lastSpeakers.male = characterName; // default to male for unknown
    }
  }
  lastSpeakers.last = characterName;
}

// ── Main Parser ────────────────────────────────────────────────────────

/**
 * Parse a chapter's raw text into voice-tagged segments.
 *
 * @param {string} rawText - Raw text from grammar JSON (may include \n, _emphasis_, curly quotes)
 * @returns {{ cleanText: string, segments: Array, stats: Object }}
 *
 * Each segment:
 *   { text: string, role: string, character: string|null, charOffset: number, charEnd: number }
 *
 * Roles: 'narrator', 'alice', 'male', 'female', 'quirky'
 */
export function parseChapterDialogue(rawText) {
  const cleanText = normalizeForTTS(rawText);
  const segments = [];
  const lastSpeakers = { female: 'Alice', male: null, neutral: null, last: null };
  const stats = { total_chars: cleanText.length, narration_chars: 0, dialogue_chars: 0, segments: 0, characters: new Set() };

  let pos = 0;

  while (pos < cleanText.length) {
    // Find next opening quote
    const nextQuote = cleanText.indexOf('"', pos);

    if (nextQuote === -1) {
      // Rest is narration
      const remaining = cleanText.slice(pos).trim();
      if (remaining) {
        segments.push({
          text: remaining,
          role: 'narrator',
          character: null,
          charOffset: pos,
          charEnd: cleanText.length,
        });
        stats.narration_chars += remaining.length;
      }
      break;
    }

    // Everything before the quote is narration
    if (nextQuote > pos) {
      const narration = cleanText.slice(pos, nextQuote);
      if (narration.trim()) {
        segments.push({
          text: narration,
          role: 'narrator',
          character: null,
          charOffset: pos,
          charEnd: nextQuote,
        });
        stats.narration_chars += narration.length;
      }
    }

    // Find matching closing quote
    let closeQuote = -1;
    let j = nextQuote + 1;
    while (j < cleanText.length) {
      if (cleanText[j] === '"') {
        closeQuote = j;
        break;
      }
      j++;
    }

    if (closeQuote === -1) {
      // Unclosed quote — treat rest of text as dialogue
      const dialogue = cleanText.slice(nextQuote);
      segments.push({
        text: dialogue,
        role: 'alice', // Default to Alice for unclosed quotes
        character: 'Alice',
        charOffset: nextQuote,
        charEnd: cleanText.length,
      });
      stats.dialogue_chars += dialogue.length;
      break;
    }

    // Extract the dialogue (including quotes for natural TTS)
    const dialogueText = cleanText.slice(nextQuote, closeQuote + 1);

    // Detect the speaker
    const { character, role } = detectSpeaker(cleanText, nextQuote, closeQuote, lastSpeakers);

    // If no character detected, try alternating with last speaker in conversation
    // (common in rapid back-and-forth dialogue)
    let finalRole = role;
    let finalChar = character;
    if (!character && role === 'narrator') {
      // Unattributed dialogue — check context for conversational alternation
      // Default: if we know who spoke last, alternate
      if (lastSpeakers.last) {
        // Try to use the "other" speaker in the conversation
        finalRole = lastSpeakers.last.toLowerCase() === 'alice' ?
          (lastSpeakers.male ? getRole(lastSpeakers.male) : (lastSpeakers.neutral ? getRole(lastSpeakers.neutral) : 'alice')) :
          'alice';
        finalChar = finalRole === 'alice' ? 'Alice' :
          (lastSpeakers.male && getRole(lastSpeakers.male) === finalRole ? lastSpeakers.male : lastSpeakers.last);
      } else {
        finalRole = 'alice';
        finalChar = 'Alice';
      }
    }

    segments.push({
      text: dialogueText,
      role: finalRole,
      character: finalChar,
      charOffset: nextQuote,
      charEnd: closeQuote + 1,
    });
    if (finalChar) {
      updateLastSpeakers(lastSpeakers, finalChar);
    }
    stats.dialogue_chars += dialogueText.length;
    if (character) stats.characters.add(character);

    pos = closeQuote + 1;
  }

  stats.segments = segments.length;
  stats.characters = [...stats.characters];

  return { cleanText, segments, stats };
}

/**
 * Merge adjacent segments with the same role to reduce TTS API calls.
 * Narration between two dialogue segments of the same character gets merged.
 */
export function mergeAdjacentSegments(segments) {
  if (segments.length <= 1) return segments;

  const merged = [segments[0]];
  for (let i = 1; i < segments.length; i++) {
    const prev = merged[merged.length - 1];
    const curr = segments[i];

    if (prev.role === curr.role) {
      // Merge: combine text, extend range
      prev.text += curr.text;
      prev.charEnd = curr.charEnd;
    } else {
      merged.push({ ...curr });
    }
  }

  return merged;
}

/**
 * Estimate total character count for TTS billing.
 * Only counts the text that will be sent to TTS (dialogue text without quotes for
 * character voices, full narration for narrator).
 */
export function estimateTTSCharacters(segments) {
  let total = 0;
  for (const seg of segments) {
    // Strip quotes from dialogue (they won't be spoken)
    let text = seg.text;
    if (seg.role !== 'narrator') {
      text = text.replace(/^"/, '').replace(/"$/, '');
    }
    total += text.length;
  }
  return total;
}

// ── CLI Test Mode ──────────────────────────────────────────────────────

if (process.argv[1] && process.argv[1].includes('dialogue-parser')) {
  // Test with a sample or with the grammar
  import('fs').then(fs => {
    import('path').then(path => {
      const __dirname2 = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Z]:)/, '$1'));
      const grammarPath = path.resolve(__dirname2, '../../grammars/alice-in-wonderland-chapter-book/grammar.json');

      try {
        const grammar = JSON.parse(fs.readFileSync(grammarPath, 'utf8'));
        const l1Items = grammar.items.filter(it => it.level === 1);

        // Group by chapter
        const chapters = {};
        for (const item of l1Items) {
          const ch = item.metadata.chapter_number;
          if (!chapters[ch]) chapters[ch] = [];
          chapters[ch].push(item);
        }

        // Parse each chapter
        let grandTotalChars = 0;
        for (const [chNum, scenes] of Object.entries(chapters).sort((a, b) => a[0] - b[0])) {
          scenes.sort((a, b) => a.metadata.scene_number - b.metadata.scene_number);
          const fullText = scenes.map(s => s.sections['Story (Original Text)'] || '').join('\n\n');
          const { cleanText, segments, stats } = parseChapterDialogue(fullText);
          const merged = mergeAdjacentSegments(segments);
          const ttsChars = estimateTTSCharacters(merged);
          grandTotalChars += ttsChars;

          console.log(`\n── Chapter ${chNum} ──`);
          console.log(`  Clean text: ${cleanText.length} chars`);
          console.log(`  Segments: ${stats.segments} raw → ${merged.length} merged`);
          console.log(`  Characters: ${stats.characters.join(', ') || '(none detected)'}`);
          console.log(`  Narration: ${stats.narration_chars} chars | Dialogue: ${stats.dialogue_chars} chars`);
          console.log(`  TTS billable: ${ttsChars} chars`);

          // Show first 5 merged segments as samples
          if (process.argv.includes('--verbose')) {
            console.log(`  Sample segments:`);
            for (const seg of merged.slice(0, 8)) {
              const preview = seg.text.slice(0, 80).replace(/\n/g, '\\n');
              console.log(`    [${seg.role}${seg.character ? '/' + seg.character : ''}] ${preview}...`);
            }
          }
        }

        console.log(`\n══ TOTAL TTS CHARACTERS: ${grandTotalChars.toLocaleString()} ══`);
        console.log(`Estimated cost (multilingual v2): $${(grandTotalChars / 1000 * 0.30).toFixed(2)}`);
        console.log(`Estimated cost (flash v2.5, 0.5x): $${(grandTotalChars / 1000 * 0.15).toFixed(2)}`);
      } catch (err) {
        console.error('Error:', err.message);
        console.error('Run from the recursive.eco-schemas root directory');
      }
    });
  });
}
