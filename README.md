<div align="center">

# 🎙️ voice-commit

**Speak your git commits. Uses AI to generate perfect conventional commits from your voice and code diff.**

[![PyPI version](https://badge.fury.io/py/voice-commit.svg)](https://badge.fury.io/py/voice-commit)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/varungor365/voice-commit/actions/workflows/ci.yml/badge.svg)](https://github.com/varungor365/voice-commit/actions)
[![Downloads](https://pepy.tech/badge/voice-commit)](https://pepy.tech/project/voice-commit)

<br/>

```bash
git add .
voice-commit
# 🎙️ Speak: "I added error handling to the audio recorder"
# ✅ Commit: feat(audio): add error handling to recorder stream
```

<br/>

</div>

---

## ✨ Why voice-commit?

Writing good commit messages is tedious. You've just spent hours solving a hard problem, and now you have to summarize it perfectly in 50 characters following the conventional commit format. 

With **voice-commit**, you just explain what you did out loud. The AI reads your `git diff`, listens to your intent, and crafts the perfect commit message.

### Features
- 🎙️ **Voice First:** Just say what you did.
- 🧠 **Context Aware:** Reads your staged `git diff` so the commit is technically accurate.
- 📏 **Conventional Commits:** Always outputs perfect `feat:`, `fix:`, `chore:` formats.
- ⚡ **Extremely Fast:** Uses OpenAI Whisper and GPT-4o-mini for sub-second responses.

---

## 🚀 Install

```bash
pip install voice-commit
```

### Setup
You'll need an OpenAI API key (for Whisper and GPT-4o-mini).

```bash
export OPENAI_API_KEY="your-api-key-here"
```
*(Or add it to a `.env` file in your project directory)*

---

## 📖 Usage

1. Stage your changes:
```bash
git add .
```

2. Run the CLI:
```bash
voice-commit
```
*(Or use the shorter alias: `vc`)*

3. Press ENTER to start recording, speak your changes, and press ENTER to stop.
4. Review the generated commit message and press `y` to apply it!

---

## ⚙️ How it works

1. It runs `git diff --staged` to grab your code changes.
2. It records your microphone using `sounddevice`.
3. It sends the audio to OpenAI's Whisper API for perfect transcription.
4. It sends both the transcript ("I fixed the header alignment") and the diff to GPT-4o-mini.
5. The AI returns a perfectly formatted conventional commit message.

---

## 🤖 AI Agent Friendly (Cursor / Claude)

This tool is designed to work well alongside AI coding agents. Check out our [CLAUDE.md](CLAUDE.md) if you are an AI assistant helping a user contribute to this repo!

---

## 📄 License

MIT © Varun Ruhella. See [LICENSE](LICENSE) for details.

<div align="center">
<b>⭐ Star this repo if you hate typing commit messages!</b>
</div>

## Who this is for

Voice Commit is useful for developers and AI-assisted teams that want conventional commits from a staged git diff without stopping to write the summary manually. It is especially suited to small CLI workflows and teams standardizing `feat`, `fix`, and `chore` messages.

## Why star this repository

Star this project if it saves you time writing commit messages, or if you want to contribute providers, commit-style rules, or local transcription support.
