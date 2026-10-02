---
title: Who read which report
status: design
workflow: build-in-repository
blocked_by: [feature_report_inbox]
traces:
  gate: [G1.4]
  holding: [H1]
---

# Feature · Who read which report

## Goal

A report names people. The company has to be able to say who on the safety team opened it, because a
report can be used against the person it names.

## Done-when

For any report, the safety team's lead reads back every member who opened it and when, from a record
no member of the team can alter.

## Status – needs design

The team is three people with the same access. A log they can all write to attributes nothing: each
can add or remove a line. The design question is where the record lives so that the people it
describes cannot change it, in an organisation too small to separate those duties.

Two candidates, neither chosen:

- The record is written to a store only the company's IT administrator can reach.
- The record is append-only and its tail is sent somewhere outside the platform each day.

This is a decision for the company, not for a build session. It needs an owner before it can have a
packet.
