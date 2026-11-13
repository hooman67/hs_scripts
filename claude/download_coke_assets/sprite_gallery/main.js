// Gallery rendering logic
// GALLERY_DATA is loaded from data.js

let currentFolder = "all";
let currentSearch = "";
let viewableItems = []; // flat list of currently displayed items (for lightbox nav)
let lbIndex = 0;

function formatSize(bytes) {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + " KB";
    if (bytes < 1073741824) return (bytes / 1048576).toFixed(1) + " MB";
    return (bytes / 1073741824).toFixed(2) + " GB";
}

function getFolderLabel(folder) {
    // Show last 2 segments for readability
    const parts = folder.split("/").filter(Boolean);
    if (parts.length <= 2) return parts.join("/");
    return parts.slice(-2).join("/");
}

function onAuthReady() {
    renderFolderNav();
    renderGallery();
    setupControls();
}

function setupControls() {
    document.getElementById("searchInput").addEventListener("input", (e) => {
        currentSearch = e.target.value.toLowerCase();
        renderGallery();
    });

    document.getElementById("sizeSlider").addEventListener("input", (e) => {
        document.getElementById("gallery").style.setProperty("--thumb-size", e.target.value + "px");
    });
}

function renderFolderNav() {
    const nav = document.getElementById("folderNav");
    const folders = Object.keys(GALLERY_DATA).sort();
    const totalCount = Object.values(GALLERY_DATA).flat().length;

    let html = `<div class="folder-chip active" onclick="setFolder('all')">All<span class="count">${totalCount}</span></div>`;
    folders.forEach(f => {
        const count = GALLERY_DATA[f].length;
        const label = getFolderLabel(f);
        html += `<div class="folder-chip" onclick="setFolder('${f.replace(/'/g, "\\'")}')" title="${f}">${label}<span class="count">${count}</span></div>`;
    });
    nav.innerHTML = html;
}

function setFolder(folder) {
    currentFolder = folder;
    // Update active chip
    document.querySelectorAll(".folder-chip").forEach(chip => {
        const isAll = folder === "all" && chip.textContent.startsWith("All");
        const isMatch = chip.getAttribute("onclick")?.includes(`'${folder}'`);
        chip.classList.toggle("active", isAll || isMatch);
    });
    renderGallery();
}

function renderGallery() {
    const gallery = document.getElementById("gallery");
    viewableItems = [];
    let html = "";

    const folders = currentFolder === "all" ? Object.keys(GALLERY_DATA).sort() : [currentFolder];

    folders.forEach(folder => {
        const items = GALLERY_DATA[folder] || [];
        const filtered = items.filter(item => {
            if (!currentSearch) return true;
            return item.n.toLowerCase().includes(currentSearch) || folder.toLowerCase().includes(currentSearch);
        });

        if (filtered.length === 0) return;

        // Section header
        html += `<div class="section-header"><h2>${getFolderLabel(folder)}</h2><div class="folder-path">${folder} &mdash; ${filtered.length} assets</div></div>`;

        filtered.forEach(item => {
            const idx = viewableItems.length;
            viewableItems.push(item);

            if (item.t) {
                // Non-viewable file (TIF, PSD, etc.)
                const ext = item.t.toUpperCase();
                html += `<div class="card tif-card" title="${item.n}">
                    <div class="thumb-placeholder"><span>${ext}</span><span>${formatSize(item.s)}</span></div>
                    <div class="info"><div class="fname" title="${item.n}">${item.n}</div><div class="fsize">${formatSize(item.s)}</div></div>
                </div>`;
            } else {
                html += `<div class="card" onclick="openModal(${idx})" title="${item.n}">
                    <img class="thumb" loading="lazy" src="../${item.p}" alt="${item.n}" onerror="this.style.display='none';this.parentElement.querySelector('.info').insertAdjacentHTML('afterbegin','<div style=\\'padding:20px;color:#555;font-size:11px\\'>Load failed</div>')">
                    <div class="info"><div class="fname" title="${item.n}">${item.n}</div><div class="fsize">${formatSize(item.s)}</div></div>
                </div>`;
            }
        });
    });

    if (!html) {
        html = '<div style="grid-column:1/-1;text-align:center;color:#555;padding:60px;">No matching assets found.</div>';
    }

    gallery.innerHTML = html;
}

// Modal / Lightbox
function openModal(idx) {
    lbIndex = idx;
    const item = viewableItems[idx];
    if (item.t) return; // Skip TIF
    const modal = document.getElementById("assetModal");
    document.getElementById("modalImage").src = "../" + item.p;
    document.getElementById("modalInfo").textContent = item.n + " \u2022 " + formatSize(item.s);
    modal.classList.add("active");
}

function closeModal() {
    document.getElementById("assetModal").classList.remove("active");
    document.getElementById("modalImage").src = "";
}

function navModal(dir) {
    // Find next non-TIF item
    let next = lbIndex;
    for (let i = 0; i < viewableItems.length; i++) {
        next = (next + dir + viewableItems.length) % viewableItems.length;
        if (!viewableItems[next].t) break;
    }
    openModal(next);
}

document.addEventListener("keydown", (e) => {
    const modal = document.getElementById("assetModal");
    if (!modal.classList.contains("active")) return;
    if (e.key === "Escape") closeModal();
    if (e.key === "ArrowLeft") navModal(-1);
    if (e.key === "ArrowRight") navModal(1);
});
