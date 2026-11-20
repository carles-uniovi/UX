/* Mejoras progresivas: sin JavaScript la navegación permanece desplegada. */
(() => {
  // La cabecera crece con etiquetas, zoom o traducciones: las anclas y el foco
  // deben quedar por debajo de su altura real, no de un desplazamiento fijo.
  const header = document.querySelector('.site-header');
  if (header && typeof ResizeObserver !== 'undefined') {
    const updateHeader = () => {
      const height = getComputedStyle(header).position === 'sticky' ? header.getBoundingClientRect().height : 0;
      document.documentElement.style.setProperty('--header-height', `${height}px`);
    };
    new ResizeObserver(updateHeader).observe(header);
    updateHeader();
  }
  const button = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#navigation');
  const mobile = matchMedia('(max-width: 64em)');
  function setOpen(open) {
    button.setAttribute('aria-expanded', String(open));
    navigation.dataset.collapsed = String(!open);
  }
  if (button && navigation) {
    button.hidden = false;
    setOpen(!mobile.matches);
    button.addEventListener('click', () => {
      const open = button.getAttribute('aria-expanded') !== 'true';
      setOpen(open);
      if (open) navigation.querySelector('a')?.focus();
    });
    mobile.addEventListener('change', () => {
      // Evita dejar el foco dentro de una región que va a ocultarse.
      if (mobile.matches && navigation.contains(document.activeElement)) button.focus();
      setOpen(!mobile.matches);
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && mobile.matches && button.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
        button.focus();
      }
    });
    document.addEventListener('click', event => {
      if (mobile.matches && !navigation.contains(event.target) && !button.contains(event.target)) setOpen(false);
    });
    document.addEventListener('focusin', event => {
      if (mobile.matches && !navigation.contains(event.target) && !button.contains(event.target)) setOpen(false);
    });
  }
  // El enlace original sigue siendo útil sin JS o sin soporte de dialog.
  // Un único reproductor evita audio simultáneo y mantiene estables las tarjetas.
  const dialog = document.querySelector('#media-player');
  if (dialog && typeof dialog.showModal === 'function') {
    const stage = dialog.querySelector('#media-stage');
    const title = dialog.querySelector('#media-title');
    const status = dialog.querySelector('#media-status');
    const direct = dialog.querySelector('#media-direct');
    const close = dialog.querySelector('.dialog-close');
    let player;
    let opener;
    close.addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', event => {
      if (event.target !== dialog) return;
      const rect = dialog.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
    });
    dialog.addEventListener('close', () => {
      // close se dispara también al pulsar Escape. Libera el archivo y devuelve
      // el foco al enlace exacto que abrió el reproductor.
      if (player) {
        if (player.tagName.toLowerCase() === 'iframe') {
          // Descargar el iframe detiene YouTube sin cargar su API global.
          player.src = 'about:blank';
        } else {
          player.pause();
          player.removeAttribute('src');
          player.load();
        }
        player = undefined;
      }
      stage.replaceChildren();
      status.textContent = '';
      direct.hidden = true;
      document.body.classList.remove('media-open');
      opener?.focus();
      opener = undefined;
    });
    for (const trigger of document.querySelectorAll('.media-trigger')) {
      trigger.setAttribute('aria-haspopup', 'dialog');
      trigger.setAttribute('aria-controls', 'media-player');
      trigger.addEventListener('click', event => {
        if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        const type = trigger.dataset.mediaType;
        if (!['audio', 'video', 'youtube'].includes(type)) return;
        const videoId = trigger.dataset.youtubeId;
        if (type === 'youtube' && !/^[A-Za-z0-9_-]{11}$/.test(videoId || '')) return;
        event.preventDefault();
        if (dialog.open) return;
        opener = trigger;
        title.textContent = trigger.dataset.mediaTitle;
        status.textContent = '';
        direct.href = trigger.href;
        direct.target = '_blank';
        direct.rel = 'noopener noreferrer';
        direct.hidden = type !== 'youtube';
        const english = document.documentElement.lang === 'en';
        direct.textContent = type === 'youtube' ? (english ? 'Watch on YouTube' : 'Ver en YouTube') : (english ? 'Open file' : 'Abrir archivo');
        direct.title = english ? 'Opens in a new tab' : 'Se abre en una pestaña nueva';
        direct.setAttribute('aria-label', `${direct.textContent} (${direct.title})`);
        player = document.createElement(type === 'youtube' ? 'iframe' : type);
        if (type === 'youtube') {
          const language = english ? 'en' : 'es';
          // Solo se conecta con YouTube al abrir el diálogo. Se mantienen los
          // controles, el teclado y la pantalla completa, sin autoplay.
          player.src = `https://www.youtube-nocookie.com/embed/${videoId}?controls=1&disablekb=0&autoplay=0&playsinline=1&cc_load_policy=1&cc_lang_pref=${language}&hl=${language}`;
          player.title = trigger.dataset.mediaTitle;
          player.allow = 'encrypted-media; picture-in-picture; fullscreen';
          player.allowFullscreen = true;
          player.referrerPolicy = 'strict-origin-when-cross-origin';
        } else {
          player.controls = true;
          player.preload = 'none';
          player.src = trigger.href;
          player.setAttribute('aria-label', trigger.dataset.mediaTitle);
          if (type === 'video') player.playsInline = true;
        }
        player.addEventListener('error', event => {
          if (!dialog.open || event.currentTarget !== player) return;
          status.textContent = document.documentElement.lang === 'en' ? 'The file could not be played.' : 'No se ha podido reproducir el archivo.';
          direct.hidden = false;
        });
        stage.replaceChildren(player);
        dialog.showModal();
        document.body.classList.add('media-open');
        close.focus();
      });
    }
  }
  // Cada dirección tiene confirmación propia; no obliga a desplazarse al final
  // de Contacto. Si falla Clipboard, se selecciona el texto para copia manual.
  for (const copy of document.querySelectorAll('.copy-email')) {
    const label = copy.textContent;
    let restore;
    copy.hidden = false;
    copy.addEventListener('click', async () => {
      const english = document.documentElement.lang === 'en';
      const status = document.getElementById(copy.dataset.status);
      clearTimeout(restore);
      copy.disabled = true;
      try {
        if (!navigator.clipboard?.writeText) throw new Error('clipboard-unavailable');
        await navigator.clipboard.writeText(copy.dataset.email);
        copy.textContent = english ? 'Copied' : 'Copiado';
        status.textContent = (english ? 'Address copied: ' : 'Dirección copiada: ') + copy.dataset.email;
      } catch {
        const target = document.getElementById(copy.dataset.copyTarget);
        const selection = window.getSelection?.();
        if (target && selection && document.createRange) {
          const range = document.createRange();
          range.selectNodeContents(target);
          selection.removeAllRanges();
          selection.addRange(range);
        }
        copy.textContent = label;
        status.textContent = english
          ? 'Automatic copying is unavailable. Select or press and hold the address, then copy it.'
          : 'La copia automática no está disponible. Selecciona o mantén pulsada la dirección y cópiala.';
      } finally {
        copy.disabled = false;
        restore = setTimeout(() => { copy.textContent = label; }, 2500);
      }
    });
  }
})();
