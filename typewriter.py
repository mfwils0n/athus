import pygame


font_name = pygame.font.match_font('couriernewttf')
def centeredText(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, (255,255,255))
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)

def leftAlignText(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, (255,255,255))
	text_rect = text_surface.get_rect()
	text_rect.topleft = (x, y)
	surf.blit(text_surface, text_rect)

def rightAlignText(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, (255,255,255))
	text_rect = text_surface.get_rect()
	text_rect.topright = (x, y)
	surf.blit(text_surface, text_rect)
