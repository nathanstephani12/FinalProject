
# Colony Protocol Constants: Design and Governance Implications

This document introduces constants from Colony’s contract suite that define the behavior of the protocol’s most important systems: **reputation**, **voting**, **funding**, and **governance**. These constants were extracted from core files including `Colony.sol`, `ColonyAuthority.sol`, `ColonyFunding.sol`, and others from the [JoinColony GitHub repo](https://github.com/JoinColony/colonyNetwork).



## Key Constants from the Colony Protocol

| Constant Name             | Value                        | Description |
|--------------------------|------------------------------|-------------|
| `DECAY_NUMERATOR`        | `999679150010889`            | Numerator used in Colony’s exponential decay formula for reputation. |
| `DECAY_DENOMINATOR`      | `1000000000000000`           | Denominator for computing the decay rate. Used in combination with the numerator to gradually decrease reputation over time. |
| `DECAY_PERIOD`           | `1 hours`                    | Time interval (in seconds) after which reputation decay is applied. |
| `UINT128_MAX`            | `2 ** 128 - 1`               | The maximum value for a 128-bit unsigned integer. Used to safely cap balances or staking variables. |
| `YAY` / `NAY`            | `1` / `0`                    | Encoded values representing binary votes in Colony's reputation-based governance system. |
| `SUBMIT_END`, `REVEAL_END`, `STAKE_END` | `1`, `2`, `0` | Enumeration states for different phases in Colony’s commit-reveal voting process. |
| `PAUSER_ROLE` / `MINTER_ROLE` | `keccak256("PAUSER_ROLE")`, etc. | Role identifiers used in Colony's access control system. |
| `TOKEN_MULTIPLIER`       | `10 ** 18`                   | Scales native token amounts to full-precision values (used across ERC20 payments and internal accounting). |
| `METATRANSACTION_NONCES_SLOT` | `41`                    | Storage slot index used to track nonces for meta-transactions. |
| `MAX_PAYOUT_MODIFIER`    | `int256(WAD)`                | The upper bound of the payout modifier for tasks or domains, used to amplify payout above nominal value. |
| `MIN_PAYOUT_MODIFIER`    | `-int256(WAD)`               | The lower bound of the payout modifier, used to penalize or reduce payout amounts during arbitration or governance review. |



## Insights and Implications

### 1. Reputation Decay System
Colony uses a time-based decay model to ensure reputation reflects ongoing contributions. Over time, inactive users see their reputation diminish, promoting fresh engagement and discouraging centralization of influence.

### 2. Governance Through Weighted Voting
Binary votes (`YAY`, `NAY`) and distinct voting phases (`SUBMIT_END`, `REVEAL_END`, `STAKE_END`) create a structured, multi-phase voting process that supports both fairness and sybil resistance. Votes are weighted by **domain-specific reputation**.

### 3. Access Control and Role Security
`PAUSER_ROLE` and `MINTER_ROLE` values are derived from keccak256 hashes, ensuring consistent role validation while avoiding magic strings. These roles control token minting, contract pausing, and other administrative actions.

### 4. Token and Funding Control
- `TOKEN_MULTIPLIER` ensures accurate financial calculations by scaling all values to standard 18-decimal precision.
- `MAX_PAYOUT_MODIFIER` and `MIN_PAYOUT_MODIFIER` provide a **programmable reward modulation mechanism**:
  - Colonies can **reward outstanding work** by increasing payouts (up to `+100%` via `WAD` scaling).
  - Or **penalize underperformance** by reducing or even zeroing out payments.
  - This directly connects Colony’s funding logic to reputation, arbitration, and governance outcomes.

### 5. Meta-Transaction Safety
Meta-transactions allow users to sign messages off-chain, saving gas. The `METATRANSACTION_NONCES_SLOT` prevents replay attacks by tracking usage through a fixed storage slot.


## Conclusion

These constants offer a window into Colony’s key priorities:

- **Adaptive reputation** that evolves over time
- **Decentralized arbitration** with weighted governance
- **Flexible compensation mechanisms** via payout modifiers
- **Modern usability features** like meta-transactions

Colony’s design blends programmable incentives with fine-grained governance, enabling collaborative organizations to make nuanced, fair, and efficient decisions without centralized intermediaries.
