# OECD visibility dashboard: rationale and source basis

## What was built

A new Streamlit dashboard was created in [streamlit_app.py](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/streamlit_app.py). It replaces the previous document-browser approach with a focused analytical product built around the OECD workbook supplied for the written assessment.

The dashboard is structured to support the output logic requested in the original assessment brief:

- executive summary
- data analysis
- LLM visibility research
- recommendations

Source: [original-written-assessment-instructions.md](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Assesment/Assesment%20instructions/original-written-assessment-instructions.md)

## Why the dashboard is structured this way

### 1. Executive summary

The first view concentrates the headline signals into a short set of metrics and one prioritisation visual. This mirrors the assessment requirement to begin with a clear management summary rather than a technical walkthrough. It is designed to answer three questions quickly:

- how visible the OECD is overall
- where the largest visibility gap sits
- whether visibility is translating into direct OECD citation

This follows the evidence-led logic used in OECD publications and the OECD Style Guide: lead with the finding, keep the wording plain, and make the source basis explicit.

Sources:

- [OECD Style Guide (Fourth Edition) - 2025.pdf](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Research/OECD%20Tone%20Of%20Voice/OECD%20Style%20Guide%20(Fourth%20Edition)%20-%202025.pdf)
- [contrast-between-oecd-workbook-and-writesonic-documentation.md](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Assesment/Assesment%20instructions/contrast-between-oecd-workbook-and-writesonic-documentation.md)

### 2. Data analysis

The second view expands the evidence base. It shows topic performance, platform comparison, daily stability, and the citation ecosystem. This was included because the workbook is not a finished KPI report; it is a prompt-level monitoring dataset. The dashboard therefore had to aggregate the rows into interpretable management views.

The topic and platform sections respond directly to the analytical uses implied by the workbook:

- where OECD is more or less visible
- how visibility differs by platform
- what source competition looks like
- whether patterns are stable across the monitoring window

Sources:

- [contrast-between-oecd-workbook-and-writesonic-documentation.md](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Assesment/Assesment%20instructions/contrast-between-oecd-workbook-and-writesonic-documentation.md)
- [Answer Engine Insights Overview _ Profound Knowledge Base.pdf](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Research/Profound/Answer%20Engine%20Insights%20Overview%20_%20Profound%20Knowledge%20Base.pdf)
- [Profound glossary _ Profound Knowledge Base.pdf](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Research/Profound/Profound%20glossary%20_%20Profound%20Knowledge%20Base.pdf)

### 2.1 Additional KPIs and diagnostics added from the wider research base

Beyond the indicators explicitly required by the assessment brief, the dashboard was extended with three additional KPIs and two extra diagnostics charts. These additions were chosen because they are conceptually supported by the wider `General LLM Research` corpus and can still be calculated directly from the workbook without introducing unsupported traffic or bot claims.

The added KPIs are:

- mention-to-citation conversion
- top-5 non-OECD source concentration
- average cross-platform spread

The added charts are:

- a topic-level mention-versus-citation chart
- a topic-level cross-platform spread chart

These additions matter for five reasons:

- the literature repeatedly distinguishes visibility from attribution, so it is useful to know whether OECD is merely mentioned or actually cited as the evidentiary source
- citation competition is a core part of AI-mediated discoverability, which justifies measuring how concentrated non-OECD source capture is
- platform heterogeneity is a recurring finding, so a spread measure is more informative than a single average
- the zero-click and answer-engine literature implies that presence in AI outputs can matter even when direct referral or behavioural attribution is incomplete
- the workbook itself is a controlled prompt-monitoring file, so the defensible way to extend it is through better proxy diagnostics, not by pretending it contains web traffic or audience data

The additional KPI layer therefore stays inside the bounds of the available data while making the analysis more aligned with current research on AI discoverability, answer-engine citation behaviour, and platform-specific mediation.

Sources:

- [DNR 2026 FINAL_2.pdf](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Things%20to%20prepare/General%20LLM%20Research/changes%20in%20the%20media%20landscape/country%20and%20regional%20media%20landscapes/DNR%202026%20FINAL_2.pdf)
- [JRC142598_01.pdf](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Things%20to%20prepare/General%20LLM%20Research/changes%20in%20the%20media%20landscape/AI%20adoption%20and%20usage%20trends/JRC142598_01.pdf)
- [Generative AI models love to cite Reuters and Axios, study finds _ Nieman Journalism Lab.pdf](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Things%20to%20prepare/General%20LLM%20Research/generative%20search%20visibility/citation%20or%20mention%20checks%20in%20AI%20outputs/Generative%20AI%20models%20love%20to%20cite%20Reuters%20and%20Axios,%20study%20finds%20_%20Nieman%20Journalism%20Lab.pdf)
- [Platform Behavior & Volatility.pdf](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Research/Writesonic/Platform%20Behavior%20%26%20Volatility.pdf)
- [Why We Monitor Real AI Platforms, Not Just APIs.pdf](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Research/Writesonic/Why%20We%20Monitor%20Real%20AI%20Platforms,%20Not%20Just%20APIs.pdf)

### 3. Platform diagnostics

The heatmap and weakest topic-platform combinations were added because the research corpus repeatedly indicates that AI answer surfaces should not be treated as interchangeable. Platform behaviour is volatile, monitoring should rely on real surfaces rather than API-only outputs, and prompt-level visibility must be interpreted comparatively.

This view therefore helps isolate:

- cross-platform asymmetries
- persistent weak spots by topic
- where monitoring should remain platform-specific

Sources:

- [Platform Behavior & Volatility.pdf](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Research/Writesonic/Platform%20Behavior%20%26%20Volatility.pdf)
- [Why We Monitor Real AI Platforms, Not Just APIs.pdf](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Research/Writesonic/Why%20We%20Monitor%20Real%20AI%20Platforms,%20Not%20Just%20APIs.pdf)
- [Prompts vs Keywords [Very Important].pdf](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Research/Writesonic/Prompts%20vs%20Keywords%20%5BVery%20Important%5D.pdf)

### 4. Prompt evidence

The prompt-level inspection panel was included because the workbook is row-level evidence. A management dashboard alone is not enough; the user also needs to verify what a platform actually answered, whether OECD was mentioned, and which sources were cited.

This section makes the evidence auditable by keeping the following visible for each selected row:

- exact prompt
- generated response
- extracted mentions
- cited URLs and domains

That approach is consistent with the monitoring logic described in the Profound material and with the workbook’s own structure.

Sources:

- [Answer Engine Insights Overview _ Profound Knowledge Base.pdf](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Research/Profound/Answer%20Engine%20Insights%20Overview%20_%20Profound%20Knowledge%20Base.pdf)
- [contrast-between-oecd-workbook-and-writesonic-documentation.md](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Assesment/Assesment%20instructions/contrast-between-oecd-workbook-and-writesonic-documentation.md)

### 5. Recommendations

The recommendations section converts the monitored evidence into an action frame. It focuses on the areas where the data is most decision-useful:

- high-volume, low-visibility topics
- the difference between mention visibility and direct OECD citation
- the need for repeated monitoring because outputs are volatile
- the need to treat visibility as a proxy rather than as a measure of impact

This is aligned with the assessment brief, which explicitly asks for recommendations, and with the broader research corpus, which cautions against overstating what monitored answer-engine outputs can prove on their own.

Sources:

- [original-written-assessment-instructions.md](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Assesment/Assesment%20instructions/original-written-assessment-instructions.md)
- [Platform Behavior & Volatility.pdf](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Research/Writesonic/Platform%20Behavior%20%26%20Volatility.pdf)
- [Why We Monitor Real AI Platforms, Not Just APIs.pdf](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Research/Writesonic/Why%20We%20Monitor%20Real%20AI%20Platforms,%20Not%20Just%20APIs.pdf)

## Why the tone and display were kept compact

The interface was intentionally reduced to short labels, sentence-case headings, compact source notes, and charts that carry most of the narrative load. This was done for three reasons:

- the OECD style material favours clarity, plain language, and evidence-first presentation
- the workbook is already dense, so the interface should remove friction rather than add more explanation
- the brief requires analytical judgement, not a generic “data room”

Sources:

- [OECD Style Guide (Fourth Edition) - 2025.pdf](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Research/OECD%20Tone%20Of%20Voice/OECD%20Style%20Guide%20(Fourth%20Edition)%20-%202025.pdf)
- [oecd-tone-of-voice-manual.md](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Research/OECD%20Tone%20Of%20Voice/oecd-tone-of-voice-manual.md)

## Why the analysis uses these caveats

The dashboard keeps caveats visible because the workbook measures controlled prompt monitoring, not organic behaviour. That distinction matters. The supporting research indicates that AI visibility should be interpreted as directional intelligence and that platform outputs are unstable over time. It also suggests that citation competition matters, because surfaced sources can shape discoverability and authority even where attribution is incomplete.

Sources:

- [contrast-between-oecd-workbook-and-writesonic-documentation.md](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Assesment/Assesment%20instructions/contrast-between-oecd-workbook-and-writesonic-documentation.md)
- [DNR 2026 FINAL_2.pdf](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Things%20to%20prepare/General%20LLM%20Research/changes%20in%20the%20media%20landscape/country%20and%20regional%20media%20landscapes/DNR%202026%20FINAL_2.pdf)
- [JRC142598_01.pdf](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Things%20to%20prepare/General%20LLM%20Research/changes%20in%20the%20media%20landscape/AI%20adoption%20and%20usage%20trends/JRC142598_01.pdf)
- [Generative AI models love to cite Reuters and Axios, study finds _ Nieman Journalism Lab.pdf](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Things%20to%20prepare/General%20LLM%20Research/generative%20search%20visibility/citation%20or%20mention%20checks%20in%20AI%20outputs/Generative%20AI%20models%20love%20to%20cite%20Reuters%20and%20Axios,%20study%20finds%20_%20Nieman%20Journalism%20Lab.pdf)

## Files created or updated

- [streamlit_app.py](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/streamlit_app.py)
- [requirements.txt](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/requirements.txt)
- [dashboard-rationale-and-references.md](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Assesment/dashboard-rationale-and-references.md)
