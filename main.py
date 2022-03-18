#####################
#   Bibliotheques   #
#####################

import tkinter as tk
import math
import random

#################
#   Classes   #
#################


class Pigs:
    """
    Classe définissant un cochon.
    Prend en entrée (__init__) :
     - la position initiale en x (posx) et en y (posy)
     - Le canva de la porcherie (can)
     - La fenêtre tkinter (fen)
     - La taille du canvas (canva_size)
    """

    def __init__(self, posx, posy, can, fen, canva_size=600):

        # Détermination du sexe
        self.sexe = 'male' if random.random() < 0.5 else 'femelle'

        # Détermination de l'age
        self.age = random.randint(0, 22)
        self.jours = 0

        # Initialisation des variables utilisées

# ##########################################################################
# BALISE 1 - Gestion du déplacement des cochons

        # Coordonnées du cochon
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

        self.DX = 0  # pas en x
        self.DY = 0  # pas en y

# ##########################################################################

        # Initialisation des variables utilisées

        self.posx = posx  # position initiale sur le canva en x
        self.posy = posy  # position initiale sur le canva en y

        self.visual = 0  # cochon
        self.piggy_size = 0  # Taille du cochon

        self.recup = 0  # Décompte du temps de récupération entre deux baillements

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
        return f"Cochon {self.sexe}, position {str(self.posy)[0:3]} : {str(self.posx)[0:3]}"

    def piggy(self):

        # ##########################################################################
        # BALISE 2
        """
        Visuel du cochon selon son age
        """

        # cochon adulte
        if 9 <= self.age <= 22:
            self.piggy_size = self.diametre
            self.visual = self.can.create_oval(self.posx,  # x1
                                               self.posy,  # x2
                                               self.posx + self.piggy_size,  # x2
                                               self.posy + self.piggy_size,  # y2
                                               width=1, fill='DeepPink2')

        # cochonnet
        else:
            self.piggy_size = self.diametre/1.2
            self.visual = self.can.create_oval(self.posx,  # x1
                                               self.posy,  # x2
                                               self.posx + self.piggy_size,  # x2
                                               self.posy + self.piggy_size,  # y2
                                               width=1, fill='LightPink1')

        self.x1, self.y1, self.x2, self.y2 = self.can.bbox(self.visual)

        # ##########################################################################

    def __direction(self):

        # ##########################################################################
        # BALISE 3
        """
        Renvoie la direction aléatoire du cochon après l'initialisation/une rencontre inter-cochon
        """
        angle = random.uniform(0, 2 * math.pi)
        self.DX = 10 * math.cos(angle)
        self.DY = 10 * math.sin(angle)

        # ##########################################################################

    def __distance(self, other_pig):

        # ##########################################################################
        # BALISE 5
        """
        Renvoie la distance inter-cochon
        """
        # Calcul du centre du cochon déplacé de DX, DY
        centredx1 = self.x1 + self.DX + self.diametre/2
        centredy1 = self.y1 + self.DY + self.diametre/2

        # Calcul le centre du deuxième cochon
        centrex2 = other_pig.x1 + self.diametre/2
        centrey2 = other_pig.y1 + self.diametre/2

        # Calcul de la distance entre les deux cochons
        self.longueur = math.sqrt((centredx1 - centrex2) ** 2 + (centredy1 - centrey2) ** 2) - self.diametre

        # ##########################################################################

    def __wall_bouncing(self):

        # ##########################################################################
        # BALISE 4
        """
        Fait rebondir les cochons qui se heurtent à une parois en inversant DX et DY
        """
        # rebond à droite et à gauche
        if self.x1 + self.piggy_size + self.DX > self.canva_size or self.x1 + self.DX < 0:
            self.DX = -self.DX

        # rebond en bas et en haut
        if self.y1 + self.piggy_size + self.DY > self.canva_size or self.y1 + self.DY < 0:
            self.DY = -self.DY

        # ##########################################################################

        # ##########################################################################
        # BALISE 8 - Gestion du baillement

    def __spont_yawning(self):
        """
        Déclenche un baillement spontanné en ajoutant un temps de récupération (recup)
        """
        if not self.age < 9 and random.random() < 0.001 and self.recup == 0:
            self.can.itemconfig(self.visual, fill='Green2')
            self.recup = 5

    def __contag_yawning(self):
        """
        Faire bailler le cochon selon sa proprabilité correspondante.
        concretement : rend le cochon vert
        """
        if random.random() < self.proba and self.recup == 0:
            self.can.itemconfig(self.visual, fill='Green2')
            self.recup = 5

    def __yawning_shield(self):
        """
        Protege un cochon d'un rebaillement pendant la durée du décompte.
        """
        if 9 <= self.age <= 22:
            if self.recup > 0:
                self.can.itemconfig(self.visual, fill='grey')  # Cochon protégé
                self.recup -= 1
            elif self.recup == 0:
                self.can.itemconfig(self.visual, fill='DeepPink2')  # Cochon déprotégé

    def __yawning_probability(self, other_pig):
        # Calcul de la probalilité de bailler

        if self.can.itemcget(other_pig.visual, 'fill') == 'Green2' and other_pig.sexe == "male":
            if other_pig.sexe == "male":

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

        # ##########################################################################

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

        # Interromp la boucle si pause
        if stop == 1:
            pass

        else:
            # initialisation du temps de recup à 0
            if not hasattr(self, 'recup'):
                self.recup = 0

            # Protection post baillement
            self.__yawning_shield()

            # Par défaut garde les valeurs DX,DY précédentes sinon initialisation de l'attribut DX et DY
            if not hasattr(self, 'DX'):
                self.__direction()

            # initilisation des variables
            self.proba = 0

            # levage du blocage du mouvement
            if self.DX == 0 or self.DY == 0:
                self.__direction()

            # Controle des parois
            self.__wall_bouncing()

            # ##########################################################################
            # Balise 6 - Iteration dans l'ensemble des cochons (sauf lui-même) pour :

            # - calculer la distance inter-cochon
            # - contrôler la superposition
            # - si superposition, étourdir le cochon (relancer la direction aléatoire
            # - calculer la probabilité de bailler en fonction de la distance

            for PIG in Piggy_list:
                if PIG.x1 != self.x1 and PIG.y1 != self.y1:

                    self.__distance(PIG)

                    if self.longueur <= 0:
                        self.DX, self.DY, proba = 0, 0, 0  # Étourdissement
                        break

                self.__yawning_probability(PIG)

            # ##########################################################################

            # Prise en compte de l'age du cochon dans
            self.proba = self.proba * self.dico_age[self.age]

            # ##########################################################################
            # Balise 7 - avancée des cochons en actualisant leur coordonées

            self.x1 += self.DX
            self.y1 += self.DY

            self.can.coords(self.visual, self.x1, self.y1, self.x1 + self.piggy_size, self.y1 + self.piggy_size)

            # ##########################################################################

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

        tk.Label(self, text="Légende :\n"
                            "Petit cercle rose pâle : cochonnet de moins de 9 mois (ne baillant pas)\n"
                            "Cercle rose : cochon prêt à bailler\n"
                            "Cercle vert : cochon baillant\n"
                            "Cercle gris : cochon ne pouvant plus bailler", font="Arial 18 italic ").pack()

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
        distance_inter_cochon = math.sqrt((self.canva_size ** 2 - self.diametre) / nb_cochon)  - self.diametre

        # Initialisation des variables
        Piggy_list = []
        posx, posy = 0, 0

        # Création des cochons
        while posy < self.canva_size - self.diametre:
            while posx < self.canva_size - self.diametre:
                if len(Piggy_list) == nb_cochon:
                    break
                pig_name = Pigs(posx, posy, can=self.canvas, fen=self, canva_size=self.canva_size)
                pig_name.piggy()
                Piggy_list.append(pig_name)
                posx += self.diametre + distance_inter_cochon

            if len(Piggy_list) == nb_cochon:
                break

            posy += self.diametre + distance_inter_cochon
            posx = 0  # retour à la ligne

        # Déplacement des cochons
        for PIG in Piggy_list:
            PIG.mouvement()


def main():

    global stop
    stop = 0

    pig_farm = Root()
    pig_farm.mainloop()


main()
