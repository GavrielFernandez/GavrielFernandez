from pathlib import Path


OUTPUT = Path(__file__).resolve().parent.parent / "portrait.svg"


def main() -> None:
    rows = ["   GGGG   FFFFFFF", "  GG  GG  FF     ", " GG        FFFFF  ", " GG   GGG  FF     ", "  GG   GG  FF     ", "   GGGG G  FF     "]
    text_rows = "\n".join(
        f'<text x="28" y="{66 + index * 26}" class="row" style="animation-delay:{index * 0.17 + 0.15}s">{row}</text>'
        for index, row in enumerate(rows)
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="370" height="270" viewBox="0 0 370 270" role="img" aria-label="Animated GF ASCII portrait placeholder">
<style>
  .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1; }}
  text {{ font-family: Consolas, "Courier New", monospace; }}
  .row {{ fill: #8b949e; font-size: 20px; opacity: 0; animation: type 0.38s steps(18, end) forwards; }}
  .caption {{ fill: #58a6ff; font-size: 13px; }}
  @keyframes type {{ from {{ opacity: 0; transform: translateX(-10px); }} to {{ opacity: 1; transform: translateX(0); }} }}
</style>
<rect class="bg" x="0.5" y="0.5" width="369" height="269" rx="6"/>
<text x="28" y="34" class="caption">[ GF ] portrait loading...</text>
{text_rows}
<text x="28" y="244" class="caption">awaiting source-photo.jpg</text>
</svg>'''
    OUTPUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()