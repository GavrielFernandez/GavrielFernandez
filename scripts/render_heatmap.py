import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "contributions.json"
OUTPUT = ROOT / "contrib-heatmap.svg"
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    days = data["days"][-371:]
    cells = []
    for index, entry in enumerate(days):
        week, day = divmod(index, 7)
        x, y = 48 + week * 15, 40 + day * 15
        level = min(int(entry["level"]), len(PALETTE) - 1)
        delay = (week + day) * 0.014
        cells.append(f'<rect class="cell" style="animation-delay:{delay:.3f}s" x="{x}" y="{y}" width="11" height="11" rx="2" fill="{PALETTE[level]}"/>')

    total = sum(1 for entry in days if int(entry["level"]) > 0)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="180" viewBox="0 0 860 180" role="img" aria-label="{data["username"]} contribution graph">
<style>
  .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1; }}
  text {{ font-family: Consolas, "Courier New", monospace; font-size: 12px; fill: #8b949e; }}
  .cell {{ opacity: 0; animation: reveal .28s ease-out forwards; }}
  @keyframes reveal {{ from {{ opacity: 0; transform: translate(-3px, -3px); }} to {{ opacity: 1; transform: translate(0, 0); }} }}
</style>
<rect class="bg" x="0.5" y="0.5" width="859" height="179" rx="6"/>
<text x="20" y="27">Sun</text><text x="20" y="72">Wed</text><text x="20" y="117">Sat</text>
{''.join(cells)}
<text x="48" y="160">{total} active days in the last 53 weeks</text>
<text x="680" y="160">Less</text><rect x="716" y="150" width="11" height="11" rx="2" fill="#161b22"/><rect x="731" y="150" width="11" height="11" rx="2" fill="#006d32"/><rect x="746" y="150" width="11" height="11" rx="2" fill="#26a641"/><rect x="761" y="150" width="11" height="11" rx="2" fill="#39d353"/><text x="780" y="160">More</text>
</svg>'''
    OUTPUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()