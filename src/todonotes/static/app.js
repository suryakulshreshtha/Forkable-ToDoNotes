/* app.js — progressive enhancement. Every feature here is optional:
   with JavaScript switched off, the plain HTML forms still work.

   1. Theme toggle      remembers light/dark in localStorage
   2. Autosave          PATCH /api/notes/<id> while you type (debounced)
   3. Checklist toggle  PATCH /api/items/<id> without a full page reload
   4. Shortcuts         "/" focuses search, Ctrl/Cmd+S saves the note
*/
(function () {
  "use strict";

  /* ---- 1. Theme toggle ------------------------------------------------- */
  var THEME_KEY = "todonotes-theme";

  function currentTheme() {
    var explicit = document.documentElement.dataset.theme;
    if (explicit) return explicit;
    return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
  }

  function setTheme(theme) {
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem(THEME_KEY, theme); } catch (e) { /* storage blocked */ }
  }

  document.addEventListener("click", function (event) {
    if (event.target.closest("[data-theme-toggle]")) {
      setTheme(currentTheme() === "dark" ? "light" : "dark");
    }
  });

  /* ---- Small fetch helper ------------------------------------------------ */
  function sendJson(method, url, data) {
    return fetch(url, {
      method: method,
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(data),
    }).then(function (response) {
      if (!response.ok) throw new Error("HTTP " + response.status);
      return response.json();
    });
  }

  /* ---- 2. Autosave --------------------------------------------------------- */
  var form = document.getElementById("note-form");
  var noteId = form && form.dataset.noteId;
  var statusEl = document.querySelector(".save-status");
  var timer = null;

  function setStatus(text) { if (statusEl) statusEl.textContent = text; }

  function autosave() {
    var payload = {
      title: form.elements.title.value,
      body: form.elements.body.value,
      pinned: form.elements.pinned.checked,
    };
    setStatus("Saving…");
    sendJson("PATCH", "/api/notes/" + noteId, payload)
      .then(function () {
        var time = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
        setStatus("Saved ✓ " + time);
      })
      .catch(function () { setStatus("Not saved — use the Save button"); });
  }

  if (form && noteId) {
    form.addEventListener("input", function () {
      setStatus("Editing…");
      clearTimeout(timer);
      timer = setTimeout(autosave, 600);
    });
  }

  /* ---- 3. Checklist toggle without reload ------------------------------- */
  document.addEventListener("submit", function (event) {
    var toggle = event.target.closest(".toggle-form");
    if (!toggle) return;
    event.preventDefault();
    var item = toggle.closest(".item");
    var button = toggle.querySelector(".check");
    var nextDone = button.getAttribute("aria-checked") !== "true";
    sendJson("PATCH", "/api/items/" + item.dataset.itemId, { done: nextDone })
      .then(function (saved) {
        button.setAttribute("aria-checked", saved.done ? "true" : "false");
        button.firstElementChild.textContent = saved.done ? "✔" : "";
        item.classList.toggle("done", saved.done);
        var all = document.querySelectorAll(".items .item").length;
        var done = document.querySelectorAll(".items .item.done").length;
        var counter = document.querySelector("#checklist-heading .count");
        if (counter) counter.textContent = done + "/" + all;
      })
      .catch(function () { toggle.submit(); /* fall back to the plain form */ });
  });

  /* ---- 4. Keyboard shortcuts --------------------------------------------- */
  document.addEventListener("keydown", function (event) {
    var typing = /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName);
    var search = document.getElementById("q");
    if (event.key === "/" && !typing && search) {
      event.preventDefault();
      search.focus();
      search.select();
    }
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "s" && form) {
      event.preventDefault();
      form.requestSubmit();
    }
  });
})();
