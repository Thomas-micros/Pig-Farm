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

    def __init__(self, dx, dy, can, fen, canva_size=600):
        """
        contructeur :
            - Initialise un attribut nommé visual représentant le cochon en lui même
            - Initialise les attributs nommés x1,y1,x2,y2 correspondant aux coordonnées du cochon
            - Initialise un attribut nommé sexe correspondand au sexe du cochon
            - Initialise un attribut nommé age correspondant à l'age du cochon
        """
        # Détermination du sexe
        self.sexe = 'male' if random.random() < 0.5 else 'femelle'

        # Détermination de l'age
        self.age = random.randint(0, 22)
        self.jours = 0

        # Initialisation des variables utilisées

# ###################################################
# BALISE 1

        self.x1 = 0  # Nouvelles coordonnées
        self.x2 = 0  # Nouvelles coordonnées
        self.y1 = 0  # Nouvelles coordonnées
        self.y2 = 0  # Nouvelles coordonnées

        self.dx = dx  # vitesse en x
        self.dy = dy  # vitesse en y

        self.DX = 0  # déplacement en x
        self.DY = 0  # déplacement en y

# ###################################################
        self.visual = 0  # cochon
        self.piggy_size = 0  # Taille du cochon

        self.decompte = 0  # Décompte du temps de récupération entre deux baillements



        self.can = can  # canvas de la porcherie
        self.fen = fen  # fenetre tkinter

        self.canva_size = canva_size
        self.diametre = self.canva_size / 20

        self.proba = 0

        # Probabilité de baillement selon l'age du cochon
        self.dico_age = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                         9: 0.52, 10: 0.5, 11: 0.1, 12: 0.15, 13: 0.45, 14: 0.4, 15: 0.2, 16: 0.13, 17: 0.4, 18: 0.8,
                         19: 0.82, 20: 0.68, 21: 0.25, 22: 0.6, 23: 0}

    def __str__(self):
        return f"Cochon {self.sexe}, position {str(self.dy)[0:3]} : {str(self.dx)[0:3]}"

    def piggy(self):

        if 9 <= self.age <= 22:
            self.piggy_size = self.diametre
            self.visual = self.can.create_oval(3 + self.dx, 3 + self.dy, 3 + self.piggy_size + self.dx,
                                               3 + self.piggy_size + self.dy, width=1, fill='DeepPink2')
        else:
            self.piggy_size = self.diametre/1.2
            self.visual = self.can.create_oval(2 + self.dx, 2 + self.dy, 2 + self.piggy_size + self.dx,
                                               2 + self.piggy_size + self.dy, width=1, fill='LightPink1')

        self.x1, self.y1, self.x2, self.y2 = self.can.bbox(self.visual)

    def __direction(self):
        """
        Méthode renvoyant deux attributs DX, DY correspondant au déplacement aléatoire du cochon
        """
        angle = random.uniform(0, 2 * math.pi)
        self.DX = 10 * math.cos(angle)
        self.DY = 10 * math.sin(angle)

    def __distance(self, other_PIG):
        """
        Méthode qui pour l'instance et un autre cochon donné calcule la distance
        les séparant nommé longueur.
        """
        # Calcul du centre du cochon déplacé de DX, DY
        centredx1 = self.x1 + self.DX + self.diametre/2
        centredy1 = self.y1 + self.DY + self.diametre/2

        # Calcul le centre du deuxième cochon
        centrex2 = other_PIG.x1 + self.diametre/2
        centrey2 = other_PIG.y1 + self.diametre/2

        # Calcul de la distance entre les deux cochons
        self.longueur = math.sqrt((centredx1 - centrex2) ** 2 + (centredy1 - centrey2) ** 2) - self.diametre

    def __Wall_bouncing(self):
        # rebond à droite et à gauche
        if self.x1 + self.piggy_size + self.DX > self.canva_size or self.x1 + self.DX < 0:
            self.DX = -self.DX

        # rebond en bas et en haut
        if self.y1 + self.piggy_size + self.DY > self.canva_size or self.y1 + self.DY < 0:
            self.DY = -self.DY

    def __spont_yawning(self):
        """
        Méthode permettant de déclancher un baillement spontanné pour le cochon.
        Modification du decompte correspondant au temps de récupération entre deux baillement.
        """
        if not self.age < 9 and random.random() < 0.001 and self.decompte == 0:
            self.can.itemconfig(self.visual, fill='Green2')
            self.decompte = 3

    def __contag_yawning(self):
        """
        Méthode permettant de faire bailler le cochon selon la proprabilité "proba"  correspondante
        """
        if random.random() < self.proba and self.decompte == 0:
            self.can.itemconfig(self.visual, fill='Green2')
            self.decompte = 3

    def __yawning_shield(self):
        """
        Méthode permettant de protéger un cochon d'un rebaillement pendant la durée du décompte.
        """
        if 9 <= self.age <= 22:
            if self.decompte > 0:
                self.can.itemconfig(self.visual, fill='grey')  # Cochon protégé
                self.decompte -= 1
            else:
                self.can.itemconfig(self.visual, fill='DeepPink2')  # Cochon déprotégé

    def __yawning_probability(self, other_PIG):
        # Calcul de la probalilité de bailler

        if self.can.itemcget(other_PIG.visual, 'fill') == 'Green2' and other_PIG.sexe == "male":
            if other_PIG.sexe == "male":
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

    def __aging(self):  # Permet le vieillissement d'un cochon une fois tout les 30 tours
        if self.jours == 30:
            self.jours = 0
            if self.age < 23:
                self.age += 1
                if self.age == 9:
                    self.piggy_size = self.diametre
            else:
                self.age = 1
                self.piggy_size = self.diametre/1.2
                self.can.itemconfig(self.visual, fill='LightPink1')
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
            self.__yawning_shield()

            # Par défaut garde les valeurs DX,DY précédentes sinon initialisation de l'attribut DX et DY
            if not hasattr(self, 'DX'):
                self.__direction()

            # levage du blocage du mouvement
            if self.DX == 0 or self.DY == 0:
                self.__direction()

            # initilisation des variables
            self.proba = 0

            # Controle des parois
            self.__Wall_bouncing()

            for PIG in Piggy_list:  # Parcours l'ensemble des cochons

                # Regarde si c'est le même cochon
                if PIG.x1 != self.x1 and PIG.y1 != self.y1:

                    self.__distance(PIG)  # Calcul de la distance avec le cochon i

                    # Contrôle de non superposition des cochons
                    if self.longueur <= 0:

                        self.DX, self.DY, proba = 0, 0, 0  # Réinitialisation des variables
                        break

                # Calcul de la probalilité de bailler
                self.__yawning_probability(PIG)

            # Prise en compte de l'age du cochon dans
            self.proba = self.proba * self.dico_age[self.age]

            # Nouvelles coordonnées du cochon
            self.x1 += self.DX
            self.y1 += self.DY

            # Déplacement du cochon
            self.can.coords(self.visual, self.x1, self.y1, self.x1 + self.piggy_size, self.y1 + self.piggy_size)

            # Baillement transmis
            self.__contag_yawning()

            # Baillement spontanné
            self.__spont_yawning()

            # Vieillissement
            self.__aging()

            # Mouvement de 50ms
            self.fen.after(125, self.mouvement)


class Counter:
    def __init__(self, nb_baillement=0):
        self.nb_baillement = nb_baillement

    def add_baillement(self):
        self.nb_baillement += 1

    def set_nb_baillement(self, nb):
        self.nb_baillement = nb

    def get_nb_baillement(self):
        return self.nb_baillement


def pause():

    global stop
    stop = 0 if stop == 1 else 1

    # Reprise du mouvement
    if stop == 0:
        for PIG in Piggy_list:
            PIG.mouvement()


class Root(tk.Tk):

    """
    Classe d'affichage
    """

    def __init__(self, canva_size=600):
        tk.Tk.__init__(self)
        self.label = tk.Label(self, text="", width=10)

        # Variables
        self.nb_baillement = 0

        self.canva_size = canva_size
        self.diametre = self.canva_size / 20

        # Labels
        tk.Label(self, text="\n\n Pig yawning simulation\n", font="Arial 12 italic ").pack()

        self.title('Piggery yawning by Thomas C. and Mathieu G.')

        self.canvas = tk.Canvas(self, width=self.canva_size, height=self.canva_size, bg='ivory')
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

        # self.label.pack()
        # self.remaining = 0
        # self.count(10)

        # global Yawning_count
        #
        # self.label.configure(text=Yawning_count)
        #
        # Yawning_count = Tkinter_variable(master=None)
        # var.set(Yawning_count)

    def erase(self):
        # Effacement des formes
        self.canvas.delete(tk.ALL)

    def generateur_de_cochon(self):
        # Mise en pause du mouvement précédent
        global stop, Piggy_list, Yawning_count
        stop = 1
        Yawning_count = 0

        # Effacement des formes
        self.erase()

        # Récupération du nombre de cochon
        nb_cochon = self.scale.get()

        # Calcul de la distance optimale entre les cochons
        distance_inter_cochon = math.sqrt((self.canva_size ** 2 - self.diametre) / nb_cochon) - self.diametre

        # Initialisation des variables
        Piggy_list = []
        dx, dy = 0, 0

        # Création des cochons
        while dy < self.canva_size - self.diametre:
            while dx < self.canva_size - self.diametre:
                if len(Piggy_list) == nb_cochon:
                    break
                name = Cochon(dx, dy, can=self.canvas, fen=self)
                name.piggy()
                Piggy_list.append(name)
                dx += self.diametre + distance_inter_cochon  # Permet de ne pas faire spawn les cochons au même endroit

            if len(Piggy_list) == nb_cochon:
                break

            dy += self.diametre + distance_inter_cochon
            dx = 0  # retour à la ligne

        # Déplacement des cochons
        for PIG in Piggy_list:
            PIG.mouvement()



# Programme principal


def main():

    global stop
    stop = 0

    PIG_FARM = Root()
    PIG_FARM.mainloop()


main()
