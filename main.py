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

    def __init__(self, dx, dy, can, fen):
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
        self.jours = 0

        # Définition des variables utilisées dans le __init__

        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0

        self.rond = 0  # cochon
        self.taille = 0  # Taille du cochon

        self.decompte = 0  # Décompte du temps de récupération entre deux baillements

        self.dx = dx  # vitesse en x ?/!\  /!\  /!\  /!\  /!\  /!\  /!\  /!\  /!\  /!\  /!\  /!\ à vérifier !
        self.dy = dy  # vitesse en y ?

        self.DX = 0  # déplacement en x ? /!\  /!\  /!\  /!\  /!\  /!\  /!\  /!\  /!\  /!\  /!\  /!\ à vérifier !
        self.DY = 0  # déplacement en y

        self.can = can  # canvas de la porcherie
        self.fen = fen  # fenetre tkinter

        self.proba = 0

        # Probabilité de baillement selon l'age du cochon
        self.dico_age = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                         9: 0.52, 10: 0.5, 11: 0.1, 12: 0.15, 13: 0.45, 14: 0.4, 15: 0.2, 16: 0.13, 17: 0.4, 18: 0.8,
                         19: 0.82, 20: 0.68, 21: 0.25, 22: 0.6, 23: 0}

    def __str__(self):
        return f"Cochon {self.sexe}, position {str(self.dy)[0:3]} : {str(self.dx)[0:3]}"

    def forme(self):

        if 9 <= self.age <= 22:
            self.taille = diametre
            self.rond = self.can.create_oval(3 + self.dx, 3 + self.dy, 3 + self.taille + self.dx,
                                             3 + self.taille + self.dy, width=1, fill='DeepPink2')
        else:
            self.taille = diametre/1.2
            self.rond = self.can.create_oval(3 + self.dx, 3 + self.dy, 3 + self.taille + self.dx,
                                             3 + self.taille + self.dy, width=1, fill='LightPink1')

        self.x1, self.y1, self.x2, self.y2 = self.can.bbox(self.rond)

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
        centredx1 = self.x1 + self.DX + diametre/2
        centredy1 = self.y1 + self.DY + diametre/2

        # Calcul le centre du deuxième cochon
        centrex2 = cochon2.x1 + diametre/2
        centrey2 = cochon2.y1 + diametre/2

        # Calcul de la distance entre les deux cochons
        self.longueur = math.sqrt((centredx1 - centrex2) ** 2 + (centredy1 - centrey2) ** 2) - diametre

    def __control_parois(self):
        # rebond à droite et à gauche
        if self.x1 + self.taille + self.DX > Taille_canva or self.x1 + self.DX < 0:
            self.DX = -self.DX

        # rebond en bas et en haut
        if self.y1 + self.taille + self.DY > Taille_canva or self.y1 + self.DY < 0:
            self.DY = -self.DY

    def __baillement_spontane(self):
        """
        Méthode permettant de déclancher un baillement spontanné pour le cochon.
        Modification du decompte correspondant au temps de récupération entre deux baillement.
        """
        if not self.age < 9 and random.random() < 0.001 and self.decompte == 0:
            self.can.itemconfig(self.rond, fill='Green2')
            self.decompte = 3

    def __baillement_transmission(self):
        """
        Méthode permettant de faire bailler le cochon selon la proprabilité "proba"  correspondante
        """
        if random.random() < self.proba and self.decompte == 0:
            self.can.itemconfig(self.rond, fill='Green2')
            self.decompte = 3

    def __baillement_protection(self):
        """
        Méthode permettant de protéger un cochon d'un rebaillement pendant la durée du décompte.
        """
        if 9 <= self.age <= 22:
            if self.decompte > 0:
                self.can.itemconfig(self.rond, fill='grey')  # Cochon protégé
                self.decompte -= 1
            else:
                self.can.itemconfig(self.rond, fill='DeepPink2')  # Cochon déprotégé

    def __probabilite(self, cochon2):
        # Calcul de la probalilité de bailler

        if self.can.itemcget(cochon2.rond, 'fill') == 'Green2' and cochon2.sexe == "male":
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

    def vieillissement(self):  # Permet le vieillissement d'un cochon une fois tout les 30 tours
        if self.jours == 30:
            self.jours = 0
            if self.age < 23:
                self.age += 1
                if self.age == 9:
                    self.taille = diametre
            else:
                self.age = 1
                self.taille = diametre/1.2
                self.can.itemconfig(self.rond, fill='LightPink1')
        else:
            self.jours += 1

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
            self.proba = self.proba * self.dico_age[self.age]

            # Nouvelles coordonnées du cochon
            self.x1 += self.DX
            self.y1 += self.DY

            # Déplacement du cochon
            self.can.coords(self.rond, self.x1, self.y1, self.x1 + self.taille, self.y1 + self.taille)

            # Baillement transmis
            self.__baillement_transmission()

            # Baillement spontannée
            self.__baillement_spontane()

            # Vieillissement
            self.vieillissement()

            # Mouvement de 50ms
            self.fen.after(120, self.mouvement)


class Counter:
    def __init__(self, nb_baillement=0):
        self.nb_baillement = nb_baillement

    def add_baillement(self):
        self.nb_baillement += 1

    def set_nb_baillement(self, nb):
        self.nb_baillement = nb

    def get_nb_baillement(self):
        return self.nb_baillement


################
#   Fonctions  #
################

def pause():
    global stop  # V A R I A B L E S G L O B A L
    stop = 0 if stop == 1 else 1

    # Reprise du mouvement
    if stop == 0:
        for cochon in ensemble_cochon:
            cochon.mouvement()


class Root(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.label = tk.Label(self, text="", width=10)

        # Variables
        self.nb_baillement = 0

        # Labels
        tk.Label(self, text="\n Welcome to the Pig Farm", font="Arial 20 bold ").pack()

        tk.Label(self, text="\n\n Pig yawning simulation\n", font="Arial 12 italic ").pack()

        self.title('Piggery yawning by Thomas C. and Mathieu G.')

        self.canvas = tk.Canvas(self, width=Taille_canva, height=Taille_canva, bg='ivory')
        self.canvas.pack(padx=5, pady=5)

        # Barre de scroll
        value = tk.DoubleVar()
        self.scale = tk.Scale(self, from_=2, to=200, length=600, variable=value, orient='horizontal')
        self.scale.pack()

        # Spacer
        tk.Label(self, text="\n").pack()

        # Boutons
        self.b_gen = tk.Button(self, text="Creation", command=self.generateur_de_cochon)
        self.b_gen.pack()

        # Spacer
        tk.Label(self, text="\n").pack()

        self.b_pause = tk.Button(self, text="Start/Pause", command=pause)
        self.b_pause.pack()

        tk.Label(self, text="\n").pack()

        tk.Label(self, text=f"Nombre de baillements : ", font="Arial 12 italic ").pack()

        # #############################################################

        self.label.pack()
        self.remaining = 0
        self.countdown(10)

    def erase(self):
        # Effacement des formes
        self.canvas.delete(tk.ALL)

    def generateur_de_cochon(self):
        # Mise en pause du mouvement précédent
        global stop, ensemble_cochon  # V A R I A B L E S G L O B A L
        stop = 1

        # Effacement des formes
        self.erase()

        # Récupération du nombre de cochon
        nb_cochon = self.scale.get()

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
                name = Cochon(dx, dy, can=self.canvas, fen=self)
                name.forme()
                ensemble_cochon.append(name)
                print(name)
                dx += diametre + distance_inter_cochon  # Permet de ne pas faire spawn les cochons au même endroit

            if len(ensemble_cochon) == nb_cochon:
                break

            dy += diametre + distance_inter_cochon
            dx = 0  # retour à la ligne

        # Déplacement des cochons
        for cochon in ensemble_cochon:
            cochon.mouvement()

    def countdown(self, remaining=None):
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.label.configure(text="time's up!")
        else:
            self.label.configure(text="%d" % self.remaining)
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)


# Programme principal

def main():
    global stop, Taille_canva, diametre  # V A R I A B L E S G L O B A L

    stop = 0

    # Déclaration de la taille de notre canva
    Taille_canva = 600
    diametre = Taille_canva / 20  # Taille d'un rond

    app = Root()
    app.mainloop()


main()
