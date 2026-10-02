---
title: The company runs it alone
traces:
  gate: [G4.1, G4.2]
---

# Milestone · The company runs it alone

## Goal

The supplier leaves and the platform keeps working. The company's own staff can change it and can
run a check-in window.

## Done-when

**The company accepts criteria G4.1 and G4.2, with nobody from the supplier present.**

### The confirmation statements

| | | Node |
|---|---|---|
| G4.1 | The company's own staff deploy a change to production | `feature_deploy_runbook` |
| G4.2 | The company's own staff run a check-in window from invitation to close | `feature_operations_rehearsal` |

## Boundaries

- Nothing the company needs may live only on a supplier machine or in a supplier account (boundary
  B4).
- No new capability. Handover changes who operates the platform, not what it does.

## Reading

**Unplanned, and the tree should say so.** Both features are one line each. They exist so that G4.1
and G4.2 have an owner. No target date is set because none has been agreed.
