#####################
#   Bibliotheques   #
#####################

import tkinter as tk
import math
import random

#################
#   Classes   #
#################


class Cochon:
    """
    Classe définissant un cochon
    """

    def __init__(self, dx, dy):
        """
        contructeur :
            - Initialise un attribut nommé rond représentant le cochon en lui même
            - Initialise les attributs nommés x1,y1,x2,y2 correspondant aux coordonnées du cochon
            - Initialise un attribut nommé sexe correspondand au sexe du cochon
            - Initialise un attribut nommé age correspondant à l'age du cochon
        """
        # Détermination du sexe
        self.sexe = 'male' if random.random() < 0.5 else 'femelle'

        # Détermination de l'age
        self.age = random.randint(0, 22)

        if 9 <= self.age <= 22:
            self.rond = can.create_oval(3 + dx, 3 + dy, 3 + diametre + dx, 3 + diametre + dy, width=1, fill='green')
        else:
            self.rond = can.create_oval(3 + dx, 3 + dy, 3 + diametre + dx, 3 + diametre + dy, width=1, fill='grey')

        self.x1, self.y1, self.x2, self.y2 = can.bbox(self.rond)

    def __direction(self):
        """
        Méthode renvoyant deux attributs DX, DY correspondant au déplacement aléatoire du cochon
        """
        angle = random.uniform(0, 2 * math.pi)
        self.DX = 10 * math.cos(angle)
        self.DY = 10 * math.sin(angle)

    def __distance(self, cochon2):
        """
        Méthode qui pour l'instance et un autre cochon donné calcule la distance
        les séparant nommé longueur.
        """
        # Calcul du centre du cochon déplacé de DX, DY
        centredx1 = self.x1 + self.DX + rayon
        centredy1 = self.y1 + self.DY + rayon

        # Calcul le centre du deuxième cochon
        centrex2 = cochon2.x1 + rayon
        centrey2 = cochon2.y1 + rayon

        # Calcul de la distance entre les deux cochons
        self.longueur = math.sqrt((centredx1 - centrex2) ** 2 + (centredy1 - centrey2) ** 2) - (rayon * 2)

    def __control_parois(self):
        # rebond à droite et à gauche
        if self.x1 + diametre + self.DX > Taille_canva or self.x1 + self.DX < 0:
            self.DX = -self.DX

        # rebond en bas et en haut
        if self.y1 + diametre + self.DY > Taille_canva or self.y1 + self.DY < 0:
            self.DY = -self.DY

    def __baillement_spontane(self):
        """
        Méthode permettant de déclancher un baillement spontanné pour le cochon.
        Modification du decompte correspondant au temps de récupération entre deux baillement.
        """
        if random.random() < 0.001 and self.decompte == 0:
            can.itemconfig(self.rond, fill='red')
            self.decompte = 3

    def __baillement_transmission(self):
        """
        Méthode permettant de faire bailler le cochon selon la proprabilité "proba"  correspondante
        """
        if random.random() < self.proba and self.decompte == 0:
            can.itemconfig(self.rond, fill='red')
            self.decompte = 3

    def __baillement_protection(self):
        """
        Méthode permettant de protéger un cochon d'un rebaillement pendant la durée du décompte.
        """
        if 9 <= self.age <= 22:
            if self.decompte > 0:
                can.itemconfig(self.rond, fill='orange')  # Cochon protégé
                self.decompte -= 1
            else:
                can.itemconfig(self.rond, fill='green')  # Cochon déprotégé

    def __probabilite(self, cochon2):
        # Calcul de la probalilité de bailler

        if can.itemcget(cochon2.rond, 'fill') == 'red' and cochon2.sexe == "male":
            if cochon2.sexe == "male":
                if self.longueur < 10:
                    self.proba += 0.65 * 0.4
                elif self.longueur < 100:
                    self.proba += 0.2 * 0.4
                else:
                    self.proba += 0.25 * 0.4
            else:
                if self.longueur < 10:
                    self.proba += 0.65 * 0.28
                elif self.longueur < 100:
                    self.proba += 0.2 * 0.28
                else:
                    self.proba += 0.25 * 0.28

    def vieillissement(self):  # Permet le vieillissement d'un cochon une fois par tour
        if self.age < 22:
            self.age += 1

    def mouvement(self):

        # Permet d'interromptre la boucle
        if stop == 1:
            pass
        else:
            # initialisation du decompte à 0
            if not hasattr(self, 'decompte'):
                self.decompte = 0

            # Protection post baillement
            self.__baillement_protection()

            # Par défaut garde les valeurs DX,DY précédentes sinon initialisation de l'attribut DX et DY
            if not hasattr(self, 'DX'):
                self.__direction()

            # levage du blocage du mouvement
            if self.DX == 0 or self.DY == 0:
                self.__direction()

            # initilisation des variables
            self.proba = 0

            # Controle des parois
            self.__control_parois()

            for cochon in ensemble_cochon:  # Parcours l'ensemble des cochons

                # Regarde si c'est le même cochon
                if cochon.x1 != self.x1 and cochon.y1 != self.y1:
                    self.__distance(cochon)  # Calcul de la distance avec le cochon i
                    # Contrôle de non superposition des cochons
                    if self.longueur <= 0:
                        self.DX, self.DY, proba = 0, 0, 0  # Réinitialisation des variables
                        break

                # Calcul de la probalilité de bailler
                self.__probabilite(cochon)

            # Prise en compte de l'age du cochon dans
            self.proba = self.proba * dico_age[self.age]

            # Nouvelles coordonnées du cochon
            self.x1 += self.DX
            self.y1 += self.DY

            # Déplacement du cochon
            can.coords(self.rond, self.x1, self.y1, self.x1 + diametre, self.y1 + diametre)

            # Baillement transmis
            self.__baillement_transmission()

            # Baillement spontannée
            self.__baillement_spontane()

            # Vieillissement
            self.vieillissement()

            # Mouvement de 50ms
            fen.after(150, self.mouvement)


################
#   Fonctions  #
################

def pause():
    global stop
    stop = 0 if stop == 1 else 1

    # Reprise du mouvement
    if stop == 0:
        for cochon in ensemble_cochon:
            cochon.mouvement()


class Porcherie:
    def __init__(self, nb_cochon):
        nb_cochon = scale.get()
        # Mise en pause du mouvement précédent
        global stop, ensemble_cochon
        stop = 1

        # Effacement des formes
        can.delete(tk.ALL)

        # Récupération du nombre de cochon
        nb_cochon = scale.get()

        # Calcul de la distance optimale entre les cochons
        distance_inter_cochon = math.sqrt((Taille_canva ** 2 - diametre) / nb_cochon) - diametre

        # Initialisation des variables
        ensemble_cochon = []
        dx, dy = 0, 0

        # Création des cochons
        while dy < Taille_canva - diametre:
            while dx < Taille_canva - diametre:
                if len(ensemble_cochon) == nb_cochon:
                    break
                name = Cochon(dx, dy)
                ensemble_cochon.append(name)
                dx += diametre + distance_inter_cochon  # Permet de ne pas faire spawn les cochons au même endroit

            if len(ensemble_cochon) == nb_cochon:
                break

            dy += diametre + distance_inter_cochon
            dx = 0  # retour à la ligne

        # Déplacement des cochons
        for cochon in ensemble_cochon:
            cochon.mouvement()


def generateur_de_cochon():
    # Mise en pause du mouvement précédent
    global stop, ensemble_cochon
    stop = 1

    # Effacement des formes
    can.delete(tk.ALL)

    # Récupération du nombre de cochon
    nb_cochon = scale.get()

    # Calcul de la distance optimale entre les cochons
    distance_inter_cochon = math.sqrt((Taille_canva ** 2 - diametre) / nb_cochon) - diametre

    # Initialisation des variables
    ensemble_cochon = []
    dx, dy = 0, 0

    # Création des cochons
    while dy < Taille_canva - diametre:
        while dx < Taille_canva - diametre:
            if len(ensemble_cochon) == nb_cochon:
                break
            name = Cochon(dx, dy)
            ensemble_cochon.append(name)
            dx += diametre + distance_inter_cochon  # Permet de ne pas faire spawn les cochons au même endroit

        if len(ensemble_cochon) == nb_cochon:
            break

        dy += diametre + distance_inter_cochon
        dx = 0  # retour à la ligne

    # Déplacement des cochons
    for cochon in ensemble_cochon:
        cochon.mouvement()


############################
#   Programme Principale   #
############################

def main():
    global stop, fen, Taille_canva, diametre, rayon, dico_age, can, scale

    stop = 0

    # Déclaration de la taille de notre canva
    Taille_canva = 400
    diametre = Taille_canva / 20  # Taille d'un rond
    rayon = diametre / 2

    # Création d'un dictionnaire des ages avec la proba de transmettre le baillement associée
    dico_age = {9: 0.52, 10: 0.5, 11: 0.1, 12: 0.15, 13: 0.45, 14: 0.4, 15: 0.2, 16: 0.13, 17: 0.4, 18: 0.8, 19: 0.82,
                20: 0.68, 21: 0.25, 22: 0.6}

    dico_age = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                9: 0.52, 10: 0.5, 11: 0.1, 12: 0.15, 13: 0.45, 14: 0.4, 15: 0.2, 16: 0.13, 17: 0.4, 18: 0.8, 19: 0.82,
                20: 0.68, 21: 0.25, 22: 0.6}

    # Création de la fenêtre
    fen = tk.Tk()

    # Labels
    tk.Label(fen, text="Welcome to the Pig Farm", font="Helvetica 16 bold ").pack()  # Titre
    tk.Label(fen, text=" Pig yawning simulation", font="Helvetica 12 italic ").pack()
    fen.title('Piggery yawning by Thomas C. and Mathieu G.')

    # Création de la porcherie
    can = tk.Canvas(fen, width=Taille_canva, height=Taille_canva, bg='ivory')
    can.pack(padx=5, pady=5)

    # Barre de scrooll
    value = tk.DoubleVar()
    scale = tk.Scale(fen, from_=1, to=200, variable=value, orient='horizontal')
    scale.pack()

    # Bouttons
    bouton_generateur = tk.Button(fen, text="Creation", command=generateur_de_cochon)
    bouton_generateur.pack(side=tk.LEFT, padx=100)

    bouton_pause = tk.Button(fen, text="Start/Pause", command=pause)
    bouton_pause.pack(side=tk.LEFT)

    fen.mainloop()


main()
