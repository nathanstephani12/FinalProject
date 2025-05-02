
# UMA Protocol Constants

This document introduces key constant values used in UMA’s smart contracts, with emphasis on the Optimistic Oracle V3, escalation managers, and governance processes. These constants define core behaviors of UMA’s assertion model, data handling, and economic guarantees. 

## Constants from Optimistic Oracle V3 and Related Modules

| Constant Name                | Value          | Description |
|-----------------------------|----------------|-------------|
| `defaultIdentifier`         | `"ASSERT_TRUTH"` | A global string used to indicate the default identifier for UMA assertions. Assertions are formatted around this schema. |
| `assertionLiveness`         | `7200` (seconds) | The duration in which a submitted assertion can be disputed. A core parameter that balances oracle speed vs. security. |
| `numericalTrue`             | `1e18`          | UMA represents `True` as the integer 1 * 10¹⁸. This standardizes boolean outputs for price request disputes. |
| `unresolvable`              | `"Unresolvable"`| A text marker returned when no answer can be determined. Often used in fallback or expired queries. |
| `PROPOSAL_HASH_KEY`         | `"proposalHash"`| A key used to index or verify proposals in UMA’s Optimistic Governor module. |
| `EXPLANATION_KEY`           | `"explanation"` | A field label used to attach justifications to proposed governance actions. |
| `RULES_KEY`                 | `"rules"`       | A field label for procedural metadata about how a given assertion should be interpreted. |
| `ancillaryBytesLimit`       | `8192`          | Defines the maximum length in bytes that the ancillary data string can be. |
| `MAX_ADDED_ANCILLARY_DATA`  | `53`            | Hard-coded maximum number of characters that can be appended to ancillary data in assertions. |
| `OO_ANCILLARY_DATA_LIMIT`   | `ancillaryBytesLimit - MAX_ADDED_ANCILLARY_DATA`    | Maximum length of ancillary data allowed in an oracle request. Crucial for gas limits and data parsing. |
| `TOO_EARLY_RESPONSE`        | `type(int256).min` | A sentinel error code returned if a user tries to settle an assertion before its liveness period expires. |



## Constants from `Constants.sol` (Updated)

The `Constants.sol` file defines **interface identifiers** used across UMA’s protocol. These constants are stored as `bytes32` values and registered in UMA’s [Finder contract](https://github.com/UMAprotocol/protocol/blob/master/packages/core/contracts/common/Finder.sol), which acts as a system-wide registry for locating key components. Instead of hardcoding addresses or string identifiers, UMA uses this centralized and immutable key-value mechanism for cross-module discovery.

| Constant Name              | Value             | Description |
|---------------------------|-------------------|-------------|
| `Oracle`                  | `"Oracle"`        | Used to locate the on-chain oracle implementation (e.g., the DVM). |
| `IdentifierWhitelist`     | `"IdentifierWhitelist"` | Points to the contract that manages approved price identifiers. |
| `Store`                   | `"Store"`         | Refers to the contract handling fee mechanics, proposer bonds, and rewards. |
| `FinancialContractsAdmin`| `"FinancialContractsAdmin"` | Identifies the admin layer for approved UMA contracts. |
| `Registry`                | `"Registry"`      | Points to the contract that tracks approved financial contracts. |
| `CollateralWhitelist`     | `"CollateralWhitelist"` | Interface ID for managing allowed collateral types. |
| `OptimisticOracle`        | `"OptimisticOracle"` | Original optimistic oracle implementation (v1). |
| `OptimisticOracleV2`      | `"OptimisticOracleV2"` | Used to access the V2 implementation of the oracle. |
| `OptimisticOracleV3`      | `"OptimisticOracleV3"` | Interface ID for the current and most advanced version of the Optimistic Oracle. |

### Why These Matter

UMA uses the `Finder` pattern to **decouple contracts** from each other. Instead of hardcoding dependencies, any module can resolve the address of another by querying the Finder with one of these constants.

- Enables **upgradability** without migrating or redeploying contracts.
- Enhances **modularity** and **testability**.
- Promotes system-wide **interface standardization**.

By using `Constants.sol` to store canonical interface identifiers, UMA ensures that its architecture is robust, flexible, and easy to maintain as new oracle versions or modules are deployed.


## Applications Across UMA's Core Contracts

### 1. Optimistic Oracle V3

- Constants like `ASSERT_TRUTH`, `assertionLiveness`, and `unresolvable` define the oracle's assertion lifecycle, standard outputs, and fallback cases.
- `OO_ANCILLARY_DATA_LIMIT` and `MAX_ADDED_ANCILLARY_DATA` help enforce efficient, on-chain-compatible data use.

### 2. Data Verification Mechanism (DVM)

- `numericalTrue` ensures compatibility with contracts expecting numeric precision in truth-based outcomes.
- `TOO_EARLY_RESPONSE` enforces time-sensitive logic for resolving assertions post-liveness.

### 3. Governance Modules

- Constants like `PROPOSAL_HASH_KEY`, `EXPLANATION_KEY`, and `RULES_KEY` are used to structure metadata for on-chain governance actions and upgrades.


## Design Implications

- **Assertion Security**: `assertionLiveness` balances fast response time with risk exposure. Increasing it provides more room for challenges, decreasing it speeds up resolutions.
- **Standardization**: UMA’s use of constants like `NUMERIC_TRUE` and `ASSERT_TRUTH` ensures system-wide consistency.
- **Governance Readability**: Standardized proposal metadata fields improve the interpretability of governance decisions.
- **Data Efficiency**: Strict ancillary data limits keep oracle requests lightweight and gas-efficient.


## Conclusion

The constants used in UMA, both from the oracle implementation and `Constants.sol`, reflect a protocol focused on trust minimization, standardization, and modularity. By defining these values centrally, UMA enhances readability, upgradability, and coordination across contracts and contributors. These constants provide key control levers that govern UMA’s dispute resolution timing, economic incentives, and governance structure.
