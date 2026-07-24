---
name: trading-platform-uiux
description: >
  MANDATORY skill for any UI/UX design, frontend component creation, chart layout, 
  dashboard styling, CSS, Tailwind, responsive layout, dark/light theme, accessibility (a11y), 
  or visual formatting task. MUST be activated whenever the user mentions UI, charts, tables, 
  trading screens, order books, responsive views, or component design.
version: 1.0.0
author: Principal UI/UX Architect
tags: [uiux, frontend, tailwindcss, react, nextjs, quantitative-trading, high-performance-ui, a11y, responsive-design]
---

# Trading Platform UI/UX Skill Specification

## 1. Purpose & Organizational Role
`trading-platform-uiux` is the foundational standard for all frontend interfaces. It ensures that the trading platform looks premium, responds instantaneously, and guarantees absolute clarity for traders making high-stakes decisions.

## 2. Activation Rules
Activate this skill whenever:
- Working on Next.js/React frontend components.
- Designing or modifying Tailwind CSS classes.
- Structuring data tables, charts, order tickets, or dashboards.
- Resolving layout bugs or responsiveness issues.
- Modifying themes (light/dark mode).

## 3. Core Principles
- **Data Clarity Over Decoration**: Ticks, prices, and P&L must be instantly readable. Avoid superfluous animations that distract from the data.
- **Tabular Numerics**: ALWAYS use `font-variant-numeric: tabular-nums` for prices and quantities to prevent jitter.
- **Consistent Color Semantics**: Green is ALWAYS profit/buy. Red is ALWAYS loss/sell. Do not mix semantic meanings.
- **High-Density but Breathable**: Trading UIs require high data density. Achieve this through precise typography and grid alignment, not by removing padding entirely.

## 4. References & Tooling
Review the `references/` directory for exact typography grids and color palettes.
Use the `scripts/` provided to generate boilerplates or validate WCAG contrast ratios.
