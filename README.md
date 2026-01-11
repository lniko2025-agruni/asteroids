# Asteroids

A fast-paced **Asteroids-style** arcade game built with **Python + Pygame**.  
Dodge falling meteors, shoot them for points, collect powerups, and survive enemy ship attacks.

---

## Features

- **Player movement + shooting**
  - Move with arrow keys
  - Shoot with Space

- **Asteroids / Meteors**
  - Meteors fall from the top at random positions
  - Colliding with a meteor damages the player

- **Score system**
  - +10 score per meteor destroyed
  - +50 score per enemy ship destroyed

- **Lives UI (Hearts)**
  - Player starts with **3 lives**
  - Max lives cap (default: **5**)

- **Powerups**
  - Temporary boost (faster movement + faster shooting)
  - Visual pulse ring effect when powered up

- **Enemy ship**
  - Spawns periodically near the top
  - Moves left → right
  - Shoots lasers that damage the player
  - Requires **3 hits** to be destroyed

---

## Controls

| Action | Key |
|-------|-----|
| Move | Arrow Keys |
| Shoot | Space |
| Start game | Space (on start screen) |
| Restart | R (on game over screen) |
| Quit | ESC / Q |

---

## Setup and Installation:

```bash
py -m venv .venv
.venv/Scripts/activate # On Windows
source .venv/bin/activate # On macOS/Linux
pip install -r requirements.txt
````

---

## Run the Game

From your project root:

```bash
py code/main.py
```

---



## Gameplay Notes

* **Meteor hit = -1 life**
* **Enemy laser hit = -1 life** (if enemy ship enabled)
* Falling heart pickups can restore lives up to `max_lives`

---
