---
title: "Vibe Coding with Claude: Building 3 Journaling AI Tools in 1 hour"
date: 2025-08-25
tags: []
author: PlayfulProcess
source: Ghost (playfulprocess.com)
---

⏰ Total time: 60 minutes
📱 Works on desktop (recommended) or mobile
💾 No coding required

## What You'll Build TodayA personalized interactive tool where users can write and get AI feedback on any topic. Total privacy: no data saved anywhere. User can export content and save it wherever they feel safe to do it.

At the end, we are going to encourage you to share the results of your work in the comments section of this post. Bonus points if you record your whole process and publish on Youtube!

By the end of Hour 1, you'll have:
✅ 3 working AI tools
✅ Published link to share with other humans
✅ Share in comments

## Prerequisites (5m)### Sign up for Claude- Go to [claude.ai](https://claude.ai)- Create a free account- You're ready!

## Section 1: Adapting a Tool (20m)### Step 1: Interact with the tool (5m)Open the [tool ](https://claude.ai/public/artifacts/94fdc893-2eb6-4b08-b2e9-e269055dbc60)and go through the process outlined. As you do this, make a list of things you'd change about the tool.

### Step 2: Try some customizations (10m)Click the button "Customize" On the top-right of the page:

![](https://blog.jongu.org/content/images/2025/08/Claude_customize-1.jpg)Try the prompts below to customize. You can paste all of them at once or see take a step-by-step approach:

> I think the Value-Driven Goals and Activity Scheduling sections are kind of the same. Merge both of them.> I want to add an option for the User to Include a Value they are trying to work on in the begining.> I would rather have all the tool in one page than making the user navigate across pages. I would like that the user see all the work immediately and be able to look into his previous answers by scrolling. Maybe with this the Summary step get obsolete.> In the Summary section you had/have you say the user can simply press CTRL+ P and print as a PDF to save their work. However, the export is broken because it just print 1page and there is some content missing. Can you create a button to export user input as a txt file so the user can save the data? Also create an import button in the begining of the section so that all the data can be visualized in this UI.You can check my chat with Claude as an example [here](https://claude.ai/share/6c048d95-7241-4b21-ba49-557cef614631). The way that I shared this was by closing the artifact temporarily (you can always go back in the chat and open it again), and clicking the Share button on the top-right corner of the page.

![](https://blog.jongu.org/content/images/2025/08/Share-Button.jpg)

### Step 3: Try your own ideas (4m)Now, look at the list you created when you first used the tool. Pick the one that seems still relevant to implement and prompt Claude to change the artifact based on it. 

Whenever in doubt about writing a prompt, ask Claude to help you frame a prompt for you before using action verbs like "Change this", "Merge that", etc. You can say something like:

> I am still bogged by XYZ, can you help me ideate on what I could change and how would you prompt yourself to make the changes? Please do not change anything in the artifact before we have a plan.If Claude ends up implementing a change you did not want, you can always go back to the prior version by clicking on the arrow down in the version tag.

![](https://blog.jongu.org/content/images/2025/08/version.jpg)

### Step 4: Publish (1m)When Claude builds an artifact, it automatically gets saved in your artifact section for later retrieval:

![](https://blog.jongu.org/content/images/2025/08/Artifacts_library.jpg)You can also hit the "Publish" button and share with anyone you would want! [This ](https://claude.ai/public/artifacts/44907df2-8e6a-4839-9889-862a905f0143)is what I created.

![](https://blog.jongu.org/content/images/2025/08/Publish.jpg)

## Section 2: Create a Tool from Scratch (15m)### Step 1: Reference (2m).Go into the [blog ](https://donaldrobertson.substack.com/p/my-self-improvement-framework)post used as reference for this tool that is in the footer of the tool. Select all content (shortcut tip: CTRL + a), copy and paste into the Claude chat (CTRL + c and CTRL + v).

### Step 2: Prompt (3m).Together with the blog post text you just created, prompt Claude to:

> Develop an artifact for me based on the artifact attached. It should have an easy way for users to export their data into a txt that they could easily re-upload in the tool to see it in the UI (user interface). Create a button for export and import in the hero session of the tool. At, the end, there should be an AI chatbot in which the AI is prompted to act as a DBT coach mixed with NVC moderator and a Stoic philosopher when answering and be fed all the user inputs to give a thoughtful answer.See if you like the results. We take intellectual property very seriously at Jongu. So, be sure to prompt Claude to include the link to the blog post in the footer and check with the author if they are ok with you publishing the tool before sharing it broadly.

> Please include a footer with the original blog post: [https://donaldrobertson.substack.com/p/my-self-improvement-framework](https://donaldrobertson.substack.com/p/my-self-improvement-framework). Also include my personal website channel for people who are interested in tools like this to be able to discover more tools: [https://www.wellness.jongu.org/](https://www.wellness.jongu.org/).Always test it 😄, as Claude makes mistakes!

You can check out my chat with Claude [here](https://claude.ai/share/1c6eda36-9401-4269-ba95-ec276f614486).

### Step 3: Optimize (10m).If the prompt is not what you would like, chat with Claude to make some changes or select a tool referrenced in [Jongu's Wellness Channel](https://www.wellness.jongu.org/) for Claude to use.

## Section 3: Create Your Personalized Tool (20m)Now that you know the capabilities, choose a tool, worksheet or method you like and prompt Claude to build them!

### Step 0 (optional): Create a Project with the Right System's Prompt and Referrences (5m).Unfortunately, this feature is only available for paid users. Fortunately, it is not required for getting the job done, but it helps.

My experience doing this is that Claude's work better with system prompts and referrences at the project-level. Claude does not keep a record or retrieves data from previous chats. So working on a project is the safest way for you to be able to rebuild artifacts seamlessly in the future.

If you are willing to pay for Claude, then, navigate to Projects and Create a new Project.

![](https://blog.jongu.org/content/images/2025/08/PRojects.jpg)Then, choose a title and a system prompt for the project. As an example, I did:

> Title: Wellness Tools Creator> Prompt: I am trying to build artifacts to be publicly available for people interested in wellness and self improvement. They should always contain the following features: 1) An import and export button in the hero session for the user to export a file in txt and be able to save their work. LAter they will be able to import the file and see it in the UI. 2) An AI chat at the end in which the AI is prompted to behave as a DBT coach, mixed with an NVC mentor and a stoic philosopher. It should alwasy provide some validation/empathy and ask a question at the end that would get the user thinking deeper.Note: You don't want this to be a fully clinical tool that would behave like a therapist because Claude is not HIPAA compliant and regulation might forbid this.

Include any documents or referrences you think might be useful for this project in the knowledge base.

![](https://blog.jongu.org/content/images/2025/08/KNowledge-base.jpg)

### Step 1: Create the Right Prompt for your Project (10m).The best prompt generator for AI is AI. Write loosely for two minutes about the tool that you want to create and prompt Claude to write a prompt for itself to create an artifact later. Then, prompt Claude to:

> Generate a prompt for me so we can plan this thoroughly before jumping into coding the artifact.> **If not using a project (Free tier), add this to your prompt at the end: **I am trying to build artifacts to be publicly available for people interested in wellness and self improvement. They should always contain the following features: 1) An import and export button in the hero session for the user to export a file in txt and be able to save their work. Later they will be able to import the file and see it in the UI. 2) An AI chat at the end in which the AI is prompted to behave as a DBT coach, mixed with an NVC mentor and a stoic philosopher. It should always provide some validation/empathy and ask a question at the end that would get the user thinking deeper.Chat briefly with Claude to answer any questions Claude might have. But, if you want to move quickly you can just ask Claude to answer what he thinks is best.

### Step 2: Prompt Claude and Customize (2m).When you think you got to a point you are comfortable with, prompt the Claude to create the artifact. Optionally, spend as much time as you want to get this into a better spot!

I know [it took me a couple of interactions](https://claude.ai/share/b92a49ba-8a45-4b70-8ba4-978fc2f6495e) to get to an acceptable place. Probably if I had spent more time designing the prompt, it would flow better. 

> Pro Tip: You can print screen the tool and paste the content in the chat so Claude can understand exactly what you are seeing!### Step 3: Share Your Work (3m).The Recursive.eco community is here to support you. Publish your artifact, copy the link and publish it as a comment to this blog post! 

(You might need to subscribe before you do, don't worry, I rarely send out newsletter)