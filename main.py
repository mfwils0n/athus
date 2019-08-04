import pygame
import random
from states import *
from gamedriver import *
#Jackie was here
#get out of my swamp

pygame.init()

run = True
is_menu = True
gameMode = 0

while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	if is_menu:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				is_menu = False
				run = False

		gameMode = showGoScreen()
		is_menu = False

	else:
		if gameMode == 0:
			playSingle()
		elif gameMode == 1:
			playMulti()

		is_menu = True

pygame.quit()