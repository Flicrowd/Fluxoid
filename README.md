<p align="center">
  <img src="Fluxoid_Logo.png" alt="Fluxoid Logo" width="160" height="160">
</p>

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

Install the required dependencies using the `requirements.txt` file based on your OS:

* **Windows:**
  ```cmd
  pip install -r requirements.txt
  ```
* **Linux / macOS:**
  ```bash
  pip3 install -r requirements.txt
  ```

 ## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

