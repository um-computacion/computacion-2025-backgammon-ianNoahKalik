#  Prompts utilizados para testing del sistema

Este archivo documenta los intercambios con herramientas de IA utilizados para mejorar la cobertura de tests, blindar casos límite y validar excepciones. El alumno escribió los primeros tests, y la IA fue utilizada como asistente técnico para completar la cobertura y asegurar robustez.

---

##  Prompt 1: Corrección de test fallido de borne-off

- **Herramienta usada**: Microsoft Copilot  
  Versión: Octubre 2025  
  Plataforma: Windows 11 + Copilot integrado

- **Prompt exacto**:  
  > FAIL: test_borneo_no_permitido_por_fichas_fuera_de_zona (main.TestJuegoBackgammon.test_borneo_no_permitido_por_fichas_fuera_de_zona)  
  > Traceback (most recent call last):  
  > File "test_game.py", line 217, in test_borneo_no_permitido_por_fichas_fuera_de_zona  
  > self.assertEqual(self.juego.jugador_blanco.fichas_salidas, 0)  
  > AssertionError: 1 != 0  
  > Ran 40 tests in 0.028s  
  > FAILED (failures=1)

- **Instrucciones del sistema**:  
  Solicité ayuda para corregir el test que fallaba, asegurando que el borne-off no se permitiera si había fichas fuera de la zona.

- **Respuesta de la IA**:  
  Explicó que el método `puede_bornear()` no estaba bloqueando correctamente el borne-off si había fichas fuera de la zona. Propuso un test corregido que vacía los puntos 18 a 23 y coloca una ficha en el punto 10 para validar que no se pueda bornear.

- **Uso de la salida**:  
   Usada con modificaciones menores (ajusté el punto y el dado según mi lógica interna)

- **Archivos afectados**:  
  - `test/test_game.py`  
  - `core/game.py`

---

##  Prompt 2: Subir cobertura de `core/game.py` al 90%

- **Herramienta usada**: Microsoft Copilot  
  Versión: Octubre 2025  
  Plataforma: Windows 11 + Copilot integrado

- **Prompt exacto**:  
  > Agregué los 10 tests pero sigue en el 69%, mirá:  
  > coverage report  
  > Name                    Stmts   Miss  Cover  
  > core/game.py              116     36    69%

- **Instrucciones del sistema**:  
  Solicité ayuda para subir la cobertura de `core/game.py` con tests quirúrgicos que activen ramas internas no cubiertas.

- **Respuesta de la IA**:  
  Propuso tests para:
  - excepción al mover ficha a destino bloqueado  
  - reingreso desde barra exitoso  
  - jugador con ficha capturada y luego reingresada  
  - jugador sin movimientos válidos  
  - jugador con todas las fichas fuera (ganador)

- **Uso de la salida**:  
   Usada con modificaciones (ajusté los puntos y dados según mi lógica)

- **Archivos afectados**:  
  - `test/test_game.py`  
  - `core/game.py`

---

##  Prompt 3: Blindaje de tests para `Tablero`

- **Herramienta usada**: Microsoft Copilot

- **Prompt exacto**:  
  > Ya hice algunos tests para Tablero, como mover fichas y mostrar el tablero. Pero quiero que me ayudes a cubrir todos los métodos, especialmente los que lanzan excepciones como PosicionFueraDeRango, OrigenSinFicha, MovimientoInvalido, etc. También quiero que el coverage llegue al 90%.

- **Respuesta de la IA**:  
  Propuso tests para:
  - `sacar_pieza`, `colocar_pieza`, `reingresar_desde_barra`, `sacar_ficha_fuera`, `todas_en_home`, `puede_reingresar`  
  - Uso de `assertRaises` para validar excepciones  
  - Separación de casos válidos y fallidos

- **Uso de la salida**:  
   Usada con modificaciones. Se mantuvo la estructura original del alumno, se agregaron los tests quirúrgicos sugeridos.

- **Archivo afectado**:  
  - `test/test_board.py`

---

##  Prompt 4: Tests para `Jugador` y flujo de turno

- **Herramienta usada**: Microsoft Copilot

- **Prompt exacto**:  
  > Ya tengo la clase Jugador con nombre, color y movimientos. Hice un test para inicialización. ¿Podés ayudarme a testear sacar_ficha, reiniciar_turno y __str__?

- **Respuesta de la IA**:  
  Propuso tests para:
  - `sacar_ficha()` con y sin fichas  
  - `reiniciar_turno()` usando `MagicMock`  
  - Validación del texto generado por `__str__()`

- **Uso de la salida**:  
   Usada con modificaciones. Se mantuvo el test original y se agregaron los casos sugeridos.

- **Archivo afectado**:  
  - `test/test_player.py`

---

Este archivo se actualiza con cada interacción relevante durante el testing. Se complementa con `prompts-desarrollo.md` y `prompts-documentacion.md`.