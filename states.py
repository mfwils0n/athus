import pygame
import sys
import random
import array
from typewriter import *
from dataclasses import dataclass


pygame.init()

is_menu = True
sw = 700
sh = 512

# def change_to_gameplay():
# 	global is_menu 
# 	is_menu = False

midwidth = sw / 2
midheight = sh / 2
leftmargin = 20
rightmargin = sw - 20

playing = False		#is the user midgame?						-> gameplay / go screen
pausing = False		#has the user paused the game?				-> pauseScreen / gameplay
reading = False		#is the user reading about this game?		-> aboutScreens / 
learning = False	#is the user looking at the instructions?	-> instructionScreen /
checking = False	#is the user checking the top scores?		-> topScores /
waiting = False

#athus = player(600, 380, 64, 64)

#initializing the components necessary to build the gameplay environment
#-----------------------------------------------------------------------
#game window
win = pygame.display.set_mode((sw, sh))
#window caption
pygame.display.set_caption("import testing")
#list of images for the background (will be chosen at random)
bg = [pygame.image.load('bgp-1.jpg'), pygame.image.load('bgp-2.jpg'), pygame.image.load('bgp-3.jpg'), pygame.image.load('bgp-4.jpg'), pygame.image.load('bgp-5.jpg'), pygame.image.load('bgp-6.jpg'), pygame.image.load('bgp-7.jpg'), pygame.image.load('bgp-8.jpg'), pygame.image.load('bgp-9.jpg'), pygame.image.load('bgp-10.jpg'), pygame.image.load('bgp-11.jpg'), pygame.image.load('bgp-12.jpg'), pygame.image.load('bgp-13.jpg'), pygame.image.load('bgp-14.jpg'), pygame.image.load('bgp-15.jpg'), pygame.image.load('bgp-16.jpg'), pygame.image.load('bgp-17.jpg'), pygame.image.load('bgp-18.jpg'), pygame.image.load('bgp-19.jpg')]
#random number from 0 to 18 that corresponds to a background image
lotto = random.randint(0,18)
#system clock
clock = pygame.time.Clock()

athus_big = pygame.image.load('athus_big.png')
oleste_big = pygame.image.load('oleste_big.png')
etro_big = pygame.image.load('etro_big_def.png')

#this method shows you the very first startup screen
def goScreenText():
	win.fill((0,0,0))

	centeredText(win, "ATHUS", 100, midwidth, sh / 5)
	centeredText(win, "PRESS [ENTER] TO BEGIN", 18, midwidth, sh / 9 * 4)
	centeredText(win, "PRESS [A] FOR ABOUT", 18, midwidth, sh / 9 * 5)
	centeredText(win, "PRESS [I] FOR INSTRUCTIONS", 18, sw / 2, sh / 9 * 6)
	centeredText(win, "PRESS [T] FOR TOP SCORES", 18, sw / 2, sh / 9 * 7)

	pygame.display.flip()


def showGoScreen():
	goScreenText()
	global waiting
	
	playing = False
	pausing = False
	reading = False
	learning = False
	checking = False

	waiting = True

	while waiting:
		clock.tick(30)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
				mode = getGameMode()
				waiting = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
				i_mode = getGameMode()
				instructions(i_mode)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
				showGoScreen()
			if event.type == pygame.KEYDOWN and (event.key == pygame.K_a or event.key == pygame.K_1):
				aboutPages(0)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
				aboutPages(1)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
				aboutPages(2)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
				showTopScores(False)

	return mode

def getGameMode():
	win.fill((0,0,0))
	centeredText(win, "CHOOSE MODE:", 80, sw / 2, sh / 4)
	centeredText(win, "PRESS [S] FOR SINGLE PLAYER", 30, sw / 2, sh / 2)
	centeredText(win, "PRESS [M] FOR MULTIPLAYER", 30, sw / 2, sh / 1.5)

	pygame.display.flip()

	waiting = True
	while waiting:
		clock.tick(30)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
				return 0
			if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
				return 1



#the text that will be drawn while the game is paused
def pausedScreen():
	centeredText(win, "PAUSED", 125, sw / 2, sh / 2 - 125)
	centeredText(win, "PRESS [P] TO UNPAUSE", 40, sw / 2, sh / 7 * 4)
	centeredText(win, "PRESS [T] TO SEE TOP SCORES", 40, sw / 2, sh / 7 * 4.75)
	centeredText(win, "PRESS [Q] TO QUIT", 40, sw / 2, sh / 7 * 5.5)

	pygame.display.flip()

#the text that will be drawn on each 'About' page
def aboutPages(page):
	win.fill((0,0,0))

	centeredText(win, "About this Game", 70, sw / 2, sh / 6)

	if page == 0:
		win.blit(athus_big, (40, 150))
		leftAlignText(win, "Athus, the creature after which this game", 20, 180, sh / 16 * 6)
		leftAlignText(win, "is named, is a light-footed Compsagnathus", 20, 180, sh / 16 * 7)
		leftAlignText(win, "with a quick-fire laser and a mighty need", 20, 180, sh / 16 * 8)
		leftAlignText(win, "to do some damage. And though he is only 6lbs, do not", 20, 37, sh / 16 * 9)
		leftAlignText(win, "underestimate his grit. He survived the Cretaceous - ", 20, 37, sh / 16 * 10)
		leftAlignText(win, "Paleogene extinction event and knows no fear.", 20, 37, sh / 16 * 11)

		centeredText(win, "PRESS [2] >", 15, sw / 5 * 4, sh /16 * 14)

	elif page == 1:
		win.blit(oleste_big, (520, 280))
		leftAlignText(win, "Oleste is a voracious theropod from the late Jurassic", 20, 37, sh / 16 * 5)
		leftAlignText(win, "period. He is something of an enigma; to date, Ornit-", 20, 37, sh / 16 * 6)
		leftAlignText(win, "holestes is known only from a single partial skeleton", 20, 37, sh / 16 * 7)
		leftAlignText(win, "with a badly crushed skull that was unearthed in Wyo-", 20, 37, sh / 16 * 8)
		leftAlignText(win, "ming, 1900. That being said, it doesn't", 20, 37, sh / 16 * 9)
		leftAlignText(win, "take a paleontologist to see that those", 20, 37, sh / 16 * 10)
		leftAlignText(win, "teeth are for bitin'. Keep an eye on him.", 20, 37, sh / 16 * 11)
		
		centeredText(win, "< PRESS [1]", 15, sw / 5, sh /16 * 14)
		centeredText(win, "PRESS [3] >", 15, sw / 5 * 4, sh /16 * 14)

	elif page == 2:
		win.blit(etro_big, (40, 200))
		leftAlignText(win, "Etro never ceases to amaze. As a dimetrodon, the very", 20, 37, sh / 15 * 5)
		leftAlignText(win, "first synapsid creature ever discovered, he harbors a", 20, 37, sh / 15 * 6)
		leftAlignText(win, "vast amount of energy. His ability to harness the po-", 20, 37, sh / 15 * 7)
		leftAlignText(win, "wer of the sun through his sail", 20, 310, sh / 15 * 8)
		leftAlignText(win, "makes him quite the formidable", 20, 310, sh / 15 * 9)
		leftAlignText(win, "adversary. Don't turn your back", 20, 310, sh / 15 * 10)
		leftAlignText(win, "towards this Cisuralian relic.", 20, 310, sh / 15 * 11)

		centeredText(win, "< PRESS [2]", 15, sw / 5, sh /16 * 14)

	centeredText(win, "<< PRESS [X] TO EXIT", 15, sw / 5, sh /17)
	centeredText(win, "PRESS [ENTER] TO PLAY >>", 15, sw / 5 * 4, sh /17)

	pygame.display.flip()

#the text that will be drawn on the 'Instructions' page
def instructions(mode):
	win.fill((0,0,0))
	if mode == 0:
		centeredText(win, "<< PRESS [X] TO EXIT", 15, sw / 5, sh /17)
		centeredText(win, "PRESS [ENTER] TO PLAY >>", 15, sw / 5 * 4, sh /17)
		centeredText(win, "SINGLEPLAYER", 60, sw / 2, sh / 5 - 20)
		# centeredText(win, "KEYS", 60, sw / 2, sh / 5 + 40)
		centeredText(win, "[^]", 30, 225, sh / 5 * 2)	
		centeredText(win, "jump", 30, 475, sh / 5 * 2)	
		centeredText(win, "[<]  [>]", 30, 225, sh / 5 * 2 + 30)
		centeredText(win, "move", 30, 475, sh / 5 * 2 + 30)
		centeredText(win, "[SPACE]", 30, 225, sh / 5 * 2 + 60)
		centeredText(win, "shoot", 30, 475, sh / 5 * 2 + 60)
		centeredText(win, "[P]", 30, 225, sh / 5 * 2 + 90)
		centeredText(win, "pause", 30, 475, sh / 5 * 2 + 90)
		centeredText(win, "[M]", 30, 225, sh / 5 * 2 + 120)
		centeredText(win, "mute music", 30, 475, sh / 5 * 2 + 120)
		centeredText(win, "[N]", 30, 225, sh / 5 * 2 + 150)
		centeredText(win, "mute sound effects", 30, 475, sh / 5 * 2 + 150)
	elif mode == 1:
		centeredText(win, "<< PRESS [X] TO EXIT", 15, sw / 5, sh /17)
		centeredText(win, "PRESS [ENTER] TO PLAY >>", 15, sw / 5 * 4, sh /17)
		centeredText(win, "MULTIPLAYER", 60, sw / 2, sh / 8)
		# centeredText(win, "KEYS", 60, sw / 2, sh / 8 + 20)
		centeredText(win, " PLAYER 1", 35, sw / 4 * 3, sh / 5 * 1.5)
		centeredText(win, " PLAYER 2", 35, sw / 4, sh / 5 * 1.5)
		centeredText(win, "[W]", 20, sw / 4, sh / 5 * 2)
		centeredText(win, "[^]", 20, sw / 4 * 3, sh / 5 * 2)
		centeredText(win, "jump", 20, sw / 2, sh / 5 * 2)	
		centeredText(win, "[<]  [>]", 20, sw / 4 * 3, sh / 5 * 2.25)
		centeredText(win, "[A]  [D]", 20, sw / 4, sh / 5 * 2.25)
		centeredText(win, "move", 20, sw / 2, sh / 5 * 2.25)
		centeredText(win, "[SPACE]", 20, sw / 4 * 3, sh / 5 * 2.5)
		centeredText(win, "[L SHIFT]", 20, sw / 4, sh / 5 * 2.5)
		centeredText(win, "shoot", 20, sw / 2, sh / 5 * 2.5)
		centeredText(win, "[P]", 20, 225, sh / 5 * 3)
		centeredText(win, "pause", 20, 475, sh / 5 * 3)
		centeredText(win, "[M]", 20, 225, sh / 5 * 3.25)
		centeredText(win, "mute music", 20, 475, sh / 5 * 3.25)
		centeredText(win, "[N]", 20, 225, sh / 5 * 3.5)
		centeredText(win, "mute sound effects", 20, 475, sh / 5 * 3.5)
	#centeredText(win, "Press [ENTER] to begin", 30, sw / 2, sh / 5 * 2 + 200)
	pygame.display.flip()


#returns the current top scores saved in the .txt file as a list
def returnCurrentTop():
	with open("topscores.txt") as file:
		topscores = [topscore.rstrip('\n') for topscore in file]
	topscores.sort(reverse = True)

	return topscores

#takes in a list and a new number and returns the top three numbers as a list
def returnTopThree(scorelist, newnumber):

	max_val = max(scorelist)
	min_val = min(scorelist)
	med_val = -1

	for item in scorelist:
		if (item != max_val and item != min_val):
			med_val = item

	print("max: " + str(max_val))
	print("med: " + str(med_val))
	print("min: " + str(min_val))
	print("new: " + str(newnumber))

	scorelist.sort(reverse = True)

	if newnumber > min(scorelist):
		print("popping from list because " + str(newnumber) + " > " + str(min(scorelist)))
		scorelist.pop(2)
		scorelist.append(newnumber)
		scorelist.sort(reverse = True)

	result = []

	for score in scorelist:
		result.append(score)

	return result

#takes in a number and adds it to the .txt file if it is one of the top 3 scores
def insertScore(number):
	linecount = len(open('topscores.txt').readlines())
	with open("topscores.txt") as file:
		topscores = [topscore.rstrip('\n') for topscore in file]

	inserted = False

	while not inserted:
	
		linecount = linecount = len(open('topscores.txt').readlines())

		with open("topscores.txt") as file:
			topscores = [topscore.rstrip('\n') for topscore in file]

		if linecount == 3:
			scorelist = []

			for singlescore in topscores:
				singlescore_int = int(singlescore)
				array = singlescore_int
				scorelist.append(singlescore_int)

			newSortedScorelist = []
			newSortedScorelist = returnTopThree(scorelist, number)

			file = open("topscores.txt", "r+")
			file.truncate(0)
			for item in newSortedScorelist:
				file.write(str(item) + "\n")
			file.close()
			inserted = True

		elif linecount == 2:
			
			scorelist = []

			for singlescore in topscores:
				singlescore_int = int(singlescore)
				array = singlescore_int
				scorelist.append(singlescore_int)

			scorelist.append(number)

			file = open("topscores.txt", "r+")
			file.truncate(0)
			for item in scorelist:
				file.write(str(item) + "\n")
			file.close()
			inserted = True

		elif linecount == 1:
			
			scorelist = []

			scorelist.append(number)

			for singlescore in topscores:
				singlescore_int = int(singlescore)
				array = singlescore_int
				scorelist.append(singlescore_int)

			file = open("topscores.txt", "r+")
			file.truncate(0)
			for item in scorelist:
				file.write(str(item) + "\n")
			file.close()
			inserted = True

		else:
			
			file = open("topscores.txt", "r+")
			file.write(str(number) + "\n")
			file.close()
			inserted = True


#the text that will be drawn to display the scores
def showTopScores(toggle):
	win.fill((0,0,0))
	centeredText(win, "<< PRESS [X] TO EXIT", 15, sw / 5, sh /17)

	if toggle:
		centeredText(win, "PRESS [P] TO RESUME >>", 15, sw / 5 * 4, sh /17)
	else:
		centeredText(win, "PRESS [ENTER] TO PLAY >>", 15, sw / 5 * 4, sh /17)

	centeredText(win, "SINGLEPLAYER", 50, sw / 2, sh / 6)
	centeredText(win, "LEADERBOARD", 50, sw / 2, sh / 6 * 1.7)
	
	templist = []
	templist = returnCurrentTop()
	max_val = templist[0]
	med_val = templist[1]
	min_val = templist[2]

	centeredText(win, "1. ", 40, 275, sh / 7 * 3)
	centeredText(win, str(max_val), 40, 450, sh / 7 * 3)
	centeredText(win, "2. ", 40, 275, sh / 7 * 4)
	centeredText(win, str(med_val), 40, 450, sh / 7 * 4)
	centeredText(win, "3. ", 40, 275, sh / 7 * 5)
	centeredText(win, str(min_val), 40, 450, sh / 7 * 5)

	pygame.display.flip()

#the logic to get the top scores and determine if the player earned a new top score
#the text that will be drawn when the player dies
def showGameOver(score):

	templist = []
	templist = returnCurrentTop()
	max_val = int(templist[0])
	med_val = int(templist[1])
	min_val = int(templist[2])

	centeredText(win, "GAME OVER", 125, sw / 2, sh / 2 - 125)
	if score > min_val:
		centeredText(win, "NEW HIGH SCORE: " + str(score), 50, sw / 2, sh / 2)
		insertScore(score)

	centeredText(win, "PRESS [T] TO SEE TOP SCORES", 30, sw / 2, sh / 3 * 2 - 20)
	centeredText(win, "PRESS [ENTER] TO PLAY AGAIN", 30, sw / 2, sh / 3 * 2 + 20)
	centeredText(win, "PRESS [Q] TO QUIT", 30, sw / 2, sh / 3 * 2 + 60)

	pygame.display.flip()

def winnerText(winner):
	centeredText(win, winner + "WINS", 80, sw / 2, sh / 3)
	centeredText(win, "PRESS [ENTER] TO PLAY AGAIN", 30, sw / 2, sh / 3 * 2 - 40)
	centeredText(win, "PRESS [Q] TO QUIT", 30, sw / 2, sh / 3 * 2 + 20)

	pygame.display.flip()


def quitWarning():
	ssw = 525
	ssh = 192
	s = pygame.Surface((ssw, ssh))
	s.fill((0,0,0))

	centeredText(s, "REALLY QUIT?", 65, 260, 30)
	centeredText(s, "[Y]      [N]", 40, 260, 130)
	win.blit(s, (sw/8, 159))

	pygame.display.flip()


	