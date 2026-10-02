---
title: Build the aggregate store the dashboard reads
status: no-packet
workflow: build-in-repository
blocked_by: [feature_report_inbox]
traces:
  gate: [G3.1]
  boundary: [B1]
  holding: [H2]
---

# Feature · Build the aggregate store the dashboard reads

## Goal

The insurer never reads the canonical store. It reads counts and rates by site and month, computed
from it, with no record and no free text behind them.

## Done-when

The aggregate store holds trends by site computed from synthetic reports and check-ins, and nothing
in it can be traced to one record.

## Status – no packet

Waits on the triage states `feature_report_inbox` defines, since a closed report and an open one
count differently.
