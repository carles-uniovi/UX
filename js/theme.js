(() => {
  const storageKey = 'adweb-theme';
  const root = document.documentElement;
  let theme = 'light';

  try {
    if (localStorage.getItem(storageKey) === 'dark') {
      theme = 'dark';
    }
  } catch {
    // El selector sigue funcionando si el navegador bloquea el almacenamiento.
  }

  // Se aplica antes de cargar el CSS para evitar mostrar el tema equivocado.
  root.dataset.theme = theme;

  document.addEventListener('DOMContentLoaded', () => {
    const button = document.querySelector('.theme-toggle');
    if (!button) return;

    const icon = button.querySelector('span');

    function updateButton() {
      button.setAttribute('aria-pressed', String(theme === 'dark'));
      icon.textContent = theme === 'dark' ? '🌞' : '🌙';
      button.title = theme === 'dark' ? 'Activar modo claro' : 'Activar modo oscuro';
    }

    updateButton();
    button.hidden = false;

    button.addEventListener('click', () => {
      theme = theme === 'dark' ? 'light' : 'dark';
      root.dataset.theme = theme;
      updateButton();

      try {
        localStorage.setItem(storageKey, theme);
      } catch {
        // Se mantiene el tema de esta pagina aunque no se pueda guardar.
      }
    });
  }, { once: true });
})();
