from __future__ import annotations

import base64
import html
import re
from pathlib import Path

import streamlit as st

try:
    from PyPDF2 import PdfReader
except Exception:  # pragma: no cover
    PdfReader = None


WORKSPACE_ROOT = Path(__file__).resolve().parent
TEXT_SUFFIXES = {".md", ".txt", ".pdf"}
PREVIEWABLE_SUFFIXES = TEXT_SUFFIXES | {".png", ".jpg", ".jpeg", ".gif", ".webp"}
OTHER_VISIBLE_SUFFIXES = {".xlsx", ".xls", ".docx", ".doc"}
IGNORE_DIRS = {".git", ".streamlit", "__pycache__"}
PAGES = ["Library", "Search"]

SECTION_SPECS = [
    {"id": "prep", "label": "Assessment prep", "path": "Things to prepare/OECD_written_assessment_prep"},
    {"id": "llm", "label": "LLM research", "path": "Things to prepare/General LLM Research"},
    {"id": "tone", "label": "OECD tone", "path": "Research/OECD Tone Of Voice"},
    {"id": "comms", "label": "OECD communications", "path": "Research/OECD Official Communications"},
    {"id": "ai_oecd", "label": "OECD AI", "path": "Research/AI in the OECD"},
    {"id": "resources", "label": "Resources", "path": "Research/Resoruces"},
    {"id": "cases", "label": "Practice case", "path": "Assesment/Example of a case"},
    {"id": "instructions", "label": "Instructions", "path": "Assesment/Assesment instructions"},
]


def app_css() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 1500px;
            padding-top: 1rem;
            padding-bottom: 1.5rem;
        }
        .app-title {
            font-size: 2rem;
            font-weight: 760;
            letter-spacing: -0.04em;
            line-height: 1;
            margin-bottom: 0.2rem;
            color: #0f172a;
        }
        .app-subtitle {
            font-size: 0.88rem;
            color: #64748b;
            margin-bottom: 0.7rem;
        }
        .doc-card {
            border: 1px solid rgba(15, 23, 42, 0.08);
            background: #fff;
            border-radius: 18px;
            padding: 0.95rem 1rem 0.75rem;
            box-shadow: 0 12px 28px rgba(15, 23, 42, 0.04);
        }
        .doc-meta {
            color: #64748b;
            font-size: 0.82rem;
            margin-bottom: 0.2rem;
        }
        .doc-title {
            color: #0f172a;
            font-size: 1.08rem;
            font-weight: 740;
            margin-bottom: 0.1rem;
        }
        .small-note {
            color: #64748b;
            font-size: 0.82rem;
        }
        .search-hit {
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 16px;
            padding: 0.9rem 1rem;
            margin-bottom: 0.75rem;
            background: #fff;
        }
        .search-path {
            color: #64748b;
            font-size: 0.78rem;
            margin-bottom: 0.25rem;
        }
        .search-snippet {
            color: #0f172a;
            font-size: 0.92rem;
            line-height: 1.5;
        }
        .tree-wrap {
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 18px;
            padding: 0.8rem 0.8rem 0.4rem;
            background: #fff;
            box-shadow: 0 12px 28px rgba(15, 23, 42, 0.04);
        }
        .stButton > button, .stDownloadButton > button {
            border-radius: 10px;
            font-weight: 650;
        }
        .stExpander {
            border: 0 !important;
        }
        .stExpander > details {
            border: 1px solid rgba(15, 23, 42, 0.08) !important;
            border-radius: 12px !important;
            background: #fbfdff !important;
        }
        mark {
            background: #fff3bf;
            padding: 0.03rem 0.16rem;
            border-radius: 0.12rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def available_sections() -> list[dict]:
    sections = []
    for spec in SECTION_SPECS:
        absolute = WORKSPACE_ROOT / spec["path"]
        if absolute.exists():
            sections.append({**spec, "absolute_path": absolute})
    return sections


def is_visible(relative_path: Path) -> bool:
    return not any(part.startswith(".") or part in IGNORE_DIRS for part in relative_path.parts)


def is_supported_file(path: Path) -> bool:
    suffix = path.suffix.lower()
    return suffix in PREVIEWABLE_SUFFIXES or suffix in OTHER_VISIBLE_SUFFIXES


def is_inside(path: Path, root: Path) -> bool:
    return root == path or root in path.parents


def ensure_state(sections: list[dict]) -> None:
    first_section = sections[0]
    st.session_state.setdefault("page", "Library")
    st.session_state.setdefault("active_section", first_section["id"])
    st.session_state.setdefault("selected_file", None)
    st.session_state.setdefault("recent_files", [])
    st.session_state.setdefault("search_scope", "Current section")
    active_ids = {section["id"] for section in sections}
    if st.session_state["active_section"] not in active_ids:
        st.session_state["active_section"] = first_section["id"]

    selected_file = st.session_state.get("selected_file")
    if selected_file and not Path(selected_file).exists():
        st.session_state["selected_file"] = None


def section_by_id(sections: list[dict], section_id: str) -> dict:
    for section in sections:
        if section["id"] == section_id:
            return section
    return sections[0]


def section_for_path(sections: list[dict], path: Path) -> dict | None:
    for section in sections:
        if is_inside(path, section["absolute_path"]):
            return section
    return None


def set_selected_file(path: Path) -> None:
    st.session_state["selected_file"] = str(path)
    recent = st.session_state.get("recent_files", [])
    rel = str(path.relative_to(WORKSPACE_ROOT))
    recent = [item for item in recent if item != rel]
    recent.insert(0, rel)
    st.session_state["recent_files"] = recent[:10]


def breadcrumb(path: Path) -> str:
    return " / ".join(path.relative_to(WORKSPACE_ROOT).parts)


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_pdf_text(path: Path) -> str:
    if PdfReader is None:
        return ""
    try:
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception:
        return ""


def load_searchable_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        return read_text_file(path)
    if suffix == ".pdf":
        return extract_pdf_text(path)
    return ""


def format_size(size: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    current = float(size)
    for unit in units:
        if current < 1024 or unit == units[-1]:
            return f"{current:.0f} {unit}" if unit == "B" else f"{current:.1f} {unit}"
        current /= 1024
    return f"{size} B"


def file_children(folder: Path) -> tuple[list[Path], list[Path]]:
    dirs: list[Path] = []
    files: list[Path] = []
    for child in sorted(folder.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower())):
        relative = child.relative_to(WORKSPACE_ROOT)
        if not is_visible(relative):
            continue
        if child.is_dir():
            dirs.append(child)
        elif child.is_file() and is_supported_file(child):
            files.append(child)
    return dirs, files


def node_matches_filter(path: Path, query: str) -> bool:
    if not query.strip():
        return True
    q = query.lower()
    if q in path.name.lower():
        return True
    if path.is_dir():
        for child in path.iterdir():
            relative = child.relative_to(WORKSPACE_ROOT)
            if not is_visible(relative):
                continue
            if child.is_dir() or (child.is_file() and is_supported_file(child)):
                if node_matches_filter(child, query):
                    return True
    return False


def should_expand(folder: Path, selected: Path | None, query: str, depth: int) -> bool:
    if query.strip():
        return True
    if selected and (folder == selected.parent or folder in selected.parents):
        return True
    return depth == 0


def render_tree(folder: Path, selected: Path | None, query: str, depth: int = 0) -> None:
    dirs, files = file_children(folder)
    dirs = [item for item in dirs if node_matches_filter(item, query)]
    files = [item for item in files if node_matches_filter(item, query)]

    for directory in dirs:
        expanded = should_expand(directory, selected, query, depth)
        with st.expander(f"📁 {directory.name}", expanded=expanded):
            render_tree(directory, selected, query, depth + 1)

    for file_path in files:
        label = file_path.name
        if st.button(label, key=f"file-{file_path}", use_container_width=True):
            set_selected_file(file_path)
            st.rerun()


def render_sidebar(sections: list[dict]) -> dict:
    st.sidebar.markdown("## Library")
    page = st.sidebar.radio("Mode", PAGES, index=PAGES.index(st.session_state["page"]))
    st.session_state["page"] = page

    labels = {section["label"]: section["id"] for section in sections}
    current_section = section_by_id(sections, st.session_state["active_section"])
    chosen_label = st.sidebar.selectbox(
        "Section",
        list(labels.keys()),
        index=list(labels.keys()).index(current_section["label"]),
    )
    chosen_id = labels[chosen_label]
    if chosen_id != st.session_state["active_section"]:
        st.session_state["active_section"] = chosen_id
        st.rerun()

    st.sidebar.divider()
    st.sidebar.caption("Recent")
    recent = st.session_state.get("recent_files", [])
    if not recent:
        st.sidebar.caption("None")
    else:
        for rel_path in recent:
            path = WORKSPACE_ROOT / rel_path
            if not path.exists():
                continue
            if st.sidebar.button(path.name, key=f"recent-{rel_path}", use_container_width=True):
                section = section_for_path(sections, path.parent)
                if section:
                    st.session_state["active_section"] = section["id"]
                set_selected_file(path)
                st.session_state["page"] = "Library"
                st.rerun()

    return section_by_id(sections, st.session_state["active_section"])


def file_download(path: Path) -> None:
    st.download_button(
        "Download",
        data=path.read_bytes(),
        file_name=path.name,
        use_container_width=True,
    )


def pdf_viewer(path: Path) -> None:
    key = f"show-pdf-{path}"
    show = st.checkbox("Show PDF", key=key, value=st.session_state.get(key, False))
    if not show:
        st.caption("PDF off")
        return
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    src = f"data:application/pdf;base64,{encoded}"
    st.components.v1.html(
        f'<iframe src="{src}" width="100%" height="920" style="border:none;border-radius:14px;"></iframe>',
        height=940,
    )


def image_viewer(path: Path) -> None:
    st.image(str(path), use_container_width=True)


def render_preview(path: Path | None) -> None:
    if not path:
        st.markdown(
            """
            <div class="doc-card">
                <div class="doc-title">Select a document</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    suffix = path.suffix.lower()
    st.markdown(
        f"""
        <div class="doc-card">
            <div class="doc-meta">{html.escape(breadcrumb(path))}</div>
            <div class="doc-title">{html.escape(path.name)}</div>
            <div class="small-note">{suffix.lstrip('.').upper()} · {format_size(path.stat().st_size)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns([1, 6])
    with cols[0]:
        file_download(path)
    with cols[1]:
        st.write("")
    st.write("")

    if suffix == ".md":
        st.markdown(read_text_file(path))
    elif suffix == ".txt":
        st.text(read_text_file(path))
    elif suffix == ".pdf":
        pdf_viewer(path)
    elif suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
        image_viewer(path)
    else:
        st.info("Preview unavailable")


def render_library(section: dict) -> None:
    selected_file = Path(st.session_state["selected_file"]) if st.session_state.get("selected_file") else None

    st.markdown('<div class="app-title">Library</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="app-subtitle">{html.escape(section["label"])}</div>',
        unsafe_allow_html=True,
    )

    tree_col, preview_col = st.columns([1.05, 1.95], gap="large")

    with tree_col:
        filter_text = st.text_input("Filter", placeholder="Folder or file")
        st.markdown('<div class="tree-wrap">', unsafe_allow_html=True)
        render_tree(section["absolute_path"], selected_file, filter_text)
        st.markdown("</div>", unsafe_allow_html=True)

    with preview_col:
        render_preview(selected_file)


def snippet_for_query(text: str, terms: list[str], radius: int = 170) -> str:
    lowered = text.lower()
    positions = [lowered.find(term.lower()) for term in terms if lowered.find(term.lower()) != -1]
    if not positions:
        compact = text.strip().replace("\n", " ")
        return compact[: radius * 2] + ("..." if len(compact) > radius * 2 else "")
    start = max(min(positions) - radius, 0)
    end = min(start + radius * 2, len(text))
    snippet = text[start:end].replace("\n", " ")
    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet += "..."
    return snippet


def highlight_terms(text: str, terms: list[str]) -> str:
    if not terms:
        return html.escape(text)
    pattern = re.compile("(" + "|".join(re.escape(term) for term in terms if term) + ")", re.IGNORECASE)
    escaped = html.escape(text)
    return pattern.sub(lambda match: f"<mark>{html.escape(match.group(0))}</mark>", escaped)


def iter_searchable_files(roots: list[Path]):
    for root in roots:
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(WORKSPACE_ROOT)
            if not is_visible(relative):
                continue
            if path.suffix.lower() in TEXT_SUFFIXES:
                yield path


def search_documents(query: str, roots: list[Path], status_slot) -> list[dict]:
    terms = [term.strip() for term in re.split(r"\s+", query) if term.strip()]
    if not terms:
        return []

    results: list[dict] = []
    scanned = 0
    for path in iter_searchable_files(roots):
        scanned += 1
        if scanned == 1 or scanned % 10 == 0:
            status_slot.caption(f"Scanning {scanned} docs...")
        text = load_searchable_text(path)
        haystack = f"{path.name}\n{text}".lower()
        if all(term.lower() in haystack for term in terms):
            results.append(
                {
                    "path": str(path),
                    "relative_path": str(path.relative_to(WORKSPACE_ROOT)),
                    "snippet": snippet_for_query(text, terms),
                    "kind": path.suffix.lower().lstrip("."),
                }
            )
    status_slot.empty()
    return results


def render_search(section: dict, sections: list[dict]) -> None:
    st.markdown('<div class="app-title">Search</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Runs on submit.</div>', unsafe_allow_html=True)

    scope = st.radio(
        "Scope",
        options=["Current section", "All sections"],
        index=0 if st.session_state.get("search_scope", "Current section") == "Current section" else 1,
        horizontal=True,
    )
    st.session_state["search_scope"] = scope
    roots = [section["absolute_path"]] if scope == "Current section" else [item["absolute_path"] for item in sections]

    with st.form("search-form", clear_on_submit=False):
        query = st.text_input("Keywords", placeholder="AI visibility, bot traffic, OECD tone...")
        submitted = st.form_submit_button("Search", use_container_width=True)

    if not submitted or not query.strip():
        return

    status_slot = st.empty()
    results = search_documents(query, roots, status_slot)
    st.caption(f"{len(results)} result(s)")
    if not results:
        st.warning("No matches")
        return

    terms = [term.strip() for term in re.split(r"\s+", query) if term.strip()]
    for idx, result in enumerate(results[:250]):
        path = Path(result["path"])
        st.markdown(
            f"""
            <div class="search-hit">
                <div class="search-path">{html.escape(result["relative_path"])}</div>
                <div class="doc-title">{html.escape(path.name)}</div>
                <div class="search-snippet">{highlight_terms(result["snippet"], terms)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open", key=f"open-search-{idx}", use_container_width=True):
            section_match = section_for_path(sections, path.parent)
            if section_match:
                st.session_state["active_section"] = section_match["id"]
            set_selected_file(path)
            st.session_state["page"] = "Library"
            st.rerun()


def main() -> None:
    st.set_page_config(page_title="OECD Assessment Desk", page_icon="📚", layout="wide")
    app_css()

    sections = available_sections()
    if not sections:
        st.error("No study sections found.")
        return

    ensure_state(sections)
    active_section = render_sidebar(sections)

    if st.session_state["page"] == "Search":
        render_search(active_section, sections)
    else:
        render_library(active_section)


if __name__ == "__main__":
    main()
