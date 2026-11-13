"use strict";
function onAuthReady() {
    document.getElementById("loading").hidden = true;
    document.getElementById("content").classList.remove("hidden");
    for (const image of document.querySelectorAll("img[data-src]")) image.src = image.dataset.src;
}
document.addEventListener("DOMContentLoaded", () => {
    initializeIMS();
    const key = "hp-astra-review:" + document.body.dataset.protocol + ":" + location.pathname;
    const inputs = [...document.querySelectorAll("textarea[data-case]")];
    const notice = document.getElementById("feedback-status");
    let writable = true;
    let saved = {};
    try {
        const previous = localStorage.getItem(key);
        if (previous !== null) {
            saved = JSON.parse(previous);
            if (!saved || typeof saved !== "object" || Array.isArray(saved)) throw new Error("Invalid saved comments");
        }
    } catch (error) {
        writable = false;
        notice.textContent = "Saved comments could not be loaded. Existing storage will not be overwritten. Export new comments before leaving.";
        console.error("Review comment load failed", error);
    }
    for (const input of inputs) {
        const existing = saved[input.dataset.case];
        if (typeof existing === "string") input.value = existing;
        input.addEventListener("input", () => {
            if (!writable) return;
            try {
                localStorage.setItem(key, JSON.stringify(Object.fromEntries(inputs.map(item => [item.dataset.case, item.value]))));
                notice.textContent = "Comments saved in this browser only. Export the JSON to share them.";
            } catch (error) {
                writable = false;
                notice.textContent = "Browser storage failed. Export comments before leaving; no server copy exists.";
                console.error("Review comment save failed", error);
            }
        });
    }
    document.getElementById("export-feedback").addEventListener("click", () => {
        const content = {
            protocol_sha256: document.body.dataset.protocol,
            report: location.href,
            exported_utc: new Date().toISOString(),
            comments: inputs.filter(item => item.value.trim()).map(item => ({
                case_id: item.dataset.case, image_sha256: item.dataset.sha,
                image: new URL(item.dataset.image, location.href).href, comment: item.value.trim()
            }))
        };
        const url = URL.createObjectURL(new Blob([JSON.stringify(content, null, 2)], {type: "application/json"}));
        const anchor = Object.assign(document.createElement("a"), {href: url, download: "hp_astra_judge_feedback.json"});
        anchor.click();
        setTimeout(() => URL.revokeObjectURL(url), 1000);
    });
});
