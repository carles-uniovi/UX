/* Se ejecuta antes del CSS para aplicar la preferencia sin destellos. */
(() => {
  // Antes del primer pintado se reserva el espacio de los controles y se
  // recoge la navegación móvil. Sin JS, el menú permanece visible.
  document.documentElement.classList.add('js');
  if (location.pathname.endsWith('/buscar.html') && new URLSearchParams(location.search).get('q')?.trim()) {
    document.documentElement.classList.add('search-pending');
  }
  let theme = 'light';
  try { theme = localStorage.getItem('adweb-v3-theme') === 'dark' ? 'dark' : 'light'; }
  catch { /* El tema sigue disponible si el almacenamiento está bloqueado. */ }
  document.documentElement.dataset.theme = theme;
  document.addEventListener('DOMContentLoaded', () => {
    document.documentElement.classList.remove('search-pending');
    // Si site.js no llega a cargar, recupera los enlaces de navegación.
    if (!document.querySelector('#navigation')?.hasAttribute('data-collapsed')) {
      document.documentElement.classList.remove('js');
    }
    const button = document.querySelector('.theme-toggle');
    if (!button) return;
    const update = () => {
      button.setAttribute('aria-pressed', String(theme === 'dark'));
      const english = document.documentElement.lang === 'en';
      button.title = theme === 'dark'
        ? (english ? 'Enable light mode' : 'Activar modo claro')
        : (english ? 'Enable dark mode' : 'Activar modo oscuro');
      button.setAttribute('aria-label', button.title);
    };
    update();
    button.hidden = false;
    button.addEventListener('click', () => {
      theme = theme === 'light' ? 'dark' : 'light';
      document.documentElement.dataset.theme = theme;
      update();
      try { localStorage.setItem('adweb-v3-theme', theme); }
      catch { /* La preferencia se conserva durante esta página. */ }
    });
  }, { once: true });
})();
