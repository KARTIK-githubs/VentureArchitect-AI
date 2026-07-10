/**
 * VentureArchitect AI — Blueprint Page JavaScript
 * Renders the AI-generated startup blueprint from sessionStorage
 *
 * NOTE: $ is declared in main.js which loads before this file on every page.
 * Do NOT redeclare it here — that causes "Identifier '$' has already been
 * declared" under "use strict" and halts all JS on the blueprint page.
 */

"use strict";

// $ is provided by main.js (loaded first via base.html)

// ── Agent metadata ────────────────────────────────────────────
const SECTION_META = [
    {
        icon: "bi bi-lightbulb-fill",
        color: "#6366f1",
        bg: "rgba(99,102,241,0.12)",
        badge: "Agent 1",
    },
    {
        icon: "bi bi-graph-up-arrow",
        color: "#0ea5e9",
        bg: "rgba(14,165,233,0.12)",
        badge: "Agent 2",
    },
    {
        icon: "bi bi-diagram-3-fill",
        color: "#10b981",
        bg: "rgba(16,185,129,0.12)",
        badge: "Agent 3",
    },
    {
        icon: "bi bi-shield-exclamation",
        color: "#f59e0b",
        bg: "rgba(245,158,11,0.12)",
        badge: "Agent 4",
    },
    {
        icon: "bi bi-megaphone-fill",
        color: "#ec4899",
        bg: "rgba(236,72,153,0.12)",
        badge: "Agent 5",
    },
];

// ── Simple markdown-to-HTML renderer ─────────────────────────
function renderMarkdown(md) {
    if (!md) return "<p><em>No content generated for this section.</em></p>";

    let html = md
        // Tables: convert | separated rows
        .replace(/^\|(.+)\|$/gm, (_, row) => {
            const cells = row.split("|").map(c => c.trim());
            const isHeader = false;
            return `<tr>${cells.map(c => `<td>${c}</td>`).join("")}</tr>`;
        })
        // Wrap consecutive table rows
        .replace(/(<tr>[\s\S]*?<\/tr>\n?)+/g, m => {
            const rows = m.trim().split("\n").filter(r => r.trim() && !r.match(/^[\|\s\-]+$/));
            if (rows.length === 0) return m;
            const headerRow = rows[0];
            const bodyRows = rows.slice(1);
            // Convert first row to <th>
            const header = headerRow.replace(/<td>/g, "<th>").replace(/<\/td>/g, "</th>");
            const body = bodyRows.join("\n");
            return `<div class="table-responsive"><table class="table table-dark table-bordered va-markdown-table"><thead>${header}</thead><tbody>${body}</tbody></table></div>`;
        })
        // Horizontal rule
        .replace(/^---+$/gm, "<hr>")
        // ATX headings
        .replace(/^######\s+(.+)$/gm, "<h6>$1</h6>")
        .replace(/^#####\s+(.+)$/gm, "<h5>$1</h5>")
        .replace(/^####\s+(.+)$/gm, "<h4>$1</h4>")
        .replace(/^###\s+(.+)$/gm, "<h3>$1</h3>")
        .replace(/^##\s+(.+)$/gm, "<h2>$1</h2>")
        .replace(/^#\s+(.+)$/gm, "<h1>$1</h1>")
        // Bold + italic
        .replace(/\*\*\*(.+?)\*\*\*/g, "<strong><em>$1</em></strong>")
        .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
        .replace(/\*(.+?)\*/g, "<em>$1</em>")
        // Inline code
        .replace(/`([^`]+)`/g, "<code>$1</code>")
        // Blockquote
        .replace(/^>\s+(.+)$/gm, "<blockquote>$1</blockquote>")
        // Unordered list items
        .replace(/^[\*\-]\s+(.+)$/gm, "<li>$1</li>")
        // Ordered list items
        .replace(/^\d+\.\s+(.+)$/gm, "<oli>$1</oli>");

    // Wrap consecutive <li> in <ul>
    html = html.replace(/(<li>.*<\/li>\n?)+/gs, m => `<ul>${m}</ul>`);
    // Wrap consecutive <oli> in <ol>
    html = html.replace(/(<oli>.*<\/oli>\n?)+/gs, m => `<ol>${m.replace(/<oli>/g, "<li>").replace(/<\/oli>/g, "</li>")}</ol>`);

    // Paragraphs: wrap non-tag lines
    html = html.split("\n").map(line => {
        const trimmed = line.trim();
        if (!trimmed) return "";
        if (trimmed.match(/^<(h[1-6]|ul|ol|li|blockquote|hr|div|table|thead|tbody|tr|th|td|pre)/)) {
            return trimmed;
        }
        return `<p>${trimmed}</p>`;
    }).join("\n");

    return html;
}

// ── Build a single blueprint section card ────────────────────
function buildSectionCard(section, index) {
    const meta = SECTION_META[index] || SECTION_META[0];
    const contentHtml = renderMarkdown(section.content);
    const sectionId = `section-${index}`;

    const successBadge = section.success
        ? `<span class="va-blueprint-section-badge">✓ Complete</span>`
        : `<span class="va-blueprint-section-badge" style="background:rgba(239,68,68,0.15);color:var(--va-red);border-color:rgba(239,68,68,0.3)">⚠ Error</span>`;

    return `
    <div class="va-blueprint-section va-animate" id="${sectionId}">
      <div class="va-blueprint-section-header" onclick="toggleSection('${sectionId}')">
        <div class="va-blueprint-section-icon" style="background:${meta.bg};color:${meta.color};">
          <i class="${meta.icon}"></i>
        </div>
        <h3 class="va-blueprint-section-title">${escHtml(section.title)}</h3>
        <span class="va-blueprint-section-agent-badge me-2" style="font-size:0.7rem;color:var(--va-text-muted);">
          ${meta.badge}
        </span>
        ${successBadge}
        <i class="bi bi-chevron-down ms-2 va-chevron" style="color:var(--va-text-muted);transition:transform 0.25s;"></i>
      </div>
      <div class="va-blueprint-section-body va-section-body" id="${sectionId}-body">
        ${section.success
            ? `<div class="va-markdown-content">${contentHtml}</div>`
            : `<div class="alert alert-danger"><i class="bi bi-exclamation-triangle me-2"></i>${escHtml(section.error || "Agent failed to generate content.")}</div>`
        }
      </div>
    </div>`;
}

// ── Toggle section collapse ────────────────────────────────────
window.toggleSection = function (sectionId) {
    const body = document.getElementById(`${sectionId}-body`);
    const header = document.getElementById(sectionId)?.querySelector(".va-blueprint-section-header");
    const chevron = header?.querySelector(".va-chevron");
    if (!body) return;
    const isOpen = !body.classList.contains("d-none");
    if (isOpen) {
        body.classList.add("d-none");
        if (chevron) chevron.style.transform = "rotate(-90deg)";
    } else {
        body.classList.remove("d-none");
        if (chevron) chevron.style.transform = "rotate(0deg)";
    }
};

// ── Escape HTML ───────────────────────────────────────────────
function escHtml(str) {
    const d = document.createElement("div");
    d.appendChild(document.createTextNode(str || ""));
    return d.innerHTML;
}

// ── Build section navigation pills ────────────────────────────
function buildSectionNav(sections) {
    const nav = $("#sectionNav .d-flex");
    if (!nav) return;
    sections.forEach((section, i) => {
        const pill = document.createElement("button");
        pill.className = "va-nav-pill";
        pill.textContent = section.title;
        pill.addEventListener("click", () => {
            const target = document.getElementById(`section-${i}`);
            if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
        });
        nav.appendChild(pill);
    });
}

// ── Main render function ───────────────────────────────────────
function renderBlueprint(payload) {
    const { blueprint, idea, elapsed, generatedAt } = payload;
    const sections = blueprint?.sections || [];

    if (sections.length === 0) {
        showError("Blueprint contains no sections. Please try generating again.");
        return;
    }

    // Update title
    const title = $("#blueprintTitle");
    const subtitle = $("#blueprintSubtitle");
    if (title) {
        const shortIdea = idea.length > 80 ? idea.substring(0, 80) + "..." : idea;
        title.textContent = shortIdea;
    }
    if (subtitle) {
        const genDate = generatedAt ? new Date(generatedAt).toLocaleString() : "Just now";
        subtitle.textContent = `Generated ${genDate} · ${sections.length} sections · Powered by IBM Granite AI`;
    }

    // Update stats
    const sectionCountEl = $("#sectionCount");
    const genTimeEl = $("#generationTime");
    const successCountEl = $("#successCount");
    if (sectionCountEl) sectionCountEl.textContent = sections.length;
    if (genTimeEl) genTimeEl.textContent = elapsed ? `${elapsed}s` : "~90s";
    if (successCountEl) {
        const successCount = sections.filter(s => s.success).length;
        successCountEl.textContent = `${successCount}/${sections.length}`;
        if (successCount < sections.length) {
            successCountEl.style.color = "var(--va-amber)";
        }
    }

    // Build section navigation
    buildSectionNav(sections);

    // Render all sections
    const container = $("#blueprintSections");
    if (container) {
        container.innerHTML = sections.map((s, i) => buildSectionCard(s, i)).join("");
    }

    // Show content, hide loading
    $("#blueprint-loading")?.classList.add("d-none");
    $("#blueprint-content")?.classList.remove("d-none");

    // Trigger animations
    requestAnimationFrame(() => {
        document.querySelectorAll(".va-animate").forEach((el, i) => {
            el.style.transitionDelay = `${i * 0.05}s`;
            setTimeout(() => el.classList.add("visible"), i * 50);
        });
    });

    // Scroll active section nav pill
    initActiveSectionTracking();
}

// ── Track active section on scroll ────────────────────────────
function initActiveSectionTracking() {
    const pills = document.querySelectorAll(".va-nav-pill");
    const sections = document.querySelectorAll(".va-blueprint-section");
    if (!pills.length || !sections.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const idx = [...sections].indexOf(entry.target);
                pills.forEach((p, i) => p.classList.toggle("active", i === idx));
            }
        });
    }, { threshold: 0.3 });

    sections.forEach(s => observer.observe(s));
}

// ── Copy blueprint ─────────────────────────────────────────────
function initCopyButton() {
    const btn = $("#copyBtn");
    if (!btn) return;
    btn.addEventListener("click", () => {
        const stored = sessionStorage.getItem("va_blueprint");
        if (!stored) return;
        const { blueprint } = JSON.parse(stored);
        const text = blueprint?.sections?.map(s =>
            `# ${s.title}\n\n${s.content}`
        ).join("\n\n---\n\n") || "";

        navigator.clipboard.writeText(text).then(() => {
            btn.innerHTML = '<i class="bi bi-check-lg me-1"></i>Copied!';
            btn.style.borderColor = "var(--va-green)";
            btn.style.color = "var(--va-green)";
            setTimeout(() => {
                btn.innerHTML = '<i class="bi bi-clipboard me-1"></i>Copy';
                btn.style.borderColor = "";
                btn.style.color = "";
            }, 2000);
        }).catch(() => {
            alert("Could not copy to clipboard. Please manually select and copy the content.");
        });
    });
}

// ── New Blueprint button ───────────────────────────────────────
function initNewBlueprintButton() {
    const btn = $("#newBlueprintBtn");
    if (!btn) return;
    btn.addEventListener("click", () => {
        sessionStorage.removeItem("va_blueprint");
        window.location.href = "/#generate";
    });
}

// ── Error display ──────────────────────────────────────────────
function showError(message) {
    $("#blueprint-loading")?.classList.add("d-none");
    $("#blueprint-content")?.classList.add("d-none");
    const errEl = $("#blueprint-error");
    if (errEl) {
        errEl.classList.remove("d-none");
        const msgEl = $("#errorMessage");
        if (msgEl) msgEl.textContent = message;
    }
}

// ── Init ───────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
    initCopyButton();
    initNewBlueprintButton();

    const stored = sessionStorage.getItem("va_blueprint");
    if (!stored) {
        showError("No blueprint found. Please go back and generate a new blueprint.");
        return;
    }

    try {
        const payload = JSON.parse(stored);
        if (!payload?.blueprint) {
            showError("Invalid blueprint data. Please regenerate.");
            return;
        }
        renderBlueprint(payload);
    } catch (e) {
        console.error("Blueprint parse error:", e);
        showError("Could not load blueprint. Please regenerate.");
    }
});
