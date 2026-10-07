// Expression input for the Binary Tree page. Adds an expression box to the same card
// and shows its pre/in/post trees below. No sidebar item, no other JS/HTML edits needed.
(() => {
  const $ = s => document.querySelector(s);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
 
  const page = $("#page-tree"), card = page && page.querySelector(".input"), outTree = $("#out-tree");
  if (!card || !outTree) return;
 
  const css = document.createElement("style");
  css.textContent = `#out-expr h3{margin:16px 0 6px}#out-expr h3 small{font-weight:400;opacity:.7;margin-left:8px}
  #out-expr .seq{font-family:ui-monospace,Consolas,monospace;margin:6px 0 0;word-break:break-all}
  #out-expr .tree{overflow-x:auto;border-radius:8px}#expr-error{color:#e5534b;min-height:1.2em;margin:6px 0 0}`;
  document.head.append(css);
 
  const box = document.createElement("div");
  box.innerHTML = `<hr style="border:0;border-top:1px solid rgba(255,255,255,.12);margin:14px 0">
    <label>Or enter an expression <input id="expr" value="A+B/D-E" placeholder="A+B/D-E"></label>
    <div class="row"><button id="expr-go">Build from expression</button></div><p id="expr-error"></p>`;
  card.append(box);
 
  const out = document.createElement("div");
  out.id = "out-expr";
  page.append(out);
 
  // When the traversal Analyze redraws its output, hide the expression result and show it again.
  new MutationObserver(() => { out.innerHTML = ""; outTree.style.display = ""; })
    .observe(outTree, {childList: true});
 
  const walk = {
    pre:  n => n ? [n, ...walk.pre(n.l), ...walk.pre(n.r)] : [],
    in:   n => n ? [...walk.in(n.l), n, ...walk.in(n.r)] : [],
    post: n => n ? [...walk.post(n.l), ...walk.post(n.r), n] : [],
  };
  const isOp = v => v.length === 1 && "+-*/^".includes(v);
 
  function draw(root, order) {
    const nodes = [], edges = [];
    (function go(n, d, p) {
      if (!n) return;
      n.px = 36 + n.x * 52; n.py = 32 + d * 64;
      nodes.push(n);
      if (p) edges.push([p, n]);
      go(n.l, d + 1, n); go(n.r, d + 1, n);
    })(root, 0, null);
    const w = 72 + Math.max(...nodes.map(n => n.x)) * 52, h = Math.max(...nodes.map(n => n.py)) + 40;
    return `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" style="background:#fff">` +
      edges.map(([a, b]) => `<line x1="${a.px}" y1="${a.py}" x2="${b.px}" y2="${b.py}" stroke="#9fb1bb" stroke-width="2"/>`).join("") +
      nodes.map(n => `<circle cx="${n.px}" cy="${n.py}" r="18" fill="${isOp(n.v) ? "#fde8c8" : "#e3f3f4"}" stroke="#0e7c86" stroke-width="2"/>` +
        `<text x="${n.px}" y="${n.py + 5}" text-anchor="middle" font-size="14" fill="#14262f">${esc(n.v)}</text>` +
        `<circle cx="${n.px + 14}" cy="${n.py - 14}" r="9" fill="#0e7c86"/>` +
        `<text x="${n.px + 14}" y="${n.py - 10}" text-anchor="middle" font-size="11" fill="#fff">${order.indexOf(n) + 1}</text>`).join("") + "</svg>";
  }
 
  async function build() {
    const res = await fetch("/api/expression", {method: "POST", headers: {"Content-Type": "application/json"},
                                                body: JSON.stringify({expr: $("#expr").value})});
    const d = await res.json();
    $("#expr-error").textContent = d.error || "";
    if (d.error) return;
    outTree.style.display = "none";
    $("#out-expr").innerHTML = [
      ["Preorder (prefix)", "Root → Left → Right", "pre", d.prefix],
      ["Inorder (infix)", "Left → Root → Right", "in", d.infix],
      ["Postorder (postfix)", "Left → Right → Root", "post", d.postfix],
    ].map(([name, rule, k, text]) =>
      `<h3>${name} <small>${rule}</small></h3><div class="tree">${draw(d.tree, walk[k](d.tree))}</div>` +
      `<p class="seq">${esc(text)}</p>`).join("");
  }
 
  $("#expr-go").onclick = build;
  $("#expr").addEventListener("keydown", e => { if (e.key === "Enter") build(); });
})();
 