"use strict";
let DATA;
const escapeHtml = value => String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#039;");
const jsonText = value => typeof value === "string" ? value : JSON.stringify(value, null, 2);

function card(cell, label) {
    return `<article class="card"><h3>${escapeHtml(label)}</h3>
      <img class="output" src="${escapeHtml(cell.image)}" alt="${escapeHtml(label)}"
        width="2368" height="1776" loading="lazy" decoding="async">
      <p class="muted">${escapeHtml(cell.environment)}</p>
      <details class="source-prompt"${document.getElementById("showPrompts").checked ? " open" : ""}>
        <summary>Source prompt</summary><p>${escapeHtml(cell.prompt)}</p></details>
      <details class="inputs"><summary>Actual generation inputs</summary>
        <div class="input-grid">${["product", "reference", "geometry_guide"].map(role =>
            `<figure><figcaption>${escapeHtml(role.replaceAll("_", " "))}</figcaption>
              <img src="${escapeHtml(cell.inputs[role])}" alt="${escapeHtml(role)}" loading="lazy"></figure>`).join("")}</div>
        <a href="${escapeHtml(cell.inputs.audit_url)}" target="_blank" rel="noopener">Input hash bindings</a>
      </details></article>`;
}

function render() {
    if (!DATA) return;
    const selected = document.getElementById("device").value;
    const rows = DATA.rows.filter(row => !selected || row.key[0] === selected);
    document.getElementById("comparison").innerHTML = rows.map(row =>
        `<section class="pair" data-key="${escapeHtml(row.key.join(" / "))}">
          <h2>${escapeHtml(row.device)} / ${escapeHtml(row.camera)} / rank ${row.rank}</h2>
          <div class="columns">${card(row.v6_4, "V6.4 / PR 4523 - V15.7 shapes")}
            ${card(row.v6_5, "V6.5 / PR 4523 - V15.7 shapes")}</div>
          <details class="feedback"><summary>Original V6.4 C-Tech feedback and Astra's design response</summary>
            <h3>Original C-Tech comment</h3><p>${escapeHtml(row.feedback)}</p>
            <h3>Astra's proposed writer changes</h3>
            <ul>${row.astra_disposition.writer_changes.map(value => `<li>${escapeHtml(value)}</li>`).join("")}</ul>
            <h3>Downstream limitations</h3>
            <ul>${row.astra_disposition.downstream_limitations.map(value => `<li>${escapeHtml(value)}</li>`).join("")}</ul>
            <p class="muted">This is the design response to the original slot, not a judgment that the new ranked scene implements every suggestion.</p>
          </details>
          <details class="source-context"><summary>Original Smart Brief and source messaging</summary>
            <h3>Smart Brief</h3><pre>${escapeHtml(jsonText(row.source_input.smart_brief))}</pre>
            <h3>Source messaging</h3><pre>${escapeHtml(jsonText(row.source_input.source_messaging))}</pre>
          </details>
        </section>`).join("");
    document.getElementById("status").textContent = `${rows.length} / 30 matched slots - ${rows.length * 2} images`;
}

async function onAuthReady() {
    try {
        const response = await fetch("./data.json", {cache: "no-store"});
        if (!response.ok) throw new Error(`Gallery data HTTP ${response.status}`);
        const data = await response.json();
        if (data.rows.length !== 30 || data.image_count !== 60) throw new Error("Expected30 complete two-column comparisons.");
        DATA = data;
        const devices = [...new Map(DATA.rows.map(row => [row.key[0], row.device])).entries()];
        document.getElementById("device").innerHTML = '<option value="">All devices</option>' +
            devices.map(([id, name]) => `<option value="${escapeHtml(id)}">${escapeHtml(name)}</option>`).join("");
        render();
    } catch (error) {
        console.error("V6.5 comparison failed", error);
        document.getElementById("error").textContent = `Unable to load comparison: ${error.message}`;
    }
}

document.getElementById("device").addEventListener("change", render);
document.getElementById("showPrompts").addEventListener("change", event => {
    document.querySelectorAll(".source-prompt").forEach(details => { details.open = event.target.checked; });
});
document.getElementById("comparison").addEventListener("click", event => {
    const image = event.target.closest("img");
    if (!image) return;
    document.getElementById("largeImage").src = image.src;
    document.getElementById("largeImage").alt = image.alt;
    document.getElementById("originalImage").href = image.src;
    document.getElementById("lightbox").showModal();
});
document.getElementById("closeImage").addEventListener("click", () => document.getElementById("lightbox").close());
