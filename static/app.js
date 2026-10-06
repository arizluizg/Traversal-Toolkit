const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
const show = v => typeof v === "boolean" ? (v ? "Yes" : "No") : v;
const table = rows => "<table>" + rows.map(([k, v]) => `<tr><th>${esc(k)}</th><td>${esc(show(v))}</td></tr>`).join("") + "</table>";
const FIELDS = ["pre", "ino", "post", "str_a", "str_b", "find", "set_a", "set_b"];

// Sidebar toggle
$("#toggle-sidebar").onclick = () => {
  $("#sidebar").classList.toggle("closed");
};

// Page navigation
document.querySelectorAll(".sidebar-item").forEach(btn => {
  btn.onclick = () => {
    document.querySelectorAll(".sidebar-item").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
    btn.classList.add("active");
    const page = $("#page-" + btn.dataset.page);
    if (page) page.classList.add("active");
  };
});

// Set default active
if ($("#page-tree")) $("#page-tree").classList.add("active");

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

async function analyzeTree() {
  const body = {pre: $("#pre").value, ino: $("#ino").value, post: $("#post").value, str_a: "preorder", str_b: "postorder", find: "", set_a: "", set_b: "", dfa: $("#dfa").value, dfa_source: "preorder", dfa_custom: ""};
  const res = await fetch("/api/analyze", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)});
  const d = await res.json();
  $("#error").textContent = d.error || "";
  if (d.error) return;
  $("#out-tree").innerHTML = `<div class="tree">${drawTree(d.tree, d.inorder)}</div>` + table(d.summary);
}

async function analyzeText() {
  const a = $("#text-input").value;
  const b = $("#text-input-b").value;
  
  if (!a && !b) {
    $("#out-combined").style.display = "none";
    $("#results-grid").style.display = "none";
    return;
  }
  
  const cleanA = a.toLowerCase().replace(/\s+/g, "");
  const reversedA = cleanA.split("").reverse().join("");
  const cleanB = b.toLowerCase().replace(/\s+/g, "");
  const reversedB = cleanB.split("").reverse().join("");
  
  // Combined operations
  const combined = [
    ["Text A", a],
    ["Text B", b],
    ["Concatenation (A + B)", a + b],
    ["Length A / B", `${a.length} / ${b.length}`],
  ];
  
  // Text A operations
  const opsA = [
    ["Reversed", a.split("").reverse().join("")],
    ["Is palindrome", cleanA === reversedA],
    ["Uppercase", a.toUpperCase()],
    ["Lowercase", a.toLowerCase()],
    ["First 3 chars", a.substring(0, 3)],
    ["Last 3 chars", a.substring(a.length - 3)],
    ["Unique chars", new Set(a).size],
  ];
  
  // Text B operations
  const opsB = [
    ["Reversed", b.split("").reverse().join("")],
    ["Is palindrome", cleanB === reversedB],
    ["Uppercase", b.toUpperCase()],
    ["Lowercase", b.toLowerCase()],
    ["First 3 chars", b.substring(0, 3)],
    ["Last 3 chars", b.substring(b.length - 3)],
    ["Unique chars", new Set(b).size],
  ];
  
  $("#out-combined").style.display = "block";
  $("#results-grid").style.display = "grid";
  $("#out-combined").innerHTML = table(combined);
  $("#out-text-a").innerHTML = table(opsA);
  $("#out-text-b").innerHTML = table(opsB);
}

async function analyzeSets() {
  const a = $("#set_a").value.split(/[\s,]+/).filter(x => x);
  const b = $("#set_b").value.split(/[\s,]+/).filter(x => x);
  const A = new Set(a), B = new Set(b);
  const fmt = s => "{" + Array.from(s).sort().join(", ") + "}";
  
  const ops = [
    ["Set A", fmt(A)],
    ["Set B", fmt(B)],
    ["Union", fmt(new Set([...A, ...B]))],
    ["Intersection", fmt(new Set([...A].filter(x => B.has(x))))],
    ["A - B", fmt(new Set([...A].filter(x => !B.has(x))))],
    ["B - A", fmt(new Set([...B].filter(x => !A.has(x))))],
    ["|A| / |B|", `${A.size} / ${B.size}`],
  ];
  
  $("#out-set").innerHTML = table(ops);
}

async function analyzeDFA() {
  const dfa_text = $("#dfa").value;
  const test_str = $("#dfa_string").value;
  
  if (!test_str) {
    $("#out-dfa").innerHTML = "<p class='hint'>Enter a test string.</p>";
    return;
  }
  
  const body = {dfa: dfa_text, dfa_source: "custom", dfa_custom: test_str, pre: "", ino: "", post: "", str_a: "preorder", str_b: "postorder", find: "", set_a: "", set_b: ""};
  const res = await fetch("/api/analyze", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)});
  const d = await res.json();
  
  if (d.error) {
    $("#out-dfa").innerHTML = `<p class="hint" style="color:var(--bad)">${esc(d.error)}</p>`;
    return;
  }
  
  $("#out-dfa").innerHTML = `<pre>${esc(d.dfa.trace.join("\n"))}</pre>` +
    `<p class="${d.dfa.accepted ? "ok" : "no"}"><strong>${d.dfa.accepted ? "ACCEPTED" : "REJECTED"}</strong></p>`;
}

// Event listeners
$("#go").onclick = analyzeTree;
$("#text-analyze").onclick = analyzeText;
$("#set-analyze").onclick = analyzeSets;
$("#dfa-analyze").onclick = analyzeDFA;

// Load examples
fetch("/api/samples").then(r => r.json()).then(list => {
  list.forEach((s, i) => $("#example").add(new Option(s.name, i)));
  $("#example").onchange = e => {
    const s = list[e.target.value];
    if (!s) return;
    $("#pre").value = s.pre; $("#ino").value = s.ino; $("#post").value = s.post;
    analyzeTree();
  };
});
