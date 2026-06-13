import os
import json
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import anthropic

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

# Read voice guide
with open("voice.md", "r") as f:
    VOICE_GUIDE = f.read()

# Read already posted artists
with open("posted_artists.md", "r") as f:
    POSTED_ARTISTS = f.read()

def find_and_research_artist():
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    print("Finding a new artist...")

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4000,
        tools=[
            {
                "type": "web_search_20250305",
                "name": "web_search"
            }
        ],
        messages=[
            {
                "role": "user",
                "content": f"""You are a researcher and writer for @archivingpresence, 
an Instagram account that curates interactive contemporary art — 
sound installations, light works, participatory art, and public interventions.

These artists have already been posted about — do not use them:
Chiharu Shiota, Matteo Ingrao, Tomislav Topić

Your task:
1. Search the web to find one compelling contemporary installation artist 
   who has NOT been posted about yet. Focus on artists whose work is 
   immersive, participatory, or sensory — work that changes when you 
   are physically inside it.

2. Research that artist deeply:
   - Their most significant or recent installation work
   - Exhibition history — where has this work been shown?
   - Any artist statement or interview quotes
   - The human experience of being inside the work
   - Any cultural, philosophical, or historical context that unlocks the work

3. Find the quiet question hiding inside the work — the thing the work 
   asks of the person standing in it.

4. Write THREE different Instagram captions for this work using the 
   voice guide below. Each caption should have a different emotional 
   entry point — a different way into the same work.

Voice guide — write in this style:
- Never describe the art. Describe the experience of being near it.
- Use the body as the entry point — hands, skin, eyes, movement.
- Short sentences land the weight. Long sentences carry the atmosphere.
- Ask one quiet question and leave it open. Never answer it.
- Give cultural or philosophical context first, then the work.
- Never use art jargon like "explores" or "interrogates".
- End on something unresolved.

Format your response as JSON like this:
{{
  "artist_name": "name here",
  "instagram_handle": "@handle or empty string if not found",
  "work_title": "title of the work",
  "exhibition": "where and when it was shown",
  "context": "the cultural or philosophical angle you found",
  "quiet_question": "the question hiding in the work",
  "caption_1": "first caption here",
  "caption_2": "second caption here", 
  "caption_3": "third caption here"
}}

Once you have finished all research, output ONLY a single JSON object.
No thinking. No explanation. No preamble. Just the raw JSON starting 
with {{ and ending with }}.
If you cannot find an artist, still return the JSON with your best attempt."""
            }
        ]
    )

    # Extract text from response
    # Extract text from response - handle web search tool blocks
    response_text = ""
    for block in message.content:
        if block.type == "text":
            response_text += block.text

    print("Raw response:", response_text[:300])
    # Find JSON block in response
    start = response_text.find("{")
    end = response_text.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError("No JSON found in response")
    clean = response_text[start:end]
    return json.loads(clean)

def save_content(data):
    today = datetime.date.today().strftime("%Y-%m-%d")
    filename = f"content_{today}_{data['artist_name'].replace(' ', '_')}.md"
    
    content = f"""# {data['artist_name']} — {data['work_title']}
Generated: {today}

## Research notes
**Exhibition:** {data['exhibition']}
**Context:** {data['context']}
**The quiet question:** {data['quiet_question']}

---

## Caption 1
{data['caption_1']}

---

## Caption 2
{data['caption_2']}

---

## Caption 3
{data['caption_3']}

---
{data['instagram_handle']}
"""
    
    with open(filename, "w") as f:
        f.write(content)
    
    print(f"Saved: {filename}")
    return filename, content

def update_posted_artists(artist_name):
    with open("posted_artists.md", "a") as f:
        f.write(f"\n- {artist_name}")
    print(f"Added {artist_name} to posted artists list")

def send_email(data, content):
    msg = MIMEMultipart()
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = GMAIL_ADDRESS
    msg["Subject"] = f"📸 Thursday post ready: {data['artist_name']} — {data['work_title']}"

    body = f"""
Your Thursday post is ready for @archivingpresence.

Artist: {data['artist_name']}
Work: {data['work_title']}
Shown at: {data['exhibition']}

---

CAPTION 1
{data['caption_1']}

---

CAPTION 2
{data['caption_2']}

---

CAPTION 3
{data['caption_3']}

---

Instagram handle: {data['instagram_handle']}

Pick the caption that feels right, find an image, and post.
    """

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.send_message(msg)
    
    print("Email sent!")

def run():
    print("archivingpresence content agent running...")
    
    data = find_and_research_artist()
    print(f"Found artist: {data['artist_name']}")
    print(f"Work: {data['work_title']}")
    print(f"Quiet question: {data['quiet_question']}")
    
    filename, content = save_content(data)
    update_posted_artists(data['artist_name'])
    send_email(data, content)
    
    print("Done. Check your email for this week's post.")

run()