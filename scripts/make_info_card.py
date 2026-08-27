from pathlib import Path
from xml.sax.saxutils import escape

from profile import PROFILE


OUTPUT = Path(__file__).resolve().parent.parent / "info-card.svg"


def line(y: int, label: str, value: str, delay: float) -> str:
    return f'''<g class="line" style="animation-delay:{delay}s">
  <text x="28" y="{y}" class="key">{escape(label)}</text>
  <text x="154" y="{y}" class="value">{escape(value)}</text>
</g>'''


def main() -> None:
    rows = [
        (76, "name", PROFILE["name"]),
        (108, "role", PROFILE["role"]),
        (140, "based", PROFILE["location"]),
        (172, "focus", PROFILE["focus"]),
        (204, "stack", PROFILE["stack"]),
        (236, "now", PROFILE["exploring"]),
    ]
    lines = "\n".join(line(y, label, value, index * 0.18 + 0.2) for index, (y, label, value) in enumerate(rows))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="490" height="270" viewBox="0 0 490 270" role="img" aria-label="Profile information for {escape(PROFILE["name"])}">
<style>
  .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1; }}
  .bar {{ fill: #161b22; }}
  text {{ font-family: Consolas, "Courier New", monospace; font-size: 14px; }}
  .title {{ fill: #e6edf3; font-size: 13px; }}
  .key {{ fill: #58a6ff; }} .value {{ fill: #c9d1d9; }}
  .line {{ opacity: 0; transform: translateX(-7px); animation: print 0.35s ease-out forwards; }}
  @keyframes print {{ to {{ opacity: 1; transform: translateX(0); }} }}
</style>
<rect class="bg" x="0.5" y="0.5" width="489" height="269" rx="6"/>
<path class="bar" d="M6 0h478a6 6 0 0 1 6 6v32H0V6a6 6 0 0 1 6-6z"/>
<circle cx="19" cy="19" r="5" fill="#ff5f56"/><circle cx="37" cy="19" r="5" fill="#ffbd2e"/><circle cx="55" cy="19" r="5" fill="#27c93f"/>
<text class="title" x="82" y="24">neofetch --profile</text>
{lines}
</svg>'''
    OUTPUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()