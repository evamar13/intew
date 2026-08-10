# Maki Scoring Methods

## Purpose

This document summarizes the scoring logic described in Maki’s candidate-help materials, focusing on how different activity types are evaluated.

## Key principle

Maki states that assessment scores are indicators designed to support recruitment decisions, not to automate them.

Important constraints explicitly stated:

- scores do not automatically qualify candidates
- scores do not automatically disqualify candidates
- recruiters may override a low score
- results are only one part of the overall hiring decision

## 1. AI-scored activities

Maki explains that some activities are scored using AI models.

Examples mentioned:

- open-ended language proficiency assessments
- structured interviews assessing soft skills

### Language assessments

Language assessments are described as being scored against the `CEFR` framework.

Depending on the activity, scoring may include:

- task achievement
- coherence and cohesion
- lexical range
- grammatical range
- pronunciation for spoken responses

### Structured interviews and soft-skill assessments

These are described as using `Behaviourally Anchored Rating Scales (BARS)`.

Maki’s explanation highlights that BARS-based scoring is:

- structured
- transparent
- auditable

Each soft skill is described as composed of multiple sub-dimensions, with each sub-dimension evaluated using its own scoring grid. The sub-dimension scores are then combined into an overall skill score.

### Example provided by Maki

For `Teamwork`, Maki gives an illustrative structure with sub-dimensions such as:

- collaboration
- supportiveness
- communication

Illustrative rating anchors:

- `5 - Excellent`: specific example, clear role, clear outcome, and reflection
- `3 - Adequate`: general example but lacking detail
- `1 - Limited`: vague or off-topic answer without a clear example

Maki notes that the real BARS scales are more detailed than the simplified example.

## 2. Deterministic scoring

Maki also explains that some activities are scored with fixed, deterministic rules, with no human or AI interpretation involved.

Two main patterns are described.

### A. Weighted answer scoring

In some assessments:

- the best answer receives the highest point value
- partially correct answers may receive fewer points
- some answers receive no points

#### Single-choice example

- Answer 1: `3` points
- Answer 2: `2` points
- Answer 3: `0` points

If the candidate selects Answer 2:

- score = `2 / 3 ≈ 0.67`

#### Multiple-choice weighted example

Maki describes a formula based on:

- sum of points for selected answers
- divided by sum of points for all positive answers

Negative points may apply for incorrect selections, but the score for a question cannot go below `0%`.

Example values:

- Answer 1: `+3`
- Answer 2: `+3`
- Answer 3: `+2`
- Answer 4: `-1`

If the candidate selects 2 and 3:

- `5 / 8 = 62.5%`

### B. Correct/incorrect scoring

Other assessments simply mark answers as correct or incorrect.

This applies to:

- single choice
- numerical questions
- true/false
- some multiple-choice formats

For single choice, numerical, and true/false:

- correct answer = `1`
- incorrect answer = `0`
- final score = total points earned divided by total number of questions

For multiple-choice questions, Maki gives this pattern:

- correct answers selected ÷ total correct answers
- minus `(wrong answers selected × 0.5)`

Scores per question cannot go below `0`.

Example where Answers 1 and 2 are correct, and Answer 3 is incorrect:

- Select 1 + 3: `1/2 - 0.5 = 0`
- Select 1 only: `1/2 = 0.5`
- Select 1 + 2: `2/2 = 1`
- Select 3 only: `0/2 - 0.5 = 0`

## Final-score logic

Maki explains final scores as based on:

- total points earned across questions
- divided by total number of questions

or, for specific question-level formulas, aggregated from question-level calculations according to the rules of the assessment.

## Candidate support

For additional questions on scoring, the help article directs candidates to:

- `candidates@makipeople.com`
