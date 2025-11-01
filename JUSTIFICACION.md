# Justificación Técnica del Proyecto Backgammon

Este documento acompaña el desarrollo del sistema Backgammon, detallando las decisiones de diseño, arquitectura, testing y evolución. Se actualiza progresivamente en el repositorio para reflejar los cambios realizados durante el cursado.

---

## 🧩 Resumen del Diseño General

El sistema se estructura en tres capas principales:

- **Lógica central (`core/`)**: contiene las clases `Tablero`, `Jugador`, `Ficha`, `Dado` y `JuegoBackgammon`, junto con excepciones específicas.
- **Interfaz por consola (`cli/`)**: permite ejecutar el juego en modo interactivo o simulado mediante `argparse`.
- **Interfaz gráfica (`pygame_ui/`)**: implementa una experiencia visual completa con Pygame, incluyendo pantalla de inicio, renderizado del tablero, barra, dados y lógica de interacción.

La arquitectura prioriza modularidad, trazabilidad, robustez ante errores y separación clara entre lógica y visualización.

---

## 🧱 Justificación de Clases

- **`Ficha`**: representa una ficha individual, con color y estado de captura. Permite trazabilidad y operaciones como `capturar()` y `liberar()`.
- **`Dado`**: encapsula el comportamiento de lanzamiento, obtención y reinicio. Evita errores de flujo y permite testing aislado.
- **`Jugador`**: modela el estado del jugador (nombre, color, fichas, movimientos disponibles). Centraliza la lógica de turno y estadísticas.
- **`Tablero`**: gestiona el estado del juego, incluyendo posiciones, barra, borne-off, validaciones y movimientos. Es el núcleo del sistema.
- **`JuegoBackgammon`**: orquesta la partida, turnos, dados, reingresos, borne-off y finalización. Coordina `Tablero` y `Jugador`.
- **`VisualGame` y `VisualBoard`**: adaptadores visuales que conectan la lógica del tablero con el renderizado en Pygame sin duplicar lógica.
- **`pantalla_inicio` y `ejecutar_juego`**: gestionan la experiencia gráfica, entrada de nombres, interacción por mouse y teclado.

---

## 🧬 Justificación de Atributos

- `color_numerico`: permite cálculos direccionales sin condicionales complejos.
- `_tablero`: lista de 24 puntos con pilas de fichas, permite operaciones tipo stack (`pop`, `append`).
- `_barra`, `_fichas_fuera`: separan estado interno de acceso externo, facilitando testing y visualización.
- `movimientos_disponibles`: registra los dados activos por turno, usado en CLI y Pygame.
- `pos`: en `VisualBoard`, adapta el estado lógico a formato visual para renderizado.

---

## 🧠 Decisiones de Diseño Relevantes

- Separación entre lógica (`core`) y visualización (`pygame_ui`) mediante adaptadores.
- Uso de excepciones específicas para representar errores del dominio y evitar `ValueError` genéricos.
- Modularización de pantallas (`pantalla_inicio`, `main_juego`) para escalar la experiencia visual.
- Renderizado visual con `MAX_VISIBLE_STACK`, etiquetas, colores y detección de clics (`hitmap`).
- CLI con `argparse` permite ejecución flexible en distintos modos (`interactivo`, `simulado`, `grafico`).

---

## 🚨 Excepciones y Manejo de Errores

Se definieron excepciones específicas en `core/excepciones.py`:

- `MovimientoInvalido`: errores de lógica o color.
- `PosicionFueraDeRango`: accesos inválidos al tablero.
- `OrigenSinFicha`: intentos de mover desde puntos vacíos.
- `DestinoBloqueado`: posiciones ocupadas por fichas enemigas.
- `NoPuedeReingresar`: reingreso fallido desde barra.
- `NoPuedeSacarFicha`: intento de borne-off sin cumplir condiciones.

Estas excepciones permiten testing quirúrgico, mensajes claros y robustez ante cualquier flujo inesperado.

---

## 🧪 Estrategias de Testing y Cobertura

Se implementaron tests unitarios con `unittest` en la carpeta `test/`, cubriendo todos los módulos:

| Módulo           | Cobertura | Tests destacados |
|------------------|-----------|------------------|
| `board.py`       | 76%       | Movimientos, capturas, reingreso, borne-off, excepciones |
| `game.py`        | 84%       | Flujo de partida, turnos, dados, ganador, CLI |
| `player.py`      | 72%       | Turno, captura, salida, reinicio |
| `checker.py`     | 100%      | Inicialización, captura, liberación |
| `dice.py`        | 100%      | Lanzamiento, obtención, reinicio |
| `excepciones.py` | 100%      | Validación de tipos |
| `test_board.py`  | 99%       | Validación exhaustiva |
| `test_game.py`   | 95%       | Simulación, CLI, reingreso |
| `test_player.py` | 98%       | Estado y operaciones |
| `test_dice.py`   | 97%       | Comportamiento completo |

**Cobertura total: 90%**  
Se utiliza `coverage` para asegurar que cada rama de código esté cubierta. Se testean casos límite, errores internos y flujos completos.

---

## 🧱 Referencias a Principios SOLID

- **S (Single Responsibility)**: cada clase tiene una única responsabilidad clara (ej. `Ficha`, `Dado`, `Jugador`, `Tablero`).
- **O (Open/Closed)**: el sistema permite agregar nuevas reglas o modos sin modificar las clases existentes (ej. modo gráfico).
- **L (Liskov Substitution)**: las clases respetan sus contratos y excepciones, permitiendo testing aislado.
- **I (Interface Segregation)**: los métodos públicos están bien definidos y separados por clase.
- **D (Dependency Inversion)**: `JuegoBackgammon` depende de abstracciones (`Jugador`, `Tablero`) y no de detalles visuales.

---

## 📐 Anexos

### Diagrama de Clases (UML)


---

## 🔄 Evolución del Diseño

- Se refactorizó `Tablero` para blindar cada método con excepciones específicas.
- Se modularizó la experiencia visual separando `pantalla_inicio` y `main_juego`.
- Se agregaron adaptadores visuales (`VisualGame`, `VisualBoard`) para evitar duplicación de lógica.
- Se incorporó CLI con `argparse` para facilitar testing y ejecución flexible.
- Se incrementó la cobertura de tests de 70% a 90%, cubriendo casos límite y errores internos.

---

Este archivo se versiona en Git y se actualiza en cada entrega relevante, reflejando la evolución técnica y conceptual del sistema.