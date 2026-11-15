/* Se ejecuta antes del CSS para aplicar la preferencia sin destellos. */
(() => {
  let theme = 'light';
  try { theme = localStorage.getItem('adweb-theme') === 'dark' ? 'dark' : 'light'; }
  catch { /* El tema sigue disponible si el almacenamiento está bloqueado. */ }
  document.documentElement.dataset.theme = theme;
  document.addEventListener('DOMContentLoaded', () => {
    const button = document.querySelector('.theme-toggle');
    if (!button) return;
    const update = () => {
      button.setAttribute('aria-pressed', String(theme === 'dark'));
      const english = document.documentElement.lang === 'en';
      button.title = theme === 'dark'
        ? (english ? 'Enable light mode' : 'Activar modo claro')
        : (english ? 'Enable dark mode' : 'Activar modo oscuro');
    };
    update();
    button.hidden = false;
    button.addEventListener('click', () => {
      theme = theme === 'light' ? 'dark' : 'light';
      document.documentElement.dataset.theme = theme;
      update();
      try { localStorage.setItem('adweb-theme', theme); }
      catch { /* La preferencia se conserva durante esta página. */ }
    });
  }, { once: true });
})();
