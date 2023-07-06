import pygame
import os

dirt_1 = pygame.image.load("sprites/dirt_1.png")

class Animation():
    def __init__(self, animation_frames, duration, key) -> None:
        self.frames = animation_frames
        self.frame_count = len(animation_frames)
        self.duration = duration
        self.base_duration = duration
        self.key = key


animation_dict = {}

# load animations and add them to the animation_dict
def load_animation(path, duration):
    for i in os.listdir(path):
        if i.endswith(".png"):
            animation = [pygame.image.load(f"{path}/{i}") for i in os.listdir(path)]
        

    if path.split("/")[-1] not in animation_dict:
        animation_dict[path.split("/")[-1]] = Animation(animation, duration, path.split("/")[-1])
        return
    
    else:
        raise Exception("Animation already exists")
    

# frame independent animation
def animate(self, animation, dt):
    animation.duration -= dt
    if animation.duration <= 0:
        animation.duration = animation.base_duration
        animation.frames.append(animation.frames.pop(0))

    self.image = animation_dict[animation.key].frames[0]

    return animation.frames[0]


# this is ugly but it works
grass_neighbors = [
    (False, False, False, False),
    (True, False, False, True),
    (False, False, True, True),
    (False, False, False, True),
    (False, True, False, True),
    (False, True, True, True),
    (True, True, True, True),
    (True, True, True, False),
    (True, False, True, False),
    (True, False, True, True),
    (True, False, False, False),
    (False, False, True, False),
    (False, True, False, False),
    (True, True, False, True),
    (True, True, False, False),
    (False, True, True, False),
]

# load grass images
grass_images = {}
for i, v in enumerate(grass_neighbors):
    grass_images[v] = pygame.image.load(f"sprites/grass/grass_{i + 1}.png")
