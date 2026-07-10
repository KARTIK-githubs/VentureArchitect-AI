/**
 * VentureArchitect AI — Main JavaScript
 * Handles: Landing page, idea input, API call, progress tracker
 */

"use strict";

// ── Utilities ───────────────────────────────────────────────
const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];
const el = (tag, attrs = {}, ...children) => {
    const e = document.createElement(tag);
    Object.entries(attrs).forEach(([k, v]) => {
        if (k === "className") e.className = v;
        else if (k === "innerHTML") e.innerHTML = v;
        else e.setAttribute(k, v);
    });
    children.forEach(c => e.appendChild(typeof c === "string" ? document.createTextNode(c) : c));
    return e;
};

// ── Constants ────────────────────────────────────────────────
const AGENT_NAMES = [
    "Idea Analysis Agent",
    "Market Research Agent",
    "Business Strategy Agent",
    "Risk Analysis Agent",
    "Investor Pitch Agent",
];

const AGENT_MESSAGES = [
    "🔍 Analyzing your startup concept...",
    "📊 Researching markets and competitors...",
    "💼 Designing your business model...",
    "⚠️ Identifying risks and opportunities...",
    "🎤 Crafting your investor pitch...",
];

// ── Char Counter ─────────────────────────────────────────────
function initCharCounter() {
    const textarea = $("#startupIdea");
    const counter = $("#charCount");
    if (!textarea || !counter) return;

    textarea.addEventListener("input", () => {
        const len = textarea.value.length;
        counter.textContent = `${len} / 2000`;
        counter.style.color = len > 1800 ? "var(--va-amber)" : len > 1950 ? "var(--va-red)" : "";
    });
}

// ── Example Prompts ──────────────────────────────────────────
function initExamplePrompts() {
    $$(".va-example-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const textarea = $("#startupIdea");
            if (!textarea) return;
            textarea.value = btn.dataset.idea || "";
            textarea.dispatchEvent(new Event("input"));
            textarea.scrollIntoView({ behavior: "smooth", block: "center" });
            textarea.focus();
        });
    });
}

// ── Progress Tracker ─────────────────────────────────────────
function setStepStatus(index, status) {
    const step = $(`#step-${index}`);
    if (!step) return;
    step.className = `va-progress-step${status ? ` is-${status}` : ""}`;
    const statusEl = step.querySelector(".va-step-status");
    const iconEl = step.querySelector(".va-step-dot i");

    const statusMap = {
        running: { text: "⚡ Running...", icon: "bi bi-arrow-repeat" },
        done:    { text: "✅ Complete",  icon: "bi bi-check-lg" },
        error:   { text: "❌ Failed",    icon: "bi bi-exclamation-lg" },
        waiting: { text: "Waiting...",   icon: getDefaultIcon(index) },
    };
    const s = statusMap[status] || statusMap.waiting;
    if (statusEl) statusEl.textContent = s.text;
    if (iconEl) iconEl.className = s.icon;
}

function getDefaultIcon(i) {
    const icons = [
        "bi bi-lightbulb-fill",
        "bi bi-graph-up-arrow",
        "bi bi-diagram-3-fill",
        "bi bi-shield-exclamation",
        "bi bi-megaphone-fill",
    ];
    return icons[i] || "bi bi-cpu-fill";
}

function updateProgress(step, total = 5) {
    const bar = $("#overallProgress");
    if (bar) bar.style.width = `${Math.round(((step + 1) / total) * 100)}%`;
}

// ── Simulated agent progress during API wait ─────────────────
let progressSimInterval = null;
let currentSimStep = 0;

function startProgressSimulation() {
    currentSimStep = 0;
    // Mark step 0 as running immediately
    updateAgentUI(0, "running");

    progressSimInterval = setInterval(() => {
        // Advance sim step roughly every 18 seconds
        // (5 agents × ~18s = 90s total estimate)
    }, 18000);
}

function updateAgentUI(index, status) {
    const label = $("#currentAgentLabel");
    if (label) {
        if (status === "running") {
            label.textContent = AGENT_MESSAGES[index] || "Processing...";
        }
    }
    setStepStatus(index, status);
    if (status === "running") updateProgress(index);
}

function stopProgressSimulation() {
    if (progressSimInterval) {
        clearInterval(progressSimInterval);
        progressSimInterval = null;
    }
}

// Advance simulated step forward every ~15 seconds
function advanceSimStep() {
    if (currentSimStep < AGENT_NAMES.length - 1) {
        setStepStatus(currentSimStep, "done");
        currentSimStep++;
        updateAgentUI(currentSimStep, "running");
    }
}

// ── Main Generate Flow ───────────────────────────────────────
function initGenerateFlow() {
    const btn = $("#generateBtn");
    if (!btn) return;

    btn.addEventListener("click", async () => {
        const textarea = $("#startupIdea");
        const idea = textarea?.value?.trim() || "";

        if (idea.length < 10) {
            showToast("Please describe your startup idea in more detail (at least 10 characters).", "warning");
            textarea?.focus();
            return;
        }

        // Switch to loading phase
        showLoadingPhase();
        startProgressSimulation();

        // Start timer for sim advancement
        const simTimers = [];
        AGENT_NAMES.forEach((_, i) => {
            if (i === 0) return; // already set
            simTimers.push(setTimeout(() => advanceSimStep(), i * 16000));
        });

        const startTime = Date.now();

        // Abort after 5 minutes (5 agents × ~60s max each)
        const controller = new AbortController();
        const fetchTimeout = setTimeout(() => controller.abort(), 300000);

        try {
            const response = await fetch("/api/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ startup_idea: idea }),
                signal: controller.signal,
            });

            clearTimeout(fetchTimeout);
            simTimers.forEach(t => clearTimeout(t));
            stopProgressSimulation();

            const data = await response.json();
            const elapsed = ((Date.now() - startTime) / 1000).toFixed(0);

            if (!response.ok || !data.success) {
                showErrorPhase(data.error || "Generation failed. Please try again.");
                return;
            }

            // Mark all steps done
            AGENT_NAMES.forEach((_, i) => setStepStatus(i, "done"));
            updateProgress(4);
            $("#currentAgentLabel") && ($("#currentAgentLabel").textContent = "✅ Blueprint complete!");

            // Store result and redirect
            const blueprintPayload = {
                blueprint: data.blueprint,
                idea: idea,
                elapsed: elapsed,
                generatedAt: new Date().toISOString(),
            };
            sessionStorage.setItem("va_blueprint", JSON.stringify(blueprintPayload));

            // Short delay so user sees the completed state
            setTimeout(() => {
                window.location.href = "/blueprint";
            }, 1200);

        } catch (err) {
            clearTimeout(fetchTimeout);
            simTimers.forEach(t => clearTimeout(t));
            stopProgressSimulation();
            console.error("Generate error:", err);
            if (err.name === "AbortError") {
                showErrorPhase("Request timed out after 5 minutes. The AI models may be overloaded — please try again.");
            } else {
                showErrorPhase(err.message || "Network error. Please check your connection and try again.");
            }
        }
    });
}

function showLoadingPhase() {
    const inputPhase = $("#input-phase");
    const loadingPhase = $("#loading-phase");
    if (inputPhase) inputPhase.classList.add("d-none");
    if (loadingPhase) loadingPhase.classList.remove("d-none");
}

function showErrorPhase(message) {
    const loadingPhase = $("#loading-phase");
    const inputPhase = $("#input-phase");
    if (loadingPhase) loadingPhase.classList.add("d-none");
    if (inputPhase) inputPhase.classList.remove("d-none");
    showToast(message, "error");
    AGENT_NAMES.forEach((_, i) => setStepStatus(i, "waiting"));
}

// ── Toast Notifications ──────────────────────────────────────
function showToast(message, type = "info") {
    const colors = {
        info:    "var(--va-accent)",
        success: "var(--va-green)",
        warning: "var(--va-amber)",
        error:   "var(--va-red)",
    };
    const icons = {
        info:    "bi-info-circle-fill",
        success: "bi-check-circle-fill",
        warning: "bi-exclamation-triangle-fill",
        error:   "bi-x-circle-fill",
    };

    const toast = el("div", {
        className: "va-toast",
        innerHTML: `<i class="bi ${icons[type] || icons.info} me-2" style="color:${colors[type] || colors.info}"></i>${message}`,
    });

    const style = toast.style;
    style.position = "fixed";
    style.bottom = "1.5rem";
    style.right = "1.5rem";
    style.zIndex = "9999";
    style.background = "var(--va-surface-2)";
    style.border = `1px solid ${colors[type] || colors.info}33`;
    style.borderRadius = "var(--va-radius-sm)";
    style.padding = "0.85rem 1.25rem";
    style.fontSize = "0.875rem";
    style.maxWidth = "400px";
    style.boxShadow = "0 8px 24px rgba(0,0,0,0.4)";
    style.transition = "all 0.3s ease";
    style.opacity = "0";
    style.transform = "translateY(10px)";
    style.display = "flex";
    style.alignItems = "center";

    document.body.appendChild(toast);
    requestAnimationFrame(() => {
        toast.style.opacity = "1";
        toast.style.transform = "translateY(0)";
    });

    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateY(10px)";
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// ── Scroll animations ────────────────────────────────────────
function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
            }
        });
    }, { threshold: 0.1 });

    $$(".va-animate").forEach(el => observer.observe(el));

    // Add va-animate to agent cards and feature cards
    $$(".va-agent-card, .va-feature-card, .va-step-card").forEach((card, i) => {
        card.classList.add("va-animate");
        card.style.transitionDelay = `${i * 0.07}s`;
        observer.observe(card);
    });
}

// ── Init ─────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
    initCharCounter();
    initExamplePrompts();
    initGenerateFlow();
    initScrollAnimations();

    // Smooth scroll for anchor links
    $$('a[href^="#"]').forEach(a => {
        a.addEventListener("click", e => {
            const target = $(a.getAttribute("href"));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: "smooth" });
            }
        });
    });
});
