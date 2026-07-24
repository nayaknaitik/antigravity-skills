# System Constraints Matrix Template

## Constraints Matrix: {{ SYSTEM_NAME }}

| Constraint ID | Category | Description of Constraint | Architectural / Engineering Impact | Flexibility |
| :--- | :--- | :--- | :--- | :---: |
| `CON-01` | Regulatory | SEC Rule 15c3-5 Pre-trade Risk Filter | Pre-trade filter cannot be bypassed by any strategy | NON-NEGOTIABLE |
| `CON-02` | Technology | Must run on RedHat Enterprise Linux 9 with real-time kernel | Requires RT kernel tuning and CPU pinning | MANDATORY |
