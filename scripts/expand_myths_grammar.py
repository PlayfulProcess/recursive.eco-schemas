#!/usr/bin/env python3
"""
Expand Myths Through Many Eyes grammar:
1. Add `grammars` links (GitHub URLs) to all existing items
2. Add astrology metadata (planets, signs) to all myth items
3. Add 12 new L1 myths to expand from 31→43 myths
4. Update threads, cultures, meta cards
5. Recalculate sort_orders
"""
import json

BASE = "https://github.com/PlayfulProcess/recursive.eco-schemas/tree/main/grammars/"

with open("grammars/myths-through-many-eyes/grammar.json") as f:
    g = json.load(f)

items = g["items"]

# ═══════════════════════════════════════════════════════════════════════════
# 1. GRAMMARS LINKS + ASTROLOGY METADATA FOR EXISTING ITEMS
# ═══════════════════════════════════════════════════════════════════════════

# Map item IDs → source grammar folder names (only existing grammars)
grammar_links = {
    # --- MYTHS ---
    "myth-prometheus": ["greek-mythology", "bulfinch-s-classical-mythology"],
    "myth-persephone": ["greek-mythology", "bulfinch-s-classical-mythology"],
    "myth-psyche-eros": ["bulfinch-s-classical-mythology", "metamorphoses-ovid"],
    "myth-orpheus": ["metamorphoses-ovid", "greek-mythology", "bulfinch-s-classical-mythology"],
    "myth-theseus-minotaur": ["greek-mythology", "bulfinch-s-classical-mythology"],
    "myth-narcissus": ["metamorphoses-ovid", "bulfinch-s-classical-mythology"],
    "myth-osiris-isis": ["egyptian-mythology"],
    "myth-weighing-heart": ["egyptian-mythology"],
    "myth-inanna": [],  # will link when myths-babylonia-assyria is built
    "myth-gilgamesh": [],  # same
    "myth-odin-yggdrasil": ["prose-edda"],
    "myth-ragnarok": ["prose-edda"],
    "myth-fisher-king": [],  # mabinogion not built yet
    "myth-taliesin": [],  # mabinogion not built yet
    "myth-krishna-arjuna": ["bhagavad-gita", "mahabharata"],
    "myth-churning-ocean": ["mahabharata"],
    "myth-buddha-bodhi": ["gospel-of-buddha"],
    "myth-sophia-fall": [],  # pistis-sophia not built yet
    "myth-flood": ["prose-edda", "popol-vuh"],
    "myth-creation-chaos": ["prose-edda"],
    "myth-alchemical-wedding": [],  # hidden-symbolism-alchemy not built yet
    "myth-hero-twins": ["popol-vuh"],
    "myth-sun-wukong": [],  # journey to the west not available
    "myth-izanagi-izanami": ["japanese-fairy-tales"],
    "myth-raven-steals-light": ["folklore-north-american-indian", "myths-north-american-indians"],
    "myth-vasalisa-baba-yaga": [],  # russian-folk-tales not built yet
    "myth-skeleton-woman": [],  # oral tradition, no text source
    "myth-anansi": ["west-african-folk-tales"],
    "myth-scheherazade": [],  # arabian-nights not built yet
    "myth-seal-wife": ["celtic-fairy-tales"],
    "myth-bluebeard": ["grimms-fairy-tales"],
    # --- INTERPRETERS ---
    "interp-jung": ["jungian-archetypes"],
    "interp-campbell": [],  # Hero with 1000 Faces under copyright
    "interp-rank": [],  # myth-birth-hero-rank not built yet
    "interp-frazer": ["golden-bough"],
    "interp-alchemists": [],  # hidden-symbolism-alchemy not built yet
    "interp-neumann": [],  # under copyright
    "interp-hillman": [],  # under copyright
    "interp-eliade": [],  # under copyright
    "interp-shrei": [],  # podcast, copyrighted
    "interp-akomolafe": [],  # under copyright
    "interp-shaw": [],  # under copyright
    "interp-estes": [],  # under copyright
    "interp-warner": [],  # under copyright
    # --- THREADS ---
    "thread-descent": ["greek-mythology", "egyptian-mythology", "prose-edda", "popol-vuh"],
    "thread-dying-god": ["egyptian-mythology", "prose-edda", "bhagavad-gita"],
    "thread-sacred-marriage": ["metamorphoses-ovid", "egyptian-mythology", "mahabharata"],
    "thread-dragon-fight": ["greek-mythology", "prose-edda", "bhagavad-gita"],
    "thread-trickster": ["folklore-north-american-indian", "west-african-folk-tales"],
    "thread-great-mother": ["greek-mythology", "egyptian-mythology"],
    "thread-flood-renewal": ["prose-edda", "popol-vuh", "bhagavad-gita"],
    "thread-stolen-light": ["folklore-north-american-indian", "metamorphoses-ovid"],
    # --- CULTURES ---
    "culture-greek": ["greek-mythology", "bulfinch-s-classical-mythology", "metamorphoses-ovid"],
    "culture-egyptian-mesopotamian": ["egyptian-mythology", "mahabharata"],
    "culture-northern": ["prose-edda", "celtic-fairy-tales", "kalevala"],
    "culture-eastern": ["bhagavad-gita", "mahabharata", "gospel-of-buddha", "japanese-fairy-tales"],
    "culture-african-arabian": ["west-african-folk-tales", "folklore-north-american-indian"],
    # --- META ---
    "meta-monomyth": ["golden-bough", "jungian-archetypes"],
    "meta-collective-unconscious": ["jungian-archetypes", "golden-bough"],
    "meta-living-symbol": ["jungian-archetypes"],
}

# Astrology metadata for myths
astrology_map = {
    "myth-prometheus": {"planets": ["Uranus"], "signs": ["Aquarius"], "themes": ["rebellion", "awakening", "stolen-fire"]},
    "myth-persephone": {"planets": ["Pluto", "Moon"], "signs": ["Scorpio", "Cancer"], "themes": ["descent", "abduction", "seasonal-return"]},
    "myth-psyche-eros": {"planets": ["Venus", "Pluto"], "signs": ["Libra", "Scorpio"], "themes": ["love-ordeal", "soul-desire", "sacred-marriage"]},
    "myth-orpheus": {"planets": ["Neptune", "Venus"], "signs": ["Pisces", "Libra"], "themes": ["music", "grief", "the-veil"]},
    "myth-theseus-minotaur": {"planets": ["Mars", "Sun"], "signs": ["Aries", "Leo"], "themes": ["labyrinth", "courage", "shadow-confrontation"]},
    "myth-narcissus": {"planets": ["Neptune", "Venus"], "signs": ["Pisces", "Libra"], "themes": ["reflection", "self-image", "dissolution"]},
    "myth-osiris-isis": {"planets": ["Pluto", "Saturn"], "signs": ["Scorpio", "Capricorn"], "themes": ["death-rebirth", "dismemberment", "resurrection"]},
    "myth-weighing-heart": {"planets": ["Saturn", "Jupiter"], "signs": ["Libra", "Capricorn"], "themes": ["judgment", "truth", "cosmic-justice"]},
    "myth-inanna": {"planets": ["Venus", "Pluto"], "signs": ["Taurus", "Scorpio"], "themes": ["descent-of-venus", "stripping", "underworld-queen"]},
    "myth-gilgamesh": {"planets": ["Saturn", "Mars"], "signs": ["Capricorn", "Aries"], "themes": ["mortality", "friendship", "failed-immortality"]},
    "myth-odin-yggdrasil": {"planets": ["Mercury", "Jupiter", "Pluto"], "signs": ["Scorpio", "Sagittarius"], "themes": ["sacrifice-for-wisdom", "world-tree", "runes"]},
    "myth-ragnarok": {"planets": ["Pluto", "Uranus"], "signs": ["Scorpio", "Aquarius"], "themes": ["apocalypse", "renewal", "twilight-of-gods"]},
    "myth-fisher-king": {"planets": ["Chiron", "Saturn"], "signs": ["Virgo", "Pisces"], "themes": ["wound", "wasteland", "grail"]},
    "myth-taliesin": {"planets": ["Mercury", "Moon"], "signs": ["Gemini", "Cancer"], "themes": ["shapeshifting", "poetic-inspiration", "cauldron"]},
    "myth-krishna-arjuna": {"planets": ["Jupiter", "Sun"], "signs": ["Sagittarius", "Leo"], "themes": ["dharma", "cosmic-vision", "duty"]},
    "myth-churning-ocean": {"planets": ["Saturn", "Jupiter"], "signs": ["Capricorn", "Sagittarius"], "themes": ["cooperation-of-opposites", "poison-before-nectar", "cosmic-effort"]},
    "myth-buddha-bodhi": {"planets": ["Saturn", "Neptune"], "signs": ["Capricorn", "Pisces"], "themes": ["renunciation", "enlightenment", "still-sitting"]},
    "myth-sophia-fall": {"planets": ["Moon", "Neptune"], "signs": ["Pisces", "Cancer"], "themes": ["divine-feminine-in-exile", "spark-in-matter", "gnosis"]},
    "myth-flood": {"planets": ["Neptune", "Pluto"], "signs": ["Pisces", "Scorpio"], "themes": ["dissolution", "purification", "ark"]},
    "myth-creation-chaos": {"planets": ["Saturn", "Pluto"], "signs": ["Capricorn", "Scorpio"], "themes": ["primordial-sacrifice", "form-from-formless", "cosmic-egg"]},
    "myth-alchemical-wedding": {"planets": ["Sun", "Moon"], "signs": ["Leo", "Cancer"], "themes": ["coniunctio", "opposites-united", "philosophers-stone"]},
    "myth-hero-twins": {"planets": ["Mars", "Mercury"], "signs": ["Gemini", "Aries"], "themes": ["twin-journey", "underworld-trickery", "ball-game"]},
    "myth-sun-wukong": {"planets": ["Mars", "Mercury", "Jupiter"], "signs": ["Aries", "Gemini", "Sagittarius"], "themes": ["rebellion", "trickster-journey", "submission-to-dharma"]},
    "myth-izanagi-izanami": {"planets": ["Sun", "Moon"], "signs": ["Cancer", "Scorpio"], "themes": ["divine-couple", "creation-death", "taboo-of-looking"]},
    "myth-raven-steals-light": {"planets": ["Mercury", "Uranus"], "signs": ["Gemini", "Aquarius"], "themes": ["trickster-theft", "light-liberation", "appetite-as-gift"]},
    "myth-vasalisa-baba-yaga": {"planets": ["Moon", "Pluto"], "signs": ["Cancer", "Scorpio"], "themes": ["feminine-initiation", "dark-mother", "intuition-doll"]},
    "myth-skeleton-woman": {"planets": ["Pluto", "Moon"], "signs": ["Scorpio", "Cancer"], "themes": ["life-death-life", "love-beyond-death", "bones"]},
    "myth-anansi": {"planets": ["Mercury", "Uranus"], "signs": ["Gemini", "Aquarius"], "themes": ["trickster-liberation", "stories-as-wealth", "cunning"]},
    "myth-scheherazade": {"planets": ["Mercury", "Moon"], "signs": ["Gemini", "Cancer"], "themes": ["narrative-survival", "feminine-cunning", "healing-through-story"]},
    "myth-seal-wife": {"planets": ["Neptune", "Moon"], "signs": ["Pisces", "Cancer"], "themes": ["wild-nature-captured", "longing", "return-to-sea"]},
    "myth-bluebeard": {"planets": ["Pluto", "Mars"], "signs": ["Scorpio", "Aries"], "themes": ["forbidden-knowledge", "predator", "curiosity-as-weapon"]},
}

# Apply grammars links and astrology to existing items
for item in items:
    iid = item["id"]
    # Grammars links
    if iid in grammar_links and grammar_links[iid]:
        item["grammars"] = [BASE + name for name in grammar_links[iid]]
    # Astrology metadata
    if iid in astrology_map:
        if "metadata" not in item:
            item["metadata"] = {}
        item["metadata"]["astrology"] = astrology_map[iid]


# ═══════════════════════════════════════════════════════════════════════════
# 2. TWELVE NEW L1 MYTHS
# ═══════════════════════════════════════════════════════════════════════════

new_myths = [
    {
        "id": "myth-dionysus",
        "name": "Dionysus: The God Who Dies and Returns",
        "sort_order": 0,
        "category": "myths",
        "level": 1,
        "sections": {
            "The Story": "Born of Zeus and a mortal woman, Semele, who was tricked by jealous Hera into demanding to see Zeus in his true form — and was incinerated by the sight. Zeus snatched the unborn child from her womb and sewed him into his own thigh until he was ready to be born. Dionysus grew up in secret, raised by nymphs, already showing his power: wine flowed from the ground where he walked, ivy grew from his thyrsus, and animals came wild-eyed to follow him. But the Titans — ancient enemies of the Olympians — tore the infant god to pieces and devoured him. Only his heart survived, from which he was reborn. Grown to godhood, Dionysus traveled the world with his wild procession — maenads, satyrs, panthers — teaching the vine and the ecstatic rites. Those who accepted him found liberation and joy. Those who resisted — King Pentheus of Thebes, who tried to imprison him — were torn apart by the god's own followers, by their own mothers made mad with divine frenzy.",
            "Source": "Euripides, The Bacchae (405 BCE). Ovid, Metamorphoses. Hesiod, Theogony. Orphic Hymns. Nonnus, Dionysiaca. Public domain translations available from multiple sources.",
            "The Images": "The twice-born god — birth from the thigh of the father, resurrection from the heart after dismemberment. The vine — the plant that transforms (grape to wine, consciousness to ecstasy). The mask — Dionysus is the god of theater, the one who wears faces. The maenad — the woman set free from social constraint, terrifying and holy. The sparagmos — the tearing apart of the god (and of the resistant king), the necessary destruction that precedes new life. The thyrsus — a fennel stalk tipped with pine cone, phallic and vegetal, the wild made into a scepter.",
            "Culture": "Greek. Dionysus is the most dangerous god in the Greek pantheon — not because he is evil but because he dissolves boundaries: between human and animal, civilization and wildness, sobriety and ecstasy, life and death. Nietzsche made him the pole opposite Apollo: where Apollo orders, Dionysus dissolves. Campbell saw him as the quintessential dying god of the Mediterranean. Jung saw the Dionysian as the return of the repressed — what happens when a civilization denies its irrational depths."
        },
        "keywords": ["dionysus", "wine", "ecstasy", "dismemberment", "rebirth", "maenads", "greek"],
        "metadata": {
            "origin": "Greek",
            "astrology": {"planets": ["Neptune", "Pluto"], "signs": ["Pisces", "Scorpio"], "themes": ["ecstasy", "dissolution", "divine-madness"]}
        },
        "grammars": [BASE + "greek-mythology", BASE + "metamorphoses-ovid", BASE + "bulfinch-s-classical-mythology"]
    },
    {
        "id": "myth-medusa",
        "name": "Medusa: The Gaze That Turns to Stone",
        "sort_order": 0,
        "category": "myths",
        "level": 1,
        "sections": {
            "The Story": "In the oldest telling, Medusa was not always a monster. She was a beautiful priestess of Athena, ravished by Poseidon in Athena's own temple. The goddess, furious — not at Poseidon but at Medusa — transformed her: her hair became writhing serpents, her gaze turned any living thing to stone, and she was banished to a cave at the edge of the world with her two Gorgon sisters. There she lived in exile until Perseus came. Armed with gifts from the gods — Athena's polished shield, Hermes' winged sandals, Hades' cap of invisibility — he approached the sleeping Medusa backward, watching her reflection in the mirror-shield, and cut off her head with a sickle. From her severed neck sprang two beings: Pegasus the winged horse and Chrysaor the golden warrior — children of Poseidon, long trapped in her monstrous body. Perseus carried the head as a weapon, turning his enemies to stone, before giving it to Athena, who mounted it on her shield — the aegis.",
            "Source": "Hesiod, Theogony. Ovid, Metamorphoses IV. Pindar, Pythian Ode XII. Apollodorus, Bibliotheca. Multiple public domain translations.",
            "The Images": "The Gorgon face — the apotropaic image, placed on shields and temples to ward off evil, the face so terrible it protects. The snakes — the chthonic feminine, the wisdom of the body, the power that moves without legs. The mirror-shield — the only way to face what cannot be faced directly. The petrifying gaze — the trauma that freezes. The severed head that still works — rage does not die when you cut it off. Pegasus from the neck — beauty and freedom born from the wound.",
            "Culture": "Greek. Medusa is perhaps the most reinterpreted figure in world mythology. The classical reading: the hero slays the monster. The feminist reading (Cixous, Estés, Warner): a rape victim is punished instead of the rapist, her rage is called monstrous, and she is killed by a man who cannot even look at her directly. The Jungian reading: the Medusa is the Terrible Mother, the aspect of the feminine that petrifies the ego. The deepest reading: Medusa is the face of the real — the thing that cannot be looked at directly and must be seen in reflection. Every mirror is her shield."
        },
        "keywords": ["medusa", "gorgon", "gaze", "stone", "serpent", "feminine-rage", "mirror"],
        "metadata": {
            "origin": "Greek",
            "astrology": {"planets": ["Pluto", "Moon"], "signs": ["Scorpio", "Cancer"], "themes": ["feminine-rage", "petrification", "transformation-through-horror"]}
        },
        "grammars": [BASE + "greek-mythology", BASE + "metamorphoses-ovid", BASE + "bulfinch-s-classical-mythology"]
    },
    {
        "id": "myth-circe",
        "name": "Circe: The Witch Who Transforms",
        "sort_order": 0,
        "category": "myths",
        "level": 1,
        "sections": {
            "The Story": "On the island of Aeaea, surrounded by wolves and lions who were once men, lives Circe — daughter of the sun god Helios and the ocean nymph Perse, aunt of Medea, sister of the sorcerer king Aeëtes. When Odysseus's sailors arrive on her shore, she welcomes them warmly — feasts them, gives them wine laced with honey and cheese. Then she touches them with her wand, and they become pigs: their bodies swinish, their minds still human, weeping in pig-form. Odysseus, warned by Hermes and armed with the herb moly, resists the transformation. When Circe's wand fails against him, she is shocked — then admiring. He demands she restore his men. She does. He stays a year — not as her prisoner but as her lover and student. She teaches him what he cannot learn from battle: how to speak with the dead, how to navigate by the underworld, how to listen. When he finally leaves, she gives him the knowledge that will get him home.",
            "Source": "Homer, Odyssey X-XII. Ovid, Metamorphoses XIV. Apollonius Rhodius, Argonautica. Public domain translations by Fagles, Butler, Lattimore, and others.",
            "The Images": "The potion — the substance that reveals your true nature (the brutish become beasts). The wand — the power to transform, wielded by a woman. The moly — the divine protection that lets you face the witch without being changed. The year of staying — not conquest but dwelling, the hero who stops. The pigs — what men become when they feed without consciousness. The teaching — the knowledge that comes not from questing but from the feminine, the magical, the still.",
            "Culture": "Greek. Circe has been read as villain (the seductress who degrades men), as warning (the dangerous feminine), and — increasingly — as teacher. Warner reads her as the powerful woman the patriarchal imagination can only understand as a witch. Hillman sees her island as a station of the soul's journey where the heroic ego must be undone. The transformation of men into pigs is not arbitrary cruelty — it is revelation: she shows them what they already are. Only the one who can resist (Odysseus, with divine help) earns the right to receive her teaching."
        },
        "keywords": ["circe", "witch", "transformation", "pigs", "odysseus", "magic", "feminine-power"],
        "metadata": {
            "origin": "Greek",
            "astrology": {"planets": ["Pluto", "Neptune", "Moon"], "signs": ["Scorpio", "Pisces"], "themes": ["transformation", "sorcery", "feminine-knowledge"]}
        },
        "grammars": [BASE + "greek-mythology", BASE + "bulfinch-s-classical-mythology"]
    },
    {
        "id": "myth-amaterasu",
        "name": "Amaterasu Hides in the Cave",
        "sort_order": 0,
        "category": "myths",
        "level": 1,
        "sections": {
            "The Story": "Amaterasu, the sun goddess, ruler of the High Plain of Heaven, had a brother — Susanoo, the storm god, wild and destructive. After a series of outrages — he destroyed her rice paddies, defecated in her palace, hurled a flayed horse through the roof of her weaving hall, killing one of her maidens — Amaterasu withdrew. She sealed herself inside the Rock Cave of Heaven and barred the door. The world went dark. Without the sun, nothing grew. Evil spirits multiplied. The eight hundred gods gathered in panic. They tried everything: roosters crowing, offerings, prayers. Nothing worked. Then Ame-no-Uzume, the goddess of dawn and mirth, overturned a tub before the cave, climbed on top, and began to dance. She pulled open her robes, exposed herself, and danced with wild abandon. The gods erupted in laughter — eight hundred divine beings roaring with mirth in the darkness. Amaterasu, bewildered that anyone could laugh while the world was dark, cracked the door to look. The gods had placed a mirror outside. She saw her own radiance reflected back. As she reached toward it, a strong god pulled her out. They sealed the cave. Light returned to the world.",
            "Source": "Kojiki (Record of Ancient Matters, 712 CE), translated by Basil Hall Chamberlain (1882, public domain). Nihon Shoki (Chronicles of Japan, 720 CE). Both are foundational texts of Shinto mythology.",
            "The Images": "The cave — the withdrawal of life-force, the depression of the divine. The darkness — what happens when the creative feminine retreats. The obscene dance — joy and body as the cure for despair, laughter in the dark. The mirror — you cannot know your own light until it is reflected back. The crack in the door — curiosity, the first movement of return. The eight hundred laughing gods — community as therapy, joy as a lure more powerful than duty.",
            "Culture": "Japanese (Shinto). This is the only major sun-withdrawal myth in which the sun is female and the solution is not heroic battle but comedy and eros. Amaterasu is not rescued — she rescues herself, drawn out by curiosity and the reflection of her own beauty. Eliade saw this as the archetypal myth of the sun's annual return; Shaw reads it as the ecology of depression and recovery; Campbell noted its structural similarity to Demeter's mourning but with a radically different resolution — not grief satisfied but laughter provoked."
        },
        "keywords": ["amaterasu", "sun-goddess", "cave", "withdrawal", "laughter", "mirror", "japanese"],
        "metadata": {
            "origin": "Japanese",
            "astrology": {"planets": ["Sun", "Moon"], "signs": ["Leo", "Cancer"], "themes": ["light-withdrawal", "divine-feminine-sun", "joy-as-medicine"]}
        },
        "grammars": [BASE + "japanese-fairy-tales"]
    },
    {
        "id": "myth-sedna",
        "name": "Sedna: Mother of the Sea",
        "sort_order": 0,
        "category": "myths",
        "level": 1,
        "sections": {
            "The Story": "Sedna was a girl who refused to marry. Every suitor her father brought, she rejected. Finally a mysterious stranger appeared — handsome, wearing fine furs — and she went with him. Across the water, she discovered he was not human but a bird-spirit, a fulmar in disguise, and his fine home was a nest of fish skins and feathers on a barren rock. She wept. When her father came to rescue her in his kayak, the bird-spirit raised a terrible storm. Terrified for his own life, the father threw Sedna overboard to appease the spirit. She clung to the gunwale. He chopped off her fingers, joint by joint. The first joints became seals. The second joints became walruses. The third became whales. Sedna sank to the bottom of the sea, where she became Nuliajuk, Mother of the Sea Beasts, ruler of the ocean floor. All the animals that feed the Inuit come from her mutilated hands. When humans violate taboos — waste meat, mistreat animals, break sacred rules — Sedna's hair becomes tangled with filth, and she withholds the animals. The shaman must journey to the sea floor, comb her hair, and soothe her rage before the animals return.",
            "Source": "Collected from Central Inuit (Baffin Island, Igloolik) communities by Franz Boas (1888), Knud Rasmussen (1929), and others. Multiple variants across the Arctic. Public domain ethnographic sources.",
            "The Images": "The refusal to marry — the autonomous feminine that will not be domesticated on terms set by others. The bird-husband — the wrong marriage, the deception of beauty. The father's betrayal — the one who should protect you is the one who sacrifices you. The severed fingers — mutilation that becomes creation, the wound that generates all life. The sea floor — the deepest unconscious, where the source of nourishment lives. The tangled hair — ecological sin made visible. The shaman's comb — the ritual act that restores relationship between human and more-than-human.",
            "Culture": "Inuit (Central Arctic). Sedna is the most important deity in Inuit religion — the one on whom all life depends. Her story is not a hero myth but an origin-of-suffering myth: everything that feeds us comes from a wound, an original betrayal. Shaw reads her as the ultimate ecological teaching — the animals are gifts from a wounded goddess, and if we dishonor the gift, she withholds it. Estés would recognize the mutilated feminine whose suffering generates life. Akomolafe might see the tangled hair as the world's refusal to be managed by human convenience."
        },
        "keywords": ["sedna", "sea-mother", "fingers", "seals", "shaman", "arctic", "ecological"],
        "metadata": {
            "origin": "Inuit (Central Arctic)",
            "astrology": {"planets": ["Neptune", "Pluto", "Moon"], "signs": ["Pisces", "Scorpio", "Cancer"], "themes": ["sea-mother", "sacred-wound-creates-life", "ecological-reciprocity"]}
        },
        "grammars": [BASE + "folklore-north-american-indian"]
    },
    {
        "id": "myth-coyote",
        "name": "Coyote the Trickster",
        "sort_order": 0,
        "category": "myths",
        "level": 1,
        "sections": {
            "The Story": "There is no one Coyote story — there are thousands, told by hundreds of nations across North America, and Coyote is never the same twice. He is the one who stole fire from the Fire People and brought it to humans (Klamath). He is the one who scattered the stars carelessly across the sky because he got bored of placing them carefully (Navajo). He is the one who challenged the river to a race and lost, and that is why rivers are winding (many nations). He tried to fly with the birds and fell. He tried to catch his own shadow. He tried to seduce the chief's daughter by disguising himself as a baby. He died — many times — and came back, because Coyote cannot stay dead. In some stories he shapes the world: he pushed apart the sky and earth, he named the animals, he stole daylight. In other stories he is simply hungry, foolish, lecherous, and unlucky. He is both creator and buffoon, and the traditions that tell his stories insist: he is both at the same time.",
            "Source": "Oral traditions of Navajo, Crow, Blackfoot, Nez Perce, Klamath, Paiute, Maidu, and many other nations. Collected by Boas, Lowie, Sapir, Ramsey, and others. Barry Lopez, Giving Birth to Thunder, Sleeping with His Daughter (1977) is an accessible compilation. Public domain ethnographic collections in the Smithsonian's Annual Reports.",
            "The Images": "The fire theft — Coyote as Prometheus, but funnier, clumsier, and motivated by cold rather than philosophy. The scattered stars — creation through carelessness, beauty from impatience. The death-and-return — you cannot kill appetite. The shapeshifting — Coyote becomes whatever the story needs, never fixed in one form. The foolishness — wisdom that comes not from being right but from being willing to be wrong, repeatedly, publicly, hilariously.",
            "Culture": "Pan-North American Indigenous. Coyote is not a god, not a hero, not a villain — he is the principle of ongoing disruption. Akomolafe reads the trickster tradition as the mythic embodiment of the crack — the place where the system fails and something new leaks through. Radin (The Trickster, 1956) saw Coyote as the earliest and most fundamental mythic figure: older than the hero, older than the god, the original consciousness before it learned to be serious. Jung wrote the commentary to Radin's book, recognizing in the trickster the shadow of the culture-hero."
        },
        "keywords": ["coyote", "trickster", "fire-theft", "foolish", "creator", "indigenous", "shapeshifter"],
        "metadata": {
            "origin": "Pan-North American Indigenous",
            "astrology": {"planets": ["Mercury", "Uranus"], "signs": ["Gemini", "Aquarius"], "themes": ["trickster", "sacred-foolishness", "creation-through-error"]}
        },
        "grammars": [BASE + "folklore-north-american-indian", BASE + "myths-north-american-indians"]
    },
    {
        "id": "myth-handless-maiden",
        "name": "The Handless Maiden",
        "sort_order": 0,
        "category": "myths",
        "level": 1,
        "sections": {
            "The Story": "A miller, tricked by the devil, promises 'what stands behind your mill' — thinking it is only the apple tree. But his daughter is standing there. The devil comes to collect. The girl weeps so much over her hands that her tears purify them, and the devil cannot touch her. He demands the father cut off her hands. The father, in agonized obedience, does it. The handless maiden wanders into the world, weeping. She comes to a royal orchard and, guided by an angel (or the wind, or her own desperate hunger), eats a pear from the king's tree. The king sees her, loves her, and marries her, making her silver hands. But the devil forges letters that make the king believe she has given birth to a monster. More letters: the king orders her killed. She flees with her baby into the forest. For seven years she lives in the wild, cared for by a spirit of the woods. At a spring in the forest, her real hands grow back. The king searches the world for her, finds her whole, and they are reunited.",
            "Source": "Brothers Grimm, 'The Girl Without Hands' (KHM 31). Variants across Europe, the Middle East, and North Africa (ATU tale type 706). Over 100 versions collected. Estés and Shaw both make this a central teaching story.",
            "The Images": "The severed hands — the creative, grasping, making power taken from a woman by her own father. The devil's bargain — the father who sells his daughter without knowing it (and then carries out the mutilation). The tears that purify — grief as protection. The silver hands — the false replacement, the prosthetic competence that is not real healing. The seven years in the forest — the long time of growing back what was taken, which cannot be rushed. The spring — the living water where regeneration happens. The real hands — what grows back when you live wild long enough.",
            "Culture": "European (German, Italian, Russian, Armenian variants). This is Shaw's and Estés's shared masterwork myth. Shaw tells it over three hours, insisting the time is part of the medicine. Estés devotes the longest chapter in Women Who Run With the Wolves to it. Both read it as the story of what happens when a woman's (or anyone's) creative power is severed by patriarchal complicity — and the long, forest-dwelling recovery required to grow it back. The seven years in the wild is not metaphorical: it takes that long."
        },
        "keywords": ["handless-maiden", "severed-hands", "forest", "regrowth", "feminine", "initiation", "fairy-tale"],
        "metadata": {
            "origin": "European (German/pan-European)",
            "astrology": {"planets": ["Saturn", "Moon", "Pluto"], "signs": ["Capricorn", "Cancer", "Scorpio"], "themes": ["mutilation-and-regrowth", "father-wound", "long-healing"]}
        },
        "grammars": [BASE + "grimms-fairy-tales"]
    },
    {
        "id": "myth-pandora",
        "name": "Pandora: The First Woman Opens the Jar",
        "sort_order": 0,
        "category": "myths",
        "level": 1,
        "sections": {
            "The Story": "After Prometheus stole fire, Zeus devised a punishment — not for Prometheus (who was already chained) but for humanity. He ordered Hephaestus to fashion a woman from earth and water, beautiful beyond mortal measure. Athena dressed her and taught her weaving. Aphrodite gave her beauty and desire. Hermes gave her a cunning mind and a lying tongue, and named her Pandora — 'All-Gifted.' Zeus sent her to Epimetheus, Prometheus's slow-witted brother, as a gift. She carried with her a great jar (pithos — mistranslated as 'box' since the Renaissance). Though warned never to open it, Pandora lifted the lid. Out flew every evil: disease, famine, war, death, old age, sorrow. She slammed it shut. Inside, trapped under the rim, remained one thing: Hope (Elpis). Whether hope's imprisonment is mercy or the cruelest evil of all has been debated for three thousand years.",
            "Source": "Hesiod, Works and Days (c. 700 BCE) and Theogony. Apollodorus, Bibliotheca. Public domain translations by Evelyn-White, Lattimore, and others.",
            "The Images": "The all-gifted woman — creation as weapon, beauty as trap, the gods' revenge delivered in feminine form. The jar — the container of everything humanity was not supposed to know or endure. The opening — curiosity as the act that unleashes suffering and simultaneously defines humanity. Hope trapped inside — the most ambiguous image in all Greek mythology: is hope our comfort or our final delusion?",
            "Culture": "Greek. Pandora is the Greek Eve — and Warner has written extensively about how both figures serve the same patriarchal narrative: the first woman's curiosity causes the fall of humanity. But Warner also reads against the grain: Pandora's opening of the jar is the same gesture as Bluebeard's wife opening the forbidden door — the refusal to remain ignorant, the insistence on knowing, which is punished but which is also the beginning of consciousness. Without Pandora, humanity would be comfortable and oblivious. With her, we suffer — but we know."
        },
        "keywords": ["pandora", "jar", "hope", "curiosity", "first-woman", "punishment", "greek"],
        "metadata": {
            "origin": "Greek",
            "astrology": {"planets": ["Venus", "Pluto"], "signs": ["Scorpio", "Libra"], "themes": ["curiosity-as-fall", "hope-in-darkness", "feminine-as-gift-and-trap"]}
        },
        "grammars": [BASE + "greek-mythology", BASE + "bulfinch-s-classical-mythology"]
    },
    {
        "id": "myth-quetzalcoatl",
        "name": "Quetzalcoatl: The Feathered Serpent",
        "sort_order": 0,
        "category": "myths",
        "level": 1,
        "sections": {
            "The Story": "Quetzalcoatl — the Feathered Serpent, the Plumed Dragon — existed before the world. With his rival-twin Tezcatlipoca (the Smoking Mirror), he created humanity, the sun, and the calendar. As god, he descended to the underworld Mictlan to recover the bones of the ancient dead, sprinkled them with his own blood, and from them made the present race of humans — the Fifth Sun's people. As priest-king of Tula, he was the ideal ruler: teaching arts, agriculture, the calendar, and prohibiting human sacrifice. But Tezcatlipoca tricked him: showed him a mirror (his own face, aged and mortal), gave him pulque until he was drunk, and lured him into incest with his own sister. Shattered by shame, Quetzalcoatl burned himself on a funeral pyre and rose as Venus, the Morning Star. Or: he sailed east on a raft of serpents, promising to return. The Aztecs awaited his return. When Cortés arrived from the east in 1519, the question of whether Moctezuma believed he was the returning Quetzalcoatl became one of history's most contested legends.",
            "Source": "Aztec and Toltec oral traditions recorded in the Florentine Codex (Bernardino de Sahagún, 1577), Annals of Cuauhtitlan, and other post-Conquest Nahuatl sources. Popol Vuh contains related Mesoamerican creation mythology. Public domain colonial-era translations.",
            "The Images": "The Feathered Serpent — earth (serpent) and sky (bird) united in one being, the reconciliation of opposites. The bones in the underworld — creation from death, humanity made from the remains of previous failures. The blood offering — the creator who gives his own substance to make the creation live. The mirror — self-knowledge as the beginning of the fall. The morning star — the risen god, transformed through shame and fire into light.",
            "Culture": "Mesoamerican (Aztec/Toltec/Maya). Quetzalcoatl is the Mesoamerican Christ-Prometheus-Odin: the god who sacrifices himself to create humanity, who descends to the underworld for the dead, who teaches civilization, who falls through human weakness, and who rises transformed. Campbell devoted extensive analysis to the Feathered Serpent as evidence of the monomyth. Eliade saw the Morning Star transformation as the clearest example of celestial ascent mythology. The serpent-bird unity is the alchemical coniunctio in Mesoamerican form: matter and spirit, venom and flight, in one body."
        },
        "keywords": ["quetzalcoatl", "feathered-serpent", "venus", "morning-star", "creation", "mesoamerican"],
        "metadata": {
            "origin": "Mesoamerican (Aztec/Toltec)",
            "astrology": {"planets": ["Venus", "Mercury", "Sun"], "signs": ["Libra", "Gemini", "Leo"], "themes": ["morning-star", "serpent-bird-union", "divine-king-fall"]}
        },
        "grammars": [BASE + "popol-vuh"]
    },
    {
        "id": "myth-oedipus",
        "name": "Oedipus: The Man Who Solved the Riddle",
        "sort_order": 0,
        "category": "myths",
        "level": 1,
        "sections": {
            "The Story": "An oracle told King Laius of Thebes that his son would kill him and marry his wife. When a son was born, Laius pierced the infant's ankles (Oedipus means 'swollen foot') and ordered him exposed on a mountainside. A shepherd saved him. Raised by the king and queen of Corinth, believing they were his parents, Oedipus grew up brilliant, restless, and tormented by a rumor that he was adopted. He consulted the oracle at Delphi, which told him only this: you will kill your father and marry your mother. Horrified, he fled Corinth — running straight toward Thebes. At a crossroads he quarreled with an old man and killed him: Laius, his father. At Thebes, a sphinx terrorized the city with a riddle: What walks on four legs in the morning, two at noon, three in the evening? Oedipus answered: Man. The sphinx died. Thebes made him king and gave him the widowed queen: Jocasta, his mother. Years of prosperity. Children. A plague. Investigation. Discovery. Jocasta hanged herself. Oedipus put out his own eyes and wandered blind for the rest of his life.",
            "Source": "Sophocles, Oedipus Rex (c. 429 BCE) and Oedipus at Colonus (401 BCE). Homer, Odyssey XI. Apollodorus, Bibliotheca. Euripides, The Phoenician Women. Public domain translations by Jebb, Fagles, Grene, and others.",
            "The Images": "The pierced ankles — the wound at the foundation, the original damage that names you. The crossroads — the place of fatal choice, where all roads lead to the same destination. The riddle of the sphinx — the answer is yourself, and solving it does not save you. The eyes — Oedipus sees the truth and blinds himself; the blind prophet Tiresias saw the truth all along. The investigation — the detective who discovers that the criminal is himself.",
            "Culture": "Greek. Freud made Oedipus the cornerstone of psychoanalysis: the unconscious desire for the opposite-sex parent that drives the psyche. Rank saw the birth-myth pattern: the exposed infant who becomes king (Moses, Perseus, Romulus). Jung saw the myth as about consciousness — the ego that insists on knowing the truth about itself, even when the truth destroys it. But Sophocles' own vision may be deeper than any interpreter's: Oedipus is the man who did everything right — solved the riddle, served his city, pursued the truth — and was destroyed precisely by his virtues. The myth asks: what if being right is not enough?"
        },
        "keywords": ["oedipus", "riddle", "fate", "blindness", "self-knowledge", "sphinx", "tragedy"],
        "metadata": {
            "origin": "Greek",
            "astrology": {"planets": ["Sun", "Saturn", "Pluto"], "signs": ["Leo", "Capricorn", "Scorpio"], "themes": ["fate", "self-discovery", "tragic-knowledge"]}
        },
        "grammars": [BASE + "greek-mythology", BASE + "bulfinch-s-classical-mythology"]
    },
    {
        "id": "myth-ariadne",
        "name": "Ariadne and the Thread",
        "sort_order": 0,
        "category": "myths",
        "level": 1,
        "sections": {
            "The Story": "Ariadne was the daughter of King Minos of Crete and Pasiphaë, and half-sister of the Minotaur — the bull-headed monster born of her mother's unnatural union with a divine bull. The Minotaur lived at the center of the Labyrinth, built by Daedalus, and every year Athens sent seven young men and seven young women to be devoured. When Theseus came as one of the sacrificial youths, Ariadne saw him and loved him. She gave him a ball of thread — the clew — telling him to fasten one end at the entrance and unwind it as he went. He found the Minotaur, killed it, and followed the thread back to the light. She had saved him. He promised to take her with him, to marry her. They sailed together. At the island of Naxos, he abandoned her — left her sleeping on the shore and sailed away. She woke alone. But Dionysus found her there, weeping on the beach, and made her his bride. He placed her wedding crown among the stars as the constellation Corona Borealis.",
            "Source": "Ovid, Metamorphoses VIII and Heroides X. Plutarch, Life of Theseus. Catullus, Poem 64. Apollodorus, Bibliotheca. Homer, Odyssey and Iliad (brief references). Public domain translations.",
            "The Images": "The thread — the lifeline, the connection to the way back, the feminine intelligence that navigates the labyrinth. The labyrinth — the structure that traps, the unconscious, the place where the monster waits. The abandonment on Naxos — the hero who uses the feminine and discards it, the broken promise. The sleeping woman on the shore — vulnerability, the moment between one life and the next. Dionysus finding her — the god of ecstasy chooses the woman the hero abandoned. The crown in the stars — the mortal woman made immortal by divine love, not by heroic achievement.",
            "Culture": "Greek. Ariadne has been read as the helper-maiden (Campbell), the anima figure who enables the hero (Jung), and the discarded woman redeemed by a greater love (Hillman). Hillman's reading is the most radical: Ariadne's abandonment by Theseus is necessary — the hero's love is too literal, too achievement-oriented. She needs to be abandoned by the daylight ego so that Dionysus — the god of depth, ecstasy, and soul — can find her. Her crown becomes a constellation: not a trophy but a transformation. Warner reads the story differently: another woman used and abandoned, whose rescue by another man is still defined by male desire."
        },
        "keywords": ["ariadne", "thread", "labyrinth", "abandonment", "dionysus", "crown", "naxos"],
        "metadata": {
            "origin": "Greek",
            "astrology": {"planets": ["Moon", "Venus", "Neptune"], "signs": ["Virgo", "Libra", "Pisces"], "themes": ["the-thread", "abandonment-and-divine-love", "labyrinth-wisdom"]}
        },
        "grammars": [BASE + "greek-mythology", BASE + "metamorphoses-ovid", BASE + "bulfinch-s-classical-mythology"]
    },
    {
        "id": "myth-tammuz-dumuzi",
        "name": "Tammuz and Ishtar: The Dying Consort",
        "sort_order": 0,
        "category": "myths",
        "level": 1,
        "sections": {
            "The Story": "Tammuz (Sumerian: Dumuzi) was the shepherd-king, the young husband of Inanna-Ishtar, goddess of love and war. When Inanna descended to the underworld and was held there, the price of her release was a substitute — someone must take her place. She returned to the upper world to find Tammuz sitting on her throne, dressed in fine garments, showing no grief for her absence. In rage, she fixed on him the eye of death: 'Take him.' The galla demons dragged Tammuz to the underworld. His sister Geshtinanna wept and volunteered to share his fate. The compromise: Tammuz would spend half the year below and half above, alternating with his sister. In summer, the land is green — Tammuz is above. In autumn, the women of Mesopotamia wept for Tammuz as the vegetation died, singing laments at the temple gates. He is the green that goes brown, the seed that enters the ground, the husband who pays the price for the wife's ambition and power.",
            "Source": "Sumerian texts: 'Inanna's Descent to the Netherworld,' 'Dumuzi's Dream,' and the Dumuzi-Inanna love songs (c. 2100-1600 BCE). Akkadian: 'Ishtar's Descent to the Netherworld.' Translated by Samuel Noah Kramer and Thorkild Jacobsen. Ezekiel 8:14 records women 'weeping for Tammuz' at the temple gates in Jerusalem.",
            "The Images": "The shepherd on the throne — the consort who enjoys the queen's power without understanding its cost. The eye of death — the goddess's gaze that selects the sacrifice. The weeping sister — the bond of sibling love that mediates between life and death. The alternation — half above, half below: the eternal rhythm of the seasons as divine commuting. The lamentation — the communal weeping for the dying god, the ritual that accompanies the death of green things.",
            "Culture": "Sumerian/Mesopotamian. Tammuz is the prototype dying god that Frazer placed at the center of The Golden Bough — the divine figure whose death IS the death of vegetation and whose return IS the spring. But the Sumerian version is more complex than Frazer's: Tammuz doesn't die nobly. He dies because his wife is angry that he didn't mourn her. The sacrifice is not willing but imposed. This makes it feel more real than sanitized versions: the cycles of nature are driven not by cosmic harmony but by divine rage, grief, and the impossible negotiations of love."
        },
        "keywords": ["tammuz", "dumuzi", "ishtar", "dying-god", "vegetation", "underworld", "lamentation"],
        "metadata": {
            "origin": "Sumerian/Mesopotamian",
            "astrology": {"planets": ["Venus", "Pluto"], "signs": ["Taurus", "Scorpio"], "themes": ["dying-consort", "vegetation-cycle", "sacrifice-for-return"]}
        },
        "grammars": []  # myths-babylonia-assyria not yet built
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# 3. INSERT NEW MYTHS
# ═══════════════════════════════════════════════════════════════════════════

# Find the last myth (raven or bluebeard depending on current state)
last_myth_idx = None
for i, item in enumerate(items):
    if item["category"] == "myths":
        last_myth_idx = i

# Insert after the last myth
for j, myth in enumerate(new_myths):
    items.insert(last_myth_idx + 1 + j, myth)

# ═══════════════════════════════════════════════════════════════════════════
# 4. UPDATE THREADS
# ═══════════════════════════════════════════════════════════════════════════

thread_new_refs = {
    "thread-descent": ["myth-medusa", "myth-handless-maiden", "myth-sedna"],
    "thread-dying-god": ["myth-dionysus", "myth-tammuz-dumuzi", "myth-quetzalcoatl"],
    "thread-sacred-marriage": ["myth-ariadne", "myth-tammuz-dumuzi"],
    "thread-dragon-fight": ["myth-oedipus", "myth-circe"],
    "thread-trickster": ["myth-coyote"],
    "thread-great-mother": ["myth-sedna", "myth-amaterasu", "myth-medusa"],
    "thread-flood-renewal": [],
    "thread-stolen-light": ["myth-pandora"],
}

for item in items:
    if item["id"] in thread_new_refs and thread_new_refs[item["id"]]:
        item["composite_of"].extend(thread_new_refs[item["id"]])

# ═══════════════════════════════════════════════════════════════════════════
# 5. UPDATE CULTURES
# ═══════════════════════════════════════════════════════════════════════════

culture_new_refs = {
    "culture-greek": ["myth-dionysus", "myth-medusa", "myth-circe", "myth-pandora", "myth-oedipus", "myth-ariadne"],
    "culture-egyptian-mesopotamian": ["myth-tammuz-dumuzi"],
    "culture-northern": ["myth-handless-maiden"],
    "culture-eastern": ["myth-amaterasu"],
}

for item in items:
    if item["id"] in culture_new_refs:
        item["composite_of"].extend(culture_new_refs[item["id"]])

# Add new culture card for Indigenous Americas (Sedna, Coyote, + existing Hero Twins, Raven)
# Find insertion point after culture-african-arabian
african_idx = next(i for i, item in enumerate(items) if item["id"] == "culture-african-arabian")
items.insert(african_idx + 1, {
    "id": "culture-indigenous-americas",
    "name": "Indigenous Americas: Tricksters, Sea Mothers, and the Living Land",
    "sort_order": 0,
    "category": "cultures",
    "level": 2,
    "sections": {
        "The World": "From the Arctic ice to the Amazon basin, the indigenous peoples of the Americas developed mythologies rooted in reciprocity with the land, the animals, and the spirits. There is no single 'Native American mythology' — there are hundreds of distinct traditions. But certain patterns recur: the trickster (Coyote, Raven, Anansi-influenced Br'er Rabbit) as world-maker and sacred fool. The animal-people who existed before humans and whose stories explain why the world is as it is. The sea and earth mothers (Sedna, Spider Woman, Corn Mother) whose bodies are the source of sustenance. The ball game between life and death (the Hero Twins in Xibalba). The understanding that the land is not a resource but a relative — that mountains, rivers, and animals are persons, and mythology is the record of relationships between persons of different kinds.",
        "What Makes It Unique": "The indigenous American contribution to world mythology is ecological personhood — the radical idea that the non-human world is composed of persons (animal persons, plant persons, river persons, stone persons) with whom humans exist in ongoing relationship. Myths are not stories about the past — they are protocols for maintaining these relationships. When Sedna's hair tangles, the shaman combs it: this is not metaphor but diplomacy. When Coyote steals fire, the theft creates an obligation. The Hero Twins' ball game in the underworld is not adventure but negotiation. Akomolafe and Shaw both draw deeply from this understanding: myth as ecology, story as kinship.",
        "Contemplation": "These traditions ask a question the Western mythic imagination rarely poses: what do we owe the animals? What do we owe the river? If the land is a person, what does it mean that we have treated it as property?"
    },
    "keywords": ["indigenous", "americas", "trickster", "ecological", "reciprocity", "land"],
    "composite_of": [
        "myth-raven-steals-light",
        "myth-hero-twins",
        "myth-coyote",
        "myth-sedna"
    ],
    "relationship_type": "emergence",
    "metadata": {}
})

# ═══════════════════════════════════════════════════════════════════════════
# 6. UPDATE INTERPRETER COMPOSITE_OF WITH NEW MYTHS
# ═══════════════════════════════════════════════════════════════════════════

interp_new_refs = {
    "interp-jung": ["myth-dionysus", "myth-oedipus"],
    "interp-campbell": ["myth-quetzalcoatl", "myth-oedipus", "myth-ariadne"],
    "interp-rank": ["myth-oedipus"],
    "interp-frazer": ["myth-tammuz-dumuzi", "myth-dionysus"],
    "interp-neumann": ["myth-medusa", "myth-sedna"],
    "interp-hillman": ["myth-ariadne", "myth-dionysus"],
    "interp-eliade": ["myth-amaterasu", "myth-quetzalcoatl"],
    "interp-akomolafe": ["myth-coyote"],
    "interp-shaw": ["myth-handless-maiden", "myth-sedna"],
    "interp-estes": ["myth-handless-maiden", "myth-medusa", "myth-circe"],
    "interp-warner": ["myth-pandora", "myth-circe", "myth-medusa", "myth-ariadne"],
}

for item in items:
    if item["id"] in interp_new_refs:
        item["composite_of"].extend(interp_new_refs[item["id"]])

# ═══════════════════════════════════════════════════════════════════════════
# 7. UPDATE META-COLLECTIVE-UNCONSCIOUS
# ═══════════════════════════════════════════════════════════════════════════

# No change needed — it already references all interpreters

# ═══════════════════════════════════════════════════════════════════════════
# 8. UPDATE DESCRIPTION
# ═══════════════════════════════════════════════════════════════════════════

g["description"] = g["description"].replace(
    "Thirty-one world myths",
    "Forty-three world myths"
)

# Add astrology to tags if not there
if "astrology" not in g["tags"]:
    g["tags"].append("astrology")
    g["tags"].append("planets")

# ═══════════════════════════════════════════════════════════════════════════
# 9. RECALCULATE SORT_ORDERS
# ═══════════════════════════════════════════════════════════════════════════

for i, item in enumerate(items):
    item["sort_order"] = i + 1

g["items"] = items

with open("grammars/myths-through-many-eyes/grammar.json", "w") as f:
    json.dump(g, f, indent=2, ensure_ascii=False)

# Report
from collections import Counter
cats = Counter(i["category"] for i in items)
levels = Counter(i["level"] for i in items)
has_grammars = sum(1 for i in items if i.get("grammars"))
has_astrology = sum(1 for i in items if i.get("metadata", {}).get("astrology"))

print(f"Total items: {len(items)}")
print(f"Categories: {dict(cats)}")
print(f"Levels: {dict(levels)}")
print(f"Items with grammars links: {has_grammars}")
print(f"Items with astrology metadata: {has_astrology}")
print(f"Sections: {sum(len(i.get('sections', {})) for i in items)}")
print(f"Sort orders: 1..{items[-1]['sort_order']}")
