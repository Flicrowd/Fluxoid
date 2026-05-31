# Fluxoid

A complete neon-styled desktop game developed by **Flicrowd**. The project features an immersive space aesthetic, atmospheric background music, and dynamic audio effects.

## 🚀 Key Features
* **Cohesive Visual Style:** Designed with a vibrant neon color palette that perfectly complements the deep space nebula background.
* **Custom Resolution:** The game window is optimized at **1060x600** px to provide an expanded field of view.
* **Refined Code Architecture:** 
  * Game physics and collision detection are calculated entirely using `pygame.Rect` modules.
  * Optimized keyboard input handling via logical state flags inside a unified event loop for fluid paddle movement.
* **Endless Replayability Loop:** The gameplay is fully cyclical. Upon hitting a Win or Game Over state, the game pauses and allows an instant reset by pressing the **ENTER** key.

## 🛠️ Requirements & Installation

1. Install the required dependencies using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the main entry point of the game:
   ```bash
   python main.py
   ```

---
*💡 Note for NixOS users: Before running the project, ensure your development environment includes Python 3 and the Pygame library (e.g., by initializing an isolated shell via `nix-shell -p python3Packages.pygame`).*
