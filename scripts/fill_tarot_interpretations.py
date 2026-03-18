#!/usr/bin/env python3
"""
Fill the 390 stub sections in the Tarot of All Tarots grammar.

For each of 78 cards, generates 5 interpretive sections:
  Archetype, Professional, Relationship, Consciousness, Shadow

Uses lookup tables for suit/number/major symbolism + each card's existing
keywords and RWS summary text as seeds. No AI inference — runs in seconds.
"""

import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAMMAR_PATH = os.path.join(BASE, "grammars", "tarot-of-all-tarots", "grammar.json")

# ─── Suit symbolism ──────────────────────────────────────────────────────────

SUIT_DATA = {
    "wands": {
        "element": "Fire",
        "domain": "will, passion, creativity, ambition",
        "professional": "entrepreneurship, creative projects, leadership, initiative",
        "relationship": "passion, attraction, adventure, sexual energy, shared vision",
        "consciousness": "purpose, vitality, the creative spark, kundalini energy",
        "shadow": "burnout, ego-driven ambition, restlessness, aggression",
    },
    "cups": {
        "element": "Water",
        "domain": "emotion, intuition, love, the unconscious",
        "professional": "emotional intelligence, team harmony, creative flow, empathy in leadership",
        "relationship": "love, intimacy, emotional bonding, vulnerability, family",
        "consciousness": "the feeling body, dreams, psychic sensitivity, devotion",
        "shadow": "emotional overwhelm, codependency, escapism, illusion",
    },
    "swords": {
        "element": "Air",
        "domain": "intellect, truth, conflict, clarity",
        "professional": "analysis, strategy, difficult decisions, honest communication",
        "relationship": "communication, conflict resolution, truth-telling, boundaries",
        "consciousness": "discernment, mental clarity, cutting through illusion, meditation on thought",
        "shadow": "overthinking, cruelty, anxiety, weaponized intellect, isolation",
    },
    "pentacles": {
        "element": "Earth",
        "domain": "material world, body, craft, abundance",
        "professional": "career building, financial planning, skill mastery, long-term investment",
        "relationship": "stability, commitment, building a home, shared resources, sensual grounding",
        "consciousness": "embodiment, presence, connection to nature, the sacred in the material",
        "shadow": "greed, workaholism, materialism, stagnation, hoarding",
    },
}

# ─── Number symbolism (for pips 1-10) ────────────────────────────────────────

NUMBER_DATA = {
    1: {
        "stage": "seed, pure potential, the gift offered",
        "professional": "A new opportunity arrives — raw and unformed. This is the spark before the plan, the offer before the negotiation. Accept it before your mind talks you out of it.",
        "relationship": "The beginning of something. A first meeting, a rekindled spark, or the sudden arrival of a feeling you weren't expecting. Don't analyze it yet — just feel it.",
        "consciousness": "Pure potential entering your field. The universe extends a hand. The only question is whether you'll take it.",
        "shadow": "Missed opportunities. Refusing the gift because the packaging isn't what you expected. Potential that stays forever potential.",
    },
    2: {
        "stage": "duality, balance, choice, partnership",
        "professional": "A decision between two paths. Partnerships and negotiations. The need to weigh options carefully before committing resources.",
        "relationship": "The dance of two. Balance between giving and receiving. A relationship at the point where both parties must choose engagement or withdrawal.",
        "consciousness": "The experience of polarity — light/dark, inner/outer, self/other. Sitting with paradox rather than resolving it prematurely.",
        "shadow": "Indecision that becomes paralysis. Playing both sides. Avoiding commitment by keeping all options perpetually open.",
    },
    3: {
        "stage": "creation, expression, initial fruition, collaboration",
        "professional": "First results from collaboration. Creative output becomes visible. Teamwork produces something none could make alone.",
        "relationship": "The relationship bears fruit — a child, a project, a shared creation. Joy in what you've built together. Celebration of growth.",
        "consciousness": "Creative expression as spiritual practice. The trinity of body, mind, and spirit in alignment. What you create reveals who you are.",
        "shadow": "Scattered energy. Too many collaborations diluting focus. Superficial results from insufficient depth.",
    },
    4: {
        "stage": "structure, stability, foundation, consolidation",
        "professional": "Building solid foundations. Establishing systems and routines. The work isn't exciting, but it's essential. Structure enables future growth.",
        "relationship": "Stability and security. The comfortable routines of established love. But also the risk of taking stability for granted.",
        "consciousness": "Grounding. The four directions, the four elements. A time to consolidate what you know before seeking more.",
        "shadow": "Rigidity. Mistaking the structure for the thing it protects. Control disguised as care. Stagnation mistaken for stability.",
    },
    5: {
        "stage": "disruption, conflict, change, crisis as teacher",
        "professional": "Disruption and challenge. Plans are tested. Loss may precede necessary change. The question isn't whether difficulty comes, but what you learn from it.",
        "relationship": "Conflict surfaces what was hidden. Arguments that reveal deeper needs. The relationship faces a test that could strengthen or break it.",
        "consciousness": "The dark night of the soul — mild or severe. Old structures crack so new growth can emerge. Suffering as initiation.",
        "shadow": "Victimhood. Refusing to learn from difficulty. Creating conflict to avoid intimacy. Self-fulfilling prophecies of failure.",
    },
    6: {
        "stage": "harmony, reciprocity, generosity, equilibrium restored",
        "professional": "Generosity and fair exchange. Giving and receiving in balance. Success shared with others. Mentorship and earned reward.",
        "relationship": "Harmony restored. Giving and receiving in equal measure. Nostalgia for simpler times. Acts of kindness that strengthen bonds.",
        "consciousness": "The beauty of balance. Generosity as a spiritual practice. Recognizing that what you give returns to you in altered form.",
        "shadow": "Inequality disguised as generosity. Power dynamics in giving. Nostalgia that prevents presence. Keeping score.",
    },
    7: {
        "stage": "reflection, assessment, inner work, perseverance",
        "professional": "Strategic patience. Assessing progress before the next move. Not everything yields to effort — some things require faith and waiting.",
        "relationship": "Taking stock of the relationship. What is it becoming? Patience with growth that can't be rushed. Inner work that benefits the partnership.",
        "consciousness": "The mystic number. Seven chakras, seven days of creation. A time for introspection, meditation, and trusting the process.",
        "shadow": "Paralysis by analysis. Waiting when action is needed. Using 'inner work' as an excuse to avoid outer engagement.",
    },
    8: {
        "stage": "mastery, movement, power, acceleration",
        "professional": "Rapid development. Skills coming together. Mastery through repetition and dedication. Things are moving fast — stay focused.",
        "relationship": "A relationship gaining momentum. Quick developments. The energy is strong — channel it wisely rather than letting it scatter.",
        "consciousness": "The infinity loop — mastery that circles back to beginner's mind. Power that comes from alignment, not force.",
        "shadow": "Haste. Mistaking speed for progress. Power without wisdom. Burnout from unsustainable acceleration.",
    },
    9: {
        "stage": "culmination, near-completion, wisdom earned, solitude",
        "professional": "Near the summit. Most of the work is done. A time for final refinement rather than new initiatives. The wisdom of experience.",
        "relationship": "A mature relationship with deep roots. Self-sufficiency within partnership. The wisdom that comes from having weathered many seasons together.",
        "consciousness": "The hermit's number. Wisdom earned through experience. Nearing the end of a cycle with the awareness to appreciate the journey.",
        "shadow": "Isolation. Guarding what you've built so fiercely that you can't share it. Near-completion anxiety. Perfectionism that prevents finishing.",
    },
    10: {
        "stage": "completion, legacy, fullness, the cycle turning",
        "professional": "A cycle complete. Legacy and inheritance — what you've built will outlast the effort. But completion also means a new beginning approaches.",
        "relationship": "Family, lineage, the full weight of love sustained over time. The blessing and burden of everything you've built together.",
        "consciousness": "The wheel turns full circle. One journey ends, another begins. The 10 contains the 1 — completion holds the seed of new beginning.",
        "shadow": "Burden. Carrying too much. The weight of completion without renewal. Endings resisted. Legacy as chain rather than gift.",
    },
}

# ─── Court card symbolism ────────────────────────────────────────────────────

COURT_DATA = {
    "page": {
        "role": "student, messenger, beginner, the young explorer",
        "professional": "A new student or apprentice energy. Fresh ideas, willingness to learn, a message arriving about opportunities. The courage to begin without mastery.",
        "relationship": "Youthful energy in love — curiosity, playfulness, the thrill of discovery. Can indicate a young person, or the young part of anyone experiencing something new.",
        "consciousness": "Beginner's mind. The willingness to not know. Approaching the mystery with curiosity rather than expertise.",
        "shadow": "Immaturity. All enthusiasm, no follow-through. Naivety mistaken for wisdom. Avoiding growth by perpetually staying the beginner.",
    },
    "knight": {
        "role": "quester, champion, extremist, the one who charges",
        "professional": "Charging toward a goal with single-minded focus. The energy is intense and directional. Great for launching, risky for nuance.",
        "relationship": "Passionate pursuit — romantic, intense, sometimes overwhelming. The knight courts or rescues, but may struggle with the quieter work of sustaining.",
        "consciousness": "The quest as spiritual path. Seeking truth with the whole body. The danger is confusing the seeking with the finding.",
        "shadow": "Fanaticism. Charging without looking. Mistaking intensity for depth. The crusader who destroys what they meant to save.",
    },
    "queen": {
        "role": "nurturer, embodiment, inward mastery, the one who holds",
        "professional": "Mastery expressed through nurturing — building teams, creating culture, holding space for others' growth. Influence through presence, not force.",
        "relationship": "Deep emotional intelligence in partnership. The capacity to hold complexity, nurture growth, and create sanctuary. Receptive power.",
        "consciousness": "Inward mastery. The element fully internalized and expressed through being rather than doing. Wisdom embodied.",
        "shadow": "Manipulation through caretaking. Smothering. Passive aggression. Using emotional mastery to control rather than liberate.",
    },
    "king": {
        "role": "sovereign, outward mastery, authority, the one who commands",
        "professional": "Full authority and competence. Leadership from experience. The responsibility to wield power wisely and for others' benefit.",
        "relationship": "Maturity, stability, protection. The partner who shows up fully formed — reliable but potentially rigid. Authority in the family system.",
        "consciousness": "Outward mastery. The element fully expressed in the world. But the king's throne can become a prison — sovereignty requires continued growth.",
        "shadow": "Tyranny. Rigidity masquerading as strength. Using authority to avoid vulnerability. The king who forgot he was once a page.",
    },
}

# ─── Major Arcana archetypes ─────────────────────────────────────────────────

MAJOR_DATA = {
    0: {
        "archetype": "The eternal beginner. Zero contains everything and nothing — the void before creation, the leap before the landing. Every journey begins with the Fool's willingness to step into the unknown without a map. This is not ignorance but a radical openness that the experienced have forgotten.",
        "professional": "You are being called to begin something without guarantee of success. The Fool in career readings says: take the leap. Start the business, change the field, propose the idea that scares you. Your lack of experience is actually your advantage — you'll see what the experts can't.",
        "relationship": "Fall in love with the falling. The Fool brings the energy of new romance — exhilarating, terrifying, completely irrational. In established relationships, it asks: where have you stopped being surprised? Bring beginner's mind back to someone you think you know.",
        "consciousness": "The Fool is the consciousness before it identifies with any role or story. In meditation, this is the space between thoughts. In spiritual life, it's the willingness to abandon everything you think you know about enlightenment and just... walk.",
        "shadow": "Recklessness disguised as freedom. Refusing to learn from experience. Serial beginning without completion. The spiritual tourist who collects initiations but never commits to practice. Naivety weaponized against those asking reasonable questions.",
    },
    1: {
        "archetype": "The channel between above and below, the one who makes the invisible visible. The Magician doesn't create from nothing — they arrange what's already present into new configurations. One hand points to heaven, the other to earth: 'As above, so below.' This is the archetype of conscious creation through focused will.",
        "professional": "You have all the tools you need — they're on the table in front of you. The Magician says: stop gathering resources and start combining them. Communication, initiative, and skill converge now. A powerful time for pitching, presenting, or launching.",
        "relationship": "Conscious communication transforms a relationship. The Magician brings charisma and intentionality — the power to create the dynamic you want through clear speech and focused attention. But ensure you're creating WITH someone, not performing AT them.",
        "consciousness": "The awakened will. The realization that consciousness is not passive — it actively shapes reality through attention and intention. This is the archetype behind every meditation practice, every prayer, every act of deliberate creation.",
        "shadow": "Manipulation. Using charisma and skill to deceive. The con artist, the smooth talker, the guru who uses spiritual language to control. Power without ethics. Technique without heart.",
    },
    2: {
        "archetype": "The keeper of hidden knowledge. She sits between the pillars of light and dark, holding a scroll she doesn't show you — not because you can't see it, but because some truths must be approached through silence. The High Priestess is intuition before it becomes thought, knowing before it becomes words.",
        "professional": "Trust your gut. The data is incomplete, the rational analysis falls short, but something in you knows. The High Priestess in career matters says: listen to what isn't being said in the meeting, read between the lines of the contract, pay attention to the unease you can't explain.",
        "relationship": "The mystery at the heart of every relationship — the parts of your partner you'll never fully know, and the parts of yourself that emerge only in their presence. Honor the unknown. Stop trying to make everything explicit.",
        "consciousness": "Pure receptivity. The consciousness that receives rather than grasps. In meditation, this is the awareness that witnesses thoughts without engaging them. The lunar mind, the dream life, the voice that speaks in symbols.",
        "shadow": "Secrets that become lies. Withholding as power. Using mystery to avoid intimacy. The spiritual bypasser who retreats into 'inner knowing' to avoid engaging with messy human reality.",
    },
    3: {
        "archetype": "The Great Mother — not domesticated, not gentle, but fecund and wild. The Empress is nature's intelligence expressing through you: the body's wisdom, the creative impulse, the urge to nurture what you've brought into being. She is abundance without apology.",
        "professional": "A fertile period for creative work. Projects grow naturally now — nurture them with attention but don't over-manage. The Empress in career says: create beauty, tend to the workplace environment, lead through abundance rather than scarcity.",
        "relationship": "Sensual, nurturing, deeply embodied love. The Empress brings physical affection, domestic warmth, and the creation of beauty in shared spaces. If you want to improve a relationship, cook together, garden together, make something together.",
        "consciousness": "The body as sacred temple. The Empress is embodied spirituality — not transcendence but immanence. God is not above; God is in the soil, the bread, the lover's skin. Practice: notice where your body is right now.",
        "shadow": "Smothering. Over-identifying with the nurturer role. Creative overproduction without discernment. Using beauty or pleasure to avoid necessary pain. The devouring mother.",
    },
    4: {
        "archetype": "Structure that serves life. The Emperor builds the walls that protect the garden — without him, the Empress's abundance has no form. This is the archetype of benevolent authority: rules that create freedom, boundaries that enable growth, power exercised for the common good.",
        "professional": "Take charge. Build systems. Establish the structure that will sustain your vision long-term. The Emperor in career says: write the business plan, set the budget, hire the team, define the roles. Vision without structure is just daydreaming.",
        "relationship": "Stability, protection, and clear boundaries. The Emperor in relationships provides the structure within which love can safely grow — but must be careful not to become controlling. The question: are your rules protecting the relationship or protecting your ego?",
        "consciousness": "The ordered mind. The capacity to think systematically, to build mental models, to create frameworks for understanding. But consciousness is bigger than any framework — the Emperor must eventually bow to what he can't contain.",
        "shadow": "Tyranny. Rigidity. Control masquerading as protection. The father wound — authority experienced as oppression. Building walls so high that nothing new can enter.",
    },
    5: {
        "archetype": "The bridge between the human and the divine — not through private mysticism but through shared tradition. The Hierophant represents teaching, initiation, and the living transmission of wisdom through community. He is the structure of spiritual practice itself.",
        "professional": "Mentorship, institutional knowledge, and established paths. The Hierophant in career says: find a teacher, follow the proven method, respect the tradition before you innovate. Sometimes the conventional path IS the right path.",
        "relationship": "Commitment formalized — marriage, vows, shared spiritual practice. The Hierophant in relationships asks: what is the sacred container holding your love? Shared values, shared rituals, shared community strengthen bonds.",
        "consciousness": "The role of tradition in spiritual growth. Not all structures are prisons — some are ladders. Meditation techniques, prayer practices, initiatory lineages: these are the Hierophant's gifts. The question is whether you're learning from the tradition or hiding behind it.",
        "shadow": "Dogma. Spiritual authority used to control. The institution that protects itself at the expense of the people it serves. Conformity mistaken for belonging. Shame-based religion.",
    },
    6: {
        "archetype": "The moment of choice that defines everything after. The Lovers is not merely romance — it's the archetype of conscious choice, of values clarified through the experience of desire. When you choose one path, you release all others. This is the card of commitment born from genuine attraction.",
        "professional": "A significant choice that will define your professional identity. Partnerships, mergers, or value-based decisions. The Lovers in career says: choose what you love, not what's safe. But choose — ambivalence is its own decision.",
        "relationship": "Deep attraction, soul-level connection, and the terrifying vulnerability of truly choosing another person. The Lovers asks: are you choosing this relationship freely, or are you choosing it by default? Real love requires real choice.",
        "consciousness": "The union of opposites within the self — masculine and feminine, conscious and unconscious, human and divine. The alchemical marriage. The moment when duality becomes dialogue rather than division.",
        "shadow": "Temptation without discernment. Choice avoided through distraction. The inability to commit because something better might come along. Desire disconnected from values. Betrayal.",
    },
    7: {
        "archetype": "Directed will moving through the world. The Chariot doesn't meander — it chooses a direction and moves with the full force of aligned intention. The sphinxes pulling it represent opposing forces (light/dark, conscious/unconscious) held in dynamic tension by the charioteer's mastery.",
        "professional": "Momentum and determination. The Chariot in career says: you know what you want — now go get it. Overcome obstacles through sheer force of will and strategic direction. This is the energy of the product launch, the campaign push, the finishing sprint.",
        "relationship": "Moving a relationship forward through active effort. The Chariot in love says: don't wait for things to happen — create the direction. Plan the trip, have the conversation, make the move. But ensure you're driving together, not dragging your partner along.",
        "consciousness": "The mastery of opposing inner forces — not by suppressing one side but by holding both in creative tension. This is the discipline of meditation: thoughts pull in every direction, and you hold the reins without fighting them.",
        "shadow": "Bulldozing. Steamrolling others in pursuit of your goal. Confusing stubbornness with determination. Road rage of the soul — directed aggression masquerading as purpose. Control that crushes what it touches.",
    },
    8: {
        "archetype": "Courage that comes from compassion, not conquest. Strength is not the warrior's brute force but the calm hand on the lion's jaw — the power to face what is wild and fierce (in the world, in yourself) with gentleness. True strength bends without breaking.",
        "professional": "Quiet persistence through difficulty. Strength in career says: this isn't a problem you can solve with force or cleverness — it requires patience, endurance, and inner fortitude. Lead through calm presence, not loud authority.",
        "relationship": "The courage to be vulnerable. Strength in love says: open your heart even when it's been hurt before. Tame the fierce parts of yourself not through suppression but through compassion. Love the lion; don't cage it.",
        "consciousness": "The integration of instinct and awareness. Strength is what happens when you stop fighting your animal nature and start working WITH it. The tantric path: transforming raw energy into wisdom through acceptance rather than rejection.",
        "shadow": "Repression disguised as composure. 'Keeping it together' at the cost of authenticity. Using gentleness to avoid necessary confrontation. Self-control that becomes self-imprisonment.",
    },
    9: {
        "archetype": "The lamp in the darkness, carried by one who walks alone. The Hermit has left the marketplace not to escape the world but to find something the world can't give — the inner light that only solitude reveals. This is the archetype of the seeker, the sage, the introvert's deepest gift.",
        "professional": "Step back from the noise. The Hermit in career says: you need time alone to think. The answer won't come from another meeting or more data — it will come from quiet reflection. Take the retreat, close the door, do the deep work.",
        "relationship": "Healthy solitude within partnership. The Hermit in love says: needing time alone doesn't mean you love less — it means you need to refill the well that love draws from. A relationship that can't tolerate solitude can't sustain intimacy.",
        "consciousness": "The contemplative path. Meditation, retreat, the long slow work of self-knowledge. The Hermit's lamp is not for showing others the way — it's for illuminating the path immediately before your own feet.",
        "shadow": "Isolation masquerading as wisdom. Using spiritual seeking to avoid human connection. The hermit who has been alone so long they've forgotten how to come back. Withdrawal as passive aggression.",
    },
    10: {
        "archetype": "The turning point that no one controls. The Wheel of Fortune is the great leveler — what goes up comes down, what falls will rise, and the only constant is change itself. This is fate, karma, the impersonal cycles of existence. Your job is not to stop the wheel but to find the still point at its center.",
        "professional": "Change is coming whether you plan for it or not. The Wheel in career says: ride the upswings with gratitude and the downswings with grace. Position yourself at the center of change rather than clinging to the rim.",
        "relationship": "Relationships cycle through seasons — growth, stability, challenge, renewal. The Wheel says: this too shall pass, whether 'this' is difficulty or bliss. What remains is the commitment to stay on the ride together.",
        "consciousness": "The meditation on impermanence. The Wheel teaches the Buddhist truth: attachment to any state — even joy — creates suffering. Freedom is found not in controlling circumstances but in witnessing them with equanimity.",
        "shadow": "Fatalism. Using 'it's meant to be' to avoid taking responsibility. Gambling with life instead of engaging with it. Blaming luck for what effort could change.",
    },
    11: {
        "archetype": "The reckoning that cannot be avoided. Justice is not punishment but natural consequence — the universe's way of maintaining balance. What you have sown, you will reap. This card asks not 'are you innocent?' but 'are you honest?' The scales weigh truth, not intention.",
        "professional": "Legal matters, contracts, and accountability. Justice in career says: be scrupulously honest — every shortcut will be found, every promise will be tested. Fairness in negotiations creates lasting partnerships.",
        "relationship": "Accountability in love. Justice asks: are you treating your partner fairly? Are the scales balanced — effort, attention, sacrifice? If something feels unjust, it probably is, and ignoring it won't restore balance.",
        "consciousness": "Karma as teacher, not punisher. Justice in consciousness says: every action has consequences in the inner world as well as the outer. Self-honesty is the prerequisite for every other spiritual virtue.",
        "shadow": "Harsh judgment — of self or others. Legalism without mercy. Using 'fairness' to justify cruelty. The inability to forgive, dressed up as moral clarity.",
    },
    12: {
        "archetype": "The wisdom that comes only from surrender. The Hanged Man hangs willingly — not tortured but transformed by choosing to see the world from a completely different angle. What looks like sacrifice from outside is revelation from within. The ego's loss is the soul's gain.",
        "professional": "Pause. The Hanged Man in career says: stop pushing. The answer will come not from more effort but from a radical change of perspective. Sometimes the most productive thing you can do is nothing at all.",
        "relationship": "Sacrifice that transforms both giver and receiver. The Hanged Man in love asks: what would you willingly give up — control, being right, your timeline — to see your relationship from your partner's perspective?",
        "consciousness": "The mystical inversion. Ego death as liberation. The Hanged Man is the meditator who has stopped trying to achieve enlightenment and is simply hanging in the question. This is the way through, not around.",
        "shadow": "Martyrdom. Suffering for its own sake. Using self-sacrifice to manipulate others' guilt. Passivity disguised as surrender. Spiritual bypassing: 'I'm at peace with it' when you're actually frozen.",
    },
    13: {
        "archetype": "The great transformation that clears the way for new life. Death is not an ending but a threshold — the compost from which new growth emerges. What dies is the form, not the essence. The skeleton rides forward because Death never looks back. This is the most misunderstood and most necessary card in the deck.",
        "professional": "Something in your career is ending — a role, a project, a way of working. Death in career says: let it go. The job that served you for years no longer does. The business model needs to die for the new one to be born. Grieve, then move.",
        "relationship": "A relationship is transforming at the deepest level. Death in love doesn't mean breakup — it means the old version of 'us' must die so a new version can emerge. The couple who survives this card is reborn together.",
        "consciousness": "Ego death. The dissolution of who you thought you were, making space for who you actually are. Every genuine spiritual transformation involves a Death card. The caterpillar doesn't 'improve' into a butterfly — it dissolves entirely.",
        "shadow": "Resisting necessary endings. Keeping dead things alive through sheer will. The relationship, job, or belief system that should have been released years ago. Also: nihilism — glorifying destruction without honoring what's being born.",
    },
    14: {
        "archetype": "The art of finding the middle way. Temperance is the alchemist's card — mixing opposites into something greater than either. Fire and water, heaven and earth, patience and passion: this angel holds them all in balance. Not compromise (which weakens both) but integration (which strengthens both).",
        "professional": "Balance and integration in work life. Temperance in career says: the extremes aren't working. Find the middle path between overwork and disengagement, between vision and pragmatism, between innovation and reliability.",
        "relationship": "The art of blending two lives without losing either one. Temperance in love says: a good relationship isn't 50/50 — it's a third thing created from the unique combination of two wholes. Practice the alchemy of 'we' without dissolving the 'I.'",
        "consciousness": "The middle way of the Buddha. Integration of shadow and light. Temperance is the spiritual practice of holding paradox: being fully human AND fully divine, fully present AND fully surrendered.",
        "shadow": "Lukewarmness. Moderation as mediocrity. Avoiding passion because balance feels safer. Using 'both sides' rhetoric to avoid taking a stand. Diluting everything until nothing has flavor.",
    },
    15: {
        "archetype": "The chains you've chosen to wear. The Devil doesn't bind you — look closely and the chains are loose enough to remove. This is the archetype of addiction, materialism, and shadow contracts: the bargains you've made with parts of yourself you'd rather not acknowledge. Liberation begins with seeing the chains clearly.",
        "professional": "Golden handcuffs, toxic work cultures, and addictive patterns. The Devil in career says: what are you tolerating because you're afraid to lose the paycheck, the status, the security? Name the chain before you try to break it.",
        "relationship": "Codependency, power imbalances, and shadow dynamics. The Devil in love asks: where are you bound by fear rather than drawn by love? Toxic patterns repeat until they're made conscious. Look at what you'd rather not see.",
        "consciousness": "The shadow self. Everything you've denied, projected, or repressed. The Devil says: your liberation lives in the places you refuse to look. Jung's insight: 'Until you make the unconscious conscious, it will direct your life and you will call it fate.'",
        "shadow": "The shadow of the shadow — denying that you have a shadow at all. Spiritual materialism: using enlightenment language to avoid genuine self-confrontation. Also: wallowing in darkness without seeking the door.",
    },
    16: {
        "archetype": "The lightning strike that destroys false structures. The Tower is the most feared card in the deck — and the most liberating. What falls was built on shaky foundations. The crown blown off the top represents ego-structures, false beliefs, and institutions that served their time. Truth doesn't always knock politely.",
        "professional": "Sudden disruption — layoffs, market crashes, revelations that change everything. The Tower in career says: the old structure is falling. You can't stop it, but you can choose how you respond. Sometimes the building must come down so something true can be built.",
        "relationship": "The argument that changes everything. A revelation, a betrayal, or a truth that can no longer be contained. The Tower in love is painful but honest — what survives the lightning is what was real all along.",
        "consciousness": "Sudden awakening. The shattering of a worldview, the death of a belief system, the moment when everything you thought you knew falls away and you're left standing in the rubble, blinking, finally free. Zen calls this 'the bottom falling out of the bucket.'",
        "shadow": "Destruction without rebuilding. Tearing things down because it's easier than repairing them. Addiction to crisis and drama. Using 'radical honesty' as a weapon. Burning bridges you'll need later.",
    },
    17: {
        "archetype": "Hope after the storm. The Star appears after the Tower's destruction — naked, vulnerable, and pouring water onto the earth and back into the pool. This is the archetype of renewal, grace, and the quiet confidence that emerges after you've survived the worst. The Star doesn't shout. She shines.",
        "professional": "Inspiration and renewed purpose after difficulty. The Star in career says: the crisis is over. Now is the time for vision, creativity, and gentle rebuilding. Trust your gifts — they survived the storm for a reason.",
        "relationship": "Vulnerability as strength. The Star in love says: strip away the armor, the performance, the protection — and let yourself be seen as you are. This is the intimacy that becomes possible only after the walls have come down.",
        "consciousness": "Grace. The Star is the spiritual experience of being held by something larger — not earned through practice but given freely. Hope that doesn't deny suffering but exists alongside it. The light at the end that was always there.",
        "shadow": "False hope. Wishing instead of working. Using optimism to avoid grief. The inability to be present with darkness because you're always reaching for the light. Spiritual bypassing in its prettiest form.",
    },
    18: {
        "archetype": "The journey through the unconscious. The Moon illuminates not by revealing but by casting shadows — everything looks different in moonlight, and the path forward is unclear. This is the archetype of the dreamworld, of anxiety, of the imagination's power to create monsters and miracles from the same raw material.",
        "professional": "Confusion, uncertainty, and the need to navigate by intuition rather than logic. The Moon in career says: things aren't what they seem. Don't make major decisions now — wait for clarity. Trust your instincts when the data is unreliable.",
        "relationship": "The unconscious dynamics beneath the surface of love. Projections, fantasies, fears. The Moon in relationships asks: are you seeing your partner clearly, or are you seeing your own shadow reflected in the moonlight?",
        "consciousness": "The descent into the unconscious. Dreams, archetypal encounters, the dissolution of rational certainty. The Moon is the territory between waking and sleeping, between the known self and the vast unknown. Walk carefully, but walk.",
        "shadow": "Paranoia, illusion, and deception. Seeing threats that aren't there and missing the ones that are. Anxiety that feeds itself. Using intuition as an excuse for irrationality. Getting lost in the unconscious and forgetting the way back.",
    },
    19: {
        "archetype": "Joy without condition. The Sun shines on everyone equally — it doesn't ask whether you deserve it. This is the archetype of vitality, clarity, childlike delight, and the simple happiness of being alive. After the Moon's confusion, the Sun says: the world is exactly as beautiful as it looks right now.",
        "professional": "Success, visibility, and recognition. The Sun in career says: your work is being seen and appreciated. Enjoy the moment. Collaborate openly, share credit generously, and let your natural enthusiasm inspire others.",
        "relationship": "Warmth, joy, and playful connection. The Sun in love says: lighten up. Not everything needs to be processed, analyzed, or healed. Sometimes love is just two people laughing in the sunlight. Let it be easy.",
        "consciousness": "Enlightenment as simplicity. After all the mystical complexity of the Moon, the Sun says: the truth is simple. You are alive. The world is beautiful. This moment is enough. The child who doesn't know about darkness sees more clearly than the philosopher who knows too much.",
        "shadow": "Forced positivity. Toxic optimism. Insisting everything is fine when it isn't. The spiritual ego that has 'transcended' negative emotions. Burnout from performing happiness. Sunburn: too much light without shade.",
    },
    20: {
        "archetype": "The call you cannot refuse. Judgement is resurrection — the moment when everything buried rises to the surface for final accounting. This is not punishment but clarification: at last, you see your whole life clearly and can say 'yes' or 'no' to who you've been. The trumpet calls you to your truest self.",
        "professional": "A pivotal evaluation — of your career, your choices, your direction. Judgement in career says: everything you've done has led to this moment of reckoning. Be honest about what's working and what isn't. This is the time for radical career honesty.",
        "relationship": "A relationship reaches a moment of truth. Judgement in love says: look at everything — the good, the bad, the buried. Forgiveness and accountability are both required. The relationship either rises to a new level or acknowledges its end.",
        "consciousness": "The awakening of the deeper Self. In Jungian terms, this is individuation — hearing the call of who you actually are beneath all the roles and masks. Judgement says: the time for hiding is over. Answer the call.",
        "shadow": "Judging others instead of yourself. Using 'accountability' to avoid your own reckoning. Self-condemnation that disguises itself as spiritual seriousness. Refusing the call because answering it would require changing everything.",
    },
    21: {
        "archetype": "The dance of completion. The World is wholeness — not perfection but integration. All four elements, all four directions, all the lessons of the major arcana gathered into a single moment of knowing: you are complete, you are whole, and the journey continues. The World is both ending and beginning, both arrival and departure.",
        "professional": "A major cycle complete. The World in career says: celebrate what you've accomplished. This is graduation, the successful project, the vision realized. Savor it — and know that the Fool's next journey is already calling.",
        "relationship": "A relationship that has come full circle — deep, tested, whole. The World in love says: you've built something real. Not perfect, but complete. This is the relationship that has weathered every card in the deck and dances still.",
        "consciousness": "Integration. The World is the mandala — all parts of the self gathered into wholeness. This is not the end of growth but the completion of a cycle. In the World, you realize that you were always whole, always complete, always home.",
        "shadow": "Refusing to complete the cycle. Fear of the ending that makes way for new beginnings. Perfectionism that prevents finishing. The spiritual seeker who is always 'almost there' but never arrives. Also: completion without gratitude.",
    },
}


# ─── Generate content ─────────────────────────────────────────────────────────

def extract_core_meaning(item):
    """Extract the core meaning from the RWS section text."""
    rws_text = item["sections"].get("Rider-Waite-Smith (1909)", "")
    m = re.search(r"\*\*Core meaning:\*\*\s*(.+?)(?:\n|$)", rws_text)
    if m:
        return m.group(1).strip()
    return ""


def fill_major(item):
    """Fill stubs for a major arcana card."""
    number = item["metadata"]["number"]
    data = MAJOR_DATA.get(number)
    if not data:
        return  # shouldn't happen

    item["sections"]["Archetype"] = data["archetype"]
    item["sections"]["Professional"] = data["professional"]
    item["sections"]["Relationship"] = data["relationship"]
    item["sections"]["Consciousness"] = data["consciousness"]
    item["sections"]["Shadow"] = data["shadow"]


def fill_minor(item):
    """Fill stubs for a minor arcana card."""
    suit = item["metadata"]["suit"]
    number = item["metadata"]["number"]
    rank = item["metadata"].get("rank", "")
    keywords = item.get("keywords", [])
    core = extract_core_meaning(item)
    suit_info = SUIT_DATA.get(suit, {})
    element = suit_info.get("element", "")

    # Court card or pip?
    if number >= 11:
        court = COURT_DATA.get(rank, {})
        kw_str = ", ".join(keywords) if keywords else suit_info.get("domain", "")

        item["sections"]["Archetype"] = (
            f"The {rank.title()} of {suit.title()} — {court.get('role', '')}. "
            f"In the element of {element} ({suit_info.get('domain', '')}), "
            f"this figure embodies {kw_str}. "
            f"{core}"
        )
        item["sections"]["Professional"] = (
            f"{court.get('professional', '')} "
            f"In the {element} suit, this specifically concerns {suit_info.get('professional', '')}."
        )
        item["sections"]["Relationship"] = (
            f"{court.get('relationship', '')} "
            f"The {suit.title()} dimension adds: {suit_info.get('relationship', '')}."
        )
        item["sections"]["Consciousness"] = (
            f"{court.get('consciousness', '')} "
            f"Through {element}: {suit_info.get('consciousness', '')}."
        )
        item["sections"]["Shadow"] = (
            f"{court.get('shadow', '')} "
            f"The {suit.title()} shadow: {suit_info.get('shadow', '')}."
        )
    else:
        num_info = NUMBER_DATA.get(number, {})
        kw_str = ", ".join(keywords) if keywords else ""

        item["sections"]["Archetype"] = (
            f"The {num_info.get('stage', '')} of {element}. "
            f"{core} "
            f"Keywords: {kw_str}." if kw_str else
            f"The {num_info.get('stage', '')} of {element}. {core}"
        )
        item["sections"]["Professional"] = (
            f"{num_info.get('professional', '')} "
            f"In the {element} suit ({suit_info.get('professional', '')}), "
            f"this energy manifests as: {kw_str or suit_info.get('domain', '')}."
        )
        item["sections"]["Relationship"] = (
            f"{num_info.get('relationship', '')} "
            f"Through {suit.title()} ({element}): {suit_info.get('relationship', '')}."
        )
        item["sections"]["Consciousness"] = (
            f"{num_info.get('consciousness', '')} "
            f"The {element} path: {suit_info.get('consciousness', '')}."
        )
        item["sections"]["Shadow"] = (
            f"{num_info.get('shadow', '')} "
            f"The {suit.title()} shadow specifically: {suit_info.get('shadow', '')}."
        )


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    with open(GRAMMAR_PATH) as f:
        grammar = json.load(f)

    filled = 0
    for item in grammar["items"]:
        arcana = item["metadata"].get("arcana", "")
        if arcana == "major":
            fill_major(item)
        else:
            fill_minor(item)
        filled += 1

    with open(GRAMMAR_PATH, "w") as f:
        json.dump(grammar, f, indent=2, ensure_ascii=False)

    # Verify
    stubs_remaining = 0
    for item in grammar["items"]:
        for k, v in item["sections"].items():
            if "[To be written" in str(v):
                stubs_remaining += 1

    print(f"Filled interpretive sections for {filled} cards")
    print(f"Stubs remaining: {stubs_remaining}")
    print(f"File size: {os.path.getsize(GRAMMAR_PATH) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
