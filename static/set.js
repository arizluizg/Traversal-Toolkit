const setSection = document.getElementById('page-set');
if (setSection) {
  const esc = (value) => String(value).replace(/[&<>\"]/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', '\\': '&#92;' }[char]));
  const show = (value) => typeof value === 'boolean' ? (value ? 'Yes' : 'No') : value;
  const table = (rows) => '<table>' + rows.map(([key, value]) => `<tr><th>${esc(key)}</th><td>${esc(show(value))}</td></tr>`).join('') + '</table>';

  const setInputs = {
    a: document.getElementById('set-a'),
    b: document.getElementById('set-b'),
    run: document.getElementById('set-run'),
    output: document.getElementById('set-output')
  };

  function analyzeSets() {
    const a = setInputs.a.value.split(/[\s,]+/).filter(Boolean);
    const b = setInputs.b.value.split(/[\s,]+/).filter(Boolean);
    const A = new Set(a);
    const B = new Set(b);
    const format = (values) => '{' + Array.from(values).sort().join(', ') + '}';

    const operations = [
      ['Set A', format(A)],
      ['Set B', format(B)],
      ['Union', format(new Set([...A, ...B]))],
      ['Intersection', format(new Set([...A].filter((value) => B.has(value))))],
      ['A - B', format(new Set([...A].filter((value) => !B.has(value))))],
      ['B - A', format(new Set([...B].filter((value) => !A.has(value))))],
      ['|A| / |B|', `${A.size} / ${B.size}`]
    ];

    setInputs.output.innerHTML = table(operations);
  }

  setInputs.run.addEventListener('click', analyzeSets);
}
