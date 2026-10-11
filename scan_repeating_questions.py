"""Scan local PhilNITS AM/Subject A PDFs and build an offline repeat report."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
from difflib import SequenceMatcher
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata
import webbrowser

import pymupdf

ROOT = Path(__file__).resolve().parent
PDF_NAME = re.compile(r"^(\d{4})(S|A|Apr|Oct|May)_FE[_-](AM|A)_Questions?$", re.I)
HEADING = re.compile(r"^Q(\d{1,2})\.?(?:\s|$)", re.I)
CHOICE = re.compile(r"(?m)^\s*([a-d])\)\s*")
STOP = set("which of the following is a an in to for and or that this when what how be as by with from on are it at can used represents here each has have correct most".split())
TRANSLATION = str.maketrans({"−": "-", "–": "-", "—": "-", "‘": "'", "’": "'", "“": '"', "”": '"', "\u00ad": "", "\u00a0": " "})


@lru_cache(maxsize=20000)
def normalize(text: str) -> str:
    # NFC preserves superscripts/subscripts; NFKC would erase mathematical distinctions.
    text = unicodedata.normalize("NFC", text).translate(TRANSLATION)
    text = re.sub(r"(?<=\w)-\s*\n\s*(?=[a-z])", "", text)
    return " ".join(text.split()).casefold()


def split_question(text: str) -> tuple[str, list[str]]:
    text = re.sub(r"^\s*Q\d+\.?\s*", "", text, flags=re.I)
    markers = list(CHOICE.finditer(text))
    if [m[1].lower() for m in markers] != list("abcd"):
        return text.strip(), []
    return text[:markers[0].start()].strip(), [
        text[m.end():markers[i + 1].start() if i < 3 else len(text)].strip()
        for i, m in enumerate(markers)
    ]


def boundaries(doc, paper: str) -> dict[int, tuple[int, float]]:
    """Require a complete, spatially ordered sequence; ignore circuit labels like Q2."""
    candidates = defaultdict(list)
    for page_no, page in enumerate(doc):
        lines = []
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                text = "".join(span["text"] for span in line["spans"]).strip()
                lines.append((line["bbox"][1], line["bbox"][0], text))
        for y, x, text in sorted(lines):
            match = HEADING.match(text)
            if match and x < page.rect.width * .35 and not re.match(r"^[-–—,]", text[match.end():].lstrip()):
                candidates[int(match[1])].append((page_no, max(45, y - 4)))
    expected = 80 if paper == "AM" else 60
    if sorted(candidates) != list(range(1, expected + 1)):
        raise ValueError(f"Expected Q1–Q{expected}; missing {sorted(set(range(1, expected + 1)) - candidates.keys())}; unexpected {sorted(candidates.keys() - set(range(1, expected + 1)))}")
    # All candidates for Q1 must precede real Q2. The last Q1 is the actual exam,
    # whereas the earlier Q1 may be the instruction-page sample.
    selected = {}
    for q in range(1, expected + 1):
        previous = selected.get(q - 1, (-1, 0))
        next_candidates = candidates.get(q + 1)
        upper = min((p for p in next_candidates if p > previous), default=(len(doc), 0)) if next_candidates else (len(doc), 0)
        valid = [pos for pos in candidates[q] if previous < pos < upper]
        if q == 1 and valid:
            selected[q] = valid[-1]
        elif len(valid) == 1:
            selected[q] = valid[0]
        else:
            raise ValueError(f"Ambiguous Q{q} boundary: {valid}")
    return selected


def segments(doc, start, end):
    for page_no in range(start[0], end[0] + 1):
        page = doc[page_no]
        top = start[1] if page_no == start[0] else 45
        bottom = end[1] if page_no == end[0] else page.rect.height - 30
        if bottom > top + 12:
            yield page_no, page, pymupdf.Rect(0, top, page.rect.width, bottom)


def read_question(doc, start, end):
    parts, reasons = [], set()
    for _, page, clip in segments(doc, start, end):
        parts.append(page.get_text(clip=clip))
        if any(clip.intersects(pymupdf.Rect(image["bbox"])) for image in page.get_image_info()):
            reasons.add("Embedded image")
        if any(clip.intersects(d["rect"] + (-1, -1, 1, 1)) and (d["rect"].width > 10 or d["rect"].height > 10) for d in page.get_drawings()):
            reasons.add("Vector diagram or table")
        # Plain PDF text does not preserve the position of superscripts/subscripts.
        spans = [s for b in page.get_text("dict", clip=clip)["blocks"] for line in b.get("lines", []) for s in line["spans"]]
        if any(s.get("flags", 0) & 1 for s in spans):
            reasons.add("Positioned mathematical text")
    text = "\n".join(parts).strip()
    stem, choices = split_question(text)
    if len(normalize(stem)) < 35 or len(choices) != 4 or any(not c for c in choices):
        reasons.add("Insufficient text or incomplete choices")
    if "\ufffd" in text or "\x00" in text:
        reasons.add("Unreadable PDF characters")
    if re.search(r"\b(diagram|table|figure|graph|chart|shown (below|above))\b", stem, re.I):
        reasons.add("Visual content referenced")
    return stem, choices, sorted(reasons)


def question_key(q):
    return normalize(q["stem"]), tuple(sorted(normalize(c) for c in q["choices"]))


@lru_cache(maxsize=8000)
def informative(text):
    return frozenset(t for t in re.findall(r"[\w]+", normalize(text)) if len(t) > 1 and t not in STOP)


@lru_cache(maxsize=8000)
def variant_text(text):
    return re.sub(r"\b(?:\d+(?:\.\d+)?|[a-z])\b", "VALUE", normalize(text))


def similarity(a, b, threshold=.8):
    sa, sb = normalize(a["stem"]), normalize(b["stem"])
    ta, tb = informative(sa), informative(sb)
    if len(ta & tb) < 3 or not ta or not tb or min(len(sa), len(sb)) / max(len(sa), len(sb)) < .55:
        return 0.0
    dice = 2 * len(ta & tb) / (len(ta) + len(tb))
    if dice < .45:
        return 0.0
    matchers = [SequenceMatcher(None, sa, sb, autojunk=False),
                SequenceMatcher(None, variant_text(sa), variant_text(sb), autojunk=False)]
    # quick_ratio is an upper bound, so this skips expensive comparisons without
    # discarding any pair that could meet the requested threshold.
    if .9 * (.7 * max(m.quick_ratio() for m in matchers) + .3 * dice) + .1 < threshold:
        return 0.0
    character = max(m.ratio() for m in matchers)
    stem_score = .7 * character + .3 * dice
    ca = " | ".join(sorted(normalize(c) for c in a["choices"]))
    cb = " | ".join(sorted(normalize(c) for c in b["choices"]))
    choice_score = SequenceMatcher(None, ca, cb, autojunk=False).ratio() if ca and cb else 0
    return .9 * stem_score + .1 * choice_score


def match_questions(questions, threshold=.8):
    exact_index = defaultdict(list)
    for i, q in enumerate(questions):
        if not q["review_reasons"]:
            exact_index[question_key(q)].append(i)
    exact, near, visual = [], [], []
    for ids in exact_index.values():
        if len({questions[i]["paper_id"] for i in ids}) > 1:
            exact.append({"kind": "exact", "ids": ids, "score": 1.0})
    # Use informative-token postings, omitting corpus-wide boilerplate tokens.
    postings = defaultdict(list)
    tokens = [informative(q["stem"]) for q in questions]
    for i, terms in enumerate(tokens):
        for term in terms:
            postings[term].append(i)
    for i, q in enumerate(questions):
        shared = Counter()
        for term in tokens[i]:
            if len(postings[term]) <= max(20, len(questions) * .15):
                shared.update(j for j in postings[term] if j > i)
        for j, overlap in shared.items():
            other = questions[j]
            if overlap < 2 or q["paper_id"] == other["paper_id"]:
                continue
            unverified = bool(q["review_reasons"] or other["review_reasons"])
            if not unverified and question_key(q) == question_key(other):
                continue
            score = similarity(q, other, threshold)
            if score >= threshold:
                item = {"kind": "visual" if unverified else "strong" if score >= .9 else "moderate", "ids": [i, j], "score": round(score, 4)}
                changes = []
                if normalize(q["stem"]) != normalize(other["stem"]):
                    changes.append("Wording or example changed")
                    values = lambda s: re.findall(r"\b(?:\d+(?:\.\d+)?|[a-z])\b", normalize(s))
                    if values(q["stem"]) != values(other["stem"]):
                        changes.append("Numbers or variable tokens changed")
                if question_key(q)[1] != question_key(other)[1]:
                    changes.append("Answer choices changed")
                item["changes"] = changes
                (visual if unverified else near).append(item)
    def frequency(item):
        return len({questions[i]["paper_id"] for i in item["ids"]})
    exact.sort(key=lambda r: (-frequency(r), -max(questions[i]["year"] for i in r["ids"])))
    near.sort(key=lambda r: (-r["score"], -frequency(r), -max(questions[i]["year"] for i in r["ids"])))
    visual.sort(key=lambda r: -r["score"])
    return exact + near + visual


def parse_years(value):
    if value is None:
        return None
    result = set()
    for part in value.split(","):
        match = re.fullmatch(r"(\d{4})(?:-(\d{4}))?", part.strip())
        if not match:
            raise argparse.ArgumentTypeError("Use years such as 2015-2026 or 2007,2010,2026")
        first, last = int(match[1]), int(match[2] or match[1])
        if first > last or not 1900 <= first <= last <= 2100:
            raise argparse.ArgumentTypeError("Year range must be ascending and between 1900 and 2100")
        result.update(range(first, last + 1))
    return result


def note_for(root, year, season, paper, number):
    names = [f"{year}{season}_FE_{paper}_{number}.md", f"{year}{season}_FE-{paper}_{number}.md"]
    if paper == "AM":
        names.append(f"{year}{season}_FE_{number}.md")
    return next((p.resolve().as_uri() for name in names if (p := root / str(year) / name).is_file()), None)


def scan(root, output, years=None, papers=None):
    questions, coverage, failures, notices = [], [], [], []
    sources = root / "Exam_Q&A"
    if not sources.is_dir():
        raise ValueError(f"Missing source directory: {sources}")
    for pdf in sorted(sources.rglob("*.pdf")):
        match = PDF_NAME.fullmatch(pdf.stem)
        if not match:
            if "question" in pdf.stem.lower() and re.search(r"FE[_-](?:AM|A)_", pdf.stem, re.I):
                failures.append({"source": str(pdf.relative_to(root)), "error": "Unrecognized paper filename"})
            continue
        year, season, paper = match.groups()
        year, paper = int(year), paper.upper()
        season = {"apr": "S", "may": "S", "oct": "A"}.get(season.lower(), season.upper())
        if (years is not None and year not in years) or (papers and paper not in papers):
            continue
        paper_id = f"{year}{season}_{paper}"
        entry = {"id": paper_id, "year": year, "session": pdf.parent.name, "paper": paper, "source": str(pdf.relative_to(root)), "questions": 0}
        coverage.append(entry)
        try:
            with pymupdf.open(pdf) as doc:
                bounds = boundaries(doc, paper)
                pending = []
                for number, start in bounds.items():
                    end = bounds.get(number + 1, (len(doc) - 1, doc[-1].rect.height - 30))
                    stem, choices, reasons = read_question(doc, start, end)
                    pending.append({"id": f"{paper_id}_Q{number}", "paper_id": paper_id, "year": year, "session": entry["session"], "paper": paper, "number": number, "stem": stem, "choices": choices, "review_reasons": reasons, "source": pdf.resolve().as_uri(), "page": start[0] + 1, "note": note_for(root, year, season, paper, number), "previews": [], "_bounds": (start, end), "_pdf": str(pdf)})
                questions.extend(pending)
                entry["questions"] = len(pending)
        except Exception as exc:
            failures.append({"source": entry["source"], "error": str(exc)})
    represented = {(c["year"], c["session"].lower()) for c in coverage}
    year_set = years if years is not None else {c["year"] for c in coverage}
    latest = max((c["year"], c["session"].lower() == "october") for c in coverage) if coverage else (0, False)
    for year in sorted(year_set):
        for session in ("April", "October"):
            # May replaces April in 2015. Do not invent a future autumn paper.
            present = (year, session.lower()) in represented or (session == "April" and (year, "may") in represented)
            if not present and (years is not None or (year, session == "October") <= latest):
                notices.append(f"No selected question PDF for {year} {session}; availability is not verified.")
    return questions, coverage, failures, notices


def write_report(output, questions, results, coverage, failures, notices, threshold):
    output.mkdir(parents=True, exist_ok=True)
    previews = output / "previews"
    previews.mkdir(exist_ok=True)
    required = {i for r in results for i in r["ids"]} | {i for i, q in enumerate(questions) if q["review_reasons"]}
    by_pdf = defaultdict(list)
    for i in required:
        by_pdf[questions[i]["_pdf"]].append(i)
    for pdf, ids in by_pdf.items():
        with pymupdf.open(pdf) as doc:
            digest = hashlib.sha256(Path(pdf).read_bytes()).hexdigest()[:10]
            for i in ids:
                q = questions[i]
                crop_digest = hashlib.sha256(repr(q["_bounds"]).encode()).hexdigest()[:8]
                for page_no, page, clip in segments(doc, *q["_bounds"]):
                    name = f"{q['id']}_{digest}_{crop_digest}_{page_no + 1}.png"
                    target = previews / name
                    if not target.exists():
                        page.get_pixmap(matrix=pymupdf.Matrix(1.25, 1.25), clip=clip, alpha=False).save(target)
                    q["previews"].append("previews/" + name)
    for q in questions:
        q.pop("_pdf")
        q.pop("_bounds")
    data = {"schema": 1, "generated_at": datetime.now(timezone.utc).isoformat(), "minimum_similarity": threshold, "questions": questions, "results": results, "coverage": coverage, "failures": failures, "notices": notices}
    encoded = json.dumps(data, ensure_ascii=False)
    (output / "results.json").write_text(encoded, encoding="utf-8")
    safe = encoded.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    template = (ROOT / "repeat_questions_report.html").read_text(encoding="utf-8")
    (output / "index.html").write_text(template.replace("__REPORT_DATA__", safe), encoding="utf-8")
    return data


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--years", type=parse_years)
    parser.add_argument("--papers", nargs="+", choices=["AM", "A"], default=["AM", "A"])
    parser.add_argument("--min-similarity", type=float, default=.8)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--open", action="store_true")
    args = parser.parse_args(argv)
    if not .8 <= args.min_similarity <= 1:
        parser.error("--min-similarity must be between 0.8 and 1")
    root = args.root.resolve()
    output = (args.output or root / "reports" / "repeating-questions").resolve()
    # Generated output cannot be an exam/note directory or overwrite a source.
    if output == root or any(output == root / n or root / n in output.parents for n in ["Exam_Q&A", "Files", *[str(y) for y in range(1900, 2101)]]):
        parser.error("Choose a separate report directory, outside source PDFs, images, and year notes")
    try:
        print("Reading exam PDFs...", flush=True)
        questions, coverage, failures, notices = scan(root, output, args.years, args.papers)
        print(f"Read {len(questions)} questions from {len(coverage)} papers; {len(failures)} extraction failures. Comparing...", flush=True)
        results = match_questions(questions, args.min_similarity)
        print("Writing report and source previews...", flush=True)
        write_report(output, questions, results, coverage, failures, notices, args.min_similarity)
    except (ValueError, OSError) as exc:
        print(f"Scan failed: {exc}", file=sys.stderr)
        return 1
    counts = Counter(r["kind"] for r in results)
    print(f"Exact groups: {counts['exact']}; strong pairs: {counts['strong']}; moderate pairs: {counts['moderate']}; visual pairs: {counts['visual']}")
    print(f"Questions needing review: {sum(bool(q['review_reasons']) for q in questions)}")
    print(f"Report: {output / 'index.html'}")
    if args.open:
        webbrowser.open((output / "index.html").as_uri())
    return 2 if failures or not questions else 0


if __name__ == "__main__":
    sys.exit(main())
