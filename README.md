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
Using Clock
```python
clock = pygame.time.Clock() # This will give a clock object
# In While loop
clock.tick(60) # Caps fps at 60
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

```python
# Surfaces
# Creating surfaces
S1Width, S1Hight = 200, 300
Test_Surface = pygame.Surface((S1Width, S1Hight)) # Same as creating the screen
# Images
Sky_Surface = pygame.image.load('Resources\Images\Sky.png')
Ground_Surface = pygame.image.load('Resources\Images\ground.png')
# Text
Text_Surface = test_font.render('Dungeon Run', False, 'Black') # .render(text, Anti-Alias(Smooth edges), color)

# Displaying the Surfaces

# To attach the regular surafce with the display surface
# Needs two arguments (The surface, the position)
# screen.blit(Test_Surface, (200, 100)) # BlIT: Block Image Transfer | You put one surface on top of another surface.
# Here sky is rendered below the ground
screen.blit(Sky_Surface, (0, 0))
screen.blit(Ground_Surface, (0, 300))
screen.blit(Text_Surface, (300, 50))
```

[**Color Codes**](https://htmlcolorcodes.com/color-names/)
