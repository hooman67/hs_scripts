"use strict";
let DATA;
const escapeHtml = value => String(value ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#039;");
const jsonDetails = (title, value) => `<details><summary>${escapeHtml(title)}</summary><pre>${escapeHtml(JSON.stringify(value, null, 2))}</pre></details>`;
const imageHtml = (url, label) => `<img class="zoom" loading="lazy" src="${escapeHtml(url)}" alt="${escapeHtml(label)}">`;
function outputHtml(output, title) {
    const heading = `<h3>${escapeHtml(title)} <span class="badge ${output.reuse_status}">${escapeHtml(output.reuse_status)}</span>${output.restart ? ' <span class="badge">restarted interrupted job</span>' : ""}</h3>`;
    if (output.status !== "done") return `<article class="output ${escapeHtml(output.status)}">${heading}<p>${escapeHtml(output.status.toUpperCase())}</p><pre>${escapeHtml(output.error || "")}</pre>${output.record_url ? `<a href="${escapeHtml(output.record_url)}">Preserved failure record</a>` : ""}</article>`;
    const inputs = output.inputs;
    return `<article class="output">${heading}${imageHtml(output.image, title)}
        <p><a href="${escapeHtml(output.image)}" target="_blank" rel="noopener">Full PNG</a> |
        <a href="${escapeHtml(output.record_url)}">Original generation record</a> |
        <a href="${escapeHtml(output.job_url)}">Job/request</a> |
        <a href="${escapeHtml(output.status_url)}">Full native status</a></p>
        <details><summary>Exact image-model prompt</summary><p>${escapeHtml(output.scene_debug.finalPrompt)}</p></details>
        ${inputs ? `<details><summary>Actual model inputs: product PNG, geometry guide, Astra style reference</summary>
            <h4>Actual prepared product PNG</h4>${imageHtml(inputs.product, "Actual prepared product")}
            <h4>Only image-model input: generated geometry guide</h4>${imageHtml(inputs.geometry_guide, "Actual geometry guide")}
            <h4>Astra style reference (planning/writing only)</h4>${imageHtml(inputs.reference, "Actual Astra style reference")}
            <p><a href="${escapeHtml(inputs.audit_url)}">Hash bindings, original study and evidence boundary</a></p></details>` : "<p>Actual-input materialization pending.</p>"}
        ${jsonDetails("Full rewrite, geometry and generation debug", output.scene_debug)}
        ${jsonDetails("Source, job, image, commit and runtime provenance", {
            reuse_status: output.reuse_status, origin_study_manifest_sha256: output.origin_study_manifest_sha256,
            run_sha256: output.run_sha256, record_sha256: output.record_sha256, job_id: output.job_id,
            image_sha256: output.image_sha256, lineage: output.lineage, restart: output.restart})}
        <p class="muted">Not evaluated by a judge.</p></article>`;
}
function rowHtml(row) {
    const p = row.prompt;
    return `<section class="pair"><h2>${escapeHtml(row.device)} / ${escapeHtml(row.camera)} / rank ${row.rank}</h2>
        <p>${escapeHtml(row.key.join(" / "))} — ${escapeHtml(p.environment)} — Source ${p.source_relevance_score}/100, C-Tech ${p.ctech_reference_score}/100</p>
        <p class="prompt">${escapeHtml(p.text)}</p><p>Approved props: ${escapeHtml((p.prop_ids || []).join(", "))}</p>
        ${jsonDetails("Full Smart Brief, source messaging and camera input", row.source_input)}
        ${jsonDetails("Full writer record, approved props, scores and camera rationale", p)}
        ${jsonDetails("Bank debug, source provenance and original text-service outcome", row.bank_audit)}
        <div class="image-scroll"><div class="image-grid">
        ${outputHtml(row.outputs.v6_3_pr4417, "V6.3 / PR4417 — V21.2")}
        ${outputHtml(row.outputs.v6_3_pr4523, "V6.3 / PR4523 — V21.3 shapes")}
        </div></div></section>`;
}
function render() {
    if (!DATA) return;
    const query = document.getElementById("search").value.trim().toLowerCase();
    const state = document.getElementById("state").value;
    const exactKey = DATA.rows.some(row => row.prompt.prompt_key.toLowerCase() === query);
    const rows = DATA.rows.filter(row => (!query || (exactKey ? row.prompt.prompt_key.toLowerCase() === query :
        `${row.key.join(" ")} ${row.device} ${row.camera} ${JSON.stringify(row.prompt)}`.toLowerCase().includes(query)))
        && (!state || Object.values(row.outputs).some(o => o.status === state || o.reuse_status === state)));
    document.getElementById("status").textContent = `${DATA.status.toUpperCase()} | ${
        Object.entries(DATA.cells).map(([name, c]) => `${name}: ${c.done}/160 done (${c.reused} reused +${c.new_done} new), ${c.failed} failed, ${c.pending} pending`).join(" | ")
    } | ${DATA.actual_input_audits}/320 actual-input audits | ${rows.length}/160 rows shown | ${DATA.built_at_utc}`;
    document.getElementById("comparison").innerHTML = rows.map(rowHtml).join("");
}
async function loadData() {
    document.getElementById("error").textContent = "";
    try {
        const response = await fetch("../data/comparison.json", {cache: "no-store"});
        if (!response.ok) throw new Error(`Comparison data HTTP ${response.status}`);
        DATA = await response.json();
        render();
    } catch (error) {
        document.getElementById("error").textContent = `Unable to load current study results: ${error.message}`;
    }
}
function onAuthReady() { loadData(); }
document.getElementById("refresh").addEventListener("click", loadData);
document.getElementById("search").addEventListener("input", render);
document.getElementById("state").addEventListener("change", render);
document.addEventListener("click", event => {
    if (!event.target.classList.contains("zoom")) return;
    document.getElementById("largeImage").src = event.target.src;
    document.getElementById("lightbox").showModal();
});
document.getElementById("closeImage").addEventListener("click", () => document.getElementById("lightbox").close());
