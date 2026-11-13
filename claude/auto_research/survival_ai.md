# Survival AI — Offline, Sensor-Aware Emergency Intelligence Device

**Research status:** COMPLETE — desk research; paid/customer validation not started  
**Research as-of date:** 2026-10-02  
**Decision owner:** Hooman Shariati  
**Canonical file:** `/home/colligo/hs_scripts/claude/auto_research/survival_ai.md`

## Contents

- [Research brief and decision](#research-brief-and-decision)
- [Method and evidence rules](#method-and-evidence-rules)
- [Executive conclusion](#executive-conclusion)
- [Competitive landscape](#competitive-landscape)
- [Products and projects in development](#products-and-projects-in-development)
- [Unmet need and defensible wedge](#unmet-need-and-defensible-wedge)
- [Product definition](#product-definition)
- [Technical feasibility and prototype architecture](#technical-feasibility-and-prototype-architecture)
- [Sensors, navigation, connectivity, and power](#sensors-navigation-connectivity-and-power)
- [Safety, medical, legal, licensing, and liability](#safety-medical-legal-licensing-and-liability)
- [Customer, market, business model, and go-to-market](#customer-market-business-model-and-go-to-market)
- [Economics, roadmap, and validation gates](#economics-roadmap-and-validation-gates)
- [Risks, contradictions, and open questions](#risks-contradictions-and-open-questions)
- [Recommendation and scorecard](#recommendation-and-scorecard)
- [Sources](#sources)

## Research brief and decision

**USER-CONFIRMED concept:** A portable, solar-chargeable device combining an offline-capable LLM,
curated survival manuals, maps, herbal and medical references, and sensor inputs. Satellite or cellular
connectivity may supplement it when available, but the core must remain useful offline. Sensors are a
strategic part of the eventual product even if the first prototype is narrower.

**Decision this research supports:** Is there a venture-worthy gap for an integrated “survival AI”
device, or do existing commercial products, open-source stacks, smartphones, satellite communicators,
and rugged-computing substitutes already satisfy the need more safely and cheaply?

**Primary customer:** not fixed in advance. Compare preparedness/go-bag consumers, hikers and
overlanders, disaster-response organizations, and military/public-safety buyers; prefer the segment
with the easiest credible entry, shortest validation cycle, and acceptable liability burden.

**Required output:** exhaustive competition and development-pipeline analysis first, followed by the
full product, technical, customer, market, business-model, prototype, risk, and validation deep dive.

## Method and evidence rules

### Competing hypotheses

1. **Integrated-device thesis:** offline reasoning + curated knowledge + maps + sensors creates enough
   added utility and trust to support a dedicated device and venture-scale business.
2. **Smartphone-substitute thesis:** a modern phone/tablet with offline maps, downloaded references,
   local models, and a power bank/solar panel already solves the job more cheaply and conveniently.
3. **Specialist-device thesis:** Garmin/inReach-class navigation and SOS devices win because reliability,
   certification, battery life, and communications matter more than general intelligence.
4. **Software-first thesis:** the opportunity exists, but the correct wedge is offline software and
   curated/safety-bounded retrieval on customers' existing hardware; dedicated hardware comes later.
5. **Institutional thesis:** consumers are too price-sensitive and liability-prone; the viable customer
   is disaster response, field operations, public safety, or defense.

### Competition search scope

The competitive search must cover:

- direct “survival AI,” emergency AI, offline survival assistant, and outdoor AI products;
- survival/reference apps, offline-first knowledge libraries, and medical/first-aid apps;
- offline maps, navigation, GPS, PLBs, satellite messengers, radios, mesh networks, and SOS devices;
- rugged phones/tablets and expedition/off-grid computing products;
- local/offline LLM apps and dedicated AI hardware;
- Kiwix/Internet-in-a-Box/Raspberry Pi and other DIY/open-source substitutes;
- sensor-rich outdoor devices, watches, weather meters, environmental monitors, and medical tools;
- announced, beta, crowdfunding, patent, research, defense, and open-source projects in development;
- adjacent incumbents able to bundle the feature; and
- the nontechnical substitutes: manuals, maps, training, checklists, and human experts.

For each material competitor or substitute, capture: availability/status, target buyer, form factor,
offline behavior, knowledge and maps, sensor inputs, communications, power/battery, price, business
model, evidence of traction where available, strengths, gaps, and threat to this concept.

### Evidence and confidence

- **VERIFIED:** directly supported by a current primary source or independently corroborated reliable
  sources; include full URL, retrieval date, scope, and source limitation.
- **ASSUMED:** transparent estimate or interpretation; state what would verify or falsify it.
- **UNVERIFIED:** plausible but materially unsupported, stale, inaccessible, or single-sourced where
  corroboration is required; it cannot drive the recommendation alone.
- **USER-CONFIRMED:** Hooman's preference, constraint, or concept—not external proof.

Primary sources (official product pages/manuals, repositories, filings, standards, papers, patents,
regulators) outrank reviews, news, directories, social posts, and crowdfunding claims. “Announced” is
not “shipping”; “offline maps” is not “offline AI”; SOS capability is not proof of general survival
guidance. Blocked or deleted sources remain visible and are not evidence of absence.

### Normalization and quality gates

- Compare real street price and required subscription separately.
- Separate idle, typical, and maximum power; reconcile Wh, W, and claimed runtime.
- Distinguish GPS reception, local sensors, terrestrial messaging, satellite messaging, and formal PLB
  distress signaling.
- Distinguish locally stored documents, retrieval-augmented generation, and model-embedded knowledge.
- Treat medical/herbal guidance as high-risk; examine source licensing, citation fidelity, uncertainty,
  contraindications, and the device's inability to replace professional care.
- Red-team the preferred concept against smartphone, specialist-device, and software-first alternatives.

### Bounded research batches and stopping rule

1. Commercial direct and adjacent competitor inventory.
2. In-development, open-source, crowdfunding, patent, and institutional pipeline.
3. Technical architecture, power/sensors, safety/liability, market, and business feasibility.
4. Central verification, normalization, contradiction search, synthesis, and scorecard.

Stop desk research when additional searches no longer change the competitor taxonomy or product verdict,
or when the next uncertainty requires a prototype benchmark or customer interview rather than more web
search. No external outreach, purchase, publication, or submission is authorized in this round.

## Executive conclusion

### Verdict: do not build the all-in-one device yet

The broad concept is **not novel and is not presently a good hardware bet**. The exact promise—an
offline LLM, survival manuals, maps, optional solar power, and emergency tooling—appeared repeatedly
in this search:

- **VERIFIED:** 18 named direct downloadable mobile offerings are catalogued below, including Power Prepper,
  Gridless, VELORYN, Prepper AI, and Prepper Offline AI. Several already claim citations, camera
  recognition, maps, phone-sensor context, SOS tools, or peer messaging.
- **VERIFIED:** at least eight purchasable or announced USB/standalone products were found, from the
  $69.99 Docket drive to the $2,499 Survival Expert case.
- **VERIFIED:** [Project NOMAD](https://github.com/Crosstalk-Solutions/project-nomad) is a mature,
  free, open-source near-equivalent with offline knowledge, world maps, optional local RAG, documented
  solar/battery hardware, and roughly 38,900 GitHub stars when checked.
- **VERIFIED:** [RACHEL AI](https://worldpossible.org/products/rachel-ai-rachel-6) is a $750 beta
  battery-powered offline knowledge hotspot with AI search from an established offline-education
  organization.
- **VERIFIED:** the hard, safety-critical jobs are already owned by Garmin, ACR, ZOLEO, Apple,
  mapping apps, rugged phones, Kiwix, and specialist sensors.

The search found **no proven commercial product that integrates every component**—rugged standalone
compute, local cited reasoning, offline maps, native satellite SOS, mesh, camera, environmental
sensors, and solar—in one box. This is a search-bounded absence, not proof of a moat. Integration is
technically possible, but it is likely a liability and power/cost burden before it is a durable
advantage. A customer can assemble most of the capability from a phone, a $149–$400 satellite
communicator or $460 PLB, downloaded maps/content, and a power bank.

**Recommendation: CONDITIONAL VALIDATE for software; NO-GO NOW for custom hardware.** Test a
safety-bounded Android application on the customer's existing phone, aimed first at preparedness and
overlanding users. It should use deterministic emergency flows, exact cited excerpts, offline maps,
and optional data from trusted external sensors. Keep distress signaling on a separate certified
PLB/satellite communicator. Build a sensor puck or rugged private-label bundle only if paid tests show
that sensor-guided decisions improve outcomes by at least 20% and buyers will pay at least a $150
premium.

The possible wedge is **not “ChatGPT for survival,” “all the books in your pocket,” or merely “has
sensors.”** Competitors already make those claims. The narrow remaining thesis is:

> auditable offline decision support that combines authoritative, licensed, versioned procedures with
> trusted live sensor inputs, explains what the readings mean, and knows when to abstain.

That thesis is plausible but unproven. Current competitor traction is weak: the strongest direct
Android listing found had only a 5K+ install band, while many iOS products had zero ratings. This may
mean an early category—or a small willingness-to-pay problem. Paid validation, not more desk research,
is now the correct next step.

## Competitive landscape

### 1. Direct standalone and USB products

Availability and prices below were **VERIFIED** on official pages on 2026-10-02. Features are vendor
claims unless independently tested; none of these products was purchased for this research.

| Product | Status / price | Claimed product | Competitive meaning |
|---|---:|---|---|
| [survivorGPT](https://www.getsurvivorgpt.com/) | Batch-2 preorder, $499 | Standalone offline device with manuals, maps, and voice; USB-C and solar-compatible | Direct match; young vendor, no independent traction found |
| [Soren](https://www.sorenkit.com/) | $799 / $999 / $1,399 | Offline appliance, 1–2 TB, local AI, battery and solar options | Direct match; page inconsistently describes Intel N100 and “ARM efficiency cores,” weakening confidence |
| [BunkerTablet](https://bunkerai.io/products/bunkertablet) | Listed sold out; page shows contradictory $799/$999 pricing | Rugged Android tablet, local AI, survival library, GPS/compass | Closest conventional tablet bundle; pricing and delivery evidence are weak |
| [Off Grid AI Core](https://offgridai.io/products/off-grid-ai-core-offline-survival-intelligence-system) | $149.95 USB; bundles to $449.95 | Manuals, maps, and offline AI on removable storage; power/solar bundles | Demonstrates low-cost bundle and severe price pressure |
| [Survival Expert](https://www.survivalexpert.ai/) | Early access, $2,499 | 24-lb Pelican case with Mac mini M4, display, 1,097 manuals, 7B RAG and Jackery battery | Technically credible basecamp class, but not a pocket/go-bag device |
| [Trove Drive](https://trovedrive.com/) | Kickstarter announced; $69 founder / $99 list | USB-hosted 4B model, 380+ books, Wikipedia and maps; host needs 8 GB RAM | Direct announced product; host computer remains the real device |
| [Dracher AI Survival Drive](https://www.drachershop.com/products/dracher-ai-offline-survival-drive) | $119 | USB with 13 models, manuals, maps, vision, voice and citations | Vendor claims 18,003 manuals and 800 customers; both **UNVERIFIED** |
| [Doomsday Media](https://www.doomsday.media/) | Current storefront | Offline AI USB with 400+ manuals | Direct low-cost substitute; no independent traction found |
| [Docket Survival](https://docketoffline.ai/) | In stock, $69.99 sale | Rugged USB-A/C drive, local models and guides | Markets “AI hardware” but has no compute, display, battery, GPS, sensors, or radio |
| [Kiwix Hotspot](https://get.kiwix.org/en/solutions/hotspots/kiwix-hotspot/) | Shipping; $300 bare to $399 Prepper Premium | Raspberry Pi 5, 256 GB NVMe, 4–9 W; up to 24 Wi-Fi clients; preparedness/medical/reference packs; power-bank/solar support | Strong $300 low-power benchmark for the library/hotspot job; standard offer has no LLM |
| [OffGrid AI Toolkit](https://offgridaitoolkit.com/) | $149 Core / $249 Map | Host-computer package with local AI/photo analysis, user knowledge and US maps | Another direct commodity bundle; sales/performance unverified |

RDAP checks showed that survivorGPT, Soren, Trove, and Dracher domains were registered in 2025–2026.
That and the limited independent coverage suggest a recent storefront wave rather than a mature,
validated category. The evidence does **not** establish that these vendors ship at scale.

### 2. Direct mobile software

The inventory below is intentionally broad because this is where the proposed software feature set is
already most densely represented. Store availability, visible ratings, dates, and Android install
bands were **VERIFIED** on official Apple/Google pages; all feature descriptions remain developer
claims.

| Product | Visible traction / price | Claimed offline capabilities | Threat |
|---|---|---|---|
| [Power Prepper](https://play.google.com/store/apps/details?id=com.powerprepper.app) | Android 100+ downloads; plan price not public | 4,100 books, cited local answers, maps, first aid, plant ID, barometer, EMF and seismometer | **Very high:** closest functional match, including sensor story |
| [Gridless](https://gridlessoffline.com/) ([Android](https://play.google.com/store/apps/details?id=com.mywellnessjourney.gridless), [iOS](https://apps.apple.com/us/app/gridless-offline-ai-survival/id6780575307)) | Android 50+; iOS 0 ratings; $4.99 IAP | Local Llama/Gemma RAG, books/Wikipedia, species classifier, maps, tools, local Wi-Fi sharing | **Very high:** exact software implementation |
| [VELORYN](https://play.google.com/store/apps/details?id=com.aegisvectro.veloryn) | Android 1K+; one-time IAP | Local reasoning/vision, GPS/biome/time context, offline world maps, 30+ tools, Bluetooth/Wi-Fi mesh | **Very high:** already claims sensor-aware, context-aware and mesh behavior |
| [Prepper Offline AI](https://play.google.com/store/apps/details?id=com.offlineiasolutions.survivalassitant) | Android 5K+; one-time unlock | Local multimodal model using camera, microphone and text | **High:** largest direct Android install band found |
| [Prepper AI](https://play.google.com/store/apps/details?id=app.prepperai.app) | Android 100+; $9.99/mo or $149.99 lifetime | 74+ military/TCCC/FEMA sources, world topo maps and camera analysis | **Very high:** near-identical buyer and positioning |
| [Post Apoc AI](https://apps.apple.com/us/app/post-apoc-ai/id6760765851) | iOS 0 ratings; $4.99 lifetime | 300+ guides, maps, mesh chat, barometer warning, LiDAR and other phone-sensor tools | **High feature threat;** breadth is unvalidated |
| [Basekit](https://apps.apple.com/us/app/basekit-offline-survival-ai/id6762096706) | iOS 0 ratings; $9.99/mo or $59.99 Pro | Offline multimodal answers and 200+ FEMA/Army/CDC/Red Cross-derived scenarios | High software and safety-positioning threat |
| [ECHO](https://apps.apple.com/us/app/echo-survival-ai/id6756616533) | iOS 0 ratings; $12.99 lifetime | Local model, field guides, GPS, compass, barometer, breadcrumbs and voice | Near-exact phone package |
| [Docket app](https://apps.apple.com/us/app/docket-offline-ai-maps/id6770796644) | iOS 5 ratings; $49.99/yr or $129.99 lifetime | Local models, document RAG, encrypted vault, US maps and routing | Extends Docket beyond its USB product |
| [Worst Case AI](https://apps.apple.com/us/app/worst-case-ai-survival-guide/id6792806254) | iOS 1 rating; $39.99/yr | 1,000+ reviewed, prewritten answers selected locally; sources shown; 130 manuals and maps | **High conceptual threat:** safer non-generative approach |
| [Survival AI — The Ark](https://apps.apple.com/us/app/survival-ai-the-ark/id6746391165) | iOS 134 ratings, 4.49/5 | Offline survival knowledge; technical implementation undisclosed | Best visible direct iOS traction, but opaque |
| [Signal Radar](https://apps.apple.com/us/app/signal-radar-offline-sos-ai/id6759822954) | iOS 4 ratings; $9.99 | Local model/image ID; detects restored cellular service and sends prepared location email | Useful cellular-restoration workflow, not satellite |
| [Survival Assistant](https://apps.apple.com/us/app/survival-assistant-offline/id6505061099) | Android 500+; iOS 0 ratings; about $5–10 | Offline 2,000-species classifier, first aid, maps, GPX and phone sensors | Non-chat substitute; explicitly warns against eating identified species |
| [SurvivalAI](https://apps.apple.com/us/app/survivalai/id6760428067) | iOS 0 ratings; free | 500+ offline articles; Claude/vision services only while online | Direct name, weaker offline intelligence |
| [Northstar](https://apps.apple.com/us/app/northstar-offline-ai/id6759740560) | iOS 7 ratings; $9.99 lifetime | On-phone emergency AI | Narrow exact-positioned substitute |
| [HAVEN](https://havensurvival.com/offline-ai-survival/) | iOS/Android; $24.99 Pro; iOS had 1 rating when checked | Claims 22 on-device models, 19 books, 17 scenarios, maps, camera and Bluetooth mesh | High claimed overlap; quality and traction remain unverified |
| [Custos](https://apps.apple.com/us/app/custos-survival-prepper/id6760218134) | iOS 0 ratings; €14.99/yr or €24.99 lifetime | Static crisis/first-aid library, maps and safe locations | Shows an LLM is not necessary for the baseline job |
| [Survival Kit](https://apps.apple.com/us/app/survival-kit-offline-tools/id6763125045) | iOS 0 ratings; free | Static first aid plus compass, altimeter, Morse and low-battery mode | Free baseline substitute |

**What the direct category says:** supply is abundant, differentiation is weak, pricing is compressed
($4.99 lifetime through roughly $60/year, with a few $129–$150 lifetime offers), and demonstrated
traction is modest. This evidence argues against “offline LLM” as either moat or headline product.

### 3. The modular substitute stack

A prospective buyer does not compare only with direct “survival AI” products. The stronger competitor
is a modular kit whose individual parts are mature and trusted.

| Job | Established options | Current evidence and implication |
|---|---|---|
| Authoritative first aid | [American Red Cross First Aid](https://apps.apple.com/us/app/first-aid-american-red-cross/id529160691), [IFRC First Aid](https://apps.apple.com/us/app/first-aid-ifrc/id1312876691), [GOES](https://goes.health/), [Deployed Medicine](https://apps.apple.com/us/app/deployed-medicine/id1203051672) | Free/low-cost offline protocols; Red Cross had 2,349 iOS ratings. Trust is far above a new AI brand. |
| Offline knowledge | [Kiwix](https://kiwix.org/en/applications/), [Internet-in-a-Box](https://internet-in-a-box.org/) | Mature offline Wikipedia/reference distribution; Internet-in-a-Box explicitly supports solar deployments. |
| Offline maps | [AllTrails](https://apps.apple.com/us/app/alltrails-hike-bike-run/id405075943), [Avenza](https://apps.apple.com/us/app/avenza-maps-offline-mapping/id388424049), [Gaia](https://apps.apple.com/us/app/gaia-gps-mobile-trail-maps/id1201979492), [onX](https://apps.apple.com/us/app/onx-backcountry-3d-trail-maps/id1529165366), [Organic Maps](https://apps.apple.com/us/app/organic-maps-offline-maps-gps/id1567437057), [OsmAnd](https://apps.apple.com/us/app/osmand-maps-travel-navigate/id934850257) | Offline maps/search/routing are commodity; leading products have thousands to over one million ratings. |
| Satellite messaging/SOS | [Garmin inReach](https://www.garmin.com/en-US/p/765374/), [ZOLEO](https://www.zoleo.com/en-us/satellite-communicator), [Bivy Stick](https://www.acrartex.com/products/bivy-stick/), [Apple satellite SOS](https://support.apple.com/en-us/101573) | $149–$400 hardware plus plans; trusted networks, dispatch and long battery life. |
| Formal distress beacon | [ACR ResQLink](https://www.acrartex.com/products/resqlink-400/) | $459.95, no subscription, 406 MHz Cospas-Sarsat, 24+ hours. A hard reliability benchmark. |
| Radio/mesh | [Beartooth](https://beartooth.com/products/beartooth-mk-ii-plus), [BTECH GMRS-PRO](https://baofengtech.com/product/gmrs-pro/), [Rocky Talkie](https://rockytalkie.com/products/expedition-radio), [Meshtastic](https://meshtastic.org/) | Mature voice/data options; regulations, antennas and RF reliability are their own product domains. |
| Rugged compute | [Ulefone Armor 28 Ultra](https://store.ulefone.com/products/armor-28-ultra), [Unihertz Tank 3 Pro](https://www.unihertz.com/products/tank-3-pro), Samsung XCover/Tab Active | $600–$1,000 Android hardware already supplies display, radios, GNSS, camera, sensors, charging and local-AI-capable RAM. |
| Field sensors | [Kestrel 5500](https://kestrelinstruments.com/kestrel-5500-weather-meter), [WeatherFlow WEATHERmeter](https://shop.weatherflow.com/products/weathermeter), [Atmotube PRO](https://atmotube.com/atmotube-pro) | $89.95–$379 specialist instruments already expose calibrated environmental data to phones. |
| Local model runtime | [PocketPal](https://apps.apple.com/us/app/pocketpal-ai/id6502579498), [Private LLM](https://apps.apple.com/us/app/private-llm-local-ai-chat/id6448106860), [Locally AI](https://apps.apple.com/us/app/locally-ai-by-lm-studio/id6741426692) | General local models and document chat are already free or about $5. |

One credible DIY bundle is an existing phone + a $5–$150 survival app + free Kiwix/Organic Maps + a
$149 ZOLEO or $460 subscription-free PLB + commodity power bank/solar panel. A dedicated device must
beat that bundle on tested reliability, battery, safety and integration—not on its checklist.

### 4. Incumbents best positioned to absorb the feature

1. **Garmin** already owns satellite SOS, location, maps, weather, outdoor sensors and an audience
   willing to buy premium hardware.
2. **Apple, Google and Samsung** own the phone, on-device model runtime, camera/GNSS, app distribution
   and increasingly satellite connectivity.
3. **onX, Outside/Gaia, AllTrails and Avenza** own mapping subscriptions and outdoor users.
4. **ACR, ZOLEO, Iridium and Globalstar partners** own emergency communications and dispatch trust.
5. **Red Cross, FEMA, IFRC and Defense Health Agency** own authoritative guidance and institutional
   credibility.
6. **Kiwix, World Possible and Internet-in-a-Box** own open/offline content distribution.

Any one could add a local retrieval assistant more cheaply than a startup could recreate its core
asset. The startup therefore needs a cross-system safety/evaluation layer and proprietary field data,
not a collection of public manuals.

## Products and projects in development

The development pipeline is already active. Repository activity and star/fork counts were read from
GitHub on 2026-10-02; stars are interest signals, not customers.

| Project | Current status | What exists | Signal / implication |
|---|---|---|---|
| [Project NOMAD](https://github.com/Crosstalk-Solutions/project-nomad) / [build deck](https://www.projectnomad.us/deck) | Open source, Apache-2.0; v1.35.0 released 2026-09-29; pushed 2026-10-02 | Kiwix survival/medical knowledge, global ProtoMaps, optional Ollama + Qdrant RAG; documented Pelican-case build with mini-PC, router, 240 Wh battery and optional 110 W solar | ~38.9K stars / 3.9K forks. **Exact, credible adjacent project**; explicitly not a sold product. Author's measured runtime: ~7h normal and ~2h15 continuous AI. |
| [RACHEL AI / RACHEL 6](https://worldpossible.org/products/rachel-ai-rachel-6) | $750 beta | Battery Wi-Fi hotspot with 5+ claimed hours and intent-aware search across offline content | Credible nonprofit/distribution benchmark. Broader RACHEL fleet metrics do not prove beta-product demand. |
| [offline-survival](https://github.com/carlospolop/offline-survival) | Open source; v0.2.1, 2026-06-24 | Desktop library builder combining Kiwix and local AI | Confirms the knowledge/RAG layer is reproducible software. |
| [survival-device](https://github.com/dylanfeltus/survival-device) | Prototype repo; 5 stars, no release; last commit 2026-03-05 | Orange Pi Zero 2W, UPS/7 Ah battery, optional 20 W solar and RAG | Near-exact DIY appliance, but no validation or distribution. |
| [survival-station](https://github.com/JoshKappler/survival-station) | Prototype repo; no release; last commit 2026-08-27 | Local AI, 85 GB Kiwix, US PMTiles and manuals | Another straightforward implementation. |
| [survival-copilot](https://github.com/Chriskatz/survival-copilot) | Hackathon demo; no release; last commit 2026-06-17 | On-device QVAC LLM/RAG over Meshtastic; LoRa, triage and SDR FM implemented; solar/satellite described as future | Exact communications-plus-AI direction already being explored. |
| [offline-triage-node](https://github.com/marras0914/offline-triage-node) | Pre-field-test prototype; last commit 2026-09-02 | Battery edge node, captive Wi-Fi and LLM triage | Highlights medical-use ambition and lack of field validation. |
| [SHTF](https://github.com/XyraSinclair/SHTF) | MIT repo; 6 stars; last commit 2026-09-03 | Printable/offline library, maps and optional AI | Low-traction long-tail substitute. |
| Trove Drive | Announced Kickstarter | See direct-device table | Delivery, certification, and customer count remain unverified. |

Additional exact or near-exact active repositories include
[Rushlight](https://github.com/liekzejaws/rushlight) (Android maps, llama.cpp RAG, Kiwix and peer-to-peer;
75 stars), [refugiOS](https://github.com/Ganso/refugiOS) (bootable Pi/USB knowledge-and-model system;
626 stars), [OutdoorGPT](https://github.com/Rensvandeschoot/Outdoor-GPT) (Pi voice RAG/e-ink/hand-crank
prototype), [SurvivalRAG](https://github.com/bdkoeh/survivalRAG) (70-source RAG and self-evaluation),
[BunkerAI OSS](https://github.com/douglaspriester/bunkerAI) (browser UI, Kiwix, maps, voice and local AI),
and [CyberDeck](https://github.com/sarogamedev/CyberDeck) (Ollama/Kiwix/RAG/maps/LAN/BLE stack). Component
projects such as [Blackbox Node](https://github.com/wadadawadada/blackbox_node),
[MESH-API](https://github.com/mr-tbot/mesh-api), [Delling](https://github.com/tronba/Delling), and
[offgrid-tools](https://github.com/psyb0t/offgrid-tools) already cover local AI over mesh, telemetry,
SDR reception, or bundled services. Most have tiny communities or no field evidence, but together they
show that assembling the software layer is not a defensible technical feat.

### Patent/prior-art warning

**VERIFIED publication:** [WO2024089300A1, “Multimedia autonomous electronic survival device”](https://patents.google.com/patent/WO2024089300A1/en),
priority 2022-10-24 and published 2024-05-02, describes a portable enclosure with a processor, stored
organized survival knowledge, audiovisual/touch interface, battery, RF transceiver, GPS and autonomous
renewable energy generation. The abstract does not require an LLM, but the system overlap is material.
Google Patents displayed “Ceased”; national-family status and claim scope are **UNVERIFIED** and require
patent counsel.

Related active or published work includes AI building-emergency guidance
([US20230360506A1 / US12205447B2](https://patents.google.com/patent/US20230360506A1/en)), a personalized
generative-AI safety manual ([KR20250061982A](https://patents.google.com/patent/KR20250061982A/en)), and
AI/ML situational awareness for responders ([US12520117B2](https://patents.google.com/patent/US12520117B2/en)).
This is not a freedom-to-operate opinion; professional family/classification review is a hardware-launch
gate.

### Institutional and research pipeline

Government work validates disconnected sensor fusion, not demand for this consumer product. NIST funded
a $1.2M [first-responder intelligent assistant](https://www.nist.gov/ctl/pscr/funding-opportunities/past-funding-opportunities/psiap-2022/first-responder-intelligent)
and a $1.4M [GPS-denied wearable navigation project](https://www.nist.gov/ctl/pscr/funding-opportunities/past-funding-opportunities/psiap-2022/navigation-environment-merging)
in 2022; it also studies [AI-enabled smart firefighting](https://www.nist.gov/programs-projects/artificial-intelligence-enabled-smart-firefighting).
DHS describes human-in-the-loop first-responder AI using sensor and communications data
([source](https://www.dhs.gov/science-and-technology/news/2024/10/31/feature-article-ai-means-better-faster-and-more-first-responders)),
and the [DARPA Triage Challenge](https://www.darpa.mil/research/challenges/darpa-triage-challenge) runs
through 2026. An Army SBIR topic offered up to $2M for multimodal generative AI, RAG, geospatial
analysis and hallucination controls in disconnected situational awareness
([source](https://armysbir.army.mil/topics/dynamic-generative-llm-continuous-situational-awareness/));
an awardee/result was not located. These are sophisticated, long-cycle institutional programs, not
evidence that a general-purpose consumer appliance will sell.

## Unmet need and defensible wedge

### What is already commodity

- Downloaded manuals, Wikipedia and maps.
- A local 1–4B language model and document RAG.
- Phone camera, GNSS, barometer, compass and inertial sensors.
- Solar charging as an accessory claim.
- Generic “works when the grid is down” positioning.
- A long feature list assembled from open-source components.

### What could still matter

The unmet need is not access to information; it is making the correct next decision under stress,
with incomplete information, while preserving battery and never creating false confidence. The most
defensible version would provide:

1. **Auditable authority:** licensed, versioned sources; exact excerpts and page/edition citations;
   provenance shown before generated explanation.
2. **Safety-bounded orchestration:** deterministic triage/checklist/routing logic; explicit uncertainty,
   contraindications, and abstention; model used for language, not truth.
3. **Validated sensor-to-action mappings:** e.g., pressure trend + location + forecast cache; shelter
   CO2/PM trend; water measurements—each tied to a reviewed decision tree and field evaluation.
4. **Interoperability:** read from existing phones, Kestrel-class instruments, NOAA receivers and
   Garmin/ZOLEO-class devices without trying to replace their certified safety functions.
5. **Evidence from field outcomes:** a proprietary corpus of anonymized scenarios, failure modes,
   sensor traces and expert adjudications. This—not model weights—is the potential data moat.

“Has sensors” is insufficient: Power Prepper, VELORYN and Post Apoc AI already claim phone-sensor
context. A sensor feature earns hardware complexity only if a controlled field test shows at least a
20% improvement in correct task completion or time-to-decision, and buyers show willingness to pay a
$150+ premium.

## Product definition

### Recommended first product: FieldGuide AI for Android (working description)

An offline-first, safety-bounded decision-support app for preparedness and overlanding users. It runs
on a recent Android phone, stores regional maps and a small authoritative corpus, retrieves exact
passages, and guides the user through reviewed emergency procedures. It may ingest phone and optional
Bluetooth sensor readings, but it never claims to replace a PLB, medical professional, or certified
alarm.

**V1 includes**

- offline scenario intake by touch and voice, with a prominent “signal/SOS first” branch;
- deterministic flows for a tightly bounded initial set such as hypothermia prevention, lost-person
  actions, water treatment, shelter ventilation, weather deterioration and vehicle immobilization;
- hybrid keyword + semantic retrieval, with title, edition, excerpt, page and confidence shown;
- offline regional vector/topographic maps, waypoints and breadcrumbs;
- phone context: time, location, heading, altitude/pressure trend, battery and weather cache;
- optional BLE environmental feed, clearly labeling sensor quality and freshness;
- signed, versioned content/model packages with rollback;
- low-power “cards only” mode when battery is scarce.

**V1 explicitly excludes**

- autonomous distress signaling, a first-party satellite modem, or replacement for a PLB;
- diagnosis, drug dosing, medical-device interpretation, or treatment personalization;
- plant/mushroom edibility decisions and herbal dosing/treatment;
- unsupported environmental alarms such as using a VOC sensor as a life-safety CO detector;
- open-ended ingestion into the high-trust corpus without curation and rights review.

### Eventual product ladder—only after gates

1. Android software on the user's phone.
2. Optional BLE environmental puck using certified/calibrated components where possible.
3. Private-label rugged Android kit with tested power and mounts.
4. Basecamp/institutional appliance only if field organizations demonstrate pull.

A custom phone/tablet motherboard is deliberately absent. It adds manufacturing, thermal, RF,
battery, certification, repair, inventory and support risk without yet proving a unique customer job.

## Technical feasibility and prototype architecture

### Feasible architecture

```text
camera / GNSS / phone sensors / optional BLE instruments
                         |
                  typed sensor gateway
                         |
deterministic emergency rules + map/routing engine + source retriever
                         |
      cited evidence bundle + confidence / contraindications
                         |
             small local LLM for explanation only
                         |
     answer + exact sources + next checks + abstain/SOS path
```

- **Runtime:** llama.cpp, MediaPipe, ExecuTorch or MLC-class mobile runtime. Google documents
  [on-device LLM inference on Android](https://developers.google.com/edge/mediapipe/solutions/genai/llm_inference/android),
  and [llama.cpp](https://github.com/ggml-org/llama.cpp) supports quantized local inference.
- **Model:** test 1–4B instruction models at 4-bit quantization; 7–8B belongs only on high-RAM/basecamp
  hardware. Approximate weight storage is 1.5 GB for 3B Q4, 2 GB for 4B Q4 and 4 GB for 8B Q4 before
  runtime/KV-cache overhead (**ASSUMED arithmetic**, verify on target devices).
- **Retrieval:** SQLite FTS5/BM25 plus compact embeddings and reranker; retrieve only the small relevant
  passage set. Maps, routing, sensor thresholds and emergency trees remain deterministic.
- **Trust boundary:** model output cannot override a protocol, fabricate a citation, alter a measured
  value or silently convert units. Uncertainty and stale/missing sensor data remain visible.
- **Updates:** signed content manifests, checksums, local audit log and rollback. Core emergency cards
  remain available if the model or index fails.

A phone proof is feasible now. NVIDIA's [Jetson Orin Nano Super](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/)
is $249, 8 GB and configurable at 7/15/25 W, but a Jetson case is a basecamp demonstrator rather than a
good go-bag default. It consumes more power and recreates functions already present on a phone.

### Required technical acceptance tests

- cold offline start under 10 seconds and median answer under 5 seconds on target hardware;
- top-3 retrieval recall at least 95% on the curated scenario set;
- citation-entailment accuracy at least 95%;
- zero severity-1 harmful errors in an expert-adjudicated test suite;
- at least 90% correct abstention on insufficient or contradictory evidence;
- 72-hour mixed-use field duty cycle with the chosen phone/power configuration;
- offline update verification, rollback, corruption recovery and graceful no-model fallback;
- drop, water, temperature, glove, glare, depleted-battery and disconnected-sensor tests.

## Sensors, navigation, connectivity, and power

### Sensor roadmap

| Tier | Inputs | Recommendation |
|---|---|---|
| 0: phone | GNSS, camera, accelerometer/gyro, compass, barometer where available, mic, battery | Use immediately; calibrate for device variance and make quality visible |
| 1: optional BLE puck | temperature, humidity, pressure; PM2.5/smoke; CO2 for enclosed shelter; optional wind/UV | Prototype after software validation; use external placement to avoid self-heating/enclosure bias |
| 2: separate certified instruments | UL-listed CO alarm, radiation meter, thermal camera, water test instrument | Integrate readings where APIs permit; do not recreate safety certification |
| 3: raw medical readings | thermometer and pulse oximeter | Display/record only under reviewed protocols; no diagnosis or personalized dosing |

The [Bosch BME688](https://www.bosch-sensortec.com/en/products/environmental-sensors/gas-sensors/bme688/)
and [Sensirion SCD41](https://sensirion.com/products/catalog/SCD41) show that compact environmental
sensing is feasible. Productization is harder: vented sensing conflicts with waterproofing; placement,
condensation, contamination, drift and calibration can make a plausible number dangerously wrong.

### Connectivity boundary

- Core maps, procedures and inference work offline.
- Opportunistically update weather, content and model packages over cellular/Wi-Fi.
- Interoperate with Garmin/ZOLEO/Bivy-class satellite products; do not route or suppress their SOS.
- Meshtastic/local Wi-Fi can support noncritical peer messages, but must not be described as guaranteed
  rescue connectivity.
- Include NOAA weather-radio reception only as a separately tested module/accessory; do not imply that
  internet weather cache equals broadcast alerts.

### Power reality

Using a 5,100 mAh phone battery at roughly 3.85 V gives about 19.6 Wh. At 80% usable energy and 6 W
continuous inference/screen load, runtime is about 2.6 hours; intermittent field use should be much
longer but needs measurement. A nominal 100 Wh bank at 85% delivery supplies about 85 Wh, roughly 4.3
such phone charges.

For a Jetson system with 4–6 W of display/router/storage overhead, the same usable 85 Wh yields roughly:

| Jetson mode + peripherals | Approx. load | Continuous runtime from nominal 100 Wh |
|---|---:|---:|
| 7 W + 5 W | 12 W | 7.1 h |
| 15 W + 5 W | 20 W | 4.25 h |
| 25 W + 5 W | 30 W | 2.83 h |

These are **ASSUMED engineering calculations**, not measured product claims. They align directionally
with Project NOMAD's published measurements: about 7 hours of normal use and 2h15 of continuous AI
from its 240 Wh power station.

Current 50–100 W folding panels cost roughly $250 and weigh around 3.1–3.2 kg in inspected Goal Zero
and Jackery listings. At four peak-sun-hours and 50% total field yield, a 50 W panel produces about
100 Wh/day and a 100 W panel about 200 Wh/day (**ASSUMED**). Shade, orientation, heat, clouds and
winter can cut that severely. “Solar chargeable” is easy; “energy independent in an emergency” is not.

## Safety, medical, legal, licensing, and liability

### The central product risk

In a survival context, a fluent wrong answer can be worse than no answer. NIST's
[Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) identifies confabulation
and dangerous recommendations among material generative-AI risks. The product must be designed as a
cited protocol navigator, not an oracle.

Research benchmarks reinforce the concern. [DisasterQA](https://arxiv.org/abs/2410.20707) found that
disaster-domain knowledge and decision reliability still needed improvement, while the 2026
[DORA benchmark](https://arxiv.org/abs/2605.11633) reported persistent grounding, tool-argument and
long-workflow failures across 515 expert disaster-response tasks. These papers are not field trials,
but they are contrary evidence against trusting general-model fluency in emergencies.

Required controls:

- emergency contact/SOS guidance before extended chat where appropriate;
- exact-source-first UI and a deterministic protocol as the controlling artifact;
- explicit “unknown,” “sensor stale,” “sources disagree,” and “seek professional help” states;
- expert-authored scenario tests, red-team cases, unit and dosage checks, and release blocking;
- no model-generated changes to medication, evacuation, rescue or hazardous-material rules;
- independent certified alarm/PLB paths that continue if the app, phone or model fails.

Herbal medicine and wild-food identification are especially poor V1 features. Poison Control warns of
serious poisoning from wild mushrooms ([source](https://www.poison.org/articles/wild-mushroom-warning));
competitors themselves refuse edibility verdicts. Static identification confidence is not safety.

### Medical/regulatory boundary

Whether software becomes a regulated medical device depends substantially on intended use and whether
it diagnoses, treats, or interprets patient-specific signals. FDA's governing device-software framework
and statutory exclusions need specialist review before launch; see [21 USC §360j(o)](https://www.law.cornell.edu/uscode/text/21/360j).
The safe initial scope is general educational guidance and deterministic first-aid protocols, not
diagnosis, dosing or interpretation of physiological data. This report is not legal advice.

### Content and map rights

A “library of everything” is not automatically licensable:

- US federal works may be public domain, but third-party material embedded in them may not be; see
  [USA.gov copyright guidance](https://www.usa.gov/government-copyright) and 17 USC §105.
- Red Cross [terms](https://www.redcross.org/terms-of-use.html) restrict use; app availability is not a
  commercial redistribution license.
- WHO material commonly carries licenses such as CC BY-NC-SA, which may conflict with a commercial
  product; verify item by item.
- OpenStreetMap is under the [ODbL](https://www.openstreetmap.org/copyright), with attribution and
  share-alike obligations depending on use.
- Kiwix software availability does not grant commercial rights to every packaged corpus; libkiwix's
  GPL obligations also require architecture review.

Before a paid beta, create a rights matrix with owner, exact edition, license, derivative/RAG rights,
attribution, update cadence and medical review. Content clearance is a launch gate, not cleanup work.

### Physical product obligations

A real accessory/device may trigger FCC/IC radio compliance, Bluetooth qualification, EMC, battery
transport testing such as UN 38.3, product safety, ingress/drop claims and labeling. IP68 cannot be
inferred from a waterproof-looking case. Product-liability insurance and counsel are mandatory before
customers rely on hardware or medical/environmental interpretations.

## Customer, market, business model, and go-to-market

### Best first customer

| Segment | Ease | Why / why not | Verdict |
|---|---:|---|---|
| Preparedness consumers / overlanders | Highest | Reachable communities, own Android hardware, buy kits/sensors, recurring drills; lower procurement friction | **Start here**, especially vehicle/basecamp users where weight and charging are less punishing |
| Hikers/backpackers | Medium | Large outdoor spend, but extreme weight/reliability demands and entrenched Garmin/map apps | Use as test users, not the first broad positioning |
| Disaster-response NGOs/teams | Low–medium | Strong offline need and possible higher WTP, but deployment, training, multilingual content and procurement slow sales | Phase 2 design partners after consumer proof |
| Public safety / military | Lowest | Security, accreditation, contracting, ruggedization and incumbent requirements; high consequence of error | Do not target first |

The easiest credible entry is therefore **preparedness/overlanding Android users**, not generic
consumers. They tolerate a kit, power bank and optional sensors better than ultralight hikers and are
much faster to reach than institutions.

### Pricing hypotheses—not validated demand

- App: $59–$99 one-time for a core offline regional pack.
- Optional content/model/map updates: $29–$59/year; core purchased content remains usable offline.
- Sensor puck: $249–$399 only after the sensor value gate.
- Rugged private-label kit: $999–$1,499 only after demonstrated pull.

Direct apps anchor much lower, so premium pricing requires proof of expert review, auditability and
better field performance. Subscription-only emergency access is likely trust-negative; sell durable
offline capability and charge for updates/services.

### Go-to-market test

Recruit from preparedness, overlanding, amateur-radio/Meshtastic and outdoor safety communities. Do
not advertise “AI knows how to save you.” Demonstrate three before/after field scenarios in which the
system identifies missing facts, consumes a real sensor reading, cites the exact procedure and either
recommends a safe next step or abstains. Compare directly against a phone with Kiwix/maps and a static
checklist.

No robust TAM is claimed in this round. Garmin reported roughly $2.054B of 2025 outdoor-segment sales
in its filing, which validates outdoor-electronics spend but says almost nothing about willingness to
pay for survival AI. The weak direct-app traction is the more decision-relevant evidence today.

## Economics, roadmap, and validation gates

### Capital and effort

| Stage | Scope | Estimated capital | Time | Evidence status |
|---|---|---:|---:|---|
| Phase 0 | Android proof, licensed starter corpus, maps, evaluation suite, expert review | $25K–$100K | 6–10 weeks | **ASSUMED**; within Hooman's capital range |
| Phase 1 | Paid beta and field tests on user phones | Additional $10K–$40K | 2–3 months | **ASSUMED** |
| Phase 2 | BLE environmental-puck prototypes | $25K–$50K prototype; $150K–$400K productization | 4–12 months | **ASSUMED**; certification/calibration dominate |
| Phase 3 | Custom integrated rugged device | $750K–$2M | 12–24+ months | **ASSUMED**; outside current side-business constraints |

A proof can cost nearly zero in compute hardware if it uses Hooman's existing compatible Android
phone. A representative prototype sensor puck is roughly $85 in dev boards, sensors, battery and case
before engineering/certification. A Jetson/Pelican/basecamp demonstration was estimated around $1,550,
but it would validate assembly rather than demand.

### Validation sequence

1. **Six-to-ten-week software proof:** 20–30 high-value scenarios, 3 model candidates, authoritative
   citations, regional maps, deterministic flows and failure tests. No custom enclosure.
2. **Customer discovery and paid gate:** interview 30 preparedness/overlanding users and collect at
   least 20 paid $79 preorders from no more than 500 targeted prospects. Refundable intent is weaker;
   actual payment is the signal.
3. **Field comparison:** static cards vs cited RAG vs sensor-aware product in timed, blinded scenarios.
4. **Sensor experiment:** attach existing BLE instruments first. Build a puck only if it improves
   correct task completion or time-to-decision by at least 20% and buyers accept a $150+ premium.
5. **Private-label hardware:** only after software retention, support burden and power tests pass.

### Kill conditions

- Fewer than 20 paid preorders from 500 well-targeted prospects.
- Fewer than 30% of interviews identify a recurring decision that existing phone/maps/manual tools do
  not handle adequately.
- Expert tests reveal any severity-1 harmful error after the safety architecture is implemented.
- Retrieval/citation/abstention gates cannot be met on a target phone.
- No clean commercial rights path for the minimum corpus and maps.
- Sensor context fails the 20% outcome-improvement or $150 willingness-to-pay gate.
- Customer acquisition cost exceeds 30% of first-year gross profit in the initial channel.
- The experience is not clearly better than Kiwix + map app + static protocol cards.

### Venture-scale reality

This could become a useful niche product. It is not yet a venture-scale thesis. Venture scale would
likely require 100K+ paying users, institutional deployments, or a broader offline field-operations
platform spanning disaster response, remote work and industrial safety. The consumer hardware path
alone is more likely to become a complex, support-heavy small business than a high-margin venture.

## Risks, contradictions, and open questions

### Adverse evidence that changed the thesis

1. **Exact competition is dense.** The initial intuition that this was an open product category is
   false. At least 20 apps, multiple purchasable devices and several active open-source builds were
   found.
2. **Sensors are not automatically the moat.** Competitors already claim barometer, environmental,
   camera and context-aware features. Proprietary validated sensor-to-decision data might be a moat;
   the sensors themselves are not.
3. **Generation may be the wrong safety primitive.** Worst Case AI's reviewed static answers and the
   authoritative Red Cross/Deployed Medicine apps directly challenge the assumption that an LLM
   improves emergencies.
4. **The phone is unusually strong hardware.** It already integrates the expensive components and
   receives platform investment in local AI and satellite services.
5. **Low visible traction is ambiguous but concerning.** Dense supply with mostly zero-to-low ratings
   may represent a young category, poor product quality, or weak demand. Only payment tests resolve it.
6. **Solar creates false comfort.** A panel is not guaranteed energy under trees, smoke, storms or
   winter; stored energy and disciplined duty cycling matter more.
7. **More content can make the product worse.** Duplicated, stale, conflicting or unlicensed manuals
   degrade retrieval and increase legal/safety risk.

### Unresolved questions requiring experiments, counsel, or customers

- Which three recurring, high-stakes decisions actually cause target users to reach for multiple
  tools today?
- Does cited, sensor-aware guidance outperform a laminated checklist under stress?
- Which external sensors are trusted enough and common enough to integrate without owning hardware?
- What content can be commercially licensed and kept current at sustainable cost?
- Will customers pay a premium for safety review, or do they perceive a $5 app as equivalent?
- Can the app maintain useful latency, heat and battery on a range of rugged Android devices?
- Can marketing avoid unsafe reliance while still communicating a compelling benefit?

### Research limitations

The search covered official app stores, vendor sites, repositories and leading adjacent categories,
but cannot prove universe-wide absence. Apple does not expose downloads; Google exposes only coarse
install bands; vendor feature/manual/customer/runtime claims were not bench-tested; non-English stores,
private defense work and unpublished prototypes may be missing. Several vendor pages are internally
inconsistent. No product was purchased, no patent opinion was commissioned, and no customer was
interviewed. Those limits are reflected in the verdict.

## Recommendation and scorecard

### Decision

- **Dedicated all-in-one survival device:** **4.4/10 — NO-GO NOW.** Technically buildable but crowded,
  commodity at the software layer, expensive and risky at the hardware layer, and outcompeted on
  rescue trust by specialist products.
- **Safety-bounded, sensor-aware Android product:** **5.9/10 — CONDITIONAL VALIDATE.** Founder-buildable
  and cheap to test, but demand, safety advantage, content rights and sensor value are unproven.

| Dimension | Weight | Android-first | Dedicated device | Reason |
|---|---:|---:|---:|---|
| Customer pain / urgency | 15% | 6 | 6 | Offline emergencies are real; frequency and willingness to pay are unclear |
| Competition / differentiation | 15% | 4 | 3 | Dense apps, exact projects and powerful modular substitutes |
| Technical feasibility | 15% | 8 | 5 | Phone implementation is straightforward; custom device adds power/RF/rugged complexity |
| Safety / regulatory feasibility | 15% | 4 | 3 | High consequence of error; hardware and sensing add obligations |
| Founder-market fit | 15% | 8 | 5 | AI/software fits Hooman; consumer hardware, field medicine and outdoor brand-building fit less |
| Capital / speed to test | 10% | 8 | 3 | App fits $25–150K and 6–10 weeks; productized hardware does not |
| Economics / willingness to pay | 10% | 4 | 5 | App price pressure; hardware has higher ASP but worse margin/support risk |
| Moat / expansion potential | 5% | 4 | 5 | Only evaluated procedures and field data could become defensible |
| **Weighted total** | **100%** | **5.9** | **4.4** | Dedicated score is 4.35 before one-decimal rounding; neither is a build commitment |

### Recommended next action

Do not design a case, PCB, satellite radio or solar bundle. Build the smallest Android proof that can
answer one question: **does audited, sensor-aware offline guidance measurably beat the tools people
already carry?** If the paid and field gates pass, integrate existing certified peripherals and only
then revisit a rugged bundle. If they fail, stop—the open-source and modular stacks already solve the
“books are heavy” problem.

## Sources

All online sources were retrieved 2026-10-02 unless a release/filing date is stated. Material direct
sources are linked inline above. Additional primary references used for technical and safety analysis:

- NIST, *Artificial Intelligence Risk Management Framework: Generative AI Profile*:
  https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
- Google, Android on-device LLM inference:
  https://developers.google.com/edge/mediapipe/solutions/genai/llm_inference/android
- llama.cpp repository: https://github.com/ggml-org/llama.cpp
- NVIDIA Jetson Orin Nano Super:
  https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/
- OpenStreetMap copyright/license: https://www.openstreetmap.org/copyright
- US government copyright guidance: https://www.usa.gov/government-copyright
- American Red Cross terms: https://www.redcross.org/terms-of-use.html
- US medical-device software statute, 21 USC §360j(o):
  https://www.law.cornell.edu/uscode/text/21/360j
- Poison Control wild-mushroom warning:
  https://www.poison.org/articles/wild-mushroom-warning
- Bosch BME688: https://www.bosch-sensortec.com/en/products/environmental-sensors/gas-sensors/bme688/
- Sensirion SCD41: https://sensirion.com/products/catalog/SCD41

**Source audit note:** official store/vendor pages verify that a listing and stated offer existed, not
that claims are accurate or units shipped. GitHub activity verifies public development, not production
readiness or commercial demand. Estimates and inferences are labeled **ASSUMED**; unsupported vendor
traction/runtime/library claims remain **UNVERIFIED** and do not drive the recommendation.
