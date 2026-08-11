# Overview and Methodology of the AI Incidents and Hazards Monitor

Methodology and disclosures

## Overview

The AI Incidents and Hazards Monitor (AIM) was initiated and is being developed by the [OECD.AI expert group on AI incidents](https://oecd.ai/en/site/incidents) with the support of the [Patrick J. McGovern Foundation](https://www.mcgovern.org/). The goal of the AIM is to track actual AI incidents and hazards, as [defined by the OECD](https://www.oecd.org/en/publications/defining-ai-incidents-and-related-terms_d1a8d965-en.html), in real time and provide the evidence base to inform related AI policy discussions.

The AIM detects AI incidents and hazards from reputable international news outlets. The data is provided by [Event Registry](https://eventregistry.org/) (ER), a news intelligence platform that monitors and aggregates world news by processing over 150 000 news articles daily. Event Registry detects events, which are clusters of news articles reporting on the same happening. These events are tagged with related concepts. The events provided by Event Registry to AIM are limited to those that include AI concepts.

While recognising the likelihood that these incidents and hazards only represent a subset of all AI incidents and hazards worldwide, these publicly reported incidents and hazards nonetheless provide a useful starting point for building the evidence base.

An open submission process following the [common reporting framework for AI incidents](https://www.oecd.org/en/publications/towards-a-common-reporting-framework-for-ai-incidents_f326d4ac-en.html) is currently being developed to complement AI incidents and hazards from news articles. Other next steps include complementing incidents and hazards with court rulings and decisions by supervisory authorities wherever they exist.

The data collection and analysis for the AIM is done to ensure, to the best extent possible, the reliability, objectivity and quality of the information for AI incidents and hazards.

## Definitions

Thanks to the work of the [OECD.AI expert group on AI incidents](https://oecd.ai/en/site/incidents), AI incident terminology and related terms were defined. Published in May 2024, the paper [Defining AI incidents and related terms](https://www.oecd-ilibrary.org/science-and-technology/defining-ai-incidents-and-related-terms_d1a8d965-en) defines:

- An **AI incident** as an event where the development or use of an AI system results in actual harm.
- An **AI hazard** as an event where the development or use of an AI system is potentially harmful.

An AI incident is an event, circumstance or series of events where the development, use or malfunction of one or more AI systems directly or indirectly leads to any of the following harms:

- injury or harm to the health of a person or groups of people
- disruption of the management and operation of critical infrastructure
- violations of human rights or a breach of obligations under the applicable law intended to protect fundamental, labour and intellectual property rights
- harm to property, communities or the environment

An AI hazard is an event, circumstance or series of events where the development, use or malfunction of one or more AI systems could plausibly lead to an AI incident, meaning any of the following harms:

- injury or harm to the health of a person or groups of people
- disruption of the management and operation of critical infrastructure
- violations to human rights or a breach of obligations under the applicable law intended to protect fundamental, labour and intellectual property rights
- harm to property, communities or the environment

These definitions were built based on the definition of an AI system as described in the [OECD Recommendation on AI](https://oecd.ai/en/ai-principles) of 2019 and revised in 2024.

An AI system is a machine-based system that, for explicit or implicit objectives, infers, from the input it receives, how to generate outputs such as predictions, content, recommendations, or decisions that can influence physical or virtual environments. Different AI systems vary in their levels of autonomy and adaptiveness after deployment.

## Information Transparency Disclosures

Background: use of the OECD AI Incidents and Hazards Monitor is subject to the terms and conditions found at `www.oecd.org/termsandconditions`. The disclosures below do not modify or supersede those terms. They are intended to provide greater transparency surrounding the information included in the AIM.

### Third-Party Information

The AIM serves as an accessible starting point for understanding the landscape of AI-related challenges. It is populated with news articles from various third-party outlets and news aggregators with which the OECD has no affiliation.

### Views Expressed

Any views or opinions expressed in the AIM are solely those of the third-party outlets that created them and do not represent the views or opinions of the OECD. The inclusion of any news article or incident does not constitute an endorsement or recommendation by the OECD.

### Errors and Omissions

The OECD cannot guarantee and does not independently verify the accuracy, completeness, or validity of third-party information provided in the AIM. Information included in the AIM may contain errors and omissions.

### Intellectual Property

Any copyrights, trademarks, service marks, collective marks, design rights, or other intellectual property or proprietary rights mentioned, cited, or otherwise included in the AIM are the property of their respective owners. Their inclusion does not imply that they may be used for any other purpose. The OECD is not endorsed by, does not endorse, and is not affiliated with any of the holders of such rights, and cannot grant any rights to use or otherwise exploit these protected materials.

## Methodology for Monitoring AI Incidents and Hazards

Since `November 2024`, incidents and hazards are identified and added to the AIM through the following steps.

Historical incidents and hazards collected prior to November 2024 are being retrospectively annotated using the same methodology to ensure consistency.

### 1. Retrieval of AI-tagged events

Events tagged with AI-related concepts, including artificial intelligence, machine learning, generative AI, self-driving car and facial recognition, are retrieved from Event Registry.

### 2. Event-level classification

LLMs are used to classify AI-related events into three categories:

- AI incidents
- AI hazards
- unrelated events

This classification is based on the event summary provided by Event Registry.

The process is two-step:

- a smaller model, `OpenAI GPT-4o mini`, filters out events that seem unrelated to AI incidents and hazards
- a larger model, `OpenAI GPT-4o`, reclassifies the remaining events to confirm whether they are incidents or hazards

### 3. Article-level classification

Individual news articles are also classified into incidents and hazards using LLMs, following the same process as for events. Here, article content is used instead of event summaries to enhance reliability.

This helps ensure:

- all articles related to an event are relevant
- the event classification is supported by its underlying articles

If some articles are classified differently, the event adopts the most common classification among them.

Example:

- if an event is initially classified as an incident
- and it has three related articles
- and two of those are classified as hazards
- then the event label is changed to `hazard`

If none of the articles for an event are classified as an incident or hazard, the event as a whole is reclassified as `unrelated`.

The event-level and article-level classification steps help ensure that only pertinent events are included in the AIM.

### 4. Metadata enrichment

Each event is enriched with metadata, including:

- title
- summary
- harm type
- severity
- affected stakeholders
- country where it occurred

This metadata is LLM-generated using `OpenAI o3-mini` from the top three articles of each event, selected from different news outlets.

Articles are ranked based on their outlets' ranking in their respective country. This is meant to balance outlet popularity with fair geographical representation.

Currently, the summary and metadata are generated when the incident or hazard is added to the AIM.

### 5. Clustering similar events

Similar events are grouped by analysing their summaries and identifying related events in AIM using cosine similarity.

For each new incident or hazard:

- the top 10 closest summaries, or embeddings, from existing AIM events are identified
- an LLM, `OpenAI o3-mini`, assesses whether any of these similar events should be clustered together

If no similar events are found, a new incident or hazard is created.

## Update Frequency

The pipeline runs daily, processing events from one to four days earlier. This window helps maximise information capture while allowing media outlets time to report relevant events and Event Registry time to process and cluster them.

In particular:

- news articles related to ongoing incidents or hazards are retrieved from Event Registry for four days after an event
- those articles are then added to the relevant event in AIM

This is intended to capture the most relevant articles during the peak of media coverage. Articles that appear after that timeframe are more likely to be misclassified as a separate event.

## Summary Table of the Methodology

| Stage | Summary |
| --- | --- |
| Identification and classification | AI events and their articles are classified as AI incidents, hazards or unrelated based on OECD definitions. On average, about 1 000 AI events are analysed daily, resulting in around 10 AI incidents or hazards. |
| Data enrichment | AI incidents and hazards are enhanced with metadata and reporting-framework criteria such as title, summary, country, industry, and affected stakeholders. |
| Clustering | Articles are added to events up to 4 days after the event was first registered. Before upload to AIM, new incidents and hazards are checked against existing events and grouped where relevant. |

## Additional Notes

To note, an AI event contains multiple news articles. Articles are added to events up to four days after an event was first registered. The AIM detects on average about `30` incidents and hazards per day.

Prior to `November 2024`, AI incidents and hazards were classified and included in the AIM using traditional machine learning techniques. An archive exists at `https://oecd.ai/en/eventregistry` for more information.
