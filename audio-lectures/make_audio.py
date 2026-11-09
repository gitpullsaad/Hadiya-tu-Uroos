"""Turn the lecture scripts in scripts/*.md into MP3 files in mp3/.

Uses the offline Kokoro TTS model (kokoro-onnx). Model files are not in the repo;
download them once and pass their folder with --models:
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin

Usage: python3 make_audio.py --models DIR [script.md ...]
"""
import argparse, pathlib, re, subprocess, sys, tempfile

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

HERE = pathlib.Path(__file__).parent
VOICE, SPEED = "am_michael", 0.92


def blocks(md: str):
    """Yield (kind, text) where kind is 'heading' or 'para'."""
    for raw in re.split(r"\n\s*\n", md.strip()):
        text = " ".join(raw.split())
        if not text:
            continue
        if text.startswith("#"):
            yield "heading", text.lstrip("#").strip().replace(" — ", ". ")
        else:
            yield "para", text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", required=True)
    ap.add_argument("files", nargs="*")
    a = ap.parse_args()
    m = pathlib.Path(a.models)
    k = Kokoro(str(m / "kokoro-v1.0.onnx"), str(m / "voices-v1.0.bin"))
    files = [pathlib.Path(f) for f in a.files] or sorted((HERE / "scripts").glob("*.md"))
    out_dir = HERE / "mp3"
    out_dir.mkdir(exist_ok=True)
    for f in files:
        out = out_dir / (f.stem + ".mp3")
        if out.exists() and out.stat().st_mtime > f.stat().st_mtime:
            print("skip", out.name)
            continue
        parts, sr = [], 24000
        for kind, text in blocks(f.read_text()):
            audio, sr = k.create(text, voice=VOICE, speed=SPEED, lang="en-us")
            gap = 1.0 if kind == "heading" else 0.6
            parts += [np.zeros(int(0.3 * sr), dtype=np.float32)] if kind == "heading" else []
            parts += [audio, np.zeros(int(gap * sr), dtype=np.float32)]
        with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
            sf.write(tmp.name, np.concatenate(parts), sr)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp.name,
                            "-ac", "1", "-b:a", "48k", "-metadata", f"title={f.stem}",
                            "-metadata", "album=Hadiya tul Uroos lectures", str(out)], check=True)
        print("wrote", out.name, flush=True)


if __name__ == "__main__":
    sys.exit(main())
