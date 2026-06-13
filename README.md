# archivingpresence Content Agent 📸

An autonomous content research agent for [@archivingpresence](https://instagram.com/archivingpresence) — 
an Instagram account curating interactive contemporary art installations.

Every Thursday it finds a new artist, researches their work, and writes 
three caption options in my voice — ready to review and post.

Built by Kritika Singh — Senior UX Designer & Creator

---

## The problem

Running a curation account means constantly finding new artists, 
researching their work deeply, and writing captions that sound like 
you — not like a press release. All three together took hours every week.

I wanted an agent that handles the research and first draft, 
so I spend my time on creative judgement rather than legwork.

---

## What it does

Every Thursday morning, automatically:

1. Searches the web for a compelling contemporary installation artist
   not previously posted about
2. Researches their most significant work — exhibition history, 
   artist statements, critical writing
3. Finds the human angle — the cultural reference, the bodily 
   experience, the quiet question inside the work
4. Writes three caption options in my specific voice
5. Emails me the options to review, pick, and post

---

## The voice challenge

The hardest part wasn't the code — it was capturing voice.

My captions follow specific rules:
- Never describe the art. Describe the experience of being near it.
- Use the body as the entry point — hands, skin, eyes, movement.
- Short sentences land the weight. Long sentences carry the atmosphere.
- Ask one quiet question and leave it open. Never answer it.
- Give cultural or philosophical context first, then the work.
- Never use art world jargon.

These rules live in `voice.md` — the agent's style guide. 
It reads this before writing anything.

---

## Stack

- Python
- Anthropic Claude API with web search (claude-sonnet-4-5)
- Gmail SMTP
- cron (runs every Thursday automatically)

---

## How it works

---

## Key files

- `content_agent.py` — the main agent script
- `voice.md` — writing rules and style guide (the agent's brief)
- `posted_artists.md` — running list of covered artists (agent's memory)

---

## Sample output

The agent emails something like this every Thursday:

---

## Portfolio

kritikacsingh.com  
[@archivingpresence](https://instagram.com/archivingpresence)