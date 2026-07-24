# High Frequency UI Patterns

## 1. Tick Flashing
When a price updates via WebSocket, do not change the background color of the cell (it creates visual fatigue). Instead, briefly flash the text color:
- **Up Tick**: `text-success-600` for 600ms, transitioning back to default.
- **Down Tick**: `text-danger-600` for 600ms, transitioning back to default.

## 2. The Order Ticket
The order ticket must have absolute visual hierarchy:
- Use `backdrop-blur` to focus the user's attention.
- Explicit toggle switches (BUY vs SELL). The BUY button should always be distinct from the SELL button via semantic colors (never just a primary blue for both).
- Show Margin Required vs Available Margin right above the submit button to prevent errors.

## 3. Data Tables
- Sticky headers (`sticky top-0`).
- Tabular nums (`tabular-nums`).
- Right-align all numeric values (prices, quantities) so decimals align perfectly.
- Left-align strings (symbols, names).
