#  Backgammon - Proyecto Final Computación 2

## Descripción

Implementación completa del juego de mesa Backgammon con arquitectura modular, manejo robusto de errores, testing exhaustivo y dos interfaces de usuario:

- Interfaz gráfica con Pygame
- Interfaz por línea de comandos (CLI)

Incluye documentación técnica (`JUSTIFICACION.md`), registro de prompts usados con IA y cobertura de testing superior al 90%.

---

## Reglas Implementadas

- **Movimientos básicos**:
  - Mover fichas según valores de dados
  - Dirección específica según color (Blancas: 24→1, Negras: 1→24)
  - Uso de uno o dos dados por turno

- **Capturas**:
  - Un punto con una sola ficha puede ser capturado
  - Fichas capturadas van a la barra
  - Reingreso obligatorio desde barra antes de otros movimientos

- **Bloqueos**:
  - Puntos con 2+ fichas enemigas están bloqueados
  - No se puede mover a través de 6 puntos bloqueados consecutivos

- **Sacar fichas (Bear Off)**:
  - Permitido solo cuando todas las fichas están en el último cuadrante
  - Uso de dado exacto o mayor si no hay fichas más lejanas
  - Victoria al sacar todas las fichas

---

## Estructura del Proyecto
backgammon/ ├── core/                 # Lógica central del juego │   ├── board.py         # Tablero y reglas │   ├── game.py          # Flujo de partida │   ├── player.py        # Jugador │   ├── dice.py          # Dado │   ├── checker.py       # Ficha │   ├── excepciones.py   # Excepciones específicas │   └── src/             # Submódulos internos │ ├── cli/                 # Interfaz por consola │   └── main.py │ ├── pygame_ui/           # Interfaz gráfica con Pygame │   ├── main.py          # Pantalla de inicio │   ├── main_juego.py    # Lógica visual del juego │   ├── render.py        # Renderizado del tablero │   └── adaptador.py     # Adaptador visual del estado lógico │ ├── test/                # Tests unitarios │   ├── test_board.py │   ├── test_game.py │   ├── test_player.py │   ├── test_dice.py │   ├── test_checker.py │   └── test_cli.py │ ├── README.md ├── JUSTIFICACION.md ├── prompts-desarrollo.md ├── prompts-testing.md ├── prompts-documentacion.md └── requirements.txt



---

## Requerimientos

### Sistema
- Python 3.10 o superior
- Sistema operativo: Windows / Linux / MacOS

### Dependencias
- pygame==2.5.2
- coverage==7.4.3
- pylint (opcional para linting)

---

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu_usuario/backgammon-proyecto-final.git
cd backgammon-proyecto-final

- Crear y activar entorno virtual:
python -m venv venv

# Windows
venv\Scripts\activate


- Instalar dependencias:
pip install -r requirements.txt

Ejecución
Interfaz Gráfica (Pygame)
python pygame_ui/main.py



python pygame_ui/main.py


Interfaz por Consola (CLI)

python cli/main.py --modo interactivo --jugador1 Ian --jugador2 Bot

Opciones disponibles:
- --modo: interactivo, simulado, grafico
- --jugador1, --jugador2: nombres de los jugadores

Testing
Ejecutar tests
python -m unittest discover test



ver covertura
coverage run -m unittest discover
coverage report
coverage html  # Genera reporte visual

Cobertura actual: 90%
Tests quirúrgicos para board, game, player, checker, dice, CLI y simulación

Desarrollo
Linting
pylint core/ cli/ pygame_ui/ test/

Documentación
- Diseño técnico en JUSTIFICACION.md
- Registro de prompts usados con IA:
- prompts-desarrollo.md
- prompts-testing.md
- prompts-documentacion.md


Contribuciones
- Fork del repositorio
- Crear rama para feature/fix
- Commit con mensaje claro
- Pull request con descripción técnica

Licencia
MIT License — Ver LICENSE.md


Autor
Ian Kalik
 
---