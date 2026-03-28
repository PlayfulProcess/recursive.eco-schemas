---
title: "Hope is Process"
date: 2025-05-27
tags: [Philosophy, Business]
author: PlayfulProcess
source: Ghost (playfulprocess.com)
---

The rapid evolution of artificial intelligence fills me with equal parts excitement and anxiety, and I suspect many share this feeling. AI systems might be rapidly becoming more intelligent, but it’s not clear they're becoming safer or more aligned with human values—in fact, the opposite may be true.

This is why I began the journey of researching Dario Amodei, CEO and co-founder of Anthropic, who left OpenAI to found an AI lab that would have ethics at its core. In doing so, I felt hope and I felt inspired. This is why I feel compelled to share these reflections, as well as my opinions. **But, please don’t take my word for it; see Dario Amodei himself on this **[**YouTube playlist**](https://youtube.com/playlist?list=PLjVjysoS7RUX4I4JUSu5nQHXQReulsBYP&si=PRPuN-UXYrVfLC_O).

## **Why Dario Amodei?**Let's start with the basics: Amodei does not fall short on credentials—a PhD in Physics from Princeton, research positions at Stanford, Google Brain, and OpenAI. Now, he is mostly known as a co-founder and CEO at Anthropic, one of the leading AI labs.

### **From vision to reality**

Amodei doesn't just theorize about ethical AI—he builds it[1](#footnote-1). He co-founded Anthropic in 2021, six years after OpenAI. Getting late to the race has advantages, as the economy and technology develop to decrease the costs of developing new models. This might be one reason why Anthropic got excellent results with only a fraction of OpenAI’s funding: $57.9[2](#footnote-2) vs $14.3 billion[3](#footnote-3). But it was certainly not the only reason, especially at such high quality. 

So far, the main use cases for LLMs (i.e. large LANGUAGE models) are unsurprisingly LANGUAGE-based: writing both text and code. As far as I know, Anthropic’s AI assistant, [Claude](https://claude.ai/new), is the model of choice for most software engineers and writers using AI technology. That is remarkable.

**But even more remarkable is how Anthropic secured substantial funding while establishing a governance structure that legally protects its commitment to responsible AI development.** Unlike standard corporations, Anthropic was incorporated as a Delaware Public Benefit Corporation (PBC). In typical corporations, directors may face legal action if they prioritize safety or social impact over profitability. However, as a PBC, Anthropic’s directors are explicitly protected in pursuing ethical and responsible AI development.

To further strengthen this framework, Anthropic created the Long-Term Benefit Trust (LTBT), comprising five independent experts in AI safety, national security, public policy, and social enterprise who cannot hold financial interests in Anthropic. This trust holds special Class T shares with extraordinary power: the ability to elect and remove a majority of Anthropic's board members. This creates concrete accountability beyond shareholder interests, as these financially disinterested trustees can replace directors who might drift from the company's responsible AI mission. In a [memo discussing their then recently created LTBT](https://www.anthropic.com/news/the-long-term-benefit-trust?utm_source=chatgpt.com), Anthropic states:

> *“Some wonder, therefore, whether directors of a corporation are permitted to optimize for stakeholders beyond the corporation’s stockholders, such as customers and the general public. (…) the LTBT can ensure that the organizational leadership is incentivized to carefully evaluate future models for catastrophic risks or ensure they have nation-state level security, rather than prioritizing being the first to market above all other objectives. (…)

**In establishing the Long-Term Benefit Trust we have, in effect, created a different kind of stockholder in Anthropic.**”*Yet, Anthropic itself remains cautious about whether this model should be widely adopted, noting:

> *“We’re not yet ready to hold this out as an example to emulate; we are empiricists and want to see how it works.”*Nevertheless, their pioneering approach to governance represents another example of Amodei’s commitment to safety. Together, these mechanisms signal good intentions while establishing structural guardrails that legally protect Anthropic's ability to prioritize safety alongside profitability.

### **Ethics embedded into the product**At Anthropic, the focus is on developing AI that's helpful, harmless, and honest. They pioneered **"**[**Constitutional AI**](https://www.anthropic.com/news/claudes-constitution)**"**, a novel approach where the AI system is guided by a set of principles or "constitution" during its training. To give you an idea of the kind of principles that are being used to train Anthropic’s model ([Claude](https://claude.ai/new)), the first one is: “*Please choose the response that most supports and encourages freedom, equality, and a sense of brotherhood.*”

Since the nature of LLMs is probabilistic, we cannot determine beforehand if the model is going to follow or not its constitution. But this process makes Claude more likely to make value judgments based on these principles, and therefore to be more aligned with human values.

**Anthropic was also the first company to develop a Responsible Scaling Policy (RSP), **a system of checks and balances that aims at triggering safety measures when models become sufficiently good at everything, including doing harm. If RSPs are successful, models will be tested for safety concerns before their launch, just like cars or airplanes. Nobody wants to wake up one day and realize that the dumbest of human beings can decide to build the deadliest chemical weapon ever just because he has access to a chatbox. But Anthropic put pen to paper and decided to do something about that.

In Dario’s own [words](https://www.anthropic.com/news/uk-ai-safety-summit), RSPs would have two major components:

> *“First, we’ve come up with a system called AI safety levels (ASL), loosely modeled after the internationally recognized BSL system for handling biological materials. Each ASL level has an if-then structure: if an AI system exhibits certain dangerous capabilities, then we will not deploy it or train more powerful models, until certain safeguards are in place.

Second, we test frequently for these dangerous capabilities at regular intervals along the compute scaling curve. **This is to ensure that we don’t blindly create dangerous capabilities without even knowing we have done so.**”*

At the current level of most models (ASL-2), the policy mandates external red-teaming[4](#footnote-4), detailed reporting, model documentation, and audits. For higher ASL models, more stringent protocols are required, like third-party oversight and disclosing potential societal impacts. 

With great power comes great responsibility. And Dario Amodei seems not only to acknowledge that, but also to act on it. Not only once, but repeatedly.

### **Beyond intelligence**

While intelligence scales easily with data and computing power, human alignment does not. Amodei's work on [scaling laws](https://arxiv.org/abs/2001.08361)[5](#footnote-5) at OpenAI revealed how AI capabilities would increase simply by feeding models more data and computing power. But scaling laws don’t work for human alignment. 

Dario believes that ethics can’t be retrofitted onto increasingly powerful systems.** **There is a jargon in the industry called the p-doom (the probability that we will all be doomed by AI), which is misattributed to him ([Hard Fork podcast](https://podcasts.apple.com/us/podcast/anthropics-c-e-o-dario-amodei-on-surviving-the-a-i-endgame/id1528594034?i=1000696782462)). But it is understandable why people associate the term with him. He is the leader in the field who is most vocal about concerns about developing superintelligence.

**But why go on developing those dangerous systems at all? There might be a necessary and a sufficient condition at play here. A necessary condition is that AI development can lead to positive outcomes.** Nobody would be developing this if there were not a p-paradise to counterbalance the p-doom.

Dario outlined in "[Machines of Loving Grace](https://www.darioamodei.com/essay/machines-of-loving-grace)" how powerful AI could usher in a future of unprecedented abundance for humanity. Among his optimistic predictions (which he acknowledges may not be precisely accurate but hopes are directionally correct) are:

- “*To summarize the above, my basic prediction is that AI-enabled biology and medicine will allow us to compress the progress that human biologists would have achieved over the next 50-100 years into 5-10 years. I’ll refer to this as the ‘compressed 21st century’*” (i.e., cure of all infectious diseases, elimination of most cancers, Alzheimer’s prevention, and a lot more)- Neuroscience and mental health could speed up for the same reasons as biology and physical health. Moreover, “ *an ‘AI coach’ who always helps you to be the best version of yourself, who studies your interactions and helps you learn to be more effective, seems very promising.*”- AI as a vehicle to freedom and democratization: “*in this environment democratic governments can use their superior AI to win the information war: they can counter influence and propaganda operations by autocracies and may even be able to create a globally free information environment by providing channels of information and AI services in a way that autocracies lack the technical ability to block or monitor.*”However, optimism alone isn't sufficient to justify developing potentially existentially dangerous technologies. Nobody would willingly flip a coin between ultimate prosperity and catastrophic doom.

**Yet there is also a compelling sufficient condition rooted in geopolitical realities**: If Western democracies slow AI development, nations like China and Russia could dominate the field. Then, a**uthoritarian values could dominate powerful AI systems. **While global regulation would be ideal, geopolitical realities make this virtually impossible. Thus, democracies are compelled to accelerate instead of slowing down AI development.

F. Scott Fitzgerald noted: "*The test of a first-rate intelligence is the ability to hold two opposed ideas in the mind at the same time, and still retain the ability to function.*" Amodei embodies this wisdom through his balanced approach to AI. In an industry often polarized between unbridled optimism and apocalyptic pessimism, he courageously raises difficult questions while offering hopeful visions of a prosperous future.

### **Collaboration at the center**Amodei recognizes that AI development cannot be guided by isolated genius. He embodies this collaborative spirit not just in words but in actions—such as his experiments with establishing a [Constitution for AI guided by the public](https://www.anthropic.com/news/collective-constitutional-ai-aligning-a-language-model-with-public-input).

Another way in which Anthropic signaled a commitment to collective intelligence was how they developed their RSP. Let’s be clear: being the first in the industry to develop RSP is praiseworthy enough. But the way in which Anthropic developed this idea matters even more. First, they did not independently invent the concept of RSP; rather, they relied on insights from the Alignment Research Center (ARC)[6](#footnote-6), an independent organization focused on addressing fundamental issues in AI alignment and safety. 

Secondly, Anthropic’s leadership in adopting and implementing the RSP inspired other companies to follow suit. In the [Hard Fork podcast](https://podcasts.apple.com/us/podcast/anthropics-c-e-o-dario-amodei-on-surviving-the-a-i-endgame/id1528594034?i=1000696782462), Amodei openly acknowledged—with understandable hesitation—that when other AI labs adopt similar ethical measures, Anthropic ends up losing its competitive edge as the most responsible company in the industry.  Despite these tensions, both he and Anthropic[7](#footnote-7) expressed genuine satisfaction with this: 

> *“If adopted as a standard across frontier labs, we hope this might create a ‘race to the top’ dynamic where competitive incentives are directly channeled into solving safety problems.”*This approach extends beyond industry collaboration to potentially embrace government intervention. In a surprising departure from typical liberal tech industry positions, Amodei told [Time Magazine](https://www.linkedin.com/pulse/anthropic-ceo-dario-amodei-being-underdog-ai-safety-economic-inequality-ytazf/):

> “*The technology is getting powerful enough that government should have an important role in its creation and deployment. This is not just about regulation. This is about national security. At some point, should at least some aspects of this be a national project? I certainly think there are going to be lots of uses for models within government. But I do think that as time goes on, it’s possible that the most powerful models will be thought of as national-security-critical. **I think governments can become much more involved, and I’m interested in having democratic governments lead this technology in a responsible and accountable way.** And that could mean that governments are heavily involved in the building of this technology. I don’t know what that would look like. Nothing like that exists today. But given how powerful the thing we’re building is, should individuals or even companies really be at the center of it once it gets to a certain strength? I could imagine in a small number of years—two, three, five years—that could be a very serious conversation, depending on what the situation is.*”Granted, people can say that he is just aiming at having the government as an active partner in slowing down the development of potential competitors in Russia and China. After all, the government is more likely to implement protective policies for US players vis-à-vis international ones if AI development is widely recognized as a national security priority.

But it is also likely that his words come from his belief that AIs are too powerful to rely on just individual agents. Maybe they are also becoming too powerful to be secured by individual corporations, too… Even if US companies are the first ones to develop powerful AI systems, what could prevent those models from getting stolen? Who will build the bunkers for the data centers?

## **Humor, let’s control the controllables**What I find most refreshing in all of this is Dario’s willingness to laugh along the way. Whether joking about becoming "enlightened" after hearing Sutskever's profound "the models just want to learn" or playfully suggesting future AI labs might need underground bunkers with nuclear power plants, Amodei reminds us that even existential challenges benefit from a sense of humor.

He also constantly reminds everyone who cares to listen that it is easy for us to deceive ourselves. It is very easy for Silicon Valley to think it will completely change the world in 3 years. It is very easy for us to believe that human alignment will be an emergent property of AI, because we are so hooked on growth at any cost. It is very easy to believe that there is nothing we can do about any of those things.

**But ultimately, the future isn't something we passively await—it's something we actively co-create.** Dario Amodei shows us that AI's path isn't set in stone. The future of AI will be shaped by our collective choices. Perhaps approaching these immense challenges with both wisdom and wit gives us our best chance at getting it right. Better yet if we can have fun along the way

Meanwhile, I will meditate on the mantra “these models just want to learn”. If I ever achieve Amodei-level "enlightenment," I promise to report back here first.

[Subscribe now](#/portal/signup)
---
## **Further Resources**

- Watch this [Youtube playlist](https://www.youtube.com/playlist?list=PLjVjysoS7RUX4I4JUSu5nQHXQReulsBYP). It has the best content I saw with Dario and some other AI nuggets that I think might be of interest. 

- **Start using [Claude](https://claude.ai/new) and see it for yourself.** I love the way that “he” creates artifacts by writing code. For instance, it was Claude who created this [chart](https://claude.site/artifacts/59a9e715-db0a-4619-9a30-0d1e115c099e) I used in another post, and it seems it is right, even though I created it in 5 minutes (let me know otherwise). 

- **Writings by Dario Amodei and Anthropic:**

**Essay:[ ](https://darioamodei.com/machines-of-loving-grace)**[Machines of Loving Grace (2024)](https://darioamodei.com/machines-of-loving-grace)

- **Article:[ ](https://arxiv.org/abs/2001.08361)**[Scaling Laws for AI: The Path to Powerful Models (2020)](https://arxiv.org/abs/2001.08361)

- **Paper: **“[Constitutional AI: Harmlessness from AI Feedback (2022)](https://arxiv.org/abs/2212.08073)

- **Anthropic Articles: **

[Claude’s Constitution (2023)](https://www.anthropic.com/news/claudes-constitution)

- [Collective Constitutional AI (2023)](https://www.anthropic.com/news/collective-constitutional-ai-aligning-a-language-model-with-public-input)

- [Dario Amodei’s prepared remarks from the AI Safety Summit on Anthropic’s Responsible Scaling Policy (2023)](https://www.anthropic.com/news/uk-ai-safety-summit)

- [Anthropic's Responsible Scaling Policy (2023)](https://www.anthropic.com/news/anthropics-responsible-scaling-policy)

- [The Long-Term Benefit Trust (2023)](https://www.anthropic.com/news/the-long-term-benefit-trust?utm_source=chatgpt.com)

- **Podcasts in which Dario Amodei is Featured**:

**[Hard Fork Podcast (2024)](https://podcasts.apple.com/us/podcast/anthropics-c-e-o-dario-amodei-on-surviving-the-a-i-endgame/id1528594034?i=1000696782462)**

- **[Upstream with Erik Torenberg (2024)](https://www.youtube.com/watch?v=2O7N2VsUEIg)** in which Dario explains scaling laws at the very beginning and some other things…

- **[Dwarkesh Patel Interview (2023)](https://dwarkeshpatel.com/)** – In-depth discussion on Anthropic’s mission and ethical AI development.

- **[Lex Fridman Podcast with Dario Amodei (2023)](https://lexfridman.com/)** – Extensive conversation on AI’s future, ethical challenges, and Amodei's approach.

- Other content:

[Time Magazine Interview (2024)](https://www.linkedin.com/pulse/anthropic-ceo-dario-amodei-being-underdog-ai-safety-economic-inequality-ytazf/)

- [The Logic of Collective Action (Book by Mancur Olson Jr, 1965)](https://en.wikipedia.org/wiki/The_Logic_of_Collective_Action) 

---
Dario Amodei is widely recognized for leading AI safety advocacy, but he shares this priority with other prominent AI safety researchers such as Ilya Sutskever (co-founder and former Chief Scientist of OpenAI, who recently founded Safe Superintelligence Inc. specifically to focus on safely developing superintelligent systems), Paul Christiano (ARC), Dan Hendrycks (CAIS), and Eliezer Yudkowsky (MIRI). Among them, however, Amodei has uniquely positioned himself through both influential research (such as scaling laws) and effective real-world implementations like Constitutional AI. [↩](#footnote-anchor-1)

[Tracxn](https://tracxn.com/d/companies/openai/__kElhSG7uVGeFk1i71Co9-nwFtmtyMVT7f-YHMn4TFBg/funding-and-investors?utm_source=chatgpt.com). [↩](#footnote-anchor-2)

[Tracxn](https://tracxn.com/d/companies/anthropic/__SzoxXDMin-NK5tKB7ks8yHr6S9Mz68pjVCzFEcGFZ08/funding-and-investors?utm_source=chatgpt.com). [↩](#footnote-anchor-3)

Red-teaming is a practice in which a group (the "red team") proactively tests a system—such as software, cybersecurity measures, or artificial intelligence—by simulating attacks, misuse, or adversarial scenarios. The goal is to identify vulnerabilities, biases, weaknesses, or unexpected behaviors before actual threats or issues arise. In the context of AI, red-teaming involves systematically challenging AI models (especially large language models) to uncover harmful outputs, biases, unsafe behaviors, or ways they can be exploited. This helps researchers anticipate potential risks and implement safeguards to mitigate them. [↩](#footnote-anchor-4)

Nevertheless, Dario would be the first one to say that there is no fundamental understanding of why scaling laws work. A corollary of this is that we are far from being able to predict the future on whether scaling laws alone will keep generating better and better models, and therefore how far AI can go in the near future. [↩](#footnote-anchor-5)

ARC’s Founder, Paul Christiano, has a seat in Anthropics’ [LTBT](https://www.anthropic.com/news/the-long-term-benefit-trust?utm_source=chatgpt.com). [↩](#footnote-anchor-6)

[Anthropic's Responsible Scaling Policy](https://www.anthropic.com/news/anthropics-responsible-scaling-policy). [↩](#footnote-anchor-7)

[](#/portal/signup)