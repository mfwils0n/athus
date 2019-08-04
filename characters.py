import pygame
import sys
import random
import array
#from dataclasses import dataclass


pygame.init()

sw = 700
sh = 512

class player1(object):
	walkRight = [pygame.image.load('player1right_1.png'), pygame.image.load('player1right_2.png'), pygame.image.load('player1right_3.png'), pygame.image.load('player1right_4.png'), pygame.image.load('player1right_5.png'), pygame.image.load('player1right_6.png'), pygame.image.load('player1right_7.png'), pygame.image.load('player1right_8.png')]
	walkLeft = [pygame.image.load('player1left_1.png'), pygame.image.load('player1left_2.png'), pygame.image.load('player1left_3.png'), pygame.image.load('player1left_4.png'), pygame.image.load('player1left_5.png'), pygame.image.load('player1left_6.png'), pygame.image.load('player1left_7.png'), pygame.image.load('player1left_8.png')]
	charRight = pygame.image.load('player1stand_r.png')
	charLeft = pygame.image.load('player1stand_l.png')
	lShoot = pygame.image.load('player1shoot_l.png')
	rShoot = pygame.image.load('player1shoot_r.png')

	def __init__(self, x, y, width, height, mode):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.mode = mode
		self.vel = 5
		self.isJump = False
		self.jumpCount = 10
		self.left = True
		self.right = False
		self.walkCount = 0
		self.timeSinceHit = 0
		self.standing = True
		self.isShooting = False
		self.healthboxColor = (0, 250, 0)
		self.isInvincible = False
		self.visible = True
		self.hitbox = (self.x + 16, self.y + 10, 28, 50)
		self.healthbox = (sw/2 - 128, 20, 256, 8)
		self.health = 16
		self.loop = 0
		self.score = 0
		self.pause = False

	def draw(self,win):
		if not self.pause:
			if self.walkCount + 1 >= 24:	# 24 fps because there are 8 frames
				self.walkCount = 0

			if not (self.standing):			# if athus is not standing, then athus is
				if self.left:				# moving left, or
					win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
					self.walkCount += 1
				elif self.right:			# moving right, or
					win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
					self.walkCount += 1
			elif (self.isShooting):			# shooting
				if self.left:
					win.blit(self.lShoot, (self.x, self.y))
				else:
					win.blit(self.rShoot, (self.x, self.y))
				self.isShooting = False
			else:							# else, athus is standing
				if self.right:
					win.blit(self.charRight, (self.x,self.y))
				elif self.left:
					win.blit(self.charLeft, (self.x,self.y))

		elif self.pause:
			if self.right:			# pausing to the right
				win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
			else:						# pausing to the left
				win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))

		self.hitbox = (self.x + 16, self.y + 10, 28, 50)

		if self.mode == 0:
			pygame.draw.rect(win, (255,255,255), (sw/2 - 131, 18, 261, 12), 10)
			pygame.draw.rect(win, (255,0,0), self.healthbox, 8)
			pygame.draw.rect(win, self.healthboxColor, (222, 20, (self.health * 16), 8), 8)
			pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
		else:
			pygame.draw.rect(win, (255,255,255), (394, 18, 261, 12), 10)
			pygame.draw.rect(win, (255,0,0), (397, 20, 256, 8), 8)
			pygame.draw.rect(win, self.healthboxColor, (397, 20, (self.health * 16), 8), 8)


	def hit(self):
		global gameover
		self.timeSinceHit = pygame.time.get_ticks()
		if self.health > 0:
			if self.health > 9:
				self.healthboxColor = (0, 250, 0)
			elif self.health <= 9 and self.health > 5:
				self.healthboxColor = (255, 204, 0)
			elif self.health <= 5 and self.health > 0:
				self.healthboxColor = (247, 137, 46)

			if not self.isInvincible:
				self.health = self.health -1
				# athusHitSound.play()
				
		
		elif self.health == 0:
			print('p1 died')
			self.healthboxColor = (255, 0, 0)
			# athusDeadSound.play()
			self.isInvincible = True
			gameover = True

class player2(object):
	walkRight = [pygame.image.load('player2right_1.png'), pygame.image.load('player2right_2.png'), pygame.image.load('player2right_3.png'), pygame.image.load('player2right_4.png'), pygame.image.load('player2right_5.png'), pygame.image.load('player2right_6.png'), pygame.image.load('player2right_7.png'), pygame.image.load('player2right_8.png')]
	walkLeft = [pygame.image.load('player2left_1.png'), pygame.image.load('player2left_2.png'), pygame.image.load('player2left_3.png'), pygame.image.load('player2left_4.png'), pygame.image.load('player2left_5.png'), pygame.image.load('player2left_6.png'), pygame.image.load('player2left_7.png'), pygame.image.load('player2left_8.png')]
	charRight = pygame.image.load('player2stand_r.png')
	charLeft = pygame.image.load('player2stand_l.png')
	lShoot = pygame.image.load('player2shoot_l.png')
	rShoot = pygame.image.load('player2shoot_r.png')


	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.vel = 5
		self.isJump = False
		self.jumpCount = 10
		self.left = False
		self.right = True
		self.walkCount = 0
		self.timeSinceHit = 0
		self.standing = True
		self.isShooting = False
		self.healthboxColor = (0, 250, 0)
		self.isInvincible = False
		self.visible = True
		self.hitbox = (self.x + 16, self.y + 10, 28, 50)
		self.healthbox = (47, 20, 256, 8)
		self.health = 16
		self.loop = 0
		self.pause = False


	def draw(self,win):
		if not self.pause:
			if self.walkCount + 1 >= 24:	# 24 fps because there are 8 frames
				self.walkCount = 0

			if not (self.standing):			# if athus is not standing, then athus is
				if self.left:				# moving left, or
					win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
					self.walkCount += 1
				elif self.right:			# moving right, or
					win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
					self.walkCount += 1
			elif (self.isShooting):			# shooting
				if self.left:
					win.blit(self.lShoot, (self.x, self.y))
				else:
					win.blit(self.rShoot, (self.x, self.y))
				self.isShooting = False
			else:							# else, athus is standing
				if self.right:
					win.blit(self.charRight, (self.x,self.y))
				elif self.left:
					win.blit(self.charLeft, (self.x,self.y))
		
		elif self.pause:
				if self.right:				# pausing to the right
					win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
				else:						# pausing to the left
					win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))

		self.hitbox = (self.x + 16, self.y + 10, 28, 50)
		pygame.draw.rect(win, (255,255,255), (44, 18, 261, 12), 10)
		pygame.draw.rect(win, (255,0,0), self.healthbox, 8)
		pygame.draw.rect(win, self.healthboxColor, (47, 20, (self.health * 16), 8), 8)
		pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


	def hit(self):
		global gameover
		self.timeSinceHit = pygame.time.get_ticks()
		if self.health > 0:
			if self.health > 9:
				self.healthboxColor = (0, 250, 0)
			elif self.health <= 9 and self.health > 5:
				self.healthboxColor = (255, 204, 0)
			elif self.health <= 5 and self.health > 0:
				self.healthboxColor = (247, 137, 46)

			if not self.isInvincible:
				self.health = self.health -1
				# athusHitSound.play()
				
		
		elif self.health == 0:
			print('p2 died')
			self.healthboxColor = (255, 0, 0)
			# athusDeadSound.play()
			self.isInvincible = True
			gameover = True

# PLAYER 1' LASERS #

class projectile1(object):
	def __init__(self, x, y, radius, length, color, facing):
		self.x = x
		self.y = y
		self.radius = radius
		self.length = length
		self.color = color
		self.facing = facing
		self.i = 1
		self.vel = 8 * facing

	def draw(self, win):
		pygame.draw.circle(win, (255, 255, 0), (round(self.x), round(self.y)), self.radius)

# PLAYER 2'S LASERS #

class projectile2(object):
	def __init__(self, x, y, radius, length, color, facing):
		self.x = x
		self.y = y
		self.radius = radius
		self.length = length
		self.color = color
		self.facing = facing
		self.i = 1
		self.vel = 8 * facing

	def draw(self, win):
		
		pygame.draw.circle(win, (0, 255, 0), (round(self.x), round(self.y)), self.radius)

# ETRO'S LASERS #

class projectile3(object):
	def __init__(self, x, y, radius, length, color, facing):
		self.x = x 
		self.y = y
		self.radius = radius
		self.length = length
		self.color = color
		self.facing = facing
		self.vel = 6 * facing
		self.i = 1

	def draw(self, win):
		
		pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

# OLESTE #

class enemy1(object):
	walkRight = [pygame.image.load('olester-1.png'), pygame.image.load('olester-2.png'), pygame.image.load('olester-3.png'), pygame.image.load('olester-4.png'), pygame.image.load('olester-5.png'), pygame.image.load('olester-6.png'), pygame.image.load('olester-7.png'), pygame.image.load('olester-8.png'), pygame.image.load('olester-9.png'), pygame.image.load('olester-10.png')]
	walkLeft = [pygame.image.load('olestel-1.png'), pygame.image.load('olestel-2.png'), pygame.image.load('olestel-3.png'), pygame.image.load('olestel-4.png'), pygame.image.load('olestel-5.png'), pygame.image.load('olestel-6.png'), pygame.image.load('olestel-7.png'), pygame.image.load('olestel-8.png'), pygame.image.load('olestel-9.png'), pygame.image.load('olestel-10.png')]
	ocharRight = pygame.image.load('olest_stand-r.png')
	# ocharLeft = pygame.image.load('olest_stand-l.png')
	
	def __init__(self, x, y, width, height, end):
		self.x = x
		self.y = y
		self.onScreen = False
		self.width = width
		self.height = height
		self.end = end
		self.path = [self.x, end]
		self.walkCount = 0
		self.vel = 3
		self.hitbox = (self.x + 12, self.y + 10, 34, 50)
		self.health = 10
		self.visible = True
		self.pause = False

	def draw(self, win):
		self.move()
		if self.visible:
			if not self.pause:
				if self.walkCount +1 >= 30:	# 30 fps because there are 10 frames
					self.walkCount = 0

				if self.vel > 0:			# walking to the right
					win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
					self.walkCount += 1
				else:						# walking to the left
					win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
					self.walkCount += 1
			elif self.pause:
				if self.vel > 0:			# pausing to the right
					win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
				else:						# pausing to the left
					win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))

			self.hitbox = (self.x + 12, self.y + 10, 34, 50)
			pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 5))
			pygame.draw.rect(win, (0,250,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((50//10) * (10 - self.health)), 5))
			pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
			# pygame.draw.rect(win, (0,0,0), (109, 390, 34, 50), 2)

	def move(self):
		if not self.pause:
			if not self.onScreen and not self.x < 0:
				self.onScreen = True
				self.path = [0, self.end]

			if self.vel > 0:
				if self.x < self.path[1] + self.vel:
					self.x += self.vel
				else:
					self.vel = self.vel * -1
					self.x += self.vel
					self.walkCount = 0
			else:
				if self.x > self.path[0] - self.vel:
					self.x += self.vel
				else:
					self.vel = self.vel * -1
					self.x += self.vel
					self.walkCount = 0

	def hit(self):
		
		if self.health > 1:
			self.health -= 1
		else:
			self.reset()

	def reset(self):
		print("resetting oleste....")
		self.x = -80
		self.y = 380
		self.health = 10
		self.onScreen = False
		self.walkCount = 0
		self.facing = 1
		self.left = False
		self.right = True
		self.visible = True
		self.onScreen = False
		self.healthboxColor = (0, 250, 0)


# ETRO #

class enemy2(object):
	walkRight = [pygame.image.load('etror-1.png'), pygame.image.load('etror-2.png'), pygame.image.load('etror-3.png'), pygame.image.load('etror-4.png'), pygame.image.load('etror-5.png'), pygame.image.load('etror-6.png'), pygame.image.load('etror-7.png'), pygame.image.load('etror-8.png'), pygame.image.load('etror-9.png'), pygame.image.load('etror-10.png'), pygame.image.load('etror-11.png'), pygame.image.load('etror-12.png'), pygame.image.load('etror-13.png'), pygame.image.load('etror-14.png'), pygame.image.load('etror-15.png'), pygame.image.load('etror-16.png'), pygame.image.load('etror-17.png'), pygame.image.load('etror-18.png'), pygame.image.load('etror-19.png')]
	walkLeft = [pygame.image.load('etrol-1.png'), pygame.image.load('etrol-2.png'), pygame.image.load('etrol-3.png'), pygame.image.load('etrol-4.png'), pygame.image.load('etrol-5.png'), pygame.image.load('etrol-6.png'), pygame.image.load('etrol-7.png'), pygame.image.load('etrol-8.png'), pygame.image.load('etrol-9.png'), pygame.image.load('etrol-10.png'), pygame.image.load('etrol-11.png'), pygame.image.load('etrol-12.png'), pygame.image.load('etrol-13.png'), pygame.image.load('etrol-14.png'), pygame.image.load('etrol-15.png'), pygame.image.load('etrol-16.png'), pygame.image.load('etrol-17.png'), pygame.image.load('etrol-18.png'), pygame.image.load('etrol-19.png')]
	
	def __init__(self, x, y, width, height, end):
		self.x = x
		self.y = y
		self.onScreen = False
		self.left = False
		self.right = True
		self.facing = 1
		self.width = width
		self.height = height
		self.end = end
		self.path = [self.x, end]
		self.walkCount = 0
		self.vel = 1
		self.hitbox = (self.x + 16, self.y + 18, 36, 44)
		self.health = 20
		self.visible = True
		self.pause = False

	def draw(self, win):
		self.move()
		if self.visible:
			if not self.pause:
				if self.walkCount +1 >= 57:
					self.walkCount = 0

				if self.vel > 0:		# walking to the right
					win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
					self.walkCount += 1
					self.right = True
					self.left = False
					self.facing = 1
				else:					# walking to the left
					win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
					self.walkCount += 1
					self.left = True
					self.right = False
					self.facing = -1
			
			elif self.pause:
				if self.vel > 0:		# walking to the right
					win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
					self.right = True
					self.left = False
					self.facing = 1
				else:					# walking to the left
					win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
					self.left = True
					self.right = False
					self.facing = -1

			self.hitbox = (self.x + 16, self.y + 18, 36, 44)
			pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 5))
			pygame.draw.rect(win, (0,250,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((50/20) * (20 - self.health)), 5))
		# pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

	def move(self):
		if not self.pause:
			if not self.onScreen and not self.x < 0:	# once the dino is fully on the screen, this 
				self.onScreen = True					# prevents it from going off again
				self.path = [0, self.end]

			if (self.walkCount//3) >= 9 and (self.walkCount//3) <= 13:	# when etro gets to the 'fire' frames of
				if (self.walkCount//3) == 12:							# his animation sequence, he stays still
					pass
			else:
				if self.vel > 0:							# when velocity is positive, etro is moving right
					if self.x < self.path[1] + self.vel:
						self.x += self.vel
					else:
						self.vel = self.vel * -1
						self.x += self.vel
						self.walkCount = 0
				else:										# when velocity is negative, etro is moving left
					if self.x > self.path[0] - self.vel:
						self.x += self.vel
					else:
						self.vel = self.vel * -1
						self.x += self.vel
						self.walkCount = 0

	def hit(self):
		if self.health > 1:
			self.health -= 1
		else:
			self.reset()

	def reset(self):
		print("resetting etro....")
		self.x = -80
		self.y = 380
		self.health = 20
		self.onScreen = False
		self.walkCount = 0
		self.facing = 1
		self.left = False
		self.right = True
		self.visible = True
		self.onScreen = False
		self.healthboxColor = (0, 250, 0)

	