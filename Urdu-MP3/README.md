# Urdu-MP3 — ہدیۃ العروس (Urdu audio)

The book's content in Urdu, one MP3 per chapter, read by Microsoft's natural Pakistani Urdu voice (`ur-PK-AsadNeural`), slightly slowed down.

These are **summaries in Urdu**, written from the study notes (`.claude/skills/hadiya-tul-uroos/references/notes.md`). They follow the book's chapter and section order and keep its rulings, evidence and the author's preferred views. They are not the author's exact words. Each file has the chapter's content only, with no lecture framing and nothing added.

| File | باب |
|---|---|
| `00-pesh-lafz.mp3` | پیش لفظ |
| `01-baab-1.mp3` | نکاح کی ضرورت اور اسے ترک کرنے کے نقصانات |
| `02-baab-2.mp3` | نکاح کا اسلامی طریقہ: رشتے کے انتخاب سے ولیمے تک |
| `03-baab-3.mp3` | شادی بیاہ کی رسومات اور جہیز |
| `04-baab-4.mp3` | میاں بیوی، نومولود اور سسرال کے حقوق |
| `05-baab-5.mp3` | متعہ، حلالہ، شغار |
| `06-baab-6.mp3` | طلاق اور عدت |
| `07-baab-7.mp3` | متفرق اور پیچیدہ مسائل |
| `08-baab-8.mp3` | ظہار، ایلاء، لعان |
| `09-baab-9.mp3` | میاں بیوی کے خصوصی مسائل اور پردہ |
| `10-baab-10.mp3` | تعدد ازدواج |
| `11-baab-11.mp3` | اسلام اور ضبطِ ولادت |
| `12-baab-12.mp3` | گھریلو ٹوٹکے اور نسخے |

- `text/` holds the Urdu text of each file, so you can read along.
- `make_urdu_audio.py` rebuilds the MP3s after a text is edited; only changed files are rebuilt. It needs network access to `speech.platform.bing.com`. Use `--voice ur-PK-UzmaNeural` for the female voice.
