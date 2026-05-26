<script>
(function() {
  const html = document.documentElement;
  const stored = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = stored || (prefersDark ? 'dark' : 'light');
  html.setAttribute('data-bs-theme', theme);
  const body = document.body;
  if (theme === 'dark') {
    body.classList.remove('quarto-light');
    body.classList.add('quarto-dark');
  } else {
    body.classList.remove('quarto-dark');
    body.classList.add('quarto-light');
  }
  const tools = document.querySelector('.quarto-navbar-tools');
  if (tools) {
    const btn = document.createElement('button');
    btn.id = 'theme-toggle';
    btn.setAttribute('aria-label', 'Toggle theme');
    btn.style.cssText = 'display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border:1px solid var(--border);border-radius:var(--radius);background:var(--surface);cursor:pointer;padding:0;font-size:1.1rem;line-height:1;';
    btn.innerHTML = theme === 'dark' ? '&#x2600;&#xFE0F;' : '&#x1F319;';
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      const current = html.getAttribute('data-bs-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-bs-theme', next);
      if (next === 'dark') {
        body.classList.remove('quarto-light');
        body.classList.add('quarto-dark');
      } else {
        body.classList.remove('quarto-dark');
        body.classList.add('quarto-light');
      }
      btn.innerHTML = next === 'dark' ? '&#x2600;&#xFE0F;' : '&#x1F319;';
      localStorage.setItem('theme', next);
    });
    tools.appendChild(btn);
  }
})();
</script>
