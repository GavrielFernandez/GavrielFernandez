import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

from profile import PROFILE


OUTPUT = Path(__file__).resolve().parent.parent / "data" / "contributions.json"


class ContributionParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.days: list[dict[str, int | str]] = []

    def handle_starttag(self, tag: str, attributes: list[tuple[str, str | None]]) -> None:
        attrs = dict(attributes)
        if "data-date" in attrs and "data-level" in attrs:
            self.days.append({"date": attrs["data-date"] or "", "level": int(attrs["data-level"] or 0)})


def main() -> None:
    url = f"https://github.com/users/{PROFILE['username']}/contributions"
    request = Request(url, headers={"User-Agent": "GitHub-profile-README"})
    with urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8")

    parser = ContributionParser()
    parser.feed(html)
    if not parser.days:
        raise RuntimeError("GitHub returned no contribution days. Check the username or try again later.")

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps({"username": PROFILE["username"], "days": parser.days}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()