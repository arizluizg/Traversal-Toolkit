const dfaSection = document.getElementById('page-dfa');
if (dfaSection) {
  const esc = (value) => String(value).replace(/[&<>\"]/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', '\\': '&#92;' }[char]));

  const dfaInputs = {
    definition: document.getElementById('dfa-definition'),
    string: document.getElementById('dfa-string'),
    run: document.getElementById('dfa-run'),
    output: document.getElementById('dfa-output')
  };

  async function analyzeDFA() {
    const definition = dfaInputs.definition.value;
    const testString = dfaInputs.string.value;

    if (!testString) {
      dfaInputs.output.innerHTML = "<p class='hint'>Enter a test string.</p>";
      return;
    }

    const body = {
      dfa: definition,
      dfa_source: 'custom',
      dfa_custom: testString,
      pre: '',
      ino: '',
      post: '',
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
    if (data.error) {
      dfaInputs.output.innerHTML = `<p class="hint" style="color:var(--bad)">${esc(data.error)}</p>`;
      return;
    }

    dfaInputs.output.innerHTML = `<pre>${esc(data.dfa.trace.join('\n'))}</pre>` +
      `<p class="${data.dfa.accepted ? 'ok' : 'no'}"><strong>${data.dfa.accepted ? 'ACCEPTED' : 'REJECTED'}</strong></p>`;
  }

  dfaInputs.run.addEventListener('click', analyzeDFA);
}
