import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from voice_commit import ai, git


def test_has_staged_changes():
    with patch('voice_commit.git.subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.stdout = "diff --git a/file b/file"
        mock_run.return_value = mock_result
        
        assert git.has_staged_changes() == True

def test_no_staged_changes():
    with patch('voice_commit.git.subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_run.return_value = mock_result
        
        assert git.has_staged_changes() == False

@patch('voice_commit.ai._get_client')
def test_transcribe_audio(mock_get_client):
    mock_client = MagicMock()
    mock_transcript = MagicMock()
    mock_transcript.text = "this is a test"
    mock_client.audio.transcriptions.create.return_value = mock_transcript
    mock_get_client.return_value = mock_client
    
    # We use a mock path, the content doesn't matter since we mock the API
    with patch('builtins.open', unittest.mock.mock_open(read_data=b"data")):
        result = ai.transcribe_audio(Path("fake.wav"))
        assert result == "this is a test"

@patch('voice_commit.ai._get_client')
def test_generate_commit_message(mock_get_client):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "feat: add test feature"
    mock_response.choices = [MagicMock(message=mock_message)]
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client
    
    diff = "diff --git a/file b/file"
    instruction = "add test feature"
    result = ai.generate_commit_message(diff, instruction)
    
    assert result == "feat: add test feature"
    
def test_make_commit():
    with patch('voice_commit.git.subprocess.run') as mock_run:
        result = git.make_commit("feat: test commit")
        assert result == True
        mock_run.assert_called_once_with(["git", "commit", "-m", "feat: test commit"], check=True)
