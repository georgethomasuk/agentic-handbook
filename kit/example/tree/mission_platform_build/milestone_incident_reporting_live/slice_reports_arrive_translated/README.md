---
title: Reports arrive translated
traces:
  gate: [G1.2]
---

# Slice · Reports arrive translated

## Goal

The safety team does not all read every language a report is written in. A report filed in another
language is readable by the whole team in the working language, with the original beside it.

## Done-when

Demonstrated on a synthetic report in a second language: the working-language text appears in the
inbox, marked as machine-translated, with the original one action away.

## Boundaries

- **Inside the agreed region, with no training on the content.** Both are read back from the
  service's own configuration, not assumed.
- **Machine translation is labelled wherever it is shown.**
- A report that cannot be translated is still delivered, in its original language, and says so.

## Inherited context

- The translation service is a third party processing free text. Its handling of that text is a
  position the company has to declare, not a control the build can add.

## Reading

**The build here is small and the decision was not.** Where free text may be sent was settled with
the company before `feature_translation_service_access` was briefed. That feature's record holds what
was read back.
