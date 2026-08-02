# voice-commit - AI Agent Guidelines

This file provides context and instructions for AI agents (like Claude, Cursor, Copilot) when operating in this repository.

## Project Context
- **Primary Goal:** Provide a CLI tool that uses local microphone input to generate perfect conventional commits via OpenAI's Whisper and GPT APIs.
- **Tech Stack:** Python 3.9+, `sounddevice` (audio), `openai` (API), `rich` (CLI UI).

## Coding Standards
1. **No bloated dependencies:** We try to keep the dependency footprint extremely small. Do not introduce new heavy libraries unless absolutely necessary.
2. **Type Hints:** All new functions must include Python type hints.
3. **Error Handling:** Gracefully catch exceptions (especially API errors or microphone missing errors) and use `rich` console to print beautiful, user-friendly error messages.

## Testing
- Ensure you run `pytest` before committing any code changes.
- Tests should mock `subprocess.run` (for git commands), `sounddevice` (for audio), and `openai.OpenAI` (for API calls) to ensure tests can run in a CI environment without real credentials or hardware.

## Architecture
- `cli.py`: The entry point and UI logic.
- `audio.py`: Handles all microphone interaction.
- `ai.py`: Handles LLM and transcription API calls.
- `git.py`: Wraps `git` CLI operations.
