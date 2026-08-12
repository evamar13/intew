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
PAGES = ["Home", "Library", "Search"]

SECTION_SPECS = [
    {
        "id": "prep",
        "label": "Assessment prep",
        "description": "Core preparation notes, inferred evaluation model, methods and competency prep.",
        "path": "Things to prepare/OECD_written_assessment_prep",
    },
    {
        "id": "llm",
        "label": "LLM research",
        "description": "AI discoverability, generative search, bot traffic, attribution and measurement research.",
        "path": "Things to prepare/General LLM Research",
    },
    {
        "id": "tone",
        "label": "OECD tone of voice",
        "description": "Writing structure, argument logic, data narration and OECD-style expression patterns.",
        "path": "Research/OECD Tone Of Voice",
    },
    {
        "id": "comms",
        "label": "OECD communications",
        "description": "Directorate COM, official channels, publications, audience structure and communications model.",
        "path": "Research/OECD Official Communications",
    },
    {
        "id": "ai_oecd",
        "label": "OECD AI",
        "description": "OECD AI principles, policy resources, AI index, incidents, risks and public-sector material.",
        "path": "Research/AI in the OECD",
    },
    {
        "id": "resources",
        "label": "External resources",
        "description": "Eurostat, OECD data explorer, AI policy navigator, tools, metrics and external reference sets.",
        "path": "Research/Resoruces",
    },
    {
        "id": "cases",
        "label": "Practice case",
        "description": "Example case material and practice output for the written assessment.",
        "path": "Assesment/Example of a case",
    },
    {
        "id": "instructions",
        "label": "Assessment instructions",
        "description": "Logistics and activity instructions relevant to the written exercise format.",
        "path": "Assesment/Assesment instructions",
    },
]


def app_css() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 1450px;
            padding-top: 1.2rem;
            padding-bottom: 2rem;
        }
        .app-title {
            font-size: 2.35rem;
            font-weight: 760;
            letter-spacing: -0.04em;
            line-height: 1;
            margin-bottom: 0.3rem;
            color: #0f172a;
        }
        .app-subtitle {
            font-size: 0.98rem;
            color: #475569;
            max-width: 62rem;
            margin-bottom: 1rem;
        }
        .soft-card {
            border: 1px solid rgba(15, 23, 42, 0.08);
            background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
            border-radius: 22px;
            padding: 1rem 1.1rem 0.7rem;
            box-shadow: 0 16px 30px rgba(15, 23, 42, 0.04);
        }
        .hero-card {
            background:
                radial-gradient(circle at top right, rgba(180, 223, 255, 0.55), transparent 28%),
                linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 26px;
            padding: 1.25rem 1.35rem 1rem;
            box-shadow: 0 18px 34px rgba(15, 23, 42, 0.05);
        }
        .section-label {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #64748b;
            margin-bottom: 0.2rem;
        }
        .section-title {
            font-size: 1.15rem;
            font-weight: 720;
            color: #0f172a;
            margin-bottom: 0.25rem;
        }
        .section-copy {
            color: #475569;
            font-size: 0.92rem;
            line-height: 1.5;
            margin-bottom: 0.25rem;
        }
        .path-chip {
            display: inline-block;
            border-radius: 999px;
            padding: 0.3rem 0.6rem;
            background: #f1f5f9;
            color: #334155;
            font-size: 0.78rem;
            margin-top: 0.15rem;
        }
        .preview-meta {
            color: #64748b;
            font-size: 0.84rem;
            margin-bottom: 0.2rem;
        }
        .preview-title {
            color: #0f172a;
            font-size: 1.15rem;
            font-weight: 760;
            margin-bottom: 0.1rem;
        }
        .search-hit {
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 18px;
            padding: 0.95rem 1rem;
            margin-bottom: 0.8rem;
            background: #fff;
        }
        .search-path {
            color: #64748b;
            font-size: 0.8rem;
            margin-bottom: 0.3rem;
        }
        .search-snippet {
            color: #0f172a;
            font-size: 0.93rem;
            line-height: 1.56;
        }
        .small-note {
            color: #64748b;
            font-size: 0.84rem;
        }
        .stButton > button, .stDownloadButton > button {
            border-radius: 12px;
            font-weight: 650;
        }
        .stRadio [role="radiogroup"] {
            gap: 0.4rem;
        }
        mark {
            background: #fff3bf;
            padding: 0.04rem 0.16rem;
            border-radius: 0.15rem;
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


def section_map(sections: list[dict]) -> dict[str, dict]:
    return {section["id"]: section for section in sections}


def default_section_id(sections: list[dict]) -> str:
    return sections[0]["id"]


def is_visible(relative_path: Path) -> bool:
    return not any(part.startswith(".") or part in IGNORE_DIRS for part in relative_path.parts)


def is_supported_file(path: Path) -> bool:
    suffix = path.suffix.lower()
    return suffix in PREVIEWABLE_SUFFIXES or suffix in OTHER_VISIBLE_SUFFIXES


def is_inside_section(path: Path, section_root: Path) -> bool:
    return section_root == path or section_root in path.parents


def ensure_state(sections: list[dict]) -> None:
    if not sections:
        return

    section_lookup = section_map(sections)
    default_id = default_section_id(sections)

    st.session_state.setdefault("page", "Home")
    st.session_state.setdefault("active_section", default_id)
    if st.session_state["active_section"] not in section_lookup:
        st.session_state["active_section"] = default_id

    active_section = section_lookup[st.session_state["active_section"]]
    st.session_state.setdefault("current_folder", str(active_section["absolute_path"]))
    st.session_state.setdefault("selected_file", None)
    st.session_state.setdefault("recent_files", [])
    st.session_state.setdefault("search_scope", "Current section")

    current_folder = Path(st.session_state["current_folder"])
    if (
        not current_folder.exists()
        or not current_folder.is_dir()
        or not is_inside_section(current_folder, active_section["absolute_path"])
    ):
        st.session_state["current_folder"] = str(active_section["absolute_path"])

    selected_file = st.session_state.get("selected_file")
    if selected_file:
        file_path = Path(selected_file)
        if not file_path.exists() or not is_inside_section(file_path.parent, active_section["absolute_path"]):
            st.session_state["selected_file"] = None


def set_active_section(section_id: str, sections: list[dict]) -> None:
    lookup = section_map(sections)
    section = lookup[section_id]
    st.session_state["active_section"] = section_id
    st.session_state["current_folder"] = str(section["absolute_path"])
    st.session_state["selected_file"] = None


def set_current_folder(path: Path) -> None:
    st.session_state["current_folder"] = str(path)
    st.session_state["selected_file"] = None


def set_selected_file(path: Path) -> None:
    st.session_state["selected_file"] = str(path)
    recent = st.session_state.get("recent_files", [])
    rel = str(path.relative_to(WORKSPACE_ROOT))
    recent = [item for item in recent if item != rel]
    recent.insert(0, rel)
    st.session_state["recent_files"] = recent[:8]


def breadcrumb(path: Path) -> str:
    return " / ".join(path.relative_to(WORKSPACE_ROOT).parts)


def open_parent(folder: Path, section_root: Path) -> Path:
    if folder == section_root:
        return folder
    return folder.parent


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
    for child in sorted(folder.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower())):
        relative = child.relative_to(WORKSPACE_ROOT)
        if not is_visible(relative):
            continue
        if child.is_dir():
            dirs.append(child)
        elif child.is_file() and is_supported_file(child):
            files.append(child)
    return dirs, files


def filter_items(items: list[Path], query: str) -> list[Path]:
    if not query.strip():
        return items
    lowered = query.lower()
    return [item for item in items if lowered in item.name.lower()]


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


def render_sidebar(sections: list[dict]) -> dict:
    lookup = section_map(sections)
    st.sidebar.markdown("## Navigator")
    page = st.sidebar.radio("Workspace", PAGES, index=PAGES.index(st.session_state["page"]))
    st.session_state["page"] = page

    labels = {section["label"]: section["id"] for section in sections}
    current_label = lookup[st.session_state["active_section"]]["label"]
    chosen_label = st.sidebar.selectbox("Focus area", list(labels.keys()), index=list(labels.keys()).index(current_label))
    chosen_section_id = labels[chosen_label]
    if chosen_section_id != st.session_state["active_section"]:
        set_active_section(chosen_section_id, sections)
        st.rerun()

    st.sidebar.divider()
    st.sidebar.caption("Recent files")
    recent = st.session_state.get("recent_files", [])
    if not recent:
        st.sidebar.caption("No recent files yet.")
    else:
        for rel_path in recent:
            path = WORKSPACE_ROOT / rel_path
            if not path.exists():
                continue
            if st.sidebar.button(path.name, key=f"recent-{rel_path}", use_container_width=True):
                section = lookup[st.session_state["active_section"]]
                if not is_inside_section(path.parent, section["absolute_path"]):
                    for candidate in sections:
                        if is_inside_section(path.parent, candidate["absolute_path"]):
                            set_active_section(candidate["id"], sections)
                            break
                st.session_state["current_folder"] = str(path.parent)
                st.session_state["selected_file"] = str(path)
                st.session_state["page"] = "Library"
                st.rerun()

    st.sidebar.divider()
    st.sidebar.caption("The app only surfaces study folders relevant to the assessment.")
    return lookup[st.session_state["active_section"]]


def file_download(path: Path) -> None:
    st.download_button(
        "Download",
        data=path.read_bytes(),
        file_name=path.name,
        use_container_width=True,
    )


def pdf_viewer(path: Path) -> None:
    key = f"show-pdf-{path}"
    show = st.checkbox("Load PDF preview", key=key, value=st.session_state.get(key, False))
    if not show:
        st.info("PDF preview is off by default for speed. Enable it only when needed.")
        return
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    src = f"data:application/pdf;base64,{encoded}"
    st.components.v1.html(
        f'<iframe src="{src}" width="100%" height="920" style="border:none;border-radius:14px;"></iframe>',
        height=940,
    )


def image_viewer(path: Path) -> None:
    st.image(str(path), use_container_width=True)


def render_file_preview(path: Path) -> None:
    suffix = path.suffix.lower()
    st.markdown(
        f"""
        <div class="soft-card">
            <div class="preview-meta">{html.escape(str(path.relative_to(WORKSPACE_ROOT)))}</div>
            <div class="preview-title">{html.escape(path.name)}</div>
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
        st.info("Preview is not available for this file type. Use download.")


def render_home(sections: list[dict]) -> None:
    st.markdown('<div class="app-title">OECD Assessment Desk</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-subtitle">Use this as a working desk during the written exercise: start from the prep notes, jump into source research fast, and open only the documents you need.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-card">
            <div class="section-label">Recommended flow</div>
            <div class="section-title">1. Prep notes → 2. Source research → 3. Case practice → 4. Tone check</div>
            <div class="section-copy">
                Start with the curated prep folder, use search when you need evidence, then compare your answer structure against the example case and tone guidance.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    priority_ids = ["prep", "cases", "tone", "llm", "comms", "ai_oecd", "resources", "instructions"]
    ordered = [section for section in sections if section["id"] in priority_ids]
    sort_index = {section_id: idx for idx, section_id in enumerate(priority_ids)}
    ordered.sort(key=lambda section: sort_index[section["id"]])

    cols = st.columns(2, gap="large")
    for idx, section in enumerate(ordered):
        with cols[idx % 2]:
            st.markdown(
                f"""
                <div class="soft-card">
                    <div class="section-label">Focus area</div>
                    <div class="section-title">{html.escape(section["label"])}</div>
                    <div class="section-copy">{html.escape(section["description"])}</div>
                    <div class="path-chip">{html.escape(section["path"])}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            open_col, search_col = st.columns(2)
            with open_col:
                if st.button("Open library", key=f"home-open-{section['id']}", use_container_width=True):
                    st.session_state["active_section"] = section["id"]
                    st.session_state["current_folder"] = str(section["absolute_path"])
                    st.session_state["selected_file"] = None
                    st.session_state["page"] = "Library"
                    st.rerun()
            with search_col:
                if st.button("Search here", key=f"home-search-{section['id']}", use_container_width=True):
                    st.session_state["active_section"] = section["id"]
                    st.session_state["current_folder"] = str(section["absolute_path"])
                    st.session_state["selected_file"] = None
                    st.session_state["search_scope"] = "Current section"
                    st.session_state["page"] = "Search"
                    st.rerun()


def render_library(section: dict) -> None:
    current_folder = Path(st.session_state["current_folder"])
    selected_file = st.session_state.get("selected_file")

    st.markdown('<div class="app-title">Library</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="app-subtitle">{html.escape(section["label"])} · {html.escape(breadcrumb(current_folder))}</div>',
        unsafe_allow_html=True,
    )

    nav_col, preview_col = st.columns([1.05, 1.95], gap="large")

    with nav_col:
        st.markdown(
            f"""
            <div class="soft-card">
                <div class="section-label">Current focus</div>
                <div class="section-title">{html.escape(section["label"])}</div>
                <div class="section-copy">{html.escape(section["description"])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")

        nav_a, nav_b = st.columns(2)
        with nav_a:
            if st.button("Section root", use_container_width=True):
                set_current_folder(section["absolute_path"])
                st.rerun()
        with nav_b:
            disabled = current_folder == section["absolute_path"]
            if st.button("Up", use_container_width=True, disabled=disabled):
                set_current_folder(open_parent(current_folder, section["absolute_path"]))
                st.rerun()

        filter_text = st.text_input("Filter this folder", placeholder="Type a folder or file name")
        dirs, files = list_folder(current_folder)
        dirs = filter_items(dirs, filter_text)
        files = filter_items(files, filter_text)

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

        if not dirs and not files:
            st.info("No visible files or folders here.")

    with preview_col:
        if selected_file:
            render_file_preview(Path(selected_file))
        else:
            st.markdown(
                """
                <div class="soft-card">
                    <div class="section-label">Preview</div>
                    <div class="section-title">Select a document</div>
                    <div class="section-copy">Use the left panel to move through folders. Nothing is loaded until you open a file.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


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


def render_search(section: dict, sections: list[dict]) -> None:
    st.markdown('<div class="app-title">Search</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-subtitle">Search is lazy by design. Nothing is scanned until you submit a query.</div>',
        unsafe_allow_html=True,
    )

    scope = st.radio(
        "Search scope",
        options=["Current section", "All sections"],
        index=0 if st.session_state.get("search_scope", "Current section") == "Current section" else 1,
        horizontal=True,
    )
    st.session_state["search_scope"] = scope
    roots = [section["absolute_path"]] if scope == "Current section" else [item["absolute_path"] for item in sections]

    with st.form("search-form", clear_on_submit=False):
        query = st.text_input("Keywords", placeholder="Example: AI visibility OR bot traffic")
        submitted = st.form_submit_button("Run search", use_container_width=True)

    if not submitted or not query.strip():
        return

    status_slot = st.empty()
    results = search_documents(query, roots, status_slot)
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
                <div class="preview-title">{html.escape(path.name)}</div>
                <div class="search-snippet">{highlight_terms(result["snippet"], terms)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        action_col, meta_col = st.columns([1, 1])
        with action_col:
            if st.button("Open in library", key=f"open-search-{idx}", use_container_width=True):
                for candidate in sections:
                    if is_inside_section(path.parent, candidate["absolute_path"]):
                        st.session_state["active_section"] = candidate["id"]
                        break
                st.session_state["current_folder"] = str(path.parent)
                st.session_state["selected_file"] = str(path)
                set_selected_file(path)
                st.session_state["page"] = "Library"
                st.rerun()
        with meta_col:
            st.caption(result["kind"].upper())


def main() -> None:
    st.set_page_config(page_title="OECD Assessment Desk", page_icon="📚", layout="wide")
    app_css()

    sections = available_sections()
    if not sections:
        st.error("No study sections were found in this workspace.")
        return

    ensure_state(sections)
    active_section = render_sidebar(sections)

    page = st.session_state["page"]
    if page == "Home":
        render_home(sections)
    elif page == "Search":
        render_search(active_section, sections)
    else:
        render_library(active_section)


if __name__ == "__main__":
    main()
