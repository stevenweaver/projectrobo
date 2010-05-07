import pygame
pygame.init()
music = pygame.mixer.Sound('/home/steven/tmnt.wav')
music.play()
music.set_volume(0.9) 

while 1:
    x = 1
