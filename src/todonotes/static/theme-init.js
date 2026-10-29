/* Apply the saved theme before the first paint (avoids a flash of the wrong theme).
 *
 * A separate file, loaded WITHOUT defer/async, because the page's Content-Security-Policy
 * allows scripts only from this app itself: no inline <script> blocks.
 */
try {
  var saved = localStorage.getItem("todonotes-theme");
  if (saved === "light" || saved === "dark") document.documentElement.dataset.theme = saved;
} catch (e) { /* private mode or blocked storage: follow the OS setting */ }
