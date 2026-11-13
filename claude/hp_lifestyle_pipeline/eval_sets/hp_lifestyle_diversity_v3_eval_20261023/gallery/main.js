const sourceById = new Map(Object.entries(V3_DATA.sources));
const caseById = new Map(Object.entries(V3_DATA.cases));
const renderById = new Map(Object.entries(V3_DATA.renders));
const candidateByKey = new Map(V3_DATA.candidates.map(item => [item.candidate_key, item]));
let currentView = "generations";
let currentPage = 1;
let initialized = false;
let lazyDetailCounter = 0;
const lazyDetailValues = new Map();

function escapeHtml(value) {
    return String(value ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#039;");
}
function referencePath(render) { return `../assets/references/${encodeURIComponent(render.reference_asset_filename)}`; }
function outputPath(result) { return `../images/${encodeURIComponent(result.generated_image.filename)}`; }
function departureLabels(candidate) { return (candidate.creative_departures || []).map(item => typeof item === "string" ? item : (item.label_id || item.label || item.description)); }
function relationshipClass(value) { return value === "source_grounded" ? "grounded" : value === "source_adjacent" ? "adjacent" : "departure"; }
function score(candidate) { return Number(candidate.source_relevance_score ?? candidate.score_total ?? 0); }

function jsonDetails(summary, value, open = false) {
    const key = `json-${++lazyDetailCounter}`;
    lazyDetailValues.set(key, value);
    return `<details data-lazy-json="${key}"${open ? " open" : ""}><summary>${escapeHtml(summary)}</summary><pre>Open to render JSON.</pre></details>`;
}

function renderLazyDetail(detail) {
    if (!detail.open || detail.dataset.rendered === "true") return;
    const value = lazyDetailValues.get(detail.dataset.lazyJson);
    detail.querySelector("pre").textContent = JSON.stringify(value, null, 2);
    detail.dataset.rendered = "true";
}

function bindLazyDetails() {
    document.querySelectorAll("details[data-lazy-json]").forEach(detail => {
        detail.addEventListener("toggle", () => renderLazyDetail(detail));
        renderLazyDetail(detail);
    });
}

function addOptions(id, values) {
    const select = document.getElementById(id);
    [...new Set(values.filter(value => value !== undefined && value !== null && value !== ""))].sort().forEach(value => {
        const option = document.createElement("option"); option.value = value; option.textContent = value; select.appendChild(option);
    });
}

function onAuthReady() {
    if (!initialized) { initialize(); initialized = true; }
    render();
}

function initialize() {
    const m = V3_DATA.metadata;
    document.getElementById("subtitle").textContent = `${m.source_count} sources · ${m.case_count} source-camera banks · ${m.candidate_count}/${m.expected_candidate_count} validated candidates · ${m.selected_count}/${m.expected_selected_count} selected image rows · ${m.generation_status_counts.done || 0} generated`;
    document.getElementById("runContext").textContent = JSON.stringify(V3_DATA.run_context, null, 2);
    addOptions("sourceFilter", V3_DATA.candidates.map(item => item.source_id));
    addOptions("deviceFilter", V3_DATA.candidates.map(item => item.device_type));
    addOptions("cameraFilter", V3_DATA.candidates.map(item => item.camera_tag));
    addOptions("environmentFilter", V3_DATA.candidates.map(item => item.display_environment));
    addOptions("relationshipFilter", V3_DATA.candidates.map(item => item.relationship));
    addOptions("departureFilter", V3_DATA.candidates.flatMap(departureLabels));
    addOptions("stratumFilter", V3_DATA.candidates.filter(item => item.selection).map(item => item.selection.rank_stratum));
    addOptions("statusFilter", V3_DATA.generation_rows.map(item => item.status));
    document.querySelectorAll(".view-tab").forEach(button => button.addEventListener("click", () => { currentView = button.dataset.view; currentPage = 1; document.querySelectorAll(".view-tab").forEach(tab => tab.classList.toggle("active", tab === button)); render(); }));
    ["searchInput", "sourceFilter", "deviceFilter", "cameraFilter", "environmentFilter", "relationshipFilter", "departureFilter", "stratumFilter", "statusFilter", "scoreMin", "scoreMax", "pageSize"].forEach(id => document.getElementById(id).addEventListener(id === "searchInput" || id.startsWith("score") ? "input" : "change", () => { currentPage = 1; render(); }));
    document.getElementById("prevPage").addEventListener("click", () => { currentPage = Math.max(1, currentPage - 1); render(); window.scrollTo({top:0, behavior:"smooth"}); });
    document.getElementById("nextPage").addEventListener("click", () => { currentPage += 1; render(); window.scrollTo({top:0, behavior:"smooth"}); });
    const modal = document.getElementById("assetModal"); modal.addEventListener("click", event => { if (event.target === modal) closeModal(); }); modal.querySelector(".close-btn").addEventListener("click", closeModal); document.addEventListener("keydown", event => { if (event.key === "Escape") closeModal(); });
}

function filters() {
    return { query:document.getElementById("searchInput").value.trim().toLowerCase(), source:document.getElementById("sourceFilter").value, device:document.getElementById("deviceFilter").value, camera:document.getElementById("cameraFilter").value, environment:document.getElementById("environmentFilter").value, relationship:document.getElementById("relationshipFilter").value, departure:document.getElementById("departureFilter").value, stratum:document.getElementById("stratumFilter").value, status:document.getElementById("statusFilter").value, min:Number(document.getElementById("scoreMin").value || 0), max:Number(document.getElementById("scoreMax").value || 100) };
}

function matchesCandidate(candidate, f, includeQuery = true) {
    if (f.source !== "all" && candidate.source_id !== f.source) return false;
    if (f.device !== "all" && candidate.device_type !== f.device) return false;
    if (f.camera !== "all" && candidate.camera_tag !== f.camera) return false;
    if (f.environment !== "all" && candidate.display_environment !== f.environment) return false;
    if (f.relationship !== "all" && candidate.relationship !== f.relationship) return false;
    if (f.departure !== "all" && !departureLabels(candidate).includes(f.departure)) return false;
    if (f.stratum !== "all" && candidate.selection?.rank_stratum !== f.stratum) return false;
    if (score(candidate) < f.min || score(candidate) > f.max) return false;
    if (!includeQuery || !f.query) return true;
    const evidence = resolveEvidence(candidate).map(item => `${item.id} ${item.message_id} ${item.path} ${item.quote}`).join(" ");
    const taxonomyTriggers = (candidate.display_environment_triggers || []).flatMap(item => [item.field, ...(item.terms || [])]).join(" ");
    return [candidate.candidate_key,candidate.source_id,candidate.camera_tag,candidate.display_environment,candidate.environment,candidate.display_environment_rule_id,taxonomyTriggers,candidate.subsetting,candidate.text,candidate.relationship,candidate.explanation,departureLabels(candidate).join(" "),evidence].join(" ").toLowerCase().includes(f.query);
}

function resolveEvidence(candidate) {
    const debug = caseById.get(candidate.case_id)?.accepted?.debug || {};
    const byId = new Map((debug.source_evidence || []).map(item => [item.id, item]));
    return (candidate.evidence_ids || []).map(id => byId.get(id) || {id, missing:true});
}

function filteredItems() {
    const f = filters();
    if (currentView === "candidates") return V3_DATA.candidates.filter(item => matchesCandidate(item, f));
    const priority = {done:0, failed:1, pending:2, missing:3};
    return V3_DATA.generation_rows.filter(row => {
        const candidate = candidateByKey.get(row.candidate_key);
        if (!candidate || !matchesCandidate(candidate, f, false)) return false;
        if (f.status !== "all" && row.status !== f.status) return false;
        if (!f.query) return true;
        const result = row.result || {};
        return `${result.usedPrompt || ""} ${result.job_id || ""} ${result.request_id || ""} ${row.row_id}`.toLowerCase().includes(f.query) || matchesCandidate(candidate, f, true);
    }).sort((left, right) => (priority[left.status] ?? 9) - (priority[right.status] ?? 9));
}

function candidateBadges(candidate) {
    const selected = candidate.selection ? `<span class="badge selected">selected · ${escapeHtml(candidate.selection.rank_stratum)}</span>` : "";
    return `<div class="badges"><span class="badge rank">rank ${candidate.rank}</span><span class="badge score">${score(candidate)}/100</span><span class="badge environment">${escapeHtml(candidate.display_environment)}${candidate.subsetting ? ` · ${escapeHtml(candidate.subsetting)}` : ""}</span><span class="badge ${relationshipClass(candidate.relationship)}">${escapeHtml(candidate.relationship)}</span>${selected}</div>`;
}

function environmentTaxonomyHtml(candidate) {
    return jsonDetails("Environment taxonomy", {
        display_environment: candidate.display_environment,
        original_environment_family: candidate.environment,
        rule_id: candidate.display_environment_rule_id,
        triggers: candidate.display_environment_triggers,
    });
}

function candidatePromptHtml(candidate) {
    return `${candidateBadges(candidate)}<p class="prompt-text">${escapeHtml(candidate.text)}</p><div class="record-id">${escapeHtml(candidate.candidate_key)} · ${escapeHtml(candidate.text_sha256)}</div>${environmentTaxonomyHtml(candidate)}`;
}

function identityHtml(candidate) {
    const c = caseById.get(candidate.case_id);
    return `<div class="badges"><span class="badge device">${escapeHtml(candidate.device_type)}</span><span class="badge camera">${escapeHtml(candidate.camera_tag)}</span></div><div class="identity-meta"><strong>${escapeHtml(candidate.source_id)}</strong><span>${escapeHtml(c?.manifest?.view_role)}</span><span>${escapeHtml(candidate.case_id)}</span><span>${escapeHtml(c?.manifest?.group_id)}</span></div>`;
}

function scoreHtml(candidate) {
    const components = candidate.score_components || {};
    return `<div class="score-total">${score(candidate)} / 100</div><div class="score-components">${Object.entries(components).map(([name,value]) => `<span>${escapeHtml(name)}</span><strong>${escapeHtml(value)}</strong>`).join("")}</div><p class="explanation">${escapeHtml(candidate.explanation)}</p>${departureLabels(candidate).length ? `<h4>Creative departures</h4><ul class="departure-list">${(candidate.creative_departures || []).map(item => `<li><code>${escapeHtml(typeof item === "string" ? item : (item.label_id || item.label || "departure"))}</code> ${escapeHtml(typeof item === "string" ? "" : (item.description || item.reason || ""))}</li>`).join("")}</ul>` : `<p class="explanation">No labeled creative departures.</p>`}`;
}

function evidenceHtml(candidate) {
    const evidence = resolveEvidence(candidate);
    return evidence.length ? `<ul class="evidence-list">${evidence.map(item => `<li><code>${escapeHtml(item.id)}</code> ${item.missing ? "unresolved evidence ID" : `<strong>${escapeHtml(item.message_id)}.${escapeHtml(item.path)}</strong>: “${escapeHtml(item.quote)}”`}</li>`).join("")}</ul>` : `<p class="explanation">No source evidence claimed for this candidate.</p>`;
}

function visualHtml(candidate) {
    const c = caseById.get(candidate.case_id);
    return `<details open><summary>Visible-scene signature</summary><pre>${escapeHtml(JSON.stringify(candidate.visual_signature, null, 2))}</pre></details><details><summary>Camera omissions</summary><pre>${escapeHtml(JSON.stringify(candidate.camera_omissions, null, 2))}</pre></details><details><summary>Resolved camera</summary><pre>${escapeHtml(JSON.stringify(c?.accepted?.debug?.camera || c?.manifest?.expected_camera, null, 2))}</pre></details>`;
}

function auditHtml(candidate) {
    const c = caseById.get(candidate.case_id);
    const changedOriginalIds = new Set((c?.normalization_log?.changes || []).map(item => item.original_id));
    const changed = (c?.normalization_log?.id_map || []).some(item => item.normalized_id === candidate.id && changedOriginalIds.has(item.original_id));
    const rejected = c?.rejected_attempts || [];
    return `${candidate.selection ? `<div class="badges"><span class="badge selected">${escapeHtml(candidate.selection.selection_id)}</span></div>${jsonDetails("Selection provenance", candidate.selection)}` : `<p class="pending-message">Not selected for the 108-row image sample.</p>`}<div class="badges"><span class="badge ${changed ? "adjacent" : "grounded"}">${changed ? "deterministically normalized" : "unchanged by normalizer"}</span><span class="badge family">${escapeHtml(c?.accepted?.raw_record_status)}</span>${rejected.length ? `<span class="badge departure">${rejected.length} rejected prior attempt${rejected.length === 1 ? "" : "s"}</span>` : ""}</div>${jsonDetails("Full runtime input", c?.input)}${jsonDetails("Normalized candidate used for selection", candidate.raw_candidate, true)}${jsonDetails("Normalized bank output", c?.normalized_output)}${jsonDetails("Deterministic normalization log", c?.normalization_log)}${jsonDetails("Raw versus normalized validation audit", c?.validation_audit)}${jsonDetails("Raw model output before normalization", c?.raw_model_output)}${jsonDetails("Complete immutable raw API record", c?.raw_model_record)}${rejected.length ? jsonDetails("Rejected prior attempts — excluded from candidate bank", rejected) : ""}${jsonDetails("Complete normalized bank debug", c?.accepted?.debug)}`;
}

function candidateRowHtml(candidate) {
    return `<tr><td>${candidatePromptHtml(candidate)}</td><td>${identityHtml(candidate)}</td><td>${scoreHtml(candidate)}</td><td>${evidenceHtml(candidate)}</td><td>${visualHtml(candidate)}</td><td>${auditHtml(candidate)}</td></tr>`;
}

function referenceHtml(row) {
    const render = renderById.get(row.render_id); const path = referencePath(render);
    return `<button class="image-button" type="button" data-image="${path}" data-label="Reference · ${escapeHtml(render.render_id)}"><img loading="lazy" src="${path}" width="${render.width}" height="${render.height}" alt="${escapeHtml(render.render_id)} reference"></button><div class="asset-meta"><strong>${escapeHtml(render.device_type)} · ${escapeHtml(render.role)}</strong><span>${escapeHtml(render.source_camera_name)}</span><span>${escapeHtml(render.render_id)}</span><span>${render.width}×${render.height} · ${escapeHtml(render.sha256)}</span></div>`;
}

function sourceHtml(candidate) {
    const c = caseById.get(candidate.case_id);
    return `${jsonDetails("Full source messaging", sourceById.get(candidate.source_id))}${jsonDetails("Exact runtime input", c?.input)}`;
}

function outputHtml(row) {
    const result = row.result;
    if (row.status !== "done") return `<span class="status-pill ${escapeHtml(row.status)}">${escapeHtml(row.status)}</span><div class="${row.status === "failed" ? "failure-message" : "pending-message"}">${escapeHtml(result?.error || "No completed generation record is available for this selected row.")}</div>`;
    const image = result.generated_image; const path = outputPath(result);
    return `<button class="image-button" type="button" data-image="${path}" data-label="Generated · ${escapeHtml(row.row_id)}"><img loading="lazy" src="${path}" width="${image.native_width}" height="${image.native_height}" alt="Generated output"></button><div class="asset-meta"><span>seed ${escapeHtml(result.returned_seed)}</span><span>${image.native_width}×${image.native_height}</span><span>${escapeHtml(image.sha256)}</span></div>`;
}

function generationRowHtml(row) {
    const candidate = candidateByKey.get(row.candidate_key); const result = row.result;
    return `<tr><td>${candidatePromptHtml(candidate)}${jsonDetails("Selection provenance", candidate.selection)}</td><td>${referenceHtml(row)}</td><td>${sourceHtml(candidate)}</td><td>${scoreHtml(candidate)}${evidenceHtml(candidate)}</td><td>${outputHtml(row)}</td><td>${result?.usedPrompt ? `<details><summary>View usedPrompt</summary><pre>${escapeHtml(result.usedPrompt)}</pre></details>` : `<span class="status-pill ${escapeHtml(row.status)}">${escapeHtml(row.status)}</span>`}</td><td>${result ? jsonDetails("Complete generation record", result) : `<span class="status-pill ${escapeHtml(row.status)}">${escapeHtml(row.status)}</span>`}</td></tr>`;
}

function render() {
    lazyDetailValues.clear(); lazyDetailCounter = 0;
    const items = filteredItems(); const selected = document.getElementById("pageSize").value; const pageSize = selected === "all" ? Math.max(items.length,1) : Number(selected); const pageCount = Math.max(1,Math.ceil(items.length/pageSize)); currentPage = Math.min(currentPage,pageCount); const start=(currentPage-1)*pageSize; const visible=items.slice(start,start+pageSize);
    document.getElementById("candidateView").classList.toggle("hidden", currentView !== "candidates"); document.getElementById("generationView").classList.toggle("hidden", currentView !== "generations"); document.getElementById("statusFilter").parentElement.classList.toggle("hidden", currentView !== "generations");
    if (currentView === "candidates") document.getElementById("candidateRows").innerHTML = visible.map(candidateRowHtml).join(""); else document.getElementById("generationRows").innerHTML = visible.map(generationRowHtml).join("");
    document.getElementById("emptyState").classList.toggle("hidden", items.length !== 0); const selectedCount = currentView === "candidates" ? items.filter(item => item.selection).length : items.length; document.getElementById("resultSummary").textContent = `${items.length} matching ${currentView === "candidates" ? "text candidates" : "selected image rows"} · ${selectedCount} selected · ${new Set(items.map(item => item.source_id)).size} sources`;
    document.getElementById("pageStatus").textContent = items.length ? `Page ${currentPage} of ${pageCount} · rows ${start+1}–${start+visible.length}` : "No rows"; document.getElementById("prevPage").disabled=currentPage<=1; document.getElementById("nextPage").disabled=currentPage>=pageCount;
    document.querySelectorAll(".image-button").forEach(button => button.addEventListener("click", () => openModal(button.dataset.image,button.dataset.label)));
    bindLazyDetails();
}

function openModal(path,label) { document.getElementById("modalImage").src=path; document.getElementById("modalInfo").textContent=label; document.getElementById("assetModal").classList.add("active"); }
function closeModal() { document.getElementById("assetModal").classList.remove("active"); document.getElementById("modalImage").src=""; }
