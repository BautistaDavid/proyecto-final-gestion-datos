# Guion del presentador

Sustentación del proyecto final de Gestión de Datos: monitoreo de reputación de Banco Davivienda.
Este archivo se genera desde las notas de `index.html` (tecla **N** en la presentación); para cambiar el guion, editen las notas y vuelvan a ejecutar `construir.py`.

| Bloque | Tiempo | Diapositivas |
|---|---|---|
| Elevator pitch | 5 min | 1–2 |
| Material técnico | 10 min | 3–22 |
| Trabajo en equipo | 2 min | 23 |
| Preguntas | 5 min | 24 |

**Cómo usar este guion.** Cada diapositiva tiene tres partes: la **idea clave** (lo único que el público debe recordar), el texto para decir en voz alta y, a veces, un *si preguntan* con el detalle técnico. Lo de *si preguntan* no se dice en la presentación; es apoyo para la ronda de preguntas. No hace falta leer el texto palabra por palabra: basta con transmitir la idea clave y las cifras.

## Glosario rápido

| Término | En palabras simples |
|---|---|
| Queja fundada | Queja que se cerró a favor del cliente: el banco reconoce que el cliente tenía la razón. |
| Homologar | Emparejar a mano categorías que dos fuentes nombran distinto (por ejemplo, el mismo producto con otro nombre). |
| Puntos físicos | Oficinas y cajeros del banco (canales 4 y 14). Sirven para comparar departamentos de distinto tamaño. |
| Vista minable | La tabla final, lista para analizar: una fila por mes, departamento y producto. |
| Left join | Unir dos tablas conservando todas las filas de la tabla base, aunque la otra no tenga pareja. |
| Índice relativo | Cuánto subieron las quejas de un departamento frente a lo normal, comparado con lo que subió el país ese mes. |
| Regla de Tukey | Regla estándar para detectar valores fuera de rango: marca lo que se aleja del 50 % central de los datos más de 1,5 veces el ancho de ese 50 %. |
| Periodo de arranque | Enero a septiembre de 2023, cuando Smartsupervision apenas empezaba a reportar; no se evalúa. |
| Correlación | Qué tanto se mueven juntas dos variables; va de −1 a 1, y cerca de 1 significa que suben juntas. |
| Mediana | El valor del medio cuando se ordenan los datos; no se deja arrastrar por valores extremos como el promedio. |
| MAR | Datos que faltan más en un grupo que en otro, según algo que sí se observa (aquí, la instancia que recibió la queja). |
| CRISP-DM | Metodología por fases para proyectos de datos; este hito cubre las tres primeras: negocio, datos y preparación. |

## 1. Monitoreo de reputación de Banco Davivienda con quejas oficiales

**Idea clave:** Presentarnos y decir de qué se trata en una frase.

(≈15 s) Buenas tardes. Somos David, Belky y Fabian. Nuestro proyecto busca ayudar a Banco Davivienda a cuidar su reputación usando las quejas que sus clientes ponen ante la Superintendencia Financiera, que son datos públicos. Primero va el pitch y después les mostramos cómo lo hicimos.

## 2. [ESPACIO RESERVADO: ELEVATOR PITCH]
*01 · Elevator pitch*

**Idea clave:** Vender el proyecto a un posible patrocinador (lo completa el equipo).

(5 min) Estructura sugerida en la sección 2.4 del cuaderno: gancho (30 s), problema (1 min), solución con las dos preguntas (1 min 30 s), evidencia (1 min 30 s) y pedido al patrocinador (30 s). Cifras que pueden usar en la evidencia: 1.231.059 quejas de Banco Davivienda entre enero de 2023 y septiembre de 2026; en el 74,8 % de las quejas cerradas el cliente tenía la razón; 11 alertas en 10 departamentos. Para pasar al bloque técnico: "Ahora les mostramos cómo llegamos a esas cifras".

## 3. Las señales de una crisis ya están en las quejas
*02 · Comprensión del negocio*

**Idea clave:** Dos preguntas: qué arreglar primero y dónde aparece un problema antes de que sea noticia.

(≈35 s) Los bancos suelen enterarse de una crisis de reputación cuando ya está en los medios, pero las quejas de los clientes llevan meses avisando. Por eso nos hicimos dos preguntas. La primera: qué productos y qué motivos concentran las quejas fundadas, que son aquellas en las que al final el banco reconoce que el cliente tenía la razón. La segunda: si mirando las quejas mes a mes en cada departamento podemos detectar subidas raras que sirvan como alerta.

*Si preguntan:* ¿Por qué dos fuentes? La primera pregunta necesita saber cómo terminó cada queja, y eso solo lo trae el histórico de 2010 a 2022. La segunda necesita el mes y el departamento, y eso solo lo trae Smartsupervision, desde 2023.

## 4. Dos fuentes de quejas y tres de apoyo, todas oficiales
*03 · Procedencia y linaje*

**Idea clave:** Usamos cinco tablas públicas: dos de quejas y tres que ayudan a interpretarlas.

(≈35 s) Todo sale de datos.gov.co. Hay dos fuentes de quejas: el histórico de la Superintendencia Financiera, de 2010 a 2022, que dice cómo terminó cada queja, y Smartsupervision, desde 2023, que dice en qué mes y en qué departamento se puso. Las otras tres ayudan: cuántas oficinas y cajeros tiene el banco en cada departamento, una tabla para traducir códigos de departamento a nombres, y las sanciones de la Superintendencia de Industria y Comercio como contexto del sector. Entre julio y diciembre de 2022 ninguna fuente tiene datos, por eso no unimos las dos series en una sola.

*Si preguntan:* La descarga está en un cuaderno aparte y los archivos quedan guardados en el repositorio con su fecha y una huella digital (hash), así los tres trabajamos siempre sobre la misma copia.

## 5. Solo el 20 % de los productos cruzaba sin homologar
*04 · Integración*

**Idea clave:** Las dos fuentes llaman distinto a los mismos productos; tuvimos que emparejarlos a mano.

(≈40 s) Para llevar lo que sabemos del histórico a las quejas nuevas, había que emparejar los productos de las dos fuentes. El problema es que cada una los nombra distinto. Cruzando solo nombres idénticos, apenas una de cada tres quejas encontraba pareja: el 34,7 %. Por eso homologamos, es decir, revisamos a mano 65 productos y los agrupamos en 14 categorías comunes. Con eso, tres de cada cuatro quejas quedan emparejadas, el 74,8 %. Las que no tienen equivalente usan el promedio del banco, 77,5 %.

*Si preguntan:* Para los depósitos de bajo monto probamos usar la tasa de cuenta de ahorros en vez del promedio: el resultado cambia menos de medio punto (0,39), así que dejamos la opción más prudente.

## 6. El denominador son 2.736 puntos físicos estables, no 28.987
*04 · Integración*

**Idea clave:** Para comparar departamentos grandes y pequeños, dividimos las quejas por las oficinas y cajeros.

(≈40 s) Bogotá siempre va a tener más quejas que Vaupés, solo por tamaño. Para comparar de forma justa dividimos las quejas por los puntos de atención del banco. El dataset trae tres tipos de canal, pero no dice qué es cada uno. Por su tamaño y porque casi no cambian de un mes a otro, concluimos que los canales 4 y 14 son oficinas y cajeros: 2.736 puntos en total. El canal 10 tiene casi 29.000 puntos y cambia mucho; parece corresponder a datáfonos, así que lo dejamos fuera.

*Si preguntan:* Como es una deducción, la pusimos a prueba: si usamos solo el canal 4, el orden de los departamentos casi no cambia; si sumamos el 10, sí cambia. Las alertas no se ven afectadas, porque se calculan con las quejas y no con los puntos.

## 7. Bogotá concentra el 63,8 % de las quejas registradas
*05 · Exploración*

**Idea clave:** Comparar quejas totales mide el tamaño del departamento, no sus problemas.

(≈35 s) Un dato lo muestra: Bogotá tiene el 63,8 % de todas las quejas. Además, entre departamentos, el número de quejas sigue casi exacto al número de puntos de atención: la correlación es 0,96, muy cerca del máximo, que es 1. O sea, a más oficinas, más quejas. Por eso no comparamos quejas totales sino quejas por cada 100 puntos. Sospechamos que parte del peso de Bogotá viene de quejas digitales que se registran en la capital, pero no lo podemos comprobar, así que no tocamos el dato.

*Si preguntan:* Los datos están muy cargados hacia valores pequeños: la mitad de los registros tiene una sola queja, pero el promedio es 10,9 porque unos pocos son enormes. Por eso reportamos la mediana además del promedio.

## 8. Tukey fila por fila marcaba el 86,9 % de las quejas
*05 · Calidad*

**Idea clave:** Separamos los huecos de la fuente de los picos reales: los huecos se marcan, los picos se conservan.

(≈35 s) Revisamos la calidad de los datos. No hay registros duplicados ni valores imposibles; los problemas son huecos de la fuente. Octubre de 2026 viene incompleto, con solo 905 quejas, y lo sacamos. Febrero de 2026 no tiene datos y no lo llenamos con cero, porque parecería que las quejas se desplomaron. Y no borramos los valores extremos: para nosotros un mes con muchas quejas no es un error, es justo lo que buscamos.

*Si preguntan:* Si aplicábamos la regla de valores extremos registro por registro, marcaba el 86,9 % de las quejas, así que no servía; la aplicamos sobre los totales de cada departamento por mes. Los 1.194 registros sin ubicación faltan más en una instancia que en otras (eso es lo que se llama MAR); siguen en los totales nacionales y solo salen de los cálculos por departamento.

## 9. Cuatro left joins, 8.647 filas, ninguna perdida
*06 · Preparación*

**Idea clave:** Armamos una sola tabla final uniendo todo, y comprobamos que no se perdiera ni se duplicara nada.

(≈35 s) Con los datos limpios armamos la vista minable: una tabla única, lista para analizar, con una fila por mes, departamento y producto. Partimos de las quejas de Smartsupervision y les pegamos cuatro piezas: la tasa histórica de cada producto, el código del departamento, los datos del departamento, como puntos de atención y alertas, y los datos del mes. En cada paso contamos filas: entran 8.647 y salen 8.647, nada se pierde ni se duplica.

*Si preguntan:* Cada unión es un left join: se conservan todas las filas de la tabla base aunque la otra no tenga pareja. El histórico, aunque es la fuente principal, entra como un dato por producto (su tasa), no como filas. También aplicamos las transformaciones del curso, por ejemplo recortar los extremos y usar logaritmos para que las cifras sean comparables.

## 10. Ahorros y tarjeta suman el 83 % de las quejas fundadas
*07 · Resultados P1*

**Idea clave:** Dos productos explican casi todas las quejas en las que el cliente tenía la razón.

(≈30 s) Primera respuesta. Entre 2010 y 2022, la cuenta de ahorros y la tarjeta de crédito suman el 83 % de las quejas en las que el cliente tenía la razón. Las dos crecen mucho desde 2017. Ojo: esto mide cantidad, no calidad; más quejas también pueden significar más clientes. El gráfico solo muestra años completos para no confundir con 2022, que tiene medio año de datos.

## 11. El cliente gana tres de cada cuatro quejas con desenlace
*07 · Resultados P1*

**Idea clave:** En tres de cada cuatro quejas el cliente tenía la razón, pero depende mucho del producto.

(≈25 s) Cuando una queja se resuelve a favor del cliente, el banco está reconociendo un error. En Davivienda eso pasa en el 74,8 % de las quejas cerradas: tres de cada cuatro. Pero no es igual en todos los productos, y por eso en nuestro análisis cada producto tiene su propia tasa y no un promedio general.

## 12. En leasing no habitacional el cliente gana solo el 33,8 %
*07 · Resultados P1*

**Idea clave:** El leasing no habitacional es el caso que más llama la atención.

(≈30 s) Aquí está la tasa por producto. En cuenta de ahorros el cliente tiene la razón 8 de cada 10 veces; en tarjeta de crédito, 7 de cada 10. El caso llamativo es el leasing no habitacional: el cliente solo gana una de cada tres. Con estos datos no sabemos si son quejas sin fundamento o si el producto se le explica mal al cliente; es algo para revisar con el banco.

## 13. La tasa a favor del cliente cambia hasta 54 puntos entre años
*07 · Resultados P1*

**Idea clave:** La tasa cambia de un año a otro, por eso la miramos año por año.

(≈25 s) Además, esa tasa no es fija. En crédito de vivienda pasó de 27 % en 2011 a 81 % en 2019. Por eso respondemos año por año y no con un solo promedio. Esto también es una limitación: para 2023 en adelante suponemos que se mantiene la tasa de 2019 a 2022, porque la fuente nueva no dice cómo terminó cada queja.

## 14. Las quejas fundadas pasaron de los cobros a los canales
*07 · Resultados P1*

**Idea clave:** Las quejas fundadas pasaron de los cobros a las fallas de los canales.

(≈30 s) ¿Cómo cambiaron los motivos? Comparamos 2010–2015 con 2016–2022. Los cargos que el cliente no reconoce bajaron del 53 % al 36 %, y las fallas de canales y cajeros subieron 9 puntos, hasta el 31 %. En palabras simples: el problema pasó de lo que se le cobra al cliente a que los canales funcionen bien.

*Si preguntan:* Los motivos también tuvieron que agruparse, porque los nombres cambiaron con los años. Creemos que lo que antes se llamaba "descuentos injustificados" hoy se llama "transacción no reconocida", y por eso esos dos grupos solo se comparan sumados.

## 15. 11 alertas en 10 departamentos: el 1,9 % de los meses
*08 · Resultados P2*

**Idea clave:** Un mes cuenta como alerta si es raro para ese departamento y no es algo de todo el país.

(≈40 s) Segunda pregunta. Para cada departamento comparamos las quejas del mes con lo normal de sus seis meses anteriores. Después lo comparamos con lo que pasó en todo el país ese mismo mes, para no confundir un problema local con algo nacional. Si la subida se sale de lo habitual para ese departamento, la marcamos como alerta, usando la regla de Tukey, una forma estándar de detectar valores fuera de rango. Resultado: 11 alertas en 10 departamentos, menos del 2 % de los meses revisados.

*Si preguntan:* Esa comparación con el país se llama índice relativo. Para que dos o tres quejas no disparen una alerta en un departamento pequeño, exigimos al menos 100 quejas de referencia y 12 meses con datos.

## 16. El país crece sin saltos: nunca superó su umbral
*08 · Resultados P2*

**Idea clave:** A nivel país no hubo ninguna crisis: el crecimiento fue gradual.

(≈25 s) Esta es la serie de todo el país. Las quejas crecieron 29 % entre octubre de 2023 y septiembre de 2026, pero de forma gradual: el país nunca cruzó su propio umbral de alerta. La zona gris es el arranque de Smartsupervision, que no evaluamos, y los puntos marcan los meses con alerta en algún departamento.

## 17. 17 de las 20 alertas iniciales caían en 2023
*08 · Resultados P2*

**Idea clave:** Al principio las alertas detectaban el arranque del sistema, no problemas reales; lo corregimos.

(≈30 s) Esta fue una decisión importante. En la primera versión salían 20 alertas, y 17 estaban en 2023. No tenía sentido que ese fuera el peor año del banco: era el sistema nuevo empezando a reportar en cada departamento. Por eso dejamos fuera los primeros nueve meses de 2023. Quedaron 11 alertas, ninguna en 2023. Preferimos pocas alertas confiables a muchas falsas.

## 18. Los 11 picos fueron locales, ninguno nacional
*08 · Resultados P2*

**Idea clave:** Todos los picos fueron locales: el país estaba normal en cada caso.

(≈30 s) Cada fila es una alerta: el punto azul es cuánto subió el departamento y el gris cuánto subió el país ese mismo mes. En todos los casos el país estaba normal, o sea, fueron problemas locales. Los más fuertes: Meta, que subió 55 % en marzo de 2026, y Cauca, 53 % en abril. Risaralda tuvo dos meses seguidos con alerta, en 2024.

*Si preguntan:* En diciembre de 2025 y enero de 2026 subieron cinco departamentos a la vez con el país estable; valdría la pena revisar si tuvieron algo en común, como una campaña o un cambio de proceso.

## 19. Entre 9 y 13 alertas con cualquier umbral, todas locales
*08 · Resultados P2*

**Idea clave:** El resultado no depende del umbral que elegimos.

(≈25 s) ¿Y si hubiéramos elegido otro umbral? Exigimos que un departamento tenga al menos 100 quejas de referencia, para que unas pocas quejas no disparen alertas. Probamos con 30, 50, 100 y 200: salen entre 9 y 13 alertas, y siempre son locales. El resultado es estable.

## 20. 9 de los 10 departamentos con alerta superan la mediana
*08 · Resultados P2*

**Idea clave:** Los picos aparecen donde ya hay más quejas por cada oficina.

(≈30 s) Aquí sí usamos la división por puntos de atención: quejas al mes por cada 100 oficinas y cajeros. Nueve de los diez departamentos con alerta están por encima de la mediana, que es 462. O sea, son los primeros lugares para revisar. Bogotá aparece muy arriba, con 2.088, pero ese valor puede estar inflado por quejas digitales registradas en la capital.

## 21. La concentración del 83 % no depende de ningún supuesto
*09 · Limitaciones*

**Idea clave:** Lo principal se sostiene; lo que es estimado, lo decimos.

(≈30 s) ¿Qué tan firmes son los resultados? Lo central, sí: que ahorros y tarjeta concentren el 83 % sale de datos observados, sin supuestos. Lo que es estimado lo declaramos: las quejas fundadas desde 2023 son una estimación, los códigos de canal son una deducción nuestra, y las alertas son señales para investigar, no fallas confirmadas, porque no las cruzamos con información interna del banco.

*Si preguntan:* Somos tres integrantes y el enunciado pedía cinco; por eso nos concentramos en las tres primeras fases de CRISP-DM (entender el negocio, entender los datos y prepararlos) y no en construir un modelo.

## 22. Priorizar dos productos y revisar diez departamentos
*10 · Conclusiones*

**Idea clave:** Qué haría el banco con estos resultados.

(≈30 s) En concreto, le diríamos a Davivienda: primero, revisar la cuenta de ahorros y la tarjeta de crédito; segundo, revisar el funcionamiento de canales y cajeros, el motivo que más creció; tercero, entender qué pasa con el leasing no habitacional. Y para las alertas: preguntar a las regiones qué pasó en Meta, Cauca y Risaralda, y repetir el cálculo cada mes. El siguiente paso sería un modelo que anticipe la alerta antes de que ocurra.

## 23. Tres integrantes con experiencia en Davivienda, cinco reuniones
*11 · Trabajo en equipo*

**Idea clave:** Cómo nos organizamos como equipo.

(2 min) David y Fabian trabajan actualmente en Davivienda y Belky trabajó allí hace un tiempo, así que los tres llegamos con conocimiento del negocio, y eso nos ayudó a elegir las preguntas y a leer los resultados. David llevó la ingeniería de datos y apoyó la parte estadística; Belky y Fabian se repartieron el análisis estadístico y la comunicación. Nos reunimos una vez por semana, por lo general el día de la clase o al día siguiente, entre el 24 de octubre y el 18 de noviembre: cinco reuniones para tomar las decisiones grandes y mostrar avances. El día a día lo resolvíamos en nuestro grupo de WhatsApp, y una regla clave fue trabajar siempre sobre una sola versión del proyecto: si una cifra no salía del cuaderno, no la usábamos.

*Si preguntan:* En las reuniones definimos el caso de estudio y las preguntas, qué fuentes usar, cómo tratar los problemas de calidad y los criterios de las alertas. [Completar con el resumen de la autoevaluación y la evaluación de pares de la sección 9.4.]

## 24. Todo el análisis se reproduce desde el repositorio

**Idea clave:** Cerrar e invitar a preguntas.

(5 min de preguntas) Gracias. El cuaderno, los datos y la tabla final están en el repositorio, y cualquier cifra de esta presentación sale de una celda ejecutada. Quedamos atentos a sus preguntas.
