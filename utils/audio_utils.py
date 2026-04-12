# Try importing sounddevice safely
try:
    import sounddevice as sd
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    SOUNDDEVICE_AVAILABLE = False

import soundfile as sf
import numpy as np

SAMPLE_RATE = 16000


def record_audio(duration=3, device=0):
    """
    Record audio from microphone (only if available)
    """
    if not SOUNDDEVICE_AVAILABLE:
        raise RuntimeError("Microphone recording not supported in this environment")

    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        device=device
    )
    sd.wait()
    return audio.flatten()


def save_audio(file_path, audio):
    """
    Save audio to WAV file
    """
    sf.write(file_path, audio, SAMPLE_RATE)


def load_audio_for_waveform(file_path):
    """
    Load audio for visualization
    """
    import librosa
    y, sr = librosa.load(file_path, sr=SAMPLE_RATE)
    return y


def normalize_audio(audio):
    """
    Normalize audio signal
    """
    return audio / np.max(np.abs(audio))