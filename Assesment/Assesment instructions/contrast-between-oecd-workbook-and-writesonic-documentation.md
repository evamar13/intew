# OECD Workbook: Source-Validated Dataset Note

## Scope

This note explains the OECD assessment workbook `tiny_mce_3d2e5fe2-264a-4209-92c3-464559e5dbf3_Excel File supporting document_Question1_Junior AI & Communication Officer REF3112J.xlsx` using the workbook itself and the platform documentation available in the Profound and Writesonic research folders.

## What the workbook contains

The workbook is a **prompt-level AI answer monitoring export** used to assess OECD visibility across AI answer platforms.

Its structure is:

- `1` sheet: `Prompts in LLMs`
- `12,871` data rows
- `50` columns
- a short preamble in rows `1-3`
- the actual header row starting on row `4`

The preamble states:

- `Filter: 13-19 July, Unbranded prompts only`
- `Source: Profound, automatically prompts LLM platforms with specific prompts defined by the OECD`

The workbook is therefore a structured monitoring export, not a general OECD communications dashboard.

## What one row represents

Each row represents one observed response instance:

- one prompt
- on one date
- in one platform
- for one topic
- with one resulting answer and its related metadata

This is row-level evidence rather than an already-aggregated KPI report.

## Core fields

The main fields are:

- `run_id`: unique identifier for the observation
- `date`: date of execution
- `platform`: AI platform tested
- `topic`: OECD policy topic linked to the prompt
- `tags`: prompt classification labels
- `region`: market field; in this export it is always `United States`
- `type`: analysis label, primarily visibility and in some cases sentiment
- `prompt`: exact prompt sent to the answer engine
- `mentions`: detected brand or entity references in the answer
- `normalized_mentions`: cleaned or standardised version of the mentions field
- `position`: ranked placement field
- `response`: generated answer text
- `search_queries`: auxiliary field, frequently empty
- `mentioned?`: binary result, `Yes` or `No`
- `citation_1` to `citation_36`: URLs or webpages cited in the answer

## Platform coverage

The dataset covers `6` platforms:

- `Google AI Overviews`
- `ChatGPT`
- `Google Gemini`
- `Microsoft Copilot`
- `Perplexity`
- `Google AI Mode`

Most platforms contain `2,149` rows each. `Google AI Mode` contains `2,126`.

## Topic coverage

The export includes `22` OECD-related topics. The largest is:

- `Employment and Labour Markets` with `3,143` rows

Other large topics include:

- `ODA and Development Finance`
- `Tax and Revenue Statistics`
- `PISA and Education Performance`
- `Health System Performance`
- `Better Life Index and Wellbeing`
- `Social Expenditure and Inequality`
- `Migration and Integration`
- `Research, Development and Innovation`
- `Economy and Growth`

The workbook is broad across OECD policy areas rather than tied to a single product or publication line.

## Time coverage

The dataset covers `7` days:

- `2026-07-13`
- `2026-07-14`
- `2026-07-15`
- `2026-07-16`
- `2026-07-17`
- `2026-07-18`
- `2026-07-19`

Most days contain `1,842` observations. `2026-07-14` contains `1,819`.

## Validated interpretation of the dataset

The workbook should be interpreted as a **Profound Answer Engine Insights-style export** that captures how the OECD performs across AI answer engines through recurring prompt executions.

This interpretation is supported by the workbook preamble and by Profound documentation stating that:

- prompts are queries Profound automatically sends to answer engines on a daily basis
- each response is captured as a data point
- prompts are organized into topics
- tags provide an additional classification layer
- exports can contain prompts, AI responses, mentions, sentiment, and related metrics

The Writesonic documentation supports the same broad operating model: prompts rather than SEO keywords, answer-level monitoring, and separate treatment of visibility, mentions, citations, sentiment, and platform differences.

## Meaning of the main analytical concepts

### Visibility

Visibility should be read as an **answer-level presence/absence concept**. The OECD either appears in a given AI answer or it does not.

At an aggregated level, visibility can then be expressed as a percentage. Profound documentation defines visibility as a binary metric and describes visibility score as the proportion of relevant responses in which the brand appears.

This means:

- the workbook does not directly contain a final dashboard visibility score
- the workbook contains the row-level evidence needed to calculate visibility by platform, topic, prompt subset, or time period

### Mentions

The workbook tracks mentions separately from citations.

The most defensible interpretation is:

- `mentions` captures raw extracted references to brands or entities in the answer
- `normalized_mentions` standardises those references into a cleaned form

This reading is consistent with Profound’s definitions of mentions, data cleansing, and answer-level brand analysis, although the exact transformation logic is not described field by field in the reviewed materials.

### Citations

Citations are a distinct analytical layer from mentions.

In both Profound and Writesonic documentation, citations are defined as webpages, articles, or resources referenced in answer-engine outputs. In this workbook, the citation columns therefore represent substantive evidence about:

- which sources answer engines rely on
- whether OECD pages are used directly as source material
- which external domains shape OECD-relevant AI answers

### Position

`position` should be treated cautiously.

The field clearly behaves like a ranked placement indicator. However, the Profound documentation defines **Position** as a comparative performance concept derived from broader indicators such as share of voice, rather than simply literal order of mention in a single answer.

The safest interpretation is:

- `position` is a ranked placement field
- it is not a traditional search ranking
- it should not be assumed to mean literal in-answer mention order unless separately confirmed by export-specific documentation

### Region

The export shows only `United States` in the `region` field.

The most defensible interpretation is that the file reflects a **single configured market**. Language may have been fixed in the underlying configuration and omitted from the export.

### Type

The `type` field includes:

- `Visibility`
- `Sentiment, Visibility`
- `Visibility, Sentiment`

The documentation confirms that visibility and sentiment are separate analytical dimensions. The field should therefore be treated as an analysis label indicating which dimensions were attached to the record, without overinterpreting the exact encoding.

## Observed field behavior

The workbook shows:

- `mentioned? = Yes` in `8,389` rows
- `mentioned? = No` in `4,482` rows

So the OECD appears in roughly two-thirds of the tested prompt-platform cases.

Other field behavior:

- `response` is populated in `12,837` rows
- `mentions` and `normalized_mentions` are populated in `11,071` rows
- `citation_1` is populated in `10,632` rows
- average citations per row: `6.62`
- maximum citations in one row: `36`

The workbook is therefore useful not only for visibility analysis but also for citation and source-ecosystem analysis.

## Initial analysis of the workbook data

The figures below are calculated directly from the workbook export. They should be interpreted as **observed row-level mention rates within this dataset**, not as official dashboard-level visibility scores unless recalculated according to the source platform’s exact reporting logic.

### Overall OECD presence

Across all `12,871` observed response rows:

- the OECD is marked as mentioned in `8,389` rows
- the OECD is not mentioned in `4,482` rows
- the observed OECD mention rate across all rows is `65.18%`

This indicates that, within this monitored prompt set, the OECD appears in roughly two-thirds of the tested AI-answer instances.

| Metric | Value |
| --- | ---: |
| Total rows | 12,871 |
| Rows where OECD is mentioned | 8,389 |
| Rows where OECD is not mentioned | 4,482 |
| Observed OECD mention rate | 65.18% |

### Platform-level pattern

Observed OECD mention rate by platform:

- `ChatGPT`: `69.89%` (`1,502/2,149`)
- `Google AI Overviews`: `69.29%` (`1,489/2,149`)
- `Google Gemini`: `65.75%` (`1,413/2,149`)
- `Google AI Mode`: `63.26%` (`1,345/2,126`)
- `Perplexity`: `62.77%` (`1,349/2,149`)
- `Microsoft Copilot`: `60.07%` (`1,291/2,149`)

This suggests three broad tiers in the monitored period:

- strongest observed OECD presence in `ChatGPT` and `Google AI Overviews`
- middle performance in `Google Gemini`, `Google AI Mode`, and `Perplexity`
- weakest observed OECD presence in `Microsoft Copilot`

| Platform | Rows | Rows with OECD mention | Observed mention rate |
| --- | ---: | ---: | ---: |
| ChatGPT | 2,149 | 1,502 | 69.89% |
| Google AI Overviews | 2,149 | 1,489 | 69.29% |
| Google Gemini | 2,149 | 1,413 | 65.75% |
| Google AI Mode | 2,126 | 1,345 | 63.26% |
| Perplexity | 2,149 | 1,349 | 62.77% |
| Microsoft Copilot | 2,149 | 1,291 | 60.07% |

### Topic-level pattern

The workbook is not evenly favorable to the OECD across topics.

Highest observed OECD mention rates among topics with at least `200` rows:

- `Tax and Revenue Statistics`: `92.43%`
- `Structural Reform and Productivity`: `92.34%`
- `PISA and Education Performance`: `88.51%`
- `Artificial Intelligence and Digital`: `88.10%`
- `Social Expenditure and Inequality`: `83.15%`
- `Public Governance`: `82.69%`
- `ODA and Development Finance`: `81.73%`
- `Health System Performance`: `80.42%`

Lowest observed OECD mention rates among topics with at least `200` rows:

- `Employment and Labour Markets`: `39.90%`
- `FDI and International Investment`: `41.99%`
- `Climate and Environment`: `43.57%`
- `Financial Markets and Investment`: `46.63%`
- `Environment (General)`: `47.14%`
- `Macroeconomic Benchmarks`: `53.81%`
- `Better Life Index and Wellbeing`: `54.85%`
- `Research, Development and Innovation`: `63.10%`

This pattern suggests that OECD visibility is strongest where the OECD has long-established statistical or comparative authority and weaker in areas where answer engines appear to rely more heavily on alternative institutional, academic, or market sources.

| Highest-volume / highest-strength topics | Rows | Rows with OECD mention | Observed mention rate |
| --- | ---: | ---: | ---: |
| Tax and Revenue Statistics | 964 | 891 | 92.43% |
| Structural Reform and Productivity | 209 | 193 | 92.34% |
| PISA and Education Performance | 879 | 778 | 88.51% |
| Artificial Intelligence and Digital | 252 | 222 | 88.10% |
| Social Expenditure and Inequality | 546 | 454 | 83.15% |
| Public Governance | 335 | 277 | 82.69% |
| ODA and Development Finance | 1,007 | 823 | 81.73% |
| Health System Performance | 669 | 538 | 80.42% |

| Lowest-volume / weakest large topics | Rows | Rows with OECD mention | Observed mention rate |
| --- | ---: | ---: | ---: |
| Employment and Labour Markets | 3,143 | 1,254 | 39.90% |
| FDI and International Investment | 462 | 194 | 41.99% |
| Climate and Environment | 420 | 183 | 43.57% |
| Financial Markets and Investment | 208 | 97 | 46.63% |
| Environment (General) | 210 | 99 | 47.14% |
| Macroeconomic Benchmarks | 210 | 113 | 53.81% |
| Better Life Index and Wellbeing | 629 | 345 | 54.85% |
| Research, Development and Innovation | 504 | 318 | 63.10% |

### The largest topic is also the weakest

`Employment and Labour Markets` is the largest topic in the workbook with `3,143` rows, but it also shows the weakest observed OECD mention rate among high-volume topics: `39.90%`.

This is analytically important because:

- it is a major topic in the dataset
- it materially drags down the OECD’s overall observed presence
- it suggests a substantial visibility gap in a domain where many competing sources are also highly active

### Stability over time

Observed OECD mention rate by day:

- `2026-07-13`: `63.57%`
- `2026-07-14`: `65.42%`
- `2026-07-15`: `64.88%`
- `2026-07-16`: `64.33%`
- `2026-07-17`: `66.99%`
- `2026-07-18`: `65.09%`
- `2026-07-19`: `65.96%`

The daily range is relatively narrow. Within this short window, the dataset suggests moderate day-to-day stability rather than sharp volatility in overall OECD presence.

| Date | Rows | Rows with OECD mention | Observed mention rate |
| --- | ---: | ---: | ---: |
| 2026-07-13 | 1,842 | 1,171 | 63.57% |
| 2026-07-14 | 1,819 | 1,190 | 65.42% |
| 2026-07-15 | 1,842 | 1,195 | 64.88% |
| 2026-07-16 | 1,842 | 1,185 | 64.33% |
| 2026-07-17 | 1,842 | 1,234 | 66.99% |
| 2026-07-18 | 1,842 | 1,199 | 65.09% |
| 2026-07-19 | 1,842 | 1,215 | 65.96% |

### Platform-topic extremes

The strongest and weakest observed combinations help identify where OECD visibility is concentrated or missing:

- `ChatGPT` performs especially strongly in `Tax and Revenue Statistics` (`96.27%`)
- `Google Gemini` performs especially strongly in `PISA and Education Performance` (`96.60%`)
- `Google AI Mode` performs especially strongly in `Tax and Revenue Statistics` (`94.97%`)
- `Perplexity` performs especially strongly in `Health System Performance` (`87.50%`)

By contrast, `Employment and Labour Markets` is the weakest topic in nearly every platform-level breakdown reviewed:

- `ChatGPT`: `35.62%`
- `Google Gemini`: `32.00%`
- `Microsoft Copilot`: `36.95%`
- `Perplexity`: `36.19%`
- `Google AI Mode`: `43.24%`

This indicates that the weakness in employment-related prompts is systemic across platforms rather than platform-specific.

| Platform | Strongest topic in reviewed high-volume combinations | Rate | Weakest topic in reviewed high-volume combinations | Rate |
| --- | --- | ---: | --- | ---: |
| ChatGPT | Tax and Revenue Statistics | 96.27% | Employment and Labour Markets | 35.62% |
| Google AI Overviews | PISA and Education Performance | 93.88% | Better Life Index and Wellbeing | 48.57% |
| Google Gemini | PISA and Education Performance | 96.60% | Employment and Labour Markets | 32.00% |
| Microsoft Copilot | Tax and Revenue Statistics | 88.20% | Employment and Labour Markets | 36.95% |
| Perplexity | Health System Performance | 87.50% | Employment and Labour Markets | 36.19% |
| Google AI Mode | Tax and Revenue Statistics | 94.97% | Employment and Labour Markets | 43.24% |

### Citation ecosystem

The most frequently cited domains in the workbook overall are:

- `oecd.org`
- `sciencedirect.com`
- `pmc.ncbi.nlm.nih.gov`
- `youtube.com`
- `ourworldindata.org`
- `unctad.org`
- `imf.org`
- `en.wikipedia.org`
- `ec.europa.eu`
- `taxfoundation.org`

This indicates that OECD content does appear prominently in the citation ecosystem, but answer engines also draw heavily on:

- academic publishers
- public research repositories
- multilateral institutions
- statistical and policy explainer sites
- video and open-web sources

| Most frequently cited domains overall | Citation occurrences |
| --- | ---: |
| oecd.org | 12,229 |
| sciencedirect.com | 2,066 |
| pmc.ncbi.nlm.nih.gov | 2,013 |
| youtube.com | 1,265 |
| ourworldindata.org | 1,256 |
| unctad.org | 1,192 |
| imf.org | 1,192 |
| en.wikipedia.org | 1,027 |
| ec.europa.eu | 1,005 |
| taxfoundation.org | 942 |

### OECD citation performance

Rows containing at least one OECD citation (`oecd.org` or `oecd.ai`):

- `5,508` out of `12,871` rows (`42.79%`)

Rows where the OECD is mentioned and also cited:

- `5,054` out of `8,389` OECD-mentioned rows (`60.25%`)

This matters because the OECD is often mentioned without an OECD webpage being cited directly. In other words:

- mention presence is stronger than direct source citation
- some AI answers refer to OECD findings or authority while grounding the answer in non-OECD sources

| OECD citation indicator | Value |
| --- | ---: |
| Rows with at least one OECD citation (`oecd.org` or `oecd.ai`) | 5,508 |
| Share of all rows with at least one OECD citation | 42.79% |
| Rows where OECD is both mentioned and cited | 5,054 |
| Share of OECD-mentioned rows that also cite an OECD domain | 60.25% |

### Source competition when the OECD is absent

When the OECD is not mentioned, the most common cited domains include:

- `sciencedirect.com`
- `pmc.ncbi.nlm.nih.gov`
- `unctad.org`
- `youtube.com`
- `ourworldindata.org`
- `brookings.edu`
- `imf.org`
- `nber.org`
- `ec.europa.eu`
- `academic.oup.com`

This suggests that the OECD’s main competition in the monitored answer environment is not only other intergovernmental organisations. It also includes:

- academic journal ecosystems
- public-research repositories
- think tanks
- open educational sources
- explainers and secondary interpretation sites

| Most common cited domains when OECD is not mentioned | Citation occurrences |
| --- | ---: |
| sciencedirect.com | 981 |
| pmc.ncbi.nlm.nih.gov | 714 |
| oecd.org | 712 |
| unctad.org | 478 |
| youtube.com | 472 |
| ourworldindata.org | 393 |
| brookings.edu | 378 |
| imf.org | 351 |
| nber.org | 327 |
| ec.europa.eu | 311 |

### Main analytical implications from the dataset

The workbook points to five main implications:

1. The OECD has substantial observed presence overall, but that presence is uneven across platforms and topics.
2. The OECD is particularly strong in tax, education performance, governance, development finance, and health-related topics.
3. The largest visibility gap appears in `Employment and Labour Markets`, with additional weaknesses in environment, investment, and macroeconomic benchmark topics.
4. OECD mention presence is materially stronger than direct OECD citation presence, which suggests an opportunity to strengthen source-level reliance on OECD pages.
5. The competitive source environment is diverse and includes academic, multilateral, public-sector, and open-web sources, not just direct institutional peers.

## What the dataset can support analytically

The file can support analysis of questions such as:

- whether the OECD is mentioned for a given prompt
- in which platforms the OECD is more or less visible
- in which topics the OECD is more or less visible
- when the OECD is present, how it performs relative to other brands or sources
- which external sources are cited in OECD-relevant answers
- where citation gaps or source opportunities may exist

## What the dataset is not

The workbook is not:

- website traffic data
- bot log data
- observed user clickstream data
- a direct measure of OECD audience behavior
- a causal measure of OECD influence in AI systems

It is a controlled monitoring export based on scripted prompts. It is therefore strong for comparative directional analysis but limited for claims about actual user exposure or impact.

## Reading guidance

The correct reading is:

- this is a comparative AI-answer visibility dataset
- it is useful for identifying relative strengths and weaknesses by platform, topic, and prompt set
- it supports citation and source-competition analysis
- it supports directional inference rather than definitive audience-impact claims

## Main caveats

The main caveats are:

- `United States` only
- `unbranded prompts only`
- short observation window: `13-19 July 2026`
- one monitoring provider: `Profound`
- platform responses are volatile and can change quickly
- visibility does not necessarily equal trust, influence, usage, or policy impact
- some fields, especially `position`, `type`, and `search_queries`, remain underdefined at export level

## Recommended wording for the assessment

> The supporting workbook is a prompt-level monitoring export covering unbranded OECD-relevant queries run across multiple AI answer platforms between 13 and 19 July 2026 in the United States. Each row captures an individual response instance, including the prompt, platform, topic, generated answer, whether the OECD was mentioned, and the cited sources. The file should therefore be treated as a structured AI-answer visibility dataset rather than as web traffic or user-behavior data.

## References

OECD assessment workbook, `tiny_mce_3d2e5fe2-264a-4209-92c3-464559e5dbf3_Excel File supporting document_Question1_Junior AI & Communication Officer REF3112J.xlsx`, preamble and tabular structure reviewed on 12 August 2026.

Profound Knowledge Base (2026), *Answer Engine Insights Overview*, accessed 12 August 2026.

Profound Knowledge Base (2026), *How to create topics and prompts to track in Profound*, accessed 12 August 2026.

Profound Knowledge Base (2026), *Profound glossary*, accessed 12 August 2026.

Profound Documentation (2026), *About Agent Analytics*, accessed 12 August 2026.

Writesonic Documentation (2026), *AI Search Vocabulary & Metrics [Very Important]*, accessed 12 August 2026.

Writesonic Documentation (2026), *Prompts vs Keywords [Very Important]*, accessed 12 August 2026.

Writesonic Documentation (2026), *All Prompts and Answers*, accessed 12 August 2026.

Writesonic Documentation (2026), *All Citations*, accessed 12 August 2026.

Writesonic Documentation (2026), *Overview: Platforms*, accessed 12 August 2026.
