---
title: The insurer sees trends by site
traces:
  gate: [G3.1, G3.2]
---

# Slice · The insurer sees trends by site

## Goal

An analyst opens the dashboard and reads how each site's incident rate and wellbeing scores have
moved, without ever being shown a group small enough to be a person.

## Done-when

Demonstrated on synthetic data that includes one site below the minimum: the large sites chart
normally and the small site shows as suppressed, in every chart.

## Boundaries

- A chart is handed aggregates that are already suppressed. No chart suppresses for itself.
- No drill-down from a figure to the records behind it.
