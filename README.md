# 👻 GhostTales — An Offline Ghost Story Generator Powered by Open AI

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 4: Ghost in the Machine](https://dev.to/challenges/hacktoberfest-week4-2026-10-26)*

## What I Built

**GhostTales** is a dark-themed, offline-first ghost story generator that brings supernatural storytelling to life through an interactive web application.

Inspired by the *Ghost in the Machine* theme, I wanted to explore the idea of a mysterious creative voice living inside a computer — one that can turn a few simple prompts into an eerie story.

Users can choose from five atmospheric settings:

- 🏚️ Abandoned Mansion
- 🌲 Foggy Forest
- 🏘️ Forgotten Village
- 🚂 Midnight Train
- 🗼 Cursed Lighthouse

They can also select a storytelling mood, customize the protagonist, introduce a cursed object or clue, and add their own twist.

GhostTales includes a built-in demo mode, an optional local AI mode, a story library for saving favorites, and a download feature for keeping stories as text files.

The interface uses a dark background with purple and cyan accents to create an immersive, mysterious atmosphere.

## Demo

**Screenshots or video:** https://drive.google.com/file/d/1qmhSZDd0J7ekV8auaLcUKSoIypcy1nQY/view?usp=sharing

## Code

**GitHub repository:** https://github.com/prathamesh-1983/GhostTales-Project

The project includes:

- `app.py` — the Streamlit application, interface, story generation and local AI integration
- `requirements.txt` — Python dependencies
- `data/` — local story storage
- `README.md` — setup instructions, architecture and troubleshooting
- `LICENSE` — MIT License

The source code is organized to make the project easy to run, explore, and extend.

## How I Built It

I built GhostTales using Python and Streamlit, with a local-first architecture.

### Technology stack

- **Python:** Application logic and story generation
- **Streamlit:** Interactive web interface
- **Ollama:** Local model inference
- **Gemma:** Example open-weight language model
- **JSON:** Local storage for saved stories
- **HTML and CSS:** Dark visual styling within the Streamlit interface
- **Git and GitHub:** Source control and project sharing

### Two ways to generate stories

**1. Built-in demo mode**

The application includes a built-in Python story engine that works without installing a language model. It uses setting-specific details, story structures, and alternate titles to demonstrate the experience.

This makes the project easy to test on a beginner's computer.

**2. Local AI mode**

GhostTales can connect to Ollama running on the same computer and send prompts to a locally installed model.

For example, after installing Ollama and downloading a compatible model, I can select a setting such as *Midnight Train*, choose *Psychological Horror*, and ask the model to create a story with a custom twist.

The application sends the prompt to Ollama's local API and displays the generated response.

The model must be downloaded beforehand, but once the dependencies and model files are available, local inference can work without an internet connection.

## Why Does Open Innovation Matter?

For me, the most interesting part of this project is the possibility of creating something personal without making a remote AI service a permanent requirement.

Using an open-weight model with local inference makes several things possible:

- **Privacy:** Prompts can stay on the user's machine when the application is configured entirely for local inference.
- **Offline access:** Stories can be generated without an internet connection after the model and dependencies have been downloaded.
- **Experimentation:** Developers can try different compatible models and compare their storytelling styles.
- **Accessibility:** Users can explore generative AI without necessarily needing a paid, per-request cloud API.
- **Control:** The application can be modified, extended, and adapted to different creative needs.

A closed API can be convenient, but it may require an internet connection, impose usage limits, or send prompts to an external service.

With GhostTales, I wanted local AI to be more than a technical feature. It is part of the project's purpose: creativity that can live on your own machine.

The built-in demo mode also makes it possible to explore the interface without downloading a model, although it is a template-based generator rather than a language model.

## My Agent Session

This section is optional.

GhostTales is primarily a local AI storytelling application rather than an autonomous agent, so I have not included a DevRelay agent session.

If I record a development session using DevRelay, I can add the session link here.

## The Spirit of It 👻

Imagine sitting alone at midnight. Rain taps against the window, the room is quiet, and your laptop is the only source of light.

You choose *Foggy Forest*, select *Slow-burn Suspense*, and enter a mysterious clue.

A story begins to unfold.

The forest seems to listen. The footsteps behind the protagonist arrive half a second late. The path home disappears.

That is the experience I wanted GhostTales to capture: the feeling that a simple machine can become a doorway into a world of imagination.

The stories are fictional, but the experience is personal. Each prompt lets the user create a different little mystery.

And perhaps that is the ghost in the machine — not a literal spirit, but the unexpected sense of life that emerges when technology becomes a creative tool.

## Prize Categories

**Primary submission:** Hacktoberfest Open-Source AI Challenge Week 4 — Ghost in the Machine.

**Partner categories:** None claimed at this stage.

The project includes optional Ollama integration and an example Gemma model, but I will enter a partner-specific prize category only after verifying that the implementation meets that category's official requirements.

## What's Next?

I'd love to extend GhostTales with:

- Interactive stories with multiple endings
- A local library with search and filtering
- More narrator personalities and horror styles
- Multilingual story generation
- Optional text-to-speech narration
- Additional local models and model comparisons

Building GhostTales has been an opportunity to explore how open AI can support creativity while keeping local execution and user control in mind.

If you could summon one ghost story from your computer, **what would you want it to be about?**

Thanks for reading! 👻

#devchallenge #hf26challenge #opensource #python #ollama #gemma #generativeai
