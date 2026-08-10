# Maki System Check: Recruiter Configuration And Scoring

## Purpose

Maki’s recruiter-facing `System-check` feature allows employers to verify a candidate’s remote-work technical compatibility and configure how that verification contributes to the evaluation.

## Installation-dependent checks

The source material states that some checks require the candidate to install the System Check software.

The options explicitly listed as requiring installation are:

- free disk space
- network connection
- memory
- processor clock speed
- processor core number
- machine type
- screen resolution

Other options require only candidate acceptance and do not require additional installation.

## Recruiter configuration options

Recruiters can:

- enable or disable specific characteristics for evaluation
- leave measures unspecified, in which case the result is only displayed
- enter custom comparison values for each characteristic
- adjust the weighting of the system-check evaluation in the total score

This allows the system check to function either as:

- an informational verification step
- or a weighted scored component of the assessment

## Scoring logic

The scoring model described is deterministic:

- each validated criterion receives a score of `1`
- each non-validated criterion receives a score of `0`

At the end of the evaluation:

- a total percentage of validated criteria is calculated
- that percentage becomes the system-check score

If not all characteristics are completed:

- the score is still calculated automatically
- using the available completed characteristics

## Privacy note for recruiters

The recruiter-facing material also states that if a candidate has concerns about storage of this data, they may contact:

- `privacy@makipeople.com`

to request deletion.
