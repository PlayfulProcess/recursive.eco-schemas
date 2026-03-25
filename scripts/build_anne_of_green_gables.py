#!/usr/bin/env python3
"""
Build grammar.json for Anne of Green Gables by L.M. Montgomery.

Source: Project Gutenberg eBook #45
Structure: 38 chapters
Levels:
  L1: Individual chapters (full text)
  L2: Thematic groupings with composite_of + chapter summaries
  L3: Meta-categories (The Story, Themes)
"""

import json
import re
from pathlib import Path

SEED_FILE = Path(__file__).parent.parent / "seeds" / "anne-of-green-gables.txt"
OUTPUT_DIR = Path(__file__).parent.parent / "grammars" / "anne-of-green-gables"
OUTPUT_FILE = OUTPUT_DIR / "grammar.json"

CHAPTER_TITLES = {
    1: "Mrs. Rachel Lynde Is Surprised",
    2: "Matthew Cuthbert Is Surprised",
    3: "Marilla Cuthbert Is Surprised",
    4: "Morning at Green Gables",
    5: "Anne's History",
    6: "Marilla Makes Up Her Mind",
    7: "Anne Says Her Prayers",
    8: "Anne's Bringing-up Is Begun",
    9: "Mrs. Rachel Lynde Is Properly Horrified",
    10: "Anne's Apology",
    11: "Anne's Impressions of Sunday-school",
    12: "A Solemn Vow and Promise",
    13: "The Delights of Anticipation",
    14: "Anne's Confession",
    15: "A Tempest in the School Teapot",
    16: "Diana Is Invited to Tea with Tragic Results",
    17: "A New Interest in Life",
    18: "Anne to the Rescue",
    19: "A Concert, a Catastrophe, and a Confession",
    20: "A Good Imagination Gone Wrong",
    21: "A New Departure in Flavorings",
    22: "Anne Is Invited Out to Tea",
    23: "Anne Comes to Grief in an Affair of Honor",
    24: "Miss Stacy and Her Pupils Get Up a Concert",
    25: "Matthew Insists on Puffed Sleeves",
    26: "The Story Club Is Formed",
    27: "Vanity and Vexation of Spirit",
    28: "An Unfortunate Lily Maid",
    29: "An Epoch in Anne's Life",
    30: "The Queen's Class Is Organized",
    31: "Where the Brook and River Meet",
    32: "The Pass List Is Out",
    33: "The Hotel Concert",
    34: "A Queen's Girl",
    35: "The Winter at Queen's",
    36: "The Glory and the Dream",
    37: "The Reaper Whose Name Is Death",
    38: "The Bend in the Road",
}

CHAPTER_SUMMARIES = {
    1: "Mrs. Rachel Lynde, Avonlea's self-appointed observer of everyone's business, is astonished to see Matthew Cuthbert driving to town. She discovers the Cuthberts have decided to adopt an orphan boy to help with the farm. This opening chapter establishes the community of Avonlea and its watchful, gossipy, but ultimately caring nature.",
    2: "Matthew goes to the train station expecting a boy and finds Anne Shirley — a scrawny, red-haired girl with an enormous capacity for talk. On the drive to Green Gables, Anne transforms the ordinary landscape into a wonder with her imagination, renaming places and talking non-stop. Matthew, the shyest man in Avonlea, is quietly enchanted.",
    3: "Marilla confronts the mistake: they asked for a boy, and a girl has come. Anne, overhearing, is devastated — she has been unwanted her whole life, and here it is happening again. She cries herself to sleep while Marilla struggles with the practical problem and Matthew quietly advocates for keeping her.",
    4: "Anne wakes to the beauty of Green Gables in morning light. For the first time in her life, she sees a real home — the cherry tree in bloom, the brook, the garden. She names the cherry tree 'Snow Queen' and pours out her longing for beauty and belonging to Marilla, who doesn't quite know what to make of her.",
    5: "Marilla asks about Anne's history. The story is heartbreaking: orphaned as a baby, passed from one reluctant household to another, raising other people's children, never wanted, never belonging. Anne tells it with characteristic honesty and without self-pity, though the facts speak for themselves.",
    6: "Marilla decides to keep Anne, partly out of duty and partly because something about the child has gotten under her skin. She announces the decision with typical brusqueness, but Anne's ecstatic response — tears of joy and a fierce hug — cracks Marilla's reserve for the first time.",
    7: "Marilla discovers that Anne has never been taught to pray. Anne composes her own prayer on the spot — a characteristic blend of imagination, sincerity, and unintentional comedy. This chapter establishes Anne's relationship with religion: genuine feeling expressed in utterly unconventional ways.",
    8: "Anne's education begins — in domesticity, deportment, and self-control. Marilla teaches her to do housework, attend church, and behave properly. Anne tries earnestly but keeps getting distracted by beauty, imagination, and her own tendency to talk. The tension between Marilla's rules and Anne's nature drives many chapters to come.",
    9: "Mrs. Rachel Lynde visits and pronounces Anne homely and red-haired. Anne explodes in a fury of wounded pride, stamping her foot and telling Mrs. Lynde exactly what she thinks of her. Marilla is horrified but also secretly impressed by the child's fire. Anne is sent to her room to repent.",
    10: "Marilla insists Anne apologize to Mrs. Lynde. Anne, after much inner struggle, produces an apology so theatrical and over-the-top that Mrs. Lynde is charmed rather than offended. Anne discovers that the right kind of humility can be a performance — and that Mrs. Lynde is kinder than she seemed.",
    11: "Anne attends Sunday school for the first time. She decorates her hat with wildflowers, which scandalizes some and delights others. Her honest questions about theology and her creative interpretation of scripture reveal both her hunger for beauty and her difficulty fitting into conventional molds.",
    12: "Anne meets Diana Barry, the girl next door, and they swear a solemn vow of eternal friendship. This bosom-friend relationship is one of the book's great joys — two girls creating their own rituals, language, and world. Anne finally has what she's always longed for: someone who chooses her.",
    13: "Anne anticipates a Sunday school picnic with almost unbearable excitement. Montgomery captures the intensity of childhood anticipation — how waiting for something wonderful can be an experience as rich as the thing itself. Anne's capacity for joy is as outsized as her capacity for sorrow.",
    14: "Anne confesses to losing Marilla's amethyst brooch, though she actually didn't do it. She makes up an elaborate false confession just so Marilla will let her go to the picnic. When the brooch is found (caught in a shawl), Marilla must confront her own unfairness and Anne's willingness to lie for love of life.",
    15: "Anne starts school and immediately clashes with Gilbert Blythe, the handsomest and smartest boy in Avonlea, who calls her 'Carrots' and pulls her braid. Anne smashes her slate over his head and begins a feud that will last years — and mask a connection that runs deeper than either will admit.",
    16: "Anne invites Diana for tea and accidentally serves her currant wine instead of raspberry cordial. Diana gets tipsy, and her mother, Mrs. Barry, forbids their friendship entirely. Anne is devastated — the loss of Diana feels like the loss of everything she's worked to build in Avonlea.",
    17: "Separated from Diana, Anne throws herself into studying. She discovers a passion for academic competition, driven partly by her rivalry with Gilbert Blythe. Miss Stacy, a new teacher with progressive methods, arrives and recognizes Anne's potential. A new chapter of Anne's life begins.",
    18: "Diana's little sister Minnie May comes down with croup in the night while the adults are away. Anne, who learned to nurse sick children in her orphan days, saves Minnie May's life. Mrs. Barry, grateful, lifts the ban on Diana's friendship. Anne's difficult past becomes her gift.",
    19: "Anne performs at a concert, recites dramatically, and then makes a confession: she and Diana and some friends were playing dares and Anne walked the ridgepole of a roof, fell off, and broke her ankle. Her imagination and dramatic flair, so often her glory, sometimes lead her into real danger.",
    20: "Anne and Diana play in the 'Haunted Wood' — a place Anne's imagination has populated with ghosts. When Anne must walk through it alone at night, she terrifies herself so thoroughly that she resolves to stop imagining scary things. A lesson in how imagination cuts both ways.",
    21: "Anne tries to make a cake for Mrs. Allan and accidentally flavors it with liniment instead of vanilla. The mistake is both hilarious and mortifying. Anne's domestic disasters are a running theme — she is so busy dreaming that she forgets the practical world. But her sincerity always wins people over.",
    22: "Anne is invited to tea at the manse. She conducts herself beautifully, demonstrating that she can be graceful and poised when she chooses. The chapter shows Anne's growth — she is learning to channel her intensity without losing her spark.",
    23: "Anne, dared by Josie Pye, walks the ridgepole of the Barry kitchen roof and falls off, spraining her ankle. She spends seven weeks in bed, during which she reflects, reads, and matures. The accident is a turning point — Anne begins to think before she leaps.",
    24: "Miss Stacy organizes a concert, and Anne throws herself into recitation with passionate intensity. Her talent for performance and her love of beauty find a constructive outlet. Miss Stacy becomes a mentor who nurtures Anne's gifts while gently curbing her excesses.",
    25: "Matthew notices that Anne dresses differently from other girls and quietly insists on buying her a dress with puffed sleeves — the fashion of the moment. His shy, wordless love for Anne is one of the book's most touching elements. The dress is a gift of belonging.",
    26: "Anne and her friends form a Story Club to write and share fiction. Anne's stories are melodramatic, full of murders, deathbed scenes, and passionate declarations. The chapter is both funny and significant — Anne is finding her voice as a creator, even if her taste needs refining.",
    27: "Anne, consumed by vanity, dyes her red hair with a peddler's dye — and it turns green. She must have it cut short, suffering weeks of mortification. The episode teaches Anne about vanity, but also reveals how deeply her red hair — her perceived flaw — is actually part of her identity.",
    28: "Anne and her friends reenact 'The Lady of Shalott' on the pond, with Anne as Elaine floating in a flat-bottomed boat. The boat leaks, and Anne must cling to a bridge pile until Gilbert Blythe rescues her. She still refuses to speak to him. The scene is comic and mythic at once.",
    29: "An epoch: Anne is finally persuaded to forgive Gilbert Blythe. After years of feuding, she speaks to him — briefly, grudgingly — and the ice begins to thaw. This chapter marks Anne's movement from childhood stubbornness toward adolescent complexity.",
    30: "Miss Stacy organizes a special class to prepare students for the Queen's Academy entrance exam. Anne and Gilbert are the top competitors. Anne's academic ambition intensifies, driven by her desire to make Matthew and Marilla proud and to prove herself worthy of everything they've given her.",
    31: "Anne is fifteen, on the threshold between childhood and adulthood. Montgomery writes beautifully about this transition — the brook that becomes a river, the girl who senses that wonder and responsibility will now walk side by side. Anne's imagination matures but doesn't diminish.",
    32: "The pass list for Queen's Academy is published. Anne has tied with Gilbert Blythe for top marks. The community celebrates, and Matthew and Marilla glow with pride. Anne's academic triumph validates every difficult decision they made in keeping her.",
    33: "Anne performs at a hotel concert in White Sands and is a sensation. A wealthy woman, a friend of the premier, offers to sponsor Anne's education. Anne is beginning to move beyond Avonlea into the wider world, carrying her intensity and imagination with her.",
    34: "Anne leaves for Queen's Academy in Charlottetown — her first time away from Green Gables. She is homesick, ambitious, and determined. The chapter captures the excitement and loneliness of leaving home for the first time.",
    35: "Anne's winter at Queen's is a story of hard work, friendship, and growing up. She wins the Avery Scholarship for English — the highest academic prize. Her rivalry with Gilbert remains, but the antagonism has softened into mutual respect.",
    36: "Anne returns home triumphant with the Avery Scholarship, which will fund her university education at Redmond College. The community celebrates. Anne's dreams of becoming a writer and scholar seem within reach. This is the climax of her academic journey.",
    37: "Matthew Cuthbert dies suddenly of a heart attack after learning the family savings are lost in a bank failure. The chapter is devastating — Matthew, who saved Anne from the orphanage, who bought her puffed sleeves, who loved her quietly and completely, is gone. Anne's deepest grief.",
    38: "Anne gives up the Avery Scholarship to stay at Green Gables with Marilla, whose eyesight is failing. She will teach at the Avonlea school instead — and Gilbert Blythe, who won the school, gives it up for her so she won't have to board away from home. Anne and Gilbert are finally, truly friends. The bend in the road leads not to loss but to love.",
}

CHAPTER_REFLECTIONS = {
    1: "Mrs. Lynde thinks she knows everything about everyone. What's good about being observant — and what's wrong with being nosy?",
    2: "Anne names everything beautiful she sees — the Avenue becomes 'White Way of Delight.' Why do names matter? Does renaming something change how you see it?",
    3: "Anne says 'Nobody ever did want me.' What is it like to feel unwanted? What changes when someone finally chooses you?",
    4: "Anne sees Green Gables for the first time and falls in love. What does it feel like to see a place and know it could be home?",
    5: "Anne's history is sad, but she doesn't feel sorry for herself. Where do you think her strength comes from?",
    6: "Marilla decides to keep Anne. What do you think changed her mind? Was it logic or feeling?",
    7: "Anne makes up her own prayer. Is there a right way to pray, or is sincerity enough?",
    8: "Anne has trouble following rules because her imagination keeps pulling her away. Is daydreaming a problem or a gift?",
    9: "Anne loses her temper when Mrs. Lynde insults her looks. When is anger justified? How should we handle it?",
    10: "Anne's apology to Mrs. Lynde is dramatic and over-the-top. Is it genuine? Can a performance also be sincere?",
    11: "Anne decorates her hat with flowers for church. Why do people care so much about fitting in? Should they?",
    12: "Anne and Diana swear to be bosom friends forever. What makes a friendship feel sacred?",
    13: "Anne can barely wait for the picnic. When have you wanted something so much the waiting was almost too much to bear?",
    14: "Anne confesses to something she didn't do. Why would someone lie to get permission to have fun? Was it wrong?",
    15: "Anne smashes her slate over Gilbert's head. What's behind such a fierce reaction? Is there more going on than anger?",
    16: "Anne loses Diana's friendship because of an honest mistake. Have you ever been punished for something that wasn't your fault?",
    17: "Without Diana, Anne turns to books and studying. How do we cope when we lose something important to us?",
    18: "Anne saves Minnie May's life using skills she learned as an orphan. How can difficult experiences from our past become strengths?",
    19: "Anne walks the ridgepole on a dare and falls. Why do we sometimes do dangerous things to prove ourselves?",
    20: "Anne scares herself with her own imagination. Can too much imagination be dangerous? How do you keep it healthy?",
    21: "The liniment cake is both funny and embarrassing. How do you handle moments when you mess up in front of people you want to impress?",
    22: "Anne shows she can be poised and graceful when she tries. Is the 'real' Anne the wild one or the polished one — or both?",
    23: "After her fall, Anne has time to reflect. What can we learn from being forced to slow down?",
    24: "Anne loves performing and reciting poetry. What do you love doing so much that it doesn't feel like work?",
    25: "Matthew notices Anne needs puffed sleeves before she asks. What does it mean when someone pays attention to what you need without being told?",
    26: "Anne's stories are full of dramatic deaths and passionate love. Why do young writers (and readers) love extreme emotions?",
    27: "Anne dyes her hair and it turns green. What can we learn from trying to change something about ourselves that we don't like?",
    28: "Anne plays Elaine the Lily Maid and almost drowns. Why is she drawn to dramatic, tragic stories?",
    29: "Anne finally forgives Gilbert. What makes forgiveness possible — and why does it sometimes take so long?",
    30: "Anne studies fiercely to pass the Queen's exam. What drives her — ambition, love, or something else?",
    31: "Anne stands between childhood and adulthood. What does it feel like to know things are about to change forever?",
    32: "Anne ties with Gilbert for top marks. How does competition with someone else push us to be our best?",
    33: "Anne performs at the hotel concert and is offered sponsorship. When has an unexpected opportunity changed your path?",
    34: "Anne leaves Green Gables for the first time. What is hardest about leaving home — and what is most exciting?",
    35: "Anne wins the Avery Scholarship. What does this achievement mean to her — and to Matthew and Marilla?",
    36: "Anne comes home triumphant. How does it feel to succeed and share that success with the people who believed in you?",
    37: "Matthew dies. How do we go on when we lose someone we love deeply? What does Matthew's love mean to Anne?",
    38: "Anne gives up her scholarship to stay with Marilla. Is this sacrifice — or is it a choice made from love? What does the 'bend in the road' mean?",
}

CHAPTER_PARENT_NOTES = {
    1: "Montgomery opens with the community, not the orphan. This establishes that Anne is arriving into a world that already has its own rhythms, opinions, and expectations. Mrs. Lynde represents the community's judgment — which Anne will both challenge and ultimately win over.",
    2: "The buggy ride is one of the great 'getting to know you' scenes in literature. Watch how Matthew — a man terrified of women and girls — falls in love with Anne without saying a word. His silence is as eloquent as her chatter.",
    3: "Anne's devastation at being unwanted is the emotional bedrock of the book. Every subsequent chapter — her need to belong, her fear of rejection, her fierce loyalty — grows from this wound. This chapter is worth discussing with children who have experienced rejection.",
    4: "Anne's ability to see beauty everywhere is not escapism — it's a survival skill refined through years of having nothing. She names things because naming creates relationship. The cherry tree becomes 'Snow Queen' and thereby becomes hers. This is the power of imagination to create belonging.",
    5: "Anne's history is Dickensian in its grimness, but Montgomery tells it without sentimentality. Anne is not defined by her suffering — she is defined by what she made of it. This chapter is important for children in difficult circumstances: your past is not your identity.",
    6: "Marilla's decision is the book's first great act of love, though Marilla would never call it that. She frames it as duty, but something deeper is at work. This is a beautiful example of how people who struggle to express emotion can still act from the heart.",
    7: "Anne's prayer is pure Montgomery — funny, sincere, and surprisingly profound. The scene raises real questions about the relationship between form and feeling in religion. Anne doesn't know the conventions, but her prayer is more genuine than many conventional ones.",
    8: "The tension between Anne's nature and Marilla's expectations will drive much of the plot. Neither is wrong: Marilla's structure is genuinely needed, and Anne's imagination is genuinely valuable. The book argues for balance, not victory of one over the other.",
    9: "Anne's fury at Mrs. Lynde is her most dramatic early outburst. Montgomery treats it with nuance — Anne is wrong to be rude, but her feelings are understandable. Mrs. Lynde was cruel, even if she didn't mean to be. This chapter is rich territory for discussing the difference between valid feelings and inappropriate expression.",
    10: "The over-the-top apology is quintessential Anne — she can't do anything halfway. Montgomery asks: is performative humility genuine? The answer seems to be yes, for Anne: her feelings are real, even when her expression is theatrical. This is a key insight into creative, intense children.",
    11: "The wildflower hat encapsulates Anne's relationship with convention. She sees beauty; the community sees impropriety. Neither is entirely right. This tension between individual expression and social belonging runs through the entire book.",
    12: "The bosom-friend scene is beloved because it captures something real about childhood friendship — the intensity, the ritual, the sense that this relationship is the most important thing in the world. Anne and Diana's friendship validates each other's existence.",
    13: "Montgomery writes about anticipation with extraordinary precision. Anne's ability to wring maximum joy from waiting is a genuine gift — and a form of mindfulness, though Montgomery wouldn't have used that word. Discuss with your child: is the waiting sometimes better than the thing?",
    14: "The false confession is morally complex. Anne lies, but her motive is understandable. Marilla's initial assumption of guilt is unfair. The chapter raises questions about trust, justice, and the difference between truth and honesty.",
    15: "The slate scene is iconic and important. Gilbert's 'Carrots' is a real insult to Anne, touching her deepest insecurity. Her response is excessive but proportional to her pain. The rivalry that begins here masks attraction — a dynamic Montgomery handles with wonderful subtlety.",
    16: "The currant wine episode is both hilarious and consequential. Anne loses her best friend through an honest mistake — a taste of how the adult world often works. The injustice of Mrs. Barry's punishment teaches Anne that life is not always fair.",
    17: "Without Diana, Anne redirects her energy toward academics. This chapter shows Anne's resilience: when one door closes, she finds another. Miss Stacy's arrival is providential — Anne needs a mentor who sees her gifts, not just her flaws.",
    18: "The Minnie May scene is crucial: Anne's orphan experiences — nursing sick children, managing crises — save a life. Montgomery argues that suffering is not wasted; it becomes competence. This is a powerful message for children who have been through difficult times.",
    19: "Anne's ridgepole walk is a parable about peer pressure and the desire to prove oneself. Montgomery treats it with humor but also seriousness — Anne really does get hurt. The chapter is useful for discussing when to refuse a dare.",
    20: "The Haunted Wood chapter is Montgomery's meditation on imagination's dangers. Anne, who uses imagination to beautify the world, here uses it to terrify herself. She learns an important lesson: you are responsible for what you imagine.",
    21: "The liniment cake is pure comedy, but underneath it is Anne's desperate desire to be competent at domestic work — to prove she belongs in the household. Her failures are always in the gap between dreaming and doing.",
    22: "Anne at the manse tea shows her capacity for growth. She can be graceful, attentive, and socially skilled. This is not a different Anne — it's the same Anne, with her energy directed. Montgomery argues that wild children don't need to be tamed, just focused.",
    23: "The ridgepole fall and subsequent convalescence give Anne time to mature. Montgomery uses illness and recovery as a metaphor for growing up — the body slows down so the mind can catch up.",
    24: "Miss Stacy is the book's ideal teacher — she recognizes Anne's gifts, channels her energy, and challenges her without breaking her spirit. If your child has a teacher like this, treasure them.",
    25: "Matthew's puffed sleeves are one of the most touching gifts in literature. He can barely speak to women, but he notices Anne's longing and acts on it. This chapter demonstrates that love is attention — seeing what someone needs and providing it, however awkwardly.",
    26: "The Story Club chapters are about finding your creative voice. Anne's stories are terrible by adult standards — overwrought and melodramatic — but they're a necessary stage. Every writer starts by imitating badly. Montgomery respects the process.",
    27: "The hair-dyeing episode teaches Anne about vanity — but also about self-acceptance. Her red hair, which she has always hated, is part of who she is. Trying to change it makes things worse. Montgomery's message: your perceived flaws may be your most distinctive features.",
    28: "The Lily Maid scene is quintessential Anne — she lives inside stories so intensely that she nearly drowns in one. Gilbert's rescue creates a debt she refuses to acknowledge. The tension between imagination and reality, between pride and gratitude, is perfectly calibrated.",
    29: "Forgiving Gilbert is a milestone of maturity. Anne held the grudge so long it became part of her identity. Letting it go requires her to change — not just her behavior, but her self-concept. This is a profound lesson about how pride becomes a prison.",
    30: "The Queen's class marks Anne's transition from child to young adult. Her academic ambition is driven by love — for Matthew, for Marilla, for learning itself. Competition with Gilbert is the engine, but gratitude is the fuel.",
    31: "This lyrical chapter is Montgomery at her best — the brook-becoming-river metaphor captures the bittersweet transition from childhood. Anne senses that she is gaining something (maturity, purpose) and losing something (unselfconscious wonder). Both feelings are real.",
    32: "The pass list scene is cathartic — years of effort culminating in success. Notice that Anne ties with Gilbert rather than beating him. Montgomery refuses to make it a simple victory; the rival is also worthy. This is sophisticated storytelling.",
    33: "The hotel concert expands Anne's world beyond Avonlea. She discovers she has gifts that the wider world values. The offer of sponsorship represents the larger life that awaits — but also the pull away from home.",
    34: "Leaving home is terrifying for Anne, who fought so hard to find one. The homesickness is real and intense. Montgomery doesn't minimize it — she shows that loving your home and needing to leave it are not contradictory.",
    35: "Queen's Academy is where Anne proves herself in the wider world. The Avery Scholarship for English validates not just her intelligence but her particular gift — the gift of words, of stories, of seeing beauty. It's deeply satisfying.",
    36: "The homecoming triumph is bittersweet in retrospect, given what follows. Montgomery gives Anne (and the reader) a chapter of pure joy before the grief to come. This is honest storytelling — life gives us both.",
    37: "Matthew's death is one of the most devastating moments in children's literature. Montgomery doesn't soften it. The bank failure, the heart attack, the simple finality — it's real grief, respectfully rendered. This chapter validates children's experience of loss.",
    38: "The ending is controversial: Anne gives up her scholarship to care for Marilla. Is this self-sacrifice or self-determination? Montgomery frames it as choice, not obligation — Anne chooses love over ambition, home over adventure. Gilbert's gift of the school makes it possible. The 'bend in the road' is Montgomery's mature vision: you can't see what's coming, but you can trust the road.",
}

THEMATIC_GROUPS = {
    "theme-belonging-and-identity": {
        "name": "Belonging and Identity",
        "description": "Anne's deepest need is to belong — to a family, a community, a place. These chapters trace her journey from unwanted orphan to beloved daughter of Avonlea, exploring how identity forms through relationship and place.",
        "for_parents": "Anne's hunger for belonging drives the entire novel. She has been passed from household to household, never chosen, never wanted. Green Gables is the first place that becomes home, and her fierce attachment to it grows from profound need. These chapters are especially powerful for adopted children, foster children, or any child who has felt like an outsider. The message is clear: belonging is not about blood — it's about love, choice, and showing up.",
        "keywords": ["belonging", "identity", "orphan", "home", "family", "acceptance"],
        "chapters": [2, 3, 4, 5, 6, 25, 34, 38],
    },
    "theme-imagination-and-beauty": {
        "name": "Imagination and the Love of Beauty",
        "description": "Anne sees the world through a lens of wonder — she renames places, tells stories, and transforms the ordinary into the magnificent. These chapters celebrate the imagination as a source of joy, resilience, and connection to the world.",
        "for_parents": "Anne's imagination is both her greatest gift and her greatest challenge. It lets her see beauty everywhere and survive hardship through storytelling, but it also leads her into trouble (the Haunted Wood, the ridgepole, the liniment cake). Montgomery treats imagination with respect and nuance: it is valuable, but it must be balanced with practical attention. These chapters are wonderful for creative, dreamy children who sometimes struggle in structured settings.",
        "keywords": ["imagination", "beauty", "stories", "naming", "wonder", "creativity"],
        "chapters": [2, 4, 13, 20, 26, 28, 31],
    },
    "theme-scrapes-and-growing-pains": {
        "name": "Scrapes and Growing Pains",
        "description": "Anne's childhood is a series of spectacular mishaps — smashed slates, green hair, liniment cakes, and near-drownings. Each disaster teaches her something, and each recovery makes her stronger.",
        "for_parents": "Montgomery uses Anne's scrapes as a philosophy of education: children learn through mistakes, not through perfection. Each disaster has consequences, but also lessons. Anne doesn't repeat her worst mistakes — she grows from them. These chapters are reassuring for parents of impulsive, dramatic children: the same intensity that creates problems also drives achievement.",
        "keywords": ["mistakes", "growing-up", "lessons", "scrapes", "impulsive", "learning"],
        "chapters": [9, 14, 15, 16, 19, 21, 23, 27],
    },
    "theme-quiet-love": {
        "name": "Quiet Love",
        "description": "Matthew's shy devotion, Marilla's hidden tenderness, and the community's gradual acceptance of Anne. Love in this book is rarely spoken aloud — it is shown through puffed sleeves, open doors, and the decision to keep an orphan girl when a boy was ordered.",
        "for_parents": "Montgomery understands that love is often inarticulate. Matthew can barely speak to women but buys Anne puffed sleeves. Marilla frames everything as duty but acts from the heart. Mrs. Lynde criticizes but cares. These chapters show children that love doesn't always look the way it does in stories — sometimes it's a shy man's quiet attention or a stern woman's decision to keep trying.",
        "keywords": ["love", "matthew", "marilla", "quiet", "devotion", "family"],
        "chapters": [2, 6, 8, 25, 30, 37, 38],
    },
    "theme-rivalry-and-friendship": {
        "name": "Rivalry and Friendship",
        "description": "Anne's relationships define her — the bosom friendship with Diana, the fierce rivalry with Gilbert, the mentorship of Miss Stacy. These chapters explore how connection shapes who we become.",
        "for_parents": "Anne's friendships and rivalries model different kinds of relationships. Diana provides unconditional acceptance; Gilbert provides challenge and competition; Miss Stacy provides intellectual nurture. All three are necessary. The Anne-Gilbert dynamic is especially interesting for older children: their rivalry masks respect and attraction, and Anne's refusal to forgive teaches a lesson about pride that she eventually learns herself.",
        "keywords": ["friendship", "rivalry", "diana", "gilbert", "miss-stacy", "connection"],
        "chapters": [12, 15, 17, 18, 29, 32, 35],
    },
    "theme-ambition-and-sacrifice": {
        "name": "Ambition and Sacrifice",
        "description": "Anne's academic ambition drives the second half of the novel — the Queen's class, the entrance exams, the Avery Scholarship. But the story ends with sacrifice: giving up the scholarship to stay with Marilla. These chapters explore what we strive for and what we're willing to give up.",
        "for_parents": "Montgomery presents ambition as a virtue — Anne works fiercely and honestly for her achievements. But the ending complicates this: Anne gives up her hard-won scholarship to care for Marilla. Is this retreat or maturity? Montgomery frames it as choice — Anne chooses relationship over personal advancement. This tension between ambition and love is one the book never fully resolves, which makes it honest.",
        "keywords": ["ambition", "scholarship", "sacrifice", "achievement", "choice", "duty"],
        "chapters": [30, 32, 35, 36, 37, 38],
    },
}


def read_and_strip_gutenberg(filepath):
    """Read the seed text and strip Gutenberg header/footer."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK ANNE OF GREEN GABLES ***"
    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[start_idx + len(start_marker):]

    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK ANNE OF GREEN GABLES ***"
    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]

    return text.strip()


def roman_to_int(s):
    """Convert Roman numeral string to integer."""
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50}
    result = 0
    for i, c in enumerate(s):
        if i + 1 < len(s) and values[c] < values[s[i + 1]]:
            result -= values[c]
        else:
            result += values[c]
    return result


def split_into_chapters(text):
    """Split the full text into chapters.

    Anne of Green Gables uses: CHAPTER I. Title Here
    """
    chapter_pattern = re.compile(
        r'^CHAPTER\s+((?:X{0,3})(?:IX|IV|V?I{0,3}))\.\s+(.+?)$',
        re.MULTILINE
    )

    matches = list(chapter_pattern.finditer(text))
    chapters = {}

    for i, match in enumerate(matches):
        roman = match.group(1)
        chapter_num = roman_to_int(roman)

        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()

        # Clean up extra blank lines
        content = re.sub(r'\n{4,}', '\n\n\n', content)

        chapters[chapter_num] = content

    return chapters


def get_chapter_keywords(chapter_num):
    """Return keywords for a chapter."""
    keywords_map = {
        1: ["mrs-lynde", "avonlea", "community", "cuthberts", "adoption"],
        2: ["matthew", "train", "anne", "imagination", "first-meeting"],
        3: ["marilla", "unwanted", "orphan", "decision", "tears"],
        4: ["green-gables", "morning", "beauty", "naming", "cherry-tree"],
        5: ["history", "orphan", "past", "hardship", "resilience"],
        6: ["decision", "keeping-anne", "duty", "love", "belonging"],
        7: ["prayer", "religion", "sincerity", "unconventional"],
        8: ["rules", "housework", "education", "daydreaming"],
        9: ["mrs-lynde", "anger", "red-hair", "pride", "outburst"],
        10: ["apology", "performance", "humility", "forgiveness"],
        11: ["church", "wildflowers", "hat", "convention", "individuality"],
        12: ["diana", "bosom-friend", "vow", "friendship", "belonging"],
        13: ["anticipation", "picnic", "joy", "waiting", "excitement"],
        14: ["confession", "brooch", "lie", "truth", "justice"],
        15: ["gilbert", "carrots", "slate", "rivalry", "school"],
        16: ["diana", "currant-wine", "tragedy", "separation", "injustice"],
        17: ["studying", "miss-stacy", "mentor", "academics", "coping"],
        18: ["croup", "minnie-may", "rescue", "healing", "competence"],
        19: ["concert", "ridgepole", "dare", "danger", "confession"],
        20: ["haunted-wood", "fear", "imagination", "self-scaring"],
        21: ["liniment", "cake", "domestic-disaster", "embarrassment"],
        22: ["tea", "manse", "poise", "grace", "growth"],
        23: ["ridgepole", "fall", "injury", "reflection", "maturing"],
        24: ["concert", "recitation", "miss-stacy", "performance", "talent"],
        25: ["matthew", "puffed-sleeves", "dress", "love", "attention"],
        26: ["story-club", "writing", "creativity", "melodrama"],
        27: ["hair-dye", "vanity", "green-hair", "identity", "self-acceptance"],
        28: ["lily-maid", "elaine", "boat", "gilbert", "rescue"],
        29: ["forgiveness", "gilbert", "pride", "maturity", "epoch"],
        30: ["queens-class", "exam", "competition", "ambition", "study"],
        31: ["transition", "brook-river", "growing-up", "threshold"],
        32: ["pass-list", "results", "tied", "achievement", "pride"],
        33: ["hotel-concert", "performance", "wider-world", "sponsorship"],
        34: ["queens-academy", "leaving-home", "homesickness", "independence"],
        35: ["queens", "scholarship", "avery", "hard-work", "winter"],
        36: ["homecoming", "triumph", "avery-scholarship", "celebration"],
        37: ["matthew", "death", "bank-failure", "grief", "loss"],
        38: ["sacrifice", "scholarship", "marilla", "gilbert", "bend-in-road"],
    }
    return keywords_map.get(chapter_num, [])


def build_grammar():
    """Build the complete Anne of Green Gables grammar."""
    text = read_and_strip_gutenberg(SEED_FILE)
    chapters = split_into_chapters(text)

    if len(chapters) != 38:
        print(f"WARNING: Expected 38 chapters, found {len(chapters)}: {sorted(chapters.keys())}")

    items = []
    sort_order = 0
    chapter_ids = {}

    # === L1: Individual chapters ===
    for chapter_num in sorted(chapters.keys()):
        sort_order += 1
        item_id = f"chapter-{chapter_num:02d}"
        chapter_ids[chapter_num] = item_id

        chapter_text = chapters[chapter_num]

        item = {
            "id": item_id,
            "name": f"Chapter {chapter_num}: {CHAPTER_TITLES[chapter_num]}",
            "sort_order": sort_order,
            "category": f"chapter-{chapter_num:02d}",
            "level": 1,
            "sections": {
                "Story": chapter_text,
                "Reflection": CHAPTER_REFLECTIONS.get(chapter_num, "What does this chapter make you think about?"),
                "For Parents": CHAPTER_PARENT_NOTES.get(chapter_num, ""),
            },
            "keywords": get_chapter_keywords(chapter_num),
            "metadata": {
                "chapter_number": chapter_num,
                "chapter_name": CHAPTER_TITLES[chapter_num],
            },
        }
        items.append(item)

    # === L2: Chapter summaries ===
    for chapter_num in sorted(chapters.keys()):
        sort_order += 1
        summary_id = f"summary-chapter-{chapter_num:02d}"

        item = {
            "id": summary_id,
            "name": f"Summary: {CHAPTER_TITLES[chapter_num]}",
            "sort_order": sort_order,
            "category": "chapter-summary",
            "level": 2,
            "relationship_type": "emergence",
            "composite_of": [chapter_ids[chapter_num]],
            "sections": {
                "About": CHAPTER_SUMMARIES.get(chapter_num, ""),
                "For Parents": CHAPTER_PARENT_NOTES.get(chapter_num, ""),
            },
            "keywords": get_chapter_keywords(chapter_num),
            "metadata": {
                "chapter_number": chapter_num,
                "chapter_name": CHAPTER_TITLES[chapter_num],
            },
        }
        items.append(item)

    # === L2: Thematic groups ===
    for theme_id, theme_data in THEMATIC_GROUPS.items():
        sort_order += 1

        theme_chapter_ids = [chapter_ids[ch] for ch in theme_data["chapters"] if ch in chapter_ids]

        item = {
            "id": theme_id,
            "name": theme_data["name"],
            "sort_order": sort_order,
            "category": "theme",
            "level": 2,
            "relationship_type": "emergence",
            "composite_of": theme_chapter_ids,
            "sections": {
                "About": theme_data["description"],
                "For Parents": theme_data["for_parents"],
            },
            "keywords": theme_data["keywords"],
            "metadata": {},
        }
        items.append(item)

    # === L3: Meta-categories ===
    all_summary_ids = [f"summary-chapter-{n:02d}" for n in sorted(chapters.keys())]
    all_theme_ids = list(THEMATIC_GROUPS.keys())

    sort_order += 1
    items.append({
        "id": "meta-the-story",
        "name": "The Story",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "relationship_type": "emergence",
        "composite_of": all_summary_ids,
        "sections": {
            "About": "The complete narrative of Anne of Green Gables: an unwanted orphan girl arrives at a Prince Edward Island farm, transforms the lives of everyone she meets through the sheer force of her imagination and love, and grows from a wild, talkative child into a young woman who chooses love over ambition. Thirty-eight chapters trace Anne Shirley's journey from the train station to the bend in the road, carried by her fierce imagination, her hunger for belonging, and her refusal to be anyone other than herself.",
            "For Parents": "Anne of Green Gables has endured for over a century because it tells the truth about childhood — the intensity, the drama, the scrapes, and the growth. Montgomery respects children's feelings without patronizing them. The book argues that difficult children are often gifted children, that imagination is a survival skill, and that love can be quiet and still be fierce. Read it together and trust the story to do its work.",
        },
        "keywords": ["complete-story", "narrative", "anne-shirley", "chapters"],
        "metadata": {},
    })

    sort_order += 1
    items.append({
        "id": "meta-themes",
        "name": "Themes",
        "sort_order": sort_order,
        "category": "meta",
        "level": 3,
        "relationship_type": "emergence",
        "composite_of": all_theme_ids,
        "sections": {
            "About": "The great themes of Anne of Green Gables — belonging and identity, imagination and beauty, scrapes and growing pains, quiet love, rivalry and friendship, and ambition and sacrifice. These groupings reveal how Montgomery weaves together the personal and the universal, making one girl's story into a mirror for every reader.",
            "For Parents": "These thematic groupings help you explore the novel beyond the plot. Each theme connects chapters that share a common thread. If your child identifies with Anne's outsider status, start with 'Belonging and Identity.' If they love Anne's disasters, 'Scrapes and Growing Pains' provides the laughs and the lessons. The story speaks to every reader differently — let your child find their own way in.",
        },
        "keywords": ["themes", "analysis", "groupings", "perspectives"],
        "metadata": {},
    })

    # === Build the grammar ===
    grammar = {
        "_grammar_commons": {
            "schema_version": "1.0",
            "license": "CC-BY-SA-4.0",
            "attribution": [
                {
                    "name": "L.M. Montgomery",
                    "date": "1908",
                    "note": "Original author of Anne of Green Gables",
                },
                {
                    "name": "Project Gutenberg",
                    "date": "2008",
                    "note": "eBook #45 — produced by David Widger and Charles Keller",
                },
                {
                    "name": "PlayfulProcess",
                    "date": "2026-03-04",
                    "note": "Grammar construction, chapter summaries, and thematic groupings",
                },
            ],
        },
        "name": "Anne of Green Gables",
        "description": (
            "L.M. Montgomery's Anne of Green Gables (1908) — the story of Anne Shirley, "
            "a fierce, imaginative orphan who transforms the quiet community of Avonlea, "
            "Prince Edward Island, through the sheer force of her personality, her love of beauty, "
            "and her hunger for belonging. From the train station to the bend in the road, "
            "thirty-eight chapters trace Anne's journey from unwanted child to beloved daughter, "
            "exploring imagination, resilience, friendship, and the quiet power of love.\n\n"
            "Source: Project Gutenberg eBook #45 (https://www.gutenberg.org/ebooks/45).\n\n"
            "PUBLIC DOMAIN ILLUSTRATION REFERENCES:\n"
            "- M.A. and W.A.J. Claus (1908, L.C. Page & Company) — original edition illustrators, "
            "black-and-white plates capturing Anne's arrival and Avonlea life\n"
            "- Elizabeth Chicken (1933, Harrap) — beloved British edition illustrations with soft, "
            "pastoral watercolors of Prince Edward Island\n"
            "- Sybil Tawse (1933, Pitman) — delicate pen-and-ink drawings"
        ),
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "tags": [
            "children",
            "classic",
            "imagination",
            "resilience",
            "belonging",
            "public-domain",
            "l-m-montgomery",
            "full-text",
            "chapters",
            "multi-level",
            "canada",
        ],
        "roots": ["wonder-imagination"],
        "shelves": ["children"],
        "lineages": ["Linehan", "Andreotti"],
        "worldview": "imaginative",
        "items": items,
    }

    return grammar


def main():
    print(f"Reading seed text from {SEED_FILE}...")
    grammar = build_grammar()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    items = grammar["items"]
    l1 = [i for i in items if i["level"] == 1]
    l2 = [i for i in items if i["level"] == 2]
    l3 = [i for i in items if i["level"] == 3]

    print(f"Grammar written to {OUTPUT_FILE}")
    print(f"  L1 chapters: {len(l1)}")
    print(f"  L2 summaries + themes: {len(l2)}")
    print(f"  L3 meta-categories: {len(l3)}")
    print(f"  Total items: {len(items)}")

    # Self-check
    ids = [i["id"] for i in items]
    id_set = set(ids)
    dupes = len(ids) - len(id_set)
    if dupes:
        print(f"  WARNING: {dupes} duplicate IDs found!")

    broken = []
    for item in items:
        for ref in item.get("composite_of", []):
            if ref not in id_set:
                broken.append((item["id"], ref))
    if broken:
        print(f"  WARNING: {len(broken)} broken references:")
        for item_id, ref in broken:
            print(f"    {item_id} -> {ref}")


if __name__ == "__main__":
    main()
