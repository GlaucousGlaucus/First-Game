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
