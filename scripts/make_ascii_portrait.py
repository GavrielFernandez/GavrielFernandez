from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageEnhance, ImageOps


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "assets" / "source-photo.jpg"
OUTPUT = ROOT / "portrait.svg"
RAMP = " .`:-=+*#%@"


def image_to_rows(image: Image.Image, width: int = 42) -> list[str]:
    grayscale = ImageOps.grayscale(image)
    grayscale = ImageOps.autocontrast(grayscale, cutoff=1)
    grayscale = ImageEnhance.Contrast(grayscale).enhance(1.35)
    height = max(1, int(grayscale.height / grayscale.width * width * 0.5))
    pixels = grayscale.resize((width, height)).load()
    return ["".join(RAMP[pixels[x, y] * (len(RAMP) - 1) // 255] for x in range(width)) for y in range(height)]


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Add a portrait photo at {SOURCE.name} before running this script.")

    rows = image_to_rows(Image.open(SOURCE))
    line_height = 11
    height = max(270, 64 + len(rows) * line_height + 28)
    art = "\n".join(
        f'<text class="row" x="18" y="{54 + index * line_height}" style="animation-delay:{index * 0.045 + 0.1:.3f}s">{escape(row)}</text>'
        for index, row in enumerate(rows)
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="370" height="{height}" viewBox="0 0 370 {height}" role="img" aria-label="Animated ASCII portrait">
<style>
  .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1; }}
  text {{ font-family: Consolas, "Courier New", monospace; }}
  .title {{ fill: #58a6ff; font-size: 12px; }}
  .row {{ fill: #c9d1d9; font-size: 10px; opacity: 0; animation: print .2s linear forwards; }}
  @keyframes print {{ from {{ opacity: 0; transform: translateX(-7px); }} to {{ opacity: 1; transform: translateX(0); }} }}
</style>
<rect class="bg" x="0.5" y="0.5" width="369" height="{height - 1}" rx="6"/>
<text class="title" x="18" y="30">[ GF ] ASCII PORTRAIT</text>
{art}
</svg>'''
    OUTPUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()