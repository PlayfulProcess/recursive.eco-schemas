#!/usr/bin/env python3
"""
Parser for Myths and Legends of the Great Plains by K.B. Judson (Project Gutenberg #22083).
Outputs grammar.json into grammars/myths-legends-great-plains/
"""

import json
import os
import re

SEED_PATH = os.path.join(os.path.dirname(__file__), '..', 'seeds', 'myths-legends-great-plains.txt')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'grammars', 'myths-legends-great-plains')
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'grammar.json')


# Story definitions extracted from Table of Contents
STORY_DEFS = [
    {"title": "THE CREATION", "id": "the-creation", "name": "The Creation", "tribe": "Osage",
     "keywords": ["creation", "osage", "elk", "wind", "earth", "water"], "themes": ["creation", "cosmology"]},
    {"title": "HOW THE WORLD WAS MADE", "id": "how-the-world-was-made", "name": "How the World Was Made", "tribe": "Cherokee",
     "keywords": ["creation", "cherokee", "water-beetle", "buzzard", "mountains"], "themes": ["creation", "cosmology"]},
    {"title": "THE FLOOD AND THE RAINBOW", "id": "flood-and-rainbow", "name": "The Flood and the Rainbow", "tribe": "Delaware",
     "keywords": ["flood", "rainbow", "delaware", "rain", "promise"], "themes": ["creation", "cosmology"]},
    {"title": "THE FIRST FIRE", "id": "the-first-fire", "name": "The First Fire", "tribe": "Cherokee",
     "keywords": ["fire", "cherokee", "water-spider", "raven", "owl"], "themes": ["creation", "animal-tales"]},
    {"title": "THE ANCESTORS OF PEOPLE", "id": "ancestors-of-people", "name": "The Ancestors of People", "tribe": "Osage",
     "keywords": ["ancestors", "osage", "origins", "shell-people", "sky-people"], "themes": ["creation"]},
    {"title": "ORIGIN OF STRAWBERRIES", "id": "origin-of-strawberries", "name": "Origin of Strawberries", "tribe": "Cherokee",
     "keywords": ["strawberries", "cherokee", "man", "woman", "reconciliation"], "themes": ["creation", "love"]},
    {"title": "SACRED LEGEND", "id": "sacred-legend", "name": "Sacred Legend", "tribe": "Omaha",
     "keywords": ["sacred", "omaha", "vision", "ceremony", "spiritual"], "themes": ["ceremony", "cosmology"]},
    {"title": "THE LEGEND OF THE PEACE PIPES", "id": "legend-of-peace-pipes", "name": "The Legend of the Peace Pipes", "tribe": "Omaha",
     "keywords": ["peace-pipe", "omaha", "calumet", "ceremony", "peace"], "themes": ["ceremony"]},
    {"title": "A TRADITION OF THE CALUMET", "id": "tradition-of-calumet", "name": "A Tradition of the Calumet", "tribe": "Delaware",
     "keywords": ["calumet", "pipe", "delaware", "tradition", "peace"], "themes": ["ceremony"]},
    {"title": "THE SACRED POLE", "id": "the-sacred-pole", "name": "The Sacred Pole", "tribe": "Omaha",
     "keywords": ["sacred-pole", "omaha", "ceremony", "leadership", "tribal"], "themes": ["ceremony"]},
    {"title": "IKTO AND THE THUNDERS", "id": "ikto-and-the-thunders", "name": "Ikto and the Thunders", "tribe": "Teton",
     "keywords": ["ikto", "trickster", "thunder", "teton", "sioux"], "themes": ["trickster", "thunder"]},
    {"title": "THE THUNDER BIRD", "id": "thunder-bird-comanche", "name": "The Thunder Bird (Comanche)", "tribe": "Comanche",
     "keywords": ["thunder-bird", "comanche", "storm", "power"], "themes": ["thunder"]},
    {"title": "THE THUNDER BIRD", "id": "thunder-bird-assiniboin", "name": "The Thunder Bird (Assiniboin)", "tribe": "Assiniboin",
     "keywords": ["thunder-bird", "assiniboin", "storm", "eagle"], "themes": ["thunder"]},
    {"title": "SONG TO THE THUNDER GODS", "id": "song-to-thunder-gods", "name": "Song to the Thunder Gods", "tribe": "Omaha",
     "keywords": ["thunder", "song", "omaha", "prayer", "gods"], "themes": ["thunder", "ceremony"]},
    {"title": "SONGS OF THE BUFFALO HUNT", "id": "songs-of-buffalo-hunt", "name": "Songs of the Buffalo Hunt", "tribe": "Sioux",
     "keywords": ["buffalo", "hunt", "sioux", "songs", "ceremony"], "themes": ["buffalo", "ceremony"]},
    {"title": "ORIGIN OF THE BUFFALO", "id": "origin-of-buffalo", "name": "Origin of the Buffalo", "tribe": "Teton",
     "keywords": ["buffalo", "origin", "teton", "underground", "sioux"], "themes": ["creation", "buffalo"]},
    {"title": "THE BUFFALO BEING", "id": "the-buffalo-being", "name": "The Buffalo Being", "tribe": "Teton",
     "keywords": ["buffalo", "spirit", "teton", "vision", "power"], "themes": ["buffalo", "spirit-world"]},
    {"title": "THE YOUTH AND THE UNDERGROUND PEOPLE", "id": "youth-and-underground-people", "name": "The Youth and the Underground People", "tribe": "Omaha",
     "keywords": ["underground", "omaha", "youth", "buffalo", "spirit-people"], "themes": ["buffalo", "spirit-world"]},
    {"title": "THE BUFFALO AND THE GRIZZLY BEAR", "id": "buffalo-and-grizzly-bear", "name": "The Buffalo and the Grizzly Bear", "tribe": "Omaha",
     "keywords": ["buffalo", "grizzly", "bear", "omaha", "contest"], "themes": ["buffalo", "animal-tales"]},
    {"title": "MY FIRST BUFFALO HUNT", "id": "my-first-buffalo-hunt", "name": "My First Buffalo Hunt", "tribe": "Omaha",
     "keywords": ["buffalo", "hunt", "omaha", "first-person", "youth"], "themes": ["buffalo"]},
    {"title": "BIRD OMENS", "id": "bird-omens", "name": "Bird Omens", "tribe": "Sioux",
     "keywords": ["birds", "omens", "sioux", "signs", "prophecy"], "themes": ["birds", "ceremony"]},
    {"title": "THE BIRD CHIEF", "id": "the-bird-chief", "name": "The Bird Chief", "tribe": "Omaha",
     "keywords": ["bird", "chief", "omaha", "eagle", "owl", "woodpecker"], "themes": ["birds"]},
    {"title": "SONG OF THE BIRDS", "id": "song-of-the-birds", "name": "Song of the Birds", "tribe": "Pawnee",
     "keywords": ["birds", "song", "pawnee", "flight"], "themes": ["birds", "ceremony"]},
    {"title": "SONG OF KAWAS, THE EAGLE", "id": "song-of-kawas", "name": "Song of Kawas, the Eagle", "tribe": "Pawnee",
     "keywords": ["eagle", "kawas", "pawnee", "song", "sacred"], "themes": ["birds", "ceremony"]},
    {"title": "THE EAGLE'S REVENGE", "id": "eagles-revenge", "name": "The Eagle's Revenge", "tribe": "Cherokee",
     "keywords": ["eagle", "revenge", "cherokee", "hunter", "justice"], "themes": ["birds", "animal-tales"]},
    {"title": "THE RACE BETWEEN HUMMING BIRD AND CRANE", "id": "race-hummingbird-crane", "name": "The Race Between Humming Bird and Crane", "tribe": "Cherokee",
     "keywords": ["hummingbird", "crane", "race", "cherokee", "contest"], "themes": ["birds", "animal-tales"]},
    {"title": "RABBIT AND THE TURKEYS", "id": "rabbit-and-turkeys", "name": "Rabbit and the Turkeys", "tribe": "Omaha",
     "keywords": ["rabbit", "turkeys", "trickster", "omaha", "dance"], "themes": ["trickster", "animal-tales"]},
    {"title": "UNKTOMI AND THE BAD SONGS", "id": "unktomi-and-bad-songs", "name": "Unktomi and the Bad Songs", "tribe": "Dakota",
     "keywords": ["unktomi", "spider", "trickster", "dakota", "songs"], "themes": ["trickster"]},
    {"title": "HOW THE PHEASANT BEAT CORN", "id": "how-pheasant-beat-corn", "name": "How the Pheasant Beat Corn", "tribe": "Cherokee",
     "keywords": ["pheasant", "corn", "cherokee", "contest", "nature"], "themes": ["animal-tales"]},
    {"title": "WHY THE TURKEY GOBBLES", "id": "why-turkey-gobbles", "name": "Why the Turkey Gobbles", "tribe": "Cherokee",
     "keywords": ["turkey", "cherokee", "origin-story", "voice"], "themes": ["animal-tales", "creation"]},
    {"title": "OMAHA BELIEFS", "id": "omaha-beliefs", "name": "Omaha Beliefs", "tribe": "Omaha",
     "keywords": ["omaha", "beliefs", "customs", "sacred", "nature"], "themes": ["ceremony", "cosmology"]},
    {"title": "PAWNEE BELIEFS", "id": "pawnee-beliefs", "name": "Pawnee Beliefs", "tribe": "Pawnee",
     "keywords": ["pawnee", "beliefs", "customs", "sacred", "stars"], "themes": ["ceremony", "cosmology"]},
    {"title": "A SONG OF HOSPITALITY", "id": "song-of-hospitality", "name": "A Song of Hospitality", "tribe": "Sioux",
     "keywords": ["hospitality", "song", "sioux", "welcome", "generosity"], "themes": ["ceremony"]},
    {"title": "A SONG OF THE MARCH", "id": "song-of-the-march", "name": "A Song of the March", "tribe": "Sioux",
     "keywords": ["march", "song", "sioux", "journey", "movement"], "themes": ["ceremony"]},
    {"title": "SONG OF THE PRAIRIE BREEZE", "id": "song-of-prairie-breeze", "name": "Song of the Prairie Breeze", "tribe": "Kiowa",
     "keywords": ["prairie", "breeze", "kiowa", "wind", "nature"], "themes": ["ceremony", "nature-world"]},
    {"title": "OLD-WOMAN-WHO-NEVER-DIES", "id": "old-woman-who-never-dies", "name": "Old-Woman-Who-Never-Dies", "tribe": "Mandan",
     "keywords": ["old-woman", "mandan", "corn", "agriculture", "fertility"], "themes": ["creation", "nature-world"]},
    {"title": "LEGEND OF THE CORN", "id": "legend-of-corn", "name": "Legend of the Corn", "tribe": "Arikara",
     "keywords": ["corn", "arikara", "agriculture", "origin", "mother-corn"], "themes": ["creation", "nature-world"]},
    {"title": "TRADITION OF THE FINDING OF HORSES", "id": "finding-of-horses", "name": "Tradition of the Finding of Horses", "tribe": "Ponca",
     "keywords": ["horses", "ponca", "discovery", "animals", "plains"], "themes": ["creation", "animal-tales"]},
    {"title": "DAKOTA BELIEFS AND CUSTOMS", "id": "dakota-beliefs-customs", "name": "Dakota Beliefs and Customs", "tribe": "Dakota",
     "keywords": ["dakota", "beliefs", "customs", "sacred", "traditions"], "themes": ["ceremony", "cosmology"]},
    {"title": "WHY THE TETONS BURY ON SCAFFOLDS", "id": "why-tetons-bury-scaffolds", "name": "Why the Tetons Bury on Scaffolds", "tribe": "Teton",
     "keywords": ["burial", "scaffold", "teton", "death", "customs"], "themes": ["spirit-world", "ceremony"]},
    {"title": "THE GHOST'S RESENTMENT", "id": "ghosts-resentment", "name": "The Ghost's Resentment", "tribe": "Dakota",
     "keywords": ["ghost", "resentment", "dakota", "spirit", "death"], "themes": ["spirit-world"]},
    {"title": "THE FORKED ROADS", "id": "the-forked-roads", "name": "The Forked Roads", "tribe": "Omaha",
     "keywords": ["afterlife", "roads", "omaha", "death", "judgment"], "themes": ["spirit-world"]},
    {"title": "TATTOOED GHOSTS", "id": "tattooed-ghosts", "name": "Tattooed Ghosts", "tribe": "Dakota",
     "keywords": ["tattoo", "ghost", "dakota", "spirit", "afterlife"], "themes": ["spirit-world"]},
    {"title": "A GHOST STORY", "id": "a-ghost-story", "name": "A Ghost Story", "tribe": "Ponca",
     "keywords": ["ghost", "ponca", "spirit", "encounter", "fear"], "themes": ["spirit-world"]},
    {"title": "THE GHOST AND THE TRAVELER", "id": "ghost-and-traveler", "name": "The Ghost and the Traveler", "tribe": "Teton",
     "keywords": ["ghost", "traveler", "teton", "journey", "spirit"], "themes": ["spirit-world"]},
    {"title": "THE MAN WHO SHOT A GHOST", "id": "man-who-shot-ghost", "name": "The Man Who Shot a Ghost", "tribe": "Teton",
     "keywords": ["ghost", "shooting", "teton", "bravery", "spirit"], "themes": ["spirit-world"]},
    {"title": "THE INDIAN WHO WRESTLED WITH A GHOST", "id": "indian-who-wrestled-ghost", "name": "The Indian Who Wrestled with a Ghost", "tribe": "Teton",
     "keywords": ["ghost", "wrestling", "teton", "courage", "spirit"], "themes": ["spirit-world"]},
    {"title": "THE WAKANDA, OR WATER GOD", "id": "wakanda-water-god", "name": "The Wakanda, or Water God", "tribe": "Yankton",
     "keywords": ["wakanda", "water", "god", "yankton", "spirit"], "themes": ["spirit-world", "nature-world"]},
    {"title": "THE SPIRIT LAND", "id": "the-spirit-land", "name": "The Spirit Land", "tribe": "Arapahoe",
     "keywords": ["spirit-land", "arapahoe", "afterlife", "journey", "death"], "themes": ["spirit-world"]},
    {"title": "WAZIYA, THE WEATHER SPIRIT", "id": "waziya-weather-spirit", "name": "Waziya, the Weather Spirit", "tribe": "Teton",
     "keywords": ["waziya", "weather", "spirit", "teton", "cold"], "themes": ["spirit-world", "nature-world"]},
    {"title": "KANSAS BLIZZARDS", "id": "kansas-blizzards", "name": "Kansas Blizzards", "tribe": "Kansa",
     "keywords": ["blizzard", "kansas", "kansa", "winter", "storm"], "themes": ["nature-world"]},
    {"title": "IKTO AND THE SNOWSTORM", "id": "ikto-and-snowstorm", "name": "Ikto and the Snowstorm", "tribe": "Teton",
     "keywords": ["ikto", "trickster", "snow", "teton", "storm"], "themes": ["trickster", "nature-world"]},
    {"title": "THE SOUTHERN BRIDE", "id": "the-southern-bride", "name": "The Southern Bride", "tribe": "Cherokee",
     "keywords": ["bride", "south", "cherokee", "love", "seasons"], "themes": ["love", "nature-world"]},
    {"title": "THE FALLEN STAR", "id": "the-fallen-star", "name": "The Fallen Star", "tribe": "Dakota",
     "keywords": ["star", "fallen", "dakota", "sky", "hero", "journey"], "themes": ["heroes", "cosmology"]},
    {"title": "QUARREL OF THE SUN AND MOON", "id": "quarrel-sun-and-moon", "name": "Quarrel of the Sun and Moon", "tribe": "Omaha",
     "keywords": ["sun", "moon", "quarrel", "omaha", "celestial"], "themes": ["cosmology"]},
    {"title": "WHY THE POSSUM PLAYS DEAD", "id": "why-possum-plays-dead", "name": "Why the Possum Plays Dead", "tribe": "Cherokee",
     "keywords": ["possum", "cherokee", "playing-dead", "origin"], "themes": ["animal-tales", "creation"]},
    {"title": "BOG MYTH", "id": "bog-myth", "name": "Bog Myth", "tribe": "Dakota",
     "keywords": ["bog", "dakota", "earth", "swamp", "myth"], "themes": ["nature-world"]},
    {"title": "COYOTE AND SNAKE", "id": "coyote-and-snake", "name": "Coyote and Snake", "tribe": "Omaha",
     "keywords": ["coyote", "snake", "omaha", "trickster", "betrayal"], "themes": ["trickster", "animal-tales"]},
    {"title": "WHY THE WOLVES HELP IN WAR", "id": "why-wolves-help-in-war", "name": "Why the Wolves Help in War", "tribe": "Dakota",
     "keywords": ["wolves", "war", "dakota", "alliance", "warriors"], "themes": ["animal-tales"]},
    {"title": "HOW RABBIT ESCAPED FROM THE WOLVES", "id": "rabbit-escaped-wolves", "name": "How Rabbit Escaped from the Wolves", "tribe": "Cherokee",
     "keywords": ["rabbit", "wolves", "cherokee", "escape", "trickster"], "themes": ["trickster", "animal-tales"]},
    {"title": "HOW RABBIT LOST HIS FAT", "id": "how-rabbit-lost-fat", "name": "How Rabbit Lost His Fat", "tribe": "Omaha",
     "keywords": ["rabbit", "fat", "omaha", "trickster", "loss"], "themes": ["trickster", "animal-tales"]},
    {"title": "HOW FLINT VISITED RABBIT", "id": "how-flint-visited-rabbit", "name": "How Flint Visited Rabbit", "tribe": "Cherokee",
     "keywords": ["flint", "rabbit", "cherokee", "trickster", "fire"], "themes": ["trickster"]},
    {"title": "HOW RABBIT CAUGHT THE SUN IN A TRAP", "id": "rabbit-caught-sun", "name": "How Rabbit Caught the Sun in a Trap", "tribe": "Omaha",
     "keywords": ["rabbit", "sun", "trap", "omaha", "trickster"], "themes": ["trickster", "cosmology"]},
    {"title": "HOW RABBIT KILLED THE GIANT", "id": "rabbit-killed-giant", "name": "How Rabbit Killed the Giant", "tribe": "Omaha",
     "keywords": ["rabbit", "giant", "omaha", "trickster", "hero"], "themes": ["trickster", "heroes"]},
    {"title": "HOW THE DEER GOT HIS HORNS", "id": "how-deer-got-horns", "name": "How the Deer Got His Horns", "tribe": "Cherokee",
     "keywords": ["deer", "horns", "cherokee", "race", "origin"], "themes": ["animal-tales", "creation"]},
    {"title": "WHY THE DEER HAS BLUNT TEETH", "id": "why-deer-blunt-teeth", "name": "Why the Deer Has Blunt Teeth", "tribe": "Cherokee",
     "keywords": ["deer", "teeth", "cherokee", "origin", "punishment"], "themes": ["animal-tales", "creation"]},
    {"title": "LEGEND OF THE HEAD OF GOLD", "id": "legend-head-of-gold", "name": "Legend of the Head of Gold", "tribe": "Dakota",
     "keywords": ["gold", "head", "dakota", "magic", "quest"], "themes": ["heroes"]},
    {"title": "THE MILKY WAY", "id": "the-milky-way", "name": "The Milky Way", "tribe": "Cherokee",
     "keywords": ["milky-way", "cherokee", "stars", "corn", "dog"], "themes": ["cosmology", "creation"]},
    {"title": "COYOTE AND GRAY FOX", "id": "coyote-and-gray-fox", "name": "Coyote and Gray Fox", "tribe": "Ponca",
     "keywords": ["coyote", "fox", "ponca", "trickster", "contest"], "themes": ["trickster", "animal-tales"]},
    {"title": "ICTINIKE AND THE TURTLE", "id": "ictinike-and-turtle", "name": "Ictinike and the Turtle", "tribe": "Omaha",
     "keywords": ["ictinike", "turtle", "omaha", "trickster", "contest"], "themes": ["trickster"]},
    {"title": "ICTINIKE AND THE CREATORS", "id": "ictinike-and-creators", "name": "Ictinike and the Creators", "tribe": "Omaha",
     "keywords": ["ictinike", "creators", "omaha", "trickster", "power"], "themes": ["trickster", "creation"]},
    {"title": "HOW BIG TURTLE WENT ON THE WARPATH", "id": "big-turtle-warpath", "name": "How Big Turtle Went on the Warpath", "tribe": "Omaha",
     "keywords": ["turtle", "warpath", "omaha", "war", "hero", "humor"], "themes": ["heroes", "animal-tales"]},
]

# L2 thematic groupings
THEME_GROUPS = [
    {
        "id": "theme-creation-cosmology",
        "name": "Creation and Cosmology",
        "category": "themes",
        "about": "How did the world begin? How were the sun and moon set in their paths? These origin stories from the Osage, Cherokee, Delaware, and other nations tell of a time when the earth was covered with water, when animals dived to bring up mud, and when the Great Buzzard's wings carved the mountains. Each tribe carries its own version of the beginning, yet all share a vision of the world as a living creation brought forth through cooperation between beings.",
        "for_readers": "These creation stories offer a vision of the world as intentionally made and carefully ordered. Notice how animals, spirits, and people all participate in the making of the world. What does it mean to live in a world that was created through cooperation rather than command?",
        "member_ids": ["the-creation", "how-the-world-was-made", "flood-and-rainbow", "the-first-fire", "ancestors-of-people", "origin-of-strawberries", "origin-of-buffalo", "old-woman-who-never-dies", "legend-of-corn", "the-milky-way", "quarrel-sun-and-moon", "why-turkey-gobbles", "why-possum-plays-dead", "how-deer-got-horns", "why-deer-blunt-teeth", "finding-of-horses"],
        "keywords": ["creation", "origins", "cosmology", "world-making"]
    },
    {
        "id": "theme-sacred-ceremony",
        "name": "Sacred Ceremony and Belief",
        "category": "themes",
        "about": "The spiritual life of the Plains Indians was woven into every aspect of existence. The sacred pole, the peace pipe, the songs sung to the Thunder Gods and the buffalo herds — these are not merely rituals but living connections between the people and the mysterious powers that sustain the world. These texts preserve the words, songs, and ceremonies that shaped daily life on the Great Plains.",
        "for_readers": "These ceremonial texts reveal a world in which the sacred is not separate from daily life but embedded within it. Songs are prayers, objects are medicines, and every relationship — with animals, with weather, with the dead — is governed by reverence and reciprocity.",
        "member_ids": ["sacred-legend", "legend-of-peace-pipes", "tradition-of-calumet", "the-sacred-pole", "song-to-thunder-gods", "songs-of-buffalo-hunt", "bird-omens", "song-of-the-birds", "song-of-kawas", "song-of-hospitality", "song-of-the-march", "song-of-prairie-breeze", "omaha-beliefs", "pawnee-beliefs", "dakota-beliefs-customs", "why-tetons-bury-scaffolds"],
        "keywords": ["ceremony", "sacred", "song", "prayer", "belief"]
    },
    {
        "id": "theme-trickster",
        "name": "Trickster Tales",
        "category": "themes",
        "about": "The trickster — whether Rabbit, Ictinike, Ikto, Unktomi (Spider), or Coyote — is one of the most enduring figures in Plains mythology. Sometimes clever, sometimes foolish, always disruptive, the trickster teaches through misadventure. These tales are funny, surprising, and deeply instructive about the consequences of cunning, greed, and overconfidence.",
        "for_readers": "The trickster is never simply good or bad — he is the force that disrupts comfortable certainties and reveals hidden truths. Notice how the trickster's cleverness often backfires. What does this teach about the difference between cunning and wisdom?",
        "member_ids": ["ikto-and-the-thunders", "rabbit-and-turkeys", "unktomi-and-bad-songs", "ikto-and-snowstorm", "coyote-and-snake", "rabbit-escaped-wolves", "how-rabbit-lost-fat", "how-flint-visited-rabbit", "rabbit-caught-sun", "rabbit-killed-giant", "coyote-and-gray-fox", "ictinike-and-turtle", "ictinike-and-creators"],
        "keywords": ["trickster", "rabbit", "coyote", "ictinike", "ikto", "spider"]
    },
    {
        "id": "theme-buffalo",
        "name": "The Buffalo: Life of the Plains",
        "category": "themes",
        "about": "The buffalo was the center of Plains Indian life — food, clothing, shelter, tools, and spiritual power all flowed from this great animal. These stories tell of the buffalo's origin in the underground world, of the ceremonies and songs that called the herds near, and of the sacred relationship between hunter and hunted. To understand the Plains Indians is to understand the buffalo.",
        "for_readers": "The buffalo was not merely a resource but a relative, a spiritual being whose sacrifice sustained human life. These stories reveal a relationship of profound reciprocity between humans and the natural world. What would it mean to treat our food sources with this kind of reverence?",
        "member_ids": ["songs-of-buffalo-hunt", "origin-of-buffalo", "the-buffalo-being", "youth-and-underground-people", "buffalo-and-grizzly-bear", "my-first-buffalo-hunt"],
        "keywords": ["buffalo", "hunt", "plains", "sacred", "sustenance"]
    },
    {
        "id": "theme-spirit-world",
        "name": "Ghosts and the Spirit World",
        "category": "themes",
        "about": "The dead are not far away on the Great Plains. Ghosts walk the earth, spirits dwell in water and wind, and the roads that the dead must travel are mapped with precision. These tales — of ghostly encounters, scaffold burials, spirit lands, and the mysterious Wakanda — reveal a world in which the boundary between living and dead is thin and permeable.",
        "for_readers": "These ghost stories are not merely frightening tales — they are maps of the afterlife and guides for the living. The ghosts in these stories have purposes and grievances. What do they teach about unfinished business, proper mourning, and the obligations of the living to the dead?",
        "member_ids": ["ghosts-resentment", "the-forked-roads", "tattooed-ghosts", "a-ghost-story", "ghost-and-traveler", "man-who-shot-ghost", "indian-who-wrestled-ghost", "wakanda-water-god", "the-spirit-land", "why-tetons-bury-scaffolds"],
        "keywords": ["ghost", "spirit", "afterlife", "death", "spirit-land"]
    },
    {
        "id": "theme-birds-sky",
        "name": "Birds and the Sky World",
        "category": "themes",
        "about": "The power of flight inspired deep reverence among all Plains peoples. Eagle is chief of the birds and the most sacred creature of the sky. Owl rules the night, Woodpecker the trees, Duck the water. The songs and stories of birds carry messages from the spirit world and mark the rhythms of the natural year. The Thunder Bird, mightiest of all, commands the storms with its great jointed wings.",
        "for_readers": "Birds in these stories are not merely animals but messengers, omens, and spiritual powers. The eagle's flight is prayer made visible. What would it mean to read the movements of birds as the Plains peoples did — as signs from the living world?",
        "member_ids": ["thunder-bird-comanche", "thunder-bird-assiniboin", "song-to-thunder-gods", "bird-omens", "the-bird-chief", "song-of-the-birds", "song-of-kawas", "eagles-revenge", "race-hummingbird-crane"],
        "keywords": ["birds", "eagle", "thunder-bird", "sky", "flight", "omens"]
    },
    {
        "id": "theme-animal-tales",
        "name": "Animal Tales and Why Stories",
        "category": "themes",
        "about": "Why does the possum play dead? How did the deer get his horns? Why does the turkey gobble? These 'why' stories explain the characteristics of animals through narrative, revealing a world in which every creature's nature has a story behind it. Animals are not just animals — they are characters with histories, personalities, and relationships to the human world.",
        "for_readers": "These 'just-so' stories are enchanting for children and adults alike. They invite us to look at familiar animals with fresh eyes and to imagine the stories behind their shapes, sounds, and habits. Try making up your own 'why' stories about the animals you see every day.",
        "member_ids": ["the-first-fire", "buffalo-and-grizzly-bear", "eagles-revenge", "race-hummingbird-crane", "how-pheasant-beat-corn", "why-turkey-gobbles", "why-possum-plays-dead", "why-wolves-help-in-war", "how-deer-got-horns", "why-deer-blunt-teeth", "big-turtle-warpath", "finding-of-horses"],
        "keywords": ["animals", "why-stories", "origin", "nature"]
    },
    {
        "id": "theme-nature-weather",
        "name": "The Natural World: Weather, Seasons, and Earth",
        "category": "themes",
        "about": "On the Great Plains, weather is not background — it is a living force. The Thunder Gods roll across the sky, Waziya the Weather Spirit brings cold from the north, blizzards sweep in to test human endurance, and the prairie breeze carries songs. These stories tell of a world where weather has personality, seasons have stories, and the earth itself is alive with power.",
        "for_readers": "Living on the open plains meant living in intimate relationship with weather. These stories invite us to experience weather not as an inconvenience but as a conversation with living powers. The next time a storm rolls in, consider what the Thunder Gods might be saying.",
        "member_ids": ["waziya-weather-spirit", "kansas-blizzards", "ikto-and-snowstorm", "the-southern-bride", "song-of-prairie-breeze", "bog-myth", "old-woman-who-never-dies"],
        "keywords": ["weather", "storms", "seasons", "wind", "earth", "nature"]
    },
    {
        "id": "theme-heroes",
        "name": "Heroes and Quests",
        "category": "themes",
        "about": "The Fallen Star descends from the sky to walk among mortals. Big Turtle leads an unlikely war party of household objects. The young Rabbit kills a giant. These hero tales range from the cosmic to the comic, but all celebrate courage, resourcefulness, and the willingness to act when others will not.",
        "for_readers": "Heroes in Plains mythology come in unexpected forms — a fallen star, a turtle, a rabbit. What does it mean that the most heroic figures are often the most unlikely? These stories challenge us to find the hero in the humble and the overlooked.",
        "member_ids": ["the-fallen-star", "legend-head-of-gold", "rabbit-killed-giant", "big-turtle-warpath"],
        "keywords": ["hero", "quest", "courage", "journey"]
    },
]

# L3 meta-categories
L3_DEFS = [
    {
        "id": "meta-themes",
        "name": "Themes of the Great Plains",
        "category": "meta",
        "about": "The myths and legends of the Great Plains flow from a world of vast skies, rolling prairies, thunderstorms, and buffalo herds. The nine thematic streams — creation, ceremony, trickery, buffalo, spirits, birds, animals, weather, and heroism — together form a complete cosmology: a way of understanding the world as alive, interconnected, and sacred. These are not stories from the past but living teachings about how to be human in a world of infinite relationships.",
        "composite_of": [
            "theme-creation-cosmology",
            "theme-sacred-ceremony",
            "theme-trickster",
            "theme-buffalo",
            "theme-spirit-world",
            "theme-birds-sky",
            "theme-animal-tales",
            "theme-nature-weather",
            "theme-heroes"
        ],
        "keywords": ["great-plains", "themes", "cosmology", "worldview"]
    },
]


def read_seed():
    with open(SEED_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def strip_gutenberg(text):
    """Remove Gutenberg header and footer."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[text.index('\n', start_idx) + 1:]
    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]
    return text.strip()


def strip_front_matter(text):
    """Remove everything before the first story."""
    # Look for the title page of the actual content
    marker = "\nTHE CREATION\n"
    idx = text.find(marker)
    if idx != -1:
        return text[idx + 1:].strip()
    return text


def clean_text(text):
    """Clean illustration markers, footnotes, excessive whitespace."""
    text = re.sub(r'\[Illustration[^\]]*\]', '', text)
    text = re.sub(r'\[Notes:[^\]]*\]', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def extract_tribe(story_text):
    """Extract tribal attribution from the beginning of a story."""
    lines = story_text.strip().split('\n')
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Look for italic tribal attribution like _Osage_ or _Cherokee_
        m = re.match(r'^_([^_]+)_\s*$', stripped)
        if m:
            return m.group(1), i
    return None, -1


def extract_stories(text):
    """Split text into individual stories."""
    stories = []
    positions = []

    # Handle duplicate titles (two "THE THUNDER BIRD" entries)
    title_seen = {}

    for i, sdef in enumerate(STORY_DEFS):
        title = sdef["title"]
        search_from = title_seen.get(title, 0)

        # Try exact match first
        pattern = "\n" + title + "\n"
        idx = text.find(pattern, search_from)

        # Try with footnote markers like [A], [B], etc.
        if idx == -1:
            for marker in ['[A]', '[B]', '[C]', '[D]', '[E]', '[F]', '[G]', '[H]', '[I]', '[J]', '[K]', '[L]', '[M]', '[N]']:
                pattern2 = "\n" + title + marker + "\n"
                idx = text.find(pattern2, search_from)
                if idx != -1:
                    break

        if idx == -1 and text.startswith(title + "\n"):
            idx = 0

        if idx != -1:
            positions.append((idx, i))
            title_seen[title] = idx + len(title) + 1
        else:
            print(f"WARNING: Could not find story: {title}")

    positions.sort(key=lambda x: x[0])

    # Also find "THE END" to terminate last story
    end_marker = "\nTHE END\n"
    end_idx = text.find(end_marker)
    if end_idx == -1:
        end_idx = text.find("\nTHE END")
    if end_idx == -1:
        end_idx = len(text)

    for pos_idx, (start_pos, def_idx) in enumerate(positions):
        sdef = STORY_DEFS[def_idx]

        if pos_idx + 1 < len(positions):
            story_end = positions[pos_idx + 1][0]
        else:
            story_end = end_idx

        story_text = text[start_pos:story_end].strip()

        # Remove the title line(s)
        lines = story_text.split('\n')
        content_start = 0
        for j, line in enumerate(lines):
            stripped = line.strip()
            if stripped == '' or stripped == sdef["title"]:
                content_start = j + 1
            else:
                break

        story_content = '\n'.join(lines[content_start:]).strip()

        # Extract tribal attribution
        tribe_text, tribe_line = extract_tribe(story_content)
        if tribe_text and tribe_line >= 0:
            # Remove the tribe line from story content
            content_lines = story_content.split('\n')
            content_lines = content_lines[tribe_line + 1:]
            story_content = '\n'.join(content_lines).strip()

        story_content = clean_text(story_content)

        # Remove footnote markers like [A], [B], etc. and FOOTNOTE sections
        story_content = re.sub(r'\[([A-Z])\]', '', story_content)
        # Remove FOOTNOTE/FOOTNOTES sections
        story_content = re.sub(r'\n\nFOOTNOTE[S]?:.*?(?=\n\n[A-Z]|\Z)', '', story_content, flags=re.DOTALL)

        stories.append({
            "def_idx": def_idx,
            "text": story_content.strip(),
            "tribe": tribe_text or sdef.get("tribe", "")
        })

    return stories


def build_l1_items(stories):
    """Build L1 items from extracted stories."""
    items = []
    for sort_order, story in enumerate(stories):
        sdef = STORY_DEFS[story["def_idx"]]
        tribe = story["tribe"] or sdef.get("tribe", "")

        sections = {
            "Story": story["text"]
        }
        if tribe:
            sections["Tribal Source"] = tribe

        item = {
            "id": sdef["id"],
            "name": sdef["name"],
            "sort_order": sort_order,
            "level": 1,
            "category": "myth-legend",
            "sections": sections,
            "keywords": sdef["keywords"],
            "metadata": {
                "source": "Myths and Legends of the Great Plains, selected and edited by Katharine Berry Judson, A. C. McClurg & Co., Chicago, 1913",
                "tribe": tribe
            }
        }
        items.append(item)
    return items


def build_l2_items(l1_items):
    """Build L2 thematic groupings."""
    l2_items = []
    sort_order = len(l1_items)

    for group in THEME_GROUPS:
        l2_items.append({
            "id": group["id"],
            "name": group["name"],
            "sort_order": sort_order,
            "level": 2,
            "category": group["category"],
            "sections": {
                "About": group["about"],
                "For Readers": group["for_readers"]
            },
            "keywords": group["keywords"],
            "composite_of": group["member_ids"],
            "relationship_type": "emergence",
            "metadata": {}
        })
        sort_order += 1

    return l2_items, sort_order


def build_l3_items(start_sort_order):
    """Build L3 meta-categories."""
    l3_items = []
    sort_order = start_sort_order

    for l3 in L3_DEFS:
        l3_items.append({
            "id": l3["id"],
            "name": l3["name"],
            "sort_order": sort_order,
            "level": 3,
            "category": l3["category"],
            "sections": {
                "About": l3["about"]
            },
            "keywords": l3["keywords"],
            "composite_of": l3["composite_of"],
            "relationship_type": "emergence",
            "metadata": {}
        })
        sort_order += 1

    return l3_items


def build_grammar(l1_items, l2_items, l3_items):
    """Assemble the complete grammar."""
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
            "attribution": [
                {
                    "name": "Katharine Berry Judson",
                    "date": "1913",
                    "note": "Selected and edited Myths and Legends of the Great Plains, A. C. McClurg & Co., Chicago"
                },
                {
                    "name": "Bureau of American Ethnology / Various ethnologists",
                    "date": "various",
                    "note": "Original fieldwork sources: Alice C. Fletcher, J. Owen Dorsey, James Mooney, S. R. Riggs, and others"
                },
                {
                    "name": "PlayfulProcess",
                    "url": "https://lifeisprocess.substack.com/",
                    "date": "2026-03-04",
                    "note": "Grammar structure, thematic groupings, and reflections"
                }
            ]
        },
        "name": "Myths and Legends of the Great Plains",
        "description": "Seventy-two myths, legends, songs, and sacred traditions from the Great Plains Indian nations — Osage, Cherokee, Omaha, Dakota, Teton, Pawnee, Comanche, Arikara, Mandan, Ponca, Kiowa, Kansa, Delaware, Yankton, Arapahoe, and Assiniboin. Selected and edited by Katharine Berry Judson (1913) from the fieldwork of the Bureau of American Ethnology. These texts encompass creation stories, buffalo ceremonials, trickster tales, ghost encounters, sacred songs, and origin myths, preserving the living cosmology of peoples who dwelt in intimate relationship with the vast prairies, thunderstorms, and buffalo herds of the American heartland. Source: Project Gutenberg eBook #22083 (https://www.gutenberg.org/ebooks/22083).\n\nPUBLIC DOMAIN ILLUSTRATION REFERENCES: George Catlin's paintings of Plains Indian life (1830s-1840s, Smithsonian American Art Museum) — portraits, ceremonies, and landscapes. Karl Bodmer's aquatint illustrations from 'Travels in the Interior of North America' (1832-1834) — detailed depictions of Mandan, Sioux, and other Plains peoples. Edward S. Curtis photographs (early 1900s, Library of Congress) — portraits and ceremonial scenes.",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "creator_link": "https://lifeisprocess.substack.com/",
        "tags": [
            "mythology",
            "native-american",
            "great-plains",
            "creation",
            "trickster",
            "buffalo",
            "ceremony",
            "sacred-songs",
            "animism",
            "oracle"
        ],
        "roots": ["indigenous-mythology"],
        "shelves": ["earth"],
        "lineages": ["Shrei", "Andreotti"],
        "worldview": "animist",
        "cover_image_url": "",
        "items": l1_items + l2_items + l3_items
    }
    return grammar


def main():
    print("Reading seed text...")
    raw_text = read_seed()

    print("Stripping Gutenberg header/footer...")
    text = strip_gutenberg(raw_text)

    print("Stripping front matter...")
    text = strip_front_matter(text)

    print("Extracting stories...")
    stories = extract_stories(text)
    print(f"  Found {len(stories)} stories")

    print("Building L1 items...")
    l1_items = build_l1_items(stories)

    print("Building L2 items...")
    l2_items, next_sort = build_l2_items(l1_items)

    print("Building L3 items...")
    l3_items = build_l3_items(next_sort)

    print("Assembling grammar...")
    grammar = build_grammar(l1_items, l2_items, l3_items)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Writing grammar to {OUTPUT_PATH}...")
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    total_items = len(l1_items) + len(l2_items) + len(l3_items)
    print(f"\nDone! {total_items} items total:")
    print(f"  L1 (stories): {len(l1_items)}")
    print(f"  L2 (groups): {len(l2_items)}")
    print(f"  L3 (meta): {len(l3_items)}")


if __name__ == '__main__':
    main()
