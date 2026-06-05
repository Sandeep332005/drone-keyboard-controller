# Drone Keyboard Controller

A real-time keyboard-controlled drone interface built with Python, `tkinter`, and `pysimverse`.

## Features

- Live RC control via keyboard with ~100ms update loop
- Take off, land, and quit with single keypresses
- Status display in GUI window
- Safe shutdown — auto-lands if window is closed while flying

## Controls

| Key | Action |
|-----|--------|
| `T` | Take off |
| `L` | Land |
| `W` / `S` | Forward / Backward |
| `A` / `D` | Left / Right |
| `↑` / `↓` | Altitude Up / Down |
| `←` / `→` | Rotate Left / Right |
| `Q` | Quit |

## Requirements

- Python 3.8+
- `pysimverse`
- `tkinter` (bundled with standard Python on most systems)

## Installation

```bash
git clone https://github.com/Sandeep332005/drone-keyboard-controller.git
cd drone-keyboard-controller
pip install -r requirements.txt
```

## Usage

```bash
python controller.py
```

> **Important:** Click the GUI window first before using keyboard controls — tkinter needs focus to capture keypresses.

## Configuration

Edit the constants at the top of `controller.py`:

```python
MOVE_SPEED = 50          # RC movement speed (0–100)
YAW_SPEED = 50           # Rotation speed (0–100)
UPDATE_INTERVAL_MS = 100 # Control loop interval in milliseconds
```

## Architecture

```
KeyboardDroneController
├── __init__()        — connects drone, builds tkinter UI
├── on_key_press()    — handles takeoff / land / quit / movement keys
├── on_key_release()  — removes key from active set
├── get_rc_values()   — maps active_keys → (lr, fb, ud, yaw) tuple
├── control_loop()    — tkinter after() loop, sends RC every 100ms
├── stop_motion()     — zeroes all RC channels
└── on_close()        — safe shutdown with auto-land
```

## Author

**Sandeep Kumar**
- GitHub: [@Sandeep332005](https://github.com/Sandeep332005)
- LinkedIn: [linkedin.com/in/sandeep-kumar-0971b4302](https://linkedin.com/in/sandeep-kumar-0971b4302)

## License

MIT License — see [LICENSE](LICENSE)
