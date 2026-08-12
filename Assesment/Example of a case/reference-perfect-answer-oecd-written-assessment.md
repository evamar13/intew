# Reference Model Answer For A Hypothetical OECD Written Assessment

## Important Note

This is **not** a real OECD question and **not** a prediction of your exact case.

It is a reference answer built from the inferred evaluation model in [likely-evaluation-model-oecd-written-assessment.md](/Users/evadelmarperez/Library/CloudStorage/OneDrive-PUIG/Python%20projects/Personal/intew/Assesment/Example%20of%20a%20case/likely-evaluation-model-oecd-written-assessment.md).

The aim is to show what a **high-scoring written answer** could look like when the exercise is:

- analytical rather than generic
- based on a small data annex
- relevant to COM's actual monitoring work
- focused on interpretation, caveats, and action

## Refined Hypothetical Prompt

**You have joined the Communications Impact Unit in the Directorate for Communications. Four weeks ago, the OECD published a flagship report with a statistical release, press outreach, website assets and social distribution linked to a priority policy theme. The Head of Unit asks you to prepare a short internal note for management based on the annexed data.**

**Your note should:**

- identify the main performance findings
- distinguish meaningful signals from noise
- explain any anomalies or data-quality concerns
- assess visibility and influence across digital, media, policy and AI-mediated environments
- recommend how COM should adjust its monitoring, dashboard reporting and media-briefing approach over the next two months

## Annex: simplified data pack

### Table 1. Weekly performance, first four weeks after launch

| Metric | Week 1 | Week 2 | Week 3 | Week 4 |
| --- | ---: | ---: | ---: | ---: |
| Total pageviews to release assets | 84,000 | 71,500 | 49,200 | 43,800 |
| Estimated human pageviews | 70,000 | 46,000 | 39,000 | 35,000 |
| Estimated automated pageviews | 14,000 | 25,500 | 10,200 | 8,800 |
| Publication downloads | 12,400 | 8,900 | 7,600 | 7,200 |
| Average engaged time on summary page | 2m 48s | 2m 31s | 2m 54s | 3m 02s |
| Media mentions | 318 | 146 | 89 | 72 |
| Share of media coverage rated accurate | 86% | 84% | 79% | 77% |
| Mentions in official policy or institutional documents | 3 | 7 | 14 | 19 |
| New academic mentions captured | 1 | 3 | 7 | 11 |
| Identifiable referrals from known AI surfaces | 420 | 510 | 690 | 760 |
| Manual AI output checks with correct attribution | 7/12 | 8/12 | 7/12 | 8/12 |
| Manual AI output checks with material factual simplification or caveat loss | 2/12 | 2/12 | 3/12 | 3/12 |

### Table 2. Asset-level performance over the four-week period

| Asset | Total pageviews | Estimated human share | Downloads / click-through | Avg engaged time | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| Main report landing page | 92,000 | 68% | 19% | 1m 42s | Strong launch traffic, high volatility |
| Executive summary page | 61,000 | 84% | 24% | 3m 06s | Best engagement quality |
| Interactive chart page | 54,000 | 41% | 6% | 0m 51s | High automated traffic |
| Press release page | 28,000 | 79% | 9% | 1m 18s | Strong first-week media utility |
| Methodology/statistical notes page | 17,500 | 88% | 31% | 4m 11s | Lower reach, high-value use |

### Table 3. Selected crawler and traffic observations

| Observation | Finding |
| --- | --- |
| Week 2 spike in automated pageviews | Concentrated on interactive chart page and two image assets |
| Main automated user agents identified | Search engine crawlers, known AI crawlers, some unattributed scraping activity |
| Geographic distribution of suspicious traffic | Disproportionately concentrated in a small set of locations not aligned with normal OECD audience profile |
| AI-related referrals | Mostly to executive summary and methodology pages, not to the interactive chart page |
| Caching and answer-layer effects | In several manual checks, AI systems reproduced key OECD findings without generating a visible referral or link back to the original page |

### Table 4. Sampled qualitative findings from AI output checks

| Platform check summary | Finding |
| --- | --- |
| OECD cited by name | Frequent but not consistent |
| Link to OECD source included | More common in some interfaces than others |
| Statistical caveats preserved | Often partially lost |
| Summary quality | Generally acceptable at headline level, weaker on methodology and nuance |

### Table 5. Reporting and briefing constraints

| Item | Finding |
| --- | --- |
| Current management dashboard | Focuses on total traffic, downloads, media mentions and social reach; AI-related indicators are not yet integrated |
| Data quality issue | Bot and crawler traffic are not consistently separated from validated human traffic in the top-line dashboard view |
| Upcoming need | A short media brief is required next week for a senior OECD mission related to the same policy theme |
| Analyst request | Management wants two or three indicators that could be piloted in Power BI without overstating precision |

---

## Model Answer

### Internal note: first four weeks of performance for flagship OECD release

#### Summary

The release achieved strong initial reach, but the more policy-relevant result is that qualified use and institutional uptake are proving more resilient than raw traffic. The data also point to three cautions that should shape interpretation. First, a material share of volume, especially in Week 2, is automated and should not be read as audience demand. Second, the highest-value assets are not the highest-volume ones. Third, AI-mediated visibility appears to be increasing, but direct referrals alone are likely to understate total influence because generative interfaces can intermediate access to source content without returning a measurable click, and they do not always preserve attribution or nuance consistently (Kuai et al., 2026; Couraceiro and Pais, 2026; Lucchi, 2026).

This pattern is consistent with a broader shift in the information environment. Research on generative search, zero-click consumption and document-grounded question answering suggests that source material is increasingly being retrieved, synthesised and reformulated before users encounter it, which means that visibility, traffic and faithful representation can no longer be assumed to move together (Faridi et al., 2026; Sharma et al., 2026). For a public-interest institution, that implies that impact monitoring should combine traditional communications indicators with a more explicit assessment of how OECD content is surfaced, attributed and simplified in AI-mediated environments (OECD, 2021; OECD, 2024a; OECD, 2025a).

### 1. Main findings from the first four weeks

The first finding is that launch visibility was high, but not all of that visibility reflects equivalent value. Total pageviews fall from 84 000 in Week 1 to 43 800 in Week 4, which is a normal post-launch pattern. However, Week 2 is clearly distorted by automation: automated pageviews rise to 25 500 and are concentrated on the interactive chart page and image assets. That spike should therefore be treated as machine access rather than as evidence of sustained audience interest.

The second finding is that higher-value use holds up better than top-line traffic. Downloads decline more slowly than pageviews, from 12 400 to 7 200, while engaged time on the executive summary page improves by Week 4. This suggests that broad curiosity fades after launch, but the remaining audience is more likely to be purposeful and willing to spend time with the substance of the output.

The third finding is that the strongest assets in quality terms are the executive summary and the methodology page. The executive summary combines an 84% human share with strong engagement. The methodology page has lower reach, but it records the highest engagement depth and the strongest download or click-through behaviour. For OECD, that is an important result because it indicates demand for interpretive clarity and methodological grounding, not only for headline messages. It also suggests that pages containing caveats, definitions and statistical notes may play a disproportionate role in trustworthy reuse, including in retrieval-based systems that depend on authoritative source material and robust citation behaviour (Faridi et al., 2026; Hwang et al., 2025).

The fourth finding is that influence indicators are improving even as media volume declines. Media mentions fall from 318 to 72 across the four weeks, but mentions in official policy or institutional documents rise from 3 to 19 and academic mentions from 1 to 11. That is a more meaningful medium-term signal for OECD than raw launch traffic. It suggests that the release is moving from broad publicity into expert and institutional use, which is more closely aligned with the Organisation’s policy mission.

The fifth finding is that AI-mediated visibility is emerging from a low base but is strategically significant. Identifiable referrals from known AI surfaces rise from 420 to 760 while overall traffic declines. This remains a small source of direct visits, but the direction matters. Research on generative interfaces indicates that direct referral traffic captures only part of the effect because users may consume summarised answers within the interface itself, or use the original source indirectly through retrieval and synthesis without clicking through to it (Kuai et al., 2026; Couraceiro and Pais, 2026; Lucchi, 2026).

The sixth finding is that the current reporting setup is no longer sufficient. Table 5 indicates that the management dashboard still privileges total traffic and other conventional top-line indicators, while AI-related signals remain outside the core reporting view. In a role that explicitly combines traditional communications metrics with emerging AI-era indicators, that gap is itself an operational finding rather than a secondary observation.

### 2. Distinguishing signal from noise

The clearest noise in the dataset is the Week 2 spike in total traffic. If management relied on total pageviews alone, it could conclude that attention remained broadly stable after launch. The human pageview series gives a more credible picture: 70 000 in Week 1, 46 000 in Week 2, 39 000 in Week 3 and 35 000 in Week 4. That still reflects solid performance, but it is a different story from the one implied by top-line traffic.

By contrast, several indicators are stronger signals of meaningful impact. Downloads remain comparatively robust. Engaged time on the executive summary and methodology pages suggests substantive use. Policy and academic mentions indicate downstream uptake. AI-related referrals to the executive summary and methodology pages are also more informative than referrals to the interactive chart page because they point to the pages most likely to support evidence-based retrieval and more accurate reuse.

The interactive chart page should therefore be interpreted cautiously. It attracts substantial volume, but only 41% of that traffic is estimated to be human, engagement is weak, and click-through is low. It appears useful for visibility and machine access, but it is not a strong indicator of comprehension or influence on its own.

### 3. Interpreting AI-mediated visibility

The AI-related evidence should be treated as directionally important but methodologically incomplete. The increase in identifiable referrals suggests that OECD material is being reached more often through AI-mediated discovery pathways. However, the literature indicates that such pathways frequently reshape the user journey. Generative systems can satisfy part of the user’s information need within the interface itself, compressing the incentive to visit the underlying source and reducing the visibility of source plurality and caveats (Kuai et al., 2026; Couraceiro and Pais, 2026; Lucchi, 2026).

The observation on caching and answer-layer effects reinforces this point. If AI systems reproduce OECD findings from cached or previously retrieved material without generating a visible return path, standard traffic analytics will under-record influence. In practical terms, this means that direct referral series should be treated as partial indicators of presence, not as complete indicators of use.

The manual output checks help to compensate for that measurement gap. They show that OECD is often cited by name, but not consistently; that source links are uneven across interfaces; and that statistical caveats are more fragile than headline findings. This is plausible in light of current retrieval and answer-generation research. Studies of document-grounded question answering and retrieval-augmented generation show that outputs often depend on evidence selection, source reliability and synthesis choices rather than on straightforward quotation, which makes simplification and caveat loss more likely, especially for methodological material (Sharma et al., 2026; Hwang et al., 2025; Lee et al., 2025).

For COM, the issue is therefore not only whether OECD content is discoverable. It is also whether OECD evidence remains attributable, contextualised and faithfully represented when AI systems mediate access to it. That concern is consistent with OECD work on trustworthy AI, which places particular weight on transparency, accountability, traceability and context-sensitive risk management (OECD, 2024a; OECD, 2024b; OECD, 2026).

### 4. Risks and data-quality concerns

There are four main risks.

First, there is a measurement risk. If validated human indicators are not separated from automated access, the release will appear to have generated more sustained public demand than the evidence supports.

Second, there is an interpretation risk. Low direct AI referrals could be read as weak AI relevance, when in reality the influence of AI systems may be partly invisible in standard web analytics because source use does not always produce a trackable click.

Third, there is a reputational risk. The sampled AI outputs show that OECD findings can be simplified in ways that reduce methodological precision. For an organisation whose authority depends on careful use of definitions, caveats and comparability, that is not a marginal issue.

Fourth, there is a reporting risk. Exploratory AI indicators are useful, but if they are integrated into core management reporting without explicit caveats, they may be treated as more precise and more mature than they are. OECD work on AI governance and reporting frameworks suggests the opposite approach: comparable structure should be combined with transparency about scope, limitations and uncertainty (OECD, 2025a; OECD, 2025b; OECD, 2026).

Fifth, there is an operational risk. If dashboard logic, media briefs and senior management notes continue to rely on a metric structure designed mainly for pre-GenAI traffic and media cycles, COM may react too slowly to changes in discoverability, source attribution and answer-layer intermediation.

### 5. Recommended adjustments for the next two months

COM should adjust its monitoring and reporting approach in five ways.

First, management reporting should separate validated human-performance indicators from contextual machine-access indicators. Estimated human pageviews, downloads, engagement, media quality, policy references and academic mentions should remain the core performance series. Automated traffic should still be tracked, but as contextual intelligence rather than as evidence of audience value.

Second, COM should strengthen asset-level reporting. The data show that the executive summary and methodology pages are disproportionately important. Reporting should therefore compare asset types by reach, human share, engagement depth, download behaviour and evidence of trustworthy reuse, rather than relying primarily on the main landing page.

Third, COM should maintain a dedicated AI-mediated section in the reporting dashboard. That section should include identifiable AI referrals, access patterns on likely retrieval assets, periodic manual checks of attribution and caveat preservation, and a log of recurring misrepresentation patterns. This would be consistent with a structured but still exploratory approach to emerging AI-era indicators (OECD, 2025a; OECD, 2026).

Fourth, COM should define a small pilot indicator set for Power BI rather than attempting a full AI-performance index immediately. A credible first version would include: validated human traffic to priority assets; identifiable AI-surface referrals; frequency of OECD attribution in sampled AI outputs; and a simple caveat-preservation rate from manual checks. This would make the dashboard more decision-useful without giving a false sense of precision.

Fifth, COM should pair visibility metrics with representation-quality metrics. The decline in accurate media coverage from 86% to 77% shows that volume alone is not enough. The same principle applies to AI outputs. A trusted organisation should track whether its content is being represented accurately, not only whether it is being surfaced.

Sixth, COM should explicitly adapt its short briefing products. For next week’s media brief on the senior mission, I would avoid leading with total traffic and instead foreground three points: qualified engagement remains comparatively strong; policy and academic uptake are improving; and AI-mediated visibility is increasing, but attribution remains incomplete and should be caveated.

Seventh, the next management note should explicitly frame impact as a life-cycle story. Launch attention is receding, but qualified engagement and institutional uptake are strengthening. That should be presented as a transition from publicity to policy and expert use, not as a deterioration in performance.

### 6. Proposed management message

The release delivered strong launch visibility, but its more important second-phase story is that substantive use and institutional uptake are holding up better than raw traffic, while AI-mediated discovery is growing in ways that increase the need for disciplined attribution, quality checks and caveated reporting.

### Conclusion

Overall, the release is performing well, but the dataset requires careful interpretation. Raw traffic overstates sustained audience value because automation materially distorts the series, especially in Week 2. A more credible reading is that broad attention is normalising, while stronger indicators of impact, including downloads, deep engagement, policy references, academic mentions and AI-related access to high-value pages, are becoming relatively more important.

COM should therefore move from a launch-volume narrative to a second-phase framework centred on human engagement, asset quality, downstream uptake and carefully qualified AI-era indicators. That would be analytically stronger and better aligned with OECD practice on trustworthy AI, transparent reporting and evidence-based public communication (OECD, 2021; OECD, 2024b; OECD, 2025a; OECD, 2026).

## References used in this model answer

Couraceiro, P. and Pais, P.C. (2026), "News Sufficiency: How Generative AI Summaries Reduce News Consumption in Zero-Click Searches", *Journalism and Media*, Vol. 7.

Faridi, A.R., Masood, F., Keshvi and Yunus, T. (2026), "Retrieval-Augmented Generation for Large Language Models: Evolution, Architectures, Applications, and Challenges (2020-2025)", *Wiley Interdisciplinary Reviews: Data Mining and Knowledge Discovery*, Vol. 16.

Hwang, J., Park, J., Park, H., Kim, D., Park, S. and Ok, J. (2025), "Retrieval-Augmented Generation with Estimation of Source Reliability", in *Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing*.

Kuai, J., Brantner, C., Karlsson, M., Van Couvering, E. and Romano, S. (2026), "AI chatbot accountability in the age of algorithmic gatekeeping: Comparing generative search engine political information retrieval across five languages", *new media & society*, Vol. 28, No. 5.

Lee, D., Jo, Y., Park, H. and Lee, M. (2025), "Shifting from Ranking to Set Selection for Retrieval Augmented Generation", in *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*.

Lucchi, N. (2026), *The Impact of Google AI Summaries and Google AI Overviews on Publishers' Revenue and Media Freedom: Implications for the Information Ecosystem and Democratic Resilience in the European Union*, European Parliament Policy Department for Justice, Civil Liberties and Institutional Affairs.

OECD (2021), "State of implementation of the OECD AI Principles: Insights from national AI policies", *OECD Digital Economy Papers*, No. 311, OECD Publishing, Paris.

OECD (2024a), "Explanatory memorandum on the updated OECD definition of an AI system", *OECD Artificial Intelligence Papers*, No. 8, OECD Publishing, Paris.

OECD (2024b), *Report on the Implementation of the OECD Recommendation on Artificial Intelligence*, OECD, Paris.

OECD (2025a), "Towards a common reporting framework for AI incidents", *OECD Artificial Intelligence Papers*, No. 34, OECD Publishing, Paris.

OECD (2025b), "Governing with Artificial Intelligence: Are governments ready?", *OECD Artificial Intelligence Papers*, No. 20, OECD Publishing, Paris.

OECD/BCG/INSEAD (2025), *The Adoption of Artificial Intelligence in Firms: New Evidence for Policymaking*, OECD Publishing, Paris.

OECD (2026), *OECD Due Diligence Guidance for Responsible AI*, OECD Publishing, Paris.

Sharma, S., Ramu, P., Garimella, A. and Mukherjee, K. (2026), "An Answer is just the Start: Related Insight Generation for Open-Ended Document-Grounded QA", in *Findings of the Association for Computational Linguistics: ACL 2026*.
