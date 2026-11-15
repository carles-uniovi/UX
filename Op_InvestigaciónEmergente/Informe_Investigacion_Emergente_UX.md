# Áreas emergentes de investigación en experiencia de usuario

Experiencia de Usuario · Máster Universitario en Ingeniería Web

Fecha de consulta de fuentes: 14 de noviembre de 2026

## 1. Alcance y criterio de selección

La presentación de Cueva Lovelle describe un software cada vez más complejo y autónomo, en el que la inteligencia artificial interviene tanto en el desarrollo como en las aplicaciones [1]. Esta evolución plantea preguntas para la experiencia de usuario: ¿cómo sabe una persona qué está haciendo un agente?, ¿cómo corrige una respuesta incorrecta?, ¿qué ocurre si una interfaz cambia mientras la utiliza? El funcionamiento técnico del sistema no basta para responderlas. Es necesario observar cómo lo entienden y utilizan sus destinatarios.

Este informe desarrolla seis áreas relacionadas con las diapositivas 6, 9-10 y 13-18. Se han elegido porque afectan directamente a la interacción y permiten formular preguntas que pueden estudiarse mediante pruebas con usuarios. La accesibilidad, la personalización y la carga cognitiva cuentan con una larga trayectoria de investigación. Lo que justifica revisarlas aquí es la incorporación de sistemas capaces de generar contenidos, modificar interfaces y ejecutar acciones sin recibir una instrucción para cada paso.

El análisis se apoya en el material docente y en una selección de fuentes primarias de 2024-2026. Su alcance es exploratorio. Los estudios citados sirven para situar los problemas y conocer algunos resultados, sin constituir una revisión sistemática de la literatura. Las propuestas de investigación que acompañan a cada área son elaboración propia y no se han llevado a la práctica.

## 2. Posibles áreas emergentes

### 2.1. Delegación y control humano de agentes autónomos

Delegar una tarea en un agente exige decidir qué puede hacer por su cuenta y qué debe consultar antes de actuar. Los agentes descritos en la presentación planifican, utilizan herramientas y reajustan su comportamiento [1, diaps. 6, 10 y 19]. Por tanto, la persona necesita poder revisar una secuencia de acciones, reconocer una desviación y detenerla a tiempo. Un historial de actividad puede resultar insuficiente si solo permite descubrir el error después de que se haya producido.

Dizon y colaboradores compararon tres modalidades de interacción en un gestor de contenidos con 73 participantes. La asistencia redujo las acciones realizadas en la interfaz, aunque no hubo diferencias significativas en el tiempo de ejecución [2]. Conviene, por ello, estudiar cuánto trabajo requiere supervisar al agente. También importa la confianza: Lee y colaboradores encontraron una asociación entre mayor confianza en la IA y menor ejercicio declarado de pensamiento crítico [4]. Al tratarse de una encuesta, este resultado no permite establecer causalidad, pero sí justifica examinar cuándo se revisan las decisiones automáticas y cuándo se aceptan sin comprobarlas.

Una posible investigación compararía distintas formas de presentar el plan del agente y solicitar confirmación. Con el mismo agente y las mismas tareas, se introducirían errores controlados en un entorno simulado. Interesaría medir cuántos cambios no deseados permanecen al terminar, qué errores se detectan y cuánto tiempo lleva la supervisión. Preguntar a los participantes qué ha modificado el agente permitiría comprobar, además, si conservar el control implica comprender lo ejecutado.

<!-- salto de página -->

### 2.2. Interfaces híbridas gráfico-conversacionales

La pregunta de la diapositiva 13, sobre cuándo conviene conversar y cuándo utilizar una interfaz gráfica, tiene consecuencias prácticas para el diseño web [1]. Escribir una petición puede ser cómodo para expresar un objetivo, pero comparar opciones o corregir varios valores puede resultar más sencillo mediante tablas, formularios o controles visibles. Las aplicaciones que combinan ambos modos deben resolver también cómo trasladar la información de uno a otro sin obligar a repetir instrucciones.

Chen y colaboradores estudian interfaces generadas a partir de consultas y las comparan con el chat desde aspectos funcionales, interactivos y emocionales [3]. Sus resultados son favorables a las interfaces generadas en las condiciones evaluadas. Queda por determinar cómo influyen el tipo de tarea y la experiencia de la persona. Además, que los participantes prefieran una interfaz no garantiza que las respuestas sean correctas ni que puedan corregirlas con facilidad.

Para estudiar esta cuestión se podrían comparar un chat, una interfaz gráfica y una combinación de ambos con tareas equivalentes de búsqueda, comparación y edición. Los datos y las capacidades del modelo se mantendrían constantes. Además de la finalización correcta de las tareas, se registraría el tiempo necesario para corregir errores y la información perdida al cambiar de modo. Las entrevistas ayudarían a explicar las elecciones de los participantes. Así podrían establecerse criterios para decidir qué forma de interacción conviene en cada caso.

### 2.3. Personalización generativa con control y privacidad

Una interfaz que se adapta al usuario puede dar prioridad a las funciones que más utiliza. Sin embargo, si cambia la ubicación de los controles o reorganiza el contenido, también puede dificultar que encuentre algo que antes conocía. La personalización descrita en la diapositiva 14 obliga a estudiar este equilibrio entre adaptación y estabilidad [1]. A ello se añade la necesidad de recoger información sobre la persona para decidir qué modificar.

El perfil de riesgos de IA generativa del NIST recoge problemas de privacidad, sesgos y relación entre personas y sistemas [5]. En una interfaz personalizada, estas cuestiones se concretan en decisiones como qué datos se conservan, cómo se explican los cambios y si es posible rechazarlos. Falta comprobar hasta qué punto los usuarios comprenden esas decisiones y pueden modificar las preferencias que el sistema les atribuye.

Un estudio de varias sesiones permitiría comparar una interfaz fija, otra que se adapta automáticamente y una tercera que consulta los cambios antes de aplicarlos. Al variar las tareas se observaría si la adaptación sigue siendo útil o se convierte en un obstáculo. Se medirían los errores posteriores a cada cambio, el tiempo para recuperar la disposición anterior y la comprensión de los datos almacenados. Incluir a personas que prefieren desactivar la personalización ayudaría a valorar cuándo conviene mantener una alternativa estable.

<!-- salto de página -->

### 2.4. Accesibilidad inteligente y generación inclusiva

Las descripciones de imágenes, los subtítulos automáticos y la adaptación cognitiva que recoge la diapositiva 15 pueden facilitar el acceso a contenidos [1]. Su utilidad depende, sin embargo, de la tarea. Una descripción puede estar bien redactada y omitir el dato que necesita la persona; un texto simplificado puede perder una condición importante. La investigación debe comprobar si estas ayudas permiten utilizar el servicio con autonomía y conservar la información necesaria.

Guriţă y Vatavu analizaron 90 interfaces generadas y entrevistaron a ocho profesionales del diseño. Encontraron cumplimiento básico de accesibilidad, pero también patrones homogéneos que pueden dificultar la atención a necesidades específicas [6]. Estos resultados muestran la importancia de ampliar la evaluación: las comprobaciones técnicas deben acompañarse de pruebas con las personas que van a utilizar las adaptaciones.

Una línea de trabajo consistiría en diseñar las ayudas junto con personas que usan tecnologías de apoyo y comparar tres versiones: el contenido original, una adaptación revisada y otra generada automáticamente. Se registraría si la tarea se completa sin ayuda, qué información se omite y cuánto esfuerzo requiere corregir la adaptación. Los resultados se analizarían por necesidad y configuración de apoyo, ya que un promedio puede ocultar dificultades de un grupo concreto. También se comprobaría si las opciones para corregir o desactivar la ayuda son accesibles y comprensibles.

### 2.5. Neuroergonomía y adaptación a la carga cognitiva

La presentación propone utilizar seguimiento ocular, EEG y otros sensores para estudiar la carga cognitiva y la fatiga [1, diap. 16]. Estas medidas podrían servir para ajustar la cantidad de información mostrada o sugerir una pausa. Antes de aplicar esos cambios es necesario averiguar si la estimación es fiable y si la intervención mejora la experiencia. Una pausa inoportuna o una reorganización inesperada pueden interrumpir una tarea que la persona estaba realizando correctamente.

Sun y Liao estudiaron las pausas adaptativas en realidad aumentada mediante la conductancia de la piel como indicador indirecto. En la parte adaptativa disminuyó el indicador acumulado de carga, aunque el efecto sobre el rendimiento fue inconcluso [7]. Por tanto, conviene examinar por separado la respuesta fisiológica y la ejecución de la tarea. También habría que comprobar si lo observado se mantiene fuera del entorno experimental y con usuarios de características diferentes.

Para investigarlo se podrían comparar una interfaz fija, otra con pausas programadas y una tercera que adapte la información según las señales registradas. La evaluación combinaría errores y tiempos de tarea, valoraciones de carga y medidas fisiológicas, con calibración individual y una sesión posterior de comprobación. Interesarían especialmente las falsas alarmas y el tiempo necesario para retomar el trabajo. La persona debería poder rechazar los cambios. La recogida de señales exigiría consentimiento específico, limitar los datos almacenados y revisar las interferencias de la medición, sin tratar estos indicadores como medidas directas del pensamiento.

<!-- salto de página -->

### 2.6. UX sostenible de servicios con IA

La sostenibilidad del software también depende de cómo se utiliza una aplicación. Solicitar varias respuestas, generar contenido que se descarta o repetir una operación puede aumentar el consumo del servicio. La diapositiva 18 incorpora la eficiencia energética y la responsabilidad social entre los retos del desarrollo [1]. Desde UX interesa estudiar qué decisiones de diseño permiten reducir ese consumo manteniendo la calidad que necesita el usuario.

Luccioni, Jernite y Strubell compararon la energía y las emisiones de inferencia de distintos modelos y tareas [8]. Su trabajo muestra diferencias que deben tenerse en cuenta al elegir cómo resolver una petición, aunque no permite asignar un consumo universal a cada consulta. A partir de ello, cabe investigar si ofrecer respuestas más breves, reutilizar resultados o reservar la generación más costosa para ciertas tareas reduce recursos sin dificultar el uso.

Un experimento podría comparar el servicio habitual con una versión que permita elegir el detalle de la respuesta y solicitar ampliaciones después. Se medirían la energía por tarea completada, la calidad del resultado mediante una rúbrica y el número de veces que se pide regenerarlo. Habría que documentar el hardware y qué partes del sistema se incluyen en la medición. Un seguimiento posterior permitiría comprobar si el ahorro por operación se mantiene o si conduce a un mayor uso total. La información presentada al usuario tendría que ser comprensible y basarse en mediciones justificadas.

## 3. Propuesta prioritaria para un estudio en Ingeniería Web

Para un trabajo de Ingeniería Web, la supervisión de agentes ofrece un punto de partida viable: permite construir un prototipo pequeño y observar errores concretos. Se propone estudiar si revisar una previsualización editable antes de confirmar reduce los cambios no deseados y cuánto tiempo añade esa revisión.

El prototipo sería un gestor de contenidos simulado con dos variantes. La primera mostraría una confirmación genérica de la acción; la segunda, el plan y una previsualización de los cambios. En ambas sería posible rechazar la operación. Para atribuir las diferencias a la interfaz se mantendrían constantes el agente, sus respuestas y los errores introducidos. Cada participante probaría las dos variantes con tareas equivalentes, alternando el orden y la asignación de tareas para reducir el efecto del aprendizaje.

La medida principal sería la proporción de casos en los que queda un cambio no deseado al finalizar. El tiempo total, la comprensión de lo modificado y la carga percibida ayudarían a interpretar ese resultado. Un piloto con participantes de distinta experiencia serviría para ajustar las tareas y estimar la muestra de un estudio posterior. Los criterios de análisis se fijarían de antemano y los resultados incluirían tamaños de efecto e incertidumbre. Se utilizarían datos ficticios y acciones reversibles, con consentimiento de los participantes y una explicación final de los errores simulados.

## 4. Conclusión

Las áreas examinadas requieren evaluar tanto lo que hace el sistema como la capacidad del usuario para comprenderlo y actuar sobre él. Reducir clics, generar una adaptación o detectar una señal fisiológica no permite, por sí solo, concluir que la experiencia ha mejorado. Para valorar cada propuesta habrá que observar el resultado de las tareas, el esfuerzo que exige y las diferencias entre usuarios. En aplicaciones que cambian con el modelo o se adaptan durante el uso, esta evaluación deberá repetirse para comprobar que las mejoras se mantienen.

<!-- salto de página -->

## 5. Referencias

[1] Cueva Lovelle, J. M. (2026). *Nuevos retos de investigación en Ingeniería del Software*. Presentación docente, Universidad de Oviedo. Archivo aportado: `2026-11-05-Retos-Ing-Software.pdf`, 38 diapositivas. Fecha indicada en el nombre del archivo: 5 de noviembre de 2026. Las referencias a diapositivas cuentan las páginas del PDF desde 1.

[2] Dizon, G., Sta Maria, T. J., Deja, J. A., y Sumi, Y. (2026). *Delegating or Doing? Understanding User Behavior in Hybrid Human-Agent Interfaces*. Prepublicación consultada, arXiv:2608.19551v2, 25 de agosto de 2026. [Texto y metadatos](https://arxiv.org/abs/2608.19551v2).

[3] Chen, J., Zhang, Y., Zhang, Y., Shao, Y., y Yang, D. (2026). *Generative Interfaces for Language Models*. Versión consultada: arXiv:2508.19227v3, 1 de mayo de 2026; primera versión de 2025. Identificada por sus autores como trabajo de Findings of ACL 2026. [Texto y metadatos](https://arxiv.org/abs/2508.19227v3).

[4] Lee, H.-P., Sarkar, A., Tankelevitch, L., Drosos, I., Rintel, S., Banks, R., y Wilson, N. (2025). *The Impact of Generative AI on Critical Thinking: Self-Reported Reductions in Cognitive Effort and Confidence Effects From a Survey of Knowledge Workers*. CHI 2025, artículo 1121, 1-22. [DOI: 10.1145/3706598.3713778](https://doi.org/10.1145/3706598.3713778).

[5] National Institute of Standards and Technology. (2024). *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*. NIST AI 600-1, julio de 2024. [DOI: 10.6028/NIST.AI.600-1](https://doi.org/10.6028/NIST.AI.600-1).

[6] Guriţă, A.-E., y Vatavu, R.-D. (2025). *Good Accessibility, Handcuffed Creativity: AI-Generated UIs Between Accessibility Guidelines and Practitioners’ Expectations*. Designing Interactive Systems Conference (DIS 2025), 13 páginas. [DOI: 10.1145/3715336.3735691](https://doi.org/10.1145/3715336.3735691).

[7] Sun, J., y Liao, T. (2025). *Designing adaptive feedback systems for managing cognitive load in augmented reality*. Design Science, 11, e49. Publicado el 26 de noviembre de 2025. [DOI: 10.1017/dsj.2025.10040](https://doi.org/10.1017/dsj.2025.10040).

[8] Luccioni, A. S., Jernite, Y., y Strubell, E. (2024). *Power Hungry Processing: Watts Driving the Cost of AI Deployment?* ACM Conference on Fairness, Accountability, and Transparency (FAccT 2024). [DOI: 10.1145/3630106.3658542](https://doi.org/10.1145/3630106.3658542).
