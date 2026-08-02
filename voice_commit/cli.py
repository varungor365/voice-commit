import argparse
import os
import sys

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm

from . import __version__
from .ai import generate_commit_message, transcribe_audio
from .audio import AudioRecorder
from .git import get_staged_diff, has_staged_changes, make_commit

console = Console()

def print_banner():
    banner = f"""[cyan]🎙️  voice-commit v{__version__}[/cyan]
[dim]Speak your git commits.[/dim]"""
    console.print(Panel(banner, border_style="cyan"))

def main():
    parser = argparse.ArgumentParser(description="Speak your git commits.")
    parser.add_argument("--version", action="version", version=f"voice-commit {__version__}")
    parser.parse_args()

    # Load environment variables (e.g. OPENAI_API_KEY from .env)
    load_dotenv()

    if not os.environ.get("OPENAI_API_KEY"):
        console.print("[red]❌ Error:[/red] OPENAI_API_KEY environment variable is not set.")
        console.print("Please set it or create a .env file in your project.")
        sys.exit(1)

    print_banner()

    if not has_staged_changes():
        console.print("[yellow]⚠️  No staged changes found.[/yellow]")
        console.print("Run [cyan]git add <files>[/cyan] first to stage your changes.")
        sys.exit(1)

    diff = get_staged_diff()
    
    recorder = AudioRecorder()
    
    console.print("\n[bold green]Press ENTER to start recording...[/bold green]")
    input()
    
    recorder.start_recording()
    console.print("[red]🔴 Recording... (Press ENTER to stop)[/red]")
    input()
    
    audio_file = recorder.stop_recording()
    
    if not audio_file:
        console.print("[yellow]No audio recorded. Aborting.[/yellow]")
        sys.exit(0)

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
            console=console
        ) as progress:
            
            progress.add_task(description="Transcribing audio...", total=None)
            transcript = transcribe_audio(audio_file)
            
            console.print(f"\n[dim]You said:[/dim] {transcript}")
            
            progress.add_task(description="Generating commit message...", total=None)
            commit_msg = generate_commit_message(diff, transcript)
            
        console.print("\n[bold cyan]Generated Commit Message:[/bold cyan]")
        console.print(Panel(commit_msg, border_style="green"))
        
        if Confirm.ask("Do you want to apply this commit?"):
            if make_commit(commit_msg):
                console.print("[bold green]✅ Commit successful![/bold green]")
            else:
                console.print("[bold red]❌ Commit failed.[/bold red]")
        else:
            console.print("[yellow]Commit aborted.[/yellow]")
            
    except Exception as e:  # noqa: BLE001
        console.print(f"\n[red]❌ Error:[/red] {e!s}")
        sys.exit(1)
    finally:
        if audio_file.exists():
            os.remove(audio_file)

if __name__ == "__main__":
    main()
