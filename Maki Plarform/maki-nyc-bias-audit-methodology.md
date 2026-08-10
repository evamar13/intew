# Maki NYC Local Law 144 Bias Audit Methodology

## Purpose

This document captures the bias-audit information provided for Maki’s assessment tools under `NYC Local Law 144`, focusing on the summary details shared for `Mochi` and `Shiro`.

## Audit scope

- Organization: `Maki People`
- Legislation: `NYC Local Law 144`
- Protected attributes reviewed:
  - `gender`
  - `race_ethnicity`

## Mochi: voice screening audit summary

### System description

`Mochi` is described as an AI-powered voice screening tool that conducts structured conversational screenings through spoken interactions.

Its pipeline includes:

- candidate audio captured through phone-based or web-based delivery
- automatic speech recognition (ASR) to convert speech into text
- transcript standardization
- evaluation through BARS-based scoring
- large language model scoring against behavioural criteria
- dimension-level scores aggregated into overall skill scores
- output in structured scorecards

### Assessment design

Mochi evaluates `19 soft skills`.

Each skill is assessed through two questions:

- an initial broad contextual question
- a follow-up question probing more deeply into a specific scenario

The interaction is conversational, but the structure and scoring intent are standardized.

### Key positioning

Mochi is described as:

- a decision-support system, not an autonomous hiring decision-maker
- designed for fairness and bias mitigation
- privacy-aware
- explainable through standardized scorecards and qualitative rationale

## Shiro: written soft-skills assessment audit summary

### System description

`Shiro` is described as an AI-assisted assessment platform for evaluating candidate soft skills through structured written responses.

Its pipeline includes:

- collection of standardized open-ended responses
- mapping each response to skill, behavioural dimension, and question type
- light preprocessing that does not alter semantic content
- scoring through predefined BARS rubrics
- dimension-level scoring by a large language model
- weighted aggregation into overall skill scores
- structured scorecards with quantitative scores and qualitative explanations

### Assessment design

Shiro also evaluates `19 soft skills`, using two open-ended questions per skill:

- one broad contextual question
- one scenario-based probe

This structure is intended to capture both breadth and depth of behaviour while reducing reliance on self-perception alone.

## Shared synthetic audit dataset

The bias-audit summaries describe a common synthetic dataset design used for testing.

### Dataset characteristics

- model used for transcript generation: `OpenAI GPT-5-mini via Azure`
- job roles: `40`
- quality levels: `7`
- intersectional demographic groups: `14`
- total simulated interviews: `3,920`

### Job range

Roles span from entry-level positions such as:

- Janitor
- Cashier
- Bartender

to professional and managerial roles such as:

- Financial Manager
- Software Developer
- Corporate Lawyer

### Quality levels

Responses were calibrated across seven quality levels:

- Very Poor
- Poor
- Below Average
- Average
- Above Average
- Good
- Excellent

Each level had instructions controlling:

- reasoning depth
- specificity of examples
- level of self-reflection
- target answer length

### Demographic coverage

The summaries describe `14 intersectional demographic groups` built from:

- `7` EEO-1 race/ethnicity categories
- `2` sex categories

Race and ethnicity categories referenced include:

- Hispanic or Latino
- White
- Black or African American
- Native Hawaiian or Pacific Islander
- Asian
- Native American or Alaska Native
- Two or More Races

The summaries note that at least one intentional misspelling of demographic phrasing was inserted per transcript to test sensitivity to demographic signals.

## Reported impact-ratio snapshot

The shared impact-ratio snapshot included:

- gender:
  - Male: impact ratio `0.99`, scoring rate `0.50`, sample `1,960`
  - Female: impact ratio `1.00`, scoring rate `0.50`, sample `1,960`
- race/ethnicity:
  - White: impact ratio `0.85`, scoring rate `0.45`, sample `560`
  - Asian: impact ratio `0.91`, scoring rate `0.48`, sample `560`
  - Two or More Races: impact ratio `0.94`, scoring rate `0.49`, sample `560`
  - Hispanic or Latino: impact ratio `0.96`, scoring rate `0.51`, sample `560`
  - Black or African American: impact ratio `0.97`, scoring rate `0.51`, sample `560`
  - Native Hawaiian or Other Pacific Islander: impact ratio `0.99`, scoring rate `0.52`, sample `560`
  - American Indian or Alaska Native: impact ratio `1.00`, scoring rate `0.53`, sample `560`

## Main distinctions between Mochi and Shiro

- `Mochi` starts with spoken interaction and adds an ASR step before scoring.
- `Shiro` starts with written open-ended responses.
- Both are described as using BARS-based logic and standardized scorecards.
- Both are framed as decision-support tools rather than autonomous hiring systems.
