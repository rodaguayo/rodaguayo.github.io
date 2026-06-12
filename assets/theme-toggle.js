<script>
function sunSVG() {
  return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';
}
function moonSVG() {
  return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
}
(function() {
  const html = document.documentElement;
  const stored = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = stored || (prefersDark ? 'dark' : 'light');
  html.setAttribute('data-bs-theme', theme);
  const nav = document.querySelector('.navbar');
  if (nav) nav.setAttribute('data-bs-theme', theme);
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
    btn.style.cssText = 'display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border:1px solid var(--border);border-radius:var(--radius);background:var(--surface);cursor:pointer;padding:0;';
    btn.innerHTML = theme === 'dark' ? sunSVG() : moonSVG();
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      const current = html.getAttribute('data-bs-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-bs-theme', next);
      if (nav) nav.setAttribute('data-bs-theme', next);
      if (next === 'dark') {
        body.classList.remove('quarto-light');
        body.classList.add('quarto-dark');
      } else {
        body.classList.remove('quarto-dark');
        body.classList.add('quarto-light');
      }
      btn.innerHTML = next === 'dark' ? sunSVG() : moonSVG();
      localStorage.setItem('theme', next);
    });
    tools.appendChild(btn);
  }
})();
</script>
