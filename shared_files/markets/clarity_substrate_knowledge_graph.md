# Clarity Substrate Knowledge Graph — Market Analysis Domain
## Initialized 2026-04-15

### Node Registry
1. CRE-distress (office vacancy, regional bank exposure)
2. Private-credit-defaults (record 9.2%, covenant-lite, BDC NAV erosion)
3. Tariff-shock (middle-market revenue collapse catalyst)
4. Consumer-credit-stress (credit card delinquencies, auto loan stress)
5. Middle-market-borrowers (CONVERGENCE NODE — overlaps nodes 1,2,3)
6. Correlation-spike-risk (conjunction of multiple nodes firing)
7. Institutional-transmission (BDCs -> banks -> insurers -> pensions -> retail)

### Edge Registry (with NAL confidence)
- tariff-shock -> middle-market-revenue-collapse: stv 0.6 0.51
- middle-market-revenue-collapse -> private-credit-defaults-acceleration: stv 0.48 0.326
- private-credit-defaults -> BDC-NAV-erosion: stv 0.782 0.68
- BDC-NAV-erosion -> institutional-redemption-pressure: stv 0.587 0.408
- institutional-redemption-pressure -> forced-liquidation: stv 0.352 0.214
- forced-liquidation -> credit-contagion: stv 0.246 0.128
- CRE-distress AND private-credit-defaults -> correlation-spike: stv 0.56 0.45

### Comparative Cascade Model
| Dimension | 2008 | 2020 | 2025 (projected) |
|-----------|------|------|-------------------|
| Attenuation | Low (0.95->0.85) | Steep then reversed | Steep (0.8->0.246) |
| Policy access | Slow but available | Rapid and direct | Limited — no private loan facility |
| Self-reinforcing phase | Reached (Lehman) | Truncated pre-threshold | Not yet reached |
| Resolution timeline | 18+ months | 3 months | Unknown — policy gap suggests longer |
| Key amplifier | Leverage + opacity | Speed of onset | Policy inaccessibility + PE conflicts |

Core asymmetry: private credit is simultaneously the highest-risk asset class and the least accessible to central bank intervention tools.
