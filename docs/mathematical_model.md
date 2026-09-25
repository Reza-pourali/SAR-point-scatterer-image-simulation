# Mathematical Model

Each SAR image pixel is formed by the coherent sum of `N` independent point
scatterers:

```text
s_i = A_i exp(j phi_i)
S   = sum_i s_i
Amplitude = |S|
Phase     = arg(S)
```

The coursework uses `N = 100` scatterers per pixel and a `300 x 300` image.

## Phase configurations

| Case | Phase distribution | Interpretation |
| --- | --- | --- |
| Case 1 | Uniform(-pi, pi) | Fully dispersed phase; strongest destructive/constructive mixing |
| Case 2 | Uniform(-pi/5, pi/5) | Narrow phase range; highly coherent scattering |
| Case 3 | Uniform(-2pi/5, 2pi/5) | Intermediate phase coherence |

## Amplitude configurations

- Fixed amplitude: `A_i = 1`
- Random amplitude: `A_i ~ Uniform(0, 1)`

For `phi ~ Uniform(-a, a)`, the complex mean phasor is:

```text
E[exp(j phi)] = sin(a) / a
```

Therefore the coherent component is largest in Case 2, intermediate in Case 3,
and zero in expectation in Case 1. This explains the strong difference in
mean image amplitude across the three phase ranges.
