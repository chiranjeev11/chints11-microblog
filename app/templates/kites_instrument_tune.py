import pygame
import os

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('Dil Q ye mera flute.mp3')

pygame.mixer.music.play(loop=-1)