# Data-Rule-Generator

### Following datasets have been used from the UCI Machine learning repository to generate rules-

1. Car Dataset – (1728)

2. Contraceptive Dataset – (1473)

3. Nursery Dataset – (12960)

### Measures - Lift and Confidence

Lift generates comparatively better rules than confidence. It takes into account both left and right side probabilities. These rules generated are more reliable. We do not use pruning in Lift based rule generation, and generate all possible rules from which we can select the best rule.
