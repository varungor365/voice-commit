import queue
import sys
import tempfile
from pathlib import Path

import sounddevice as sd
import soundfile as sf


class AudioRecorder:
    def __init__(self, sample_rate=16000, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.q = queue.Queue()
        self.recording = False
        self.stream = None
        
    def _callback(self, indata, frames, time, status):
        """This is called for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(indata.copy())

    def start_recording(self):
        self.recording = True
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=self._callback
        )
        self.stream.start()

    def stop_recording(self) -> Path:
        self.recording = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
        
        # Save to temp file
        temp_dir = tempfile.gettempdir()
        file_path = Path(temp_dir) / "voice_commit_temp.wav"
        
        # Collect all audio data from queue
        audio_data = []
        while not self.q.empty():
            audio_data.append(self.q.get())
            
        if not audio_data:
            return None
            
        import numpy as np
        audio_concat = np.concatenate(audio_data, axis=0)
        
        sf.write(str(file_path), audio_concat, self.sample_rate)
        return file_path
