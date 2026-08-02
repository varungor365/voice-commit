import os
from openai import OpenAI
from pathlib import Path
from typing import Tuple

def _get_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set. Please set it to use voice-commit.")
    return OpenAI(api_key=api_key)

def transcribe_audio(file_path: Path) -> str:
    """Transcribe audio file to text using Whisper."""
    client = _get_client()
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
    return transcript.text

def generate_commit_message(diff: str, voice_instruction: str) -> str:
    """Generate a conventional commit message from diff and voice instruction."""
    client = _get_client()
    
    system_prompt = """You are an expert developer who writes perfect conventional commit messages.
Your task is to take the git diff and the user's voice instruction, and output ONLY a valid conventional commit message.
Format:
<type>[optional scope]: <description>

[optional body]

Rules:
1. Output ONLY the commit message. No markdown formatting, no explanations.
2. Use standard types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert.
3. The description must be lowercase and imperative mood (e.g. "add feature" not "added feature").
4. Incorporate the user's voice instruction as the primary intent, using the diff for technical context."""

    user_prompt = f"VOICE INSTRUCTION:\n{voice_instruction}\n\nGIT DIFF:\n{diff}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0
    )
    
    return response.choices[0].message.content.strip()
