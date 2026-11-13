/* global GENERATION_DATA */
"use strict";

let currentPage = 1;
const byId = id => document.getElementById(id);
const escapeHtml = value => String(value ?? "").replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[char]));
const pretty = value => JSON.stringify(value ?? null, null, 2);
const imagePath = value => `../${value}`;

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

function rowStatus(row) { return row.status === "failed" ? "failed" : row.status === "done" ? "done" : "pending"; }

function selectionHtml(row) {
  const label = row.selection_type === "smart_brief" ? "Smart Brief top 5" : "C-Tech top 5";
  return `<span class="badge environment">${escapeHtml(label)}</span><div class="record-id">#${escapeHtml(row.selection_rank_in_bank)} in bank</div>`;
}

function promptHtml(row) {
  const candidate = row.candidate;
  return `<div class="badges"><span class="badge environment">${escapeHtml(candidate.environment)}</span><span class="badge device">${escapeHtml(row.device_type)}</span><span class="badge view">${escapeHtml(candidate.view_role)}</span></div>
    <p class="prompt-text">${escapeHtml(candidate.text)}</p>
    <div class="record-id">Source ${escapeHtml(candidate.combined_source_relevance_score)} · Smart Brief ${escapeHtml(candidate.smart_brief_support_score)} · C-Tech ${escapeHtml(candidate.ctech_similarity_score)}<br>${escapeHtml(row.candidate_key)}<br>${escapeHtml(row.row_id)}</div>`;
}

function correctedInputHtml(row) {
  const render = row.corrected_input;
  const path = imagePath(render.gallery_path);
  return `<button class="image-button" type="button" data-image="${escapeHtml(path)}" data-label="Corrected input · ${escapeHtml(render.render_id)}"><img loading="lazy" src="${escapeHtml(path)}" alt="Corrected ${escapeHtml(row.camera_tag)} input"></button>
    <div class="image-meta"><strong>${escapeHtml(row.camera_tag)}</strong><span>${escapeHtml(render.width)}×${escapeHtml(render.height)} PNG</span><code>${escapeHtml(render.sha256.slice(0, 12))}…</code></div>`;
}

function sourceHtml(row) {
  const source = GENERATION_DATA.sources[row.case_id];
  return `${details("View Smart Brief", source.smart_brief)}${details("View source messaging", source.source_messaging)}${details("Input provenance", {input_path: source.input_path, input_sha256: source.input_sha256, camera_tag: row.camera_tag})}`;
}

function explanationHtml(row) {
  const candidate = row.candidate;
  return details("View selection + score metadata", {
    selection: {type: row.selection_type, rank_in_bank: row.selection_rank_in_bank, selection_document_label: candidate.selection_document_label},
    scores: {smart_brief_support_score: candidate.smart_brief_support_score, combined_source_relevance_score: candidate.combined_source_relevance_score, ctech_similarity_score: candidate.ctech_similarity_score, smart_brief_score_components: candidate.smart_brief_score_components, source_messaging_score_components: candidate.source_messaging_score_components},
    source: {explanation: candidate.source_explanation},
    ctech: {reference_id: candidate.ctech_reference_id, relationship: candidate.ctech_relationship, explanation: candidate.ctech_explanation},
    provenance: row.provenance
  });
}

function outputHtml(row) {
  if (row.status !== "done") {
    return `<span class="status-pill ${escapeHtml(row.status)}">${row.status === "failed" ? "error" : "pending"}</span><p class="status-message">${escapeHtml(row.error || row.status_reason || "Awaiting a durable generation record.")}</p>`;
  }
  const output = row.record.generated_image;
  const path = imagePath(output.gallery_path);
  return `<button class="image-button" type="button" data-image="${escapeHtml(path)}" data-label="Generated output · ${escapeHtml(row.row_id)}"><img loading="lazy" src="${escapeHtml(path)}" alt="Generated output for ${escapeHtml(row.row_id)}"></button>
    <div class="image-meta"><strong>done</strong><span>${escapeHtml(output.native_width)}×${escapeHtml(output.native_height)}</span><code>${escapeHtml(output.sha256.slice(0, 12))}…</code></div>`;
}

function rewrittenHtml(row) {
  if (row.status !== "done") return `<span class="status-pill ${escapeHtml(row.status)}">${row.status === "failed" ? "error" : "pending"}</span>`;
  return details("View rewritten prompt", row.record.usedPrompt || "No rewritten prompt returned.", "rewrite-details");
}

function debugHtml(row) {
  if (!row.record) return `<span class="status-pill pending">pending</span><p class="status-message">No generation record exists yet.</p>`;
  return details("View full debug / request", row.record, "debug-details");
}

function rowHtml(row) {
  return `<tr data-status="${escapeHtml(rowStatus(row))}"><td>${selectionHtml(row)}</td><td>${promptHtml(row)}</td><td>${correctedInputHtml(row)}</td><td>${sourceHtml(row)}</td><td>${explanationHtml(row)}</td><td>${outputHtml(row)}</td><td>${rewrittenHtml(row)}</td><td>${debugHtml(row)}</td></tr>`;
}

function filteredRows() {
  const query = byId("searchInput").value.trim().toLowerCase();
  const selection = byId("selectionFilter").value;
  const environment = byId("environmentFilter").value;
  const device = byId("deviceFilter").value;
  const view = byId("viewFilter").value;
  const status = byId("statusFilter").value;
  return GENERATION_DATA.rows.filter(row => {
    if (selection !== "all" && row.selection_type !== selection) return false;
    if (environment !== "all" && row.candidate.environment !== environment) return false;
    if (device !== "all" && row.device_type !== device) return false;
    if (view !== "all" && row.candidate.view_role !== view) return false;
    if (status !== "all" && rowStatus(row) !== status) return false;
    if (!query) return true;
    return [row.row_id, row.case_id, row.candidate_key, row.candidate.text, row.candidate.environment, row.candidate.subsetting, row.record?.usedPrompt].join(" ").toLowerCase().includes(query);
  });
}

function render() {
  const rows = filteredRows();
  const size = Number(byId("pageSize").value);
  const pages = Math.max(1, Math.ceil(rows.length / size));
  currentPage = Math.min(currentPage, pages);
  const start = (currentPage - 1) * size;
  const visible = rows.slice(start, start + size);
  byId("galleryRows").innerHTML = visible.map(rowHtml).join("");
  byId("emptyState").classList.toggle("hidden", rows.length !== 0);
  const counts = {done: 0, pending: 0, failed: 0};
  rows.forEach(row => { counts[rowStatus(row)] += 1; });
  byId("resultSummary").textContent = `${rows.length} matching rows · ${counts.done} done · ${counts.pending} pending · ${counts.failed} errors`;
  byId("pageStatus").textContent = rows.length ? `Page ${currentPage} of ${pages} · rows ${start + 1}–${start + visible.length}` : "No rows";
  byId("prevPage").disabled = currentPage <= 1;
  byId("nextPage").disabled = currentPage >= pages;
  document.querySelectorAll(".image-button").forEach(button => button.addEventListener("click", () => openModal(button.dataset.image, button.dataset.label)));
}

function openModal(path, label) { byId("modalImage").src = path; byId("modalInfo").textContent = label; byId("assetModal").classList.add("active"); }
function closeModal() { byId("assetModal").classList.remove("active"); byId("modalImage").src = ""; }

function initializeGallery() {
  const meta = GENERATION_DATA.metadata;
  byId("subtitle").textContent = `${meta.row_count} distinct prompts · two 40-row selections · four corrected inputs · built ${meta.built_at_utc}`;
  byId("progress").innerHTML = `<strong>${escapeHtml(meta.status_counts.done)} / ${escapeHtml(meta.row_count)}</strong><span>generated</span>`;
  byId("downloads").innerHTML = meta.downloads.map(item => `<a href="${escapeHtml(item.path)}" download>${escapeHtml(item.label)}</a>`).join("");
  addOptions("selectionFilter", meta.selections);
  addOptions("environmentFilter", meta.environments);
  addOptions("deviceFilter", meta.devices);
  addOptions("viewFilter", meta.views);
  ["searchInput", "selectionFilter", "environmentFilter", "deviceFilter", "viewFilter", "statusFilter", "pageSize"].forEach(id => byId(id).addEventListener(id === "searchInput" ? "input" : "change", () => { currentPage = 1; render(); }));
  byId("prevPage").addEventListener("click", () => { currentPage -= 1; render(); scrollTo({top: 0, behavior: "smooth"}); });
  byId("nextPage").addEventListener("click", () => { currentPage += 1; render(); scrollTo({top: 0, behavior: "smooth"}); });
  byId("assetModal").addEventListener("click", event => { if (event.target === byId("assetModal")) closeModal(); });
  document.querySelector(".close-btn").addEventListener("click", closeModal);
  document.addEventListener("keydown", event => { if (event.key === "Escape") closeModal(); });
  byId("loading").classList.add("hidden");
  byId("content").classList.remove("hidden");
  render();
}

document.addEventListener("DOMContentLoaded", initializeGallery);
