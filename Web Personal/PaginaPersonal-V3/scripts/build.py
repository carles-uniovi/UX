"""Genera los HTML estáticos y el índice del buscador. Solo usa Python estándar.

El sitio resultante no necesita Python: funciona por HTTP y abriendo index.html.
Las traducciones se mantienen junto al contenido para evitar páginas incompletas.
"""
from pathlib import Path
from html import escape
from urllib.parse import quote
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / 'PaginaPersonal'
DATE = '2026-11-20'
PUBLIC_URL = 'https://carles-uniovi.github.io/UX/v3/'
REFERENCE_URL = 'https://www.linkedin.com/in/carlos-cebell%C3%A1n-ferriz-963357347/'
LINKEDIN_URL = 'https://www.linkedin.com/in/carles-valladares-garc%C3%ADa-07a938223/'
PAGES = ['index', 'trayectoria', 'hobbies', 'intereses', 'contacto', 'ayuda', 'mapa', 'buscar', 'lectura']
LABELS = {
    'es': ['Sobre mí', 'Trayectoria', 'Aficiones', 'Intereses', 'Contacto', 'Ayuda', 'Mapa del sitio', 'Buscar', 'Versión de lectura'],
    'en': ['About me', 'Background', 'Hobbies', 'Interests', 'Contact', 'Help', 'Site map', 'Search', 'Reading version'],
}
INTRO = {
    'es': ['Mi formación, experiencia laboral y un proyecto para poner en práctica lo aprendido.', 'Videojuegos, partidas de rol y judo: lo que hago fuera de las pantallas… y también delante de ellas.', 'La música, las películas y las historias a las que me gusta volver.', 'Correo, GitHub y LinkedIn para seguir en contacto.'],
    'en': ['My education, work experience and a project to put what I have learned into practice.', 'Video games, tabletop adventures and judo: what I do away from screens… and in front of them.', 'The music, films and stories I enjoy coming back to.', 'Email, GitHub and LinkedIn to keep in touch.'],
}

# Contenido procedente de la V1 y datos adicionales facilitados por el autor,
# sin atribuirle empleos, fechas, referencias o preferencias no indicados.
HOBBIES = [
    ('videojuegos', ('Videojuegos', 'Video games'), [
        ('fire-emblem', "Fire Emblem Fortune’s Wave", 'fefw.avif', ('Uno de los juegos a los que me gusta dedicar tiempo para desconectar y sumergirme en otro mundo.', 'One of the games I enjoy spending time with to unwind and explore another world.')),
        ('baldurs-gate', 'Baldur’s Gate 3', 'bg3.webp', ('Disfruto explorando, conociendo a los personajes y tomando decisiones que dan forma a mi propia aventura.', 'Exploring, meeting the characters and shaping my own adventure are what I enjoy about this game.')),
        ('league-of-legends', 'League of Legends', 'lol.jpg', ('Una forma de compartir partidas con amigos, coordinarse en equipo e intentar que el nexo que caiga sea el contrario.', 'A way to play with friends, work as a team and try to make sure the other team’s nexus is the one that falls.')),
    ]),
    ('dnd', ('Juegos de rol: Dungeons & Dragons', 'Tabletop role-playing: Dungeons & Dragons'), [
        ('mundos-fantasia', ('Mundos de fantasía', 'Fantasy worlds'), 'd&d.jpeg', ('Me gusta imaginar lugares, personajes e historias que cobran vida alrededor de la mesa. Cada aventura es una oportunidad de descubrir un mundo diferente.', 'Imagining places, characters and stories around a table is something I enjoy. Each adventure is a chance to discover a different world.')),
        ('tardes-amigos', ('Tardes con amigos', 'Afternoons with friends'), 'd&d-amigos.jpg', ('Las partidas son una excusa para reunirnos, reírnos y construir una historia entre todos. Los planes que salen mal también suelen convertirse en buenos recuerdos.', 'Game sessions are a reason to get together, laugh and build a story together. Plans that go wrong often become fond memories too.')),
        ('algo-teatro', ('Algo de teatro', 'A little theatre'), 'dnd-actuar.jpg', ('Interpretar un personaje permite improvisar y ponerse en otra piel. Entre conversaciones y decisiones inesperadas, siempre hay espacio para un poco de teatro.', 'Playing a character is a chance to improvise and step into someone else’s shoes. Between conversations and unexpected decisions, there is always room for a little theatre.')),
    ]),
    ('judo', ('Judo', 'Judo'), [
        ('practicar-judo', ('Practicarlo', 'Practising'), 'judo-hacer.jpg', ('El judo combina actividad física, técnica y concentración. Practicarlo me permite moverme, aprender y dedicar un rato a algo fuera de las pantallas.', 'Judo combines physical activity, technique and concentration. It gives me time to move, learn and do something away from screens.')),
        ('ensenar-judo', ('Enseñarlo', 'Teaching'), 'judo-ensenyar.jpg', ('Compartir lo aprendido y ayudar a otras personas a mejorar es otra forma de disfrutar del judo. Explicar una técnica también invita a entenderla mejor.', 'Sharing what I have learned and helping others improve is another way to enjoy judo. Explaining a technique also helps me understand it better.')),
    ]),
]
INTERESTS = [
    ('musica', ('Música', 'Music'), [
        ('robe', 'Robe', 'robe.jpg', ('Uno de los artistas a los que vuelvo cuando me apetece escuchar música con calma y prestar atención a las letras.', 'An artist I come back to when I want to listen quietly and pay attention to the lyrics.'), 'Robe - Del Tiempo Perdido.mp3', 'Del Tiempo Perdido'),
        ('gavina', 'Gavina.mp3', 'gavina.jpg', ('Gavina.mp3 también tiene un hueco entre mis gustos musicales y en la música que me acompaña en el día a día.', 'Gavina.mp3 also has a place among my musical tastes and in the music that accompanies my everyday life.'), 'gavina.mp3 - SOTA EL CEL.mp3', 'SOTA EL CEL'),
        ('las-petunias', 'Las Petunias', 'las-petunias.jpg', ('Otro de los nombres que me gusta escuchar y compartir cuando hablamos de recomendaciones musicales.', 'Another name I enjoy listening to and sharing when we talk about music recommendations.'), 'Las Petunias - Marcelo Criminal.mp3', 'Marcelo Criminal'),
    ]),
    ('peliculas', ('Películas', 'Films'), [
        ('spider-verse', 'Spider-Man: Into the Spider-Verse', 'spiderman.png', ('Me llama la atención su estilo visual y la manera en que lleva la energía del cómic a la animación.', 'The visual style appeals to me. It brings the energy of comics to animation.'), 'https://www.youtube.com/watch?v=g4Hbz2jLxvQ', ('Tráiler oficial', 'Official trailer')),
        ('scott-pilgrim', 'Scott Pilgrim vs. the World', 'scott-pilgrim.jpg', ('Disfruto de su mezcla de humor, música y referencias a los videojuegos, con una personalidad visual muy marcada.', 'This film combines the humour, music and video game references I enjoy, with a distinctive visual style.'), 'https://www.youtube.com/watch?v=7wd5KEaOtm4', ('Tráiler oficial', 'Official trailer')),
    ]),
    ('series', ('Series', 'TV series'), [
        ('doctor-who', 'Doctor Who', 'dr.who.jpg', ('Me gusta dejarme llevar por sus aventuras y por la posibilidad de encontrar algo distinto en cada viaje.', 'The adventures and the chance to find something different on each journey appeal to me.')),
        ('brooklyn-99', 'Brooklyn Nine-Nine', 'brooklyn99.jpg', ('Una comedia a la que recurrir para desconectar, reírme y pasar un rato con sus personajes.', 'A comedy I turn to when I want to unwind, laugh and spend some time with its characters.')),
    ]),
    ('animanga', ('Anime y manga', 'Anime and manga'), [
        ('ousama-ranking', 'Ousama Ranking', 'osama-ranking.jpg', ('Me atraen su sensibilidad y su manera de contar una aventura que invita a conectar con los personajes.', 'Its sensitive storytelling draws me into the adventure and helps me connect with the characters.')),
        ('jojo', 'JoJo’s Bizarre Adventure', 'jojo.webp', ('Me divierten su imaginación, sus situaciones extravagantes y ese estilo tan particular que lo hace reconocible.', 'The imagination, extravagant situations and distinctive style make this series fun for me.')),
    ]),
]


def plain(html):
    from html import unescape
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', html))).strip()


def icon(name):
    shapes = {
        'search': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4.5 4.5"/>',
        'menu': '<path d="M4 6h16M4 12h16M4 18h16"/>',
        'close': '<path d="m6 6 12 12M6 18 18 6"/>',
        'play': '<path d="m9 5 11 7-11 7Z"/>',
    }
    return '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' + shapes[name] + '</svg>'


def external_links(html, english):
    """Aplica la preferencia también a lectura y enlaces sin JavaScript."""
    note = 'Opens in a new tab' if english else 'Se abre en una pestaña nueva'

    def update(match):
        attrs, content = match.groups()
        external = re.search(r'\bhref="https?://', attrs)
        media = 'class="media-trigger"' in attrs
        if not external and not media:
            return match.group(0)
        attrs += ' target="_blank" rel="noopener noreferrer"'
        # Con JS los enlaces multimedia abren el diálogo; la nueva pestaña es
        # su alternativa. El resto anuncia el cambio de contexto sin texto extra visible.
        if not media:
            attrs += f' title="{note}"'
            content += f'<span class="visually-hidden"> ({note})</span>'
        return f'<a{attrs}>{content}</a>'

    return re.sub(r'<a\b([^>]*)>(.*?)</a>', update, html, flags=re.DOTALL)


def build(lang):
    en = lang == 'en'
    t = lambda es, eng: eng if en else es
    choose = lambda value: value[int(en)] if isinstance(value, tuple) else value
    labels = dict(zip(PAGES, LABELS[lang]))
    prefix = '../' if en else ''
    target = ROOT / 'en' if en else ROOT
    target.mkdir(exist_ok=True)
    entries = []

    def record(page, anchor, title, text, category=None):
        """Indexa una sección del idioma actual con un destino HTML local.

        plain elimina las etiquetas. La categoría por defecto es la página;
        cada tarjeta puede indicar una subcategoría. Estas entradas alimentan
        search-index.js, no una base de datos ni un servicio externo.
        """
        entries.append(dict(url=f'{page}.html' + (f'#{anchor}' if anchor else ''), title=plain(title), text=plain(text), category=category or labels[page]))

    def jump_links(items):
        return '<nav class="on-this-page" aria-label="' + t('En esta página', 'On this page') + '">' + ''.join(f'<a href="#{key}">{escape(title)}</a>' for key, title in items) + '</nav>'

    home = f'''<section class="hero" aria-labelledby="page-title">
      <div><p class="eyebrow">{t('Hola, soy Carles', 'Hi, I’m Carles')}</p>
      <h1 id="page-title">Carles<br>Valladares García<span class="accent-dot" aria-hidden="true">.</span></h1>
      <p class="hero-lead">{t('Informático, estudiante de Ingeniería Web y valenciano que prefiere un cachopo a una paella.', 'Computer science graduate, Web Engineering student and a Valencian who prefers cachopo to paella.')}</p>
      <p><span lang="ca">Benvingut/da al meu lloc!</span> {t('Además de informático, soy persona.', 'There’s more to me than computing.')}</p>
      <a class="button" href="trayectoria.html">{t('Conoce mi trayectoria', 'Explore my background')} <span aria-hidden="true">↗</span></a></div>
      <figure class="hero-photo"><img src="{prefix}img/index/ignasi-640.webp" srcset="{prefix}img/index/ignasi-400.webp 400w, {prefix}img/index/ignasi-640.webp 640w, {prefix}img/index/ignasi-817.webp 817w" sizes="(max-width: 35em) min(100vw - 4.4rem, 20.6rem), (max-width: 48em) 38vw, min(35vw, 26rem)" width="817" height="960" alt="{t('Gato naranja descansando', 'An orange cat resting')}" fetchpriority="high"></figure></section>
      <section class="explore" aria-labelledby="explore-title"><div class="section-heading"><h2 id="explore-title">{t('Por dónde empezar', 'Where to start')}</h2></div><div class="explore-grid">'''
    for i, page in enumerate(PAGES[1:5]):
        home += f'<a class="explore-link" href="{page}.html"><span class="number" aria-hidden="true">0{i+1}</span><h3>{labels[page]} <span aria-hidden="true">↗</span></h3><p>{INTRO[lang][i]}</p></a>'
    home += '</div></section>'
    record('index', 'page-title', labels['index'], home.split('<section class="explore"')[0])

    schools = [
        ('uv-title', 'uv', 'Universitat de València', t('Grado en Matemáticas', 'Degree studies in Mathematics'), t('Estudios iniciados, sin finalizar', 'Studies started, not completed'), t('Empecé mi vida universitaria en la UV, animado por mi tutor de bachillerato. Aunque dejé el grado antes de terminar segundo, valoro lo aprendido y una forma de pensar muy diferente de memorizar para un examen.', 'My university studies began at UV, encouraged by my secondary school tutor. Although I left before completing the second year, I value what I learned and a way of thinking very different from memorising for an exam.')),
        ('upv-title', 'upv', 'Universitat Politècnica de València', t('Grado en Informática', 'Degree in Computer Science'), t('Especialidad en Ingeniería del Software', 'Software Engineering specialisation'), t('Cambié los números por ceros y unos. Durante los cuatro años de carrera descubrí cómo funcionaba la «caja mágica» con la que jugaba por las tardes. Elegí Ingeniería del Software porque lo que más me interesaba era programar y construir aplicaciones.', 'Trading numbers for zeros and ones led me to computing. During four years of study, I discovered how the “magic box” I used for gaming worked. I chose Software Engineering because programming and building applications interested me most.')),
        ('uniovi-title', 'uniovi', 'Universidad de Oviedo', t('Máster en Ingeniería Web', 'Master’s in Web Engineering'), t('Formación de posgrado', 'Postgraduate studies'), t('El máster me permite seguir aprendiendo sobre el desarrollo de sitios y aplicaciones web. Estudiar fuera de mi tierra también es una oportunidad para conocer gente y vivir una experiencia diferente.', 'The master’s programme gives me the opportunity to keep learning about websites and web applications. Studying away from home is also a chance to meet people and experience something different.')),
    ]
    background = jump_links([('formacion', t('Formación', 'Education')), ('proyectos', t('Proyectos', 'Projects')), ('experiencia', t('Experiencia', 'Experience'))])
    background += f'<section aria-labelledby="formacion"><h2 id="formacion">{t("Formación académica", "Education")}</h2><div class="timeline">'
    for anchor, logo, university, degree, status, text in schools:
        # El nombre de la universidad ya aparece en texto junto al logotipo.
        background += f'<section class="education" aria-labelledby="{anchor}"><div class="university-logo"><img src="{prefix}img/trayectoria/{logo}.svg" width="160" height="112" alt="" loading="lazy"></div><div><p class="eyebrow">{university}</p><h3 id="{anchor}">{degree}</h3><p class="study-status">{status}</p><p>{text}</p></div></section>'
        record('trayectoria', anchor, degree + ' · ' + university, status + ' ' + text)
    background += '</div></section>'
    project = t('Este sitio es mi proyecto para aplicar lo aprendido en el máster y mejorar la experiencia de usuario.', 'This website is my project for applying what I have learned in the master’s programme and improving the user experience.')
    technology_note = t('HTML (lenguaje de marcado de hipertexto) organiza el contenido; CSS (hojas de estilo en cascada) define su presentación.', 'HTML (HyperText Markup Language) structures content; CSS (Cascading Style Sheets) controls how it looks.')
    background += f'<section class="panel" aria-labelledby="proyectos"><h2 id="proyectos">{t("Proyecto: mi web personal", "Project: my personal website")}</h2><p>{project}</p><ul class="tag-list" aria-label="{t("Tecnologías", "Technologies")}"><li>HTML</li><li>CSS</li><li>JavaScript</li></ul><p>{technology_note}</p><a href="https://github.com/carles-uniovi/UX">{t("Código en GitHub", "Code on GitHub")}</a></section>'
    # Datos laborales facilitados por el autor. No se deducen cargos ni funciones.
    jobs = [
        ('medicarama', 'Medicarama', '2025', t('Prácticas de empresa', 'Company internship'), t('En 2025 realicé prácticas de empresa en Medicarama.', 'In 2025, I completed a company internship at Medicarama.')),
        ('v2c', 'V2c', '2026', t('Experiencia laboral', 'Work experience'), t('En 2026 trabajé en V2c.', 'In 2026, I worked at V2c.')),
    ]
    background += f'<section aria-labelledby="experiencia"><h2 id="experiencia">{t("Experiencia laboral", "Work experience")}</h2><div class="contact-grid">'
    for anchor, company, year, role, text in jobs:
        background += f'<article class="panel" aria-labelledby="{anchor}"><p class="eyebrow"><time datetime="{year}">{year}</time></p><h3 id="{anchor}">{company}</h3><p class="study-status">{role}</p></article>'
        record('trayectoria', anchor, company + ' · ' + role, text)
    background += f'</div><a href="contacto.html#referencias">{t("Ver persona de referencia", "View my personal reference")} <span aria-hidden="true">↗</span></a></section>'
    record('trayectoria', 'proyectos', t('Proyecto: mi web personal', 'Project: my personal website'), project + ' ' + technology_note + ' HTML CSS JavaScript')

    def categories(page, groups, image_dir):
        content = jump_links([(key, t('Rol', 'Role-playing') if key == 'dnd' else choose(name)) for key, name, _ in groups])
        for key, group_title, cards in groups:
            content += f'<section class="category" aria-labelledby="{key}"><div class="section-heading"><h2 id="{key}">{escape(choose(group_title))}</h2></div><div class="cards">'
            for item in cards:
                anchor, title, image, text, *media = item
                title, text = choose(title), choose(text)
                # La ilustración es decorativa: título y descripción contienen
                # la información de la tarjeta, sin lectura duplicada del nombre.
                content += f'<article class="card" aria-labelledby="{anchor}"><img class="card-image" src="{prefix}img/{image_dir}/{escape(image)}" alt="" width="480" height="320" loading="lazy" decoding="async"><div class="card-body"><h3 id="{anchor}">{escape(title)}</h3><p>{escape(text)}</p>'
                extra = ''
                if media:
                    source, media_title = media
                    media_title = choose(media_title)
                    youtube = source.startswith('https://www.youtube.com/watch?v=')
                    video = youtube or source.endswith('.mp4')
                    # Identifica cada destino incluso fuera del contexto de la
                    # tarjeta (listado de enlaces de un lector de pantalla).
                    play_label = t('Ver tráiler: ', 'Watch trailer: ') + title if video else t('Escuchar: ', 'Listen to: ') + media_title
                    # El enlace funciona por sí solo. JS lo mejora con un diálogo;
                    # el reproductor no ocupa espacio dentro de la tarjeta.
                    href = source if youtube else prefix + 'docs/media/' + quote(source)
                    youtube_attr = f' data-youtube-id="{escape(source.split("v=", 1)[1])}"' if youtube else ''
                    content += f'<a class="media-trigger" href="{escape(href)}" data-media-type="{"youtube" if youtube else "video" if video else "audio"}"{youtube_attr} data-media-title="{escape(title + " · " + media_title)}">{icon("play")}<span>{escape(play_label)}</span></a>'
                    extra = media_title
                content += '</div></article>'
                record(page, anchor, title, text + ' ' + extra, labels[page] + ' / ' + choose(group_title))
            content += '</div></section>'
        return content

    hobbies = categories('hobbies', HOBBIES, 'hobbies')
    interests = categories('intereses', INTERESTS, 'intereses')
    contact = '<p class="contact-intro">' + t('Puedes escribirme al correo personal o al universitario. Pulsa la dirección para abrir tu aplicación de correo, o usa el botón para copiarla.', 'You can contact me at my personal or university email address. Select an address to open your email app, or use its button to copy it.') + '</p><div class="contact-grid">'
    for key, title, email, profile in [('personal', t('Personal', 'Personal'), 'carlesvallgar@gmail.com', 'CarlesVall'), ('universidad', t('Universidad', 'University'), 'UO319242@uniovi.es', 'carles-uniovi')]:
        email_label = t('Correo personal', 'Personal email') if key == 'personal' else t('Correo universitario', 'University email')
        github_label = t('GitHub personal', 'Personal GitHub') if key == 'personal' else t('GitHub de la Universidad', 'University GitHub')
        contact += f'<section class="panel" aria-labelledby="{key}"><h2 id="{key}">{title}</h2><a class="contact-link" href="mailto:{email}"><span>{email_label}</span><strong id="email-{key}">{email}</strong></a><button hidden class="copy-email secondary" type="button" data-email="{email}" data-copy-target="email-{key}" data-status="copy-status-{key}">{t("Copiar correo personal", "Copy personal email") if key == "personal" else t("Copiar correo universitario", "Copy university email")}</button><p class="copy-status" id="copy-status-{key}" role="status" aria-live="polite"></p><a class="contact-link" href="https://github.com/{profile}"><span>{github_label}</span><strong>@{profile}</strong></a>'
        if key == 'personal':
            contact += f'<a class="contact-link" id="linkedin" href="{LINKEDIN_URL}"><span>LinkedIn</span><strong>Carles Valladares García</strong></a>'
        contact += '</section>'
        record('contacto', key, title + ' · ' + email_label + ' · ' + github_label, email + ' ' + profile)
    record('contacto', 'linkedin', 'LinkedIn · Carles Valladares García', t('Perfil profesional de Carles Valladares García en LinkedIn.', 'Carles Valladares García’s professional profile on LinkedIn.'))
    reference_text = t('Perfil de LinkedIn de un colega como referencia personal.', 'A colleague’s LinkedIn profile as a personal reference.')
    contact += f'</div><section class="callout" aria-labelledby="referencias"><h2 id="referencias">{t("Referencia personal", "Personal reference")}</h2><a href="{REFERENCE_URL}">{t("LinkedIn de mi colega", "My colleague’s LinkedIn")}</a></section>'
    record('contacto', 'referencias', t('Persona de referencia · LinkedIn', 'Personal reference · LinkedIn'), reference_text)

    faqs = [
        ('encontrar', t('¿Cómo encuentro un contenido?', 'How do I find something?'), t('Usa el menú, el mapa del sitio o el buscador de la cabecera. En Aficiones e Intereses, los enlaces bajo el título llevan a cada categoría.', 'Use the menu, site map or search in the header. In Hobbies and Interests, the links below the title jump to each category.')),
        ('buscador', t('¿Cómo funciona el buscador?', 'How does search work?'), t('Escribe una o varias palabras, por ejemplo «judo», «Robe» o «Ingeniería Web». No distingue entre mayúsculas, minúsculas y tildes. Con varias palabras busca contenidos que incluyan todas ellas. Los resultados muestran la sección y un enlace al contenido. Si no encuentras nada, prueba con menos palabras, elige un ejemplo o consulta el mapa. Limpiar borra la consulta y permite empezar de nuevo.', 'Type one or more words, such as “judo”, “Robe” or “Web Engineering”. Search ignores case and accents. With multiple words, it looks for content containing all of them. Results show the section and a link to the content. If nothing matches, try fewer words, choose an example or use the site map. Clear removes the query so you can start again.')),
        ('teclado', t('¿Puedo usar solo el teclado?', 'Can I use only the keyboard?'), t('Pulsa Tab para avanzar y Mayús + Tab para retroceder. El primer enlace permite saltar al contenido. Enter activa enlaces y botones; Espacio también activa botones y despliega las preguntas. En móvil, el botón Menú abre la navegación y Escape la cierra. Los reproductores tienen sus propios controles de teclado.', 'Press Tab to move forward and Shift + Tab to move back. The first link skips to the content. Enter activates links and buttons; Space also activates buttons and opens questions. On mobile, the Menu button opens navigation and Escape closes it. Media players have their own keyboard controls.')),
        ('lectura', t('¿Cómo leo sin imágenes ni distracciones?', 'How do I read without images or distractions?'), t('La versión de lectura reúne el contenido personal de las cinco secciones en una página, con índice y enlaces de texto. También puedes imprimirla. La navegación y el contenido siguen disponibles si desactivas CSS, imágenes o JavaScript.', 'The reading version brings together the personal content from all five sections on one page, with a contents list and text links. You can also print it. Navigation and content remain available if you disable CSS, images or JavaScript.')),
        ('idioma', t('¿Cómo cambio el idioma o el tema?', 'How do I change the language or theme?'), t('EN (inglés) y ES (español) cambian al otro idioma en la página actual. El botón «Activar modo oscuro/claro» alterna los temas y recuerda tu elección. Puedes ampliar el texto con el zoom del navegador.', 'EN (English) and ES (Spanish) switch to the other language on the current page. The theme button enables dark or light mode and remembers your choice. You can enlarge the text with browser zoom.')),
        ('multimedia', t('¿Cómo escucho música o veo los vídeos?', 'How do I listen to music or watch videos?'), t('En Intereses, pulsa «Escuchar» o «Ver». Cierra el reproductor con la cruz o Escape para detenerlo. Los tráileres usan YouTube: sus controles ofrecen los subtítulos y pistas de audio disponibles para cada vídeo. También puedes abrirlos con «Ver en YouTube».', 'In Interests, select “Listen to” or “Watch”. Close the player with the cross or Escape to stop it. Trailers use YouTube: its controls provide the captions and audio tracks available for each video. You can also open them with “Watch on YouTube”.')),
        ('problemas', t('¿Algo no funciona?', 'Is something not working?'), t('Si el buscador indica que necesita JavaScript, usa el mapa o la versión de lectura. Si no se abre el correo, copia la dirección y pégala en tu aplicación de email. Para comunicar un problema, indica qué página estabas consultando y qué intentabas hacer.', 'If search says it needs JavaScript, use the site map or reading version. To save an address, use the copy button in its section. Confirmation appears beside that button. If automatic copying is unavailable, select the address and copy it manually. To report a problem, say which page you were on and what you were trying to do.')),
    ]
    help_content = '<div class="help-layout"><section class="faq" aria-label="' + t('Preguntas frecuentes', 'Frequently asked questions') + '">'
    for key, title, text in faqs:
        help_content += f'<details id="{key}"><summary>{title}</summary><p>{text}</p></details>'
        record('ayuda', key, title, text)
    help_content += f'</section><aside class="panel"><h2>{t("Accesos útiles", "Useful links")}</h2><ul class="text-links"><li><a href="mapa.html">{labels["mapa"]}</a></li><li><a href="lectura.html">{labels["lectura"]}</a></li><li><a href="contacto.html">{t("Comunicar un problema", "Report a problem")}</a></li></ul></aside></div>'

    sitemap = '<div class="sitemap-grid">'
    for page in PAGES[:6]:
        sitemap += f'<section class="panel"><h2><a href="{page}.html">{labels[page]}</a></h2><ul class="text-links">'
        for entry in entries:
            if entry['url'].startswith(page + '.html#'):
                sitemap += f'<li><a href="{entry["url"]}">{escape(entry["title"])}</a></li>'
        sitemap += '</ul></section>'
    sitemap += '</div><p><a href="buscar.html">' + t('Buscar en todo el sitio', 'Search the whole site') + '</a> · <a href="lectura.html">' + labels['lectura'] + '</a></p>'

    search = f'''<form class="search-form search-large" action="buscar.html" method="get" role="search" aria-label="{t('Buscar contenido', 'Search content')}"><label for="query">{t('¿Qué te gustaría encontrar?', 'What would you like to find?')}</label><div><input id="query" type="search" enterkeyhint="search" autocomplete="off" name="q" maxlength="160" aria-describedby="search-hint" placeholder="{t('Por ejemplo: judo, Robe, Ingeniería Web', 'For example: judo, Robe, Web Engineering')}"><button type="submit">{labels['buscar']}</button><button class="secondary search-clear" type="button" hidden>{t("Limpiar", "Clear")}</button></div></form><p id="search-hint">{t('Busca por palabras, con o sin tildes. Puedes combinar varias.', 'Search for words, with or without accents. You can combine several.')}</p><noscript><p class="callout">{t('El buscador necesita JavaScript. Puedes encontrar todo el contenido en el', 'Search needs JavaScript. You can find all content in the')} <a href="mapa.html">{labels['mapa']}</a> {t('o en la', 'or the')} <a href="lectura.html">{labels['lectura'].lower()}</a>.</p></noscript><p id="search-status" tabindex="-1" role="status" aria-live="polite" aria-atomic="true"></p><div id="search-results" hidden></div><div id="search-empty" hidden><p>{t('Prueba con una palabra más general o revisa la escritura.', 'Try a more general word or check the spelling.')}</p><a href="mapa.html">{labels['mapa']}</a></div>'''
    examples = [('judo', 'Judo'), (t('musica', 'music'), t('Música', 'Music')), (t('correo', 'email'), t('Buscar correo', 'Find email'))]
    search += '<nav class="search-examples" aria-label="' + t('Ideas para buscar', 'Search ideas') + '"><span>' + t('Prueba con:', 'Try:') + '</span>' + ''.join(f'<a href="buscar.html?q={quote(query)}">{label}</a>' for query, label in examples) + '</nav>'
    content = {'index': home, 'trayectoria': background, 'hobbies': hobbies, 'intereses': interests, 'contacto': contact, 'ayuda': help_content, 'mapa': sitemap, 'buscar': search}

    # Una alternativa de lectura realmente navegable, sin depender de cómo cada
    # navegador extraiga su modo lector. Reutiliza el texto del contenido canónico.
    from html.parser import HTMLParser

    class ReadingParser(HTMLParser):
        def __init__(self, page):
            super().__init__()
            self.page, self.output, self.skip = page, [], 0
            self.spans = []

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag in ('nav', 'figure', 'details', 'button', 'script'):
                self.skip += 1
            if self.skip or tag == 'img':
                return
            if tag == 'br':
                self.output.append(' ')
            elif tag == 'span':
                language = attrs.get('lang')
                self.spans.append(bool(language))
                if language:
                    self.output.append(f'<span lang="{escape(language)}">')
            if tag in ('h1', 'h2', 'h3'):
                self.output.append('<' + ('h3' if tag != 'h3' else 'h4') + '>')
            elif tag == 'strong':
                self.output.append(': <strong>')
            elif tag in ('p', 'ul', 'li', 'strong', 'small'):
                self.output.append('<' + tag + '>')
            elif tag == 'a':
                href = attrs.get('href', '')
                if href.startswith('#'):
                    href = self.page + '.html' + href
                contact_class = ' class="reading-contact"' if 'contact-link' in attrs.get('class', '').split() else ''
                self.output.append(f'<a href="{escape(href)}"{contact_class}>')

        def handle_endtag(self, tag):
            if tag in ('nav', 'figure', 'details', 'button', 'script') and self.skip:
                self.skip -= 1
                return
            if self.skip:
                return
            if tag == 'span' and self.spans:
                if self.spans.pop():
                    self.output.append('</span>')
            if tag in ('h1', 'h2', 'h3'):
                self.output.append('</' + ('h3' if tag != 'h3' else 'h4') + '>')
            elif tag in ('p', 'ul', 'li', 'a', 'strong', 'small'):
                self.output.append('</' + tag + '>' + (' ' if tag == 'a' else ''))

        def handle_data(self, data):
            if not self.skip:
                self.output.append(escape(data))

    reading = '<div class="reading">'
    reading += jump_links([(f'leer-{page}', t('Leer: ', 'Read: ') + labels[page]) for page in PAGES[:5]])
    for page in PAGES[:5]:
        parser = ReadingParser(page)
        # Se omiten los accesos de la portada porque el índice de lectura ya los cubre.
        parser.feed(content[page].split('<section class="explore"')[0] if page == 'index' else content[page])
        reading += f'<section aria-labelledby="leer-{page}"><h2 id="leer-{page}">{labels[page]}</h2>' + ''.join(parser.output) + f'<p><a href="{page}.html">{t("Abrir página", "Open page")}: {labels[page]}</a> · <a href="#page-title">{t("Volver al índice", "Back to contents")}</a></p></section>'
    reading += '</div>'
    content['lectura'] = reading

    descriptions = {page: labels[page] + ' · Carles Valladares García.' for page in PAGES}
    descriptions.update({'index': t('Conoce a Carles Valladares García: formación, aficiones, intereses y contacto.', 'Meet Carles Valladares García: education, hobbies, interests and contact.'), 'trayectoria': INTRO[lang][0], 'hobbies': INTRO[lang][1], 'intereses': INTRO[lang][2], 'contacto': INTRO[lang][3]})

    for page in PAGES:
        path = f'{page}.html'
        alternate = ('../' if en else 'en/') + path
        title = 'Carles Valladares García' if page == 'index' else labels[page] + ' · Carles Valladares García'
        nav = ''.join(f'<a href="{key}.html"' + (' aria-current="page"' if key == page else '') + f'>{labels[key]}</a>' for key in PAGES[:5])
        footer_links = ''.join(f'<a href="{key}.html"' + (' aria-current="page"' if key == page else '') + f'>{t("Lectura", "Reading") if key == "lectura" else labels[key]}</a>' for key in ('ayuda', 'mapa', 'lectura'))
        breadcrumb = '' if page == 'index' else f'<nav class="breadcrumbs" aria-label="{t("Ruta de navegación", "Breadcrumb")} "><ol><li><a href="index.html">{t("Inicio", "Home")}</a></li><li aria-current="page">{labels[page]}</li></ol></nav>'
        page_heading = '' if page == 'index' else f'<div class="page-heading"><h1 id="page-title">{labels[page]}</h1></div>'
        media_dialog = ''
        if page == 'intereses':
            media_dialog = f'<dialog class="media-dialog" id="media-player" aria-labelledby="media-title"><div class="dialog-header"><h2 id="media-title">{t("Reproductor", "Media player")}</h2><button class="icon-control dialog-close" type="button" aria-label="{t("Cerrar reproductor", "Close player")}" title="{t("Cerrar", "Close")}">{icon("close")}</button></div><div id="media-stage"></div><p id="media-status" role="status" aria-live="polite"></p><a id="media-direct" hidden>{t("Abrir archivo", "Open file")}</a></dialog>'
        # Solo el buscador carga índice, motor e interfaz; defer conserva este
        # orden y espera al DOM. El script local también funciona con file://.
        search_scripts = f'<script src="{prefix}js/search-index.js" defer></script><script src="{prefix}js/search-core.js" defer></script><script src="{prefix}js/search.js" defer></script>' if page == 'buscar' else ''
        html = f'''<!doctype html>
<html lang="{lang}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{escape(descriptions[page])}"><title>{escape(title)}</title>
<link rel="canonical" href="{PUBLIC_URL}{'en/' if en else ''}{path}"><link rel="alternate" hreflang="es" href="{PUBLIC_URL}{path}"><link rel="alternate" hreflang="en" href="{PUBLIC_URL}en/{path}"><link rel="icon" href="{prefix}img/favicon.svg" type="image/svg+xml">
<script src="{prefix}js/theme.js"></script><script src="{prefix}js/site.js" defer></script>{search_scripts}<link rel="stylesheet" href="{prefix}css/styles.css"></head>
<body><a class="skip-link" href="#contenido">{t('Saltar al contenido', 'Skip to content')}</a>
<header class="site-header"><div class="header-inner"><a class="brand" href="index.html"><span class="monogram" aria-hidden="true">cv<span>.</span></span><span>Carles<span class="brand-surname"> Valladares</span><span class="visually-hidden"> · {t("Inicio", "Home")}</span></span></a><div class="navigation" id="navigation"><nav class="primary-nav" aria-label="{t('Navegación principal', 'Main navigation')}">{nav}</nav></div><div class="header-tools"><a class="icon-control labeled-control" href="buscar.html">{icon('search')}<span>{labels['buscar']}</span></a><a class="language-switch" href="{alternate}" lang="{'es' if en else 'en'}" hreflang="{'es' if en else 'en'}" aria-label="{'ES: Español' if en else 'EN: English'}" title="{'Español' if en else 'English'}">{'ES' if en else 'EN'}</a><button class="theme-toggle icon-control" type="button" aria-pressed="false" title="{t('Activar modo oscuro', 'Enable dark mode')}" hidden><span aria-hidden="true">◐</span><span class="visually-hidden">{t('Modo oscuro', 'Dark mode')}</span></button><button class="menu-toggle icon-control labeled-control" type="button" aria-expanded="true" aria-controls="navigation" aria-label="{t('Menú', 'Menu')}" hidden>{icon('menu')}<span>{t("Menú", "Menu")}</span></button></div></div></header>
<main id="contenido" tabindex="-1">{breadcrumb}{page_heading}{content[page]}{media_dialog}</main>
<footer class="site-footer"><div><strong>Carles Valladares García</strong><p class="updated">{t('Actualizado:', 'Updated:')} <time datetime="{DATE}">{t('20 de noviembre de 2026', '20 November 2026')}</time></p></div><nav aria-label="{t('Ayuda y accesibilidad', 'Help and accessibility')}">{footer_links}</nav></footer></body></html>
'''
        clean_html = '\n'.join(line.rstrip() for line in external_links(html, en).splitlines()) + '\n'
        (target / path).write_text(clean_html, encoding='utf-8', newline='\n')
    return entries


def main():
    # Se copian recursos utilizados; no se heredan borradores, documentación o
    # páginas de prueba de la V1. Los originales nunca se modifican.
    assets = ['img/index/ignasi.png']
    assets += [f'img/trayectoria/{name}.svg' for name in ('uv', 'upv', 'uniovi')]
    for directory, groups in [('hobbies', HOBBIES), ('intereses', INTERESTS)]:
        assets += [f'img/{directory}/{item[2]}' for _, _, cards in groups for item in cards]
    assets += [f'docs/media/{item[4]}' for _, _, cards in INTERESTS for item in cards if len(item) > 4 and not item[4].startswith('https://')]
    for asset in assets:
        destination = ROOT / asset
        destination.parent.mkdir(parents=True, exist_ok=True)
        # Conserva las copias ya optimizadas; para reimportar un recurso, elimina
        # únicamente su copia de V3 antes de ejecutar este generador.
        if not destination.exists():
            shutil.copy2(SOURCE / asset, destination)
    for width in (400, 640, 817):
        optimized = ROOT / f'img/index/ignasi-{width}.webp'
        if not optimized.exists():
            raise FileNotFoundError(f'Falta {optimized.name}. Ejecuta scripts/optimize-images.py (requiere Pillow).')
    (ROOT / 'img/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#5924a6"/><text x="9" y="43" font-family="sans-serif" font-size="34" font-weight="700" fill="white">cv</text></svg>', encoding='utf-8')
    indexes = {lang: build(lang) for lang in ('es', 'en')}
    (ROOT / 'js/search-index.js').write_text('// Generado con scripts/build.py. No editar a mano.\nwindow.SEARCH_INDEX = ' + json.dumps(indexes, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')
    print(f'Generadas 18 páginas y {sum(map(len, indexes.values()))} entradas de búsqueda.')


if __name__ == '__main__':
    main()
