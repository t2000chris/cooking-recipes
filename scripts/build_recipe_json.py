#!/usr/bin/env python3
import re, json
from pathlib import Path

DOCS = Path("docs")                # MkDocs default
OUT  = DOCS / "api"

# Top-level categories (adjust if yours differ)
CATEGORIES = {"hongkong","japanese","korean","western","bakery"}

# ---- Chinese-aware parsing config ----
# We'll normalize headings by lowercasing and removing spaces/emoji.
INGR_HEAD_KWS = {
    # English
    "ingredients", "ingredient",
    # Chinese
    "材料","食材","配料","主料","辅料","調味","調味料","调味","调味料",
    "材料與調味","材料和調味","食材與調味","食材和調味"
}
METHOD_HEAD_KWS = {
    # English
    "method","methods","directions","instructions","steps","cookingmethod",
    # Chinese
    "做法","步驟","步骤","說明","说明","烹調","烹调","製作","制作","煮法","烹飪","烹饪"
}

BULLET_PREFIX_RE = re.compile(
    r"""^\s*(?:                 # common bullets / numbers (English + CJK)
        [\-\*\•\·\‧\—\–\─] |    # bullets/dashes
        [0-9０-９]+[.)、．] |     # 1. 1) １、 １．
        [①-⑳] |                 # circled numbers
        [一二三四五六七八九十]+[、.)．] |   # 一、 二. 十） etc.
        （[一二三四五六七八九十]） |        # （一）
        [A-Za-zＡ-Ｚａ-ｚ][.)、．]          # a) A．
    )\s*""",
    re.VERBOSE
)

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore")

def normalize_heading(s: str) -> str:
    # strip spaces and common emoji/symbols, lowercase
    s = re.sub(r"[\s\u200b\u200c\u200d\ufeff]", "", s)
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "", s)  # drop decorations but keep CJK/word chars
    return s.lower()

def find_section(txt: str, keywords: set[str]) -> str | None:
    matches = list(re.finditer(r"^\s*##\s+(.+)$", txt, re.M))
    for i, m in enumerate(matches):
        raw = m.group(1).strip()
        norm = normalize_heading(raw)
        if any(kw in norm for kw in keywords):  # substring match is deliberate
            start = m.end()
            end = matches[i+1].start() if i+1 < len(matches) else len(txt)
            return txt[start:end].strip()
    return None

def split_lines_listish(section: str | None, kind: str) -> list[str]:
    if not section:
        return []

    # Primary: split by lines and strip common bullet/number prefixes
    items = []
    for line in section.splitlines():
        s = line.strip()
        s = BULLET_PREFIX_RE.sub("", s)
        if s:
            items.append(s)

    # If user wrote a paragraph instead of bullets, do a smart fallback
    if len(items) <= 1:
        s = section.strip()
        if kind == "ingredients":
            # Chinese ingredients often separated by 、/，/； or commas
            parts = re.split(r"[、，,；;]\s*", s)
            parts = [p.strip(" ．。.;；,，、") for p in parts if p.strip()]
            if len(parts) > 1:
                items = parts
        else:  # method/instructions: split by 。/； or blank lines
            parts = re.split(r"(?:[。；;]\s*|\n{2,})", s)
            parts = [p.strip(" ．。;；") for p in parts if p and p.strip()]
            if len(parts) > 1:
                items = parts

    return items

def parse_tags(txt: str) -> list[str]:
    # Keep your existing English tag system if present
    fm = re.search(r"^---(.*?)---", txt, re.S | re.M)
    blob = fm.group(1) if fm else txt
    m = re.search(r"^tags:\s*\[(.*?)\]", blob, re.M)
    if m:
        return [t.strip().strip("'\"") for t in m.group(1).split(",") if t.strip()]
    return []

def h1_title(txt: str, fallback: str) -> str:
    m = re.search(r"^\s*#\s+(.+)", txt, re.M)
    return m.group(1).strip() if m else fallback

def process_file(md_path: Path, rel_under_docs: Path):
    raw = read_text(md_path)
    title = h1_title(raw, rel_under_docs.stem.replace("-", " ").title())

    ingr_sec   = find_section(raw, set(map(normalize_heading, INGR_HEAD_KWS)))
    method_sec = find_section(raw, set(map(normalize_heading, METHOD_HEAD_KWS)))

    ingredients = split_lines_listish(ingr_sec, "ingredients")
    method      = split_lines_listish(method_sec, "method")
    tags        = parse_tags(raw)

    slug = str(rel_under_docs.with_suffix("")).replace("\\", "/")  # mirrors deep folders
    folder = rel_under_docs.parts[0] if rel_under_docs.parts else ""

    data = {
        "title": title,
        "slug": slug,
        "folder": folder,
        "tags": tags,
        "ingredients": ingredients,
        "method": method
    }

    out_file = OUT / f"{slug}.json"     # docs/api/<deep/path>.json
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    return {"title": title, "slug": slug, "folder": folder, "tags": tags}

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    index = []
    for cat in CATEGORIES:
        root = DOCS / cat
        if not root.exists():
            continue
        for p in sorted(root.rglob("*.md")):
            if p.name.lower() in {"index.md", "readme.md"}:
                continue
            rel = p.relative_to(DOCS)
            index.append(process_file(p, rel))
    (OUT / "index.json").write_text(json.dumps({"recipes": index}, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
