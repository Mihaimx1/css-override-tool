(() => {
  "use strict";

  // CONFIG
  const SCOPE = "all"; // "all" | "id"
  const GRID_ID = "Grid_0ecfe177-a75f-4f4f-837d-08de2770620e"; // used if SCOPE === "id"
  const rootSelector = SCOPE === "id" ? `#${CSS.escape(GRID_ID)}` : ".k-grid";
  const styleId = "kendo-evidence-css-min";

  function injectCss() {
    const css = `
      /* Evidence-only local overrides */
      ${rootSelector} { height: auto !important; margin-bottom: 16px !important; }

      /* Main content areas */
      ${rootSelector} .k-grid-content,
      ${rootSelector} .k-grid-content-locked,
      ${rootSelector} .k-virtual-content {
        height: auto !important;
        max-height: none !important;
        overflow: visible !important;
      }

      /* Header wrappers often get extra padding to account for scrollbar */
      ${rootSelector} .k-grid-header { padding-right: 0 !important; }
      ${rootSelector} .k-grid-header-wrap,
      ${rootSelector} .k-auto-scrollable { overflow: visible !important; }

      /* Long text wrapping */
      ${rootSelector} td { overflow-wrap: anywhere; word-break: break-word; }
    `;

    let s = document.getElementById(styleId);
    if (!s) {
      s = document.createElement("style");
      s.id = styleId;
      s.type = "text/css";
      document.head.appendChild(s);
    }
    s.textContent = css;

    // Wipe inline heights once (local only)
    document.querySelectorAll(`
      ${rootSelector},
      ${rootSelector} .k-grid-content,
      ${rootSelector} .k-grid-content-locked,
      ${rootSelector} .k-virtual-content,
      ${rootSelector} .k-grid-header
    `).forEach(el => {
      el.style.height = "auto";
      el.style.maxHeight = "none";
      if (el.classList.contains("k-grid-header")) el.style.paddingRight = "0";
    });
  }

  function expandOnePass() {
    // Expand grouping rows and hierarchy rows (cover anchor/span/svg icon cases)
    const expanders = document.querySelectorAll(`
      ${rootSelector} tr.k-grouping-row[aria-expanded="false"] [class*="k-i-expand"],
      ${rootSelector} tr.k-grouping-row[aria-expanded="false"] [class*="k-i-plus"],
      ${rootSelector} tr.k-master-row td.k-hierarchy-cell [class*="k-i-expand"],
      ${rootSelector} tr.k-master-row td.k-hierarchy-cell [class*="k-i-plus"]
    `);
    expanders.forEach(el => { try { el.click(); } catch (_) {} });
  }

  function gridPresent() {
    return document.querySelector(rootSelector);
  }

  function waitForGrid(timeoutMs = 10000) {
    return new Promise(resolve => {
      if (gridPresent()) return resolve();
      const obs = new MutationObserver(() => {
        if (gridPresent()) {
          obs.disconnect();
          resolve();
        }
      });
      obs.observe(document.documentElement, { childList: true, subtree: true });
      setTimeout(() => { try { obs.disconnect(); } catch(_){} resolve(); }, timeoutMs);
    });
  }

  async function run() {
    await waitForGrid();
    injectCss();
    expandOnePass();
    // Nudge layout
    window.dispatchEvent(new Event("resize"));
    console.log("[Kendo Evidence Helper] Applied once on demand.");
  }

  // Execute immediately when injected by bg.js
  run();
})();