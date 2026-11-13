# Execution Plan: Acoustic Bird Monitoring for Wind Farm Compliance

## Summary
- **Value prop**: 24/7 automated bird species detection replaces $50-100K/year human surveyors and minimizes unnecessary turbine curtailment
- **Hardware**: Weatherproof mic array ($200) + edge compute ($150) + solar/battery ($100) + cellular ($50) = $500 BOM per node, sell at $2K. 5-10 nodes per wind farm.
- **SaaS**: $500/month per farm (species reports, curtailment triggers, compliance documentation)
- **Capital needed**: ~$250K (acoustic ML engineer + ornithologist consultant + hardware + wind farm pilot, 7 months)
- **Target**: Wind farm developers/operators (NextEra, Ørsted, Enel, Invenergy) needing ESA/MBTA compliance
- **Revenue Year 1**: 50 farms × $15K hardware + 50 × $500/mo × 8mo = $750K + $200K = **$950K**
- **Foundation**: BirdNET (Cornell Lab open-source) provides pre-trained bird species ID model → fine-tune for turbine noise environments
- **Regulatory driver**: Every US wind farm needs an Eagle Conservation Plan (ECP); automated detection enables real-time Smart Curtailment (only stop turbines when eagles are actually present, not blanket curtailment by time-of-day)
