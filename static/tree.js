const treeSection = document.getElementById('page-tree');
if (treeSection) {
  const esc = (value) => String(value).replace(/[&<>\"]/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', '\\': '&#92;' }[char]));
  const show = (value) => typeof value === 'boolean' ? (value ? 'Yes' : 'No') : value;
  const table = (rows) => '<table>' + rows.map(([key, value]) => `<tr><th>${esc(key)}</th><td>${esc(show(value))}</td></tr>`).join('') + '</table>';

  const treeInputs = {
    pre: document.getElementById('tree-pre'),
    ino: document.getElementById('tree-ino'),
    post: document.getElementById('tree-post'),
    example: document.getElementById('tree-example'),
    go: document.getElementById('tree-go'),
    error: document.getElementById('tree-error'),
    output: document.getElementById('tree-output')
  };

  function drawTree(root, ino) {
    const xs = Object.fromEntries(ino.map((value, index) => [value, index]));
    const nodes = [];
    const edges = [];

    (function go(node, depth, parent) {
      if (!node) return;
      const point = { x: 36 + xs[node.v] * 52, y: 32 + depth * 64, v: node.v };
      nodes.push(point);
      if (parent) edges.push([parent, point]);
      go(node.l, depth + 1, point);
      go(node.r, depth + 1, point);
    })(root, 0, null);

    const width = 72 + (ino.length - 1) * 52;
    const height = Math.max(...nodes.map((node) => node.y)) + 40;

    return `<svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">` +
      edges.map(([a, b]) => `<line x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}" stroke="#9fb1bb" stroke-width="2"/>`).join('') +
      nodes.map((node) => `<circle cx="${node.x}" cy="${node.y}" r="18" fill="#e3f3f4" stroke="#0e7c86" stroke-width="2"/>` +
        `<text x="${node.x}" y="${node.y + 5}" text-anchor="middle" font-size="14">${esc(node.v)}</text>`).join('') +
      '</svg>';
  }

  async function analyzeTree() {
    const body = {
      pre: treeInputs.pre.value,
      ino: treeInputs.ino.value,
      post: treeInputs.post.value,
      str_a: 'preorder',
      str_b: 'postorder',
      find: '',
      set_a: '',
      set_b: ''
    };

    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });

    const data = await response.json();
    treeInputs.error.textContent = data.error || '';
    if (data.error) return;

    treeInputs.output.innerHTML = `<div class="tree">${drawTree(data.tree, data.inorder)}</div>` + table(data.summary);
  }

  treeInputs.go.addEventListener('click', analyzeTree);

  fetch('/api/samples')
    .then((response) => response.json())
    .then((list) => {
      list.forEach((sample, index) => treeInputs.example.add(new Option(sample.name, index)));
      treeInputs.example.addEventListener('change', (event) => {
        const sample = list[event.target.value];
        if (!sample) return;
        treeInputs.pre.value = sample.pre;
        treeInputs.ino.value = sample.ino;
        treeInputs.post.value = sample.post;
        analyzeTree();
      });
    });
}
