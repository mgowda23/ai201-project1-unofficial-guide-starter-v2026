"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def _body_under_title(part: str) -> bool:
    """True if there is real text under the `# title`, not just the title."""
    lines = part.split("\n", 1)
    if not lines[0].startswith("# "):
        return True          # no title line at all, so it's all body
    return len(lines) > 1 and bool(lines[1].strip())


def split_on_paragraphs(body: str, limit: int) -> list[str]:
    """
    Break a section that came out longer than `limit` on its blank lines.

    Nothing in city_guides reaches this — the longest `##` section is 711
    characters against a limit of 800 — but a section is only a good chunk
    while sections stay short, and I would rather this fall back to paragraphs
    than hand back one enormous chunk if that ever stops being true.
    """
    pieces: list[str] = []
    current = ""

    for paragraph in body.split("\n\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        joined = f"{current}\n\n{paragraph}" if current else paragraph
        if current and len(joined) > limit:
            pieces.append(current)
            current = paragraph
        else:
            current = joined

    if current:
        pieces.append(current)
    return pieces


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    One `##` section, one chunk.

    The fourteen city_guides documents are already divided into topics by the
    person who wrote them: nine of them share the same seven-section template
    and the other five are thematic guides with four or five sections, 84
    sections in all. The baseline ignores that and cuts every 800 characters,
    and since the longest section in the corpus is 711 characters there was
    never a cut that could land *between* two sections — every one landed
    inside one. See the README for what that cost.

    The text above the first `##` is kept as its own chunk where there is any.
    Ten documents open with a real intro paragraph of 123 to 250 characters;
    the other four have nothing above the first heading but the title line, and
    those produce no extra chunk.

    No overlap, on purpose — see `config.CHUNK_OVERLAP`.
    """
    limit = config.CHUNK_SIZE
    chunks: list[Chunk] = []

    for doc in documents:
        # Every chunk carries the document's `# title`. The sections don't
        # repeat the town name — `## Where to stay` in guide_corry_vale.md
        # talks about "the entire valley" and never says "Corry Vale" — so
        # without this a section about a town can't be found by its name.
        title = doc.text.lstrip().split("\n", 1)[0].strip()
        if not title.startswith("# "):
            title = ""

        # A lookahead, so the heading stays attached to the section it labels.
        # Anchored to line starts, so "##" inside a sentence doesn't split.
        sections: list[str] = []
        for part in re.split(r"(?m)^(?=## )", doc.text):
            part = part.strip()
            if not part:
                continue
            # The bit above the first `## ` is the only part that can turn out
            # to be a heading with nothing under it. Four documents open
            # straight onto their first section, and "# Walking in the region"
            # on its own is a 23-character chunk that answers no question.
            if not part.startswith("## ") and not _body_under_title(part):
                continue
            if len(part) > limit:
                sections.extend(split_on_paragraphs(part, limit))
            else:
                sections.append(part)

        for index, section in enumerate(sections):
            # The intro chunk already opens with the title; don't repeat it.
            text = section if section.startswith("# ") else f"{title}\n\n{section}"
            chunks.append(
                Chunk(
                    text=text.strip(),
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
