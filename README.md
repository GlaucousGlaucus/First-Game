# First Python Game using Pygame

[Tut Video](https://www.youtube.com/watch?v=AY9MnQ4x3zk&t=19s)

**The Event Loop:** Checking Player input
## What Pygame does

- It helps you draw images. (and play sounds)
- Check for player inputs.
	* `input()` function just stops your code and is thus useless for games.
- Good with collision detection
## Installing Pygame
`pip install pygame`

## Creating a blank window
```python
import  pygame

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
```
> The window is created but closes as our code ends after python executes the screen code and Hence, our program stops. We need to use a a `while True` loop to keep it going 

### Controlling the Framerate

*FPS can change the animation speed and make it inconsistent*

```mermaid
flowchart
	A(Low/Unplayable Framerate) --> C(can change the animation speed / make it inconsistent)
	B(Extremely High Framerate) --> C
```
## Displaying Images 

```mermaid
flowchart
	A(Surface) --> B(Display Surface)
	A --> C(Regular Surface) 
	B --> D(The game window.\n Anything displayed goes on here)
	C --> E(Basically a single image. \n Something imported,\n rendered text or a plain color) 
	E --> F(Needs to be put on display surface to be visible)
	D --> G(Must be Unique \n Is always Visible)
	F --> H(only displayed when conntected to the display surface)
```
