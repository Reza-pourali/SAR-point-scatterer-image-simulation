# Refactor Notes

The original coursework used six small scripts with repeated code. The public
repository consolidates them into one parameterized simulation package.

## Corrections made before publication

1. **Correct case mapping**
   - Case 1: phase in `[-pi, pi]`
   - Case 2: phase in `[-pi/5, pi/5]`
   - Case 3: phase in `[-2pi/5, 2pi/5]`

2. **Correct plot titles**
   Several legacy scripts saved Case 2/3 figures while still displaying the
   title `Case 1`. Titles are generated directly from the case configuration in
   the refactored version.

3. **Removed hard-coded Windows paths**
   Outputs are written to a user-selected directory.

4. **Reproducible random-number generation**
   `numpy.random.default_rng(seed)` replaces implicit global randomness.

5. **Vectorized chunked implementation**
   The original nested Python loops over 90,000 pixels are replaced with
   vectorized NumPy operations processed in row chunks.

6. **English-only public repository**
   Source code, comments, docs, filenames, and output text are English.

7. **Legacy source inconsistency isolated**
   The uploaded legacy files do not contain one clean fixed-amplitude Case 1
   implementation and one file duplicates the random-amplitude Case 3 setup.
   The case definitions in the final coursework report are used as the
   authoritative experiment specification.
