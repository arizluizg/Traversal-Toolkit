const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
const show = v => typeof v === "boolean" ? (v ? "Yes" : "No") : v;
const table = rows => "<table>" + rows.map(([k, v]) => `<tr><th>${esc(k)}</th><td>${esc(show(v))}</td></tr>`).join("") + "</table>";
const FIELDS = ["pre", "ino", "post", "str_a", "str_b", "find", "set_a", "set_b", "dfa", "dfa_source", "dfa_custom"];

function drawTree(root, ino) {
  const xs = Object.fromEntries(ino.map((v, i) => [v, i])), nodes = [], edges = [];
  (function go(n, d, p) {
    if (!n) return;
    const pt = {x: 36 + xs[n.v] * 52, y: 32 + d * 64, v: n.v};
    nodes.push(pt);
    if (p) edges.push([p, pt]);
    go(n.l, d + 1, pt); go(n.r, d + 1, pt);
  })(root, 0, null);
  const w = 72 + (ino.length - 1) * 52, h = Math.max(...nodes.map(n => n.y)) + 40;
  return `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">` +
    edges.map(([a, b]) => `<line x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}" stroke="#9fb1bb" stroke-width="2"/>`).join("") +
    nodes.map(n => `<circle cx="${n.x}" cy="${n.y}" r="18" fill="#e3f3f4" stroke="#0e7c86" stroke-width="2"/>` +
      `<text x="${n.x}" y="${n.y + 5}" text-anchor="middle" font-size="14">${esc(n.v)}</text>`).join("") + "</svg>";
}

async function analyze() {
  const body = Object.fromEntries(FIELDS.map(f => [f, $("#" + f).value]));
  const res = await fetch("/api/analyze", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)});
  const d = await res.json();
  $("#error").textContent = d.error || "";
  if (d.error) return;
  $("#out-tree").innerHTML = `<div class="tree">${drawTree(d.tree, d.inorder)}</div>` + table(d.summary);
  $("#out-str").innerHTML = table(d.strings);
  $("#out-set").innerHTML = table(d.sets);
  $("#out-dfa").innerHTML = `<pre>${esc(d.dfa.trace.join("\n"))}</pre>` +
    `<p class="${d.dfa.accepted ? "ok" : "no"}"><strong>${d.dfa.accepted ? "ACCEPTED" : "REJECTED"}</strong></p>`;
}

document.querySelectorAll(".tabs button").forEach(b => b.onclick = () => {
  document.querySelectorAll(".tabs button, .panel").forEach(e => e.classList.remove("active"));
  b.classList.add("active");
  $("#tab-" + b.dataset.tab).classList.add("active");
});
document.querySelectorAll(".rerun").forEach(b => b.onclick = analyze);
$("#go").onclick = analyze;

fetch("/api/samples").then(r => r.json()).then(list => {
  list.forEach((s, i) => $("#example").add(new Option(s.name, i)));
  $("#example").onchange = e => {
    const s = list[e.target.value];
    if (!s) return;
    $("#pre").value = s.pre; $("#ino").value = s.ino; $("#post").value = s.post;
    analyze();
  };
});
