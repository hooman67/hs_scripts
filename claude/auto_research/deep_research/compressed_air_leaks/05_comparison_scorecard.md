# Comparison Scorecard: Compressed Air Leak Detection

## Scoring

| Dimension | Weight | Score (1-10) | Reasoning |
|-----------|--------|--------------|-----------|
| Capital required (lower = better) | 15% | **9** | ~$1,600 to working prototype; ~$15K to commercial pilot. One of the lowest-capital ideas in portfolio |
| Time to first revenue | 15% | **7** | ~20 weeks to pilot; ~6 months to first paying customer. Moderate — hardware + ML training takes time |
| Competitive moat strength | 15% | **6** | ML model trained on real factory data is defensible but replicable. No strong IP. Network effects from parameter tuning across plants add up over time |
| Technical risk (lower = better) | 10% | **8** | Core tech is proven (MEMS mic + FFT + ML). Main risk is noise rejection in real environments, but FLIR proved this works with same sensor |
| Market size (SAM) | 10% | **9** | Universal — every factory with compressed air. Hundreds of thousands of plants in US alone. SAM easily $500M+ |
| Founder-market fit (your skills) | 15% | **7** | Strong on ML/cloud, moderate learning curve on embedded/PCB. No prior manufacturing industry connections (need to build from scratch) |
| Customer accessibility | 10% | **8** | Maintenance managers are reachable via LinkedIn, trade shows, and manufacturing associations. Mid-market buyers can approve $5K without board sign-off |
| Scalability beyond prototype | 10% | **8** | Hardware is simple (contract manufactured at scale); SaaS revenue grows with each plant; minimal marginal cost per additional node |

### Weighted Total: **7.55 / 10**

Calculation: (9×0.15) + (7×0.15) + (6×0.15) + (8×0.10) + (9×0.10) + (7×0.15) + (8×0.10) + (8×0.10) = 1.35 + 1.05 + 0.90 + 0.80 + 0.90 + 1.05 + 0.80 + 0.80 = **7.65**

---

## Key Strengths

1. **Irrefutable ROI** — "We found $30K/year in leaks" is concrete, measurable, and immediately actionable
2. **Universal market** — compressed air is in every factory, everywhere
3. **Low capital requirement** — prototype buildable for <$2K, commercial for <$15K
4. **Simple technology** — no complex hardware, no novel physics, proven components
5. **Recurring revenue** — monitoring is ongoing, not one-time hardware sale

## Key Weaknesses

1. **No strong patent moat** — the approach is conceptually simple; barrier is execution + data, not IP
2. **Embedded hardware learning curve** — Hooman would need to learn PCB design + firmware (or hire)
3. **Sales requires manufacturing industry relationships** — need to build from scratch
4. **UE Systems overlap** — their OnTrak product partially addresses this market (though positioned differently)
5. **Hardware manufacturing complexity** — even simple hardware has supply chain, quality control, returns

## Comparison Notes

- Scores HIGHER than pure-software ideas on "market size" and "customer accessibility" (universal need, simple buyer)
- Scores LOWER than pure-software ideas on "moat strength" and "scalability" (hardware always harder)
- The $1,600 prototype cost makes this ideal for weekend validation before committing
