#############################################
#
# - PENDU GRAPHIQUE -
# auteur: Léo ROLLAND
#
#############################################


# Importation des modules
import random
from tkinter import *
from functools import partial
import time


############### DEFINITION DES VARIABLES ###############

mot = '' 			# Le mot qui sera a deviner, il sera défini dans la "SELECTION DU MOT"
motAffiche = ''		# Le mot deviné par le joueur qui sera completé au fur et a mesure
essais = 9 			# Le nombre d'essais max.
isKeyPressed = False # Variable qui exprime si une touche du clavier virtuel a été enfoncée.
win = None
keyboard=[]
# Statistiques :
victoires = 0
defaites = 0

#############################################


win = Tk() # Instanciation de la fenêtre principale "win"
win.geometry("800x400")
win.title('Pendu Edition Graphique - Léo ROLLAND')
frame=Frame(win,width=800, height=400) # On crée une "frame" qui accueillera tous les widgets tkinter.
frame.grid()

	
############### DEFINITION DES FONCTIONS ###############

def selectWord():
	""" Fonction modifiant la variable motAffiche et mot avec un nouveau mot tiré du fichier dictionnaire. """
	global motAffiche, mot
	# On ouvre le fichier dictionnaire pour obtenir le nombre de lignes
	f = open('dico.txt', 'r')
	lines = 0
	for line in f: # Pour chaque ligne du fichier, on incrémente le compteur de lignes
		lines+=1 # Compteur
	f.close() # On ferme le fichier

	# On choisit une ligne au hasard entre 1 et le nombre de lignes
	hasard = random.randint(1, lines-1)

	# On réouvre le fichier en lisant la ligne hasard
	f = open('dico.txt', 'r')
	for l in range(hasard): # Parcours des lignes du fichier jusqu'à valeur hasard atteinte
		mot = f.readline().replace('\n','').upper() # On lit le mot, on supprime le retour à la ligne, on le met en majuscules et on l'assigne a notre variable.

	# On crée les traits (du mot qui évoluera progressivement)
	for lettre in mot:
		motAffiche+="_"
	f.close() # On ferme le fichier

def reset():
	""" Fonction qui réinitialise l'interface """
	global frame, keyboard, title, start, win, mot, motAffiche, essais
	print("réinitialisation...")
	keyboard=[]
	mot = '' 			# Le mot qui sera a deviner, il sera défini dans la "SELECTION DU MOT"
	motAffiche = ''			# Le mot deviné par le joueur qui sera completé au fur et a mesure
	essais = 9 			# Le nombre d'essais max.
	isKeyPressed = False		# Variable qui exprime si une touche du clavier virtuel a été enfoncée.
	frame.destroy()

	frame=Frame(win,width=800, height=400) # On crée une "frame" qui accueillera tous les widgets tkinter.
	frame.grid()

	ratio = int(victoires*100/(victoires+defaites))
	title = Label(frame,text="- Pendu -  \n(Stats: %s victoires, %s défaites, %s%% de victoire)"%(victoires,defaites,ratio), font="Arial 20")
	title.place(x=120,y=60)
	start = Button(frame,text="Démarrer la partie", font="Arial 14",command=partial(initPendu) )
	start.place(x=305,y=150)

def perdu():
	""" Fonction perdu executée à la fin de la partie, elle propose au joueur de recommencer """
	global win, defaites
	Label(frame,text="Vous avez echoué...",font=("Courier", 30)).place(x=320,y=150)
	Label(frame,text="Le mot était "+mot).place(x=320,y=200)
	Button(frame,text="Recommencer",command=reset).place(x=320,y=250)
	defaites+=1

def gagne():
	""" Même chose lorsqu'il gagne """
	global win, victoires
	Label(frame,text="Vous avez gagné !",font=("Courier", 30)).place(x=320,y=150)
	Button(frame,text="Recommencer",command=reset).place(x=320,y=250)
	victoires+=1

def setWord(word):
	""" Fonction qui modifie le mot affiché dans la fenetre graphique """
	global frame
	texte = Label(frame,text=word.replace(""," "),font=("Courier", 30))
	texte.place(x=320,y=80)

def setImg(n):
	""" Fonction qui modifie l'image du pendu """
	fichierimg = PhotoImage(file='%s.png'%(n)) # On charge le fichier "n.png"
	label = Label(frame,image=fichierimg) # Et on l'affiche dans un label
	label.image = fichierimg
	label.place(x=40,y=15)

def disableKey(lettre):
	""" Fonction suppression d'une touche pressée """
	global keyboard
	for touche in keyboard:
		if touche.cget('text') == lettre:
			touche.place_forget()

def keyPressed(lettre):
	""" Fonction executée lors de l'appui d'une touche du clavier virtuel """
	global key, isKeyPressed, mot, motAffiche, essais
	disableKey(lettre)
	key = lettre

	test = key # La lettre à tester (mot) prend la valeur de la touche pressée au clavier virtuel
	trouve = False # A-on trouvé une nouvelle lettre ? (True | False)
	motReconstitue = ''

	for i in range(len(mot)): # Pour chaque lettre i du mot à trouver
		if mot[i] == test: # Si une lettre correspond à la lettre à tester
			trouve = True

	if trouve == True: # Si on a trouvé une nouvelle lettre
		motReconstitue = '' # On recrée le futur mot affiché
		for i in range(len(mot)): # On parcours chaque lettre du mot original
			if test == mot[i]:
				motReconstitue += test # Si la lettre correspond à la trouvée, on l'ajoute
			else:
				motReconstitue += motAffiche[i] # Sinon on ne change rien
		motAffiche = motReconstitue
	else:
		essais-=1 # On retire une vie
		setImg(10-essais) # On affiche l'image correspondante à la vie du joueur

        # On affiche le mot qui sera deviné
	setWord(motAffiche)

	if (essais > 0) and (motAffiche == mot): # Si il a encore des essais et qu'il a trouvé le mot
		gagne()
	if essais < 1: # S'il n'a plus de vies
		perdu()

#############################################

############### CREATION DE LA FENETRE GRAPHIQUE ###############

# Fonction qui quitte le menu du début pour lancer le jeu.
def initPendu():
	global frame
	""" Fonction d'initialisation de la partie """

	# On supprime le menu principal pour générer l'interface du jeu.
	start.place_forget()
	title.place_forget()

	selectWord() # On tire un mot au hasard

	# On place l'image du pendu n°1
	setImg(1)
	# On affiche le mot qui sera deviné
	setWord(motAffiche)

	# Création du clavier
	for i in range(26): 		# Pour chaque valeur allant de 1 à 26
		lettre = chr(i+65) 		# On détermine le caractère associé sur la table ASCII
		keyboard.append( 		# On ajoute à la liste keyboard[]
			Button( 			# Un bouton tkinter
				frame,
				text=lettre, 		# Qui prendra le texte de la lettre
				width=1,  		# Dont la largeur du bouton sera définie
				command=partial(keyPressed,lettre) # Dont la commande assignée sera la fonction keyPressed avec l'argument lettre.
				# à la bibliothèque 'partial' permet de ne pas éxécuter immédiatement la commande lors de l'écriture de celle ci
				# mais seulement d'y faire référence
			)
		)
		placementVertical = 300
		placementHorizontal = 160
		if i<10:
			keyboard[i].place(x=placementHorizontal+20+i*40,y=placementVertical) # Placement de la première rangée
		elif i<20:
			keyboard[i].place(x=placementHorizontal+i*40-380,y=placementVertical+30) # Placement seconde rangée
		else:
			keyboard[i].place(x=placementHorizontal+i*40-700,y=placementVertical+60) # Placement troisième rangée

# On crée le menu principal :
title = Label(frame,text="- Pendu -  \n(Stats: %s victoires, %s défaites, %s%% de victoire)"%(victoires,defaites,0), font="Arial 20")
title.place(x=120,y=60)
start = Button(frame,text="Démarrer la partie", font="Arial 14",command=initPendu) # Ce bouton lance la fonction juste au dessus
start.place(x=305,y=150)

# On lance la fenêtre
win.mainloop()

#############################################
