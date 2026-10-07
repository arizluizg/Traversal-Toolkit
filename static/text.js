const textSection = document.getElementById('page-text');
if (textSection) {
  const esc = (value) => String(value).replace(/[&<>\"]/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', '\\': '&#92;' }[char]));
  const show = (value) => typeof value === 'boolean' ? (value ? 'Yes' : 'No') : value;
  const table = (rows) => '<table>' + rows.map(([key, value]) => `<tr><th>${esc(key)}</th><td>${esc(show(value))}</td></tr>`).join('') + '</table>';

  const textInputs = {
    a: document.getElementById('text-input-a'),
    b: document.getElementById('text-input-b'),
    analyze: document.getElementById('text-analyze'),
    combined: document.getElementById('text-output-combined'),
    results: document.getElementById('text-results-grid'),
    outputA: document.getElementById('text-output-a'),
    outputB: document.getElementById('text-output-b')
  };

  function analyzeText() {
    const a = textInputs.a.value;
    const b = textInputs.b.value;

    if (!a && !b) {
      textInputs.combined.style.display = 'none';
      textInputs.results.style.display = 'none';
      return;
    }

    const cleanA = a.toLowerCase().replace(/\s+/g, '');
    const reversedA = cleanA.split('').reverse().join('');
    const cleanB = b.toLowerCase().replace(/\s+/g, '');
    const reversedB = cleanB.split('').reverse().join('');

    const combined = [
      ['Text A', a],
      ['Text B', b],
      ['Concatenation (A + B)', a + b],
      ['Length A / B', `${a.length} / ${b.length}`]
    ];

    const opsA = [
      ['Reversed', a.split('').reverse().join('')],
      ['Is palindrome', cleanA === reversedA],
      ['Uppercase', a.toUpperCase()],
      ['Lowercase', a.toLowerCase()],
      ['First 3 chars', a.substring(0, 3)],
      ['Last 3 chars', b ? a.substring(a.length - 3) : ''],
      ['Unique chars', new Set(a).size]
    ];

    const opsB = [
      ['Reversed', b.split('').reverse().join('')],
      ['Is palindrome', cleanB === reversedB],
      ['Uppercase', b.toUpperCase()],
      ['Lowercase', b.toLowerCase()],
      ['First 3 chars', b.substring(0, 3)],
      ['Last 3 chars', b.substring(b.length - 3)],
      ['Unique chars', new Set(b).size]
    ];

    textInputs.combined.style.display = 'block';
    textInputs.results.style.display = 'grid';
    textInputs.combined.innerHTML = table(combined);
    textInputs.outputA.innerHTML = table(opsA);
    textInputs.outputB.innerHTML = table(opsB);
  }

  textInputs.analyze.addEventListener('click', analyzeText);
}
