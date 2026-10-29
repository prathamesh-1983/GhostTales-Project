import json
import random
import re
from datetime import datetime
from pathlib import Path

import requests
import streamlit as st

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
STORIES_FILE = DATA_DIR / "stories.json"
DATA_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="GhostTales — Offline Story Generator",
    page_icon="👻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- Styling ---------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Creepster&family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
:root { --bg:#080a12; --panel:#111522; --panel2:#171b2b; --line:#2a3045; --text:#f3f1ff; --muted:#a4abc4; --purple:#a78bfa; --cyan:#67e8f9; --pink:#f0abfc; }
.stApp { background: radial-gradient(ellipse at 12% 0%, #21163c 0%, transparent 35%), radial-gradient(ellipse at 95% 20%, #102b3a 0%, transparent 28%), var(--bg); color:var(--text); font-family:'DM Sans',sans-serif; }
[data-testid="stHeader"] { background:rgba(8,10,18,.78); }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#101323,#0b0d16); border-right:1px solid var(--line); }
h1,h2,h3 { color:var(--text) !important; }
h1 { font-family:'Playfair Display',serif !important; letter-spacing:-1px; }
p, label, .stMarkdown { color:var(--text); }
.eyebrow { color:var(--cyan); letter-spacing:3px; text-transform:uppercase; font-size:.72rem; font-weight:700; }
.hero { padding:1.8rem 0 1.2rem; }
.hero-title { font-family:'Playfair Display',serif; font-size:clamp(2.6rem,6vw,5.1rem); line-height:1.02; font-weight:700; background:linear-gradient(100deg,#fff 5%,#c4b5fd 48%,#67e8f9 95%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:.5rem 0 1rem; }
.hero-sub { color:#b8bfd6; max-width:740px; font-size:1.05rem; line-height:1.8; }
.panel { background:linear-gradient(145deg,rgba(25,29,47,.94),rgba(13,16,28,.96)); border:1px solid var(--line); border-radius:18px; padding:1.2rem 1.35rem; box-shadow:0 16px 45px rgba(0,0,0,.18); }
.story { background:linear-gradient(145deg,rgba(18,22,37,.98),rgba(10,12,21,.98)); border:1px solid #34334f; border-radius:18px; padding:1.7rem; line-height:1.95; white-space:pre-wrap; color:#e9e7f7; }
.story h2 { color:#d8b4fe !important; }
.stat { border:1px solid var(--line); border-radius:14px; background:rgba(18,22,37,.72); padding:1rem; }
.stat-num { font-size:1.35rem; font-weight:700; color:var(--cyan); }
.stat-label { color:var(--muted); font-size:.82rem; }
div.stButton > button, div.stDownloadButton > button { border-radius:11px; border:1px solid #7463bb; background:linear-gradient(100deg,#7c3aed,#4f46e5); color:white; font-weight:700; min-height:2.7rem; }
div.stButton > button:hover, div.stDownloadButton > button:hover { border-color:var(--cyan); color:white; box-shadow:0 0 22px rgba(167,139,250,.25); }
.stTextInput input, .stTextArea textarea, [data-baseweb="select"] > div { background:#111522 !important; color:#f3f1ff !important; border-color:#343a52 !important; border-radius:10px !important; }
.stSelectbox label, .stSlider label, .stTextInput label, .stTextArea label { color:#c9cce0 !important; }
hr { border-color:var(--line); }
.small-muted { color:var(--muted); font-size:.86rem; }
div[data-testid="stMetric"] { background:rgba(18,22,37,.72); padding:12px; border:1px solid var(--line); border-radius:12px; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ----------------------------- Story engine ----------------------------------
SCENES = {
    "Abandoned mansion": {
        "place": "the abandoned mansion at the edge of town",
        "details": ["a chandelier swayed although every window was sealed", "footsteps crossed the landing above", "a portrait's eyes seemed to follow every movement", "a locked door breathed cold air through its keyhole"],
        "object": "a brass key wrapped in a strip of faded velvet",
    },
    "Foggy forest": {
        "place": "the forest where the fog never lifted",
        "details": ["the trees leaned inward as if sharing a secret", "a lantern bobbed between the trunks with no hand to carry it", "the path behind them vanished beneath fresh leaves", "something repeated their footsteps half a second late"],
        "object": "a cracked compass whose needle pointed underground",
    },
    "Forgotten village": {
        "place": "a village erased from every modern map",
        "details": ["every clock stopped at 3:17", "warm candlelight glowed behind windows in empty houses", "a bell rang from a church with no bell tower", "the villagers' names had been scratched from the gravestones"],
        "object": "a handwritten letter sealed with black wax",
    },
    "Midnight train": {
        "place": "the last train running through the mountains",
        "details": ["the carriage lights flickered in a pattern like Morse code", "a passenger appeared in the reflection but not in the seat", "the announcement spoke a name no one had said aloud", "the train slowed beside a station absent from the timetable"],
        "object": "a ticket dated exactly one hundred years earlier",
    },
    "Cursed lighthouse": {
        "place": "the lighthouse on the storm-battered coast",
        "details": ["the lamp turned toward the land instead of the sea", "wet footprints climbed the spiral stairs", "a voice came through the dead radio", "the keeper's log continued writing itself"],
        "object": "a salt-stained photograph with one face scratched away",
    },
}
MOODS = {
    "Slow-burn suspense": ("quiet, patient dread", "The silence seemed to wait for an answer."),
    "Psychological horror": ("uncertain reality and mounting paranoia", "They could no longer trust what the room showed them."),
    "Supernatural mystery": ("strange clues and an unsettling mystery", "The impossible clue was also the only honest one."),
    "Gothic tragedy": ("melancholy, old secrets, and lost love", "Some hauntings were simply grief that had forgotten how to leave."),
    "Campfire creepy": ("punchy scares and a memorable final twist", "Then, from inside the empty phone, a voice whispered: “Your turn.”"),
}

def read_saved_stories():
    try:
        return json.loads(STORIES_FILE.read_text(encoding="utf-8")) if STORIES_FILE.exists() else []
    except (json.JSONDecodeError, OSError):
        return []

def write_saved_stories(stories):
    STORIES_FILE.write_text(json.dumps(stories, indent=2, ensure_ascii=False), encoding="utf-8")

def build_prompt(setting, mood, protagonist, object_hint, length, custom):
    return f"""Write an original ghost story for a web app.
Setting: {setting}
Mood: {mood}
Main character: {protagonist or 'a curious stranger'}
Important object or clue: {object_hint or 'choose one that fits the setting'}
Length: approximately {length} words
Extra direction: {custom or 'Use vivid sensory detail and a satisfying twist.'}
Requirements: Make it atmospheric, original, coherent, and suitable for a general audience.
Do not claim this is a true event. Give it a title, then the story. Avoid clichés where possible."""

def local_fallback_story(setting, mood, protagonist, object_hint, length, custom):
    scene = SCENES[setting]
    mood_desc, ending_line = MOODS[mood]
    hero = protagonist.strip() if protagonist.strip() else "Mara"
    clue = object_hint.strip() if object_hint.strip() else scene["object"]
    details = random.sample(scene["details"], k=3)
    title_options = {
        "Abandoned mansion": ["The House That Held Its Breath", "The Portrait Upstairs", "A Key for the Unquiet"],
        "Foggy forest": ["Where the Trees Listen", "The Path Behind You", "A Compass for the Dead"],
        "Forgotten village": ["The Village at 3:17", "Names in the Dust", "A Letter Never Delivered"],
        "Midnight train": ["The Passenger in Car Seven", "The Stop Between Stations", "One Ticket Home"],
        "Cursed lighthouse": ["The Light That Turned Inland", "The Keeper's Last Signal", "A Face Beneath the Tide"],
    }
    title = random.choice(title_options[setting])
    extra = f" The note in the margin read: “{custom.strip()}”." if custom.strip() else ""
    story = f"""{title}

At 11:58 p.m., {hero} arrived at {scene['place']}. The local warnings had sounded theatrical in daylight. At night, under a moon the color of old bone, they felt more like instructions.

The first sign was small: {details[0]}. {hero} stopped, listened, and heard only the slow click of their own pulse. They had come looking for answers, and the {clue} in their coat pocket had brought them here.

Inside, the air tasted of rain and extinguished candles. Then {details[1]}. A voice, thin as a thread pulled through cloth, spoke from somewhere beyond the dark.

“You took your time.”

{hero} raised a light. Nothing stood in the corridor, but a line of damp footprints appeared one by one, leading toward a room that should not have existed. Every sensible part of {hero} demanded retreat. The rest—the part that had carried the clue for years—followed.

In the room lay a table, two chairs, and a mirror clouded from the inside. On the table was proof of the secret {hero} had spent a lifetime trying to uncover. The clue was not a warning. It was an invitation.

Behind them, {details[2]}. In the mirror, a second figure stood close enough to touch their shoulder. Its face was familiar, though memory had carefully hidden it.

The figure did not reach out. It only pointed to the door.

At once, {hero} understood the terrible kindness of the place: it had not trapped the dead inside. It had kept the living from discovering what they had left behind.

{ending_line}

When the clock finally struck midnight, the room was empty. On the table, the clue had become warm. And from somewhere deep in {scene['place']}, a new set of footsteps began.

{extra}"""
    # Make length setting meaningful without awkwardly truncating the story.
    if length <= 150:
        story = "\n\n".join(story.split("\n\n")[:5]) + "\n\n" + ending_line
    elif length >= 700:
        story += ("\n\nThe wind moved through the place again, carrying a sound that might have been laughter or the settling of old wood. " * 5)
    return title, story

def generate_with_ollama(prompt, model, base_url):
    endpoint = base_url.rstrip("/") + "/api/generate"
    response = requests.post(
        endpoint,
        json={"model": model, "prompt": prompt, "stream": False, "options": {"temperature": 0.9, "num_predict": 1200}},
        timeout=180,
    )
    response.raise_for_status()
    result = response.json().get("response", "").strip()
    if not result:
        raise ValueError("The model returned an empty response.")
    lines = result.splitlines()
    title = lines[0].strip("# *") if lines else "A GhostTales Story"
    if len(title) > 90 or len(title.split()) > 12:
        title = "A GhostTales Story"
    return title, result

# ----------------------------- State -----------------------------------------
if "current_story" not in st.session_state:
    st.session_state.current_story = None
if "story_mode" not in st.session_state:
    st.session_state.story_mode = "Demo mode (no model required)"

# ----------------------------- Sidebar ---------------------------------------
with st.sidebar:
    st.markdown("## 👻 GhostTales")
    st.caption("Stories from the other side.")
    st.markdown("---")
    st.markdown("### ⚙️ Story engine")
    engine = st.radio(
        "Choose generation mode",
        ["Demo mode (no model required)", "Local AI with Ollama"],
        index=0 if st.session_state.story_mode.startswith("Demo") else 1,
        help="Demo mode works immediately. Ollama mode generates text using a model installed on your computer.",
    )
    st.session_state.story_mode = engine
    ollama_url = st.text_input("Ollama URL", value="http://localhost:11434", help="Default local Ollama address.")
    model_name = st.text_input("Model name", value="gemma3:1b", help="Use the exact name of a model installed in Ollama.")
    if engine.startswith("Local"):
        st.info("Install Ollama, then run: `ollama pull gemma3:1b`")
        if st.button("Check local model connection", use_container_width=True):
            try:
                r = requests.get(ollama_url.rstrip("/") + "/api/tags", timeout=4)
                r.raise_for_status()
                models = [m.get("name", "") for m in r.json().get("models", [])]
                st.success("Ollama is reachable.")
                st.write("Installed models:", ", ".join(models) if models else "No models found.")
                if model_name not in models:
                    st.warning(f"`{model_name}` was not found in the installed model list.")
            except Exception as exc:
                st.error(f"Could not connect to Ollama: {exc}")
    st.markdown("---")
    st.markdown("### 🕯️ About")
    st.markdown("A spooky story studio built to demonstrate open-weight AI and local-first creativity.")
    st.caption("Your saved stories stay in this project's local data folder.")

# ----------------------------- Main page -------------------------------------
st.markdown("""
<div class="hero">
  <div class="eyebrow">An offline-first storytelling experiment</div>
  <div class="hero-title">GhostTales</div>
  <div class="hero-sub">Step into the dark. Choose a place the world forgot, summon a story from the silence, and discover what waits just beyond the last page.</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="stat"><div class="stat-num">LOCAL-FIRST</div><div class="stat-label">Keep AI generation on your device</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="stat"><div class="stat-num">5 WORLDS</div><div class="stat-label">Five eerie settings to explore</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="stat"><div class="stat-num">∞ STORIES</div><div class="stat-label">Remix prompts and discover endings</div></div>', unsafe_allow_html=True)

st.write("")
left, right = st.columns([0.9, 1.1], gap="large")

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### 🕯️ Summon a story")
    with st.form("story_form"):
        setting = st.selectbox("Choose your setting", list(SCENES.keys()))
        mood = st.selectbox("Choose the atmosphere", list(MOODS.keys()))
        protagonist = st.text_input("Main character", placeholder="e.g. Rowan, a night-shift archivist")
        object_hint = st.text_input("A clue or cursed object (optional)", placeholder="e.g. a watch that runs backward")
        length_label = st.select_slider("Story length", options=["Flash (150 words)", "Short (350 words)", "Long (700 words)"], value="Short (350 words)")
        length = {"Flash (150 words)": 150, "Short (350 words)": 350, "Long (700 words)": 700}[length_label]
        custom = st.text_area("Your twist (optional)", placeholder="e.g. The ghost is trying to protect the protagonist.", height=90)
        submitted = st.form_submit_button("✦ Generate my ghost story", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        prompt = build_prompt(setting, mood, protagonist, object_hint, length, custom)
        with st.spinner("The spirits are gathering their words..."):
            try:
                if engine.startswith("Local"):
                    title, story = generate_with_ollama(prompt, model_name.strip(), ollama_url.strip())
                    source = f"Local AI · {model_name.strip()}"
                else:
                    title, story = local_fallback_story(setting, mood, protagonist, object_hint, length, custom)
                    source = "Built-in offline demo engine"
                st.session_state.current_story = {
                    "title": title,
                    "story": story,
                    "setting": setting,
                    "mood": mood,
                    "source": source,
                    "created_at": datetime.now().isoformat(timespec="minutes"),
                }
            except requests.exceptions.ConnectionError:
                st.error("Ollama isn't responding. Start Ollama and make sure the selected model is installed. You can switch to Demo mode to try the interface immediately.")
            except requests.exceptions.Timeout:
                st.error("The model took too long to respond. Try a shorter story or a smaller model.")
            except Exception as exc:
                st.error(f"Story generation failed: {exc}")

with right:
    st.markdown("### 📜 The story chamber")
    current = st.session_state.current_story
    if current:
        st.caption(f"{current['setting']}  ·  {current['mood']}  ·  {current['source']}")
        safe_title = re.sub(r"[<>]", "", current["title"])
        st.markdown(f'<div class="story"><h2>{safe_title}</h2>{current["story"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(chr(10), "<br><br>")}</div>', unsafe_allow_html=True)
        st.write("")
        action1, action2 = st.columns(2)
        with action1:
            st.download_button("⬇️ Download story", data=f"{current['title']}\n\n{current['story']}", file_name="ghosttales-story.txt", mime="text/plain", use_container_width=True)
        with action2:
            if st.button("♡ Save to library", use_container_width=True):
                saved = read_saved_stories()
                saved.insert(0, current)
                write_saved_stories(saved[:100])
                st.success("Story saved to your local library.")
    else:
        st.markdown("""
        <div class="story">
          <div style="font-size:2.8rem;margin-bottom:.8rem">🌘</div>
          <h2>The page is waiting...</h2>
          Choose a setting and an atmosphere, then generate your first story. Every tale begins with a door you probably should not open.
          <br><br><span style="color:#a4abc4">Tip: Try “Midnight train” with “Psychological horror” for a reality-bending mystery.</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("## 🗝️ Your story library")
saved_stories = read_saved_stories()
if not saved_stories:
    st.markdown('<div class="panel"><span class="small-muted">No stories saved yet. Save a story to keep it here between sessions.</span></div>', unsafe_allow_html=True)
else:
    st.caption(f"{len(saved_stories)} saved entr{'y' if len(saved_stories) == 1 else 'ies'} · stored locally in data/stories.json")
    for idx, item in enumerate(saved_stories):
        with st.expander(f"📖 {item.get('title', 'Untitled')} · {item.get('setting', 'Unknown setting')} · {item.get('created_at', '')}"):
            st.write(item.get("story", ""))
            st.download_button("Download this story", data=f"{item.get('title','Untitled')}\n\n{item.get('story','')}", file_name=f"ghosttales-story-{idx+1}.txt", mime="text/plain", key=f"download_{idx}")

st.markdown("---")
st.markdown('<p class="small-muted">GhostTales · Built for the “Ghost in the Machine” open-source AI theme. Demo mode uses built-in story templates; Ollama mode uses a locally installed model. Google Fonts load from the web, but the story engine can run offline after dependencies and model files are available.</p>', unsafe_allow_html=True)
