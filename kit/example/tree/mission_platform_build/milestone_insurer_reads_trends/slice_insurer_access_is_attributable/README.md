---
title: Insurer access is attributable
traces:
  gate: [G3.1, G3.3]
---

# Slice · Insurer access is attributable

## Goal

The insurer is a different organisation reading the company's data. The company has to be able to
answer "which analyst saw this site?" from its own records.

## Done-when

Demonstrated with two analyst accounts: each views a different site, and the company's safety lead
reads back who viewed what, without asking the insurer.

## Boundaries

- No shared login, at any point, including during the build (finding F-48).
- The read log is the company's record. The insurer cannot write to it or read it.
