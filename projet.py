# -*- coding: utf-8 -*-

import pygame
import pygame.gfxdraw
import pygame.key
import numpy as np

import physique as phy

DIM = np.array([800, 800]) # [Longueur, Hauteur] de la fenêtre en pixel
NOMBRE_PROIES = 100
NOMBRE_PREDATEURS = 1

pygame.init()
pygame.font.init()
pygame.display.set_caption('Chlamydomonas')
screen = pygame.display.set_mode((DIM[0], DIM[1]))
font = pygame.font.SysFont("comicsansms", 25)
fontimportant = pygame.font.SysFont("comicsansms", 35)

sim = phy.Simulation(DIM)

"""
for i in range(10):
	masse = 1000 # np.random.random_sample()*4000
	rayon = int(np.sqrt(masse/np.pi))
	pos = np.random.rand(2)*(DIM-rayon)+rayon
	vitesse = np.random.rand(2)*300
	sim.addCell(pos, vitesse, masse, True)

#sim.addCell([400.0,400.0], [20.0,80.0], 2500.0, False)
"""

def display(sim):
	for cercle in sim.getCercles():
		pygame.gfxdraw.circle(screen, int(cercle.getPosX()), int(cercle.getPosY()), int(cercle.getRayon()), cercle.getCouleur())

	for cell in sim.getCells():
		pygame.gfxdraw.filled_circle(screen, int(cell.getPosX()), int(cell.getPosY()), cell.getRayon(), cell.getCouleur())

	compteur_step = font.render("Step : " + str(sim.getStep()), True, (0, 128, 0))
	rect_compteur_step = compteur_step.get_rect()
	rect_compteur_step.topleft = (10,6)
	screen.blit(compteur_step, rect_compteur_step)

	compteur_temps = font.render("Temps : " + str(sim.getTemps()) + " s", True, (0, 128, 0))
	rect_compteur_temps = compteur_temps.get_rect()
	rect_compteur_temps.topleft = (10,25)
	screen.blit(compteur_temps, rect_compteur_temps)

	compteur_cells = font.render("Cells : " + str(sim.getNbCells()) + " s", True, (0, 128, 0))
	rect_compteur_cells = compteur_cells.get_rect()
	rect_compteur_cells.topleft = (10,44)
	screen.blit(compteur_cells, rect_compteur_cells)

def displaypause(sim):
	screen.fill([255, 255, 255])
	display(sim)
	pygame.display.flip()
	message = fontimportant.render("SIMULATION EN PAUSE", True, (255, 0, 0))
	rect_message = message.get_rect()
	rect_message.center = (DIM[0]//2,DIM[1]//2)
	screen.blit(message, rect_message)
	pygame.display.flip()

displaypause(sim)

running=True
simulating=False
while(running):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.MOUSEBUTTONUP:
			posint = pygame.mouse.get_pos()
			pos = [float(posint[0]),float(posint[1])]
			masse = 2000 # np.random.random_sample()*4000
			rayon = int(np.sqrt(masse/np.pi))
			vitesse = np.random.rand(2)*300
			sim.addCell(pos, vitesse, masse, False)
			if not(simulating):
				displaypause(sim)

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_SPACE: # PAUSE SIMULATION
				simulating = not(simulating)
				if not(simulating):
					displaypause(sim)

			if event.key == pygame.K_a: # AJOUTER CELLULE
				masse = 1000 # np.random.random_sample()*4000
				rayon = int(np.sqrt(masse/np.pi))
				pos = np.random.rand(2)*(DIM-rayon)+rayon
				vitesse = np.random.rand(2)*300
				sim.addCell(pos, vitesse, masse, True)
				if not(simulating):
					displaypause(sim)

			if event.key == pygame.K_s: # INDUIRE UN STRESS
				if not(simulating):
					displaypause(sim)

			if event.key == pygame.K_r: # REFRESH ERCRAN
				if not(simulating):
					displaypause(sim)
			
			if event.key == pygame.K_c: # RESET
				sim = phy.Simulation(DIM)
				if not(simulating):
					displaypause(sim)
			
			


	
	if simulating:
		screen.fill([255, 255, 255])
		sim.update()
		display(sim)
		pygame.display.flip()
