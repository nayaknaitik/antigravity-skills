# Color Palette Specification

## Semantic Colors
- **Success / Buy**: `text-success-600` (Emerald) -> For positive P&L, Buy buttons.
- **Danger / Sell**: `text-danger-600` (Red) -> For negative P&L, Sell buttons, stop-loss triggers.
- **Primary Action**: `text-primary-600` (Blue) -> For non-directional primary actions (Submit, Login, active tabs).

## Grayscale / Layout
- **Background**: `bg-slate-50` -> Soft off-white to reduce eye strain over long sessions.
- **Surfaces/Cards**: `bg-white` -> With `border-slate-200` to create subtle separation.
- **Primary Text**: `text-slate-900` -> Highest contrast for critical numbers.
- **Secondary Text**: `text-slate-500` -> For labels, timestamps, and muted headers.

Always run `scripts/validate_contrast.py` if introducing new custom colors.
