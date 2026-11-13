"use strict";
let DATA;
let currentTab = "comparison";
const escapeHtml = value => String(value ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#039;");
const jsonDetails = (title, value) => `<details><summary>${escapeHtml(title)}</summary><pre>${escapeHtml(JSON.stringify(value, null, 2))}</pre></details>`;
const imageHtml = (url, label, cls = "") => `<img class="zoom ${cls}" loading="lazy" src="${escapeHtml(url)}" alt="${escapeHtml(label)}">`;

function outputHtml(output, title) {
    if (output.status !== "done") {
        return `<article class="output ${escapeHtml(output.status)}"><h4>${escapeHtml(title)}</h4><p>${escapeHtml(output.status.toUpperCase())}</p><pre>${escapeHtml(output.error || "")}</pre></article>`;
    }
    const debug = output.scene_debug;
    return `<article class="output"><h4>${escapeHtml(title)}</h4>${imageHtml(output.image, title)}
        <p><a href="${escapeHtml(output.image)}" target="_blank" rel="noopener">Full image</a> |
        <a href="${escapeHtml(output.record_url)}">Generation record</a></p>
        <details><summary>Exact image-model prompt</summary><p class="prompt">${escapeHtml(debug.finalPrompt)}</p></details>
        ${output.guide ? `<details><summary>Geometry-guide image input</summary>${imageHtml(output.guide, "Actual geometry guide")}</details>` : "<p class='muted'>Guide image not materialized in this record; geometry and input order remain in generation debug.</p>"}
        ${output.inputs ? `<details><summary>Actual prepared product and Astra style reference</summary>
            ${imageHtml(output.inputs.product, "Actual prepared product")}${imageHtml(output.inputs.reference, "Astra style reference")}
            <p><a href="${escapeHtml(output.inputs.audit_url)}">Input hash bindings and evidence limits</a></p></details>` : ""}
        ${jsonDetails("Full rewrite, geometry and generation debug", debug)}
        ${jsonDetails("Pipeline, job and image-hash provenance", {lineage: output.lineage, job_id: output.job_id, image_sha256: output.image_sha256})}
        <p class="muted">No judge verdict supplied for this image; the historical judge regression uses another set.</p></article>`;
}

function promptHtml(prompt, writer) {
    return `<article><h3>${escapeHtml(writer)} - ${escapeHtml(prompt.environment)}</h3>
        <p>Source ${prompt.source_relevance_score}/100 | C-Tech ${prompt.ctech_reference_score}/100 | rank ${prompt.bank_rank}</p>
        <p class="prompt">${escapeHtml(prompt.text)}</p>
        <p class="muted">Approved props: ${escapeHtml(prompt.prop_ids.join(", "))}</p>
        ${jsonDetails("Complete writer record, evidence, scores and camera rationale", prompt)}</article>`;
}

function comparisonHtml(row) {
    return `<section class="pair"><div class="row-title">${imageHtml(row.twin, "Input digital twin", "twin")}
        <div><h2>${escapeHtml(row.device)} / ${escapeHtml(row.camera)} / rank ${row.rank}</h2>
        <p>${escapeHtml(row.key.join(" / "))}</p>${jsonDetails("Full original Smart Brief + source messaging + camera input", row.source_input)}</div></div>
        <div class="prompt-pair">${promptHtml(row.prompts.v6_2, "V6.2")}${promptHtml(row.prompts.v6_3, "V6.3")}</div>
        <div class="image-scroll"><div class="image-grid">
        ${outputHtml(row.outputs.v6_2_pr4417, "V6.2 / PR 4417 - V15.6")}
        ${outputHtml(row.outputs.v6_2_pr4523, "V6.2 / PR 4523 - V15.7 shapes")}
        ${outputHtml(row.outputs.v6_3_pr4417, "V6.3 / PR 4417 - V15.6")}
        ${outputHtml(row.outputs.v6_3_pr4523, "V6.3 / PR 4523 - V15.7 shapes")}
        </div></div>
        <details class="historical"><summary>Additional historical V6.2 reference: V20 + local shape patch (NOT PR 4523)</summary>
        ${outputHtml(row.historical, "Historical only: PR4349 + local V20 surface-shape-r1")}</details></section>`;
}

function render() {
    if (!DATA) return;
    const query = document.getElementById("search").value.trim().toLowerCase();
    const match = row => !query || JSON.stringify(row).toLowerCase().includes(query);
    document.getElementById("status").textContent = `${DATA.status.toUpperCase()} | ${
        Object.entries(DATA.cells).map(([name, counts]) => `${name}: ${counts.done}/30 done, ${counts.failed} failed`).join(" | ")
    } | ${DATA.actual_input_audits || 0}/120 actual-input audits | snapshot ${DATA.built_at_utc}`;
    document.getElementById("comparison").innerHTML = DATA.rows.filter(match).map(comparisonHtml).join("");
    const banks = Object.entries(DATA.all_v63.bank_audit);
    document.getElementById("prompts").innerHTML = banks.map(([bank, audit]) => {
        const prompts = DATA.all_v63.prompts.filter(prompt => prompt.bank_debug_ref === bank).filter(match);
        if (!prompts.length) return "";
        return `<section class="pair"><h2>${escapeHtml(bank)}</h2>
            ${jsonDetails("Full writer input", audit.source_input)}${jsonDetails("Full writer bank debug and call provenance", audit)}
            ${prompts.map(prompt => promptHtml(prompt, "V6.3")).join("")}</section>`;
    }).join("");
    const judge = DATA.judge;
    document.getElementById("judges").innerHTML = `<p>${escapeHtml(judge.notice || "")}</p>
        ${jsonDetails("Judge candidate, calibration status and provenance", judge)}
        ${judge.r1_json_url ? `<p>${escapeHtml(judge.r1_notice)} <a href="${escapeHtml(judge.r1_json_url)}">Download first-candidate full128 comparison JSON</a></p>` : ""}
        ${judge.html_url ? `<p><a href="${escapeHtml(judge.json_url)}">Download V3 / V3.1 comparison JSON</a></p><iframe title="Historical judge regression" src="${escapeHtml(judge.html_url)}"></iframe>` : "<p>Judge regression is pending; no results are inferred.</p>"}`;
    for (const id of ["comparison", "prompts", "judges"]) document.getElementById(id).classList.toggle("hidden", id !== currentTab);
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

function onAuthReady() {
    loadData();
}

document.getElementById("search").addEventListener("input", render);
document.getElementById("refresh").addEventListener("click", loadData);
document.querySelectorAll("[data-tab]").forEach(button => button.addEventListener("click", () => {
    currentTab = button.dataset.tab;
    render();
}));
document.addEventListener("click", event => {
    if (!event.target.classList.contains("zoom")) return;
    document.getElementById("largeImage").src = event.target.src;
    document.getElementById("lightbox").showModal();
});
document.getElementById("closeImage").addEventListener("click", () => document.getElementById("lightbox").close());
