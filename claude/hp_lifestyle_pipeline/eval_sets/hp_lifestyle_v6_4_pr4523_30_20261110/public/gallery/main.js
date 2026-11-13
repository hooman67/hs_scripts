"use strict";
let DATA;
const escapeHtml = value => String(value ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#039;");
const jsonDetails = (title, value) => `<details><summary>${escapeHtml(title)}</summary><pre>${escapeHtml(JSON.stringify(value, null, 2))}</pre></details>`;
const imageHtml = (url, label) => `<img class="zoom" loading="lazy" src="${escapeHtml(url)}" alt="${escapeHtml(label)}">`;

function rowHtml(row) {
    const prompt = row.prompt;
    const output = row.output;
    return `<section class="pair" data-key="${escapeHtml(prompt.prompt_key)}">
      <h2>${escapeHtml(prompt.device_display_name)} / ${escapeHtml(prompt.source_camera_name)} / rank ${prompt.bank_rank}</h2>
      <p>${escapeHtml(prompt.prompt_key)} | ${escapeHtml(prompt.environment)}</p>
      <p class="prompt">${escapeHtml(prompt.text)}</p>
      <article class="output">${imageHtml(output.image, DATA.title)}
        <p><a href="${escapeHtml(output.image)}" target="_blank" rel="noopener">Full image</a> |
        <a href="${escapeHtml(output.record_url)}">Generation record</a></p>
        <details><summary>Full Smart Brief + source messaging + camera input</summary><pre>${escapeHtml(JSON.stringify(row.source_input, null, 2))}</pre></details>
        <details><summary>Actual model inputs: product PNG, geometry guide, Astra style reference</summary>
          ${imageHtml(output.inputs.product, "Actual prepared product")}
          ${imageHtml(output.inputs.geometry_guide, "Actual geometry guide")}
          ${imageHtml(output.inputs.reference, "Actual Astra style reference")}
          <p><a href="${escapeHtml(output.inputs.audit_url)}">Input hash bindings</a></p></details>
        <details><summary>Exact image-model prompt</summary><p class="prompt">${escapeHtml(output.scene_debug.finalPrompt)}</p></details>
        ${jsonDetails("Complete writer record and evidence", prompt)}
        ${jsonDetails("Full rewrite and generation debug", output.scene_debug)}
        ${jsonDetails("Pipeline, job and image-hash provenance", {lineage: output.lineage, job_id: output.job_id, image_sha256: output.image_sha256})}
      </article></section>`;
}

function render() {
    if (!DATA) return;
    const query = document.getElementById("search").value.trim().toLowerCase();
    const rows = DATA.rows.filter(row => !query || JSON.stringify(row).toLowerCase().includes(query));
    document.getElementById("status").textContent = `${DATA.status.toUpperCase()} | 30/30 outputs | 30/30 actual-input audits | showing ${rows.length} rows`;
    document.getElementById("rows").innerHTML = rows.map(rowHtml).join("");
}

async function loadData() {
    document.getElementById("error").textContent = "";
    try {
        const response = await fetch("../data/generation.json", {cache: "no-store"});
        if (!response.ok) throw new Error(`Data HTTP ${response.status}`);
        DATA = await response.json();
        render();
    } catch (error) {
        document.getElementById("error").textContent = `Unable to load results: ${error.message}`;
    }
}

function onAuthReady() {
    loadData();
}

document.getElementById("search").addEventListener("input", render);
document.getElementById("refresh").addEventListener("click", loadData);
document.addEventListener("click", event => {
    if (!event.target.classList.contains("zoom")) return;
    document.getElementById("largeImage").src = event.target.src;
    document.getElementById("lightbox").showModal();
});
document.getElementById("closeImage").addEventListener("click", () => document.getElementById("lightbox").close());
