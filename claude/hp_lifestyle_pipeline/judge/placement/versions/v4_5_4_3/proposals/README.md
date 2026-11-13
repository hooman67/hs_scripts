# Deterministic asymmetric-foreshortening helper proposal

This isolated proposal converts structured coordinates for at least two distinct
visible `support_side` edges into a proposed
`support_anatomy / malformed_connected_furniture` finding when:

- the edges have comparable absolute vertical displacement;
- one horizontal run is below 3% of tabletop width; and
- the opposite horizontal run is above 15% of tabletop width.

It is not imported by the V4.5.4 runtime. Integration should wait for root review
and validation because the helper cannot independently determine whether visible
furniture is an ordinary rectilinear tabletop or a legitimate non-rectangular,
hinged, tapered, curved, cropped, or occluded construction. It also trusts model
endpoint traces and a supplied tabletop-width measurement. The 3% and 15%
thresholds come from one human-reviewed failure and therefore carry material
overfit and false-positive risk. Before integration, evaluate the rule against
held-out rectilinear and non-rectilinear furniture, calibrate vertical-run
comparability, and add structured construction-type and tabletop-width fields.
