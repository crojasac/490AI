import sys
import os
import subprocess
from pathlib import Path
from wordcloud import WordCloud, STOPWORDS


def _decode_with_fallbacks(data: bytes) -> tuple[str, str]:
    """Decode bytes trying common encodings; last resort replaces errors.

    Returns (text, encoding_used).
    """
    encodings = [
        "utf-8",
        "utf-8-sig",
        "cp1252",      # common on Windows
        "latin-1",     # permissive; never fails
        "mac_roman",   # older Mac files
    ]
    for enc in encodings:
        try:
            return data.decode(enc), enc
        except UnicodeDecodeError:
            continue
    # Fallback: decode as UTF-8 replacing invalid bytes
    return data.decode("utf-8", errors="replace"), "utf-8-replace"

# %%
def read_source_text() -> str:
    script_dir = Path(__file__).resolve().parent
    txt_path = script_dir / "wordcloud.txt"
    if not txt_path.exists():
        raise FileNotFoundError(f"Expected file not found: {txt_path}")
    raw = txt_path.read_bytes()
    text, used = _decode_with_fallbacks(raw)
    # Optional: inform user if non-UTF-8 used
    if used not in ("utf-8", "utf-8-sig"):
        print(f"Note: decoded {txt_path.name} using '{used}'.")
    return text


def generate_wordcloud(text: str, out_path: Path) -> None:
    wc = WordCloud(
        width=1600,
        height=900,
        background_color="white",
        stopwords=STOPWORDS,
        collocations=True,
    ).generate(text)
    wc.to_file(str(out_path))


def open_with_default_viewer(path: Path) -> None:
    if sys.platform.startswith("darwin"):
        subprocess.run(["open", str(path)], check=False)
    elif os.name == "nt":
        os.startfile(str(path))  # type: ignore[attr-defined]
    else:
        subprocess.run(["xdg-open", str(path)], check=False)


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    out_path = script_dir / "wordcloud.png"
    text = read_source_text()
    generate_wordcloud(text, out_path)
    print(f"Saved: {out_path}")
    open_with_default_viewer(out_path)


if __name__ == "__main__":
    main()

