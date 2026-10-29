import subprocess
import math
import struct
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.pipeline.recap_smart_sync import render_smart_sync


def test_smart_sync_mixes_background_sfx():
    with tempfile.TemporaryDirectory(prefix="recap-sfx-test-") as temp:
        work = Path(temp)
        video = work / "source.mp4"
        tts = work / "tts.wav"
        background = work / "background.wav"
        output = work / "rendered.mp4"

        subprocess.run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "lavfi", "-i", "testsrc=size=320x240:rate=30:duration=2",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", str(video),
        ], check=True)
        subprocess.run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "2",
            "-c:a", "pcm_s16le", str(tts),
        ], check=True)
        subprocess.run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "lavfi", "-i", "sine=frequency=880:sample_rate=44100:duration=2",
            "-filter:a", "volume=0.25", "-c:a", "pcm_s16le", str(background),
        ], check=True)

        render_smart_sync(
            video, tts,
            [
                {"video_start": 0.0, "video_end": 1.0, "slot_duration": 1.0},
                {"video_start": 1.0, "video_end": 2.0, "slot_duration": 1.0},
            ],
            output, work / "render-work", background_audio_path=background,
        )

        decoded = subprocess.run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(output),
            "-vn", "-ac", "1", "-ar", "44100", "-f", "s16le", "pipe:1",
        ], check=True, stdout=subprocess.PIPE).stdout
        samples = struct.unpack("<" + "h" * (len(decoded) // 2), decoded)
        rms = math.sqrt(sum((sample / 32768.0) ** 2 for sample in samples) / len(samples))
        assert rms > 0.01, f"background stem was not audible; RMS={rms:.4f}"


if __name__ == "__main__":
    test_smart_sync_mixes_background_sfx()
    print("Smart Sync background/SFX integration test: PASS")
