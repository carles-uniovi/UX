# Evidencias de accesibilidad de V3

Revisión del 20/11/2026 sobre la web pública. El capítulo redactado está en [accesibilidad-v3.md](../accesibilidad-v3.md); incluye los límites y las barreras multimedia encontradas manualmente.

- `inicial/`: 18 páginas por tres herramientas, 54 resúmenes anteriores a las correcciones.
- `final/`: 54 comprobaciones válidas, con su URL y fecha UTC. Se conserva el último análisis de cada combinación de página y herramienta; los cambios posteriores se repiten en las páginas afectadas.
- `manual/`: comprobaciones de teclado, reproductores, mediciones, detalle H48 aportado por el autor y mensajes de límite de TAW. Los límites no son resultados de evaluación.
- `resultados.json` y `resultados.csv`: recuentos reconstruidos de los TXT mediante `scripts/summarize-accessibility.py`. El JSON incorpora criterios y advertencias; también el SHA-256 de cada TXT de origen.
- `revision-manual.json`: dictamen individual y evidencia de los 30 criterios que TAW no verifica, más hallazgos adicionales.

Los TXT proceden de la interfaz visible de TAW, AChecker+ o WAVE. Algunos tienen un JSON auxiliar de captura, pero el resumen canónico se reconstruye del TXT. Las capturas de pantalla muestran ejemplos; la cobertura completa se acredita con los 54 registros por fase.

Errores, advertencias, alertas y no verificados son categorías distintas. Los contadores de avisos se mantienen aunque la inspección descarte una barrera. Los ceros automáticos no acreditan conformidad WCAG AAA: faltan alternativas textuales de los audios y las alternativas de vídeo no están plenamente acreditadas.
