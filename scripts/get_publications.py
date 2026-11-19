"""Fetch publications from Semantic Scholar into _data/publications_<author>.yml.

Script version of notebooks/get_publications.ipynb. By default it is incremental:
papers already present (matched by paper_id or title) are kept untouched, so manual
edits to the YAML files survive. New papers are prepended, newest first.

Semantic Scholar provides the paper list and metadata. Figures come from arXiv only:
the first figure of the paper's arXiv HTML version is saved to images/publications/.
Papers without an arXiv version (or without figures) are skipped.

Usage (from repo root):
    pip install requests python-slugify pyyaml
    python scripts/get_publications.py                  # all authors
    python scripts/get_publications.py flora hao        # selected authors
    python scripts/get_publications.py --dry-run        # list new papers only
    python scripts/get_publications.py --since 2026-01-01

Only papers dated on/after --since are added; the default is the newest date already
in each author's file. Use --all to consider every paper.

Set S2_API_KEY to use a Semantic Scholar API key (higher rate limits); without it
the public, rate-limited endpoint is used.
"""
import argparse
import os
import re
import sys
import time
from datetime import datetime
from urllib.parse import urljoin

import requests
import yaml
from slugify import slugify

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.semanticscholar.org/graph/v1"
FIELDS = "title,authors,venue,publicationDate,externalIds"

# Semantic Scholar author IDs (several per person due to split profiles).
AUTHORS = {
    "flora": ["2253483164", "144954586", "2142031887"],
    "aditya": ["145714972"],
    "hao": ["2253463704", "1560895396"],
    "benjamin": ["2575168", "2244619392", "2284688624"],
}

session = requests.Session()
if os.environ.get("S2_API_KEY"):
    session.headers["x-api-key"] = os.environ["S2_API_KEY"]


_last_api_call = 0.0


def get(url, params=None, retries=8):
    """GET with exponential backoff on rate limiting (API calls paced to ~1 req/s)."""
    global _last_api_call
    for attempt in range(retries):
        if url.startswith(API):
            time.sleep(max(0.0, 1.1 - (time.time() - _last_api_call)))
            _last_api_call = time.time()
        r = session.get(url, params=params, timeout=60)
        if r.status_code != 429:
            return r
        time.sleep(min(2 ** attempt, 60))
    return r


def get_papers(author_id):
    url = f"{API}/author/{author_id}/papers"
    params = {"fields": FIELDS, "offset": 0, "limit": 500}
    papers = []
    while True:
        r = get(url, params)
        if r.status_code != 200:
            raise RuntimeError(f"author {author_id}: HTTP {r.status_code} {r.text[:200]}")
        result = r.json()
        papers += result.get("data", [])
        if "next" not in result:
            return papers
        params["offset"] = result["next"]


ARXIV_IMG = re.compile(r'<img[^>]*\bsrc="([^"]+\.(?:png|jpe?g|gif))"[^>]*class="ltx_graphics', re.I)


def arxiv_first_figure(arxiv_id):
    """First figure from the arXiv HTML rendering of a paper, or None."""
    r = session.get(f"https://arxiv.org/html/{arxiv_id}", timeout=60, headers={"User-Agent": "Mozilla/5.0"})
    if r.status_code != 200:
        return None
    m = ARXIV_IMG.search(r.text)
    if not m:
        return None
    src = m.group(1)
    # src is usually "<id>v<n>/fig.png" (relative to /html/), sometimes relative to the page itself
    base = "https://arxiv.org/html/" if src.startswith(arxiv_id) else r.url.rstrip("/") + "/"
    img = session.get(urljoin(base, src), timeout=60, headers={"User-Agent": "Mozilla/5.0"})
    if img.status_code == 200 and img.headers.get("content-type", "").startswith("image"):
        return img.content
    return None


def get_image(title, arxiv_id=None, dry_run=False):
    rel = f"images/publications/{slugify(title)}.png"
    path = os.path.join(REPO, rel)
    if os.path.exists(path) or dry_run:
        return rel
    if not arxiv_id:
        raise ValueError("not on arXiv, no figure source")
    content = arxiv_first_figure(arxiv_id)
    if content is None:
        raise ValueError(f"no figure found in arXiv HTML for {arxiv_id}")
    with open(path, "wb") as f:
        f.write(content)
    return rel


def parse_paper(datum, dry_run=False):
    paper_id = datum["paperId"]
    ext = datum.get("externalIds") or {}

    venue = datum.get("venue") or ""
    if venue in ("", "arXiv.org"):
        if "ArXiv" in ext:
            venue = f"arXiv preprint arXiv:{ext['ArXiv']}"
        elif venue == "arXiv.org" and "DOI" in ext:
            arxiv_id = ext["DOI"].split("/")[-1].replace("arxiv.", "")
            venue = f"arXiv preprint arXiv:{arxiv_id}"
    if not venue:
        raise ValueError("no venue")

    if "DOI" in ext:
        url = f"https://doi.org/{ext['DOI']}"
    elif "ArXiv" in ext:
        url = f"https://arxiv.org/abs/{ext['ArXiv']}"
    elif "DBLP" in ext:
        url = f"https://dblp.org/rec/{ext['DBLP']}"
    else:
        raise ValueError("no URL in externalIds")

    if not datum.get("publicationDate"):
        raise ValueError("no publication date")

    return {
        "paper_id": paper_id,
        "title": datum["title"],
        "authors": ", ".join(a["name"] for a in datum["authors"]),
        "url": url,
        "venue": venue,
        "image_url": get_image(datum["title"], ext.get("ArXiv"), dry_run),
        "date": datetime.strptime(datum["publicationDate"], "%Y-%m-%d").date(),
    }


def update_author(author, author_ids, dry_run=False, since=None, all_dates=False):
    path = os.path.join(REPO, "_data", f"publications_{author}.yml")
    existing = []
    if os.path.exists(path):
        with open(path) as f:
            existing = yaml.safe_load(f) or []

    seen_ids = {p["paper_id"] for p in existing}
    seen_titles = {slugify(p["title"]) for p in existing}

    # Default cutoff: newest paper already in the file, so older papers that were
    # deliberately left out (e.g. no figure available) are not re-added.
    if since is None and existing and not all_dates:
        since = max(str(p["date"]) for p in existing)
    if all_dates:
        since = None
    print(f"{author}: papers since {since or 'any date'}")

    new = []
    for author_id in author_ids:
        for datum in get_papers(author_id):
            title_slug = slugify(datum.get("title") or "")
            if datum["paperId"] in seen_ids or title_slug in seen_titles:
                continue
            if since and (datum.get("publicationDate") or "") < since:
                continue
            try:
                paper = parse_paper(datum, dry_run)
            except Exception as e:
                print(f"  [{author}] skip {datum['paperId']} '{datum.get('title')}': {e}")
                continue
            new.append(paper)
            seen_ids.add(paper["paper_id"])
            seen_titles.add(title_slug)

    new.sort(key=lambda p: p["date"], reverse=True)
    print(f"{author}: {len(new)} new")
    for p in new:
        print(f"    {p['date']}  {p['title']}  [{p['venue']}]")

    if new and not dry_run:
        with open(path, "w") as f:
            yaml.dump(new + existing, f, allow_unicode=True, sort_keys=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("authors", nargs="*", help=f"authors to update: {', '.join(AUTHORS)} (default: all)")
    parser.add_argument("--dry-run", action="store_true", help="print new papers without writing files")
    parser.add_argument("--since", help="only add papers published on/after YYYY-MM-DD")
    parser.add_argument("--all", action="store_true", help="ignore dates and add every missing paper")
    args = parser.parse_args()
    unknown = set(args.authors) - set(AUTHORS)
    if unknown:
        parser.error(f"unknown author(s): {', '.join(sorted(unknown))}")

    for author in args.authors or AUTHORS:
        try:
            update_author(author, AUTHORS[author], args.dry_run, args.since, args.all)
        except RuntimeError as e:
            print(f"{author}: FAILED, {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
