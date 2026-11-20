"""Crea el capítulo de accesibilidad y su PDF a partir de evidencias conservadas.

Requiere ReportLab y Pillow solo para el documento. --draft permite revisar la
maquetación mientras una repetición externa sigue pendiente; no entrega un PDF
final hasta que los 54 análisis finales tengan cero errores automáticos.
"""
from collections import Counter
from datetime import datetime, timezone
from html import escape
from pathlib import Path
import argparse
import json
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, KeepTogether, LongTable, PageBreak,
                               Paragraph, SimpleDocTemplate, Spacer, TableStyle)

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
EVIDENCE = ROOT / 'docs/accesibilidad'
LABELS = {'index': 'Inicio', 'trayectoria': 'Trayectoria', 'hobbies': 'Aficiones',
          'intereses': 'Intereses', 'contacto': 'Contacto', 'ayuda': 'Ayuda',
          'mapa': 'Mapa', 'buscar': 'Buscador', 'lectura': 'Lectura'}
ORDER = [lang + '-' + name for name in LABELS for lang in ('es', 'en')]
ACCENT = colors.HexColor('#5924a6')
INK = colors.HexColor('#272134')
SOFT = colors.HexColor('#eee8f8')


def ac_assessment(title):
    if title.startswith('Sound file'):
        return 'Problema confirmado', 'Falta alternativa textual de los tres MP3. El mismo recurso aparece en Intereses y Lectura; las 12 ocurrencias no son 12 canciones.'
    if 'irreversable transaction' in title or 'delete information' in title:
        return 'No aplica', 'El buscador no realiza transacciones ni modifica registros: consulta texto y conserva q en la URL.'
    if 'All required' in title:
        return 'No aplica', 'No se exige un campo obligatorio para buscar. La consulta vacía tiene orientación y alternativas.'
    if 'Form submission error' in title:
        return 'Comprobado', 'Se revisaron consulta vacía, sin coincidencias y recuperación. Se identifica el estado y se ofrecen ejemplos y mapa.'
    if 'Tab order' in title:
        return 'Comprobado', 'El resumen recibe foco al enviar y el siguiente Tab llega al primer resultado. No hay tabindex positivo.'
    if title.startswith('<input>'):
        return 'Comprobado', 'Consulta y estados se comunican con texto; no dependen solo de un cambio de color.'
    if title.startswith('<label>'):
        return 'Comprobado', 'La pregunta visible está asociada a query mediante for; aria-describedby enlaza la ayuda.'
    if title.startswith('<script>'):
        return 'Comprobado', 'Se verificaron teclado, foco, mensajes y ausencia de reproducción o movimiento automático en la interfaz propia.'
    if title.startswith('Visual lists'):
        return 'Corregido / revisado', 'Las listas de enlaces conservan marcado. La lista de resultados se crea solo cuando hay coincidencias; el aviso H48 de prosa se contrastó aparte.'
    if title.startswith('Unicode') or title.startswith('<dir>'):
        return 'No aplica', 'El contenido funcional ES/EN usa escritura de izquierda a derecha; no se detectaron pasajes bidireccionales que requieran cambios.'
    if title.startswith('Text may refer'):
        return 'Comprobado', 'Los controles se identifican por nombre o función; el teclado ofrece alternativas a las referencias visuales.'
    if 'skip to content' in title:
        return 'Comprobado', 'Existe un primer enlace Saltar al contenido y se comprobó el foco en main#contenido.'
    if title.startswith('Groups of links'):
        return 'Comprobado', 'Navegaciones con nombre, índices y listas permiten interpretar los grupos por su estructura y propósito.'
    if "document's primary language" in title:
        return 'Comprobado', 'Se revisaron lang ES/EN, saludo ca y nombres propios. Los nombres de obras no se tratan como párrafos sin marcar.'
    if title.startswith('Site missing'):
        return 'Comprobado', 'El mapa existe y se enlaza en el pie de las 18 páginas; los destinos se verifican localmente y en navegador.'
    if title.startswith('Repeated components'):
        return 'Comprobado', 'La plantilla conserva orden y posición relativos de navegación y pie en los dos idiomas.'
    if title.startswith('Long quotations'):
        return 'No aplica', 'No se identifican bloques de citas extensas usados como texto del perfil; títulos de obras y nombres no son citas en bloque.'
    if title.startswith('Link text'):
        return 'Corregido / revisado', 'Tráileres, saltos Leer y ejemplo Buscar correo ya distinguen sus destinos. Se inspeccionaron el propósito y el contexto de los restantes enlaces.'
    if title.startswith('<h') and 'formatting' in title:
        return 'Comprobado', 'Un h1 por página; h2/h3 organizan categorías y tarjetas; Lectura utiliza también h4. Se revisaron jerarquía y significado.'
    if title.startswith('<title>'):
        return 'Comprobado', 'Los títulos identifican al autor y la sección; su contenido e idioma coinciden con cada página.'
    if title.startswith('Alt text is not empty'):
        return 'Comprobado', 'Corresponde a la foto del gato en portada: se mantiene una alternativa informativa, sin presentarla como fotografía del autor.'
    if title.startswith('<img>') or title.startswith('Alt text does not') or title.startswith('Image may'):
        return 'Comprobado', 'Se inspeccionaron imágenes y texto adyacente. Ilustraciones y logotipos son decorativos para la tarea; la información del perfil permanece en HTML.'
    raise ValueError('Falta estudiar el aviso de AChecker: ' + title)


TAW_ASSESSMENTS = {
    '1.1.1': 'Se revisaron propósito, alternativas y redundancia: foto del gato informativa; ilustraciones y logotipos con alt vacío y contenido equivalente en texto adyacente.',
    '2.4.2': 'Se comprobaron los 18 títulos y su correspondencia con sección, autor e idioma. TAW no puede decidir por sí solo si describen bien el contenido.',
    '2.4.6': 'Se revisaron jerarquía y significado de encabezados y etiquetas, además de su asociación con campos y regiones. No se usan solo para aumentar el tamaño.',
    '3.2.5': 'Los cambios de página, pestaña o diálogo requieren activación del usuario. Los enlaces externos avisan de la nueva pestaña y el cierre del diálogo restaura el foco.',
    '3.3.1': 'El buscador admite consulta vacía, identifica la ausencia de coincidencias y anuncia el resultado con texto. No se exige un dato obligatorio sin explicación.',
    '3.3.3': 'Para recuperar una búsqueda se ofrecen palabra más general, revisión de escritura, ejemplos, Limpiar y mapa. Se verificó una consulta sin coincidencias.',
    '3.3.4': 'No hay operaciones legales, financieras ni cambios de registros. Las consultas GET y la copia de una dirección no son una transacción irreversible de la aplicación.',
    '3.3.5': 'Campo con etiqueta y ayuda asociada; ejemplos próximos, mensajes de estado y preguntas de ayuda contextual para búsqueda y copia.',
    '3.3.6': 'No hay altas, borrados o envíos de datos de aplicación que necesiten confirmación. El sitio no envía mensajes al pulsar Copiar ni ejecuta transacciones.'
}


def clean(value):
    return str(value).replace('\u2011', '-').replace('\u2013', '-').replace('\u2014', '-')


def inline(value):
    value = escape(clean(value))
    value = re.sub(r'\[([^]]+)\]\((https?://[^)]+)\)', r'<link href="\2" color="#5924a6">\1</link>', value)
    value = re.sub(r'`([^`]+)`', r'<font name="Courier">\1</font>', value)
    return re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', value).replace('\n', '<br/>')


def build_blocks(results, manual, clear):
    initial = [r for r in results if r['phase'] == 'inicial']
    final = [r for r in results if r['phase'] == 'final']
    by = {(r['phase'], r['page'], r['tool']): r for r in results}
    blocks = []

    def heading(text, level=2): blocks.append({'type': 'heading', 'text': text, 'level': level})
    def p(text): blocks.append({'type': 'p', 'text': text})
    def table(headers, rows, widths=None): blocks.append({'type': 'table', 'headers': headers, 'rows': rows, 'widths': widths})
    def bullet(text): blocks.append({'type': 'bullet', 'text': text})
    def page(): blocks.append({'type': 'page'})

    heading('Accesibilidad de la web personal V3', 1)
    p('Carles Valladares García - UO319242\nExperiencia de Usuario - Máster en Ingeniería Web\nFecha de revisión: 20 de noviembre de 2026')
    p('**Estado: ' + ('verificación automática final completada.' if clear else 'BORRADOR; repetición TAW pendiente por límite de servicio.') + '**')
    p(('Las 18 páginas se han comprobado con TAW, AChecker y WAVE: 54 análisis finales con cero errores automáticos, incluido el contraste de WAVE. ' if clear else
       'Se conservan 54 capturas de comprobación. La última repetición de Lectura inglesa aún no acredita cero en TAW y debe cerrarse antes de entregar el informe final. ') +
      'La inspección manual identifica límites de accesibilidad multimedia: los tres MP3 no tienen alternativa textual equivalente y no se acreditan todas las alternativas de los tráileres. Por ello **no se declara conformidad WCAG AAA**.')
    if not clear:
        p('**Pendiente de cierre:** repetir TAW después de los últimos ajustes en Inicio ES/EN, Trayectoria ES/EN, Aficiones EN, Ayuda ES/EN y Lectura ES/EN. Los cambios de estas nueve páginas ya se comprobaron con AChecker y WAVE sin errores. Los ceros anteriores de TAW conservan su fecha y no se presentan como una nueva ejecución sobre esos ajustes. La última captura válida de Lectura EN contiene una incidencia anterior a su última corrección.')
    heading('Alcance y método')
    p('Se evaluó la dirección pública [Web personal V3](https://carles-uniovi.github.io/UX/v3/), con nueve páginas en español y sus nueve equivalentes en inglés. Se guardaron resúmenes, filas por criterio, advertencias y capturas antes y después de corregir. Los resultados se mantienen por herramienta: sus reglas y categorías son distintas.')
    table(['Herramienta', 'Configuración y alcance'], [
        ['TAW', 'Opción WCAG 2.1 AAA. El resumen devuelto contiene 61 filas de criterios y 30 no verificados por página. Se conservan sus problemas y advertencias; el resumen declara tecnologías HTML/CSS.'],
        ['AChecker', 'AChecker+ de ACHECKS, opción WCAG 2.0 AAA Markup. Se revisan errores conocidos y advertencias del marcado.'],
        ['WAVE', 'Servicio web con estilos activos. Se separan errores, errores de contraste y alertas; no ofrece un selector que certifique AAA.']
    ], [28, 146])
    p('Las capturas registran fecha UTC. Se respetaron los límites gratuitos de TAW (intervalo de 20 segundos y 10 peticiones por hora); los mensajes de límite se guardaron y no se contaron como análisis sin problemas. El detalle H48 se solicitó por correo con autorización del autor y se incorporó el apartado que facilitó.')
    p('Se comprobó por HTTP que los 18 HTML y cuatro recursos CSS/JavaScript publicados coinciden con las fuentes revisadas, normalizando solo los saltos CRLF/LF. El registro de URL, fecha y hashes está en `manual/fuentes-publicadas.json`. Los resultados de cada herramienta tienen su propia fecha de captura.')
    p('La revisión manual combina inspección del contenido, código y árbol accesible con recorridos de teclado y mediciones de apoyo en Chrome. No es una nueva tanda con participantes ni una evaluación realizada por personas con discapacidad o con un lector de pantalla específico.')

    page(); heading('Resultados por herramienta y página')
    summary = []
    for tool in ('TAW', 'AChecker', 'WAVE'):
        before, after = [r for r in initial if r['tool'] == tool], [r for r in final if r['tool'] == tool]
        error0 = sum(r['errors'] + r.get('contrastErrors', 0) for r in before)
        error1 = sum(r['errors'] + r.get('contrastErrors', 0) for r in after)
        warn0 = sum(r.get('warnings', r.get('alerts', 0)) for r in before)
        warn1 = sum(r.get('warnings', r.get('alerts', 0)) for r in after)
        summary.append([tool, str(error0), str(error1), f'{warn0} / {warn1}'])
    table(['Herramienta', 'Errores iniciales', 'Errores finales', 'Avisos inicial / final'], summary, [32, 37, 37, 68])
    p('Los recuentos son **ocurrencias por página**, no defectos únicos. Por ejemplo, una misma canción aparece en Intereses y Lectura y en ambos idiomas. Los 30 no verificados de TAW representan criterios repetidos en cada página, no 540 problemas confirmados.')
    rows = []
    for key in ORDER:
        lang, name = key.split('-', 1)
        ti, tf = by['inicial', key, 'TAW'], by['final', key, 'TAW']
        ai, af = by['inicial', key, 'AChecker'], by['final', key, 'AChecker']
        wi, wf = by['inicial', key, 'WAVE'], by['final', key, 'WAVE']
        rows.append([lang.upper() + ' ' + LABELS[name], f"{ti['errors']} / {tf['errors']}", str(tf['warnings']),
                     str(af['errors']), f"{ai['warnings']} / {af['warnings']}", f"{wf['errors']} / {wf['contrastErrors']}", f"{wi['alerts']} / {wf['alerts']}"])
    table(['Página', 'TAW errores\ninicial / final', 'TAW avisos\nfinal', 'AC errores\nfinal', 'AC avisos\ninicial / final', 'WAVE error /\ncontraste final', 'WAVE alertas\ninicial / final'], rows, [34, 24, 20, 18, 26, 27, 25])
    p('En todas las páginas TAW mantiene 30 criterios no verificados, estudiados en el apartado de revisión manual. Datos completos, fechas y archivos de origen: `docs/accesibilidad/resultados.json` y `resultados.csv`.')

    page(); heading('Problemas corregidos y falsos positivos')
    table(['Hallazgo', 'Decisión y verificación'], [
        ['Enlaces indistinguibles (2.4.9)', 'Los dos tráileres incluyen la película en el texto. Los saltos Leer se distinguen de la navegación general y Buscar correo se distingue de Contacto. Se comprobaron destinos y nombres en ambos idiomas.'],
        ['Lista vacía del buscador (1.3.1)', 'El contenedor inicial ya no presenta una lista sin resultados. La lista ordenada se crea al obtener coincidencias y se retira al vaciar o no encontrar.'],
        ['Prosa inglesa interpretada como lista (H48)', 'El detalle TAW indicaba simulación de lista ordenada mediante párrafos. Las descripciones son relatos independientes, sin una secuencia de pasos. Se mantienen sus encabezados y párrafos y se reformulan los inicios con I. La posible lectura de I como numeración romana es una inferencia; no se atribuye a un acceso al código interno de TAW.'],
        ['Idioma de Contacto ES (3.1.1)', 'La página ya tenía lang=es. Se verificó el contenido real y se añadieron instrucciones claras de correo en ambos idiomas. La nueva prueba devuelve cero sin alterar el idioma correcto.'],
        ['Lectura duplicada de imágenes y controles', 'Los títulos ya identifican tarjetas y universidades: sus ilustraciones y logotipos se marcan como decorativos. Se retiran títulos redundantes de Buscar/Menú; la foto conserva alternativa informativa.'],
        ['Líneas de lectura demasiado largas (1.4.8)', 'La medida real detectó máximos de 89 y 87 caracteres. El ancho pasa a 60ch y los máximos medidos son 75 y 73, con interlineado y espaciado comprobados.'],
        ['Abreviaturas e instrucciones', 'Se desarrollan HTML y CSS en el contenido de proyecto/lectura, se explican EN/ES en Ayuda y el tema se identifica por su función, sin depender solo de la forma circular.']
    ], [45, 129])
    p('La técnica [H48 del W3C](https://www.w3.org/WAI/WCAG21/Techniques/html/H48) se aplica cuando el contenido representa una lista. Convertir estas descripciones en pasos numerados habría introducido una relación que no tienen. Se conserva el detalle recibido en `manual/detalle-h48-taw.txt` y los informes originales para contrastarlo.')
    p('Después de cada cambio pertinente se repitieron las páginas afectadas. Las mediciones de apoyo comprueban 21 casos del buscador, 18 casos de interfaz/accesibilidad, 144 combinaciones de página y tamaño y 36 análisis axe en claro/oscuro, sin infracciones automáticas. Nu Checker local valida los 18 HTML sin errores ni advertencias; css-tree no detecta errores en la gramática comprobada. Estos resultados complementan las tres herramientas exigidas.')

    page(); heading('Estudio de advertencias de TAW')
    taw_counts = Counter()
    for r in final:
        if r['tool'] == 'TAW':
            taw_counts.update({row['criterion'].split(' - ')[0]: row['warnings'] for row in r['rows'] if row['warnings']})
    table(['Criterio', 'N', 'Causa posible y comprobación'], [[k, str(n), TAW_ASSESSMENTS[k]] for k, n in sorted(taw_counts.items())], [20, 10, 144])
    p('Estas advertencias solicitan juicio sobre el significado o contexto. Se considera resuelto el examen cuando la comprobación documentada descarta la barrera o identifica una actuación pendiente; no se cambia el recuento bruto de la herramienta para reflejar esa valoración.')
    heading('Estudio de alertas de WAVE')
    wave_counts = Counter()
    for r in final:
        if r['tool'] == 'WAVE':
            for label in r['alertTypes']:
                n, title = label.split(' ', 1); wave_counts[title] += int(n)
    wave_explanations = {
        'Redundant link': 'La marca y el menú llevan al inicio; portada y mapa ofrecen accesos adicionales al mismo destino. La redundancia se revisa como decisión de navegación, no como un fallo automático. Se conservan los accesos útiles.',
        'Noscript element': 'El buscador tiene una alternativa para quien no ejecuta JavaScript. Se comprobó que conduce al mapa y a Lectura y que el contenido continúa disponible.',
        'Audio/Video': 'Los tres MP3 requieren revisar controles y alternativa textual. Los controles propios se verificaron; la ausencia de transcripción es un problema confirmado.',
        'YouTube video': 'Se revisaron el diálogo, nombre, ausencia de autoplay, salida y enlace alternativo. Las alternativas del contenido del vídeo no quedan acreditadas por el mero uso de YouTube.'
    }
    table(['Alerta', 'N', 'Estudio y actuación'], [[k, str(n), wave_explanations[k]] for k, n in wave_counts.items()], [33, 10, 131])
    p('Las alertas de texto alternativo redundante y títulos redundantes disminuyen tras la corrección. Las restantes alertas se conservan con su motivo. La [ayuda de WAVE](https://wave.webaim.org/help) distingue sus indicadores de una declaración de conformidad y exige evaluación humana para el contenido que no puede juzgar automáticamente.')

    page(); heading('Estudio de advertencias de AChecker')
    ac_counts = Counter()
    for r in final:
        if r['tool'] == 'AChecker': ac_counts.update(r['warningTypes'])
    p('Las advertencias se agrupan por comprobación. Las opciones PASS/FAIL que aparecen en el informe de ACHECKS son criterios de decisión para el evaluador; no se cuentan como aprobaciones o fallos elegidos. Los errores conocidos se mantienen separados de las advertencias.')
    groups = {}
    warning_rows = []
    for title, n in ac_counts.items():
        status, assessment = ac_assessment(title)
        group = (status, assessment)
        if group not in groups: groups[group] = f'A{len(groups)+1:02d}'
        warning_rows.append([title, str(n), groups[group] + ' - ' + status])
    table(['Comprobación exacta del servicio', 'N', 'Revisión'], warning_rows, [114, 10, 50])
    heading('Dictámenes de los grupos de AChecker')
    for (status, assessment), code in groups.items():
        p('**' + code + ' - ' + status + '.** ' + assessment)

    heading('Comprobación manual de los 30 no verificados')
    p('Se inspecciona cada criterio con un dictamen y una razón. Favorable se refiere a la interfaz y contenido comprobados en este entorno. Los límites de medios externos se explicitan; no se sustituyen por un aprobado general. Las evidencias concretas por fila constan en `revision-manual.json`.')
    table(['Criterio', 'Dictamen', 'Comprobación y motivo'], [[r['id'] + '\n' + r['title'], r['status'], r['observation']] for r in manual['criteria']], [32, 36, 106])
    heading('Estados y evidencias complementarias')
    bullet('Copia real de correo con confirmación junto a la dirección; consulta judo con Enter, foco en resumen, Tab al primer resultado y llegada al apartado sin quedar bajo la cabecera.')
    bullet('Salto al contenido, apertura de ayuda con Enter, audio sin autoplay y cierre por Escape con retorno al enlace; cierre y descarga del iframe de vídeo.')
    bullet('Menú a 320 px con Escape y retorno de foco; cambio de tema con nombre de acción y estado actualizados. Los tamaños son simulados en navegador, no dispositivos físicos nuevos.')
    bullet('Lectura: 60ch, interlineado 1,65, separación de párrafos de 2,5em y alineación inicial. Medidas con fuente de 16 px: 26,4 px de línea y 40 px de margen. Colores forzados y ampliación/reflujo comprobados como apoyo técnico.')

    page(); heading('Multimedia y alcance de la conclusión')
    p('**Problema confirmado: faltan alternativas textuales equivalentes de tres audios.** Identificar artista y canción no permite conocer toda la información sonora. Las advertencias de AChecker sobre transcripción y las alertas multimedia de WAVE se consideran pertinentes, aunque sus contadores de errores sean cero.')
    p('TAW devuelve no aplicable en criterios multimedia como 1.2.1 y 1.2.2 en el resumen de Lectura, aunque existen enlaces que abren esos medios. El resumen automático no acredita su accesibilidad: la inspección de los recursos y reproductores descubre requisitos que el analizador no ha verificado.')
    table(['Recurso', 'Resultado y actuación necesaria'], [
        ['Robe - Del Tiempo Perdido', 'MP3 sin transcripción enlazada. Preparar y verificar alternativa textual equivalente.'],
        ['Gavina.mp3 - SOTA EL CEL', 'MP3 sin transcripción enlazada. Preparar y verificar alternativa textual equivalente.'],
        ['Las Petunias - Marcelo Criminal', 'MP3 sin transcripción enlazada. Preparar y verificar alternativa textual equivalente.'],
        ['Spider-Man: Into the Spider-Verse', 'El reproductor, con el vídeo cargado y en reproducción, indica que no tiene subtítulos. Proporcionar una versión con subtítulos verificados y las demás alternativas exigibles.'],
        ['Scott Pilgrim vs. the World', 'Se activaron subtítulos en inglés generados automáticamente. Su presencia no acredita exactitud, descripción de sonidos ni equivalencia en español. Revisarlos y proporcionar alternativas verificadas.']
    ], [58, 116])
    p('El [criterio 1.2.1](https://www.w3.org/WAI/WCAG21/Understanding/audio-only-and-video-only-prerecorded.html) exige una alternativa equivalente para audio pregrabado. En vídeo, [1.2.6](https://www.w3.org/WAI/WCAG21/Understanding/sign-language-prerecorded.html) y [1.2.8](https://www.w3.org/WAI/WCAG21/Understanding/media-alternative-prerecorded.html) añaden requisitos AAA de interpretación y alternativa completa. No se han acreditado audiodescripción, interpretación en lengua de signos ni alternativa textual completa de estos tráileres. La presencia de un reproductor o un parámetro para solicitar subtítulos no acredita esos contenidos. Los estados observados se guardan en `manual/11-video-subtitulos.txt` y `manual/12-video-subtitulos.txt`.')
    p('La medida y corrección de lectura se interpretan según [1.4.8](https://www.w3.org/WAI/WCAG21/Understanding/visual-presentation.html). Se comprobó la presentación propia y que el navegador pudiera aplicar colores de usuario. No se atribuye a este ensayo compatibilidad con toda combinación posible de navegador y tecnología de apoyo.')
    p('**Conclusión:** ' + ('se alcanza cero errores automáticos en las tres herramientas para las páginas ensayadas, ' if clear else 'la conclusión automática final queda pendiente del último TAW, ') +
      'y queda documentada la revisión de advertencias y criterios manuales. Las alternativas multimedia pendientes impiden declarar conformidad integral AAA. Se preservan los datos originales, los avisos y sus límites para incorporarlos al informe del sitio web personal.')

    page(); heading('Evidencias y reproducción')
    p('La carpeta `docs/accesibilidad/inicial` contiene los 54 informes previos; `final` conserva los 54 informes de comprobación. `resultados.json` y `resultados.csv` incluyen fechas, URL, recuentos, criterios y hash de cada captura. `revision-manual.json` contiene los dictámenes y sus fuentes.')
    bullet('`scripts/summarize-accessibility.py` reconstruye los recuentos de las capturas guardadas. Rechaza un resumen incompleto o un mensaje de límite en lugar de interpretarlo como cero.')
    bullet('`scripts/build-accessibility-report.py` genera este capítulo y el PDF desde esos datos. Su modo final exige los 54 resultados sin errores automáticos; el modo de borrador permite revisar la maquetación antes de cerrar una repetición pendiente.')
    bullet('`scripts/check.py`, `scripts/test-search.cjs`, `scripts/test-ui.cjs`, `scripts/test-search-browser.cjs` y `scripts/test-final-browser.cjs` proporcionan comprobaciones locales adicionales. Los resultados de estas pruebas no se presentan como ejecuciones de TAW, AChecker o WAVE.')
    p('Fuentes de herramientas: [TAW](https://www.tawdis.net/), [AChecker+](https://achecks.org/achecker), [documentación AChecker](https://achecks.org/documentation/frame_content.php?p=checker%2Findex.php), [WAVE](https://wave.webaim.org/). Se registran los estándares elegidos; las interfaces no exponen una versión numérica completa de sus motores.')
    blocks.append({'type': 'images', 'items': [
        ('WAVE - Intereses EN', EVIDENCE / 'final/en-intereses-wave.jpg'),
        ('TAW - Lectura EN', EVIDENCE / 'final/en-lectura-taw.jpg'),
        ('AChecker - Intereses EN', EVIDENCE / 'final/en-intereses-achecker.jpg')
    ]})
    return blocks


def markdown(blocks):
    out = []
    for b in blocks:
        t = b['type']
        if t == 'heading': out.append('#' * b['level'] + ' ' + b['text'])
        elif t == 'p': out.append(b['text'])
        elif t == 'bullet': out.append('- ' + b['text'])
        elif t == 'table':
            rows = [b['headers'], ['---'] * len(b['headers'])] + b['rows']
            out.append('\n'.join('| ' + ' | '.join(clean(v).replace('|', '/').replace('\n', '<br>') for v in row) + ' |' for row in rows))
        elif t == 'images':
            for label, path in b['items']:
                out.append(f'![{label}](accesibilidad/{path.relative_to(EVIDENCE).as_posix()})')
    return '\n\n'.join(out) + '\n'


def render_pdf(blocks, target):
    from PIL import Image as PILImage
    for name, filename in [('Arial', 'arial.ttf'), ('Arial-Bold', 'arialbd.ttf'), ('Arial-Italic', 'ariali.ttf')]:
        pdfmetrics.registerFont(TTFont(name, str(Path('C:/Windows/Fonts') / filename)))
    pdfmetrics.registerFontFamily('Arial', normal='Arial', bold='Arial-Bold', italic='Arial-Italic', boldItalic='Arial-Bold')
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle('ReportBody', fontName='Arial', fontSize=10, leading=14.2, textColor=INK, spaceAfter=7, wordWrap='LTR'))
    styles.add(ParagraphStyle('ReportH1', fontName='Arial-Bold', fontSize=21, leading=25, textColor=INK, spaceAfter=14, keepWithNext=True))
    styles.add(ParagraphStyle('ReportH2', fontName='Arial-Bold', fontSize=13.3, leading=17, textColor=ACCENT, spaceBefore=10, spaceAfter=9, keepWithNext=True))
    styles.add(ParagraphStyle('ReportCell', parent=styles['ReportBody'], fontSize=8.5, leading=11.7, spaceAfter=0))
    styles.add(ParagraphStyle('ReportHeader', parent=styles['ReportCell'], fontName='Arial-Bold', textColor=colors.white))
    story = []
    for b in blocks:
        t = b['type']
        if t == 'page': story.append(PageBreak())
        elif t == 'heading': story.append(Paragraph(inline(b['text']), styles['ReportH1' if b['level'] == 1 else 'ReportH2']))
        elif t in ('p', 'bullet'):
            story.append(Paragraph(inline(b['text']), styles['ReportBody'], bulletText='-' if t == 'bullet' else None))
        elif t == 'table':
            values = [[Paragraph(inline(v), styles['ReportHeader']) for v in b['headers']]]
            values += [[Paragraph(inline(v), styles['ReportCell']) for v in row] for row in b['rows']]
            widths = [w * mm for w in b['widths']] if b['widths'] else None
            tab = LongTable(values, colWidths=widths, repeatRows=1, hAlign='LEFT')
            tab.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), ACCENT), ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f6f3fb')]),
                ('LINEBELOW', (0,0), (-1,0), .4, ACCENT),
                ('LINEBELOW', (0,1), (-1,-1), .25, colors.HexColor('#d9d0e4')),
                ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
                ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5)
            ]))
            story.extend([tab, Spacer(1, 9)])
        elif t == 'images':
            story.append(Paragraph('Capturas de las herramientas', styles['ReportH2']))
            for label, path in b['items']:
                if not path.is_file(): continue
                with PILImage.open(path) as im: iw, ih = im.size
                max_height = (215 if label.startswith('AChecker') else 150 if label.startswith('TAW') else 110) * mm
                width, height = min(174 * mm, max_height * iw/ih), min(max_height, 174*mm * ih/iw)
                story.append(KeepTogether([Paragraph(label, styles['ReportBody']), Image(str(path), width=width, height=height), Spacer(1,12)]))

    def furniture(canvas, doc):
        canvas.saveState(); canvas.setFont('Arial', 8); canvas.setFillColor(colors.HexColor('#51465e'))
        canvas.drawString(18*mm, A4[1]-11*mm, 'Web personal V3 - Accesibilidad')
        canvas.drawRightString(A4[0]-18*mm, A4[1]-11*mm, 'UO319242')
        canvas.setStrokeColor(colors.HexColor('#d9d0e4')); canvas.line(18*mm, 14*mm, A4[0]-18*mm, 14*mm)
        canvas.drawString(18*mm, 9*mm, '20/11/2026 - Resultados automáticos y revisión manual')
        canvas.drawRightString(A4[0]-18*mm, 9*mm, str(doc.page)); canvas.restoreState()

    target.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(target), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm,
                            topMargin=20*mm, bottomMargin=20*mm, title='Accesibilidad de la web personal V3',
                            author='Carles Valladares García - UO319242')
    doc.build(story, onFirstPage=furniture, onLaterPages=furniture)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--draft', action='store_true'); args = parser.parse_args()
    results = json.loads((EVIDENCE/'resultados.json').read_text(encoding='utf-8'))
    manual = json.loads((EVIDENCE/'revision-manual.json').read_text(encoding='utf-8'))
    final = [r for r in results if r['phase'] == 'final']
    clear = len(final) == 54 and all(r['errors'] == 0 and r.get('contrastErrors', 0) == 0 for r in final)
    if not clear and not args.draft:
        raise SystemExit('No se genera entrega final: falta cerrar algún resultado externo sin errores.')
    blocks = build_blocks(results, manual, clear)
    directory = REPO/'tmp/pdfs/ux-v3-accessibility' if args.draft else ROOT/'output/pdf'
    directory.mkdir(parents=True, exist_ok=True)
    pdf = directory/'UO319242-Informe-accesibilidad-web-personal-V3.pdf'
    md = directory/'accesibilidad-v3.md' if args.draft else ROOT/'docs/accesibilidad-v3.md'
    md.write_text(markdown(blocks), encoding='utf-8', newline='\n')
    render_pdf(blocks, pdf)
    print(('Borrador' if args.draft else 'Entrega final') + ': ' + str(pdf))


if __name__ == '__main__':
    main()
