#!/usr/bin/env python3
"""
Add 6 new L1 myths, 4 new L2 interpreters, 1 new culture card to Myths Through Many Eyes.
Also updates thread composite_of arrays and meta-collective-unconscious.
"""
import json

with open("grammars/myths-through-many-eyes/grammar.json") as f:
    g = json.load(f)

items = g["items"]

# ── 6 NEW L1 MYTHS ──────────────────────────────────────────────────────────
# Insert after myth-raven-steals-light (currently sort_order 25)

new_myths = [
    {
        "id": "myth-vasalisa-baba-yaga",
        "name": "Vasalisa and Baba Yaga",
        "sort_order": 0,  # will be recalculated
        "category": "myths",
        "level": 1,
        "sections": {
            "The Story": "After her mother dies, young Vasalisa is sent by her cruel stepsisters to fetch fire from Baba Yaga — the terrifying old woman who lives in a hut on chicken legs, surrounded by a fence of human bones topped with glowing skulls. Vasalisa's only protection is a small doll her mother gave her on her deathbed, whispering: 'Feed it when you are in need, and it will help you.' In the forest, Vasalisa sees three horsemen ride past — White (dawn), Red (sun), Black (night) — Baba Yaga's servants. At the hut, the old woman sets impossible tasks: sort poppy seeds from dirt, separate good grain from mildewed, cook and clean the entire house. Each night, when Vasalisa despairs, she feeds the doll, and the doll does the work. Baba Yaga is furious but cannot find fault. She asks: 'How do you do it?' Vasalisa answers: 'By my mother's blessing.' Baba Yaga shrieks — 'I want no blessed ones here!' — and throws her out, but gives her what she came for: a skull lantern with burning eyes. Vasalisa carries it home. The skull's gaze falls on the stepmother and stepsisters and burns them to ash.",
            "Source": "Russian fairy tale, collected by Alexander Afanasyev (Narodnye russkie skazki, 1855-1867). Variants across Slavic tradition. Estés's retelling in Women Who Run With the Wolves (1992) is the most influential modern interpretation.",
            "The Images": "The doll — the mother's gift, the intuition that works in the dark when the conscious mind fails. Baba Yaga — not good, not evil, but the wild feminine power that tests you. The hut on chicken legs — the house that moves, the wisdom that won't stand still for you. The three horsemen — the natural cycles that Baba Yaga commands. The impossible tasks — initiation through doing what cannot be done. The skull lantern — the fire that sees through pretense and burns what is false.",
            "Culture": "Russian/Slavic. Baba Yaga is one of the great ambiguous figures of world mythology — she eats children and she gives fire. She is the Terrible Mother and the Wise Woman in one body. The story is an initiation tale: to gain the fire (consciousness, autonomy, the ability to see), you must go to the terrifying feminine, submit to her tasks, and survive. Estés reads it as the recovery of women's wild instinct; folklorists read it as a puberty rite; Jungians read it as an encounter with the devouring/nourishing Great Mother."
        },
        "keywords": ["vasalisa", "baba-yaga", "doll", "initiation", "feminine", "fire", "russian"],
        "metadata": {"origin": "Russian/Slavic"}
    },
    {
        "id": "myth-skeleton-woman",
        "name": "Skeleton Woman",
        "sort_order": 0,
        "category": "myths",
        "level": 1,
        "sections": {
            "The Story": "A woman who had done something her father disapproved of was thrown off the cliffs into the sea. Fish ate her flesh. She lay on the ocean floor, her skeleton tangled in kelp, her empty eyes staring up through dark water. One day a fisherman — a lonely man who had forgotten how to be with people — cast his line into that bay. His hook caught in her ribs. Feeling the tremendous pull, he thought he had caught the greatest fish of his life. He hauled and hauled. When her skull broke the surface, he screamed and paddled for shore, but the line was tangled and she tumbled after him, rattling over the ice. In his igloo, shaking with fear, he lit his oil lamp and saw her — a pile of bones in a heap. Something in him softened. He began to untangle her, bone by bone, putting her back in order. He sang to her. He fell asleep. As he slept, a single tear rolled from his eye. Skeleton Woman crawled to him and drank that tear, which contained all his loneliness and longing. She reached into his sleeping body and took out his heart, drummed on it like a drum, and sang flesh back onto her bones. She became a woman again. She put his heart back. They woke together. They fed each other, and lived together for a long time, nourished by the creatures she called up from the sea.",
            "Source": "Inuit oral tradition. Retold by Clarissa Pinkola Estés in Women Who Run With the Wolves (1992) and by Martin Shaw in various oral performances and writings. Multiple variants across Arctic peoples.",
            "The Images": "The skeleton on the ocean floor — the life/death/life nature that waits beneath consciousness. The fisherman's hook — accidentally snagging what you were not looking for. The flight and the tangle — you cannot run from what the deep sends you. The untangling of bones — the patient work of relationship. The tear — the gift of one's genuine feeling, which feeds the other. The heart as drum — intimacy as resurrection. The flesh returning — love as the force that restores life to what was stripped bare.",
            "Culture": "Inuit/Arctic. This is not a romance — it is a myth about the Life/Death/Life nature that all real relationships require. To love another person, you must be willing to face the Death Woman — the fact that love includes death, loss, barrenness, the skeleton phase. The fisherman's willingness to untangle the bones, to give his tear and his heart, is the willingness to stay with someone through the death phase and trust that flesh will return. Shaw uses this myth to teach about wildness in relationship; Estés uses it to teach about women's deep knowing."
        },
        "keywords": ["skeleton-woman", "death", "love", "bones", "tear", "relationship", "inuit"],
        "metadata": {"origin": "Inuit/Arctic"}
    },
    {
        "id": "myth-anansi",
        "name": "Anansi the Spider",
        "sort_order": 0,
        "category": "myths",
        "level": 1,
        "sections": {
            "The Story": "In the beginning, all stories belonged to Nyame, the Sky God, who kept them locked in a golden chest beside his throne. No one on earth had stories — no tales to tell at night, no wisdom passed at the fire. Anansi the Spider, small and cunning, climbed his web up to the sky and asked Nyame for the stories. Nyame laughed: 'The price is four creatures: Onini the Python, Mmoboro the Hornets, Osebo the Leopard, and Mmoatia the Invisible Fairy.' Everyone knew this was impossible — kings and warriors had tried and failed. But Anansi went home and thought. For the python, he argued loudly with his wife about the python's length, then asked Onini to stretch along a branch to settle the matter — and tied him there. For the hornets, he poured water over them and himself, offered them a dry gourd for shelter, and plugged the hole. For the leopard, he dug a pit and covered it. For the fairy, he carved a wooden doll, covered it with sticky sap, and put yam in its hand. The fairy slapped the doll, got stuck, and couldn't escape. Anansi brought all four to Nyame. The Sky God, astonished, gave him the golden chest. From that day, all stories in the world are called 'spider stories' — Anansesem.",
            "Source": "Akan/Ashanti oral tradition (Ghana/West Africa). Carried to the Caribbean and Americas through the Middle Passage — Anansi stories survive in Jamaica, Suriname, Curaçao, and the Gullah/Geechee communities of the American South. Collected by R.S. Rattray (Akan-Ashanti Folk-Tales, 1930) and many others.",
            "The Images": "Stories locked in a golden chest — knowledge hoarded by power. The impossible price — four captures that require cleverness, not strength. Each capture uses the creature's own nature against it: the python's vanity, the hornets' need for shelter, the leopard's predation, the fairy's curiosity. The sticky doll — the trap baited with what you desire. The spider's web — the structure of connection, story, and cunning. All stories becoming 'spider stories' — the trickster as the origin of narrative itself.",
            "Culture": "Akan/Ashanti (West Africa), pan-African diaspora. Anansi is the consummate trickster — small, physically weak, endlessly clever, morally ambiguous. He is greedy, lazy, deceitful, and brilliant, and through these very qualities he liberates stories for all humanity. The Middle Passage carried Anansi across the Atlantic, where he became a figure of resistance — the enslaved person's model for surviving through wit when strength was impossible. Akomolafe reads Anansi as the crack in the system, the compost-figure who thrives in the margins of power."
        },
        "keywords": ["anansi", "spider", "trickster", "stories", "west-african", "cunning", "liberation"],
        "metadata": {"origin": "West African (Akan/Ashanti)"}
    },
    {
        "id": "myth-scheherazade",
        "name": "Scheherazade and the Thousand and One Nights",
        "sort_order": 0,
        "category": "myths",
        "level": 1,
        "sections": {
            "The Story": "King Shahryar, betrayed by his wife, goes mad with rage. He marries a new virgin each night and has her executed at dawn, so that no woman can ever betray him again. The kingdom runs out of daughters. Scheherazade, the vizier's daughter — brilliant, educated, fearless — volunteers. On her wedding night, she begins to tell the king a story. At dawn, she stops at the most suspenseful moment. The king, desperate to hear the ending, spares her for one more night. The next night she finishes that story but begins another, and stops again at dawn. Night after night, story within story within story — tales of jinns and merchants, of fishermen and kings, of Sinbad's voyages and Ali Baba's cave. For a thousand and one nights she weaves her web of narrative, and in the weaving, something changes. The king is healed. Not by argument or force, but by story. He has been made human again by listening. He spares her. He loves her. The killing stops.",
            "Source": "One Thousand and One Nights (Alf Layla wa-Layla), compiled in Arabic over centuries from Persian, Indian, and Arabic sources. Earliest fragment: 9th century CE. Galland's French translation (1704-1717) brought it to Europe. Burton's unexpurgated English translation (1885) is the most complete. Multiple public domain editions.",
            "The Images": "The murderous king — trauma turned to systemic violence, the wounded masculine that destroys what it cannot control. Scheherazade — story as survival strategy, narrative as medicine. The unfinished tale — the cliffhanger as lifeline, suspense as the thread between death and dawn. Stories within stories — the fractal structure of narrative, each tale containing another. The thousand and one nights — the slow work of healing, night by night. Dawn — the daily threat, the daily reprieve.",
            "Culture": "Persian/Arabic/Indian composite. Scheherazade is the ultimate mythic figure for the power of storytelling — she literally narrates to survive. Warner reads her as the archetypal woman using the only weapon available to her (voice, wit, narrative) against male violence. The frame story is a myth about what stories do: they postpone death, they heal trauma, they humanize the listener. The nested structure anticipates postmodern fiction by a thousand years. Every storyteller who has ever held an audience is channeling Scheherazade."
        },
        "keywords": ["scheherazade", "1001-nights", "storytelling", "survival", "frame-tale", "arabian", "healing"],
        "metadata": {"origin": "Persian/Arabic"}
    },
    {
        "id": "myth-seal-wife",
        "name": "The Seal Wife (Selkie)",
        "sort_order": 0,
        "category": "myths",
        "level": 1,
        "sections": {
            "The Story": "A fisherman walking the shore at night sees seals come onto the beach and shed their skins, becoming beautiful women who dance naked in the moonlight. He steals one skin and hides it. When the women return to the sea, one cannot find her skin. She weeps. He offers her shelter, warmth, a human life. She becomes his wife. She bears him children. She is a good wife, but there is always something in her eyes when she looks at the sea — a distance, a longing, a sorrow that will not name itself. The children love her but sense she is not entirely theirs. Years pass. One day a child finds a strange skin hidden in the rafters and brings it to the mother, not knowing what it is. The moment the seal wife touches her skin, she knows. She kisses each child. She walks to the shore. She puts on the skin and enters the water. She does not come back. Sometimes, on moonlit nights, the children see a seal in the bay, watching them.",
            "Source": "Oral tradition of the Faroe Islands, Iceland, Ireland, Scotland, and Scandinavia. Variants include the swan maiden and the silkie ballads. Collected by Jón Árnason, J.F. Campbell, and others. Shaw's oral retellings are the most powerful modern versions.",
            "The Images": "The shed skin — the wild nature that can be removed but not destroyed. The stolen skin — domestication as theft, the capture of wildness by the human world. The good wife with distant eyes — the price of living in the wrong element. The hidden skin — the essential self locked away, always waiting. The child who finds it — innocence as the agent of liberation. The return to the sea — the moment the wild self reclaims itself, even at the cost of the human bonds.",
            "Culture": "Celtic/Nordic (Scotland, Ireland, Faroe Islands, Iceland). The Selkie myth is about what happens when you try to keep wildness in the house. Shaw reads it as a teaching about ecological belonging — we all have a 'seal skin,' a wild nature shaped by the more-than-human world, and domestication (however comfortable) is a kind of captivity. Estés reads it as the story of every woman (or person) who has forgotten their wild self — who has been 'nice' so long they've forgotten the sea. The myth is heartbreaking because there is no villain: the fisherman loves her, the children need her, and she must leave anyway."
        },
        "keywords": ["selkie", "seal-wife", "wildness", "captivity", "longing", "sea", "celtic"],
        "metadata": {"origin": "Celtic/Nordic"}
    },
    {
        "id": "myth-bluebeard",
        "name": "Bluebeard",
        "sort_order": 0,
        "category": "myths",
        "level": 1,
        "sections": {
            "The Story": "A wealthy lord with a blue-tinged beard — unsettling, magnetic — marries a young woman. He gives her the keys to every room in his magnificent castle, saying she may open any door she pleases. Except one. The small key. The door at the end of the corridor. He leaves on a journey. She explores room after room of treasure, but the forbidden door calls to her. She opens it. Inside: the bodies of his previous wives, hanging from hooks, the floor thick with blood. The key slips from her hand into the blood. She picks it up, but the blood will not wash off — the key is stained permanently. Bluebeard returns, sees the key, and knows. 'Now you will join them,' he says. She begs for time to say her prayers. She sends her sister to the tower to watch for their brothers. Bluebeard sharpens his blade. At the last moment, her brothers arrive and kill him. She inherits the castle and all his wealth. She buries the dead wives with honor.",
            "Source": "Charles Perrault (Histoires ou contes du temps passé, 1697). Variants in Grimm ('Fitcher's Bird,' 'The Robber Bridegroom') and across European folklore. The tale type (ATU 312) is ancient. Warner's and Estés's analyses are the most influential modern readings.",
            "The Images": "The forbidden door — the knowledge women are told not to seek. The bloody chamber — the truth about the predator's history that society conceals. The key that won't wash clean — once you know, you cannot unknow. Bluebeard's charm — the predator who offers wealth, beauty, and freedom while hiding murder. The sister on the tower — women watching for women, the sororal network. The brothers' arrival — the community that enforces justice when the individual cannot escape alone.",
            "Culture": "European (French literary fairy tale with deep folk roots). This is the myth of the predator in the house — the charming, powerful figure whose closet hides dead women. Estés reads it as a teaching about the 'natural predator' in the psyche — the internal voice that says 'don't look, don't know, don't ask.' Warner reads it as social history: the real Bluebeards were serial wife-killers protected by wealth and power, and the tale is women's coded warning to each other. The forbidden door is curiosity — the refusal to stop knowing — and the myth says: open it. The knowing may be terrible, but not-knowing is death."
        },
        "keywords": ["bluebeard", "forbidden", "curiosity", "predator", "fairy-tale", "women", "knowledge"],
        "metadata": {"origin": "European (French)"}
    }
]

# ── 4 NEW L2 INTERPRETERS ────────────────────────────────────────────────────

new_interpreters = [
    {
        "id": "interp-akomolafe",
        "name": "Bayo Akomolafe: Myth as Compost",
        "sort_order": 0,
        "category": "interpreters",
        "level": 2,
        "sections": {
            "Who They Were": "Bayo Akomolafe (b. 1983), Nigerian-born philosopher, professor, author of These Wilds Beyond Our Fences and We Will Tell Our Own Story. Executive Director of The Emergence Network. Trained in clinical psychology, he left conventional academia to think at the edges — where post-colonial theory meets indigenous ontology, where ecology meets grief, where the trickster meets the compost heap. His work refuses the Western mythological framework of the hero's journey ('the hero is the problem') and asks instead: what if the most important mythic figure is not the one who conquers the dragon but the one who becomes food?",
            "What They Saw": "Myth as compost — not monument. Where Campbell saw the hero rising triumphant and Jung saw the ego integrating its shadow, Akomolafe sees myth as a process of decomposition. The stories that matter are not the ones that inspire us to be bigger, better, faster — they are the ones that undo us, that slow us down, that invite us to become soil. The trickster is his central figure: not the clever hero who outwits the system, but the crack in the system itself — the moment when the road fails and something unexpected grows in the failure. Anansi is not admirable; Anansi is the composting of admiration itself.",
            "Their Touchstone Myths": "Anansi the Spider (the trickster as decolonial figure — not the hero who liberates, but the crack in the system of liberation). Raven (appetite as transformation — not noble purpose but hungry accident). Creation from Chaos (the world made from decomposition, not from a plan). Inanna's Descent (not as heroic journey but as being undone — hung on a hook, rotting, becoming meat). The Flood (not catastrophe followed by renewal, but the waters that dissolve the distinction between catastrophe and renewal).",
            "The Lens": "To read a myth through Akomolafe's eyes: refuse the heroic reading. Don't ask 'who is the hero?' Ask: where does the story fail? Where does the road crack? Where does the protagonist become food, become soil, become something other than a protagonist? Notice what the myth composts — what identity, what certainty, what progress gets broken down. The trickster is not clever; the trickster is what happens when cleverness reaches its limit. The descent is not a stage in the hero's journey; the descent is the end of journeying.",
            "Blind Spots": "Akomolafe's framework can become its own form of dogma — the insistence that nothing should be heroic can itself become a heroic stance ('I am the one brave enough to refuse heroism'). His prose style, while beautiful, can be so allusive and poetic that it resists practical application. The emphasis on slowness, composting, and failure can feel like a luxury for those in genuine crisis who need to act now. And the critique of the hero's journey, however valid, can erase the real value that Campbell's framework provides to people who are suffering and need a story of return."
        },
        "keywords": ["akomolafe", "compost", "trickster", "decolonial", "slowness", "crack"],
        "composite_of": [
            "myth-anansi",
            "myth-raven-steals-light",
            "myth-creation-chaos",
            "myth-inanna",
            "myth-flood"
        ],
        "relationship_type": "emergence",
        "metadata": {}
    },
    {
        "id": "interp-shaw",
        "name": "Martin Shaw: Myth as Wilderness",
        "sort_order": 0,
        "category": "interpreters",
        "level": 2,
        "sections": {
            "Who They Were": "Martin Shaw (b. 1971), English mythologist, author of A Branch from the Lightning Tree, Scatterlings, Smoke Hole, and Courting the Wild Twin. Spent four years living alone in a tent on Dartmoor as a wilderness rite of passage. Trained as a storyteller in the oral tradition, he does not analyze myths — he tells them, in firelit rooms, over hours, with the full weight of a tradition that predates writing. His work sits at the intersection of mythology, ecology, and initiation: he argues that myths are not texts to be interpreted but living presences that require wildness — in the teller, the listener, and the land — to do their work.",
            "What They Saw": "Myth as ecology. Shaw argues that myths are not human stories about human concerns — they are the land dreaming. Every myth is rooted in a specific landscape, and when you sever the story from its place, it becomes a corpse pinned to an academic page. The oral tradition is not primitive or pre-literate — it is a sophisticated technology for keeping stories alive, allowing them to breathe, change, and respond to the moment of telling. The Selkie myth is not a metaphor for the wild feminine; it is a story told by people who lived with seals and knew them as neighbors. Skeleton Woman is not a relationship allegory; she is the actual Life/Death/Life nature that you encounter when you put your hands in cold water and pull up bones.",
            "Their Touchstone Myths": "Skeleton Woman (the central myth of his teaching — love as the willingness to face death). The Seal Wife (wildness captured and eventually escaping — the ecological soul that cannot be domesticated). The Fisher King (the wounded king whose wound is the land's wound — ecology as mythology). Taliesin (the shapeshifting chase, the cauldron of transformation — becoming animal to gain wisdom). Odin on Yggdrasil (the self-sacrifice for vision, the tree as axis of the world). Vasalisa (initiation through encounter with the terrifying feminine wild).",
            "The Lens": "To read a myth through Shaw's eyes: put it back in the landscape. Don't ask what it 'means' — ask where it was told, by whom, around what fire, in what season. Listen for the animals — they are not symbols but presences. Notice where the story goes underground, where the character enters forest or sea or cave — that's where the myth does its real work. Don't interpret; undergo. The myth is an initiation, and it will only work on you if you let it strip you the way it strips its protagonist. Read it aloud. Better yet, tell it from memory. Best of all, tell it outdoors.",
            "Blind Spots": "Shaw's insistence on the oral, embodied, land-based experience of myth can become exclusionary — if you must tell stories outdoors on Dartmoor to access their power, what about people in cities, in prisons, in hospitals? His framework romanticizes the wild and can underestimate the genuine power of literary, textual engagement with myth. His work is deeply English/Celtic, and his readings of non-European myths can lack the specificity he demands for his own tradition. And the emphasis on wilderness initiation carries gender and class assumptions about who gets to spend four years alone in a tent."
        },
        "keywords": ["shaw", "wilderness", "oral-tradition", "ecology", "initiation", "land"],
        "composite_of": [
            "myth-skeleton-woman",
            "myth-seal-wife",
            "myth-fisher-king",
            "myth-taliesin",
            "myth-odin-yggdrasil",
            "myth-vasalisa-baba-yaga"
        ],
        "relationship_type": "emergence",
        "metadata": {}
    },
    {
        "id": "interp-estes",
        "name": "Clarissa Pinkola Estés: The Wild Woman",
        "sort_order": 0,
        "category": "interpreters",
        "level": 2,
        "sections": {
            "Who They Were": "Clarissa Pinkola Estés (b. 1945), Mestiza (Mexican/Hungarian) Jungian analyst, cantadora (keeper of the old stories), poet, and author of Women Who Run With the Wolves (1992) — one of the best-selling mythology books in history. Trained in both Jungian analysis and the Latin American oral tradition of cuento (story-medicine), she bridges depth psychology and folk tradition. Her work argues that fairy tales and myths are not entertainment but psychic medicine — prescriptions for specific ailments of the soul, developed by women over millennia and transmitted in the oral tradition alongside recipes and remedies.",
            "What They Saw": "Myth as women's psychic medicine. Beneath the tamed, sanitized fairy tales collected by male scholars (Grimm, Perrault, Afanasyev), Estés finds older, wilder stories that encode women's deep knowledge about the cycles of the psyche: the Wild Woman archetype — the instinctual, creative, knowing nature that civilization teaches women to suppress. Every tale maps a specific psychic task: Vasalisa teaches intuition (the doll), Skeleton Woman teaches the Life/Death/Life nature of love, Bluebeard teaches how to recognize the predator, the Seal Wife teaches the cost of losing your wild skin. These are not 'just stories' — they are surgical instruments for psychic healing.",
            "Their Touchstone Myths": "Vasalisa and Baba Yaga (the recovery of intuition through initiation by the Dark Mother). Skeleton Woman (the Life/Death/Life nature — what must die in a relationship for it to live). Bluebeard (the natural predator of the psyche — the voice that says 'don't look, don't know'). The Seal Wife (the wild skin stolen — the cost of over-domestication). Psyche and Eros (the soul's tasks — sorting seeds, gathering golden fleece, descending to the underworld). Persephone (the naive maiden who becomes queen of the underworld through descent). Inanna (the most complete descent myth — stripped at every gate).",
            "The Lens": "To read a myth through Estés's eyes: look for the woman's journey. Who is she at the beginning? (Often: naive, over-tamed, cut off from instinct.) What happens to her? (Descent, initiation, encounter with a dark power.) What does she gain? (Instinct, knowing, fire, the ability to see.) Ask: what part of the feminine psyche has been starved, captured, or put to sleep — and what does this story prescribe to wake it? Notice the old women in the story (Baba Yaga, the doll, the grandmother) — they are the Wild Woman in her teaching form. Every fairy tale is a medicine story. What is it medicine for?",
            "Blind Spots": "Estés's framework is explicitly gendered — she writes for and about women, and her archetypal 'Wild Woman' can essentialize femininity in ways that are uncomfortable for non-binary readers or for women whose wildness doesn't look like her model. Her Jungian training leads her to universalize specific cultural stories (a Hungarian fairy tale becomes 'every woman's story'). Her writing style — passionate, poetic, incantatory — can substitute emotional intensity for analytical rigor. And her emphasis on the 'natural' and 'instinctual' can romanticize pre-modern life while underestimating the genuine liberatory power of rationality and modernity."
        },
        "keywords": ["estes", "wild-woman", "fairy-tales", "feminine", "psychic-medicine", "wolves"],
        "composite_of": [
            "myth-vasalisa-baba-yaga",
            "myth-skeleton-woman",
            "myth-bluebeard",
            "myth-seal-wife",
            "myth-psyche-eros",
            "myth-persephone",
            "myth-inanna"
        ],
        "relationship_type": "emergence",
        "metadata": {}
    },
    {
        "id": "interp-warner",
        "name": "Marina Warner: Myth as Social History",
        "sort_order": 0,
        "category": "interpreters",
        "level": 2,
        "sections": {
            "Who They Were": "Marina Warner (b. 1946), British novelist, historian, and mythographer. Author of Alone of All Her Sex (the Virgin Mary), From the Beast to the Blonde (fairy tales and their tellers), No Go the Bogeyman (fear in stories), and Stranger Magic (the Arabian Nights). DBE, FBA, Professor of English and Creative Writing at Birkbeck, University of London. Where Jung reads myths psychologically and Frazer reads them anthropologically, Warner reads them historically — as documents of social power, gender politics, and the lived experience of the women who told them. She insists on asking the question scholars forget: who is telling this story, to whom, and why?",
            "What They Saw": "Myth as social history — fairy tales as women's coded knowledge. Warner argues that fairy tales were not originally told to children but by women to women — around spinning wheels, at washing places, in kitchens — and they encode practical survival knowledge in symbolic form. Bluebeard is not an archetype; it is a warning about real husbands who murder real wives, told by women who had seen it happen. Scheherazade is not a symbol of narrative power; she is a portrait of what women actually had to do to survive in patriarchal courts — talk their way out of being killed. The magic in fairy tales is not escapism; it is the only power available to the powerless. The transformation tales (beast to man, frog to prince, ashes to gown) encode women's fantasies of changing the men and circumstances they cannot leave.",
            "Their Touchstone Myths": "Scheherazade (the woman who narrates to survive — Warner's central figure for the female storyteller's power and peril). Bluebeard (the serial killer hidden in plain sight — the fairy tale as women's crime report). Psyche and Eros (the woman who insists on seeing what she loves — curiosity as women's weapon). The Flood (survivors as refugees — Warner connects ancient flood myths to modern displacement). Sun Wukong (the trickster as political subversive, the powerless outwitting the powerful). The Hero Twins (the underworld as political underworld — the realm of those who have been defeated by power).",
            "The Lens": "To read a myth through Warner's eyes: ask who is telling this story and why. Who benefits from this version? Whose voice is missing? Look for the teller — often a woman (a grandmother, a nurse, a weaver, a spinner) — and consider what she was teaching. Notice the material conditions: the locked rooms, the spinning, the domestic labor, the marriages arranged by fathers. Don't psychologize — historicize. The cruel stepmother is not an archetype; she is a feature of societies where men remarried after their wives died in childbirth and the new wife favored her own children. Read the fairy tale as a document from a world where women's power was voice, cunning, and patience — and ask what has changed.",
            "Blind Spots": "Warner's historical lens can reduce myth to sociology — when every fairy tale becomes 'really about' social conditions, the numinous, archetypal, and genuinely mysterious dimensions disappear. Her focus on European fairy tales (French, Arabian Nights, Greek) means she says less about traditions she knows less well. Her insistence on the woman-as-teller can erase male oral traditions and the complexity of cross-gender storytelling. And her rationalist, historicist approach — however valuable — can flatten the very quality that makes myths different from other historical documents: their uncanny, dream-like, non-rational power."
        },
        "keywords": ["warner", "social-history", "fairy-tales", "gender", "power", "storytelling"],
        "composite_of": [
            "myth-scheherazade",
            "myth-bluebeard",
            "myth-psyche-eros",
            "myth-flood",
            "myth-sun-wukong",
            "myth-hero-twins"
        ],
        "relationship_type": "emergence",
        "metadata": {}
    }
]

# ── 1 NEW CULTURE CARD ──────────────────────────────────────────────────────

new_culture = {
    "id": "culture-african-arabian",
    "name": "Africa and Arabia: Tricksters, Weavers, and the Night",
    "sort_order": 0,
    "category": "cultures",
    "level": 2,
    "sections": {
        "The World": "The mythic imagination of Africa and the Arabian world is a tapestry of voices — not one tradition but hundreds, threaded together by trade routes, the Sahara, the Indian Ocean, and the ancient practice of gathering at nightfall to tell stories. West African mythology gave the world the trickster spider, the talking drum, and the principle that stories are a form of wealth that can be owned, stolen, and liberated. The Arabian Nights gave the world the frame tale — stories within stories within stories — and the figure of Scheherazade, who proved that narrative itself is a survival technology. Both traditions share a radical idea: the word is power. To tell a story is to act on the world.",
        "What Makes It Unique": "The African contribution: the trickster as survivor. Where European heroes slay dragons with swords, Anansi uses string, cleverness, and his wife's advice. The trickster tradition was carried across the Atlantic in the bodies and memories of enslaved people, becoming Br'er Rabbit, Aunt Nancy, and a thousand coded resistance tales. The Arabian contribution: the frame tale and the jinn — beings of smokeless fire who exist alongside humans in a parallel creation, neither angels nor demons but a third thing. Both traditions center oral performance: the griot, the hakawati (coffeehouse storyteller), the grandmother at the fire. In these worlds, the storyteller is not an entertainer but a keeper of power.",
        "Contemplation": "These are traditions where the small defeat the large — the spider traps the python, the bride outwits the king. When in your life has cunning been more important than strength? When has a story saved you?"
    },
    "keywords": ["african", "arabian", "trickster", "anansi", "scheherazade", "oral-tradition"],
    "composite_of": [
        "myth-anansi",
        "myth-scheherazade",
        "myth-raven-steals-light"
    ],
    "relationship_type": "emergence",
    "metadata": {}
}

# ── INSERTION LOGIC ──────────────────────────────────────────────────────────

# Find insertion points
raven_idx = next(i for i, item in enumerate(items) if item["id"] == "myth-raven-steals-light")
shrei_idx = next(i for i, item in enumerate(items) if item["id"] == "interp-shrei")
culture_eastern_idx = next(i for i, item in enumerate(items) if item["id"] == "culture-eastern")

# Insert new myths after raven (end of myths section)
for i, myth in enumerate(new_myths):
    items.insert(raven_idx + 1 + i, myth)

# Recalculate indices after myth insertion
shrei_idx = next(i for i, item in enumerate(items) if item["id"] == "interp-shrei")

# Insert new interpreters after shrei
for i, interp in enumerate(new_interpreters):
    items.insert(shrei_idx + 1 + i, interp)

# Recalculate indices after interpreter insertion
culture_eastern_idx = next(i for i, item in enumerate(items) if item["id"] == "culture-eastern")

# Insert new culture card after culture-eastern
items.insert(culture_eastern_idx + 1, new_culture)

# ── UPDATE THREAD COMPOSITE_OF ARRAYS ────────────────────────────────────────

thread_updates = {
    "thread-descent": ["myth-vasalisa-baba-yaga", "myth-bluebeard"],
    "thread-sacred-marriage": ["myth-skeleton-woman", "myth-seal-wife"],
    "thread-trickster": ["myth-anansi", "myth-scheherazade"],
    "thread-great-mother": ["myth-vasalisa-baba-yaga", "myth-skeleton-woman"],
    "thread-dragon-fight": ["myth-bluebeard"],
    "thread-stolen-light": ["myth-anansi", "myth-scheherazade"],
}

for item in items:
    if item["id"] in thread_updates:
        item["composite_of"].extend(thread_updates[item["id"]])

# Also add seal-wife to culture-northern
for item in items:
    if item["id"] == "culture-northern":
        item["composite_of"].append("myth-seal-wife")

# ── UPDATE META-COLLECTIVE-UNCONSCIOUS ───────────────────────────────────────

for item in items:
    if item["id"] == "meta-collective-unconscious":
        # Update About text
        item["sections"]["About"] = item["sections"]["About"].replace(
            "Nine interpreters — Jung, Campbell, Rank, Frazer, the alchemists, Neumann, Hillman, Eliade, Shrei —",
            "Thirteen interpreters — Jung, Campbell, Rank, Frazer, the alchemists, Neumann, Hillman, Eliade, Shrei, Akomolafe, Shaw, Estés, Warner —"
        )
        # Add new interpreters to composite_of
        item["composite_of"].extend([
            "interp-akomolafe", "interp-shaw", "interp-estes", "interp-warner"
        ])

# ── RECALCULATE ALL SORT_ORDERS ──────────────────────────────────────────────

for i, item in enumerate(items):
    item["sort_order"] = i + 1

# ── UPDATE DESCRIPTION ───────────────────────────────────────────────────────

g["description"] = g["description"].replace(
    "Twenty-five world myths",
    "Thirty-one world myths"
).replace(
    "through the eyes of Jung, Campbell, Frazer, the alchemists, and other interpreters",
    "through the eyes of thirteen interpreters — Jung, Campbell, Frazer, the alchemists, Estés, Warner, Akomolafe, Shaw, and others"
)

# ── SAVE ─────────────────────────────────────────────────────────────────────

g["items"] = items

with open("grammars/myths-through-many-eyes/grammar.json", "w") as f:
    json.dump(g, f, indent=2, ensure_ascii=False)

print(f"Total items: {len(items)}")
print(f"L1 myths: {sum(1 for i in items if i['level'] == 1)}")
print(f"L2 interpreters: {sum(1 for i in items if i['category'] == 'interpreters')}")
print(f"L2 threads: {sum(1 for i in items if i['category'] == 'threads')}")
print(f"L2 cultures: {sum(1 for i in items if i['category'] == 'cultures')}")
print(f"L3 meta: {sum(1 for i in items if i['level'] == 3)}")
print(f"Sort orders: 1..{items[-1]['sort_order']}")
