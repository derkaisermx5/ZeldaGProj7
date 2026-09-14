# Zelda Game Project 7

A Python-based game inspired by *The Legend of Zelda*, built with Pygame. This project combines previous assignments (4 & 6) and introduces interactive gameplay with a hostile Cucco sprite system.

## Features

### Core Gameplay
- **Link Character**: Navigate the game world using arrow keys
- **Collectibles**: Gather treasure chests containing rupees to increase your score
- **Obstacles**: Avoid trees that block movement
- **Boomerang Weapon**: Press SPACE to throw a boomerang in the direction Link is facing
- **Room Scrolling**: Dynamic camera system that follows Link as he moves between rooms

### Interactive Elements
- **Treasure Chests**: 
  - Contact a closed chest to open it and reveal a rupee
  - Collect the rupee to increase your rupee counter
  
- **Cucco Sprites**:
  - Peaceful when not provoked (wander around the map)
  - Become aggressive after being hit 5 times (by Link or boomerangs)
  - Angry cuccos chase Link across the screen
  - Disappear after 3 seconds of pursuit

### Edit Mode
Enable edit mode (press **E**) to place items on the map:
- **Trees**: Snap to a 75-pixel grid for organized placement
- **Treasure Chests**: Place freely
- **Cuccos**: Add additional birds to the game world

## Controls

| Key | Action |
|-----|--------|
| **Arrow Keys** | Move Link (Left, Right, Up, Down) |
| **SPACE** | Throw boomerang in Link's facing direction |
| **E** | Toggle Edit Mode |
| **C** | Clear map and reset game |
| **L** | Load saved map |
| **S** | Save current map |
| **ESC / Q** | Quit game |

## Edit Mode

In Edit Mode:
- The background changes to **light green** to indicate you're in editing mode
- A **green box** appears in the top-left corner showing the currently selected item
- **Click the green box** to cycle through available items (Trees → Treasure Chests → Cuccos)
- **Click anywhere else** on the map to place the selected item
- Return to play mode by pressing **E** again

## Project Structure

```
ZeldaGProj7/
├── game.py          # Main game file containing all game logic and classes
├── map.json         # Saved game map with sprite positions and Link's location
└── images/          # Game assets (sprites for Link, trees, chests, cuccos, boomerangs, rupees)
```

## Classes

### Sprite
Base class for all game objects with collision detection and rendering capabilities.

### Link
The player character with:
- 4-directional movement with animation
- Collision detection and handling
- Rupee collection tracking

### Tree
Static obstacles that block Link's movement.

### TreasureChest
Collectible items that:
- Open on contact with Link
- Display a rupee that can be collected
- Disappear after the rupee is collected

### Boomerang
Throwable weapon that:
- Travels in the direction Link faces
- Opens treasure chests on contact
- Is destroyed when hitting trees or chests

### Cucco
Dynamic enemy that:
- Wanders peacefully until provoked
- Becomes hostile after 5 hits
- Chases Link when angry
- Disappears after a pursuit timeout

### Model
Game state manager handling:
- Sprite management
- Collision detection and resolution
- Map saving/loading (JSON format)

### View
Rendering system that:
- Draws all sprites to the screen
- Manages camera/room scrolling
- Displays rupee counter and edit mode UI

### Controller
Input handler managing:
- Keyboard input for movement and actions
- Mouse input for placing items in edit mode
- Game state transitions

## How to Run

1. Ensure you have Python 3 and Pygame installed:
   ```bash
   pip install pygame
   ```

2. Place the `images/` directory with all game sprites in the same folder as `game.py`

3. Run the game:
   ```bash
   python game.py
   ```

## Game Objective

- Collect as many rupees as possible by finding and opening treasure chests
- Avoid collisions with trees and hostile cuccos
- Use the boomerang strategically to damage cuccos before they become too dangerous
- Save your favorite maps for later play!

## Technical Highlights

- **Object-Oriented Design**: Clean class hierarchy for easy extensibility
- **Collision Detection**: AABB (Axis-Aligned Bounding Box) collision system
- **Animation System**: Frame-based sprite animation for character movement and item effects
- **Map Persistence**: JSON-based save/load system for game state
- **Dynamic Camera**: Room-based scrolling system for larger worlds
- **AI Behavior**: Distance-based pathfinding for pursuing cuccos

## Author

Jared Ramirez  
*Assignment 7 - Date: 11/29/2025*

---

Enjoy your adventure in this Zelda-inspired world! 🗡️ 🏆
