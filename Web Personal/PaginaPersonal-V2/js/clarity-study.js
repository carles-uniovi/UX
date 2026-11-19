/* Captura exclusiva del estudio, con aceptación explícita y continuidad por pestaña.
   Las visitas normales no cargan Clarity. No se envían nombres ni perfiles. */
(() => {
  'use strict';
  const key = 'ux-clarity-tanda2';
  const allowed = /^(U0[123]|PILOTO-(PC|TABLETA|MOVIL))$/;
  const project = window.UX_CLARITY_PROJECT_ID || '';
  const url = new URL(location.href);
  const requested = url.searchParams.get('prueba');
  const en = document.documentElement.lang === 'en';
  const t = (es, english) => en ? english : es;
  let saved;
  try { saved = JSON.parse(sessionStorage.getItem(key) || 'null'); } catch (_) { /* Sin almacenamiento: no se captura. */ }
  // Un registro caduca a los 60 minutos; no arrastra aceptación a otro día.
  const valid = saved && allowed.test(saved.participant) && saved.project === project &&
    Number.isFinite(saved.started) && Date.now() - saved.started >= 0 && Date.now() - saved.started < 3600000;
  const clearRequest = () => {
    url.searchParams.delete('prueba');
    history.replaceState(null, '', url.href);
  };
  const node = (tag, text) => {
    const el = document.createElement(tag);
    if (text) el.textContent = text;
    return el;
  };
  const stop = () => {
    try { sessionStorage.removeItem(key); } catch (_) { /* La recarga tampoco cargará Clarity. */ }
    if (window.clarity) {
      window.clarity('consentv2', { analytics_Storage: 'denied', ad_Storage: 'denied' });
      // La API antigua se usa solo para borrar cookies y finalizar la sesión.
      window.clarity('consent', false);
    }
    clearRequest();
    location.reload();
  };
  function start(state) {
    const controls = node('div');
    controls.className = 'ux-study-controls';
    const status = node('p', t('Registro habilitado para ', 'Recording enabled for ') + state.participant);
    status.setAttribute('role', 'status');
    const finish = node('button', t('Finalizar registro', 'End recording'));
    finish.type = 'button';
    finish.addEventListener('click', stop);
    controls.append(status, finish);
    document.querySelector('.site-footer').append(controls);
    // Se crea la cola antes de insertar el script remoto y después de aceptar.
    window.clarity = window.clarity || function () {
      (window.clarity.q = window.clarity.q || []).push(arguments);
    };
    window.clarity('consentv2', { analytics_Storage: 'granted', ad_Storage: 'denied' });
    window.clarity('set', 'estudio', 'web-personal-tanda2');
    window.clarity('set', 'fase', state.participant.startsWith('PILOTO-') ? 'piloto' : 'real');
    window.clarity('set', 'participante', state.participant);
    const script = node('script');
    script.async = true;
    script.src = 'https://www.clarity.ms/tag/' + project;
    script.onerror = () => {
      status.textContent = t('Clarity no se ha podido cargar. No iniciar la prueba.', 'Clarity could not load. Do not start the test.');
    };
    document.head.append(script);
  }
  if (!/^https?:$/.test(location.protocol)) return;
  if (!requested && valid && /^[a-z0-9]+$/i.test(project)) { start(saved); return; }
  if (!requested || !allowed.test(requested)) return;
  // Cambiar de código en una pestaña activa no mezcla dos participantes.
  if (valid) { stop(); return; }
  const dialog = node('dialog');
  dialog.id = 'ux-study-dialog';
  dialog.setAttribute('aria-labelledby', 'ux-study-title');
  const title = node('h2', t('Prueba de usabilidad', 'Usability test'));
  title.id = 'ux-study-title';
  const info = node('p', t('Microsoft Clarity registrará las páginas visitadas, clics o toques y desplazamientos para este estudio académico. Puedes terminar el registro desde el pie de página. Código: ', 'Microsoft Clarity will record pages, clicks or taps and scrolling for this academic study. You can end recording in the footer. Code: ') + requested);
  const accept = node('button', t('Participar y registrar', 'Participate and record'));
  accept.type = 'button';
  const reject = node('button', t('Continuar sin registro', 'Continue without recording'));
  reject.type = 'button';
  const close = () => { clearRequest(); dialog.close(); dialog.remove(); };
  reject.addEventListener('click', close);
  dialog.addEventListener('cancel', event => { event.preventDefault(); close(); });
  accept.addEventListener('click', () => {
    const state = { participant: requested, project, started: Date.now() };
    try { sessionStorage.setItem(key, JSON.stringify(state)); } catch (_) {
      info.textContent = t('El navegador no permite guardar esta sesión. No iniciar la prueba.', 'This browser cannot save the session. Do not start the test.');
      return;
    }
    close();
    start(state);
  });
  if (!/^[a-z0-9]+$/i.test(project)) {
    info.textContent = t('Falta configurar el identificador del proyecto de Clarity. No iniciar la prueba.', 'The Clarity project ID has not been configured. Do not start the test.');
    accept.disabled = true;
  }
  dialog.append(title, info, accept, reject);
  document.body.append(dialog);
  dialog.showModal();
})();
