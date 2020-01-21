# -*- coding: utf-8 -*-

import numpy as np

COULEUR_PROIE_YOLO = [39, 174, 96] # Vert, la proie vie sa vie
COULEUR_PROIE_AVERTIE = [241, 196, 15] # Jaune, la proie cherche à agréger
COULEUR_PREDATEUR = [194, 54, 22] # Rouge, les méchants !!!!



dt = 0.01 # Echantillon du temps

class Simulation():
	def __init__(self, dim):
		self.dim=dim # Les dimensions de l'environnement (même que celles de la fenêtre)
		self.step=0 # Etape en cours de la simulation
		self.temps=0
		self.cells = [] # Liste des cellules simulées
		self.cellsnonagregees=[]
		self.cercles = []

	def addCell(self, pos, vitesse, masse, proie):
		c = Cellule(self, pos, vitesse, masse, proie)
		self.cells.append(c)
		self.cellsnonagregees.append(c)

	def addCercle(self, centre, rayon, lifespan=300, couleur=[0, 0, 255]): # Fonctionnalité debug
		self.cercles.append(Cercle(centre, rayon, lifespan, couleur))

	def rebondMur(self):
		for cell in self.cells:
			i = 0
			for x in cell.pos:
				if x > self.dim[i]-cell.rayon:
					dist = cell.rayon-(self.dim[i]-x)
					cell.addPos(-dist) #
					tmp = np.zeros(np.size(cell.vitesse))
					tmp[i] = -2*cell.vitesse[i]
					cell.addVitesse(tmp)
				elif x < cell.rayon: 
					dist = cell.rayon-x
					cell.addPos(dist)
					tmp = np.zeros(np.size(cell.pos))
					tmp[i] = -2*cell.vitesse[i]
					cell.addVitesse(tmp)
				i += 1

	def update(self): # Méthode pour incrémenter d'une étape la simulation
		for cercle in self.cercles:
			cercle.lifespan-=1
			# cercle.rayon+=1 Idée intéressante
			if(cercle.lifespan==0):
				self.cercles.remove(cercle)

		for cell1 in self.cellsnonagregees:
			if cell1.proie:
				cell1.addMasse(1.0)
			else:
				cell1.removeMasse(1.0)

			if not(cell1.agregee):
				cell1.avancer()
				for cell2 in self.cells:
					if cell1 != cell2:
						self.collision(cell1, cell2)

				if cell1.proie and not(cell1.consciente):
					for cercle in self.cercles:
						if cell1.dansCercle(cercle):
							cell1.priseDeConscience()


		self.rebondMur()

		self.step+=1
		self.temps+=dt

	def collision(self, c1, c2):
		# Situation : c1 vient d'avancer, doit-elle intéragir avec c2 ?
		dpos = c1.pos-c2.pos # Différence de position entre c1 et c2 pour chaque coordonnée
		dist = np.sqrt(np.sum(dpos**2)) # Distance euclidienne entre c1 et c2
		if dist < c1.rayon+c2.rayon: # Si ils se touchent
			if c1.proie == c2.proie: # Si du même type, alors collision élastique
				if c1.proie and (c1.consciente or c2.consciente):
					c1.agregation()
					c2.agregation()
				else:
					offset = dist-(c1.rayon+c2.rayon)
					c1.addPos((-dpos/dist)*offset/2)
					print(c1.proie)
					print(c2.proie)
					print(-dpos)
					print(dist)
					print(c1.pos)
					c2.addPos((dpos/dist)*offset/2)
					masse_totale = c1.masse+c2.masse
					dvitesse1 = -2*c2.masse/masse_totale*np.inner(c1.vitesse-c2.vitesse,c1.pos-c2.pos)/np.sum((c1.pos-c2.pos)**2)*(c1.pos-c2.pos)
					dvitesse2 = -2*c1.masse/masse_totale*np.inner(c2.vitesse-c1.vitesse,c2.pos-c1.pos)/np.sum((c2.pos-c1.pos)**2)*(c2.pos-c1.pos)
					c1.addVitesse(dvitesse1)
					c2.addVitesse(dvitesse2)
			elif not(c1.proie) and dist < c1.rayon+(c2.rayon/2): # Si c1 prédateur et si suffisament proche (approx moitie du corps de c2 dans c1) alors c1 mange c2 :)
				if not(c2.agregee) and c1.masse>c2.masse:
					c1.addMasse(c2.masse)
					self.cells.remove(c2)
					self.addCercle(c1.pos,100)
				else:
					offset = dist-(c1.rayon+c2.rayon)
					c1.addPos((-dpos/dist)*offset/2)
					c2.addPos((dpos/dist)*offset/2)
					masse_totale = c1.masse+c2.masse
					dvitesse1 = -2*c2.masse/masse_totale*np.inner(c1.vitesse-c2.vitesse,c1.pos-c2.pos)/np.sum((c1.pos-c2.pos)**2)*(c1.pos-c2.pos)
					dvitesse2 = -2*c1.masse/masse_totale*np.inner(c2.vitesse-c1.vitesse,c2.pos-c1.pos)/np.sum((c2.pos-c1.pos)**2)*(c2.pos-c1.pos)
					c1.addVitesse(dvitesse1)
					c2.addVitesse(dvitesse2)


	def getCercles(self):
		return self.cercles

	def getCells(self): # Méthode GET pour récupérer la liste des cellules simulées
		return self.cells

	def getStep(self): # Méthode GET pour récupérer l'étape de la simulation
		return self.step

	def getTemps(self): # Méthode GET pour récupérer l'étape de la simulation
		return self.temps

class Cellule():
	def __init__(self, sim, pos, vitesse, masse, proie=True):
		self.sim = sim
		self.pos = np.array(pos) # Format [x,y]
		self.vitesse = np.array(vitesse) # Format [vx,vy]
		self.defaultmasse = masse
		self.masse = masse
		self.proie = proie # True : est une proie, False: est un prédateur
		self.rayon = int(np.sqrt(self.masse/np.pi))
		self.consciente = False # N'est pas consciente de la présence d'un prédateur par défault
		self.agregee = False # Non agrégée par défault
		if(self.proie): # Si proie alors vert sinon rouge
			self.couleur = COULEUR_PROIE_YOLO
		else:
			self.couleur = COULEUR_PREDATEUR

	def avancer(self): 
		self.pos += self.vitesse*dt;

	def addMasse(self,masse):
		self.masse+=masse
		if(self.masse>2*self.defaultmasse):
			self.masse = self.masse-self.defaultmasse
			self.rayon = int(np.sqrt(self.masse/np.pi))
			c=Cellule(self.sim, self.pos+1, -self.vitesse, self.defaultmasse, self.proie)
			self.sim.cells.append(c)
			self.sim.cellsnonagregees.append(c)
		else:
			self.rayon = int(np.sqrt(self.masse/np.pi))

	def removeMasse(self, masse):
		self.masse-=masse
		if self.masse<0:
			self.sim.cells.remove(self)
			self.sim.cellsnonagregees.remove(self)
		else:
			self.rayon = int(np.sqrt(self.masse/np.pi))

	def addPos(self,pos):
		self.pos += pos

	def addVitesse(self, vitesse):
		self.vitesse += vitesse

	def agregation(self):
		if not(self.agregee):
			self.vitesse=np.array([0.0,0.0])
			self.agregee=True
			self.consciente=True
			self.couleur=COULEUR_PROIE_AVERTIE
			self.sim.cellsnonagregees.remove(self)

	def dansCercle(self,c):
		dpos = self.pos-c.centre
		dist = np.sqrt(np.sum(dpos**2))
		if dist < self.rayon+c.rayon:
			return True
		else:
			return False

	def priseDeConscience(self):
		self.consciente=True
		self.couleur=COULEUR_PROIE_AVERTIE

	def getPosX(self):
		return self.pos[0]
	
	def getPosY(self):
		return self.pos[1]

	def getRayon(self):
		return self.rayon

	def getCouleur(self):
		return self.couleur

class Cercle():
	def __init__(self, centre, rayon, lifespan = 3000, couleur=[0, 0, 255]):
		self.centre = np.array(centre)
		self.rayon = np.array(rayon)
		self.lifespan = lifespan
		self.couleur = couleur

	def getPosX(self):
		return self.centre[0]
	
	def getPosY(self):
		return self.centre[1]

	def getRayon(self):
		return self.rayon

	def getCouleur(self):
		return self.couleur