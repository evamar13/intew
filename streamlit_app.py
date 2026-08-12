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
DEFAULT_COLLECTIONS = [
    "Research",
    "Things to prepare",
    "Assesment",
    "OECD comunications to me",
    "Maki Plarform",
]
TEXT_SUFFIXES = {".md", ".txt", ".pdf"}
PREVIEWABLE_SUFFIXES = TEXT_SUFFIXES | {".png", ".jpg", ".jpeg", ".gif", ".webp"}
OTHER_VISIBLE_SUFFIXES = {".xlsx", ".xls", ".docx", ".doc"}
IGNORE_DIRS = {".git", ".streamlit", "__pycache__"}


def app_css() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.35rem;
            padding-bottom: 2rem;
            max-width: 1380px;
        }
        .app-title {
            font-size: 2.05rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            margin-bottom: 0.15rem;
        }
        .app-subtitle {
            color: #64748b;
            font-size: 0.96rem;
            margin-bottom: 1rem;
        }
        .panel-card {
            border: 1px solid rgba(15, 23, 42, 0.09);
            border-radius: 18px;
            padding: 0.95rem 1rem 0.45rem;
            background: #ffffff;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
        }
        .path-label {
            font-size: 0.82rem;
            color: #64748b;
            margin-bottom: 0.22rem;
        }
        .file-title {
            font-size: 1.08rem;
            font-weight: 700;
            margin-bottom: 0.15rem;
            color: #0f172a;
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
            margin-bottom: 0.3rem;
        }
        .search-snippet {
            color: #0f172a;
            font-size: 0.93rem;
            line-height: 1.55;
        }
        .stButton > button {
            border-radius: 12px;
            font-weight: 600;
        }
        mark {
            background: #fff3bf;
            padding: 0.05rem 0.16rem;
            border-radius: 0.2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def existing_collections() -> list[Path]:
    return [WORKSPACE_ROOT / name for name in DEFAULT_COLLECTIONS if (WORKSPACE_ROOT / name).exists()]


def is_visible(relative_path: Path) -> bool:
    return not any(part.startswith(".") or part in IGNORE_DIRS for part in relative_path.parts)


def is_supported_file(path: Path) -> bool:
    suffix = path.suffix.lower()
    return suffix in PREVIEWABLE_SUFFIXES or suffix in OTHER_VISIBLE_SUFFIXES


def ensure_valid_state(collection_roots: list[Path]) -> None:
    if not collection_roots:
        return
    default_root = collection_roots[0]
    current_folder = Path(st.session_state.get("current_folder", default_root))
    if not current_folder.exists() or not current_folder.is_dir():
        st.session_state["current_folder"] = str(default_root)
    selected_file = st.session_state.get("selected_file")
    if selected_file and not Path(selected_file).exists():
        st.session_state["selected_file"] = None


def set_current_folder(path: Path) -> None:
    st.session_state["current_folder"] = str(path)
    st.session_state["selected_file"] = None


def set_selected_file(path: Path) -> None:
    st.session_state["selected_file"] = str(path)


def breadcrumb(path: Path) -> str:
    return " / ".join(path.relative_to(WORKSPACE_ROOT).parts)


def open_parent(folder: Path) -> Path:
    relative = folder.relative_to(WORKSPACE_ROOT)
    if len(relative.parts) <= 1:
        return folder
    return WORKSPACE_ROOT.joinpath(*relative.parts[:-1])


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


def list_folder(folder: Path) -> tuple[list[Path], list[Path]]:
    dirs: list[Path] = []
    files: list[Path] = []
    for child in sorted(folder.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
        relative = child.relative_to(WORKSPACE_ROOT)
        if not is_visible(relative):
            continue
        if child.is_dir():
            dirs.append(child)
        elif child.is_file() and is_supported_file(child):
            files.append(child)
    return dirs, files


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


def format_size(size: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    current = float(size)
    for unit in units:
        if current < 1024 or unit == units[-1]:
            return f"{current:.0f} {unit}" if unit == "B" else f"{current:.1f} {unit}"
        current /= 1024
    return f"{size} B"


def file_download(path: Path) -> None:
    st.download_button(
        "Download",
        data=path.read_bytes(),
        file_name=path.name,
        use_container_width=True,
    )


def pdf_viewer(path: Path) -> None:
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    src = f"data:application/pdf;base64,{encoded}"
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
        <div class="panel-card">
            <div class="path-label">{html.escape(str(path.relative_to(WORKSPACE_ROOT)))}</div>
            <div class="file-title">{html.escape(path.name)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    top_cols = st.columns([1, 5])
    with top_cols[0]:
        file_download(path)
    with top_cols[1]:
        st.caption(f"{suffix.lstrip('.').upper()} · {format_size(path.stat().st_size)}")
    st.divider()

    if suffix == ".md":
        st.markdown(read_text_file(path))
    elif suffix == ".txt":
        st.text(read_text_file(path))
    elif suffix == ".pdf":
        pdf_viewer(path)
    elif suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
        image_viewer(path)
    else:
        st.info("Preview is not available for this file type. Use download.")


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


def search_documents(query: str, roots: list[Path], status_slot) -> list[dict]:
    terms = [term.strip() for term in re.split(r"\s+", query) if term.strip()]
    if not terms:
        return []

    results: list[dict] = []
    scanned = 0
    for path in iter_searchable_files(roots):
        scanned += 1
        if scanned == 1 or scanned % 10 == 0:
            status_slot.caption(f"Scanning {scanned} documents...")
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


def render_header(current_folder: Path) -> None:
    st.markdown('<div class="app-title">Research Workspace</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="app-subtitle">{html.escape(breadcrumb(current_folder))}</div>',
        unsafe_allow_html=True,
    )


def render_sidebar(collection_roots: list[Path]) -> list[str]:
    st.sidebar.markdown("## Explorer")
    available = [root.name for root in collection_roots]
    default = st.session_state.get("active_collections", available)
    selected = st.sidebar.multiselect("Collections", available, default=default)
    if not selected:
        selected = available
    st.session_state["active_collections"] = selected
    st.sidebar.divider()
    st.sidebar.caption("No recursive loading on startup.")
    return selected


def render_search(active_roots: list[Path], current_folder: Path) -> None:
    st.subheader("Search")
    scope = st.radio(
        "Scope",
        options=["Current folder", "Selected collections"],
        horizontal=True,
    )
    search_roots = [current_folder] if scope == "Current folder" else active_roots

    with st.form("workspace-search-form", clear_on_submit=False):
        query = st.text_input("Keywords", placeholder="Search only when you submit")
        submitted = st.form_submit_button("Search", use_container_width=True)

    if not submitted or not query.strip():
        return

    status_slot = st.empty()
    results = search_documents(query, search_roots, status_slot)
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
                st.session_state["current_folder"] = str(path.parent)
                st.session_state["mode"] = "Browse"
                st.rerun()
        with col_b:
            st.caption(result["kind"].upper())


def render_browse(collection_roots: list[Path], current_folder: Path) -> None:
    selected_file = st.session_state.get("selected_file")

    st.subheader("Browse")
    nav_col, preview_col = st.columns([1.08, 1.92], gap="large")

    with nav_col:
        st.markdown(
            """
            <div class="panel-card">
                <div class="path-label">Current folder</div>
                <div class="file-title">Browse the workspace structure</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")

        if len(current_folder.relative_to(WORKSPACE_ROOT).parts) > 1:
            if st.button("Up one level", use_container_width=True):
                set_current_folder(open_parent(current_folder))
                st.rerun()

        dirs, files = list_folder(current_folder)

        if dirs:
            st.caption("Folders")
            for directory in dirs:
                if st.button(f"📁 {directory.name}", key=f"dir-{directory}", use_container_width=True):
                    set_current_folder(directory)
                    st.rerun()

        if files:
            st.caption("Files")
            for file_path in files:
                if st.button(f"• {file_path.name}", key=f"file-{file_path}", use_container_width=True):
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
            st.markdown(
                """
                <div class="panel-card">
                    <div class="file-title">Select a file</div>
                    <div class="path-label">Only the opened document is loaded.</div>
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

    current_folder = Path(st.session_state["current_folder"])
    render_header(current_folder)

    mode = st.segmented_control(
        "Mode",
        options=["Browse", "Search"],
        default=st.session_state.get("mode", "Browse"),
        selection_mode="single",
    )
    st.session_state["mode"] = mode

    if mode == "Search":
        render_search(active_roots or collection_roots, current_folder)
    else:
        render_browse(active_roots or collection_roots, current_folder)


if __name__ == "__main__":
    main()
