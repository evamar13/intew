from __future__ import annotations

import base64
import html
import re
import textwrap
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parent
LOGO_PATH = ROOT / "image.png"
DISPLAY_FONT_DIR = ROOT / "Noto_Sans_Display"
FONT_FAMILY_DIR = ROOT / "Noto_Sans,Noto_Sans_Display"
WORKBOOK_PATH = ROOT / (
    "Assesment/Assesment instructions/"
    "tiny_mce_3d2e5fe2-264a-4209-92c3-464559e5dbf3_Excel File supporting document_"
    "Question1_Junior AI & Communication Officer REF3112J.xlsx"
)


REFERENCE_NOTES = [
    {
        "title": "Original written assessment instructions",
        "path": ROOT / "Assesment/Assesment instructions/original-written-assessment-instructions.md",
        "use": "Defines the required output structure: executive summary, data analysis, LLM visibility research, and recommendations.",
        "apa": "Organisation for Economic Co-operation and Development. (2026). Original written assessment instructions [Assessment brief].",
        "url": None,
    },
    {
        "title": "OECD Style Guide (Fourth Edition) - 2025",
        "path": ROOT / "Research/OECD Tone Of Voice/OECD Style Guide (Fourth Edition) - 2025.pdf",
        "use": "Shapes the dashboard tone: concise, evidence-led, plain language, and explicit source notes.",
        "apa": "Organisation for Economic Co-operation and Development. (2025). OECD style guide (4th ed.).",
        "url": None,
    },
    {
        "title": "Profound Knowledge Base: Answer Engine Insights Overview",
        "path": ROOT / "Research/Profound/Answer Engine Insights Overview _ Profound Knowledge Base.pdf",
        "use": "Supports interpretation of answer-engine visibility as a monitored discovery layer rather than a traffic metric.",
        "apa": "Profound. (n.d.). Answer engine insights overview. Profound Knowledge Base.",
        "url": None,
    },
    {
        "title": "Profound glossary",
        "path": ROOT / "Research/Profound/Profound glossary _ Profound Knowledge Base.pdf",
        "use": "Supports metric language for prompts, mentions, citations, and monitored outputs.",
        "apa": "Profound. (n.d.). Profound glossary. Profound Knowledge Base.",
        "url": None,
    },
    {
        "title": "Writesonic: Prompts vs Keywords [Very Important]",
        "path": ROOT / "Research/Writesonic/Prompts vs Keywords [Very Important].pdf",
        "use": "Supports the choice to analyse prompt-level visibility rather than rely on classic search-keyword logic.",
        "apa": "Writesonic. (n.d.). Prompts vs keywords [Very important].",
        "url": "https://docs.writesonic.com/docs/prompts-vs-keywords-very-important",
    },
    {
        "title": "Writesonic: Platform Behavior & Volatility",
        "path": ROOT / "Research/Writesonic/Platform Behavior & Volatility.pdf",
        "use": "Supports explicit caveats on platform instability and the need for repeated measurement.",
        "apa": "Writesonic. (n.d.). Platform behavior & volatility.",
        "url": "https://docs.writesonic.com/docs/platform-behavior-tracking",
    },
    {
        "title": "Writesonic: Why We Monitor Real AI Platforms, Not Just APIs",
        "path": ROOT / "Research/Writesonic/Why We Monitor Real AI Platforms, Not Just APIs.pdf",
        "use": "Supports the focus on platform-observed outputs rather than API-only testing.",
        "apa": "Writesonic. (n.d.). Why we monitor real AI platforms, not just APIs.",
        "url": "https://docs.writesonic.com/docs/why-we-monitor-real-ai-platforms-not-just-apis",
    },
    {
        "title": "OECD workbook validated note",
        "path": ROOT / "Assesment/Assesment instructions/contrast-between-oecd-workbook-and-writesonic-documentation.md",
        "use": "Provides the validated interpretation of the workbook structure and its analytical limits.",
        "apa": "Organisation for Economic Co-operation and Development. (2026). OECD workbook validated note [Internal analytical note].",
        "url": None,
    },
    {
        "title": "Reuters Institute Digital News Report 2026",
        "path": ROOT / "Things to prepare/General LLM Research/changes in the media landscape/country and regional media landscapes/DNR 2026 FINAL_2.pdf",
        "use": "Supports the broader shift in discovery and information access patterns.",
        "apa": "Egan, J., Robertson, C. T., Ross Arguedas, A., Newman, N., Kleis Nielsen, R., Mukherjee, M., & Fletcher, R. (2026). Digital news report 2026. Reuters Institute for the Study of Journalism. https://doi.org/10.60625/risj-4vgf-s811",
        "url": "https://doi.org/10.60625/risj-4vgf-s811",
    },
    {
        "title": "JRC Generative AI outlook report",
        "path": ROOT / "Things to prepare/General LLM Research/changes in the media landscape/AI adoption and usage trends/JRC142598_01.pdf",
        "use": "Supports the policy relevance of generative AI as an information intermediary.",
        "apa": "European Commission, Joint Research Centre. (2025). Generative AI outlook report: Exploring the intersection of technology, society, and policy. Publications Office of the European Union. https://doi.org/10.2760/1109679",
        "url": "https://doi.org/10.2760/1109679",
    },
    {
        "title": "Nieman Journalism Lab: Generative AI models love to cite Reuters and Axios, study finds",
        "path": ROOT / "Things to prepare/General LLM Research/generative search visibility/citation or mention checks in AI outputs/Generative AI models love to cite Reuters and Axios, study finds _ Nieman Journalism Lab.pdf",
        "use": "Supports the importance of citation competition, not only mention competition.",
        "apa": "Nieman Journalism Lab. (n.d.). Generative AI models love to cite Reuters and Axios, study finds.",
        "url": None,
    },
]

TABLE_LABELS = {
    "topic": "Topic",
    "prompts": "Observations",
    "mention_rate": "OECD mention rate",
    "oecd_citation_rate": "OECD citation rate",
    "priority_band": "Priority",
    "avg_citations": "Average citations",
    "avg_position": "Average OECD position",
    "citation_url": "Citation URL",
    "domain": "Domain",
    "platform": "Platform",
    "spread": "Cross-platform spread",
    "best_platform": "Best platform",
    "worst_platform": "Weakest platform",
    "min_rate": "Lowest mention rate",
    "max_rate": "Highest mention rate",
    "avg_rate": "Average mention rate",
}


def font_data_uri(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        data = path.read_bytes()
    except Exception:
        return None
    encoded = base64.b64encode(data).decode("ascii")
    return f"data:font/ttf;base64,{encoded}"


def inject_css() -> None:
    body_regular_uri = font_data_uri(
        FONT_FAMILY_DIR / "Noto_Sans/static/NotoSans-Regular.ttf"
    )
    body_bold_uri = font_data_uri(
        FONT_FAMILY_DIR / "Noto_Sans/static/NotoSans-Bold.ttf"
    )
    display_regular_uri = font_data_uri(
        DISPLAY_FONT_DIR / "static/NotoSansDisplay-Regular.ttf"
    )
    display_bold_uri = font_data_uri(
        DISPLAY_FONT_DIR / "static/NotoSansDisplay-Bold.ttf"
    )
    font_face_css = ""
    if body_regular_uri:
        font_face_css += f"""
        @font-face {{
            font-family: "OECD Noto Sans";
            src: url("{body_regular_uri}") format("truetype");
            font-style: normal;
            font-weight: 400;
            font-display: swap;
        }}
        """
    if body_bold_uri:
        font_face_css += f"""
        @font-face {{
            font-family: "OECD Noto Sans";
            src: url("{body_bold_uri}") format("truetype");
            font-style: normal;
            font-weight: 700;
            font-display: swap;
        }}
        """
    if display_regular_uri:
        font_face_css += f"""
        @font-face {{
            font-family: "OECD Noto Sans Display";
            src: url("{display_regular_uri}") format("truetype");
            font-style: normal;
            font-weight: 400;
            font-display: swap;
        }}
        """
    if display_bold_uri:
        font_face_css += f"""
        @font-face {{
            font-family: "OECD Noto Sans Display";
            src: url("{display_bold_uri}") format("truetype");
            font-style: normal;
            font-weight: 700;
            font-display: swap;
        }}
        """
    st.markdown(
        "<style>\n"
        + '@import url("https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded");\n'
        + '@import url("https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined");\n'
        + font_face_css
        + """
        :root {
            --midnight-blue: #101D40;
            --light-blue: #E0F2FF;
            --neutral: #FFFFFF;
            --accent-cyan: #45DEFF;
            --accent-blue: #1162D4;
            --ink: #101D40;
            --muted: #6F7C96;
            --line: #D4DFEA;
            --panel: #ffffff;
            --surface: #E0F2FF;
        }
        html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], .stApp {
            font-family: "OECD Noto Sans", "Noto Sans", sans-serif !important;
        }
        p, li, label, span, div, input, textarea, button, table, td, th {
            font-family: "OECD Noto Sans", "Noto Sans", sans-serif !important;
        }
        .material-symbols-rounded,
        .material-symbols-outlined,
        .material-icons,
        [class*="material-symbols"],
        [class*="material-icons"] {
            font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
            font-style: normal !important;
            font-weight: 400 !important;
            letter-spacing: normal !important;
            text-transform: none !important;
            white-space: nowrap !important;
            word-wrap: normal !important;
            direction: ltr !important;
            -webkit-font-smoothing: antialiased !important;
        }
        p, li, label, span, div, input, textarea, button, table, td, th {
            font-size: 15px;
            line-height: 1.45;
        }
        .stApp {
            background: var(--neutral);
            color: var(--ink);
        }
        header[data-testid="stHeader"] {
            display: none !important;
        }
        [data-testid="stToolbar"] {
            display: none !important;
        }
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        .block-container {
            max-width: min(99vw, 1920px);
            padding-top: 0.4rem;
            padding-bottom: 2rem;
            padding-left: 1.1rem;
            padding-right: 1.1rem;
        }
        .hero {
            background: var(--midnight-blue);
            color: white;
            padding: 1.25rem 1.35rem;
            border-radius: 10px;
            margin-bottom: 0.9rem;
            border: 1px solid var(--midnight-blue);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1.25rem;
        }
        .hero-copy { flex: 1 1 auto; min-width: 0; }
        .hero-logo-wrap {
            flex: 0 0 auto;
            background: var(--neutral);
            border: 1px solid rgba(255,255,255,0.28);
            border-radius: 8px;
            padding: 0.5rem 0.75rem;
        }
        .hero-logo {
            width: 170px;
            max-width: 100%;
            display: block;
        }
        .hero h1 {
            margin: 0 0 0.2rem 0;
            font-family: "OECD Noto Sans Display", "Noto Sans", sans-serif !important;
            font-size: 2rem;
            line-height: 1.1;
            font-weight: 700;
        }
        .hero p {
            margin: 0;
            color: rgba(255,255,255,0.86);
            font-size: 0.96rem;
        }
        .chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin-top: 0.9rem;
        }
        .chip {
            background: transparent;
            border: 1px solid rgba(255,255,255,0.24);
            color: white;
            border-radius: 999px;
            padding: 0.35rem 0.7rem;
            font-size: 0.78rem;
        }
        .metric-card {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 10px;
            padding: 0.9rem 1rem;
            min-height: 112px;
        }
        .metric-label {
            font-size: 0.8rem;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.03em;
            margin-bottom: 0.35rem;
        }
        .metric-value {
            font-family: "OECD Noto Sans Display", "Noto Sans", sans-serif !important;
            font-size: 1.75rem;
            line-height: 1.05;
            color: var(--midnight-blue);
            font-weight: 700;
            margin-bottom: 0.2rem;
        }
        .metric-note {
            font-size: 0.86rem;
            color: var(--muted);
        }
        .insight {
            background: var(--light-blue);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 0.85rem 1rem;
            margin-bottom: 0.55rem;
        }
        .insight strong {
            color: var(--midnight-blue);
        }
        .chart-interpretation {
            margin-top: 0.35rem;
            color: var(--midnight-blue);
            font-family: "OECD Noto Sans Display", "Noto Sans", sans-serif !important;
            font-size: 1rem;
            font-weight: 700;
            line-height: 1.35;
        }
        .chart-explanation {
            margin-top: 0.25rem;
            color: var(--muted);
            font-size: 0.84rem;
            line-height: 1.5;
        }
        .section-note {
            color: var(--muted);
            font-size: 0.88rem;
            margin-bottom: 0.5rem;
        }
        .legend-inline {
            display: flex;
            flex-wrap: wrap;
            gap: 0.8rem 1rem;
            margin-top: 0.25rem;
        }
        .legend-item {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            color: var(--muted);
            font-size: 0.84rem;
        }
        .legend-swatch {
            width: 14px;
            height: 14px;
            border-radius: 3px;
            border: 1px solid var(--line);
            flex: 0 0 auto;
        }
        .source-note {
            color: var(--muted);
            font-size: 13px;
            margin-top: 0.4rem;
            line-height: 1.45;
        }
        .reference-card {
            background: var(--neutral);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 0.85rem 1rem;
            margin: 0 0 0.65rem 0;
        }
        .reference-title {
            font-family: "OECD Noto Sans Display", "Noto Sans", sans-serif !important;
            font-size: 1rem;
            font-weight: 700;
            color: var(--midnight-blue);
            margin-bottom: 0.45rem;
        }
        .reference-line {
            color: var(--ink);
            font-size: 0.94rem;
            line-height: 1.5;
            margin-bottom: 0.2rem;
        }
        .reference-line code {
            color: #2d8b57;
            background: transparent;
            font-size: 0.9rem;
        }
        .oecd-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            background: var(--neutral);
            border: 1px solid var(--line);
            border-radius: 8px;
            overflow: hidden;
            margin: 0.25rem 0 0.5rem 0;
        }
        .oecd-table thead th {
            font-family: "OECD Noto Sans Display", "Noto Sans", sans-serif !important;
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--midnight-blue);
            background: var(--neutral);
            text-align: left;
            padding: 0.8rem 1rem;
            border-bottom: 1px solid var(--line);
            vertical-align: bottom;
        }
        .oecd-table tbody td {
            font-family: "OECD Noto Sans", "Noto Sans", sans-serif !important;
            font-size: 0.95rem;
            color: var(--ink);
            padding: 0.85rem 1rem;
            border-bottom: 1px solid var(--line);
            vertical-align: top;
            line-height: 1.45;
        }
        .oecd-table tbody tr:last-child td {
            border-bottom: none;
        }
        .oecd-table .num {
            text-align: right;
            white-space: nowrap;
        }
        .oecd-table .wrap {
            white-space: normal;
            word-break: normal;
        }
        .mini-title {
            font-family: "OECD Noto Sans Display", "Noto Sans", sans-serif !important;
            font-size: 0.95rem;
            color: var(--midnight-blue);
            font-weight: 700;
            margin-bottom: 0.35rem;
        }
        h1, h2, h3, h4, h5, h6 {
            font-family: "OECD Noto Sans Display", "Noto Sans", sans-serif !important;
            color: var(--midnight-blue);
            font-weight: 700 !important;
            font-style: normal !important;
        }
        h3 {
            font-size: 1.55rem !important;
            line-height: 1.2 !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.3rem;
        }
        .stTabs [data-baseweb="tab"] {
            font-family: "OECD Noto Sans Display", "Noto Sans", sans-serif !important;
            border-radius: 999px;
            padding: 0.4rem 0.85rem;
            background: var(--neutral);
            border: 1px solid var(--line);
            color: var(--midnight-blue);
        }
        .stTabs [aria-selected="true"] {
            background: var(--midnight-blue) !important;
            color: white !important;
            border-color: var(--midnight-blue) !important;
        }
        .sidebar-caption {
            color: var(--muted);
            font-size: 0.8rem;
            margin-top: -0.35rem;
        }
        [data-testid="stSidebar"] {
            background: var(--neutral);
            border-right: 1px solid var(--line);
        }
        [data-testid="stSidebar"] > div {
            background: var(--neutral);
        }
        [data-testid="stCaptionContainer"] p {
            font-family: "OECD Noto Sans", "Noto Sans", sans-serif !important;
            font-size: 13px !important;
            line-height: 1.45 !important;
            color: var(--muted) !important;
            margin: 0.15rem 0 0 0 !important;
            white-space: normal !important;
        }
        [data-testid="stExpander"] summary {
            font-family: "OECD Noto Sans Display", "Noto Sans", sans-serif !important;
            font-size: 18px !important;
            font-weight: 700 !important;
            color: var(--midnight-blue) !important;
            line-height: 1.35 !important;
            display: flex !important;
            align-items: center !important;
            gap: 0.45rem !important;
            white-space: normal !important;
        }
        [data-testid="stExpander"] summary p,
        [data-testid="stExpander"] summary span,
        [data-testid="stExpander"] summary div {
            font-family: "OECD Noto Sans Display", "Noto Sans", sans-serif !important;
            font-size: 18px !important;
            font-weight: 700 !important;
            line-height: 1.35 !important;
            margin: 0 !important;
            color: var(--midnight-blue) !important;
        }
        [data-testid="stExpander"] details {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--neutral);
        }
        .stPlotlyChart {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--neutral);
            padding: 0.2rem 0.15rem 0.05rem 0.15rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_workbook(path: str) -> pd.DataFrame:
    df = pd.read_excel(path, header=3)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["mentioned_bool"] = (
        df["mentioned?"].astype(str).str.strip().str.lower().eq("yes")
    )
    df["position_num"] = (
        df["position"]
        .astype(str)
        .str.extract(r"(\d+)", expand=False)
        .pipe(pd.to_numeric, errors="coerce")
    )

    citation_cols = [col for col in df.columns if col.startswith("citation_")]
    for col in citation_cols:
        df[col] = df[col].astype("string")

    def normalise_domain(url: object) -> str | None:
        if pd.isna(url):
            return None
        value = str(url).strip()
        if not value or not re.match(r"^https?://", value):
            return None
        domain = urlparse(value).netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        return domain or None

    domains_per_row: list[list[str]] = []
    first_domain: list[str | None] = []
    oecd_cited: list[bool] = []
    citation_count: list[int] = []
    non_oecd_first_domain: list[str | None] = []

    for _, row in df[citation_cols].iterrows():
        domains = []
        for value in row.tolist():
            domain = normalise_domain(value)
            if domain:
                domains.append(domain)
        domains_per_row.append(domains)
        first_domain.append(domains[0] if domains else None)
        oecd_cited.append(any(domain.endswith("oecd.org") for domain in domains))
        citation_count.append(len(domains))
        non_oecd = [domain for domain in domains if not domain.endswith("oecd.org")]
        non_oecd_first_domain.append(non_oecd[0] if non_oecd else None)

    df["citation_domains"] = domains_per_row
    df["first_citation_domain"] = first_domain
    df["oecd_cited"] = oecd_cited
    df["citation_count"] = citation_count
    df["first_non_oecd_domain"] = non_oecd_first_domain
    df["topic"] = df["topic"].fillna("Unspecified")
    df["platform"] = df["platform"].fillna("Unspecified")
    df["tags"] = df["tags"].fillna("")
    df["response"] = df["response"].fillna("")
    df["mentions"] = df["mentions"].fillna("")
    df["normalized_mentions"] = df["normalized_mentions"].fillna("")
    df["prompt"] = df["prompt"].fillna("")
    return df


def format_pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def format_pct_range(start: float, end: float) -> str:
    return f"{start * 100:.1f}% to {end * 100:.1f}%"


def wrap_label(value: str, width: int = 22) -> str:
    return "<br>".join(textwrap.wrap(value, width=width, break_long_words=False))


def bubble_label_offsets(df: pd.DataFrame) -> list[tuple[int, int]]:
    if df.empty:
        return []
    ordered = df.reset_index(drop=True).copy()
    x_min = float(ordered["prompts"].min())
    x_max = float(ordered["prompts"].max())
    y_min = float(ordered["mention_rate"].min())
    y_max = float(ordered["mention_rate"].max())
    x_span = max(x_max - x_min, 1.0)
    y_span = max(y_max - y_min, 0.01)
    x_close = max(140.0, x_span * 0.08)
    y_close = max(0.035, y_span * 0.16)

    offsets_by_index: dict[int, tuple[int, int]] = {}
    placed: list[dict[str, float]] = []
    side_toggle = -1

    for idx, row in ordered.sort_values(["mention_rate", "prompts"], ascending=[False, True]).iterrows():
        dx = 0
        dy = -48
        crowd_count = 0
        for previous in placed:
            close_x = abs(float(row["prompts"]) - previous["x"]) <= x_close
            close_y = abs(float(row["mention_rate"]) - previous["y"]) <= y_close
            if close_x and close_y:
                crowd_count += 1

        if crowd_count:
            side_toggle *= -1
            dx = 34 * side_toggle
            dy = -26 - min(crowd_count, 2) * 4
        elif float(row["mention_rate"]) >= 0.88:
            dy = -54

        if float(row["prompts"]) >= x_min + (x_span * 0.82):
            dx = -18
            dy = -34

        offsets_by_index[idx] = (dx, dy)
        placed.append({"x": float(row["prompts"]), "y": float(row["mention_rate"])})

    return [offsets_by_index[idx] for idx in ordered.index]


def rate_scatter_label_offsets(df: pd.DataFrame) -> list[tuple[int, int]]:
    if df.empty:
        return []
    ordered = df.reset_index(drop=True).copy()
    x_close = 0.07
    y_close = 0.055
    offsets_by_index: dict[int, tuple[int, int]] = {}
    placed: list[dict[str, float]] = []
    side_toggle = -1

    for idx, row in ordered.sort_values(["oecd_citation_rate", "mention_rate"], ascending=[False, True]).iterrows():
        dx = 0
        dy = -42
        crowd_count = 0
        for previous in placed:
            close_x = abs(float(row["mention_rate"]) - previous["x"]) <= x_close
            close_y = abs(float(row["oecd_citation_rate"]) - previous["y"]) <= y_close
            if close_x and close_y:
                crowd_count += 1

        if crowd_count:
            side_toggle *= -1
            dx = 30 * side_toggle
            dy = -24 - min(crowd_count, 2) * 4

        if float(row["mention_rate"]) <= 0.45 and float(row["oecd_citation_rate"]) <= 0.4:
            dy = -28

        offsets_by_index[idx] = (dx, dy)
        placed.append({"x": float(row["mention_rate"]), "y": float(row["oecd_citation_rate"])})

    return [offsets_by_index[idx] for idx in ordered.index]


def source_line(*titles: str) -> str:
    return "Source note: " + "; ".join(titles)


def build_range_legend_items(
    series: pd.Series,
    colors: list[str],
    labels: list[str],
    formatter=format_pct_range,
) -> list[dict[str, str]]:
    clean = series.dropna().astype(float)
    if clean.empty:
        return []
    min_value = float(clean.min())
    max_value = float(clean.max())
    if abs(min_value - max_value) < 1e-12:
        return [{"color": colors[0], "label": f"{labels[0]} [{formatter(min_value, max_value)}]"}]

    steps = len(colors)
    edges = [min_value + ((max_value - min_value) * idx / steps) for idx in range(steps + 1)]
    items = []
    for idx, color in enumerate(colors):
        start = float(edges[idx])
        end = float(edges[idx + 1])
        items.append(
            {
                "color": color,
                "label": f"{labels[idx]} [{formatter(start, end)}]",
            }
        )
    return items


def render_bottom_legend(intro: str, items: list[dict[str, str]]) -> None:
    items_html = "".join(
        f"<span class='legend-item'><span class='legend-swatch' style='background:{item['color']};'></span>{html.escape(item['label'])}</span>"
        for item in items
    )
    st.markdown(
        f"""
        <div class='section-note' style='margin-top:0.4rem; margin-bottom:0.6rem;'>
            {html.escape(intro)}
            <div class='legend-inline'>{items_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def presentation_label(column: str) -> str:
    if column in TABLE_LABELS:
        return TABLE_LABELS[column]
    return column.replace("_", " ").strip().capitalize()


def build_topic_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("topic", dropna=False)
        .agg(
            prompts=("run_id", "size"),
            mention_rate=("mentioned_bool", "mean"),
            oecd_citation_rate=("oecd_cited", "mean"),
            avg_citations=("citation_count", "mean"),
            avg_position=("position_num", "mean"),
        )
        .reset_index()
    )
    summary["citation_conversion"] = summary["oecd_citation_rate"].div(
        summary["mention_rate"].where(summary["mention_rate"] > 0)
    )
    summary["visibility_gap"] = 1 - summary["mention_rate"]
    summary["priority_score"] = summary["prompts"].rank(pct=True) * summary["visibility_gap"]
    summary["priority_band"] = pd.cut(
        summary["priority_score"],
        bins=[-0.01, 0.15, 0.30, 1.0],
        labels=["Monitor", "Target", "Prioritise"],
    )
    return summary.sort_values(["priority_score", "prompts"], ascending=[False, False])


def build_platform_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("platform", dropna=False)
        .agg(
            prompts=("run_id", "size"),
            mention_rate=("mentioned_bool", "mean"),
            oecd_citation_rate=("oecd_cited", "mean"),
            avg_citations=("citation_count", "mean"),
            avg_position=("position_num", "mean"),
        )
        .reset_index()
        .sort_values("mention_rate", ascending=False)
    )
    return summary


def build_daily_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("date", dropna=False)
        .agg(
            prompts=("run_id", "size"),
            mention_rate=("mentioned_bool", "mean"),
            oecd_citation_rate=("oecd_cited", "mean"),
        )
        .reset_index()
        .sort_values("date")
    )


def build_domain_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for _, row in df.iterrows():
        for domain in row["citation_domains"]:
            rows.append(
                {
                    "domain": domain,
                    "platform": row["platform"],
                    "topic": row["topic"],
                    "mentioned_bool": row["mentioned_bool"],
                }
            )
    if not rows:
        return pd.DataFrame(columns=["domain", "citations"])
    domains = pd.DataFrame(rows)
    return (
        domains.groupby("domain")
        .size()
        .reset_index(name="citations")
        .sort_values("citations", ascending=False)
    )


def build_topic_platform_spread(df: pd.DataFrame) -> pd.DataFrame:
    heatmap = df.pivot_table(
        index="topic",
        columns="platform",
        values="mentioned_bool",
        aggfunc="mean",
    )
    if heatmap.empty:
        return pd.DataFrame(
            columns=["topic", "min_rate", "max_rate", "spread", "avg_rate", "best_platform", "worst_platform"]
        )
    spread = pd.DataFrame(
        {
            "topic": heatmap.index,
            "min_rate": heatmap.min(axis=1).values,
            "max_rate": heatmap.max(axis=1).values,
            "spread": (heatmap.max(axis=1) - heatmap.min(axis=1)).values,
            "avg_rate": heatmap.mean(axis=1).values,
            "best_platform": heatmap.idxmax(axis=1).values,
            "worst_platform": heatmap.idxmin(axis=1).values,
        }
    )
    return spread.sort_values("spread", ascending=False)


def build_heatmap(df: pd.DataFrame) -> pd.DataFrame:
    return df.pivot_table(
        index="topic",
        columns="platform",
        values="mentioned_bool",
        aggfunc="mean",
    ).reset_index()


def headline_metrics(df: pd.DataFrame) -> dict[str, float]:
    avg_position = df.loc[df["mentioned_bool"], "position_num"].mean()
    mention_to_citation_conversion = df.loc[df["mentioned_bool"], "oecd_cited"].mean()
    all_non_oecd_domains = [
        domain
        for domains in df["citation_domains"]
        for domain in domains
        if not domain.endswith("oecd.org")
    ]
    if all_non_oecd_domains:
        counts = pd.Series(all_non_oecd_domains).value_counts()
        top5_non_oecd_share = float(counts.head(5).sum() / counts.sum())
    else:
        top5_non_oecd_share = float("nan")
    topic_spread = build_topic_platform_spread(df)
    avg_cross_platform_spread = (
        float(topic_spread["spread"].mean()) if not topic_spread.empty else float("nan")
    )
    return {
        "rows": float(len(df)),
        "mention_rate": float(df["mentioned_bool"].mean()),
        "oecd_citation_rate": float(df["oecd_cited"].mean()),
        "avg_citations": float(df["citation_count"].mean()),
        "avg_position": float(avg_position) if pd.notna(avg_position) else float("nan"),
        "mention_to_citation_conversion": (
            float(mention_to_citation_conversion)
            if pd.notna(mention_to_citation_conversion)
            else float("nan")
        ),
        "top5_non_oecd_share": top5_non_oecd_share,
        "avg_cross_platform_spread": avg_cross_platform_spread,
    }


def top_opportunity_sentence(topic_summary: pd.DataFrame) -> str:
    if topic_summary.empty:
        return "No filtered data available."
    row = topic_summary.iloc[0]
    return (
        f"The main visibility gap sits in {row['topic']}: it accounts for {int(row['prompts']):,} "
        f"prompt-platform tests, but OECD appears in only {row['mention_rate'] * 100:.1f}% of them."
    )


def top_platform_sentence(platform_summary: pd.DataFrame) -> str:
    if platform_summary.empty:
        return "No filtered data available."
    best = platform_summary.iloc[0]
    worst = platform_summary.iloc[-1]
    return (
        f"Performance ranges from {best['mention_rate'] * 100:.1f}% on {best['platform']} "
        f"to {worst['mention_rate'] * 100:.1f}% on {worst['platform']}."
    )


def citation_sentence(df: pd.DataFrame, domain_summary: pd.DataFrame) -> str:
    if df.empty or domain_summary.empty:
        return "No filtered data available."
    top_non_oecd = domain_summary.loc[domain_summary["domain"] != "oecd.org"].head(1)
    competitor = top_non_oecd.iloc[0]["domain"] if not top_non_oecd.empty else "non-OECD sources"
    return (
        f"OECD is cited directly in {df['oecd_cited'].mean() * 100:.1f}% of monitored answers. "
        f"The strongest recurring non-OECD citation competitor is {competitor}."
    )


def draw_metric_card(label: str, value: str, note: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_table(df: pd.DataFrame) -> None:
    columns = list(df.columns)
    header_html = "".join(
        f"<th>{html.escape(presentation_label(column))}</th>" for column in columns
    )
    body_rows = []
    for _, row in df.reset_index(drop=True).iterrows():
        cells = []
        for column in columns:
            value = "" if pd.isna(row[column]) else str(row[column])
            cell_class = "num" if column in {"prompts", "avg_citations"} else "wrap"
            cells.append(f"<td class='{cell_class}'>{html.escape(value)}</td>")
        body_rows.append("<tr>" + "".join(cells) + "</tr>")
    table_html = (
        "<table class='oecd-table'>"
        + "<thead><tr>"
        + header_html
        + "</tr></thead><tbody>"
        + "".join(body_rows)
        + "</tbody></table>"
    )
    st.markdown(table_html, unsafe_allow_html=True)


def apply_chart_theme(fig, height: int | None = None):
    fig.update_layout(
        font=dict(
            family='"OECD Noto Sans, Noto Sans, sans-serif',
            color="#101D40",
            size=14,
        ),
        title=dict(
            text="",
            font=dict(
                family='"OECD Noto Sans Display, Noto Sans, sans-serif',
                color="#101D40",
                size=24,
            ),
        ),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        margin=dict(l=14, r=14, t=24, b=14),
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="#D4DFEA",
        zeroline=False,
        linecolor="#D4DFEA",
        tickfont=dict(color="#6F7C96"),
        title_font=dict(color="#101D40"),
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#D4DFEA",
        zeroline=False,
        linecolor="#D4DFEA",
        tickfont=dict(color="#6F7C96"),
        title_font=dict(color="#101D40"),
    )
    if height is not None:
        fig.update_layout(height=height)
    return fig


def render_interpretation(lead: str, detail: str) -> None:
    st.markdown(
        f"""
        <div class="chart-interpretation">{lead}</div>
        <div class="chart-explanation">{detail}</div>
        """,
        unsafe_allow_html=True,
    )


def logo_data_uri() -> str | None:
    if not LOGO_PATH.exists():
        return None
    encoded = base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def render_header(df: pd.DataFrame) -> None:
    min_date = df["date"].min()
    max_date = df["date"].max()
    date_span = (
        f"{min_date.strftime('%d %b %Y')} to {max_date.strftime('%d %b %Y')}"
        if pd.notna(min_date) and pd.notna(max_date)
        else "Date range unavailable"
    )
    logo_uri = logo_data_uri()
    logo_html = (
        f'<div class="hero-logo-wrap"><img src="{logo_uri}" alt="OECD logo" class="hero-logo"></div>'
        if logo_uri
        else ""
    )
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-copy">
                <h1>OECD visibility in AI-generated answers</h1>
                <p>Prompt-level monitoring dashboard for unbranded queries across major AI answer surfaces.</p>
                <div class="chip-row">
                    <div class="chip">{len(df):,} prompt-platform observations</div>
                    <div class="chip">{df['platform'].nunique()} platforms</div>
                    <div class="chip">{df['topic'].nunique()} topics</div>
                    <div class="chip">Region: United States</div>
                    <div class="chip">{date_span}</div>
                </div>
            </div>
            {logo_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.markdown("## Filters")
    st.sidebar.markdown(
        '<div class="sidebar-caption">Use filters to narrow the monitored prompt set.</div>',
        unsafe_allow_html=True,
    )
    platforms = sorted(df["platform"].dropna().unique().tolist())
    topics = sorted(df["topic"].dropna().unique().tolist())
    date_min = df["date"].min().date()
    date_max = df["date"].max().date()

    selected_platforms = st.sidebar.multiselect(
        "Platforms", platforms, default=platforms
    )
    selected_topics = st.sidebar.multiselect("Topics", topics, default=topics)
    selected_dates = st.sidebar.slider(
        "Date range",
        min_value=date_min,
        max_value=date_max,
        value=(date_min, date_max),
    )
    mention_state = st.sidebar.radio(
        "Mention state",
        ["All rows", "OECD mentioned", "OECD not mentioned"],
        horizontal=False,
    )

    filtered = df[
        df["platform"].isin(selected_platforms)
        & df["topic"].isin(selected_topics)
        & df["date"].dt.date.between(selected_dates[0], selected_dates[1])
    ].copy()

    if mention_state == "OECD mentioned":
        filtered = filtered[filtered["mentioned_bool"]]
    elif mention_state == "OECD not mentioned":
        filtered = filtered[~filtered["mentioned_bool"]]

    st.sidebar.markdown("---")
    st.sidebar.metric("Rows", f"{len(filtered):,}")
    st.sidebar.metric("Mention rate", format_pct(filtered["mentioned_bool"].mean()) if not filtered.empty else "n/a")
    st.sidebar.metric("OECD citation rate", format_pct(filtered["oecd_cited"].mean()) if not filtered.empty else "n/a")
    st.sidebar.markdown("---")
    st.sidebar.caption("Monitored scope: unbranded prompts, United States, 13-19 July 2026.")
    return filtered


def render_summary_tab(df: pd.DataFrame) -> None:
    metrics = headline_metrics(df)
    topic_summary = build_topic_summary(df)
    platform_summary = build_platform_summary(df)
    domain_summary = build_domain_summary(df)
    topic_spread = build_topic_platform_spread(df)

    row1 = st.columns(5)
    with row1[0]:
        draw_metric_card("Prompt rows", f"{int(metrics['rows']):,}", "Observed prompt-platform cases")
    with row1[1]:
        draw_metric_card("OECD mentioned", format_pct(metrics["mention_rate"]), "Share of rows where OECD appears")
    with row1[2]:
        draw_metric_card("OECD cited", format_pct(metrics["oecd_citation_rate"]), "Share of rows with an oecd.org citation")
    with row1[3]:
        draw_metric_card("Avg. citations", f"{metrics['avg_citations']:.1f}", "Source density per answer")
    with row1[4]:
        avg_position_text = f"#{metrics['avg_position']:.1f}" if pd.notna(metrics["avg_position"]) else "n/a"
        draw_metric_card("Avg. OECD position", avg_position_text, "Only where OECD is mentioned")

    row2 = st.columns(3)
    with row2[0]:
        conversion_text = (
            format_pct(metrics["mention_to_citation_conversion"])
            if pd.notna(metrics["mention_to_citation_conversion"])
            else "n/a"
        )
        draw_metric_card(
            "Mention-to-citation conversion",
            conversion_text,
            "Share of OECD-mentioned rows that also cite oecd.org",
        )
    with row2[1]:
        concentration_text = (
            format_pct(metrics["top5_non_oecd_share"])
            if pd.notna(metrics["top5_non_oecd_share"])
            else "n/a"
        )
        draw_metric_card(
            "Top-5 non-OECD source concentration",
            concentration_text,
            "Share of non-OECD citations captured by the five leading external domains",
        )
    with row2[2]:
        spread_text = (
            format_pct(metrics["avg_cross_platform_spread"])
            if pd.notna(metrics["avg_cross_platform_spread"])
            else "n/a"
        )
        draw_metric_card(
            "Avg. cross-platform spread",
            spread_text,
            "Average topic-level gap between best and worst platform mention rate",
        )

    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        st.markdown("### Executive reading")
        st.markdown(
            f'<div class="insight"><strong>Visibility.</strong> OECD appears in {metrics["mention_rate"] * 100:.1f}% of monitored answers.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="insight"><strong>Topic priority.</strong> {top_opportunity_sentence(topic_summary)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="insight"><strong>Platform spread.</strong> {top_platform_sentence(platform_summary)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="insight"><strong>Citation capture.</strong> {citation_sentence(df, domain_summary)}</div>',
            unsafe_allow_html=True,
        )

    with right:
        st.markdown("### Highest-priority topics")
        table = topic_summary.loc[
            :, ["topic", "prompts", "mention_rate", "oecd_citation_rate", "priority_band"]
        ].head(7)
        display = table.copy()
        display["mention_rate"] = display["mention_rate"].map(lambda v: f"{v * 100:.1f}%")
        display["oecd_citation_rate"] = display["oecd_citation_rate"].map(lambda v: f"{v * 100:.1f}%")
        render_table(display)

    st.markdown("### Priority topics by visibility gap and monitoring volume")
    st.markdown(
        "<div class='section-note'>Bubble size reflects the number of prompt-platform observations for each topic.</div>",
        unsafe_allow_html=True,
    )
    plot_topics = topic_summary.copy()
    plot_topics["topic_label"] = plot_topics["topic"].map(lambda value: wrap_label(value, 18))
    label_offsets = bubble_label_offsets(plot_topics)
    fig = px.scatter(
        plot_topics,
        x="prompts",
        y="mention_rate",
        size="prompts",
        color="priority_band",
        custom_data=["topic", "prompts", "mention_rate", "oecd_citation_rate"],
        labels={
            "prompts": "Prompt-platform observations",
            "mention_rate": "OECD mention rate",
            "priority_band": "Priority",
        },
        color_discrete_map={
            "Prioritise": "#101D40",
            "Target": "#1162D4",
            "Monitor": "#45DEFF",
        },
        size_max=34,
    )
    fig.update_traces(
        marker=dict(line=dict(width=1, color="white"), opacity=0.9),
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            + "Observations: %{customdata[1]:,}<br>"
            + "Mention rate: %{customdata[2]:.1%}<br>"
            + "OECD citation rate: %{customdata[3]:.1%}<extra></extra>"
        ),
    )
    for (_, row), (ax, ay) in zip(plot_topics.iterrows(), label_offsets):
        fig.add_annotation(
            x=row["prompts"],
            y=row["mention_rate"],
            text=row["topic_label"],
            showarrow=True,
            arrowhead=0,
            arrowsize=1,
            arrowwidth=0.8,
            arrowcolor="#9DB2CF",
            ax=ax,
            ay=ay,
            xanchor="center",
            yanchor="bottom",
            align="center",
            bgcolor="rgba(255,255,255,0.92)",
            bordercolor="rgba(212,223,234,0.95)",
            borderwidth=1,
            borderpad=2,
            font=dict(
                family='"OECD Noto Sans, Noto Sans, sans-serif',
                size=9,
                color="#101D40",
            ),
        )
    fig.update_layout(
        margin=dict(l=24, r=20, t=56, b=86),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.7)",
        xaxis_tickformat=",",
        yaxis_tickformat=".0%",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.16,
            xanchor="right",
            x=1,
            title_text="",
        ),
        xaxis_title="Prompt-platform observations",
        yaxis_title="OECD mention rate",
        xaxis_range=[0, float(plot_topics["prompts"].max()) * 1.16],
        yaxis_range=[0.33, 1.04],
    )
    apply_chart_theme(fig, height=780)
    st.plotly_chart(fig, width="stretch")
    render_interpretation(
        "The main visibility risk is concentrated, not diffuse.",
        "Large bubbles in the lower half of the chart combine scale with weak presence, so they represent the clearest priority for intervention. The analytical logic follows prompt-based monitoring practice, where visibility is assessed comparatively across observed answer surfaces rather than treated as a conventional traffic indicator (Profound, n.d.; Writesonic, n.d.). It also fits broader evidence showing that generative systems are becoming a meaningful layer of information mediation and can create uneven topic-level discoverability (European Commission, Joint Research Centre, 2025; Egan et al., 2026).",
    )
    st.caption(
        source_line(
            "OECD workbook: Prompts in LLMs",
            "Profound Knowledge Base: Answer Engine Insights Overview",
            "Writesonic: Prompts vs Keywords [Very Important]",
            "Reuters Institute Digital News Report 2026",
            "JRC Generative AI outlook report",
            "Nieman Journalism Lab: Generative AI models love to cite Reuters and Axios, study finds",
        )
    )


def render_data_analysis_tab(df: pd.DataFrame) -> None:
    topic_summary = build_topic_summary(df)
    platform_summary = build_platform_summary(df)
    daily_summary = build_daily_summary(df)
    domain_summary = build_domain_summary(df)
    topic_spread = build_topic_platform_spread(df)

    col1, col2 = st.columns([1.62, 0.82], gap="large")
    with col1:
        st.markdown("### Visibility by topic, with OECD citation capture")
        topic_plot = topic_summary.head(12).sort_values("mention_rate").copy()
        fig = px.bar(
            topic_plot,
            x="mention_rate",
            y="topic",
            orientation="h",
            color="oecd_citation_rate",
            text="mention_rate",
            color_continuous_scale=["#E0F2FF", "#45DEFF", "#1162D4", "#101D40"],
            labels={"mention_rate": "Mention rate", "topic": ""},
        )
        fig.update_traces(texttemplate="%{text:.1%}", textposition="outside", cliponaxis=False)
        fig.update_layout(
            margin=dict(l=28, r=30, t=28, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.7)",
            xaxis_tickformat=".0%",
            xaxis_title="Mention rate",
            yaxis=dict(
                tickfont=dict(size=11),
                automargin=True,
            ),
            coloraxis_showscale=False,
        )
        apply_chart_theme(fig, height=560)
        st.plotly_chart(fig, width="stretch")
        render_bottom_legend(
            "Bar length shows OECD mention rate. Bar colour shows OECD citation rate.",
            build_range_legend_items(
                topic_plot["oecd_citation_rate"],
                ["#E0F2FF", "#45DEFF", "#1162D4", "#101D40"],
                [
                    "Lower OECD citation rate",
                    "Mid-range OECD citation rate",
                    "Higher OECD citation rate",
                    "Highest OECD citation rate",
                ],
            ),
        )
        render_interpretation(
            "Visibility varies sharply by topic, which points to a content-shape problem rather than a simple brand problem.",
            "Lower-performing topics are likely losing either retrieval priority or citation selection to external sources whose content is easier for answer engines to summarise directly. That reading is consistent with current work on AI-mediated discoverability, which shows that structure, citation patterns and answer-readiness matter alongside institutional authority (European Commission, Joint Research Centre, 2025; Nieman Journalism Lab, n.d.).",
        )

    with col2:
        st.markdown("### Seven-day stability of OECD mentions and citations")
        metric_labels = {
            "mention_rate": "OECD mention rate",
            "oecd_citation_rate": "OECD citation rate",
        }
        fig = px.line(
            daily_summary,
            x="date",
            y=["mention_rate", "oecd_citation_rate"],
            markers=True,
            labels={"value": "Rate", "date": "", "variable": ""},
        )
        fig.for_each_trace(lambda trace: trace.update(name=metric_labels.get(trace.name, trace.name)))
        fig.update_layout(
            margin=dict(l=10, r=10, t=20, b=76),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.7)",
            yaxis_tickformat=".0%",
            legend_title_text="",
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.16,
                xanchor="left",
                x=0,
            ),
            xaxis_title="Date",
            yaxis_title="Rate",
        )
        apply_chart_theme(fig, height=560)
        st.plotly_chart(fig, width="stretch")
        render_interpretation(
            "The seven-day pattern is directionally stable, but not stable enough to treat as permanent.",
            "Short-window movement is limited, which makes the main gaps credible, yet the evidence still sits within a volatile platform environment. The appropriate interpretation is therefore directional: the chart supports prioritisation, not a claim of fixed long-term ranking behaviour without repeated monitoring (Writesonic, n.d.; Egan et al., 2026).",
        )

    col3, col4 = st.columns([1.08, 0.92], gap="large")
    with col3:
        st.markdown("### Visibility and citation performance by AI platform")
        plot_df = platform_summary.melt(
            id_vars=["platform"],
            value_vars=["mention_rate", "oecd_citation_rate"],
            var_name="metric",
            value_name="rate",
        )
        plot_df["metric_label"] = plot_df["metric"].map(
            {
                "mention_rate": "OECD mention rate",
                "oecd_citation_rate": "OECD citation rate",
            }
        )
        fig = px.bar(
            plot_df,
            x="platform",
            y="rate",
            color="metric_label",
            text="rate",
            barmode="group",
            labels={"platform": "", "rate": "Rate", "metric_label": ""},
            color_discrete_map={
                "OECD mention rate": "#101D40",
                "OECD citation rate": "#1162D4",
            },
        )
        fig.update_traces(texttemplate="%{text:.1%}", textposition="outside", cliponaxis=False)
        fig.update_layout(
            margin=dict(l=10, r=10, t=20, b=82),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.7)",
            yaxis_tickformat=".0%",
            showlegend=False,
        )
        apply_chart_theme(fig, height=420)
        st.plotly_chart(fig, width="stretch")
        render_bottom_legend(
            "Bar colour distinguishes the two metrics shown in each platform comparison.",
            [
                {"color": "#101D40", "label": "OECD mention rate"},
                {"color": "#1162D4", "label": "OECD citation rate"},
            ],
        )
        render_interpretation(
            "Platform choice changes the result materially.",
            "Mention rate and OECD citation rate do not move in parallel across the systems tested, which means performance cannot be summarised with one cross-platform average alone. This is consistent with answer-engine monitoring guidance and with wider evidence on heterogeneous AI information interfaces (Writesonic, n.d.; European Commission, Joint Research Centre, 2025).",
        )

    with col4:
        st.markdown("### Most-cited domains in AI-generated answers")
        domains = domain_summary.head(10).copy()
        fig = px.bar(
            domains.sort_values("citations"),
            x="citations",
            y="domain",
            orientation="h",
            color="domain",
            text="citations",
            color_discrete_sequence=["#101D40"] + ["#E0F2FF"] * 9,
            labels={"citations": "Citations captured", "domain": ""},
        )
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False)
        fig.update_layout(
            showlegend=False,
            margin=dict(l=10, r=10, t=20, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.7)",
        )
        apply_chart_theme(fig, height=420)
        st.plotly_chart(fig, width="stretch")
        render_bottom_legend(
            "Bar colour distinguishes OECD citation volume from the leading external domains cited by answer engines.",
            [
                {"color": "#101D40", "label": "OECD domain (oecd.org)"},
                {"color": "#E0F2FF", "label": "External domains"},
            ],
        )
        render_interpretation(
            "The competitive contest is happening at the citation layer as much as at the mention layer.",
            "Answer engines are choosing which source to elevate as evidence, not just whether to mention the OECD. Strong non-OECD domains therefore represent a real authority challenge, even when OECD is present somewhere in the answer. This interpretation is aligned with emerging evidence on uneven citation distribution in generative systems (Nieman Journalism Lab, n.d.; Egan et al., 2026).",
        )

    st.markdown("### Topic table")
    display = topic_summary.loc[
        :, ["topic", "prompts", "mention_rate", "oecd_citation_rate", "avg_citations", "avg_position", "priority_band"]
    ].copy()
    display["mention_rate"] = display["mention_rate"].map(lambda v: f"{v * 100:.1f}%")
    display["oecd_citation_rate"] = display["oecd_citation_rate"].map(lambda v: f"{v * 100:.1f}%")
    display["avg_citations"] = display["avg_citations"].map(lambda v: f"{v:.1f}")
    display["avg_position"] = display["avg_position"].map(
        lambda v: f"#{v:.1f}" if pd.notna(v) else "n/a"
    )
    render_table(display)
    st.caption(
        source_line(
            "OECD workbook: Prompts in LLMs",
            "Writesonic: Platform Behavior & Volatility",
        )
    )

    st.markdown("### Additional diagnostics")
    st.markdown("#### Topics where OECD mentions do not convert into citations")
    st.markdown(
        "<div class='section-note'>Bubble size reflects the number of prompt-platform observations for each topic. The diagonal marks parity: topics below it are cited less often than they are mentioned.</div>",
        unsafe_allow_html=True,
    )
    scatter_df = topic_summary.copy()
    scatter_df["topic_label"] = scatter_df["topic"].map(lambda value: wrap_label(value, 18))
    scatter_offsets = rate_scatter_label_offsets(scatter_df)
    fig = px.scatter(
        scatter_df,
        x="mention_rate",
        y="oecd_citation_rate",
        size="prompts",
        color="priority_band",
        custom_data=["topic", "prompts", "mention_rate", "oecd_citation_rate", "citation_conversion"],
        labels={
            "mention_rate": "OECD mention rate",
            "oecd_citation_rate": "OECD citation rate",
            "priority_band": "Priority",
        },
        color_discrete_map={
            "Prioritise": "#101D40",
            "Target": "#1162D4",
            "Monitor": "#45DEFF",
        },
        size_max=30,
    )
    fig.add_shape(
        type="line",
        x0=0,
        y0=0,
        x1=1,
        y1=1,
        line=dict(color="#6F7C96", width=1, dash="dot"),
    )
    fig.update_traces(
        marker=dict(line=dict(width=1, color="white"), opacity=0.9),
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            + "Observations: %{customdata[1]:,}<br>"
            + "Mention rate: %{customdata[2]:.1%}<br>"
            + "OECD citation rate: %{customdata[3]:.1%}<br>"
            + "Mention-to-citation conversion: %{customdata[4]:.1%}<extra></extra>"
        ),
    )
    for (_, row), (ax, ay) in zip(scatter_df.iterrows(), scatter_offsets):
        fig.add_annotation(
            x=row["mention_rate"],
            y=row["oecd_citation_rate"],
            text=row["topic_label"],
            showarrow=True,
            arrowhead=0,
            arrowsize=1,
            arrowwidth=0.8,
            arrowcolor="#9DB2CF",
            ax=ax,
            ay=ay,
            xanchor="center",
            yanchor="bottom",
            align="center",
            bgcolor="rgba(255,255,255,0.92)",
            bordercolor="rgba(212,223,234,0.95)",
            borderwidth=1,
            borderpad=2,
            font=dict(
                family='"OECD Noto Sans, Noto Sans, sans-serif',
                size=9,
                color="#101D40",
            ),
        )
    fig.update_layout(
        margin=dict(l=10, r=10, t=36, b=84),
        legend_title_text="",
        xaxis_tickformat=".0%",
        yaxis_tickformat=".0%",
        xaxis_range=[0, 1.02],
        yaxis_range=[0, 1.06],
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.18,
            xanchor="right",
            x=1,
        ),
    )
    apply_chart_theme(fig, height=540)
    st.plotly_chart(fig, width="stretch")
    render_interpretation(
        "Topics that sit well below the diagonal are being mentioned more often than they are being credited.",
        "That pattern is analytically useful because it isolates attribution weakness rather than pure visibility weakness. In answer-engine environments, presence without citation can still shape exposure, but it does less to reinforce OECD source authority. This distinction is consistent with current research on citation competition and AI-mediated discoverability (Nieman Journalism Lab, n.d.; European Commission, Joint Research Centre, 2025).",
    )

    st.markdown("#### Topics with the largest platform-to-platform visibility gap")
    spread_df = topic_spread.head(12).sort_values("spread").copy()
    fig = px.bar(
        spread_df,
        x="spread",
        y="topic",
        orientation="h",
        color="avg_rate",
        text="spread",
        custom_data=["best_platform", "worst_platform", "min_rate", "max_rate"],
        color_continuous_scale=["#E0F2FF", "#1162D4", "#101D40"],
        labels={"spread": "Cross-platform spread", "topic": "", "avg_rate": "Average topic mention rate"},
    )
    fig.update_traces(
        texttemplate="%{text:.1%}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b><br>"
            + "Cross-platform spread: %{x:.1%}<br>"
            + "Best platform: %{customdata[0]} (%{customdata[3]:.1%})<br>"
            + "Weakest platform: %{customdata[1]} (%{customdata[2]:.1%})<extra></extra>"
        ),
    )
    fig.update_layout(
        margin=dict(l=12, r=12, t=30, b=20),
        xaxis_tickformat=".0%",
        coloraxis_showscale=False,
    )
    apply_chart_theme(fig, height=540)
    st.plotly_chart(fig, width="stretch")
    render_bottom_legend(
        "Bar length shows the gap between the strongest and weakest platform for each topic. Bar colour shows the average OECD mention rate across platforms.",
        build_range_legend_items(
            spread_df["avg_rate"],
            ["#E0F2FF", "#1162D4", "#101D40"],
            [
                "Lower average OECD mention rate",
                "Mid-range average OECD mention rate",
                "Higher average OECD mention rate",
            ],
        ),
    )
    render_interpretation(
        "Some topics are not just weak; they are unstable across platforms.",
        "A large spread means the same OECD topic performs very differently depending on the answer surface. That supports a platform-specific monitoring logic rather than one blended score. The point is aligned with answer-engine monitoring guidance and with broader work on heterogeneous AI information interfaces and platform intermediation (Writesonic, n.d.; Profound, n.d.; Egan et al., 2026).",
    )

    st.caption(
        source_line(
            "OECD workbook: Prompts in LLMs",
            "Platform Behavior & Volatility",
            "Why We Monitor Real AI Platforms, Not Just APIs",
            "Reuters Institute Digital News Report 2026",
            "JRC Generative AI outlook report",
            "Nieman Journalism Lab: Generative AI models love to cite Reuters and Axios, study finds",
        )
    )


def render_platform_diagnostics_tab(df: pd.DataFrame) -> None:
    heatmap = df.pivot_table(
        index="topic",
        columns="platform",
        values="mentioned_bool",
        aggfunc="mean",
    )
    heat_plot = heatmap.copy()
    heat_plot = heat_plot.loc[
        heat_plot.mean(axis=1).sort_values().index
    ]

    st.markdown("### Topic visibility by platform")
    st.markdown(
        "<div class='section-note'>Rows are sorted by each topic’s average mention rate across platforms: lowest visibility at the top, highest at the bottom.</div>",
        unsafe_allow_html=True,
    )
    fig = px.imshow(
        heat_plot,
        aspect="auto",
        color_continuous_scale=["#E0F2FF", "#45DEFF", "#1162D4", "#101D40"],
        labels={"x": "", "y": "", "color": "Mention rate"},
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=20, b=98),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.7)",
        coloraxis_colorbar=dict(
            orientation="h",
            title=dict(text="Mention rate", side="top", font=dict(size=11, color="#101D40")),
            thickness=12,
            len=0.4,
            y=-0.22,
            x=0.5,
            xanchor="center",
        ),
    )
    fig.update_yaxes(title_text="Topics sorted from low to high")
    apply_chart_theme(fig, height=760)
    st.plotly_chart(fig, width="stretch")
    render_interpretation(
        "Weak performance clusters by topic and by platform at the same time.",
        "That pattern argues against a single generic remediation tactic. The more defensible response is two-dimensional: improve answer-readiness in structurally weak topics and keep platform-specific monitoring because systems differ in retrieval, citation and response behaviour (Profound, n.d.; Writesonic, n.d.; European Commission, Joint Research Centre, 2025).",
    )

    st.markdown("### Lowest-performing topic-platform combinations")
    worst = (
        heatmap.stack()
        .reset_index(name="mention_rate")
        .sort_values("mention_rate")
        .head(15)
        .copy()
    )
    worst["mention_rate"] = worst["mention_rate"].map(lambda v: f"{v * 100:.1f}%")
    render_table(worst)

    st.markdown("### Interpretation")
    st.markdown(
        """
        <div class="insight"><strong>Platform gaps are material.</strong> Weak performance is not confined to one system; the same topic can underperform across multiple answer surfaces.</div>
        <div class="insight"><strong>Topic structure matters.</strong> High-demand policy areas with weak mention rates are likely being won by competitor domains with clearer answer formats, stronger citation capture, or more directly retrievable summaries.</div>
        <div class="insight"><strong>Monitoring should remain comparative.</strong> This workbook measures observed visibility in a controlled prompt set, not organic audience reach or downstream policy influence.</div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(
        source_line(
            "OECD workbook: Prompts in LLMs",
            "Profound glossary",
            "Writesonic: Why We Monitor Real AI Platforms, Not Just APIs",
            "Writesonic: Platform Behavior & Volatility",
        )
    )


def render_prompt_evidence_tab(df: pd.DataFrame) -> None:
    st.markdown("### Prompt explorer")
    st.markdown(
        '<div class="section-note">Use this view to inspect exact prompts, outputs, mentions and captured citations.</div>',
        unsafe_allow_html=True,
    )

    working = df.copy()
    working["row_label"] = (
        working["date"].dt.strftime("%Y-%m-%d")
        + " | "
        + working["platform"]
        + " | "
        + working["topic"]
        + " | "
        + working["prompt"].str.slice(0, 90)
    )
    selected_label = st.selectbox(
        "Select a prompt row",
        options=working["row_label"].tolist(),
        index=0 if not working.empty else None,
    )

    if not selected_label:
        st.info("No rows available for the current filter set.")
        return

    row = working.loc[working["row_label"] == selected_label].iloc[0]

    meta1, meta2, meta3, meta4 = st.columns(4)
    with meta1:
        draw_metric_card("Platform", row["platform"], row["date"].strftime("%d %b %Y"))
    with meta2:
        draw_metric_card("Topic", row["topic"], row["tags"] or "No tag metadata")
    with meta3:
        draw_metric_card("OECD mentioned", "Yes" if row["mentioned_bool"] else "No", f"Position: #{int(row['position_num'])}" if pd.notna(row["position_num"]) else "No recorded rank")
    with meta4:
        draw_metric_card("Captured citations", str(int(row["citation_count"])), "Direct source URLs in the answer")

    left, right = st.columns([0.92, 1.08], gap="large")
    with left:
        st.markdown("### Prompt")
        st.code(row["prompt"], language="text")
        st.markdown("### Mentions")
        st.write(row["normalized_mentions"] or "No extracted mentions")

    with right:
        st.markdown("### Response")
        st.write(row["response"] or "No response text captured")

    citations = [url for url in row["citation_domains"]]
    citation_urls = []
    for idx in range(1, 37):
        value = row.get(f"citation_{idx}")
        if pd.notna(value):
            citation_urls.append(str(value))
    st.markdown("### Citations")
    if citation_urls:
        render_table(
            pd.DataFrame(
                {
                    "citation_url": citation_urls,
                    "domain": [urlparse(url).netloc.lower().removeprefix("www.") for url in citation_urls],
                }
            )
        )
    else:
        st.write("No citation URLs recorded for this answer.")

    st.caption(
        source_line(
            "OECD workbook: Prompts in LLMs",
            "Profound Knowledge Base: Answer Engine Insights Overview",
        )
    )


def render_recommendations_tab(df: pd.DataFrame) -> None:
    topic_summary = build_topic_summary(df)
    platform_summary = build_platform_summary(df)
    domain_summary = build_domain_summary(df)

    top_topics = topic_summary.head(4)
    weakest_platform = platform_summary.sort_values("mention_rate").iloc[0] if not platform_summary.empty else None
    strongest_platform = platform_summary.sort_values("mention_rate", ascending=False).iloc[0] if not platform_summary.empty else None
    top_non_oecd = domain_summary.loc[domain_summary["domain"] != "oecd.org"].head(5)

    st.markdown("### Strategic recommendations")
    st.markdown(
        """
        <div class="insight"><strong>1. Prioritise the high-volume visibility gap.</strong> Build a focused remediation track for topics that combine high prompt volume with below-average OECD presence. Start with short answer-ready summaries, explicit evidence blocks, and stronger citation hooks.</div>
        <div class="insight"><strong>2. Treat citation capture as a separate objective.</strong> Mention visibility is higher than direct OECD citation. Optimisation should therefore aim to improve both retrieval and source selection.</div>
        <div class="insight"><strong>3. Maintain platform-specific monitoring.</strong> The spread between platforms is large enough to justify distinct watchlists, especially where one system materially under-indexes OECD content.</div>
        <div class="insight"><strong>4. Keep governance discipline.</strong> Use this dataset as directional intelligence, not as a proxy for audience reach, trust, or policy impact.</div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("### Immediate topic priorities")
        immediate = top_topics.loc[:, ["topic", "prompts", "mention_rate", "oecd_citation_rate"]].copy()
        immediate["mention_rate"] = immediate["mention_rate"].map(lambda v: f"{v * 100:.1f}%")
        immediate["oecd_citation_rate"] = immediate["oecd_citation_rate"].map(lambda v: f"{v * 100:.1f}%")
        render_table(immediate)

    with c2:
        st.markdown("### Monitoring implications")
        monitoring = pd.DataFrame(
            [
                {
                    "question": "Which platform needs the closest watch?",
                    "answer": weakest_platform["platform"] if weakest_platform is not None else "n/a",
                    "evidence": f"{weakest_platform['mention_rate'] * 100:.1f}% mention rate" if weakest_platform is not None else "n/a",
                },
                {
                    "question": "Where is OECD currently strongest?",
                    "answer": strongest_platform["platform"] if strongest_platform is not None else "n/a",
                    "evidence": f"{strongest_platform['mention_rate'] * 100:.1f}% mention rate" if strongest_platform is not None else "n/a",
                },
                {
                    "question": "What should source competition tracking follow?",
                    "answer": ", ".join(top_non_oecd["domain"].head(3).tolist()) if not top_non_oecd.empty else "n/a",
                    "evidence": "Top recurring non-OECD citation domains",
                },
            ]
        )
        render_table(monitoring)

    st.markdown("### Method caveats")
    st.markdown(
        """
        - This dashboard reflects a controlled prompt set, not organic user logs.
        - Coverage is limited to unbranded prompts, the United States, and 13-19 July 2026.
        - Platform outputs are volatile and should be rechecked over time.
        - Visibility, citation and position are useful proxies, but they are not direct measures of trust, behavioural impact or policy influence.
        """
    )
    st.caption(
        source_line(
            "OECD workbook validated note",
            "Writesonic: Platform Behavior & Volatility",
            "Writesonic: Why We Monitor Real AI Platforms, Not Just APIs",
            "Reuters Institute Digital News Report 2026",
            "JRC Generative AI outlook report",
        )
    )


def render_footer() -> None:
    st.markdown("### References used in the dashboard")
    for item in REFERENCE_NOTES:
        lines = [
            f"<div class='reference-title'>{item['title']}</div>",
            f"<div class='reference-line'><strong>Used for:</strong> {item['use']}</div>",
            f"<div class='reference-line'><strong>File:</strong> <code>{item['path'].relative_to(ROOT)}</code></div>",
            f"<div class='reference-line'><strong>APA:</strong> {item['apa']}</div>",
        ]
        if item["url"]:
            lines.append(
                f"<div class='reference-line'><strong>URL:</strong> <a href='{item['url']}' target='_blank'>{item['url']}</a></div>"
            )
        st.markdown(
            "<div class='reference-card'>" + "".join(lines) + "</div>",
            unsafe_allow_html=True,
        )


def main() -> None:
    st.set_page_config(
        page_title="OECD Visibility Dashboard",
        page_icon="📊",
        layout="wide",
    )
    inject_css()

    if not WORKBOOK_PATH.exists():
        st.error(f"Workbook not found: {WORKBOOK_PATH}")
        st.stop()

    df = load_workbook(str(WORKBOOK_PATH))
    render_header(df)
    filtered = render_sidebar(df)

    if filtered.empty:
        st.warning("No rows match the current filter set.")
        st.stop()

    tabs = st.tabs(
        [
            "Executive summary",
            "Data analysis",
            "Platform diagnostics",
            "Prompt evidence",
            "Recommendations",
        ]
    )

    with tabs[0]:
        render_summary_tab(filtered)
    with tabs[1]:
        render_data_analysis_tab(filtered)
    with tabs[2]:
        render_platform_diagnostics_tab(filtered)
    with tabs[3]:
        render_prompt_evidence_tab(filtered)
    with tabs[4]:
        render_recommendations_tab(filtered)

    render_footer()


if __name__ == "__main__":
    main()
