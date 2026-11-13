const caseById = new Map(Object.entries(EVAL_DATA.cases));
const promptByKey = new Map(Object.entries(EVAL_DATA.prompts));
const renderById = new Map(Object.entries(EVAL_DATA.renders));

let currentPage = 1;
let controlsInitialized = false;

function escapeHtml(value) {
    return String(value ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#039;");
}

function referencePath(render) { return `../assets/references/${encodeURIComponent(render.reference_asset_filename)}`; }
function outputPath(result) { return `../images/${encodeURIComponent(result.generated_image.filename)}`; }
function rowStatus(row) { return row.status || "missing"; }
function referenceIdentity(render) { return render.product_provenance?.device_asset_name_from_folder || render.render_id; }

function onAuthReady() {
    if (!controlsInitialized) { initializeControls(); controlsInitialized = true; }
    render();
}

function addOptions(id, values, labeler = value => value) {
    const select = document.getElementById(id);
    values.forEach(value => {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = labeler(value);
        select.appendChild(option);
    });
}

function initializeControls() {
    const m = EVAL_DATA.metadata;
    const finalPart = m.prompt_case_set_complete
        ? `${m.planned_generation_row_count} final image rows`
        : `${m.planned_generation_row_count} image rows currently known; final count waits for variable prompt outputs`;
    document.getElementById("subtitle").textContent =
        `${m.manifest_case_count} input cases · ${m.accepted_case_count} accepted / ${m.pending_case_count} pending · ` +
        `${m.source_render_pair_count} source-render pairs · ${finalPart}`;
    document.getElementById("runContext").textContent = JSON.stringify(EVAL_DATA.run_context, null, 2);

    addOptions("deviceFilter", [...new Set(EVAL_DATA.rows.map(row => row.device_type))].sort());
    addOptions("cameraFilter", [...new Set(EVAL_DATA.rows.map(row => row.camera_tag))].sort());
    addOptions("sourceFilter", [...new Set(EVAL_DATA.rows.map(row => row.source_id))].sort());
    addOptions("referenceFilter", [...new Set(EVAL_DATA.rows.map(row => referenceIdentity(renderById.get(row.render_id))))].sort());
    addOptions("statusFilter", [...new Set(EVAL_DATA.rows.map(rowStatus))].sort());
    addOptions("promptFilter", [...promptByKey.keys()].sort(), key => {
        const p = promptByKey.get(key);
        return `${p.source_id} · ${p.camera_tag} · ${p.prompt_id} · ${p.environment}`;
    });

    ["searchInput", "deviceFilter", "cameraFilter", "sourceFilter", "referenceFilter", "promptFilter", "statusFilter", "pageSize"].forEach(id => {
        document.getElementById(id).addEventListener(id === "searchInput" ? "input" : "change", () => { currentPage = 1; render(); });
    });
    document.getElementById("prevPage").addEventListener("click", () => { currentPage = Math.max(1, currentPage - 1); render(); window.scrollTo({top:0, behavior:"smooth"}); });
    document.getElementById("nextPage").addEventListener("click", () => { currentPage += 1; render(); window.scrollTo({top:0, behavior:"smooth"}); });
    const modal = document.getElementById("assetModal");
    modal.addEventListener("click", event => { if (event.target === modal) closeModal(); });
    modal.querySelector(".close-btn").addEventListener("click", closeModal);
    document.addEventListener("keydown", event => { if (event.key === "Escape") closeModal(); });
}

function filteredRows() {
    const query = document.getElementById("searchInput").value.trim().toLowerCase();
    const filters = {
        device_type: document.getElementById("deviceFilter").value,
        camera_tag: document.getElementById("cameraFilter").value,
        source_id: document.getElementById("sourceFilter").value,
        prompt_key: document.getElementById("promptFilter").value,
        status: document.getElementById("statusFilter").value,
        reference: document.getElementById("referenceFilter").value,
    };
    return EVAL_DATA.rows.filter(row => {
        const prompt = promptByKey.get(row.prompt_key);
        const render = renderById.get(row.render_id);
        if (filters.device_type !== "all" && row.device_type !== filters.device_type) return false;
        if (filters.camera_tag !== "all" && row.camera_tag !== filters.camera_tag) return false;
        if (filters.source_id !== "all" && row.source_id !== filters.source_id) return false;
        if (filters.prompt_key !== "all" && row.prompt_key !== filters.prompt_key) return false;
        if (filters.status !== "all" && rowStatus(row) !== filters.status) return false;
        if (filters.reference !== "all" && referenceIdentity(render) !== filters.reference) return false;
        if (!query) return true;
        const result = row.result || {};
        return [row.row_id, row.source_id, row.camera_tag, row.render_id, referenceIdentity(render), render.source_camera_name,
            prompt?.text, prompt?.environment, prompt?.prompt_id, result.usedPrompt, result.job_id, result.request_id]
            .join(" ").toLowerCase().includes(query);
    });
}

function evidenceHtml(items) {
    if (!items?.length) return "";
    return `<ul>${items.map(item => `<li><code>${escapeHtml(item.path)}</code>: “${escapeHtml(item.quote)}”</li>`).join("")}</ul>`;
}

function explanationHtml(row) {
    const caseData = caseById.get(row.case_id);
    const accepted = caseData.accepted;
    if (!accepted) return `<p class="fallback-status">Prompt case has not been accepted yet.</p>`;
    const debug = accepted.debug || {};
    const sections = [];
    if (debug.input_assessment) sections.push(`<h4>Input assessment</h4><p>${escapeHtml(debug.input_assessment)}</p>`);
    if (debug.count_explanation) sections.push(`<h4>Prompt-count rationale</h4><p>${escapeHtml(debug.count_explanation)}</p>`);
    const mappings = (debug.ksp_mappings || []).filter(item => !row.prompt_id || (item.prompt_ids || []).includes(row.prompt_id));
    if (mappings.length) sections.push(`<h4>KSPs mapped to this prompt</h4>${mappings.map(mapping => `<div class="reason-block"><strong>${escapeHtml(mapping.ksp_id)}</strong><p>${escapeHtml(mapping.explanation)}</p>${evidenceHtml(mapping.source_evidence)}</div>`).join("")}`);
    const vp = debug.value_proposition;
    if (vp && (!row.prompt_id || (vp.prompt_ids || []).includes(row.prompt_id))) sections.push(`<h4>Value proposition</h4><p>${escapeHtml(vp.explanation)}</p>${evidenceHtml(vp.source_evidence)}`);
    const additions = (debug.creative_additions || []).filter(item => !row.prompt_id || item.prompt_id === row.prompt_id).flatMap(item => item.details || []);
    if (additions.length) sections.push(`<h4>Creative additions</h4><ul>${additions.map(item => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`);
    if (caseData.manifest.requires_manual_fallback_review) sections.push(`<p class="fallback-status">Unknown camera fallback: manual review required and recorded in the accepted case.</p>`);
    sections.push(`<details><summary>Complete accepted prompt-case record</summary><pre>${escapeHtml(JSON.stringify(accepted, null, 2))}</pre></details>`);
    return sections.join("");
}

function promptHtml(row) {
    const prompt = promptByKey.get(row.prompt_key);
    const caseData = caseById.get(row.case_id);
    const fallback = caseData.manifest.requires_manual_fallback_review ? `<span class="badge fallback">unknown fallback reviewed</span>` : "";
    if (!prompt) return `<div class="badges"><span class="badge device">${escapeHtml(row.device_type)}</span><span class="badge camera">${escapeHtml(row.camera_tag)}</span>${fallback}</div><div class="pending-message">Prompt case is ${escapeHtml(caseData.prompt_status)}. This source-render pair is a provisional placeholder, not a final image row.</div><div class="record-id">${escapeHtml(row.source_id)} · ${escapeHtml(row.case_id)}</div>`;
    return `<div class="badges"><span class="badge device">${escapeHtml(row.device_type)}</span><span class="badge camera">${escapeHtml(row.camera_tag)}</span><span class="badge environment">${escapeHtml(prompt.environment)}</span>${fallback}</div><p class="prompt-text">${escapeHtml(prompt.text)}</p><div class="record-id">${escapeHtml(row.source_id)} · ${escapeHtml(row.case_id)}/${escapeHtml(prompt.prompt_id)} · ${escapeHtml(row.row_id)}</div>`;
}

function twinHtml(row) {
    const render = renderById.get(row.render_id);
    const path = referencePath(render);
    const identity = referenceIdentity(render);
    return `<button class="image-button" type="button" data-image="${path}" data-label="Reference · ${escapeHtml(render.render_id)}"><img loading="lazy" src="${path}" width="${render.width}" height="${render.height}" alt="${escapeHtml(render.render_id)} digital twin"></button><div class="twin-meta"><strong>${escapeHtml(identity)}</strong><span>${escapeHtml(render.camera_tag)} · source ${escapeHtml(render.source_camera_name)}</span><span>${escapeHtml(render.render_id)}</span><span>${render.width}×${render.height} PNG · ${escapeHtml(render.sha256)}</span></div>`;
}

function sourceHtml(row) {
    const c = caseById.get(row.case_id);
    const fullInput = {source_messaging: EVAL_DATA.sources[row.source_id], camera_tag: c.input.camera_tag};
    return `<details><summary>View full runtime input</summary><div class="detail-meta">${escapeHtml(c.input.input_path)} · ${escapeHtml(c.input.input_sha256)}</div><pre>${escapeHtml(JSON.stringify(fullInput, null, 2))}</pre></details><details><summary>View source provenance</summary><pre>${escapeHtml(JSON.stringify(c.source, null, 2))}</pre></details>`;
}

function outputHtml(row) {
    const result = row.result;
    const status = rowStatus(row);
    if (status !== "done") {
        const text = result?.error || (status === "missing" ? "Generation record is missing for this accepted prompt row." : status === "prompt_pending" ? "Waiting for the prompt case; this is a provisional pair placeholder." : `Generation status: ${status}`);
        return `<span class="status-pill ${escapeHtml(status)}">${escapeHtml(status)}</span><div class="${status.includes("pending") ? "pending-message" : "failure-message"}">${escapeHtml(text)}</div>`;
    }
    const image = result.generated_image;
    const path = outputPath(result);
    return `<button class="image-button" type="button" data-image="${path}" data-label="Generated · ${escapeHtml(row.row_id)}"><img loading="lazy" src="${path}" width="${image.native_width}" height="${image.native_height}" alt="Generated output for ${escapeHtml(row.row_id)}"></button><div class="output-meta"><span>Seed ${escapeHtml(result.returned_seed)}</span><span>${image.native_width}×${image.native_height}</span></div><div class="asset-hash">${escapeHtml(image.sha256)}</div>`;
}

function rewrittenPromptHtml(row) {
    const result = row.result;
    if (!result || rowStatus(row) !== "done") return `<span class="status-pill ${escapeHtml(rowStatus(row))}">${escapeHtml(rowStatus(row))}</span>`;
    return `<details><summary>View rewritten prompt</summary><pre class="generation-pre">${escapeHtml(result.usedPrompt || "")}</pre></details>`;
}

function generationDebugHtml(row) {
    const result = row.result;
    if (!result) return `<span class="status-pill ${escapeHtml(rowStatus(row))}">${escapeHtml(rowStatus(row))}</span>`;
    return `<details><summary>View complete generation record</summary><pre class="generation-pre">${escapeHtml(JSON.stringify(result, null, 2))}</pre></details>`;
}

function rowHtml(row) {
    return `<tr><td class="prompt-cell">${promptHtml(row)}</td><td class="twin-cell">${twinHtml(row)}</td><td class="collapsible-cell">${sourceHtml(row)}</td><td class="collapsible-cell"><details><summary>View explanation</summary><div class="explanation">${explanationHtml(row)}</div></details></td><td class="output-cell">${outputHtml(row)}</td><td class="collapsible-cell">${rewrittenPromptHtml(row)}</td><td class="collapsible-cell">${generationDebugHtml(row)}</td></tr>`;
}

function render() {
    const rows = filteredRows();
    const selected = document.getElementById("pageSize").value;
    const pageSize = selected === "all" ? Math.max(rows.length, 1) : Number(selected);
    const pageCount = Math.max(1, Math.ceil(rows.length / pageSize));
    currentPage = Math.min(currentPage, pageCount);
    const start = (currentPage - 1) * pageSize;
    const visible = rows.slice(start, start + pageSize);
    document.getElementById("evalRows").innerHTML = visible.map(rowHtml).join("");
    document.getElementById("emptyState").classList.toggle("hidden", rows.length !== 0);
    const counts = {};
    rows.forEach(row => { counts[rowStatus(row)] = (counts[rowStatus(row)] || 0) + 1; });
    document.getElementById("resultSummary").textContent = `${rows.length} displayed row objects · ${Object.entries(counts).sort().map(([k,v]) => `${v} ${k}`).join(" · ")} · ${new Set(rows.map(row => row.case_id)).size} cases · ${new Set(rows.map(row => row.render_id)).size} renders`;
    document.getElementById("pageStatus").textContent = rows.length ? `Page ${currentPage} of ${pageCount} · rows ${start + 1}–${start + visible.length}` : "No rows";
    document.getElementById("prevPage").disabled = currentPage <= 1;
    document.getElementById("nextPage").disabled = currentPage >= pageCount;
    document.querySelectorAll(".image-button").forEach(button => button.addEventListener("click", () => openModal(button.dataset.image, button.dataset.label)));
}

function openModal(path, label) { document.getElementById("modalImage").src = path; document.getElementById("modalInfo").textContent = label; document.getElementById("assetModal").classList.add("active"); }
function closeModal() { document.getElementById("assetModal").classList.remove("active"); document.getElementById("modalImage").src = ""; }
