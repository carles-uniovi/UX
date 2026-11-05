(() => {
  const cards = document.querySelectorAll(
    '.category-list > section > section[data-media-type], .category-list > section > section[data-media-src]'
  );
  const mediaItems = [];

  for (const card of cards) {
    const type = card.dataset.mediaType;
    const source = card.dataset.mediaSrc;
    const title = card.querySelector('h3')?.textContent?.trim();
    const image = card.querySelector(':scope > img');

    if ((type !== 'audio' && type !== 'video') || !source || !title || !image) {
      console.error('No se pudo configurar el recurso multimedia de esta tarjeta.', card);
      continue;
    }

    let mediaUrl;
    try {
      mediaUrl = new URL(source, document.baseURI);
    } catch (error) {
      console.error('La ruta del recurso multimedia no es válida.', source, error);
      continue;
    }

    if (!['http:', 'https:', 'file:'].includes(mediaUrl.protocol)) {
      console.error('El recurso multimedia debe usar una ruta local o una URL HTTP(S).', source);
      continue;
    }

    mediaItems.push({ card, image, type, source: mediaUrl.href, title });
  }

  if (mediaItems.length === 0) return;

  const dialog = document.createElement('dialog');
  dialog.className = 'media-dialog';
  dialog.setAttribute('aria-labelledby', 'media-dialog-title');

  const dialogHeader = document.createElement('header');
  const dialogTitle = document.createElement('h2');
  dialogTitle.id = 'media-dialog-title';

  const playbackStatus = document.createElement('p');
  playbackStatus.className = 'media-playback-status';
  playbackStatus.setAttribute('role', 'status');
  playbackStatus.setAttribute('aria-live', 'polite');

  const closeButton = document.createElement('button');
  closeButton.className = 'media-dialog-close';
  closeButton.type = 'button';
  closeButton.setAttribute('aria-label', 'Cerrar reproductor');
  closeButton.textContent = '×';
  closeButton.addEventListener('click', () => dialog.close());

  dialogHeader.append(dialogTitle, closeButton);
  dialog.append(dialogHeader, playbackStatus);
  document.body.append(dialog);

  let activeMedia;

  dialog.addEventListener('click', (event) => {
    if (event.target === dialog) dialog.close();
  });

  dialog.addEventListener('close', () => {
    if (!activeMedia) return;

    activeMedia.pause();
    activeMedia.removeAttribute('src');
    activeMedia.load();
    activeMedia.remove();
    activeMedia = undefined;
    playbackStatus.textContent = '';
  });

  for (const { card, image, type, source, title } of mediaItems) {
    const preview = document.createElement('figure');
    preview.className = 'media-preview';

    const trigger = document.createElement('button');
    trigger.className = 'media-trigger';
    trigger.type = 'button';
    trigger.textContent = type === 'audio' ? '♫' : '▶';
    trigger.setAttribute('aria-label', `${type === 'audio' ? 'Reproducir audio' : 'Reproducir vídeo'}: ${title}`);

    trigger.addEventListener('click', () => {
      dialogTitle.textContent = title;
      playbackStatus.textContent = '';
      activeMedia = document.createElement(type);
      activeMedia.controls = true;
      activeMedia.preload = 'metadata';
      activeMedia.autoplay = true;
      activeMedia.src = source;

      if (type === 'video') activeMedia.playsInline = true;

      dialog.append(activeMedia);
      dialog.showModal();
      closeButton.focus();

      activeMedia.play().catch((error) => {
        playbackStatus.textContent = 'El navegador ha bloqueado la reproducción automática. Pulsa reproducir en los controles.';
        console.error('No se pudo iniciar la reproducción automáticamente.', error);
      });
    });

    preview.append(image, trigger);
    card.prepend(preview);
  }
})();
