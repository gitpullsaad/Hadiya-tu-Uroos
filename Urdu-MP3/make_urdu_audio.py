"""Turn Urdu-MP3/text/*.txt into MP3 files in Urdu-MP3/ using Microsoft's
natural Urdu voices (edge-tts). Needs network access to speech.platform.bing.com.

Usage: python3 make_urdu_audio.py [--voice ur-PK-AsadNeural] [file.txt ...]
Paragraphs are separated by blank lines; a line starting with '#' is a heading
(read with a longer pause). Only changed texts are rebuilt.
"""
import argparse, asyncio, os, pathlib, subprocess, tempfile

import edge_tts

HERE = pathlib.Path(__file__).parent


def blocks(txt):
    for raw in txt.strip().split("\n\n"):
        t = " ".join(raw.split())
        if t:
            yield (t.startswith("#"), t.lstrip("#").strip())


async def speak(text, path, voice, rate, sem):
    async with sem:
        for attempt in range(5):
            try:
                await edge_tts.Communicate(text, voice, rate=rate,
                                           proxy=os.environ.get("HTTPS_PROXY")).save(path)
                return
            except Exception as e:  # network hiccup: retry with backoff
                if attempt == 4:
                    raise
                await asyncio.sleep(2 ** attempt)


async def build(src, out, voice, rate):
    with tempfile.TemporaryDirectory() as d:
        d = pathlib.Path(d)
        items = list(blocks(src.read_text(encoding="utf-8")))
        sem = asyncio.Semaphore(4)
        await asyncio.gather(*[speak(t, str(d / f"{i:04d}.mp3"), voice, rate, sem)
                               for i, (_, t) in enumerate(items)])
        for i in range(len(items)):  # decode to WAV so concat has clean timestamps
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(d / f"{i:04d}.mp3"),
                            "-ar", "24000", "-ac", "1", str(d / f"{i:04d}.wav")], check=True)
        for name, secs in (("short", 0.7), ("long", 1.4)):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                            "anullsrc=r=24000:cl=mono", "-t", str(secs), str(d / f"{name}.wav")], check=True)
        lst = d / "list.txt"
        with lst.open("w") as f:
            for i, (head, _) in enumerate(items):
                if head:
                    f.write(f"file '{d / 'short.wav'}'\n")
                f.write(f"file '{d / f'{i:04d}.wav'}'\n")
                f.write(f"file '{d / ('long.wav' if head else 'short.wav')}'\n")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                        "-i", str(lst), "-ar", "24000", "-ac", "1", "-b:a", "64k",
                        "-metadata", f"title={src.stem}", "-metadata", "album=ہدیۃ العروس", str(out)],
                       check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default="ur-PK-AsadNeural")
    ap.add_argument("--rate", default="-10%")
    ap.add_argument("files", nargs="*")
    a = ap.parse_args()
    files = [pathlib.Path(f) for f in a.files] or sorted((HERE / "text").glob("*.txt"))
    for f in files:
        out = HERE / (f.stem + ".mp3")
        if out.exists() and out.stat().st_mtime > f.stat().st_mtime:
            print("skip", out.name)
            continue
        asyncio.run(build(f, out, a.voice, a.rate))
        print("wrote", out.name, flush=True)


if __name__ == "__main__":
    main()
