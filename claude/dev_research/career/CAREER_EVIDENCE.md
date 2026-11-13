# Career Evidence — Canonical Inventory

This file separates source-backed facts, Hooman's direct account, interpretation, and open gaps.
It is not résumé prose yet.

## Contents

- [November 9 current facts and source corrections](#november-9-current-facts-and-source-corrections)
- [Evidence labels](#evidence-labels)
- [Source inventory](#source-inventory)
- [Provisional strengths — not yet résumé claims](#provisional-strengths--not-yet-résumé-claims)
- [Evidence needed for each Adobe accomplishment](#evidence-needed-for-each-adobe-accomplishment)

## November 9 current facts and source corrections

- **USER-CONFIRMED — 2026-11-09:** lives in San Jose, California; still employed at Adobe with
  the official Machine Learning Engineer, ASML title (October 2023–Present). Historical Vancouver
  employment locations remain unchanged.
- **USER-CONFIRMED — 2026-11-09:** no sponsorship needed for applying. This is not evidence of a
  specific immigration status or a guaranteed answer to future-sponsorship questions.
- **VERIFIED — CVF primary page retrieved 2026-11-09:** “Towards Autonomous Mining via
  Intelligent Excavators,” Hooman Shariati, Anuar Yeraliyev, Burhan Terai, Shahram Tafazoli, Mahdi
  Ramezani; Proceedings of CVPR **Workshops**, 2019, pages 26–32.
  https://openaccess.thecvf.com/content_CVPRW_2019/html/cv4gc/Shariati_Towards_Autonomous_Mining_via_Intelligent_Excavators_CVPRW_2019_paper.html
  This corrects the older résumé's abbreviated venue. Specific contribution still needs Hooman's
  account; author order alone does not establish it.
- **SOURCE AVAILABILITY — 2026-11-09:** raw résumé/check-in files previously read under
  `/mnt/localssd` are now missing. The inventory below is a durable historical synthesis, not a
  fresh reread of those raw inputs. Preserve its source-specific confidence labels.

## Evidence labels

- **RESUME-DOCUMENTED:** appears in the pre-Adobe résumé; self-authored historical evidence.
- **CHECKIN-SELF-REPORTED:** appears in Hooman's employee response in an Adobe check-in.
- **CHECKIN-MANAGER-CORROBORATED:** appears in the manager response in an Adobe check-in.
- **CHECKIN-GOAL:** documented as an intended goal, not evidence that it was completed.
- **USER-CONFIRMED:** stated directly by Hooman in this project.
- **PUBLICLY-VERIFIABLE:** supported by a public artifact such as a paper or repository.
- **INFERENCE:** interpretation that must not be presented as fact.
- **OPEN:** missing evidence or clarification.

## Source inventory

### Pre-Adobe résumé

Source: `/mnt/localssd/hs_aupera_resume.pdf`; inspected 2026-09-15.

- **RESUME-DOCUMENTED:** M.Eng. Computer Engineering (Machine Learning), University of British
  Columbia, 2018, stated GPA 4.0.
- **RESUME-DOCUMENTED:** B.A.Sc. Computer Engineering, University of British Columbia, 2014,
  stated GPA 3.8.
- **RESUME-DOCUMENTED:** Principal Engineer, Deep Learning at Aupera Technologies beginning May
  2021; oversight of a five-person CV team and six-person software team; responsibility spanning
  requirements, customer discussions, solution design, implementation, deployment, and support.
- **RESUME-DOCUMENTED:** Computer Vision Engineer at Aupera, October 2019–May 2021; customer
  requirements, CV research/prototyping, complete C++ solution implementation, deployment, and CI.
- **RESUME-DOCUMENTED:** ML Engineer / Deep Learning Team Lead at Motion Metrics, March 2018–October
  2019; led a six-person team building real-time mining monitoring systems; migrated legacy
  Windows/Caffe/C++ products to Linux/TensorFlow/Python while claiming improved speed and accuracy.
- **RESUME-DOCUMENTED:** Software Engineer at Fidessa, September 2014–December 2016; real-time
  Java/Linux trading algorithms, latency-critical components, C++/Java/TCL/FIX, and North/South
  American market connectivity.
- **RESUME-DOCUMENTED:** Production Line Manager at AB-InBev, May–August 2014; FANUC vision and
  robotic line modernization, maintenance planning, and operations/trades coordination.
- **RESUME-DOCUMENTED:** Historical technical exposure includes C++, Java, Python, MATLAB, Linux,
  AWS, TensorFlow, PyTorch, Caffe, real-time CV, object detection, classification, recommender,
  anomaly-detection, regression, Bayesian, tree, and reinforcement-learning methods.
- **RESUME-DOCUMENTED / PUBLICLY-VERIFIABLE:** CVPR 2019 publication, “Towards Autonomous Mining
  via Intelligent Excavators.” Bibliography verified/corrected November 9 above; individual contribution still needs checking.

### Adobe check-ins

Source directory: `/mnt/localssd/adobe_checkins`; inspected and visually rendered 2026-09-15.

- **VERIFIED — source inspection:** Eight replacement PDFs contain employee goals,
  self-reflections, year-end/quarterly responses, and several manager responses covering FY24,
  FY25, and FY26.
- **OPEN:** The generic filenames and rendered export dates do not preserve a trustworthy exact
  chronology within each fiscal year. Sequence below is based on the fiscal-year labels and the
  work progression described in the text; exact role-transition months remain to be established.

Source map:

- `Quarterly_Conversation.pdf`: FY24 goals.
- `Quarterly_Conversation (1).pdf`: FY24 progress and Clineto pipeline work.
- `Year-End_Conversation.pdf`: FY24 outcomes for VIQ, Minimal Inference, and evaluation.
- `Self_Reflection.pdf`: professional-development focus during the Clineto/VIQ period.
- `Self_Reflection (1).pdf`: integration, evaluation, and Kaizen goals.
- `Self_Reflection (2).pdf`: Clineto and Genie/Glimmer progress plus manager assessment.
- `Self_Reflection (3).pdf`: FY25 outcomes for Marketplace, Glimmer 2.0, service continuity,
  initial Foundry work, and manager assessment.
- `Goals.pdf`: FY26 Foundry goals and manager alignment.

#### FY24 — video inference, integration, and evaluation

- **CHECKIN-GOAL:** Support DMD production training, evaluation, and inference; develop practical
  inference-engineering depth for Clineto; learn DiT training; and reduce pipeline-integration time.
- **CHECKIN-SELF-REPORTED:** Led the technical effort for Clineto's Colligo video pipeline,
  including T2V, I2V, V2V, and a combined pipeline. Work spanned planning and stakeholder
  coordination, experience design, pipeline architecture and implementation, frontend changes,
  platform changes, and cross-team integration.
- **CHECKIN-SELF-REPORTED:** Designed and built SS Eval and end-to-end evaluation pipelines for
  in-painting, out-painting, and Magic Trim, while aligning model and pipeline requirements to
  reduce technical-transfer friction.
- **CHECKIN-SELF-REPORTED:** Trained, evaluated, and deployed DMD models; deployed Colligo
  pipelines on Run:AI clusters and firefly.com; transferred this operational knowledge to other
  ASML teams.
- **CHECKIN-SELF-REPORTED:** Initiated and designed a combined video pipeline intended to improve
  researcher readability, reduce dependency conflicts, replace branching business logic with
  cleaner configuration/versioning, separate inputs from parameters, and reduce future transfer
  costs.
- **CHECKIN-SELF-REPORTED:** Led the VIQ squad's production delivery of Clineto T2V, I2V, V2V
  (GenExtend), and Guided Transform pipelines; reported meeting every deadline and receiving
  feedback that the MAX deliveries were among the smoothest operations that year.
- **CHECKIN-SELF-REPORTED:** Led and evangelized Minimal Inference pipelines that exposed
  production components to researchers through a simpler interface. Associated tooling covered
  HTML generation, improved GPU utilization, distributed processing across Run:AI nodes, job
  resumption, and modeler-friendly operation; reported adoption by multiple teams.
- **CHECKIN-SELF-REPORTED:** Led training-time automatic evaluation infrastructure, including a
  self-service workflow and multiple metrics, some LLM-based. Reported completing approximately
  two SS Eval studies per week and maintaining longitudinal model-quality records.
- **CHECKIN-SELF-REPORTED:** Enforced parity and change accountability between research prototypes
  and production pipelines through before/after result review and cross-functional sign-off.

#### FY25 — evaluation platform, data platform, and hands-on systems ownership

- **CHECKIN-GOAL:** Increase model-integration velocity through researcher enablement, cleaner
  research/production boundaries, shared Mori/Colligo components where safe, parity protocols,
  deployability checks, and stronger integration tests.
- **CHECKIN-GOAL:** Expand automatic evaluation during training through targeted evaluation sets,
  milestone-based larger evaluations, regular human annotation, more metrics, and broader Kaizen
  adoption.
- **CHECKIN-SELF-REPORTED:** Coordinated integration, evaluation, and release of Clineto video
  versions 1.8, 1.9, and 2.0 and downstream I2V, T2V, V2V/GenExtend, Structure Match, and RGBA
  applications.
- **CHECKIN-SELF-REPORTED:** Led Kaizen automatic inference/evaluation, standardized result-sharing
  HTMLs across image, video, and audio teams, added a searchable backend and leadership results
  dashboard, and added asynchronously calculated evaluation metrics.
- **CHECKIN-SELF-REPORTED:** Expanded the Data Marketplace concept from Parquet management to a
  broader data-lifecycle design spanning partner teams in Firefly Engineering, Imaging, Video,
  Audio, Research, Platform/Framework, Stock ingestion, and moderation.
- **CHECKIN-SELF-REPORTED:** Aligned ASML, ingestion, Stock, and moderation teams on a fast-track
  asset-identification workflow for Keto datasets and later ingestion back into Stock systems.
- **CHECKIN-SELF-REPORTED:** Formalized Genie/Glimmer support with an internal knowledge chatbot,
  on-call procedures, documentation, Jira intake/curation, and early engagement in customer-team
  stand-ups.
- **CHECKIN-MANAGER-CORROBORATED:** The manager wrote that Hooman “exceeded expectations” soon
  after becoming manager of the data team, materially improved collaboration with Platform and
  ASML, and delivered vLLM integration and Marketplace 0.1 as foundations for the roadmap. The
  manager also credited Hooman with cross-organizational alignment, prioritization, quality, and
  speed, while recommending more delegation to create space for longer-term strategy.
- **CHECKIN-SELF-REPORTED:** Unified the top three asks from Firefly Engineering, Imaging, Video,
  Research, Platform, and Framework into a shared Data Marketplace vision presented jointly at a
  town hall.
- **CHECKIN-SELF-REPORTED:** Personally designed and implemented Glimmer 2.0, replacing an
  RDS-backed queue with SQS, removing roughly 4,000 lines of code and the PyTorch Lightning
  dependency, decoupling Glimmer from Genie, and separating framework code from user code.
- **CHECKIN-SELF-REPORTED:** Reported that Glimmer 2.0 ran without interruption for multiple days
  on more than 30 nodes in the Ohio cluster when the earlier RDS design was unavailable, improving
  hardware utilization and contributing to cost savings.
- **CHECKIN-SELF-REPORTED:** Maintained Genie/Glimmer service and overhauled both products while
  the supporting organization fell from a seven-person team—five of whom worked on these
  products—to two people, with only one IC focused on Glimmer and Hooman covering architecture and
  implementation. No major service disruption was reported.
- **CHECKIN-SELF-REPORTED:** Began Foundry delivery work with two Home Depot training rounds and a
  third starting, plus initial Coca-Cola work, with both first readouts reported on track.
- **CHECKIN-MANAGER-CORROBORATED:** The manager called these achievements “great,” said Hooman had
  progressed substantially under difficult circumstances, and identified situational decision-making
  and patience during difficult actions as the remaining development edge.

#### FY26 — Foundry customer and workflow goals

- **CHECKIN-GOAL / MANAGER-ALIGNED:** Own customer success across Home Depot, Coca-Cola, Humain,
  Tesco, HP, DSG, and other assigned Foundry programs by translating underlying customer needs into
  deliverables and using customer feedback/project success as the outcome measure.
- **CHECKIN-GOAL / MANAGER-ALIGNED:** Enable C-Techs to draft use cases and perform preliminary
  data analysis so commitments reflect technical constraints and actual data availability.
- **CHECKIN-GOAL / MANAGER-ALIGNED:** Build a more automated Foundry-specific data-delivery and
  moderation pipeline, consolidate compatible data asks across customers, and reduce stock-mission
  delivery lag.
- **CHECKIN-GOAL / MANAGER-ALIGNED:** Establish privacy-compatible Foundry evaluation and
  annotation workflows, including a Foundry-hosted Eval Hub, automated delivery from third-party
  studies, and more predictable annotation-resource planning.

### Adobe experience — Hooman's direct account

Sources: Hooman's 2026-09-14 project message and 2026-10-07 résumé clarification.

- **USER-CONFIRMED:** Adobe employment began in October 2023; current official title is Machine
  Learning Engineer, ASML.
- **USER-CONFIRMED:** Joined Adobe as an AI engineer.
- **USER-CONFIRMED:** Built Adobe's first product-video pipelines and worked on pipeline building,
  deployment, model integration, and technical transfer.
- **USER-CONFIRMED:** Moved into Foundry management; inherited a team that had been approximately
  eight people and later contracted to one or two, requiring continued IC contribution.
- **USER-CONFIRMED:** Upgraded and supported Genie and Glimmer, described as data-enrichment and
  data-loader systems used across foundation-model and research work.
- **USER-CONFIRMED:** Managed Home Depot, Coca-Cola, HP, Lionsgate, Humain, and Tesco programs—more
  simultaneous projects than any other manager, according to Hooman.
- **USER-CONFIRMED:** Returned to an IC role and recently built a Home Depot rewriter.
- **USER-CONFIRMED:** Wants deeper understanding of the end-to-end workflows delivered for
  customers, especially Coca-Cola and HP, because they represent recurring AI-product patterns.

## Provisional strengths — not yet résumé claims

- **INFERENCE:** unusually broad exposure across modeling, real-time software, production ML,
  platform/data systems, deployment, customer discovery, and technical leadership.
- **INFERENCE:** the check-ins materially strengthen a Staff/Principal narrative at the
  model-to-product boundary: research-to-production transfer, inference workflows, evaluation,
  distributed execution, platform simplification, and multi-team technical leadership recur across
  multiple review periods.
- **INFERENCE:** enterprise AI workflow ownership may differentiate Hooman from candidates who
  know models or infrastructure but have not delivered end-to-end customer value.
- **INFERENCE:** Glimmer 2.0 may be the strongest currently documented hands-on systems story
  because it combines architecture simplification, implementation ownership, distributed scale,
  reliability, customer pain, and resource constraints. Its metrics still need artifact-level
  corroboration before external use.

## Evidence needed for each Adobe accomplishment

For every major project, capture:

1. dates, title, and role;
2. problem and customer/business outcome;
3. architecture and difficult technical decisions;
4. Hooman's role as leader, architect, implementer, or contributor;
5. scale, latency, reliability, quality, cost, or delivery metrics;
6. model/data/platform technologies involved;
7. stakeholders and influence scope;
8. failure, trade-off, or recovery story;
9. what may be disclosed publicly; and
10. artifact or corroborating source.

Team outcomes achieved under Hooman's leadership are valid career evidence. Use the strongest
accurate verb supported by the record and do not default to weaker language merely because the work
was collaborative.
