from __future__ import division
import pygame
import random
import time
import sys
import array
from characters import *
from states import *


pygame.init()

clock = pygame.time.Clock()
sw = 700
sh = 512
base = 380

win = pygame.display.set_mode((sw, sh))
#window caption
pygame.display.set_caption("athus")
#list of images for the background (will be chosen at random)
bg = [pygame.image.load('bgp-1.jpg'), pygame.image.load('bgp-2.jpg'), pygame.image.load('bgp-3.jpg'), pygame.image.load('bgp-4.jpg'), pygame.image.load('bgp-5.jpg'), pygame.image.load('bgp-6.jpg'), pygame.image.load('bgp-7.jpg'), pygame.image.load('bgp-8.jpg'), pygame.image.load('bgp-9.jpg'), pygame.image.load('bgp-10.jpg'), pygame.image.load('bgp-11.jpg'), pygame.image.load('bgp-12.jpg'), pygame.image.load('bgp-13.jpg'), pygame.image.load('bgp-14.jpg'), pygame.image.load('bgp-15.jpg'), pygame.image.load('bgp-16.jpg'), pygame.image.load('bgp-17.jpg'), pygame.image.load('bgp-18.jpg'), pygame.image.load('bgp-19.jpg')]
#random number from 0 to 18 that corresponds to a background image
lotto = random.randint(0,18)
#system clock
clock = pygame.time.Clock()

athus = player1(600, base, 64, 64, 0)
agnath = player2(36, base, 64, 64)
oleste = enemy1(-80, base, 64, 64, sw - 74)
etro = enemy2(-80, base, 64, 64, sw - 74)
scoring = True
p1lasers = []
p2lasers = []
enemy_lasers = []

going = True

def change_to_menu():
	global is_menu 
	is_menu = True

def playSingle():
	mode = 0
	athus.mode = mode
	athus.score = 0

	global going
	global lotto
	global base
	global scoring

	soundOn = True
	soundEffectsOn = True
	lotto = random.randint(0, 18)

	game_time = pygame.time.get_ticks()
	game_start_time = pygame.time.get_ticks()
	timescore = 0
	time_since_hit = 0
	shootLoop = 0
	laserLoop = 0
	pause = False

	going = True

	while going:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		clock.tick(36)

		if athus.loop > 0:
			athus.loop += 1
		if athus.loop > 10:
			athus.loop = 0

		if laserLoop > 0:
			laserLoop += 1
		if laserLoop > 5:
			laserLoop = 0

		if athus.health == 0:
			athus.healthboxColor = (255, 0, 0)
			pygame.display.update()
			endGame("x", athus.score, mode)

		keys = pygame.key.get_pressed()

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
				change_to_menu()
				going = False

		if keys[pygame.K_p]:
			scoring = False
			pauseGame(mode)

		# ATHUS SCOREKEEPING #

		timealive = round((pygame.time.get_ticks() - game_start_time) / 1000)
		if timescore < timealive:
			temp = timealive - timescore
			athus.score += 1
		timescore = round((pygame.time.get_ticks() - game_start_time) / 1000)

		# ATHUS MOVEMENT #

		if keys[pygame.K_LEFT] and athus.x > athus.vel:
			athus.x -= athus.vel
			athus.left = True
			athus.right = False
			athus.standing = False

		elif keys[pygame.K_RIGHT] and athus.x < sw - athus.width - athus.vel:
			athus.x += athus.vel
			athus.right = True
			athus.left = False
			athus.standing = False

		else:
			athus.standing = True
			athus.walkCount = 0

		if not (athus.isJump):
			athus.y = base
			if keys[pygame.K_UP]:
				athus.isJump = True
				
		else:
			if athus.jumpCount >= -10:
				neg = 1
				if athus.jumpCount < 0:
					neg = -1
				athus.y -= (athus.jumpCount ** 2) * 0.5 * neg
				athus.jumpCount -= 1

			else:
				athus.isJump = False
				athus.jumpCount = 10

		if keys[pygame.K_SPACE] and athus.loop == 0:
			i = 0
			athus.isShooting = True
			if athus.left:
				facing1 = -1
				i = 2
			else:
				i = 62
				facing1 = 1

			if len(p1lasers) < 3:
				# athusLaserSound.play()
				p1lasers.append(projectile1(athus.x + i, athus.y + 30, 2, 200, (255,0,0), facing1))
				athus.loop = 1

		# ATHUS COMBAT #

		if pygame.time.get_ticks() - athus.timeSinceHit > 300:
			athus.isInvincible = False

		# etro hitting athus

		if etro.visible:
			if athus.hitbox[1] < etro.hitbox[1] + etro.hitbox[3] and athus.hitbox[1] + athus.hitbox[3] > etro.hitbox[1]:
				if athus.hitbox[0] + athus.hitbox[2] > etro.hitbox[0] and athus.hitbox[0] < etro.hitbox[0] + etro.hitbox[2]:
					display_damage = True
					athus.hit()
					time_since_hit = pygame.time.get_ticks()
					athus.isInvincible = True
		
		# oleste hitting athus

		if oleste.visible:
			if athus.hitbox[1] < oleste.hitbox[1] + oleste.hitbox[3] and athus.hitbox[1] + athus.hitbox[3] > oleste.hitbox[1]:
				if athus.hitbox[0] + athus.hitbox[2] > oleste.hitbox[0] and athus.hitbox[0] < oleste.hitbox[0] + oleste.hitbox[2]:
					display_damage = True
					athus.hit()
					time_since_hit = pygame.time.get_ticks()
					athus.isInvincible = True

		# athus shooting

		for laser1 in p1lasers:
			etro_dead = False
			oleste_dead = False

			# athus shooting etro

			if laser1.y - laser1.radius < etro.hitbox[1] + etro.hitbox[3] and laser1.y + laser1.radius > etro.hitbox[1]:
				if laser1.x + laser1.radius > etro.hitbox[0] and laser1.x - laser1.radius  < etro.hitbox[0] + etro.hitbox[2]:
					etro.hit()
					athus.score += 1
					if etro.health == 1:
						athus.score += 20
					if len(p1lasers) > 0:
						try:
							p1lasers.pop(p1lasers.index(laser1))
						except(ValueError):
							print(ValueError)
					
			# athus shooting oleste

			if laser1.y - laser1.radius < oleste.hitbox[1] + oleste.hitbox[3] and laser1.y + laser1.radius > oleste.hitbox[1]:
				if laser1.x + laser1.radius > oleste.hitbox[0] and laser1.x - laser1.radius  < oleste.hitbox[0] + oleste.hitbox[2]:
					oleste.hit()
					athus.score += 1
					if oleste.health == 1:
						athus.score += 10
					if len(p1lasers) > 0:
						try:
							p1lasers.pop(p1lasers.index(laser1))
						except(ValueError):
							print(ValueError)

			if laser1.x < sw and laser1.x > 0:
				laser1.x += laser1.vel
			else:
				try:
					p1lasers.pop(p1lasers.index(laser1))
				except(ValueError):
					print(ValueError)

		# ETRO COMBAT #

		if (etro.walkCount//3) == 12 and laserLoop == 0:
			i = 0
			if etro.left:
				efacing = -1
				i = 2
			else:
				efacing = 1
				i = 60
			if len(enemy_lasers) < 4:
				enemy_lasers.append(projectile3(etro.x + i, etro.y + 52, 3, 1, (179,255,255), efacing))
				laserLoop = 1
				# etroLaserSound.play()

		# etro shooting athus
		
		for elaser in enemy_lasers:
			if athus.hitbox[1] < elaser.y + elaser.radius and athus.hitbox[1] + athus.hitbox[3] > elaser.y:
				if athus.hitbox[0] + athus.hitbox[2] > elaser.x + elaser.radius and athus.hitbox[0] < elaser.x + elaser.radius:
					display_damage = True
					athus.hit()
					athus.isInvincible = True
					if len(enemy_lasers) > 0:
						enemy_lasers.pop(enemy_lasers.index(elaser))

			if elaser.x < sw and elaser.x > 0:
				elaser.x += elaser.vel
			else:
				enemy_lasers.pop(enemy_lasers.index(elaser))

		redrawWindow(mode)

def playMulti():
	mode = 1
	athus.mode = mode
	resetGameState(mode)
	global going
	global lotto
	global base

	score = 0
	nSeconds = 30
	eCount = 0
	oCount = 0
	nCount = 0
	soundOn = True
	soundEffectsOn = True
	timer = 0
	lotto = random.randint(0, 18)
	gameover = False
	dropping = False

	olesteOn = False
	nodonOn = False
	etroOn = False
	display_damage = False
	addscore = 0
	time_since_hit = 0
	shootLoop = 0
	laserLoop = 0
	pause = False

	dto = 0
	dte = 0
	dtn = 0

	going = True

	while going:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		# t0e = time.clock()
		# t0n = time.clock()
		# t0o = time.clock()

		clock.tick(36)

		if athus.health == 0:
			athus.healthboxColor = (255, 0, 0)
			pygame.display.update()

			winner = "PLAYER 2 "
			endGame(winner, 0, mode)
		if agnath.health == 0:
			agnath.healthboxColor = (255, 0, 0)		
			pygame.display.update()

			winner = "PLAYER 1 "
			endGame(winner, 0, mode)

		if athus.loop > 0:
			athus.loop += 1
		if athus.loop > 10:
			athus.loop = 0

		if agnath.loop > 0:
			agnath.loop += 1
		if agnath.loop > 10:
			agnath.loop = 0

		keys = pygame.key.get_pressed()

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
				change_to_menu()
				going = False

		if keys[pygame.K_p]:
			pauseGame(mode)

		# ATHUS COMBAT #

		if pygame.time.get_ticks() - athus.timeSinceHit > 300:
			athus.isInvincible = False

		for laser1 in p1lasers:
			if agnath.hitbox[1] < laser1.y + laser1.radius and agnath.hitbox[1] + agnath.hitbox[3] > laser1.y:
				if agnath.hitbox[0] + agnath.hitbox[2] > laser1.x + laser1.radius and agnath.hitbox[0] < laser1.x + laser1.radius:
					display_damage = True
					agnath.hit()
					redrawWindow(mode)
					agnath.isInvincible = True
					if len(p1lasers) > 0:
						try:
							p1lasers.pop(p1lasers.index(laser1))
						except(ValueError):
							print(ValueError)
			if laser1.x < sw and laser1.x > 0:
				laser1.x += laser1.vel
			else:
				try:
					p1lasers.pop(p1lasers.index(laser1))
				except(ValueError):
					print(ValueError)

		# AGNATH COMBAT #

		if pygame.time.get_ticks() - agnath.timeSinceHit > 300:
			agnath.isInvincible = False

		for laser2 in p2lasers:
			if athus.hitbox[1] < laser2.y + laser2.radius and athus.hitbox[1] + athus.hitbox[3] > laser2.y:
				if athus.hitbox[0] + athus.hitbox[2] > laser2.x + laser2.radius and athus.hitbox[0] < laser2.x + laser2.radius:
					display_damage = True
					athus.hit()
					redrawWindow(mode)
					athus.isInvincible = True
					if len(p2lasers) > 0:
						try:
							p2lasers.pop(p2lasers.index(laser2))
						except(ValueError):
							print(ValueError)

			if laser2.x < sw and laser2.x > 0:
				laser2.x += laser2.vel
			else:
				if len(p2lasers) > 0:
					try:
						p2lasers.pop(p2lasers.index(laser2))
					except(ValueError):
						print(ValueError)
			
		# ATHUS MOVEMENT #

		if keys[pygame.K_LEFT] and athus.x > athus.vel:
			athus.x -= athus.vel
			athus.left = True
			athus.right = False
			athus.standing = False

		elif keys[pygame.K_RIGHT] and athus.x < sw - athus.width - athus.vel:
			athus.x += athus.vel
			athus.right = True
			athus.left = False
			athus.standing = False

		else:
			athus.standing = True
			athus.walkCount = 0

		if not (athus.isJump):
			athus.y = base
			if keys[pygame.K_UP]:
				athus.isJump = True
				
		else:
			if athus.jumpCount >= -10:
				neg = 1
				if athus.jumpCount < 0:
					neg = -1
				athus.y -= (athus.jumpCount ** 2) * 0.5 * neg
				athus.jumpCount -= 1

			else:
				athus.isJump = False
				athus.jumpCount = 10

		if keys[pygame.K_SPACE] and athus.loop == 0:
			i = 0
			athus.isShooting = True
			if athus.left:
				facing1 = -1
				i = 2
			else:
				i = 62
				facing1 = 1

			if len(p1lasers) < 3:
				# athusLaserSound.play()
				p1lasers.append(projectile1(athus.x + i, athus.y + 30, 2, 200, (255,0,0), facing1))
				athus.loop = 1

		# AGNATH MOVEMENT#

		if keys[pygame.K_a] and agnath.x > agnath.vel:
			agnath.x -= agnath.vel
			agnath.left = True
			agnath.right = False
			agnath.standing = False

		elif keys[pygame.K_d] and agnath.x < sw - agnath.width - agnath.vel:
			agnath.x += agnath.vel
			agnath.right = True
			agnath.left = False
			agnath.standing = False

		else:
			agnath.standing = True
			agnath.walkCount = 0

		if not (agnath.isJump):
			agnath.y = base
			if keys[pygame.K_w]:
				agnath.isJump = True
				
		else:
			if agnath.jumpCount >= -10:
				neg = 1
				if agnath.jumpCount < 0:
					neg = -1
				agnath.y -= (agnath.jumpCount ** 2) * 0.5 * neg
				agnath.jumpCount -= 1

			else:
				agnath.isJump = False
				agnath.jumpCount = 10

		if keys[pygame.K_LSHIFT] and agnath.loop == 0:
			i = 0
			agnath.isShooting = True
			if agnath.left:
				facing2 = -1
				i = 2
			else:
				i = 62
				facing2 = 1

			if len(p2lasers) < 3:
				# athusLaserSound.play()
				p2lasers.append(projectile2(agnath.x + i, agnath.y + 30, 2, 200, (0,255,0), facing2))
				agnath.loop = 1

		redrawWindow(mode)


# this method is responsible for drawing everything that occurs during gameplay

def redrawWindow(mode):
	global lotto

	win.blit(bg[lotto], (0,0))
	athus.draw(win)

	if mode == 0:
		score_str = str(athus.score)
		rightAlignText(win, score_str, 35, 650, 30)

		oleste.draw(win)
		etro.draw(win)
		for laser in enemy_lasers:
			laser.draw(win)

	if mode == 1:
		agnath.draw(win)
		for laser2 in p2lasers:
			laser2.draw(win)

	for laser1 in p1lasers:
		laser1.draw(win)

	pygame.display.update()

def endGame(winner, score, mode):
	global going
	global lotto
	ended = True

	if mode == 0:
		showGameOver(score)

	if mode == 1:
		winnerText(winner)

	while ended:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if mode == 0 and event.type == pygame.KEYDOWN and event.key == pygame.K_t:
				showTopScores(False)
				showing = True

				while showing:
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							pygame.quit()
							quit()
						if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
							ended = False
							showing = False
						if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
							showing = False
				redrawWindow(mode)
				showGameOver(score)

			if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
				
				asking = True

				while asking:
					redrawWindow(mode)
					quitWarning()
					oleste.pause = True
					etro.pause = True
					athus.pause = True
					agnath.pause = True

					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							pygame.quit()
							quit()

						if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
							resetGameState(mode)
							ended = False
							going = False
							asking = False

						if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
							redrawWindow(mode)
							if mode == 0:
								showGameOver(score)
							if mode == 1:
								winnerText(winner)
							asking = False

				# ended = False
				# going = False
				
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				redrawWindow(mode)
				resetGameState(mode)
				ended = False
		
		oleste.pause = False
		etro.pause = False
		athus.pause = False
		agnath.pause = False
		pygame.display.update()
		clock.tick(15)

def pauseGame(mode):
	global going
	global scoring

	scoring = False
	pause = True
	pausedScreen()
	confirm = False

	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
				pause = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
				showTopScores(True)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_q:

				asking = True

				while asking:
					oleste.pause = True
					etro.pause = True
					athus.pause = True
					agnath.pause = True

					redrawWindow(mode)
					quitWarning()

					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							pygame.quit()
							quit()

						if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
							resetGameState(mode)
							pause = False
							going = False
							asking = False

						if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
							redrawWindow(mode)
							pausedScreen()	
							asking = False

			if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
				redrawWindow(mode)
				pausedScreen()
					
		oleste.pause = False
		etro.pause = False
		athus.pause = False
		agnath.pause = False
		scoring = True
		pygame.display.update()
		clock.tick(15)

def resetGameState(mode):
	global lotto
	global base

	lotto = random.randint(0,18)
	if len(p1lasers) > 0:
		p1lasers.clear()
	if len(p2lasers) > 0:
		p2lasers.clear()
	lotto = random.randint(0, 18)
	athus.x = 600
	athus.y = base
	athus.health = 16
	athus.healthboxColor = (0, 250, 0)
	athus.score = 0
	athus.left = True
	athus.left = False

	if mode == 0:
		oleste.x = -80
		oleste.y = base
		oleste.health = 10
		oleste.healthboxColor = (0, 250, 0)

		etro.x = -80
		etro.y = base
		etro.health = 20
		etro.healthboxColor = (0, 250, 0)

		if len(enemy_lasers) > 0:
			enemy_lasers.clear()

	elif mode == 1:
		agnath.x = 36
		agnath.y = base
		agnath.health = 16
		agnath.healthboxColor = (0, 250, 0)
		agnath.right = True
		agnath.left = False
	
	redrawWindow(mode)



