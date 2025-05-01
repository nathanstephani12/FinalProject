
# Analysis of Kleros System Constants

This is an overview of key constants that govern the Kleros arbitration protocol, parsed from the contracts contracts in the [kleros](https://github.com/kleros/kleros) and [kleros-interaction](https://github.com/kleros/kleros-interaction) GitHub repositories.

## Selected from `KlerosLiquid.sol`

| Constant             | Value               | Description |
|----------------------|---------------------|-------------|
| `MIN_JURORS`         | `3`                 | Sets the baseline number of jurors per dispute. Affects fairness, cost, and resistance to collusion. Serves as the default number of jurors if not specified by a dispute. |
| `MAX_STAKE_PATHS`    | `4`                 | Controls the complexity of the Sortition Sum Tree used to randomly select jurors. Helps keep gas costs manageable. |
| `ALPHA_DIVISOR`      | `1e4`               | Used for fixed-point math in penalty/reward calculations. Enables precision in computing stake adjustments. |
| `NON_PAYABLE_AMOUNT` | `(2 ** 256 - 2) / 2`| Used as a flag value to prevent unintended ETH transfers in internal functions. A safety mechanism. |
| `MULTIPLIER_DIVISOR` | `10000`             | Standard divisor for computing appeal and arbitration cost multipliers. Affects proportional stake calculations in the appeals process. |

These constants are fundamental to Kleros’s staking logic, appeal mechanism, and gas efficiency model.

## Selected from `ArbitrableTransaction.sol` and Related Contracts

| Constant             | Value                                | Description |
|----------------------|--------------------------------------|-------------|
| `RULING_OPTIONS`     | `"Reimburse partyA;Pay partyB"`      | Human-readable labels for juror voting choices. Enhances clarity and transparency. |
| `AMOUNT_OF_CHOICES`  | `2`                                  | Defines the number of voting options. In two-party disputes, this matches the binary ruling model. |
| `SENDER_WINS`        | `1`                                  | Encoded outcome used to reimburse the payer. |
| `RECEIVER_WINS`      | `2`                                  | Encoded outcome used to pay the service provider. |

These constants are specific to two-party arbitration scenarios common in freelance escrow use cases. They shape the juror interface, voting logic, and payout rules.

## Design Significance

### 1. Balancing Security and Usability
- `MIN_JURORS = 3` ensures enough decentralization for small claims.
- `RULING_OPTIONS` and `AMOUNT_OF_CHOICES` keep the system intuitive for jurors, especially non-technical ones.

### 2. Economic and Incentive Modeling
- `ALPHA_DIVISOR` and `MULTIPLIER_DIVISOR` ensure juror incentives are precisely tunable using fixed-point math.
- These constants affect how much jurors are slashed or rewarded, which directly impacts the system’s resistance to manipulation.

### 3. System Safety and Performance
- `NON_PAYABLE_AMOUNT` is an important defense-in-depth measure.
- `MAX_STAKE_PATHS` directly constrains resource usage during juror selection, avoiding performance degradation.

## Conclusion

Together, these constants reflect the Kleros system’s key values:
- Efficiency: Low juror minimums and binary outcomes enable fast resolution.
- Security: Stake management and ETH safety measures reduce risk.
- Transparency: Readable ruling options and encoded outcomes increase trust.
