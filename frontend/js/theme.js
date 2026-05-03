export const initTheme = () => {
  const saved = localStorage.getItem('nc_theme') || 'dark';
  applyTheme(saved);
  document.getElementById('btn-theme').addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    applyTheme(current === 'dark' ? 'light' : 'dark');
  });
};

const applyTheme = (theme) => {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('nc_theme', theme);
  const icon = document.getElementById('theme-icon');
  const text = document.getElementById('theme-text');
  if (icon) icon.setAttribute('data-lucide', theme === 'light' ? 'sun' : 'moon');
  if (text) text.textContent = theme === 'light' ? 'Modo Claro' : 'Modo Oscuro';
  lucide.createIcons();
};
