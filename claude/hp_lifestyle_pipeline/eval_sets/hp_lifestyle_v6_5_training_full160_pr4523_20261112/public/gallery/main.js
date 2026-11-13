"use strict";
let DATA;
const escapeHtml = value => String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#039;");
const inputLabel = group => `${group.device} / ${group.camera}`;
const sourceText = value => typeof value === "string" ? value : JSON.stringify(value, null, 2);

function cardHtml(card, experiment, group) {
    const label = `${inputLabel(group)} - ${experiment.label} - rank ${card.rank}`;
    const inputs = card.inputs ? `<details class="model-inputs"><summary>Actual generation inputs</summary>
      <p>${escapeHtml(card.generation_prompt)}</p>
      ${["product", "reference", "geometry_guide"].map(role => `<h4>${escapeHtml(role)}</h4>
        <img src="${escapeHtml(card.inputs[role])}" alt="${escapeHtml(role)}" loading="lazy">`).join("")}
      <p><a href="${escapeHtml(card.record_url)}">Generation record</a> |
        <a href="${escapeHtml(card.inputs.audit_url)}">Actual-input hash bindings</a></p></details>` : "";
    return `<article class="card" data-rank="${card.rank}" data-prompt-key="${escapeHtml(card.prompt_key)}">
      <img class="card-image" src="${escapeHtml(card.image)}" alt="${escapeHtml(label)}"
        loading="lazy" decoding="async" width="2368" height="1776">
      <div class="card-body">
        <p class="card-caption"><strong>${card.rank} / 10</strong> - ${escapeHtml(card.environment)}</p>
        <details class="source-prompt"${document.getElementById("showPrompts").checked ? " open" : ""}>
          <summary>Source prompt</summary><p>${escapeHtml(card.prompt)}</p>
          <div class="prompt-key">${escapeHtml(card.prompt_key)}</div>
        </details>${inputs}
      </div>
    </article>`;
}

function contextHtml(context) {
    return `<details class="source-context"><summary>${escapeHtml(context.label)}</summary>
      <h4>Smart Brief</h4><pre>${escapeHtml(sourceText(context.input.smart_brief))}</pre>
      <h4>Source messaging</h4><pre>${escapeHtml(sourceText(context.input.source_messaging))}</pre>
    </details>`;
}

function groupHtml(group, selectedExperiment) {
    const experiments = group.experiments.filter(item => !selectedExperiment || item.id === selectedExperiment);
    return `<section class="input-group" id="${escapeHtml(group.id)}">
      <h2>${escapeHtml(inputLabel(group))}</h2>
      <p class="input-subtitle muted">${escapeHtml(group.camera_tag)} - ranks 1-10 from one input bank per experiment</p>
      <details class="input-context"><summary>Smart Brief and source messaging for this input</summary>
        ${group.contexts.map(contextHtml).join("")}
      </details>
      ${experiments.map(experiment => `<section class="experiment" data-experiment="${escapeHtml(experiment.id)}">
        <h3>${escapeHtml(experiment.label)} <span class="muted">- 10 generations</span></h3>
        <div class="cards">${experiment.cards.map(card => cardHtml(card, experiment, group)).join("")}</div>
      </section>`).join("")}
    </section>`;
}

function render() {
    if (!DATA) return;
    const selectedBank = document.getElementById("bank").value;
    const selectedExperiment = document.getElementById("experiment").value;
    const groups = DATA.groups.filter(group => !selectedBank || group.id === selectedBank);
    document.getElementById("groups").innerHTML = groups.map(group => groupHtml(group, selectedExperiment)).join("");
    const experiments = selectedExperiment ? 1 : DATA.experiment_count;
    document.getElementById("status").textContent =
        `${groups.length} / 16 inputs shown | ${experiments} experiments | ${groups.length * experiments * 10} / ${DATA.image_count} images`;
    document.getElementById("bankNav").innerHTML = groups.map(group =>
        `<a href="#${escapeHtml(group.id)}">${escapeHtml(inputLabel(group))}</a>`).join("");
}

async function onAuthReady() {
    const errorBox = document.getElementById("error");
    errorBox.textContent = "";
    try {
        const response = await fetch("./data.json", {cache: "no-store"});
        if (!response.ok) throw new Error(`Gallery data HTTP ${response.status}`);
        const value = await response.json();
        if (value.groups.length !== 16 || ![2, 4].includes(value.experiment_count) ||
            value.image_count !== 160 * value.experiment_count ||
            value.groups.some(group => group.experiments.length !== value.experiment_count ||
                group.experiments.some(experiment => experiment.cards.length !== 10))) {
            throw new Error("Expected sixteen complete inputs with ten images per experiment.");
        }
        DATA = value;
        document.getElementById("sourceLink").href = DATA.source_url;
        document.getElementById("bank").innerHTML = '<option value="">All 16 inputs</option>' +
            DATA.groups.map(group => `<option value="${escapeHtml(group.id)}">${escapeHtml(inputLabel(group))}</option>`).join("");
        document.getElementById("experiment").innerHTML = `<option value="">All ${DATA.experiment_count} experiments</option>` +
            DATA.groups[0].experiments.map(item => `<option value="${escapeHtml(item.id)}">${escapeHtml(item.label)}</option>`).join("");
        render();
    } catch (error) {
        console.error("Grouped gallery failed to load", error);
        errorBox.textContent = `Unable to load the grouped gallery: ${error.message}`;
    }
}

document.getElementById("bank").addEventListener("change", render);
document.getElementById("experiment").addEventListener("change", render);
document.getElementById("columns").addEventListener("input", event => {
    document.documentElement.style.setProperty("--columns", event.target.value);
    document.getElementById("columnValue").textContent = event.target.value;
});
document.getElementById("showPrompts").addEventListener("change", event => {
    document.querySelectorAll(".source-prompt").forEach(details => { details.open = event.target.checked; });
});
document.getElementById("groups").addEventListener("click", event => {
    if (!event.target.classList.contains("card-image")) return;
    document.getElementById("largeImage").src = event.target.src;
    document.getElementById("largeImage").alt = event.target.alt;
    document.getElementById("imageLabel").textContent = event.target.alt;
    document.getElementById("originalImage").href = event.target.src;
    document.getElementById("lightbox").showModal();
});
document.getElementById("closeImage").addEventListener("click", () => document.getElementById("lightbox").close());
