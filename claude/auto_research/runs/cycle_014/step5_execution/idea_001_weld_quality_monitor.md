# Execution Plan: AI Weld Quality Monitoring from Electrical Signatures

## Summary
- **Value prop**: Know every weld is good the instant it's done — no waiting for costly inspection
- **Hardware**: Hall-effect current sensor ($10) + voltage divider ($2) + ADC + MCU + WiFi = $80 BOM, sell at $500/station
- **SaaS**: $150/month per station (weld log, defect alerts, compliance reports)
- **Capital needed**: ~$250K (signal processing + ML + pilot with fab shops, 7 months)
- **Target**: Small/medium fabrication shops, structural steel, pressure vessel manufacturers
- **Revenue Year 1**: 300 stations × $500 + 300 × $150/mo × 8mo = $150K + $360K = **$510K**
- **Scale potential**: 500K+ welding stations in US manufacturing alone. At 1% penetration = 5000 stations × $1800/year = $9M ARR

## Key technical approach
- Clamp-on hall-effect sensor captures current waveform at 100kHz sampling
- Voltage tap captures arc voltage
- ML trained on good/bad weld signatures (porosity, undercut, cold lap, burn-through each have characteristic waveform patterns)
- Real-time classification with confidence score: Green (good) / Yellow (suspect) / Red (defect)
- Integration with AWS Welding Procedure Qualification Records (PQR)

## Why electrical signature works
Published research (IIW, AWS) shows that 90%+ of common weld defects produce detectable anomalies in the voltage-current relationship:
- Porosity → irregular arc voltage spikes
- Undercut → excessive current during final pass
- Cold lap → voltage drops indicating poor fusion
- Burn-through → sudden current spike + voltage collapse
