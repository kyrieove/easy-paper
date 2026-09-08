"""Save a draft as a new guide revision without replacing the reader's notes."""
import argparse
from pathlib import Path


def save_guide(draft, target):
    content = Path(draft).read_text(encoding="utf-8")
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    revision = 1
    while True:
        candidate = (target if revision == 1 else
                     target.with_name(f"{target.stem}-r{revision}{target.suffix}"))
        try:
            with candidate.open("x", encoding="utf-8") as stream:
                stream.write(content)
            return candidate
        except FileExistsError:
            revision += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft")
    parser.add_argument("target")
    args = parser.parse_args()
    print(save_guide(args.draft, args.target))
