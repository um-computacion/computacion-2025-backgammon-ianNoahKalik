#  Prompts utilizados para el desarrollo del sistema

Este archivo documenta los intercambios con herramientas de IA utilizados para revisar, corregir y mejorar partes del código durante el desarrollo del sistema Backgammon. El código base fue escrito por el alumno, y la IA fue utilizada como asistente técnico para refactorizar, blindar y validar secciones específicas.

---

##  Prompt 1: Revisión y blindaje de la clase `Tablero`

- **Herramienta usada**: Microsoft Copilot  
- **Prompt exacto**:  
  > Esta es mi clase Tablero para Backgammon. Ya tengo la estructura básica con 24 puntos, fichas, barra y borne-off. Pero quiero que me ayudes a revisar si el método mover_pieza está bien blindado. También quiero que me digas si hay alguna validación que falta o si puedo mejorar la forma en que manejo las capturas y excepciones.

- **Respuesta de la IA**:  
  - Sugirió agregar `validar_movimiento()` antes de ejecutar `sacar_pieza()`
  - Propuso blindar `reingresar_desde_barra()` con validación de destino bloqueado
  - Recomendó separar `todas_en_home()` para facilitar el borne-off
  - Propuso usar `ficha.color` en lugar de comparar con constantes

- **Uso de la salida**:  
  Usada con modificaciones.

- **Archivo final**:  
  `core/board.py`

---

##  Prompt 2: Corrección de lógica en `JuegoBackgammon`

- **Herramienta usada**: Microsoft Copilot  
- **Prompt exacto**:  
  > Ya tengo la clase JuegoBackgammon con los métodos para lanzar dados, cambiar turno y jugar en modo interactivo. Pero en el método jugar_partida_interactiva tengo problemas cuando hay fichas en la barra. A veces no se reingresan bien o se saltea el turno. ¿Podés revisar esa parte y decirme cómo blindarla mejor?

- **Respuesta de la IA**:  
  - Detectó que faltaba validación de `puede_reingresar()` antes de permitir movimientos normales
  - Sugirió agregar un contador de intentos para evitar loops infinitos
  - Recomendó mostrar mensajes claros cuando se pierde un dado por no poder mover

- **Uso de la salida**:  
  Usada con modificaciones.

- **Archivo final**:  
  `core/game.py`

---

##  Prompt 3: Corrección visual en renderizado de tablero

- **Herramienta usada**: Microsoft Copilot  
- **Prompt exacto**:  
  > Ya tengo el render_board funcionando en Pygame, pero quiero que me ayudes a mejorar cómo se apilan las fichas. A veces se superponen o no se ven bien cuando hay más de 5. También quiero que se muestre un número si hay más fichas ocultas. ¿Podés revisar esa parte?

- **Respuesta de la IA**:  
  - Propuso usar `MAX_VISIBLE_STACK` y calcular `extras` para mostrar cantidad oculta
  - Sugirió usar `draw_checker()` con parámetro `label` para mostrar el número
  - Recomendó ajustar `step` y `radius` para evitar superposición

- **Uso de la salida**:  
  Usada con modificaciones.

- **Archivo final**:  
  `pygame_ui/render.py`

---

##  Prompt 4: Validación de pantalla de inicio en Pygame

- **Herramienta usada**: Microsoft Copilot  
- **Prompt exacto**:  
  > Ya tengo la pantalla de inicio en Pygame con campos para ingresar los nombres. Pero quiero que me ayudes a validar que no se pueda empezar la partida si falta algún nombre. También quiero que se muestre un mensaje de error si eso pasa. ¿Podés revisar esa parte?

- **Respuesta de la IA**:  
  - Sugirió usar `.strip()` para validar campos vacíos
  - Propuso agregar `mensaje_error` y mostrarlo con `font.render()`
  - Recomendó centrar el botón y ajustar los colores

- **Uso de la salida**:  
  Usada con modificaciones.

- **Archivo final**:  
  `pygame_ui/main.py`

---

##  Prompt 5: Revisión de adaptador visual

- **Herramienta usada**: Microsoft Copilot  
- **Prompt exacto**:  
  > Esta es mi función adaptar_tablero. Convierte el estado del tablero en formato visual. ¿Podés revisar si está bien hecho y si hay alguna forma más clara de detectar el color de las fichas sin romper la lógica?

- **Respuesta de la IA**:  
  - Sugirió usar `punto[0].es_blanca()` y `es_negra()` en lugar de comparar con strings
  - Recomendó agregar un fallback visual en caso de error

- **Uso de la salida**:  
  Usada con modificaciones.

- **Archivo final**:  
  `pygame_ui/adaptador.py`

  