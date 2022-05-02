"""
This is a game called Treato Dreams.

A dog has fallen asleep and begins dreaming of being in the park
with treats falling from the sky.

The goal of the game is to eat treats but to avoid vegetables.

"""

import pygame
import os
import time
import random

# Load Images

BACKGROUND = pygame.image.load(os.path.join('treato-dreaming', 'background.png'))
DOG_CLOSED_MOUTH = pygame.image.load(os.path.join('treato-dreaming', 'dog_closed_mouth.png'))
DOG_OPEN_MOUTH = pygame.image.load(os.path.join('treato-dreaming', 'dog_open_mouth.png'))
BURGER = pygame.image.load(os.path.join('treato-dreaming', 'burger.png'))
CHICKEN_NUGGETS = pygame.image.load(os.path.join('treato-dreaming', 'chicken_nuggets.png'))
