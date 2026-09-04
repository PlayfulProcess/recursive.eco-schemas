#!/usr/bin/env python3
"""Build 'Roots of Moana' grammar — the real Polynesian mythology, wayfinding,
oceanic animism, music, and cultural traditions that inspired Disney's Moana."""

import json, os

grammar = {
    "_grammar_commons": {
        "schema_version": "1.0",
        "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "PlayfulProcess", "date": "2026", "note": "Grammar compilation and children's adaptations"},
            {"name": "Polynesian oral tradition", "date": "ancient–present", "note": "Stories, chants, and navigation knowledge passed down through Pacific Island cultures"},
            {"name": "Te Rangikāheke", "date": "c. 1849", "note": "Māori scholar who recorded Māui myths for George Grey's 'Polynesian Mythology' (1855)"},
            {"name": "Martha Beckwith", "date": "1940", "note": "'Hawaiian Mythology' — comprehensive scholarly collection, University of Hawaii Press"},
            {"name": "Johannes C. Andersen", "date": "1928", "note": "'Myths and Legends of the Polynesians' — comparative mythology across Pacific cultures"}
        ]
    },
    "name": "Roots of Moana — Polynesian Mythology & Wayfinding for Kids",
    "description": "The real mythic, cultural, and musical traditions behind Disney's Moana — told for children. Explore the demigod Māui's legendary feats, Polynesian star navigation, oceanic animism where every wave and wind has spirit, the sacred art of voyaging canoes, and the music traditions from hula to log drums. Each card connects a real cultural tradition to the film moment it inspired.\n\nSources: Polynesian oral tradition; George Grey's 'Polynesian Mythology' (1855); Martha Beckwith's 'Hawaiian Mythology' (1940); Johannes C. Andersen's 'Myths and Legends of the Polynesians' (1928). All source texts are public domain.\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: John La Farge's Samoan and Tahitian paintings (1890s) — luminous tropical landscapes and Pacific Islander portraits. Arman Manookian's Hawaiian paintings (1920s) — bold figurative work of island life. Jacques Arago's voyage illustrations (1817-1820) — early European depictions of Pacific navigation and culture. Illustrations from 'Polynesian Mythology' by George Grey (1855 edition) — line engravings of Māui legends.",
    "grammar_type": "custom",
    "creator_name": "PlayfulProcess",
    "tags": [
        "polynesian", "mythology", "maui", "wayfinding", "navigation",
        "pacific-islands", "animism", "ocean", "voyaging", "hula",
        "kids", "cultural-roots", "moana-inspired", "demigod",
        "hawaii", "samoa", "tonga", "new-zealand", "music", "oral-tradition"
    ],
    "roots": ["indigenous-knowledge", "mythopoetic-enchantment"],
    "shelves": ["children", "wonder", "wisdom"],
    "lineages": ["Akomolafe", "Shrei", "Andreotti"],
    "worldview": "animist",
    "items": []
}

items = []
sort = 0

# =============================================================================
# L1 ITEMS — THE REAL STORIES
# =============================================================================

# --- MĀUI THE DEMIGOD ---

maui_items = [
    {
        "id": "maui-born-of-ocean",
        "name": "Māui: Born of the Ocean",
        "category": "maui-legends",
        "sections": {
            "Story": "Baby Māui was born too small, too early. His mother Taranga wrapped him in a tuft of her hair and placed him in the sea. But the ocean didn't let him drown — the jellyfish cushioned him, the seaweed wrapped him warm, and the waves carried him to shore where his great-ancestor Tama-nui-ki-te-Rangi found him and raised him.\n\nWhen Māui grew up, he walked back to his mother's home, and she didn't even recognize him. He had to prove who he was — the tiny baby she'd given to the sea, now a young man full of tricks and courage.",
            "The Real Tradition": "In Māori tradition, Māui is 'Māui-tikitiki-a-Taranga' — Māui-formed-in-the-topknot-of-Taranga. The story of a rejected child raised by the sea or by ancestor spirits is told across Polynesia from New Zealand to Hawai'i. It teaches that the ocean is not an enemy but a parent — it gives life, carries messages, and connects all islands.",
            "Film Connection": "In Disney's Moana, baby Moana is chosen by the ocean itself — the water parts for her and hands her a shell. This mirrors Māui's birth story: the ocean as a conscious being that chooses and protects children.",
            "Reflection": "Have you ever felt too small or not good enough? Māui was the smallest baby, but the whole ocean decided he was worth saving. What does the ocean see in you?"
        },
        "keywords": ["maui", "birth", "ocean", "mother", "taranga", "rejected-child"]
    },
    {
        "id": "maui-slows-the-sun",
        "name": "Māui Lassoes the Sun",
        "category": "maui-legends",
        "sections": {
            "Story": "The days were too short! The sun raced across the sky so fast that people couldn't cook their food, dry their cloth, or finish their work before darkness fell. Māui's mother complained that nothing could get done.\n\nSo Māui braided the strongest ropes from flax — some say from his grandmother's magic jawbone hair — and traveled east to the pit where the sun sleeps. When the sun climbed out at dawn, Māui lassoed its rays one by one and BEAT the sun with his grandmother's enchanted jawbone until it promised to go slowly.\n\nThat's why summer days are long and the sun moves gently across the sky.",
            "The Real Tradition": "This is one of the most widespread Polynesian myths. In Hawai'i, the mountain Haleakalā means 'House of the Sun' — where Māui trapped it. In Māori tradition, the weapon is the jawbone of his ancestor Muriranga-whenua. The story explains seasonal variation and teaches that even cosmic forces can be tamed by human cleverness and courage.",
            "Film Connection": "In Moana, Māui sings 'You're Welcome' listing his feats — 'I lassoed the sun' is the very first one he mentions! The real myth is even wilder than the movie version.",
            "Reflection": "Māui didn't just complain about the short days — he DID something about it. What's something in your life that feels too fast or too short? What would you do if you could slow it down?"
        },
        "keywords": ["maui", "sun", "lasso", "haleakala", "jawbone", "courage"]
    },
    {
        "id": "maui-fishes-up-islands",
        "name": "Māui Fishes Up the Islands",
        "category": "maui-legends",
        "sections": {
            "Story": "Māui's brothers never wanted to take him fishing — they said he was too small and too tricky. But Māui snuck aboard their canoe and hid under the floorboards.\n\nWhen they were far out at sea, Māui popped up and cast his magic fishhook — baited with his own blood from his nose — deep into the ocean. He pulled and pulled, and up came not a fish but an ENORMOUS piece of land! The whole North Island of New Zealand rose dripping from the sea.\n\nHis brothers were so greedy they started cutting up the 'fish' before Māui could say the proper prayers, and that's why New Zealand's North Island has so many mountains and valleys — it's the thrashing, cut-up fish of Māui.",
            "The Real Tradition": "In Māori, the North Island is Te Ika-a-Māui — 'The Fish of Māui.' The South Island is his canoe. In Hawai'i, Māui fished up each island separately. In Tonga, he pulled up the Tongan islands. Every Polynesian culture has its own version of Māui's magic fishhook creating their homeland from the sea floor.",
            "Film Connection": "Māui's giant magical fishhook is central to the movie — it's what gives him his shapeshifting power. The real myth is about pulling LAND from the ocean, which is metaphorically what Polynesian navigators did: they 'found' new islands in the vast Pacific.",
            "Reflection": "The story says Māui's brothers ruined the land by being greedy. What happens when people grab at things without being thankful first?"
        },
        "keywords": ["maui", "fishhook", "islands", "new-zealand", "creation", "greed"]
    },
    {
        "id": "maui-steals-fire",
        "name": "Māui Steals Fire from the Underworld",
        "category": "maui-legends",
        "sections": {
            "Story": "One night, Māui secretly put out every fire in the village. In the morning, his mother sent him to fetch fire from his grandmother Mahuika, the fire goddess who lived in the Underworld.\n\nMahuika kept fire in her fingernails. She pulled off one nail and gave Māui its flame. But tricky Māui put it out and came back asking for more. One by one, Mahuika pulled off her fingernails and toenails, giving him fire after fire. When she realized he was tricking her, she threw her LAST nail at him in rage — and the whole world nearly burned!\n\nMāui called on the rain to save him. The fire retreated into the trees — and that's where fire lives now, hiding inside wood, waiting to be rubbed out with sticks.",
            "The Real Tradition": "This fire-origin myth explains the technology of fire-by-friction (rubbing sticks). Mahuika (Māori) or Mahui'a (Hawaiian) is the fire deity. The story appears across Polynesia and echoes the Greek myth of Prometheus — but in the Polynesian version, it's a grandson tricking a grandmother, which is funnier and more human.",
            "Film Connection": "Though this specific myth isn't shown in Moana, it shapes Māui's character as a trickster who steals from gods for humanity's benefit — exactly how the movie portrays him with the Heart of Te Fiti.",
            "Reflection": "Māui stole fire so humans could cook and stay warm. But he also nearly burned the world! Do you think the risk was worth it? When is it okay to break the rules to help others?"
        },
        "keywords": ["maui", "fire", "mahuika", "trickster", "underworld", "prometheus"]
    },
    {
        "id": "maui-and-death",
        "name": "Māui's Final Quest: The Goddess of Death",
        "category": "maui-legends",
        "sections": {
            "Story": "Māui had beaten the sun, fished up islands, stolen fire — but there was one enemy left: Death itself. His father told him about Hine-nui-te-Pō, the Great Woman of the Night, goddess of death. If Māui could crawl through her sleeping body and come out the other side, humans would live forever.\n\nMāui turned himself into a caterpillar and began to crawl inside. But a little bird — the fantail, tīwairwaka — saw him and LAUGHED so hard that it woke Hine-nui-te-Pō. She crushed Māui between her thighs, and that was the end of the great demigod.\n\nAnd that is why all humans must die — because a little bird laughed at the wrong moment.",
            "The Real Tradition": "This is the most important Māui myth — it explains why humans are mortal. The fantail bird (pīwakawaka) is still considered an omen of death in Māori culture. The story teaches that death is natural and that even the greatest hero cannot defeat it. It gives death dignity rather than treating it as pure evil.",
            "Film Connection": "Disney didn't include this myth (it's intense!), but it shapes the movie's theme: Māui's flaw is wanting to be immortal and loved forever. In the real myths, that desire literally kills him.",
            "Reflection": "Even the strongest, cleverest person who ever lived couldn't beat death. Does that make you sad, or does it make every day feel more special?"
        },
        "keywords": ["maui", "death", "hine-nui-te-po", "mortality", "fantail", "hero"]
    },
    # --- NAVIGATION & WAYFINDING ---
    {
        "id": "star-compass",
        "name": "The Star Compass: Reading the Sky",
        "category": "wayfinding",
        "sections": {
            "Story": "Imagine you're standing on a canoe in the middle of the Pacific Ocean. No land in sight. No GPS, no maps, no compass. How do you find your way?\n\nPolynesian navigators divided the horizon into a star compass — a mental map of where different stars rise and set. They memorized HUNDREDS of stars, tracking which ones appeared where throughout the night and across seasons. The star Hokule'a (Arcturus) passes directly overhead in Hawai'i, so if you sail toward it, you'll find the Hawaiian islands.\n\nThis knowledge was passed from master navigator to student through years of training, memorization, and night watches at sea.",
            "The Real Tradition": "The Hawaiian star compass (kealaikahiki) and the Micronesian star compass (etak) are sophisticated navigation systems that allowed Pacific Islanders to cross thousands of miles of open ocean. Master navigator Mau Piailug of Satawal shared this knowledge with the Polynesian Voyaging Society in the 1970s, helping revive the tradition.",
            "Film Connection": "In Moana, Moana's grandmother shows her the star compass in the secret cave, and Moana later learns to read the stars with Māui's help. The movie's navigation scenes are based on real star compass techniques.",
            "Reflection": "Polynesian navigators memorized the sky like you might memorize a book. What's the most complicated thing you've ever memorized? Imagine memorizing the entire night sky!"
        },
        "keywords": ["navigation", "stars", "hokulea", "compass", "wayfinding", "astronomy"]
    },
    {
        "id": "reading-waves",
        "name": "Reading the Waves: Ocean Swells as Maps",
        "category": "wayfinding",
        "sections": {
            "Story": "Stars only work at night and on clear nights. So how did navigators find their way during the day, or when clouds covered the sky?\n\nThey READ THE WAVES. The ocean isn't just random slosh — it has patterns. Long, deep swells roll in consistent directions across the whole Pacific. When those swells hit an island (even one far over the horizon), they bounce back and bend around it, creating interference patterns that a trained navigator can feel with their body.\n\nNavigators would lie down in the hull of the canoe, close their eyes, and FEEL the wave patterns through the wood. They could detect an island 50 miles away just from how the waves moved.",
            "The Real Tradition": "Marshall Islanders created 'stick charts' (mattang, meddo, rebbelib) — frameworks of palm ribs and shells showing wave refraction patterns around islands. These weren't carried on voyages; they were teaching tools. The real map was in the navigator's body — years of training to feel swells, cross-swells, and island reflections.",
            "Film Connection": "When Moana closes her eyes on the ocean and feels the water guiding her, she's using real wave-reading navigation. The movie beautifully depicts this embodied knowledge.",
            "Reflection": "These navigators didn't just think about the ocean — they FELT it with their whole body. What do you know in your body, not just your head? (Maybe riding a bike, swimming, or dancing?)"
        },
        "keywords": ["waves", "navigation", "stick-charts", "marshall-islands", "embodied-knowledge"]
    },
    {
        "id": "voyaging-canoe",
        "name": "The Voyaging Canoe: A Living Vessel",
        "category": "wayfinding",
        "sections": {
            "Story": "The great double-hulled voyaging canoes of Polynesia were engineering marvels. Two hulls connected by a platform could carry 80 people, their animals, their seeds, fresh water, and everything needed to start life on a new island — across thousands of miles of open ocean.\n\nBuilding a canoe was a sacred act. The master builder (tufunga) would choose a tree and ask its permission to be felled. Every step — cutting, shaping, lashing, launching — had prayers and ceremonies. The canoe wasn't just a boat; it was a living being with a spirit (mana) of its own.\n\nWhen the canoe was finished, it was 'born' in a launching ceremony just like a child.",
            "The Real Tradition": "The Hōkūle'a, a traditional Hawaiian double-hulled voyaging canoe, was built in 1975 and has sailed over 150,000 nautical miles using only traditional navigation. Its worldwide voyage (Mālama Honua, 2013-2017) visited 150 ports in 23 countries, proving that ancient Polynesian navigation could cross any ocean on Earth.",
            "Film Connection": "The hidden fleet of voyaging canoes that Moana discovers in the cave is based on the real historical fleet that Polynesian ancestors used during the great era of Pacific exploration (roughly 1000-1300 CE). The movie's message — 'We were voyagers' — is historically accurate.",
            "Reflection": "Polynesians built canoes strong enough to cross the Pacific using only wood, fiber, and stone tools. No metal, no engines, no GPS. What does that tell you about how clever humans can be?"
        },
        "keywords": ["canoe", "hokulea", "voyaging", "double-hull", "sacred", "engineering"]
    },
    {
        "id": "bird-signs",
        "name": "Following the Birds Home",
        "category": "wayfinding",
        "sections": {
            "Story": "When you're out on the open ocean, how do you know land is near? Follow the birds!\n\nPolynesian navigators knew that certain seabirds — like the golden plover (kōlea) and the frigatebird — fly out to sea to fish during the day but return to land at night. So if you saw birds flying in one direction at sunset, land was that way.\n\nThe golden plover is especially magical: it migrates 3,000 miles nonstop from Alaska to Hawai'i every year. Ancient Polynesians may have followed its migration route to discover new islands. The bird literally showed them the way.",
            "The Real Tradition": "Bird observation was one of the key wayfinding techniques. Different birds have different ranges from land: frigatebirds might indicate land within 75 miles, boobies within 30 miles, and terns within 15 miles. Navigators also watched the direction birds flew at dawn and dusk to determine the bearing of the nearest island.",
            "Film Connection": "In Moana, Maui shapeshifts into a hawk — birds are central to his power. And the rooster Heihei (though useless as a navigator!) represents the tradition of carrying birds on voyaging canoes, both as food and as living compasses.",
            "Reflection": "Birds don't need GPS or star charts — they just KNOW where to go. Animals have their own kind of wisdom. What can we learn from paying attention to animals?"
        },
        "keywords": ["birds", "navigation", "golden-plover", "frigatebird", "migration", "signs"]
    },
    # --- OCEANIC ANIMISM ---
    {
        "id": "ocean-as-ancestor",
        "name": "The Ocean Is an Ancestor",
        "category": "oceanic-animism",
        "sections": {
            "Story": "In Western culture, the ocean is a thing — a big body of water. But in Polynesian culture, the ocean is a WHO, not a WHAT.\n\nThe ocean (Moana, which is also a name!) is Tangaroa — a god, an ancestor, a living being. When fishermen go out to sea, they don't just 'use' the ocean; they enter a relationship with it. They offer prayers before fishing, return the first catch to Tangaroa, and never take more than they need.\n\nThe ocean gives food, carries travelers between islands, brings rain, and connects all Polynesian people. It's the great highway, the great ancestor, the great mother.",
            "The Real Tradition": "Tangaroa (Tagaloa in Samoan, Kanaloa in Hawaiian, Ta'aroa in Tahitian) is one of the most important Polynesian deities — the god of the sea and father of fish. In some traditions, Ta'aroa is the supreme creator who existed in a shell (like a cosmic egg) before creating the world. The ocean-as-ancestor concept is central to Pacific Island identity.",
            "Film Connection": "The ocean in Moana is literally a character — it chooses Moana, plays with her, helps her, and has a personality. This isn't Disney invention; it's how Polynesian culture actually relates to the sea. The ocean IS a being.",
            "Reflection": "What if the ocean really could think and feel? How would you treat the beach and the water differently?"
        },
        "keywords": ["tangaroa", "ocean", "ancestor", "animism", "relationship", "sacred"]
    },
    {
        "id": "te-fiti-and-te-ka",
        "name": "Pele and Papa: Fire and Earth Goddesses",
        "category": "oceanic-animism",
        "sections": {
            "Story": "In Hawai'i, the earth is alive because of Pele — the goddess of fire, volcanoes, and creation. She lives in Kīlauea volcano, and when lava flows, that's Pele reshaping the land. New islands are literally being BORN from her fire right now — Lōʻihi seamount is growing underwater southeast of Hawai'i and will become a new island in thousands of years.\n\nBut Pele has another side: when she's angry, she DESTROYS. Lava buries villages and forests. This isn't evil — it's the cycle of creation and destruction that makes new land possible. You can't have new islands without fire first.\n\nPapa (Papatūānuku in Māori) is the Earth Mother herself, whose body IS the land. When you stand on soil, you stand on an ancestor.",
            "The Real Tradition": "The duality of creation and destruction through volcanic activity is central to Hawaiian spirituality. Te Fiti (creative earth goddess) and Te Kā (destructive fire demon) in Moana are inspired by this real theological concept — they are the same being in different states. Pele IS both creator and destroyer.",
            "Film Connection": "Te Fiti and Te Kā in Moana are one being — the island goddess of creation who becomes a lava demon of destruction when her heart is stolen. This directly mirrors the Polynesian understanding that creation and destruction are not opposites but two faces of the same divine force.",
            "Reflection": "Te Fiti and Te Kā are the SAME person — one creates, one destroys. Can you think of a time when something had to be broken or lost before something new and good could happen?"
        },
        "keywords": ["pele", "te-fiti", "te-ka", "volcano", "creation", "destruction", "papa"]
    },
    {
        "id": "mana-and-tapu",
        "name": "Mana and Tapu: Sacred Power and Sacred Rules",
        "category": "oceanic-animism",
        "sections": {
            "Story": "Everything in Polynesia has MANA — spiritual power, prestige, authority. A great chief has mana. A master navigator has mana. A well-built canoe has mana. Even a stone can have mana if important things happened there.\n\nMana isn't like electricity — it's more like respect that has become real. When a warrior wins many battles, their weapon accumulates mana. When a family has lived honorably for generations, their land has mana.\n\nTAPU (where our word 'taboo' comes from!) means something is so sacred and full of mana that ordinary people shouldn't touch it. The chief's head was tapu. Certain fishing grounds were tapu at certain times so fish could recover. Tapu was Polynesia's way of protecting sacred things — including nature.",
            "The Real Tradition": "Mana and tapu form the spiritual-legal framework of Polynesian society. Mana can be gained through achievement and lost through shame. Tapu restrictions served ecological functions (fishing seasons, forest management) as well as social ones. The concept of tapu as environmental protection is one of the earliest known conservation systems.",
            "Film Connection": "Māui's power in the movie comes from his fishhook — an object full of mana from all his legendary deeds. When it breaks, he feels powerless. The film also shows tapu through the island's rule against going beyond the reef — a restriction that protects the community.",
            "Reflection": "Mana means that your actions give power to the things you use and the places you go. If your favorite toy or your bedroom had mana from all the good things you've done there, how much mana would it have?"
        },
        "keywords": ["mana", "tapu", "taboo", "sacred", "power", "conservation"]
    },
    {
        "id": "shapeshifting",
        "name": "Shapeshifters: Humans, Gods, and Animals Are Family",
        "category": "oceanic-animism",
        "sections": {
            "Story": "In Polynesian tradition, the line between humans, animals, and gods is very thin — and you can cross it!\n\nMāui is the most famous shapeshifter: he becomes a hawk, a worm, a caterpillar, a pigeon. But he's not unique. Many Polynesian stories feature 'aumakua (Hawaiian) or atua (Māori) — family gods who take animal form. Your family might have a shark 'aumakua, an owl 'aumakua, or a lizard 'aumakua.\n\nIf your family's 'aumakua is a shark, you would never hunt sharks. And if you saw a shark while swimming, you wouldn't panic — you'd recognize it as a relative watching over you.",
            "The Real Tradition": "'Aumakua worship is still practiced in Hawaiian culture today. Family guardian spirits manifest as specific animals (shark, owl, hawk, sea turtle, eel) and protect family members. This creates a kinship network that includes non-human beings — you literally have animal relatives. This is animism at its most practical: if every family has animal guardians, the whole ecosystem is protected by family bonds.",
            "Film Connection": "Māui's shapeshifting in Moana — turning into a hawk, a shark, a beetle — comes directly from real mythology. The movie also shows Tamatoa (the giant crab) and the Kakamora (coconut pirates) as beings with their own agency, reflecting the Polynesian view that non-human beings have personhood.",
            "Reflection": "If you had an animal guardian in your family — an 'aumakua — what animal would it be? How would it change the way you treat that animal?"
        },
        "keywords": ["shapeshifting", "aumakua", "animal-guardians", "kinship", "transformation"]
    },
    # --- MUSIC & PERFORMANCE ---
    {
        "id": "hula-as-library",
        "name": "Hula: Dancing the Stories Alive",
        "category": "music-and-performance",
        "sections": {
            "Story": "Before books and writing, how did Polynesian people remember their history, their laws, their science, and their genealogies?\n\nThey DANCED them. Hula isn't just pretty dancing — it's a living library. Each gesture means something specific: waving hands can mean ocean waves, a cupped hand means the moon, fingers rippling downward means rain. A single hula performance can tell a story that would fill a whole book.\n\nHula dancers train for years, memorizing hundreds of chants (oli) and their corresponding movements. Ancient hula (hula kahiko) was performed in temples as sacred ceremony. It was so important that making a mistake during performance was considered spiritually dangerous.",
            "The Real Tradition": "Hula was banned by Protestant missionaries in 1830 and went underground for decades. King David Kalākaua (the 'Merrie Monarch') revived it in the 1880s. Today, the Merrie Monarch Festival in Hilo is the world's premier hula competition. Hula continues to be both a cultural practice and a way of preserving Hawaiian language and knowledge.",
            "Film Connection": "The dance sequences in Moana — especially the village celebration scenes — draw on real Polynesian dance traditions. The hand-clapping, foot-stomping group dances reflect Samoan siva and slap dance (fa'ataupati). Moana's movements when she navigates echo hula hand gestures for ocean and stars.",
            "Reflection": "Imagine if your school didn't have books, and instead you had to learn everything through dance. What story would you want to learn to dance?"
        },
        "keywords": ["hula", "dance", "oral-tradition", "library", "kalakaua", "sacred"]
    },
    {
        "id": "pate-and-log-drums",
        "name": "Log Drums and Conch Shells: The Sounds of the Pacific",
        "category": "music-and-performance",
        "sections": {
            "Story": "Close your eyes and imagine the sounds of a Polynesian village: the deep BOOM of log drums (pate) echoing across the valley, the haunting call of a conch shell (pū) announcing a chief's arrival, the rhythmic slap-slap-slap of hands on skin during dance.\n\nPolynesian music is percussion-driven — no stringed instruments existed before European contact. The body itself was an instrument: chest-slapping (fa'ataupati in Samoa), thigh-slapping, hand-clapping, and foot-stomping created complex rhythms. Slit drums carved from logs could send messages between villages miles apart.\n\nThe ukulele? That came later — Portuguese immigrants brought a small guitar to Hawai'i in 1879, and Hawaiians made it their own.",
            "The Real Tradition": "Traditional Polynesian instruments include: pahu (sharkskin drum), pate/tō'ere (slit log drum), pū (conch shell trumpet), 'ulī'ulī (feathered gourd rattle), ipu (gourd drum), and the nose flute (kōauau in Māori). Each instrument has ceremonial significance. The pahu drum was so sacred it could only be played in temples.",
            "Film Connection": "The percussion-heavy score of Moana (by Lin-Manuel Miranda, Opetaia Foa'i, and Mark Mancina) was directly inspired by traditional Polynesian instruments. Opetaia Foa'i of Te Vaka brought authentic Pacific Island musical traditions — especially the log drum patterns and group chanting — into the film's soundtrack.",
            "Reflection": "Try making music with just your body — clap, stomp, slap your thighs, snap your fingers. Can you make a rhythm that feels like ocean waves?"
        },
        "keywords": ["drums", "pate", "conch", "percussion", "ukulele", "te-vaka", "rhythm"]
    },
    {
        "id": "chanting-genealogy",
        "name": "Singing Your Family Tree: Genealogy Chants",
        "category": "music-and-performance",
        "sections": {
            "Story": "In Polynesian culture, knowing your genealogy (whakapapa in Māori) isn't just nice — it's EVERYTHING. Your genealogy tells you which land you belong to, which ocean routes your ancestors sailed, which gods you're descended from, and which families you're connected to.\n\nGenealogy is sung in chants that can last for HOURS, tracing a family line back dozens of generations — sometimes all the way to the gods. A Māori person might chant their whakapapa back 40 generations to the original canoe that brought their ancestors to Aotearoa (New Zealand).\n\nWhen two strangers meet, they share genealogies to find their connection. Everyone is related if you go back far enough.",
            "The Real Tradition": "The Kumulipo is a Hawaiian creation chant of 2,102 lines that traces the genealogy of the Hawaiian royal family back to the creation of the universe — from coral polyps through fish, birds, and gods to human chiefs. Queen Lili'uokalani translated it into English in 1897. It's both a creation myth AND a royal genealogy AND a scientific taxonomy, all in one epic chant.",
            "Film Connection": "The song 'We Know the Way' in Moana is essentially a genealogy chant — it traces the voyaging heritage of Moana's people across generations. When Moana's grandmother tells her 'You know who you are,' she's invoking the power of genealogical knowledge: knowing your ancestors means knowing yourself.",
            "Reflection": "How far back can you trace your family? Ask a grandparent or elder to tell you about THEIR grandparents. Every family has a story — you just have to ask!"
        },
        "keywords": ["genealogy", "whakapapa", "chanting", "kumulipo", "ancestors", "identity"]
    },
    # --- ECOLOGY & RELATIONSHIP ---
    {
        "id": "coral-reef-village",
        "name": "The Reef Is a Village Too",
        "category": "ecology-and-relationship",
        "sections": {
            "Story": "Polynesian people didn't just live NEAR the ocean — they lived WITH it. The coral reef around an island wasn't just a place to catch fish; it was a whole community of beings that needed care and respect.\n\nDifferent fish belonged to different families. Certain areas of reef were tapu (off-limits) at certain times of year so fish could breed. Master fishermen knew every coral head, every cave, every current. They could tell what fish were present by the color of the water or the behavior of birds overhead.\n\nTaking too many fish from one area wasn't just bad practice — it was an insult to Tangaroa, the ocean ancestor. Overfishing could make the ocean angry and send storms.",
            "The Real Tradition": "The Hawaiian ahupua'a system divided land into pie-slice shaped districts running from mountain to sea. Each ahupua'a was managed as a complete ecosystem — forest, farmland, fishpond, reef, and open ocean. The konohiki (land manager) set fishing seasons and catch limits. This 800-year-old system is now studied as a model for modern sustainable resource management.",
            "Film Connection": "Motunui island in Moana has a reef that protects it — and a rule against going beyond it. The dying reef and empty fish traps that drive the plot reflect real ecological concerns: when the relationship between people and ocean breaks down, both suffer.",
            "Reflection": "The ahupua'a system meant that everyone from the mountaintop to the reef was responsible for each other. What would your neighborhood look like if everyone took care of it like that?"
        },
        "keywords": ["reef", "ahupuaa", "ecology", "conservation", "tangaroa", "sustainability"]
    },
    {
        "id": "taro-and-coconut",
        "name": "Taro and Coconut: Food as Family",
        "category": "ecology-and-relationship",
        "sections": {
            "Story": "In Hawaiian mythology, taro (kalo) isn't just food — it's your OLDER BROTHER.\n\nThe story goes like this: the sky father Wākea and the earth mother Papa had a first child who was stillborn. They buried the baby, and from its body grew the first taro plant. Their second child was the first human being. So taro is the elder sibling of all humanity — and you take care of your elders.\n\nCoconut has its own origin story: a young eel (who was really a god) loved a woman. When he was killed, he told her to bury his head. From it grew the first coconut palm — and that's why coconuts have two eyes and a mouth, like the eel god's face.\n\nEvery food plant has a story that connects it to the divine.",
            "The Real Tradition": "Hāloa (meaning 'long breath' or 'long stem') is the name of both the first taro plant and the first human in Hawaiian creation stories. Taro cultivation requires constant flowing water (lo'i kalo), and Hawaiian taro farming is one of the most sophisticated agricultural systems in the Pacific. Today, taro farming revival is central to Hawaiian cultural renaissance.",
            "Film Connection": "Moana's island Motunui is shown with taro patches and coconut groves — the two most important Polynesian food crops. The coconut is everywhere in the film (including the Kakamora coconut pirates!). When the crops start dying, it signals the deeper spiritual crisis.",
            "Reflection": "Imagine if your food was your relative! Would you eat differently? Would you waste less? Polynesian people say a prayer of thanks before eating because the food gave its life for you."
        },
        "keywords": ["taro", "coconut", "haloa", "agriculture", "sacred-food", "kinship"]
    },
    {
        "id": "tattoo-as-story",
        "name": "Tatau: Your Life Story Written on Your Skin",
        "category": "ecology-and-relationship",
        "sections": {
            "Story": "The word 'tattoo' comes from the Polynesian word 'tatau.' It was invented in the Pacific Islands, and it meant something completely different from modern tattoos.\n\nA Polynesian tattoo tells your story: where you're from, who your family is, what you've accomplished, and your role in the community. A Samoan pe'a (men's tattoo from waist to knee) takes weeks of incredibly painful sessions and is a rite of passage into adulthood. Getting it shows courage; leaving it unfinished is one of the worst shames possible.\n\nEvery symbol has meaning: ocean waves, shark teeth, spear points, turtles, the sun. A master tattoo artist (tufuga tā tatau) isn't just an artist — they're a historian, writing living documents on human skin.",
            "The Real Tradition": "Polynesian tattooing is one of the world's oldest continuous art traditions. Māori tā moko (face tattoos) are considered so personal they serve as signatures on legal documents. In 2023, UNESCO recognized Samoan tatau as an Intangible Cultural Heritage. The tools are traditional: bone combs, wooden mallets, and plant-based ink. Machine tattooing is considered inauthentic.",
            "Film Connection": "Māui's tattoos in Moana are ALIVE — they move and tell his story! This is based on the real tradition where tattoos record a person's deeds. The animated Mini-Māui tattoo character is a playful take on the idea that your tattoo IS your autobiography.",
            "Reflection": "If you were going to put your life story on your skin in symbols, what three symbols would you choose? What do they mean about who you are?"
        },
        "keywords": ["tattoo", "tatau", "pe-a", "ta-moko", "identity", "rite-of-passage"]
    },
]

for item in maui_items:
    sort += 1
    item["sort_order"] = sort
    item["level"] = 1
    items.append(item)

# =============================================================================
# L2 EMERGENCE — THEMATIC GROUPS
# =============================================================================

l2_items = [
    {
        "id": "theme-maui-legends",
        "name": "The Adventures of Māui — Demigod of the Pacific",
        "category": "theme-collections",
        "level": 2,
        "composite_of": ["maui-born-of-ocean", "maui-slows-the-sun", "maui-fishes-up-islands", "maui-steals-fire", "maui-and-death"],
        "relationship_type": "emergence",
        "sections": {
            "About": "Māui is the great hero of Polynesian mythology — a trickster demigod who slowed the sun, fished up islands from the ocean floor, stole fire from the underworld, and died trying to defeat death itself. His stories are told across every Polynesian culture from New Zealand to Hawai'i, with local variations that reflect each island's identity. He's not a distant god on a mountaintop; he's messy, tricky, brave, and very human.",
            "For Parents": "The Māui cycle is perfect for children who feel small or underestimated — Māui was literally the rejected runt who became the greatest hero. Each story also models a different kind of courage: physical (lassoing the sun), intellectual (tricking Mahuika), and the ultimate acceptance of mortality. The death myth is intense but profoundly important for conversations about mortality with older children.",
            "Cultural Note": "Māui is a living cultural figure, not just a character. Treat these stories with respect and use them as invitations to learn more about the specific Pacific Island cultures they come from."
        },
        "keywords": ["maui", "demigod", "trickster", "hero-cycle", "polynesian"]
    },
    {
        "id": "theme-wayfinding",
        "name": "Finding the Way — Polynesian Navigation",
        "category": "theme-collections",
        "level": 2,
        "composite_of": ["star-compass", "reading-waves", "voyaging-canoe", "bird-signs"],
        "relationship_type": "emergence",
        "sections": {
            "About": "Polynesian wayfinding is one of humanity's greatest intellectual achievements. Without instruments, writing, or metal tools, Pacific Islanders navigated millions of square miles of open ocean using stars, waves, birds, clouds, and deep embodied knowledge. They settled every habitable island in the Pacific — from Madagascar to Easter Island, from Hawai'i to New Zealand — in the greatest migration in human history.",
            "For Parents": "These stories naturally lead to STEM conversations: astronomy, oceanography, ecology, and engineering are all embedded in wayfinding traditions. But they also challenge the assumption that 'real science' requires instruments and laboratories. Polynesian navigation is empirical, rigorous, and more accurate than European navigation was until the 18th century.",
            "Try This": "On a clear night, go outside and find Polaris (North Star) or a bright constellation. Imagine navigating a canoe using only that star. Which direction is your home from where you're standing?"
        },
        "keywords": ["navigation", "wayfinding", "stars", "ocean", "science"]
    },
    {
        "id": "theme-animism",
        "name": "Everything Is Alive — Oceanic Animism",
        "category": "theme-collections",
        "level": 2,
        "composite_of": ["ocean-as-ancestor", "te-fiti-and-te-ka", "mana-and-tapu", "shapeshifting"],
        "relationship_type": "emergence",
        "sections": {
            "About": "In Polynesian worldview, the ocean is a person, the land is a mother, fire is a grandmother, and your family tree includes sharks, owls, and taro plants. This isn't 'primitive belief' — it's a sophisticated relational framework where everything exists in kinship networks. Mana (spiritual power) and tapu (sacred restriction) create an ethical system that governs relationships between humans, nature, and the divine.",
            "For Parents": "Oceanic animism offers children an alternative to the Western subject-object divide that separates humans from nature. These aren't fairy tales about talking animals; they're a worldview where taking care of the ocean ISN'T just environmentalism — it's taking care of family. This perspective is increasingly relevant in climate conversations.",
            "Key Concept": "Animism doesn't mean 'believing rocks have feelings.' It means living in a world where relationships — not objects — are the fundamental reality. A rock at a sacred site has mana not because it's magic, but because of all the relationships (ceremonies, stories, ancestors) that flow through it."
        },
        "keywords": ["animism", "mana", "tapu", "kinship", "worldview"]
    },
    {
        "id": "theme-music-performance",
        "name": "The Living Library — Music, Dance, and Memory",
        "category": "theme-collections",
        "level": 2,
        "composite_of": ["hula-as-library", "pate-and-log-drums", "chanting-genealogy"],
        "relationship_type": "emergence",
        "sections": {
            "About": "In cultures without writing, music and dance ARE the library, the law books, the science journals, and the family records. Polynesian performing arts encode everything from navigation routes to genealogies to ecological knowledge in forms that can be memorized, performed, and passed down for generations. Every gesture in hula, every rhythm on a log drum, every line in a genealogy chant carries specific information.",
            "For Parents": "These traditions challenge the assumption that 'real knowledge' must be written down. Children who struggle with reading may find it empowering to learn about cultures where knowledge lived in song, dance, and rhythm. Try learning a simple genealogy chant together — even four generations back is impressive!",
            "Activity": "As a family, create a short chant about your own history: where grandparents came from, what they did, how the family arrived where you live now. Add a rhythm (clapping, drumming on a table). Congratulations — you've just done what Polynesian families have done for thousands of years!"
        },
        "keywords": ["music", "dance", "oral-tradition", "hula", "chanting", "memory"]
    },
    {
        "id": "theme-ecology",
        "name": "Relatives, Not Resources — Polynesian Ecology",
        "category": "theme-collections",
        "level": 2,
        "composite_of": ["coral-reef-village", "taro-and-coconut", "tattoo-as-story"],
        "relationship_type": "emergence",
        "sections": {
            "About": "Polynesian ecology doesn't separate 'nature' from 'culture.' Taro is an older brother. The reef is a village. Coconut palms grew from a god's head. When your food and your ecosystem are your relatives, sustainability isn't an abstract concept — it's family obligation. The ahupua'a system, tattoo traditions, and food origin stories all encode the same message: you belong to the land; the land doesn't belong to you.",
            "For Parents": "These stories naturally lead to conversations about sustainability, food waste, and environmental stewardship. But they go deeper than 'take care of the planet' — they ask children to reimagine their RELATIONSHIP with the natural world. Try saying grace before a meal that thanks the actual plants and animals, not just a distant deity.",
            "For Educators": "The ahupua'a system is a ready-made unit on watershed management, ecosystem services, and indigenous resource management. The tattoo tradition connects to identity, art, and cultural preservation. These aren't supplementary 'cultural' topics — they're rigorous ecological and social science."
        },
        "keywords": ["ecology", "sustainability", "ahupuaa", "kinship", "food", "land"]
    },
]

for item in l2_items:
    sort += 1
    item["sort_order"] = sort
    items.append(item)

# =============================================================================
# L3 META-EMERGENCE
# =============================================================================

l3_items = [
    {
        "id": "meta-ocean-people",
        "name": "We Are Ocean People — The Heart of Polynesian Culture",
        "category": "meta",
        "level": 3,
        "composite_of": ["theme-maui-legends", "theme-wayfinding", "theme-animism", "theme-music-performance", "theme-ecology"],
        "relationship_type": "emergence",
        "sections": {
            "About": "Polynesian culture is oceanic at every level: the myths are about sea gods and island-fishing, the science is wave-reading and star-navigation, the music is rhythm-driven like surf, the ecology is reef-centered, and identity itself is inseparable from the voyaging canoe. To understand any part, you must understand that the ocean isn't a barrier between islands — it's the highway that connects them all. Polynesians don't live on islands in the sea; they live in the sea with islands.",
            "The Big Idea": "Epeli Hau'ofa, the great Tongan writer, said the Pacific Islands aren't 'small islands in a far sea' — they're 'a sea of islands,' connected by the ocean that Western maps show as empty space. The ocean doesn't separate; it JOINS. This is the deepest truth Moana teaches, and it comes from real Pacific Island philosophy.",
            "Why This Matters Now": "In an era of climate change, rising seas, and environmental crisis, Polynesian ocean-centered wisdom offers something the industrial world desperately needs: a way of relating to water, land, and weather as relatives rather than resources. The same navigational intelligence that crossed the Pacific can help navigate the storms ahead."
        },
        "keywords": ["polynesia", "ocean", "identity", "philosophy", "hauofa", "connection"]
    }
]

for item in l3_items:
    sort += 1
    item["sort_order"] = sort
    items.append(item)

grammar["items"] = items

# Write output
outdir = os.path.join(os.path.dirname(__file__), "..", "grammars", "roots-of-moana")
os.makedirs(outdir, exist_ok=True)
outpath = os.path.join(outdir, "grammar.json")

with open(outpath, "w") as f:
    json.dump(grammar, f, indent=2, ensure_ascii=False)

print(f"Wrote {len(items)} items to {outpath}")
print(f"  L1: {sum(1 for i in items if i['level'] == 1)}")
print(f"  L2: {sum(1 for i in items if i['level'] == 2)}")
print(f"  L3: {sum(1 for i in items if i['level'] == 3)}")
