from __future__ import annotations

import base64
import html
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import streamlit as st

try:
    from PyPDF2 import PdfReader
except Exception:  # pragma: no cover
    PdfReader = None


WORKSPACE_ROOT = Path(__file__).resolve().parent
DEFAULT_COLLECTIONS = [
    "Research",
    "Things to prepare",
    "Assesment",
    "OECD comunications to me",
    "Maki Plarform",
]
TEXT_SUFFIXES = {".md", ".txt", ".pdf"}
PREVIEWABLE_SUFFIXES = TEXT_SUFFIXES | {".png", ".jpg", ".jpeg", ".gif", ".webp"}
IGNORE_DIRS = {".git", ".streamlit", "__pycache__"}


@dataclass(frozen=True)
class DocEntry:
    path: str
    collection: str
    kind: str
    modified_ns: int
    size: int

    @property
    def rel_path(self) -> str:
        return str(Path(self.path).relative_to(WORKSPACE_ROOT))

    @property
    def name(self) -> str:
        return Path(self.path).name


def app_css() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }
        .app-title {
            font-size: 2.15rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            margin-bottom: 0.35rem;
        }
        .meta-row {
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin: 0.75rem 0 1rem 0;
        }
        .metric-chip {
            border: 1px solid rgba(15, 23, 42, 0.09);
            background: #f8fafc;
            color: #0f172a;
            border-radius: 999px;
            padding: 0.4rem 0.8rem;
            font-size: 0.9rem;
            font-weight: 600;
        }
        .browser-card {
            border: 1px solid rgba(15, 23, 42, 0.09);
            border-radius: 18px;
            padding: 1rem 1rem 0.4rem 1rem;
            background: #ffffff;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
        }
        .path-label {
            font-size: 0.82rem;
            color: #64748b;
            margin-bottom: 0.25rem;
        }
        .file-title {
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }
        .search-hit {
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 16px;
            padding: 0.9rem 1rem;
            margin-bottom: 0.75rem;
            background: #ffffff;
        }
        .search-path {
            color: #64748b;
            font-size: 0.8rem;
            margin-bottom: 0.35rem;
        }
        .search-snippet {
            color: #0f172a;
            font-size: 0.93rem;
            line-height: 1.55;
        }
        mark {
            background: #fff3bf;
            padding: 0.05rem 0.18rem;
            border-radius: 0.2rem;
        }
        .stButton > button {
            border-radius: 12px;
            font-weight: 600;
        }
        .folder-button button, .file-button button {
            width: 100%;
            text-align: left;
            justify-content: flex-start;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def existing_collections() -> list[Path]:
    return [WORKSPACE_ROOT / name for name in DEFAULT_COLLECTIONS if (WORKSPACE_ROOT / name).exists()]


def is_visible(path: Path) -> bool:
    return not any(part.startswith(".") or part in IGNORE_DIRS for part in path.parts)


@st.cache_data(show_spinner=False)
def collect_entries(collection_names: tuple[str, ...]) -> list[DocEntry]:
    entries: list[DocEntry] = []
    for name in collection_names:
        collection_root = WORKSPACE_ROOT / name
        if not collection_root.exists():
            continue
        for path in collection_root.rglob("*"):
            if not path.is_file():
                continue
            if not is_visible(path.relative_to(WORKSPACE_ROOT)):
                continue
            suffix = path.suffix.lower()
            if suffix not in PREVIEWABLE_SUFFIXES and suffix not in {".xlsx", ".xls", ".docx", ".doc"}:
                continue
            stat = path.stat()
            entries.append(
                DocEntry(
                    path=str(path),
                    collection=name,
                    kind=suffix.lstrip("."),
                    modified_ns=stat.st_mtime_ns,
                    size=stat.st_size,
                )
            )
    return sorted(entries, key=lambda item: item.rel_path.lower())


def entry_signature(entries: Iterable[DocEntry]) -> tuple[tuple[str, int, int], ...]:
    return tuple((entry.path, entry.modified_ns, entry.size) for entry in entries)


def read_markdown_or_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_pdf_text(path: Path) -> str:
    if PdfReader is None:
        return ""
    try:
        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)
    except Exception:
        return ""


@st.cache_data(show_spinner=False)
def build_search_index(signature: tuple[tuple[str, int, int], ...]) -> list[dict]:
    index: list[dict] = []
    for path_str, _, _ in signature:
        path = Path(path_str)
        suffix = path.suffix.lower()
        text = ""
        if suffix in {".md", ".txt"}:
            text = read_markdown_or_text(path)
        elif suffix == ".pdf":
            text = extract_pdf_text(path)
        if text.strip():
            index.append(
                {
                    "path": path_str,
                    "name": path.name,
                    "relative_path": str(path.relative_to(WORKSPACE_ROOT)),
                    "text": text,
                }
            )
    return index


def set_current_folder(path: Path) -> None:
    st.session_state["current_folder"] = str(path)
    st.session_state["selected_file"] = None


def set_selected_file(path: Path) -> None:
    st.session_state["selected_file"] = str(path)


def ensure_valid_state(collection_roots: list[Path]) -> None:
    if not collection_roots:
        return
    default_root = collection_roots[0]
    current_folder = Path(st.session_state.get("current_folder", default_root))
    if not current_folder.exists():
        st.session_state["current_folder"] = str(default_root)
    selected_file = st.session_state.get("selected_file")
    if selected_file and not Path(selected_file).exists():
        st.session_state["selected_file"] = None


def folder_children(folder: Path) -> tuple[list[Path], list[Path]]:
    children = [child for child in folder.iterdir() if is_visible(child.relative_to(WORKSPACE_ROOT))]
    dirs = sorted([child for child in children if child.is_dir()], key=lambda p: p.name.lower())
    files = sorted([child for child in children if child.is_file()], key=lambda p: p.name.lower())
    return dirs, files


def format_size(size: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    current = float(size)
    for unit in units:
        if current < 1024 or unit == units[-1]:
            return f"{current:.0f} {unit}" if unit == "B" else f"{current:.1f} {unit}"
        current /= 1024
    return f"{size} B"


def breadcrumb(path: Path) -> str:
    return " / ".join(path.relative_to(WORKSPACE_ROOT).parts)


def render_collection_switcher(collection_roots: list[Path]) -> list[str]:
    available = [root.name for root in collection_roots]
    default = st.session_state.get("active_collections", available)
    selected = st.sidebar.multiselect("Collections", available, default=default)
    if not selected:
        selected = available
    st.session_state["active_collections"] = selected
    return selected


def render_sidebar(collection_roots: list[Path]) -> list[str]:
    st.sidebar.markdown("## Explorer")
    selected = render_collection_switcher(collection_roots)
    st.sidebar.divider()
    st.sidebar.caption("Search covers Markdown, text and PDF content.")
    return selected


def open_parent(folder: Path) -> Path:
    relative = folder.relative_to(WORKSPACE_ROOT)
    parts = relative.parts
    if len(parts) <= 1:
        return folder
    return WORKSPACE_ROOT.joinpath(*parts[:-1])


def file_download(path: Path) -> None:
    st.download_button(
        "Download",
        data=path.read_bytes(),
        file_name=path.name,
        use_container_width=True,
    )


def pdf_viewer(path: Path) -> None:
    data = base64.b64encode(path.read_bytes()).decode("utf-8")
    src = f"data:application/pdf;base64,{data}"
    st.components.v1.html(
        f'<iframe src="{src}" width="100%" height="920" style="border:none;border-radius:12px;"></iframe>',
        height=940,
    )


def image_viewer(path: Path) -> None:
    st.image(str(path), use_container_width=True)


def render_file_preview(path: Path) -> None:
    suffix = path.suffix.lower()
    st.markdown(
        f"""
        <div class="browser-card">
            <div class="path-label">{html.escape(str(path.relative_to(WORKSPACE_ROOT)))}</div>
            <div class="file-title">{html.escape(path.name)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns([1, 6])
    with cols[0]:
        file_download(path)
    with cols[1]:
        st.caption(f"{suffix.lstrip('.').upper()} · {format_size(path.stat().st_size)}")
    st.divider()
    if suffix == ".md":
        st.markdown(read_markdown_or_text(path))
    elif suffix == ".txt":
        st.text(read_markdown_or_text(path))
    elif suffix == ".pdf":
        pdf_viewer(path)
    elif suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
        image_viewer(path)
    else:
        st.info("Preview is not available for this file type. Use download.")


def snippet_for_query(text: str, terms: list[str], radius: int = 170) -> str:
    lowered = text.lower()
    matches = [lowered.find(term.lower()) for term in terms if lowered.find(term.lower()) != -1]
    if not matches:
        trimmed = text.strip().replace("\n", " ")
        return trimmed[: radius * 2] + ("..." if len(trimmed) > radius * 2 else "")
    start = max(min(matches) - radius, 0)
    end = min(start + radius * 2, len(text))
    snippet = text[start:end].replace("\n", " ")
    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet = snippet + "..."
    return snippet


def highlight_terms(text: str, terms: list[str]) -> str:
    if not terms:
        return html.escape(text)
    pattern = re.compile("(" + "|".join(re.escape(term) for term in terms if term) + ")", re.IGNORECASE)
    escaped = html.escape(text)
    return pattern.sub(lambda match: f"<mark>{html.escape(match.group(0))}</mark>", escaped)


def search_documents(index: list[dict], query: str, selected_collections: set[str]) -> list[dict]:
    terms = [term.strip() for term in re.split(r"\s+", query) if term.strip()]
    if not terms:
        return []
    results = []
    for item in index:
        relative_path = item["relative_path"]
        collection = Path(relative_path).parts[0]
        if collection not in selected_collections:
            continue
        haystack = f"{item['name']}\n{item['text']}".lower()
        if all(term.lower() in haystack for term in terms):
            results.append(
                {
                    "path": item["path"],
                    "relative_path": relative_path,
                    "snippet": snippet_for_query(item["text"], terms),
                }
            )
    return results


def render_search(index: list[dict], selected_collections: list[str]) -> None:
    st.subheader("Search")
    query = st.text_input("Keywords", placeholder="Search across all indexed documents")
    if not query.strip():
        return

    results = search_documents(index, query, set(selected_collections))
    st.caption(f"{len(results)} result(s)")
    if not results:
        st.warning("No matches found.")
        return

    terms = [term.strip() for term in re.split(r"\s+", query) if term.strip()]
    for idx, result in enumerate(results[:250]):
        path = Path(result["path"])
        st.markdown(
            f"""
            <div class="search-hit">
                <div class="search-path">{html.escape(result["relative_path"])}</div>
                <div class="file-title">{html.escape(path.name)}</div>
                <div class="search-snippet">{highlight_terms(result["snippet"], terms)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        col_a, col_b = st.columns([1, 1])
        with col_a:
            if st.button("Open result", key=f"open-search-{idx}", use_container_width=True):
                st.session_state["selected_file"] = str(path)
                parent = path.parent
                st.session_state["current_folder"] = str(parent)
                st.session_state["mode"] = "Browse"
                st.rerun()
        with col_b:
            st.caption(path.suffix.lower().lstrip(".").upper())


def render_browse(collection_roots: list[Path], entries: list[DocEntry]) -> None:
    current_folder = Path(st.session_state["current_folder"])
    selected_file = st.session_state.get("selected_file")

    st.subheader("Browse")
    st.markdown(
        f"""
        <div class="browser-card">
            <div class="path-label">Current folder</div>
            <div class="file-title">{html.escape(breadcrumb(current_folder))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    nav_col, preview_col = st.columns([1.1, 1.9], gap="large")

    with nav_col:
        if len(current_folder.relative_to(WORKSPACE_ROOT).parts) > 1:
            if st.button("Up one level", use_container_width=True):
                set_current_folder(open_parent(current_folder))
                st.rerun()

        dirs, files = folder_children(current_folder)
        if dirs:
            st.caption("Folders")
            for directory in dirs:
                if st.button(f"📁 {directory.name}", key=f"dir-{directory}", use_container_width=True):
                    set_current_folder(directory)
                    st.rerun()
        if files:
            st.caption("Files")
            for file_path in files:
                label = f"• {file_path.name}"
                if st.button(label, key=f"file-{file_path}", use_container_width=True):
                    set_selected_file(file_path)
                    st.rerun()

        st.divider()
        st.caption("Collections")
        for root in collection_roots:
            if st.button(root.name, key=f"root-{root}", use_container_width=True):
                set_current_folder(root)
                st.rerun()

    with preview_col:
        if selected_file:
            render_file_preview(Path(selected_file))
        else:
            folder_entries = [
                entry for entry in entries if Path(entry.path).parent == current_folder
            ]
            st.markdown(
                """
                <div class="browser-card">
                    <div class="file-title">Select a file</div>
                    <div class="path-label">The preview opens here.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if folder_entries:
                st.write("")
                for entry in folder_entries[:50]:
                    st.markdown(
                        f"""
                        <div class="browser-card">
                            <div class="path-label">{html.escape(entry.kind.upper())}</div>
                            <div class="file-title">{html.escape(Path(entry.path).name)}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    if st.button("Preview", key=f"preview-{entry.path}", use_container_width=True):
                        set_selected_file(Path(entry.path))
                        st.rerun()
                    st.write("")


def render_header(entries: list[DocEntry], indexed_docs: int) -> None:
    total_pdfs = sum(1 for entry in entries if entry.kind == "pdf")
    total_markdown = sum(1 for entry in entries if entry.kind == "md")
    st.markdown('<div class="app-title">Research Workspace</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="meta-row">
            <div class="metric-chip">{len(entries)} files</div>
            <div class="metric-chip">{indexed_docs} searchable docs</div>
            <div class="metric-chip">{total_markdown} markdown</div>
            <div class="metric-chip">{total_pdfs} PDFs</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(page_title="Research Workspace", page_icon="📚", layout="wide")
    app_css()

    collection_roots = existing_collections()
    if not collection_roots:
        st.error("No content collections were found in this workspace.")
        return

    selected_collections = render_sidebar(collection_roots)
    active_roots = [root for root in collection_roots if root.name in selected_collections]
    ensure_valid_state(active_roots or collection_roots)

    entries = collect_entries(tuple(selected_collections))
    signature = entry_signature([entry for entry in entries if Path(entry.path).suffix.lower() in TEXT_SUFFIXES])
    index = build_search_index(signature)

    if not entries:
        st.warning("No supported files found in the selected collections.")
        return

    render_header(entries, len(index))
    mode = st.segmented_control(
        "Mode",
        options=["Browse", "Search"],
        default=st.session_state.get("mode", "Browse"),
        selection_mode="single",
    )
    st.session_state["mode"] = mode
    if mode == "Search":
        render_search(index, selected_collections)
    else:
        render_browse(active_roots or collection_roots, entries)


if __name__ == "__main__":
    main()
