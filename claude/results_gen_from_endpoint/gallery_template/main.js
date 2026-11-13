// Renders prompt cards from GALLERY_DATA (defined in data.js).
//   GALLERY_DATA = {
//     meta: { title, subtitle, total_rows, n_done, n_failed },
//     prompts: [{ pid, category, ar, original_prompt, rows: [{
//        input_seed, model_seed, image_filename, rewritten_prompt, rewritten_negative_prompt,
//        status, error_code, error_message
//     }, ...]}, ...]
//   }

let activeCategory = "all";
let searchQ = "";
let onlyFailed = false;
let modalIndex = 0;
let modalImages = [];

function onAuthReady() {
    renderHeader();
    renderCategoryNav();
    renderGallery();
    wireControls();
}

function renderHeader() {
    document.title = GALLERY_DATA.meta.title;
    const h1 = document.querySelector(".header-bar h1");
    if (h1) h1.textContent = GALLERY_DATA.meta.title;
    const sub = document.querySelector(".header-bar .subtitle");
    if (sub) sub.textContent = GALLERY_DATA.meta.subtitle;
}

function renderCategoryNav() {
    const nav = document.getElementById("categoryNav");
    nav.innerHTML = "";
    const counts = { all: GALLERY_DATA.prompts.length };
    for (const p of GALLERY_DATA.prompts) {
        counts[p.category] = (counts[p.category] || 0) + 1;
    }
    const cats = ["all", ...Object.keys(counts).filter(c => c !== "all").sort()];
    for (const c of cats) {
        const chip = document.createElement("div");
        chip.className = "folder-chip" + (c === activeCategory ? " active" : "");
        chip.innerHTML = `${c} <span class="count">${counts[c]}</span>`;
        chip.onclick = () => { activeCategory = c; renderCategoryNav(); renderGallery(); };
        nav.appendChild(chip);
    }
}

function wireControls() {
    document.getElementById("searchInput").addEventListener("input", e => {
        searchQ = e.target.value.trim().toLowerCase();
        renderGallery();
    });
    document.getElementById("onlyFailedBtn").addEventListener("click", e => {
        onlyFailed = !onlyFailed;
        e.target.classList.toggle("active", onlyFailed);
        renderGallery();
    });
    document.getElementById("resetFilterBtn").addEventListener("click", () => {
        searchQ = "";
        onlyFailed = false;
        activeCategory = "all";
        document.getElementById("searchInput").value = "";
        document.getElementById("onlyFailedBtn").classList.remove("active");
        renderCategoryNav();
        renderGallery();
    });
    document.getElementById("sizeSlider").addEventListener("input", e => {
        document.documentElement.style.setProperty("--thumb-size", e.target.value + "px");
    });
    document.addEventListener("keydown", e => {
        if (!document.getElementById("assetModal").classList.contains("active")) return;
        if (e.key === "Escape") closeModal();
        if (e.key === "ArrowLeft") navModal(-1);
        if (e.key === "ArrowRight") navModal(1);
    });
}

function passesFilter(p) {
    if (activeCategory !== "all" && p.category !== activeCategory) return false;
    if (onlyFailed && !p.rows.some(r => r.status !== "done")) return false;
    if (searchQ) {
        const hay = (p.pid + " " + p.category + " " + p.original_prompt).toLowerCase();
        if (!hay.includes(searchQ)) return false;
    }
    return true;
}

function renderGallery() {
    const root = document.getElementById("gallery");
    root.innerHTML = "";
    modalImages = [];
    const list = GALLERY_DATA.prompts.filter(passesFilter);
    if (list.length === 0) {
        root.innerHTML = `<div style="color:#666;padding:40px;text-align:center;">No matches.</div>`;
        return;
    }
    for (const p of list) {
        root.appendChild(renderCard(p));
    }
}

function renderCard(p) {
    const card = document.createElement("div");
    card.className = "prompt-card";

    const head = document.createElement("div");
    head.className = "card-head";
    head.innerHTML = `
        <span class="pid">#${escapeHtml(p.pid)}</span>
        <span class="cat">${escapeHtml(p.category)}</span>
        <span class="ar">${escapeHtml(p.ar)}</span>
    `;
    card.appendChild(head);

    const orig = document.createElement("div");
    orig.className = "original";
    orig.innerHTML = `<b>Original prompt:</b> ${escapeHtml(p.original_prompt)}`;
    card.appendChild(orig);

    const seeds = document.createElement("div");
    seeds.className = "seeds";
    for (const r of p.rows) {
        seeds.appendChild(renderSeed(p, r));
    }
    card.appendChild(seeds);
    return card;
}

function renderSeed(p, r) {
    const block = document.createElement("div");
    block.className = "seed-block" + (r.status === "done" ? "" : " seed-block failed failed-block");

    if (r.status !== "done") {
        block.innerHTML = `
            <div class="err">
                <div><b>input seed:</b> ${r.input_seed} — <span style="color:#f55;">${escapeHtml(r.status)}</span> <code>${escapeHtml(r.error_code || "")}</code></div>
                <div style="margin-top:6px;color:#caa;">${escapeHtml((r.error_message || "").slice(0, 600))}</div>
            </div>
        `;
        return block;
    }

    const imgSrc = "../images/" + r.image_filename;
    const myIdx = modalImages.length;
    modalImages.push({
        src: imgSrc,
        caption: `#${p.pid} • ${p.category} • input_seed=${r.input_seed} • model_seed=${r.model_seed} • ${r.image_filename}`
    });

    const img = document.createElement("img");
    img.loading = "lazy";
    img.src = imgSrc;
    img.alt = `prompt ${p.pid} seed ${r.model_seed}`;
    img.onclick = () => openModal(myIdx);
    block.appendChild(img);

    const meta = document.createElement("div");
    meta.className = "meta";
    meta.innerHTML = `
        <div class="seeds-line"><b>input_seed:</b> ${r.input_seed} &nbsp; <b>model_seed:</b> ${r.model_seed}</div>
        <details><summary>rewritten_prompt (${(r.rewritten_prompt || "").length} chars)</summary><pre>${escapeHtml(r.rewritten_prompt || "")}</pre></details>
        <details><summary>rewritten_negative_prompt (${(r.rewritten_negative_prompt || "").length} chars)</summary><pre>${escapeHtml(r.rewritten_negative_prompt || "")}</pre></details>
    `;
    block.appendChild(meta);
    return block;
}

function openModal(i) {
    modalIndex = i;
    const modal = document.getElementById("assetModal");
    modal.classList.add("active");
    syncModal();
}

function closeModal() {
    document.getElementById("assetModal").classList.remove("active");
}

function navModal(delta) {
    if (modalImages.length === 0) return;
    modalIndex = (modalIndex + delta + modalImages.length) % modalImages.length;
    syncModal();
}

function syncModal() {
    const it = modalImages[modalIndex];
    document.getElementById("modalImage").src = it.src;
    document.getElementById("modalInfo").textContent = it.caption;
}

function escapeHtml(s) {
    if (s === null || s === undefined) return "";
    return String(s)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}
