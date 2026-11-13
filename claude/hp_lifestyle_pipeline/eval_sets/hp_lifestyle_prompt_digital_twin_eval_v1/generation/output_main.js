const promptByKey = new Map(EVAL_DATA.prompts.map(prompt => [prompt.key, prompt]));
const twinById = new Map(EVAL_DATA.twins.map(twin => [twin.evalset_item_id, twin]));
const generationResults = EVAL_DATA.generation?.results || {};

let currentPage = 1;
let controlsInitialized = false;

function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function twinPath(twinFile) {
    return `../../assets/digital_twins/${encodeURIComponent(twinFile)}`;
}

function outputPath(outputFile) {
    return `../images/${encodeURIComponent(outputFile)}`;
}

function rowStatus(row) {
    return generationResults[row.row_id]?.status || "missing";
}

function onAuthReady() {
    if (!controlsInitialized) {
        initializeControls();
        controlsInitialized = true;
    }
    render();
}

function initializeControls() {
    const metadata = EVAL_DATA.metadata;
    const generation = EVAL_DATA.generation?.metadata || {};
    document.getElementById("subtitle").textContent =
        `${metadata.prompt_count} prompts × compatible twins = ${metadata.row_count} rows · ` +
        `${generation.done_count || 0} generated · ${generation.failed_count || 0} failed`;

    const deviceFilter = document.getElementById("deviceFilter");
    [...new Set(EVAL_DATA.prompts.map(prompt => prompt.device_category))]
        .sort()
        .forEach(category => {
            const option = document.createElement("option");
            option.value = category;
            option.textContent = `${category} (${metadata.row_counts_by_category[category]} rows)`;
            deviceFilter.appendChild(option);
        });

    const promptFilter = document.getElementById("promptFilter");
    EVAL_DATA.prompts.forEach(prompt => {
        const option = document.createElement("option");
        option.value = prompt.key;
        option.textContent = `${prompt.source_product} · ${prompt.source_id}/${prompt.prompt_id} · ${prompt.environment}`;
        promptFilter.appendChild(option);
    });

    ["searchInput", "deviceFilter", "promptFilter", "statusFilter", "pageSize"].forEach(id => {
        const eventName = id === "searchInput" ? "input" : "change";
        document.getElementById(id).addEventListener(eventName, () => {
            currentPage = 1;
            render();
        });
    });

    document.getElementById("prevPage").addEventListener("click", () => {
        currentPage = Math.max(1, currentPage - 1);
        render();
        window.scrollTo({top: 0, behavior: "smooth"});
    });
    document.getElementById("nextPage").addEventListener("click", () => {
        currentPage += 1;
        render();
        window.scrollTo({top: 0, behavior: "smooth"});
    });

    const modal = document.getElementById("assetModal");
    modal.addEventListener("click", event => {
        if (event.target === modal) closeModal();
    });
    modal.querySelector(".close-btn").addEventListener("click", closeModal);
    document.addEventListener("keydown", event => {
        if (event.key === "Escape") closeModal();
    });
}

function filteredRows() {
    const query = document.getElementById("searchInput").value.trim().toLowerCase();
    const device = document.getElementById("deviceFilter").value;
    const promptKey = document.getElementById("promptFilter").value;
    const status = document.getElementById("statusFilter").value;

    return EVAL_DATA.rows.filter(row => {
        const prompt = promptByKey.get(row.prompt_key);
        const result = generationResults[row.row_id] || {};
        const matchesDevice = device === "all" || row.device_category === device;
        const matchesPrompt = promptKey === "all" || row.prompt_key === promptKey;
        const matchesStatus = status === "all" || rowStatus(row) === status;
        if (!matchesDevice || !matchesPrompt || !matchesStatus) return false;
        if (!query) return true;
        const haystack = [
            prompt.text,
            prompt.environment,
            prompt.source_product,
            prompt.source_id,
            prompt.prompt_id,
            row.twin_id,
            row.device_category,
            result.debugData?.usedPrompt,
            result.job_id,
        ].join(" ").toLowerCase();
        return haystack.includes(query);
    });
}

function evidenceHtml(items) {
    if (!items?.length) return "";
    return `<ul>${items.map(item =>
        `<li><code>${escapeHtml(item.path)}</code>: “${escapeHtml(item.quote)}”</li>`
    ).join("")}</ul>`;
}

function explanationHtml(promptKey) {
    const explanation = EVAL_DATA.explanations[promptKey];
    const sections = [];
    sections.push(`<h4>Input assessment</h4><p>${escapeHtml(explanation.input_assessment)}</p>`);
    sections.push(`<h4>Prompt-count rationale</h4><p>${escapeHtml(explanation.count_explanation)}</p>`);

    if (explanation.ksp_mappings.length) {
        const mappings = explanation.ksp_mappings.map(mapping => `
            <div class="reason-block">
                <strong>${escapeHtml(mapping.ksp_id)}</strong>
                <p>${escapeHtml(mapping.explanation)}</p>
                ${evidenceHtml(mapping.source_evidence)}
            </div>`).join("");
        sections.push(`<h4>KSPs mapped to this prompt</h4>${mappings}`);
    }

    const valueProposition = explanation.value_proposition;
    if (valueProposition && Object.keys(valueProposition).length) {
        sections.push(`
            <h4>Value proposition</h4>
            <p>${escapeHtml(valueProposition.explanation)}</p>
            ${evidenceHtml(valueProposition.source_evidence)}`);
    }

    if (explanation.creative_additions.length) {
        const details = explanation.creative_additions.flatMap(item => item.details || []);
        sections.push(`<h4>Creative additions</h4><ul>${details.map(item =>
            `<li>${escapeHtml(item)}</li>`
        ).join("")}</ul>`);
    }

    sections.push(`<p class="fallback-status">Fallback used: ${explanation.used_fallback ? "Yes" : "No"}</p>`);
    return sections.join("");
}

function outputHtml(row, result) {
    const status = rowStatus(row);
    if (status !== "done") {
        const message = result?.error || (status === "missing" ? "Generation record is missing." : "Generation failed.");
        return `<span class="status-pill ${status}">${escapeHtml(status)}</span>
            <div class="failure-message">${escapeHtml(message)}</div>`;
    }
    const path = outputPath(result.output_image_filename);
    const latency = result.total_latency_ms ? `${(result.total_latency_ms / 1000).toFixed(1)}s` : "smoke import";
    return `
        <button class="image-button" type="button" data-image="${path}" data-label="Output · ${escapeHtml(row.row_id)}">
            <img loading="lazy" src="${path}" alt="Generated output for ${escapeHtml(row.row_id)}">
        </button>
        <div class="output-meta">
            <span>Seed ${escapeHtml(result.output_seed)}</span>
            <span>${escapeHtml(latency)}</span>
        </div>`;
}

function rewrittenPromptHtml(result) {
    if (!result || result.status !== "done") {
        return `<span class="status-pill ${result?.status || "missing"}">${escapeHtml(result?.status || "missing")}</span>`;
    }
    return `<details>
        <summary>View rewritten prompt</summary>
        <pre class="generation-pre">${escapeHtml(result.debugData?.usedPrompt || "")}</pre>
    </details>`;
}

function generationDebugHtml(result) {
    if (!result) {
        return `<span class="status-pill missing">missing</span>`;
    }
    return `<details>
        <summary>View generation debug</summary>
        <div class="detail-meta">Request payload</div>
        <pre class="generation-pre">${escapeHtml(JSON.stringify(result.request_payload || {}, null, 2))}</pre>
        <div class="detail-meta">debugData response</div>
        <pre class="generation-pre">${escapeHtml(JSON.stringify(result.debugData || {}, null, 2))}</pre>
    </details>`;
}

function rowHtml(row) {
    const prompt = promptByKey.get(row.prompt_key);
    const twin = twinById.get(row.twin_id);
    const source = EVAL_DATA.sources[prompt.source_id];
    const result = generationResults[row.row_id];
    const path = twinPath(row.twin_file);
    return `
        <tr>
            <td class="prompt-cell">
                <div class="badges">
                    <span class="badge device">${escapeHtml(prompt.device_category)}</span>
                    <span class="badge environment">${escapeHtml(prompt.environment)}</span>
                </div>
                <p class="prompt-text">${escapeHtml(prompt.text)}</p>
                <div class="record-id">${escapeHtml(prompt.source_product)} · ${escapeHtml(prompt.source_id)}/${escapeHtml(prompt.prompt_id)}</div>
            </td>
            <td class="twin-cell">
                <button class="image-button" type="button" data-image="${path}" data-label="Input · ${escapeHtml(row.twin_id)}">
                    <img loading="lazy" src="${path}" alt="${escapeHtml(row.twin_id)} digital twin">
                </button>
                <div class="twin-meta">
                    <strong>${escapeHtml(row.twin_id)}</strong>
                    <span>${escapeHtml(row.device_category)}</span>
                    <a href="${escapeHtml(twin.source_url)}" target="_blank" rel="noopener">Original asset</a>
                </div>
            </td>
            <td class="collapsible-cell">
                <details>
                    <summary>View source messaging</summary>
                    <div class="detail-meta">Source ${escapeHtml(prompt.source_id)}</div>
                    <pre>${escapeHtml(JSON.stringify(source, null, 2))}</pre>
                </details>
            </td>
            <td class="collapsible-cell">
                <details>
                    <summary>View explanation</summary>
                    <div class="explanation">${explanationHtml(row.prompt_key)}</div>
                </details>
            </td>
            <td class="output-cell">${outputHtml(row, result)}</td>
            <td class="collapsible-cell">${rewrittenPromptHtml(result)}</td>
            <td class="collapsible-cell">${generationDebugHtml(result)}</td>
        </tr>`;
}

function render() {
    const rows = filteredRows();
    const selectedPageSize = document.getElementById("pageSize").value;
    const pageSize = selectedPageSize === "all" ? Math.max(rows.length, 1) : Number(selectedPageSize);
    const pageCount = Math.max(1, Math.ceil(rows.length / pageSize));
    currentPage = Math.min(currentPage, pageCount);
    const start = (currentPage - 1) * pageSize;
    const visibleRows = rows.slice(start, start + pageSize);

    document.getElementById("evalRows").innerHTML = visibleRows.map(rowHtml).join("");
    document.getElementById("emptyState").classList.toggle("hidden", rows.length !== 0);
    const doneCount = rows.filter(row => rowStatus(row) === "done").length;
    document.getElementById("resultSummary").textContent =
        `${rows.length} matching rows · ${doneCount} generated · ` +
        `${new Set(rows.map(row => row.prompt_key)).size} prompts · ` +
        `${new Set(rows.map(row => row.twin_id)).size} twins`;
    document.getElementById("pageStatus").textContent =
        rows.length ? `Page ${currentPage} of ${pageCount} · rows ${start + 1}–${start + visibleRows.length}` : "No rows";
    document.getElementById("prevPage").disabled = currentPage <= 1;
    document.getElementById("nextPage").disabled = currentPage >= pageCount;

    document.querySelectorAll(".image-button").forEach(button => {
        button.addEventListener("click", () => openModal(button.dataset.image, button.dataset.label));
    });
}

function openModal(path, label) {
    document.getElementById("modalImage").src = path;
    document.getElementById("modalInfo").textContent = label;
    document.getElementById("assetModal").classList.add("active");
}

function closeModal() {
    document.getElementById("assetModal").classList.remove("active");
    document.getElementById("modalImage").src = "";
}
