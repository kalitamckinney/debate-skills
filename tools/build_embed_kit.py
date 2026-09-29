"""Build the embed kit page: one Copy button per Google Sites embed snippet."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "google-sites"
manifest = json.loads((OUT / "manifest.json").read_text())
for m in manifest:
    m["code"] = (OUT / m["file"]).read_text()
data = json.dumps(manifest).replace("</", "<\\/")

page = r'''<title>Make Your Case Embed Kit</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=Atkinson+Hyperlegible+Mono:wght@400;600&display=swap">
<style>
/* Layout: one reading column; setup steps first, then a checklist of paste-ready sections grouped by page. */
:root {
  --bg: #fbfaf6; --panel: #ffffff; --ink: #1b2430; --muted: #505a66; --line: #c9ced6;
  --accent: #0b4f8a; --accent-ink: #ffffff; --done: #1f6b3a; --soft: #eef3f8;
  --font-body: "Atkinson Hyperlegible", system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-mono: "Atkinson Hyperlegible Mono", ui-monospace, "SFMono-Regular", Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #11161c; --panel: #19212a; --ink: #eef1f5; --muted: #b3bcc7; --line: #3a4553;
  --accent: #8cc4ff; --accent-ink: #0b1a2a; --done: #8fe0a8; --soft: #1f2a36; color-scheme: dark; } }
:root[data-theme="dark"] {
  --bg: #11161c; --panel: #19212a; --ink: #eef1f5; --muted: #b3bcc7; --line: #3a4553;
  --accent: #8cc4ff; --accent-ink: #0b1a2a; --done: #8fe0a8; --soft: #1f2a36; color-scheme: dark; }
* { box-sizing: border-box; }
body { background: var(--bg); color: var(--ink); font: 17px/1.6 var(--font-body); padding-inline: 16px; padding-block: 24px 64px; }
.wrap { max-width: 46rem; margin: 0 auto; display: grid; gap: 28px; }
h1 { font-size: 2rem; line-height: 1.15; margin: 0; text-wrap: balance; }
h2 { font-size: 1.3rem; margin: 0 0 8px; text-wrap: balance; }
p { margin: 0; }
.muted { color: var(--muted); }
.step { display: grid; gap: 12px; }
.eyebrow { font: 600 .8rem/1 var(--font-mono); letter-spacing: .08em; text-transform: uppercase; color: var(--accent); }
label { font-weight: 700; }
input[type=url] { width: 100%; font: 1rem var(--font-mono); padding: 10px 12px; border: 2px solid var(--line); border-radius: 8px; background: var(--panel); color: var(--ink); }
input[type=url]:focus-visible { outline: 3px solid var(--accent); outline-offset: 1px; border-color: var(--accent); }
.status { font-size: .95rem; }
.status.ok { color: var(--done); }
ol.how { margin: 0; padding-left: 1.3rem; display: grid; gap: 6px; }
code, .mono { font-family: var(--font-mono); font-size: .92em; }
.table-wrap { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: .95rem; }
th, td { border-bottom: 1px solid var(--line); padding: 8px 10px 8px 0; text-align: left; vertical-align: top; }
th { color: var(--muted); font-weight: 700; }
.page { background: var(--panel); border: 1px solid var(--line); border-radius: 12px; padding: 16px; display: grid; gap: 10px; }
.page h3 { margin: 0; font-size: 1.15rem; display: flex; flex-wrap: wrap; gap: 4px 12px; align-items: baseline; }
.page h3 .mono { font-weight: 400; color: var(--muted); font-size: .85rem; }
.rows { list-style: none; margin: 0; padding: 0; display: grid; gap: 8px; }
.row { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 14px; padding: 10px 12px; border-radius: 8px; background: var(--soft); }
.row .what { flex: 1 1 14rem; min-width: 0; }
.row .what strong { display: block; }
.row .meta { font: .85rem var(--font-mono); color: var(--muted); font-variant-numeric: tabular-nums; }
.row.copied { box-shadow: inset 4px 0 0 var(--done); }
button.copy { font: 700 .95rem var(--font-body); padding: 8px 16px; border-radius: 8px; border: 2px solid var(--accent); background: var(--accent); color: var(--accent-ink); cursor: pointer; min-width: 7.5rem; }
button.copy:hover { filter: brightness(1.08); }
button.copy:focus-visible { outline: 3px solid var(--ink); outline-offset: 2px; }
.row.copied button.copy { background: transparent; color: var(--done); border-color: var(--done); }
textarea.fallback { width: 100%; height: 6rem; font: .8rem var(--font-mono); }
.note { border-left: 4px solid var(--accent); padding: 4px 0 4px 12px; }
@media (prefers-reduced-motion: no-preference) { .row { transition: box-shadow .2s; } }
</style>

<div class="wrap">
  <header class="step">
    <p class="eyebrow">UDL-Make Your Case · Google Sites</p>
    <h1>Make Your Case Embed Kit</h1>
    <p class="muted">Copy each section of your lesson and paste it into Google Sites. Styles and images are already packed inside each block, so there is nothing else to upload.</p>
  </header>

  <section class="step" aria-labelledby="s1">
    <p class="eyebrow">Step 1</p>
    <h2 id="s1">Create the pages in Google Sites</h2>
    <p>In your UDL copy of the site, open <strong>Pages</strong> in the right panel and add these pages. Use these exact names so the links between pages work.</p>
    <div class="table-wrap"><table>
      <thead><tr><th scope="col">Page name</th><th scope="col">Web address ends in</th></tr></thead>
      <tbody id="pagenames"></tbody>
    </table></div>
    <p class="muted">Then click <strong>Publish</strong> once (the pages can be empty) so your site gets its web address.</p>
  </section>

  <section class="step" aria-labelledby="s2">
    <p class="eyebrow">Step 2</p>
    <h2 id="s2">Enter your site's web address</h2>
    <label for="site">Published site address</label>
    <input type="url" id="site" placeholder="https://sites.google.com/view/udl-make-your-case" autocomplete="off" spellcheck="false">
    <p class="status" id="sitestatus" aria-live="polite"></p>
  </section>

  <section class="step" aria-labelledby="s3">
    <p class="eyebrow">Step 3</p>
    <h2 id="s3">Paste each section</h2>
    <ol class="how">
      <li>Click <strong>Copy</strong> next to a section below.</li>
      <li>In Google Sites, open that page and choose <strong>Insert › Embed › Embed code</strong>.</li>
      <li>Paste, click <strong>Next</strong>, then <strong>Insert</strong>.</li>
      <li>Drag the box's bottom edge down to about the suggested height, so there's no scroll bar inside it. Stretch it to full width, too.</li>
      <li>Paste the next section below it, in order.</li>
    </ol>
    <p class="note">On the <strong>Learn</strong> page, add your audio recording with <strong>Insert › Drive</strong> right after section 1.</p>
  </section>

  <div id="pages" class="step" aria-label="Sections to copy"></div>

  <section class="step" aria-labelledby="s4">
    <p class="eyebrow">Step 4</p>
    <h2 id="s4">Check and publish</h2>
    <ol class="how">
      <li>Click <strong>Preview</strong> (the screen icon) and check each page on the desktop and phone views.</li>
      <li>Click a few links between pages. If one doesn't open, check that the page name matches Step 1.</li>
      <li>Click <strong>Publish</strong>, set <strong>Who can view my site</strong> to <strong>Anyone</strong>, and open the link in an incognito window.</li>
    </ol>
    <p class="muted">Each section sits in its own box, so edit text by changing the lesson and copying the section again, not inside Google Sites.</p>
  </section>
</div>

<script type="application/json" id="data">__DATA__</script>
<script>
(function () {
  var sections = JSON.parse(document.getElementById('data').textContent);
  var siteInput = document.getElementById('site');
  var statusEl = document.getElementById('sitestatus');
  var KEY_SITE = 'embedkit.site', KEY_DONE = 'embedkit.done';
  function load(k, d) { try { var v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } }
  function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  var done = load(KEY_DONE, {});

  // Page-name table
  var seen = {}, tbody = document.getElementById('pagenames');
  sections.forEach(function (s) {
    if (seen[s.slug]) return; seen[s.slug] = 1;
    var tr = document.createElement('tr');
    tr.innerHTML = '<td>' + s.name + '</td><td class="mono">/' + s.slug + '</td>';
    tbody.appendChild(tr);
  });

  function siteBase() {
    var v = siteInput.value.trim().replace(/\/+$/, '');
    return /^https:\/\/sites\.google\.com\/.+/.test(v) ? v : '';
  }
  function showStatus() {
    var raw = siteInput.value.trim(), base = siteBase();
    if (!raw) { statusEl.className = 'status'; statusEl.textContent = 'No address yet. You can still copy; links to other pages will be plain text until you add it.'; }
    else if (!base) { statusEl.className = 'status'; statusEl.textContent = 'That doesn’t look like a Google Sites address. It should start with https://sites.google.com/'; }
    else { statusEl.className = 'status ok'; statusEl.textContent = 'Links will point to ' + base + '/…'; }
  }
  siteInput.value = load(KEY_SITE, '');
  siteInput.addEventListener('input', function () { save(KEY_SITE, siteInput.value.trim()); showStatus(); });
  showStatus();

  function codeFor(s) {
    var base = siteBase();
    if (base) return s.code.split('{{SITE}}').join(base);
    return s.code.replace(/<a href="\{\{SITE\}\}[^"]*" target="_top">([\s\S]*?)<\/a>/g, '$1');
  }

  // Sections grouped by page
  var host = document.getElementById('pages'), groups = {};
  sections.forEach(function (s) {
    if (!groups[s.slug]) {
      var card = document.createElement('section');
      card.className = 'page';
      card.innerHTML = '<h3>' + s.name + ' <span class="mono">/' + s.slug + '</span></h3><ul class="rows"></ul>';
      host.appendChild(card);
      groups[s.slug] = card.querySelector('.rows');
    }
    var id = s.file;
    var li = document.createElement('li');
    li.className = 'row' + (done[id] ? ' copied' : '');
    var label = s.parts > 1 ? 'Section ' + s.part + ' of ' + s.parts : 'Whole page';
    li.innerHTML = '<div class="what"><strong>' + label + '</strong><span class="meta">Box height ≈ ' + s.height + ' px · ' + s.kb + ' KB</span></div>';
    var btn = document.createElement('button');
    btn.className = 'copy'; btn.type = 'button';
    btn.textContent = done[id] ? 'Copy again' : 'Copy';
    btn.setAttribute('aria-label', 'Copy ' + s.name + ' ' + label.toLowerCase());
    btn.addEventListener('click', function () {
      var text = codeFor(s);
      function mark() {
        done[id] = true; save(KEY_DONE, done);
        li.classList.add('copied'); btn.textContent = 'Copied';
        setTimeout(function () { btn.textContent = 'Copy again'; }, 1800);
      }
      function fallback() {
        var ta = li.querySelector('textarea') || document.createElement('textarea');
        ta.className = 'fallback'; ta.value = text; ta.readOnly = true;
        ta.setAttribute('aria-label', 'Embed code for ' + s.name + ' ' + label.toLowerCase());
        li.appendChild(ta); ta.focus(); ta.select();
        btn.textContent = 'Press Ctrl+C / ⌘C';
      }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(mark, fallback);
      else fallback();
    });
    li.appendChild(btn);
    groups[s.slug].appendChild(li);
  });
})();
</script>
'''
(OUT / "embed-kit.html").write_text(page.replace("__DATA__", data))
print("embed-kit.html", round(len(page.encode()) / 1024 + len(data) / 1024), "KB")
