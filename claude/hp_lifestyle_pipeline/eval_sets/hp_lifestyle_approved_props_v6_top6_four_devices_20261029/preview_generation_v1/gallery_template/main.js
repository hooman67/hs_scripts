/* global GENERATION_DATA */
"use strict";

const byId = id => document.getElementById(id);
const escapeHtml = value => String(value ?? "").replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[char]));
const pretty = value => JSON.stringify(value ?? null, null, 2);
const imagePath = value => `../${value}`;
const rowsByPromptKey = new Map(GENERATION_DATA.rows.map(row => [row.prompt_key, row]));

function addOptions(id, values) {
  const select = byId(id);
  values.forEach(value => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    select.appendChild(option);
  });
}

function details(label, value, className = "") {
  return `<details class="${className}"><summary>${escapeHtml(label)}</summary><pre>${escapeHtml(typeof value === "string" ? value : pretty(value))}</pre></details>`;
}

function rowStatus(row) {
  if (row.status === "prompt_only") return "prompt_only";
  if (row.status === "failed") return "failed";
  if (row.status === "done") return "done";
  return "pending";
}

function bankLabel(bank) {
  return `${bank.device_display_name} · ${bank.source_pair} · ${bank.camera_tag}`;
}

function filteredBanks() {
  const device = byId("deviceFilter").value;
  const sourcePair = byId("sourcePairFilter").value;
  const camera = byId("cameraFilter").value;
  return GENERATION_DATA.banks.filter(bank =>
    (device === "all" || bank.device_id === device) &&
    (sourcePair === "all" || bank.source_pair === sourcePair) &&
    (camera === "all" || bank.camera_tag === camera)
  );
}

function refreshBankSelector(preferredBankId = "") {
  const select = byId("bankFilter");
  const banks = filteredBanks();
  const previous = preferredBankId || select.value;
  select.innerHTML = "";
  banks.forEach(bank => {
    const option = document.createElement("option");
    option.value = bank.bank_id;
    option.textContent = bankLabel(bank);
    select.appendChild(option);
  });
  if (banks.some(bank => bank.bank_id === previous)) select.value = previous;
  else if (banks.length) select.value = banks[0].bank_id;
  select.disabled = banks.length === 0;
}

function selectedBank() {
  return GENERATION_DATA.banks.find(bank => bank.bank_id === byId("bankFilter").value) || null;
}

function promptHtml(row) {
  const candidate = row.candidate;
  const selection = row.status === "prompt_only" ? "Prompt only" : "Top-six generated";
  return `<div class="badges"><span class="badge rank">Rank ${escapeHtml(candidate.bank_rank)}</span><span class="badge environment">${escapeHtml(candidate.environment)}</span><span class="badge device">${escapeHtml(row.device_id)}</span><span class="badge view">${escapeHtml(candidate.view_role)}</span><span class="badge ${row.status === "prompt_only" ? "prompt-only" : "generated"}">${selection}</span></div>
    <p class="prompt-text">${escapeHtml(candidate.text)}</p>
    <div class="record-id">Source ${escapeHtml(candidate.source_relevance_score)} · C-Tech ${escapeHtml(candidate.ctech_reference_score)}<br>${escapeHtml(row.prompt_key)}</div>`;
}

function correctedInputHtml(row) {
  const render = row.corrected_input;
  const path = imagePath(render.gallery_path);
  return `<button class="image-button" type="button" data-image="${escapeHtml(path)}" data-label="Corrected digital twin · ${escapeHtml(render.render_id)}"><img loading="lazy" src="${escapeHtml(path)}" alt="Corrected ${escapeHtml(row.camera_tag)} digital twin"></button>
    <div class="image-meta"><strong>${escapeHtml(row.camera_tag)}</strong><span>${escapeHtml(render.width)}×${escapeHtml(render.height)} PNG</span><code>${escapeHtml(render.sha256.slice(0, 12))}…</code></div>`;
}

function sourceHtml(row) {
  const source = GENERATION_DATA.sources[row.bank_id];
  return `<p class="shared-note">Shared by all 10 prompts in this bank.</p>${details("View Smart Brief", source.smart_brief)}${details("View source messaging", source.source_messaging)}${details("Input provenance", {input_path: source.input_path, input_sha256: source.input_sha256, camera_tag: source.camera_tag, revision: source.source_revision})}`;
}

function explanationHtml(row) {
  const candidate = row.candidate;
  return details("View explanation + score metadata", {
    selection: {bank_rank: candidate.bank_rank, generated: row.status !== "prompt_only", source_revision: candidate.source_revision, prop_ids: candidate.prop_ids},
    scores: {source_relevance_score: candidate.source_relevance_score, ctech_reference_score: candidate.ctech_reference_score, score_components: candidate.score_components},
    source: {relationship: candidate.relationship, explanation: candidate.explanation, evidence: candidate.evidence, creative_departures: candidate.creative_departures},
    ctech: {reference_id: candidate.ctech_reference_id, explanation: candidate.ctech_explanation},
    camera_fit_explanation: candidate.camera_fit_explanation,
    provenance: row.provenance
  });
}

function outputHtml(row) {
  if (row.status === "prompt_only") {
    return `<span class="status-pill prompt-only">prompt only</span><p class="status-message">This authored candidate was outside the top-six image selection. No image-generation request was made.</p>`;
  }
  if (row.status !== "done") {
    return `<span class="status-pill ${escapeHtml(row.status)}">${row.status === "failed" ? "error" : "pending"}</span><p class="status-message">${escapeHtml(row.error || row.status_reason || "Awaiting a durable generation record.")}</p>`;
  }
  const output = row.record.generated_image;
  const path = imagePath(output.gallery_path);
  return `<button class="image-button" type="button" data-image="${escapeHtml(path)}" data-label="Generated output · ${escapeHtml(row.row_id)}"><img loading="lazy" src="${escapeHtml(path)}" alt="Generated output for ${escapeHtml(row.row_id)}"></button>
    <div class="image-meta"><strong>generated</strong><span>${escapeHtml(output.native_width)}×${escapeHtml(output.native_height)}</span><code>${escapeHtml(output.sha256.slice(0, 12))}…</code></div>`;
}

function rewrittenHtml(row) {
  if (row.status === "prompt_only") return `<span class="status-pill prompt-only">not requested</span><p class="status-message">No rewrite exists because this candidate was not generated.</p>`;
  if (row.status !== "done") return `<span class="status-pill ${escapeHtml(row.status)}">${row.status === "failed" ? "error" : "pending"}</span>`;
  return details("View rewritten prompt", row.record.usedPrompt || "No rewritten prompt returned.", "rewrite-details");
}

function debugHtml(row) {
  if (row.status === "prompt_only") return `<span class="status-pill prompt-only">not requested</span><p class="status-message">No endpoint request or debug response exists.</p>`;
  if (!row.record) return `<span class="status-pill pending">pending</span><p class="status-message">No durable generation record exists yet.</p>`;
  return details("View full debug / request", row.record, "debug-details");
}

function rowHtml(row) {
  return `<tr data-status="${escapeHtml(rowStatus(row))}"><td>${promptHtml(row)}</td><td>${correctedInputHtml(row)}</td><td>${sourceHtml(row)}</td><td>${explanationHtml(row)}</td><td>${outputHtml(row)}</td><td>${rewrittenHtml(row)}</td><td>${debugHtml(row)}</td></tr>`;
}

function bankContextHtml(bank) {
  const source = GENERATION_DATA.sources[bank.bank_id];
  return `<div class="bank-heading"><div><p class="eyebrow">Selected prompt bank</p><h2>${escapeHtml(bank.device_display_name)} · ${escapeHtml(bank.camera_tag)}</h2><p>${escapeHtml(bank.bank_id)}</p></div><div class="bank-count"><strong>10</strong><span>ranked prompts</span></div></div>
    <div class="bank-facts"><div><span>Device</span><strong>${escapeHtml(bank.device_display_name)} (${escapeHtml(bank.device_type)})</strong></div><div><span>Smart Brief / source pair</span><strong>${escapeHtml(bank.source_pair)}</strong></div><div><span>Camera</span><strong>${escapeHtml(bank.camera_tag)}</strong><small>${escapeHtml(bank.source_camera_name)} · ${escapeHtml(bank.view_role)}</small></div><div><span>Selection</span><strong>${escapeHtml(bank.generated_selection_count)} generated · ${escapeHtml(bank.prompt_only_count)} prompt-only</strong></div></div>
    <div class="bank-source-details">${details("View shared Smart Brief", source.smart_brief)}${details("View shared source messaging", source.source_messaging)}</div>`;
}

function rowsForSelectedBank(bank) {
  const query = byId("searchInput").value.trim().toLowerCase();
  const environment = byId("environmentFilter").value;
  const status = byId("statusFilter").value;
  return bank.prompt_keys.map(key => rowsByPromptKey.get(key)).filter(row => {
    if (environment !== "all" && row.candidate.environment !== environment) return false;
    if (status !== "all" && rowStatus(row) !== status) return false;
    if (!query) return true;
    return [row.prompt_key, row.candidate.text, row.candidate.environment, row.candidate.ctech_reference_id, row.record?.usedPrompt].join(" ").toLowerCase().includes(query);
  });
}

function render() {
  const banks = filteredBanks();
  const bank = selectedBank();
  if (!bank) {
    byId("bankContext").innerHTML = "";
    byId("galleryRows").innerHTML = "";
    byId("emptyState").classList.remove("hidden");
    byId("resultSummary").textContent = "No prompt bank matches the selected device, source pair, and camera filters.";
    byId("bankStatus").textContent = "No banks";
    byId("prevBank").disabled = true;
    byId("nextBank").disabled = true;
    return;
  }
  const bankIndex = banks.findIndex(item => item.bank_id === bank.bank_id);
  const rows = rowsForSelectedBank(bank);
  byId("bankContext").innerHTML = bankContextHtml(bank);
  byId("galleryRows").innerHTML = rows.map(rowHtml).join("");
  byId("emptyState").classList.toggle("hidden", rows.length !== 0);
  const generated = bank.prompt_keys.map(key => rowsByPromptKey.get(key)).filter(row => row.status === "done").length;
  byId("resultSummary").textContent = `${bankLabel(bank)} · showing ${rows.length} of 10 prompts · ${generated} generated outputs · ${bank.prompt_only_count} prompt-only candidates`;
  byId("bankStatus").textContent = `Bank ${bankIndex + 1} of ${banks.length}`;
  byId("prevBank").disabled = bankIndex <= 0;
  byId("nextBank").disabled = bankIndex >= banks.length - 1;
  document.querySelectorAll(".image-button").forEach(button => button.addEventListener("click", () => openModal(button.dataset.image, button.dataset.label)));
}

function moveBank(offset) {
  const banks = filteredBanks();
  const index = banks.findIndex(bank => bank.bank_id === byId("bankFilter").value);
  const next = banks[index + offset];
  if (!next) return;
  byId("bankFilter").value = next.bank_id;
  render();
  scrollTo({top: 0, behavior: "smooth"});
}

function openModal(path, label) { byId("modalImage").src = path; byId("modalInfo").textContent = label; byId("assetModal").classList.add("active"); }
function closeModal() { byId("assetModal").classList.remove("active"); byId("modalImage").src = ""; }

function initializeGallery() {
  const meta = GENERATION_DATA.metadata;
  byId("subtitle").textContent = `${meta.bank_count} separate device + source + camera banks · 10 ranked prompts per bank · built ${meta.built_at_utc}`;
  byId("progress").innerHTML = `<strong>${escapeHtml(meta.generation_status_counts.done)} / ${escapeHtml(meta.generation_row_count)}</strong><span>generated outputs</span>`;
  byId("downloads").innerHTML = meta.downloads.map(item => `<a href="${escapeHtml(item.path)}" download>${escapeHtml(item.label)}</a>`).join("");
  addOptions("environmentFilter", meta.environments);
  addOptions("deviceFilter", [...new Set(GENERATION_DATA.banks.map(bank => bank.device_id))]);
  addOptions("sourcePairFilter", [...new Set(GENERATION_DATA.banks.map(bank => bank.source_pair))]);
  addOptions("cameraFilter", [...new Set(GENERATION_DATA.banks.map(bank => bank.camera_tag))]);
  refreshBankSelector();
  ["deviceFilter", "sourcePairFilter", "cameraFilter"].forEach(id => byId(id).addEventListener("change", () => { refreshBankSelector(); render(); }));
  byId("bankFilter").addEventListener("change", render);
  ["environmentFilter", "statusFilter"].forEach(id => byId(id).addEventListener("change", render));
  byId("searchInput").addEventListener("input", render);
  byId("prevBank").addEventListener("click", () => moveBank(-1));
  byId("nextBank").addEventListener("click", () => moveBank(1));
  byId("assetModal").addEventListener("click", event => { if (event.target === byId("assetModal")) closeModal(); });
  document.querySelector(".close-btn").addEventListener("click", closeModal);
  document.addEventListener("keydown", event => { if (event.key === "Escape") closeModal(); });
  byId("loading").classList.add("hidden");
  byId("content").classList.remove("hidden");
  render();
}

document.addEventListener("DOMContentLoaded", initializeGallery);
