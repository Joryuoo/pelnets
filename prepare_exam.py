"""Prepare PhilNITS AM/PM/Subject A/B PDFs, then build reviewed Obsidian cards.

Run ``python prepare_exam.py --help`` for the two-step workflow. This tool never
generates explanations or guesses answers; reviewed data is required to build.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from io import BytesIO
import json
from pathlib import Path
import re
import shutil
import sys

import pymupdf
from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parent
TOPICS = frozenset(
    "number-systems operating-systems project-management accounting probability "
    "cybersecurity systems-architecture sets digital-logic algorithms hardware "
    "service-management data-structures programming web-technologies "
    "information-management statistics networking math business-administration "
    "software software-testing software-engineering devops "
    "object-oriented-programming automata-theory data-encoding cloud-computing "
    "artificial-intelligence".split()
)
PDF_NAME = re.compile(r"^(\d{4})(S|A|Apr|Oct|May)_FE(?:_|-)(AM|PM|A|B)_Questions?$", re.I)
Q_HEADING = re.compile(r"^Q(\d{1,2})\.?(?:\s|$)", re.I)
SQ_HEADING = re.compile(r"^Subquestion(?:\s+(\d+))?$", re.I)


def pdf_identity(pdf: Path) -> tuple[str, str, str]:
    match = PDF_NAME.fullmatch(pdf.stem)
    if not match:
        raise ValueError(f"Unrecognized question PDF name: {pdf.name}")
    year, season, paper = match.groups()
    season = {"apr": "S", "may": "S", "oct": "A"}.get(season.lower(), season.upper())
    return year, season, paper.upper()


def text_lines(page: pymupdf.Page):
    """Return spatially ordered PDF lines, not substring search matches."""
    lines = []
    for block in page.get_text("dict")["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            content = "".join(span["text"] for span in line["spans"]).strip()
            if content:
                lines.append((line["bbox"][1], line["bbox"][0], content))
    return sorted(lines)


def find_boundaries(doc: pymupdf.Document, paper: str):
    candidates: dict[int, list[tuple[int, float]]] = {}
    subquestions: dict[int, list[tuple[int, float, int | None]]] = {}
    current_q = None
    for page_no, page in enumerate(doc):
        for y, x, content in text_lines(page):
            q_match = Q_HEADING.match(content)
            if q_match and re.match(r"^[-–—,]", content[q_match.end():].lstrip()):
                q_match = None  # "Q1 – Q80" in instructions is not a question.
            if q_match and x < page.rect.width * 0.35:
                q = int(q_match.group(1))
                candidates.setdefault(q, []).append((page_no, max(0, y - 4)))
                current_q = q
                continue
            if paper == "PM" and current_q is not None:
                sq_match = SQ_HEADING.fullmatch(content)
                if sq_match and x < page.rect.width * 0.4:
                    number = int(sq_match.group(1)) if sq_match.group(1) else None
                    subquestions.setdefault(current_q, []).append(
                        (page_no, max(0, y - 4), number)
                    )
    if not candidates:
        raise ValueError("No question headings found; this PDF needs manual boundary review")
    questions = {}
    for q, positions in candidates.items():
        if len(positions) == 1:
            questions[q] = positions[0]
        elif paper in ("AM", "A") and q == 1 and 2 in candidates:
            # Older papers introduce the notation with a sample Q1 before the exam.
            before_q2 = [pos for pos in positions if pos < candidates[2][0]]
            if not before_q2:
                raise ValueError("Could not identify the actual Q1 heading")
            questions[q] = before_q2[-1]
        else:
            print(f"Warning: Duplicate Q{q} headings: {positions}. Using the first one.")
            questions[q] = positions[0]
    actual = sorted(questions)
    if actual != list(range(1, actual[-1] + 1)):
        raise ValueError(f"Question headings are incomplete: {actual}")
    if paper == "PM":
        for q in actual:
            markers = subquestions.get(q, [])
            if not markers:
                raise ValueError(f"Q{q} has no exact Subquestion heading")
            numbers = [number for _, _, number in markers]
            if len(markers) == 1 and numbers[0] is None:
                pass
            elif numbers != list(range(1, len(markers) + 1)):
                raise ValueError(f"Q{q} subquestion headings are ambiguous: {numbers}")
            start = questions[q]
            end = questions.get(q + 1, (len(doc) - 1, doc[-1].rect.height))
            if not (start < markers[0][:2] and markers[-1][:2] < end):
                raise ValueError(f"Q{q} has a subquestion outside its question range")
    return questions, subquestions


def segment_text(doc, start, end) -> str:
    result = []
    for page_no in range(start[0], end[0] + 1):
        page = doc[page_no]
        top = start[1] if page_no == start[0] else 45
        bottom = end[1] if page_no == end[0] else page.rect.height - 30
        if bottom - top > 12:
            result.append(page.get_text(clip=pymupdf.Rect(0, top, page.rect.width, bottom)))
    return "\n".join(result).strip()


def render_segment(doc, start, end, output: Path, prefix: str) -> list[str]:
    names = []
    for page_no in range(start[0], end[0] + 1):
        page = doc[page_no]
        top = start[1] if page_no == start[0] else 45
        bottom = end[1] if page_no == end[0] else page.rect.height - 30
        if bottom - top <= 12:
            continue
        pix = page.get_pixmap(
            clip=pymupdf.Rect(30, top, page.rect.width - 30, bottom),
            dpi=170, alpha=False,
        )
        image = Image.open(BytesIO(pix.tobytes("png"))).convert("RGB")
        diff = ImageChops.difference(
            image, Image.new("RGB", image.size, "white")
        ).convert("L")
        bbox = diff.point(lambda value: 255 if value > 25 else 0).getbbox()
        if bbox is None:
            continue
        pad = 14
        image = image.crop((
            max(0, bbox[0] - pad), max(0, bbox[1] - pad),
            min(image.width, bbox[2] + pad), min(image.height, bbox[3] + pad),
        ))
        if image.height < 35:
            continue
        name = f"{prefix}_p{len(names) + 1}.png"
        image.save(output / name, optimize=True)
        names.append(name)
    if not names:
        raise ValueError(f"No visible image content for {prefix}")
    if len(names) == 1 and "_Body" not in prefix and "_SQ" not in prefix:
        old = output / names[0]
        new = output / f"{prefix}_full.png"
        old.rename(new)
        names = [new.name]
    return names


def answer_pdf_for(question_pdf: Path) -> Path | None:
    candidates = [
        question_pdf.with_name(question_pdf.name.replace("_Questions.pdf", "_Answers.pdf")),
        question_pdf.with_name(question_pdf.name.replace("_Question.pdf", "_Answer.pdf")),
    ]
    return next((path for path in candidates if path != question_pdf and path.exists()), None)


def prepare(question_pdf: Path, work: Path) -> dict:
    year, season, paper = pdf_identity(question_pdf)
    if work.exists() and any(work.iterdir()):
        raise FileExistsError(f"Work directory is not empty: {work}")
    work.mkdir(parents=True, exist_ok=True)
    (work / "images").mkdir()
    (work / "contexts").mkdir()
    doc = pymupdf.open(question_pdf)
    questions, subquestions = find_boundaries(doc, paper)
    prefix = f"{year}{season}_FE_{paper}" if paper in ("AM", "PM") else f"{year}{season}_FE-{paper}"
    cards = []
    for q, start in sorted(questions.items()):
        end = questions.get(q + 1, (len(doc) - 1, doc[-1].rect.height))
        if paper != "PM":
            key = str(q)
            text = segment_text(doc, start, end)
            (work / "contexts" / f"{key}.txt").write_text(text, encoding="utf-8")
            images = render_segment(doc, start, end, work / "images", f"{prefix}_Q{q}")
            title = f"{year}{season}_FE_{q}" if paper == "AM" else f"{year}{season}_FE-{paper}_{q}"
            cards.append({"key": key, "question": q, "title": title,
                          "context": f"contexts/{key}.txt", "images": images})
        else:
            markers = [marker[:2] for marker in subquestions[q]]
            body = segment_text(doc, start, markers[0])
            body_images = render_segment(
                doc, start, markers[0], work / "images", f"{prefix}_Q{q}_Body"
            )
            (work / "contexts" / f"Q{q}_body.txt").write_text(body, encoding="utf-8")
            for sq, sq_start in enumerate(markers, 1):
                sq_end = markers[sq] if sq < len(markers) else end
                key = f"{q}.{sq}"
                sq_text = segment_text(doc, sq_start, sq_end)
                (work / "contexts" / f"Q{q}_SQ{sq}.txt").write_text(
                    sq_text, encoding="utf-8"
                )
                images = render_segment(
                    doc, sq_start, sq_end, work / "images", f"{prefix}_Q{q}_SQ{sq}"
                )
                cards.append({"key": key, "question": q, "subquestion": sq,
                              "title": f"{year}{season}_FE_PM_{key}",
                              "context": [f"contexts/Q{q}_body.txt", f"contexts/Q{q}_SQ{sq}.txt"],
                              "images": body_images + images if sq == 1 else images})
    answer_pdf = answer_pdf_for(question_pdf)
    if answer_pdf:
        with pymupdf.open(answer_pdf) as answer_doc:
            answer_text = "\n".join(page.get_text() for page in answer_doc)
        (work / "answer_key.txt").write_text(answer_text, encoding="utf-8")
    manifest = {"schema": 1, "source": str(question_pdf.resolve()),
                "answer_source": str(answer_pdf.resolve()) if answer_pdf else None,
                "year": year, "season": season, "paper": paper, "cards": cards}
    (work / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    example = {card["key"]: {"topics": [], "answer": "", "explanation": ""}
               for card in cards}
    if paper in ("AM", "A"):
        for value in example.values():
            value["front_text"] = ""  # Use for plain-text cards; leave empty for images.
    (work / "review.example.json").write_text(
        json.dumps(example, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return manifest


def validate_review(manifest: dict, review: dict) -> None:
    if not isinstance(review, dict):
        raise ValueError("Review JSON must be an object keyed by card")
    keys = {card["key"] for card in manifest["cards"]}
    if set(review) != keys:
        raise ValueError(f"Review keys differ from manifest: missing={keys-set(review)}, extra={set(review)-keys}")
    for card in manifest["cards"]:
        key = card["key"]
        data = review[key]
        if not isinstance(data, dict):
            raise ValueError(f"{key}: review entry must be an object")
        topics = data.get("topics")
        if (not isinstance(topics, list) or not 1 <= len(topics) <= 3
                or not all(isinstance(topic, str) for topic in topics)
                or len(topics) != len(set(topics))):
            raise ValueError(f"{key}: choose 1–3 distinct topics")
        if not set(topics) <= TOPICS:
            raise ValueError(f"{key}: unregistered topics: {set(topics)-TOPICS}")
        if not isinstance(data.get("answer"), str) or not isinstance(data.get("explanation"), str):
            raise ValueError(f"{key}: answer and explanation must be text")
        if manifest["paper"] in ("AM", "A") and not isinstance(data.get("front_text", ""), str):
            raise ValueError(f"{key}: front_text must be text")
        sources = data.get("references", [])
        if (not isinstance(sources, list) or not all(
                isinstance(source, str) and source.strip() for source in sources)):
            raise ValueError(f"{key}: references must be a list of nonempty text entries")
        answer = data["answer"].strip()
        explanation = data["explanation"].strip()
        if len(explanation) < 40 or "```mermaid" in explanation.lower():
            raise ValueError(f"{key}: explanation is missing, too short, or uses Mermaid")
        if manifest["paper"] == "PM":
            if not re.fullmatch(r"[a-j](?:,\s*[a-j])*", answer, re.I):
                raise ValueError(f"{key}: PM answer must be comma-separated letters")
        elif not re.fullmatch(r"[a-j]\)(?:\s+.+)?", answer, re.I):
            raise ValueError(f"{key}: answer needs a letter and choice text")
        if manifest["paper"] in ("AM", "A") and data.get("front_text"):
            front = data["front_text"].strip()
            if "\n?\n" in front or not all(
                re.search(rf"(?m)^{letter}\)", front) for letter in "abcd"
            ):
                raise ValueError(f"{key}: plain-text front needs complete choices a)–d)")


def build(work: Path, review_path: Path, root: Path) -> int:
    manifest = json.loads((work / "manifest.json").read_text(encoding="utf-8"))
    review = json.loads(review_path.read_text(encoding="utf-8"))
    validate_review(manifest, review)
    notes = root / manifest["year"]
    if manifest["paper"] == "PM":
        notes /= "PM"
    images_dir = root / "Files"
    target_notes = [notes / f'{card["title"]}.md' for card in manifest["cards"]]
    selected_images = {
        image for card in manifest["cards"]
        if not (manifest["paper"] in ("AM", "A") and review[card["key"]].get("front_text"))
        for image in card["images"]
    }
    # Check every destination before writing anything. Existing draft cards are sacred.
    conflicts = [path for path in target_notes if path.exists()]
    conflicts += [images_dir / image for image in selected_images if (images_dir / image).exists()]
    if conflicts:
        raise FileExistsError(f"Refusing to overwrite {len(conflicts)} existing file(s): {conflicts[:4]}")
    if any(not (work / "images" / image).exists() for image in selected_images):
        raise FileNotFoundError("A prepared image is missing")
    notes.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)
    for image in sorted(selected_images):
        shutil.copy2(work / "images" / image, images_dir / image)
    created = datetime.now().strftime("%Y-%m-%d %H:%M")
    for card, target in zip(manifest["cards"], target_notes):
        data = review[card["key"]]
        topic_tags = "\n".join(
            f'  - {topic}/{manifest["year"]}' for topic in data["topics"]
        )
        front = data.get("front_text", "").strip() if manifest["paper"] in ("AM", "A") else ""
        if not front:
            front = "\n".join(f"![[{image}]]" for image in card["images"])
        text = (f'---\ncreated: {created}\nstatus: "#philnits"\ntags:\n'
                f'{topic_tags}\n  - year/{manifest["year"]}\n---\n\n'
                f'# {card["title"]}\n\n{front}\n?\n{data["answer"].strip()}\n\n'
                f'### Explanation\n{data["explanation"].strip()}\n\n---\n')
        sources = data.get("references", [])
        if sources:
            text += "\n# References\n" + "\n".join(
                f"- {source.strip()}" for source in sources
            ) + "\n"
        target.write_text(text, encoding="utf-8")
    return len(target_notes)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prep = commands.add_parser("prepare", help="Extract boundaries, context and images into a new work directory")
    prep.add_argument("question_pdf", type=Path)
    prep.add_argument("--work", type=Path, required=True)
    build_command = commands.add_parser("build", help="Build cards from a complete, human-reviewed JSON file")
    build_command.add_argument("--work", type=Path, required=True)
    build_command.add_argument("--review", type=Path, required=True)
    build_command.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            manifest = prepare(args.question_pdf, args.work)
            print(f'Prepared {len(manifest["cards"])} {manifest["paper"]} cards in {args.work}')
            print("Review manifest.json, the small context files, and answer_key.txt before completing review.example.json.")
        else:
            count = build(args.work, args.review, args.root)
            print(f"Built {count} reviewed cards")
    except (ValueError, FileExistsError, FileNotFoundError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
