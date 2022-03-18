import tkinter as tk
import math
import random

# ### Définition des classes :


class Pigs:
    """
    Classe définissant un cochon.
    Prend en entrée (__init__) :
     - la position initiale en x (posx) et en y (posy)
     - Le canva de la porcherie (can)
     - La fenêtre tkinter (fen)
     - La taille du canvas (canva_size)

     La gestion des bâillement se fait à partir de l'age et de la couleur du cochon :
     rose pâle (LightPink1) : cochonnet de moins de 9 mois (ne bâillant pas)
     rose (DeepPink2) : cochon prêt à bâiller\n"
     vert (Green2) : cochon bâillant\n"
     gris (grey) : cochon ne pouvant plus bâiller
    """

    def __init__(self, posx, posy, can, fen, canva_size=500):

        # Détermination du sexe
        self.sexe = 'male' if random.random() < 0.5 else 'femelle'

        # Détermination de l'age
        self.age = random.randint(0, 22)
        self.jours = 0

        # ## Initialisation des variables utilisé
        # Coordonnées du cochon
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0

        self.DX = 0  # pas en x
        self.DY = 0  # pas en

        self.posx = posx  # position initiale sur le canva en x
        self.posy = posy  # position initiale sur le canva en y

        self.visual = 0  # cochon
        self.piggy_size = 0  # Taille du cochon

        self.recup = 0  # Décompte du temps de récupération entre deux bâillements

        self.can = can  # canvas de la porcherie
        self.fen = fen  # fenetre tkinter

        self.canva_size = canva_size
        self.diametre = self.canva_size / 20

        self.proba = 0

        # Probabilité de bâillement selon l'age du cochon
        self.dico_age = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                         9: 0.52, 10: 0.5, 11: 0.1, 12: 0.15, 13: 0.45, 14: 0.4, 15: 0.2, 16: 0.13, 17: 0.4, 18: 0.8,
                         19: 0.82, 20: 0.68, 21: 0.25, 22: 0.6, 23: 0}

    def __str__(self):
        return f"Cochon {self.sexe}, position {str(self.posy)[0:3]} : {str(self.posx)[0:3]}"

    def piggy(self):
        """
        Génère le visuel du cochon (visual) selon son age et sa position
        """

        # cochon adulte #
        if 9 <= self.age <= 22:
            self.piggy_size = self.diametre
            self.visual = self.can.create_oval(self.posx,  # x1
                                               self.posy,  # y1
                                               self.posx + self.piggy_size,  # x2
                                               self.posy + self.piggy_size,  # y2
                                               width=1, fill='DeepPink2')

        # cochonnet #
        else:
            self.piggy_size = self.diametre/1.2
            self.visual = self.can.create_oval(self.posx,  # x1
                                               self.posy,  # y1
                                               self.posx + self.piggy_size,  # x2
                                               self.posy + self.piggy_size,  # y2
                                               width=1, fill='LightPink1')

        self.x1, self.y1, self.x2, self.y2 = self.can.bbox(self.visual)

    def __direction(self):
        """
        Renvoie la direction aléatoire du cochon après l'initialisation OU une rencontre inter-cochon
        """
        angle = random.uniform(0, 2 * math.pi)
        self.DX = 10 * math.cos(angle)
        self.DY = 10 * math.sin(angle)

    def __distance(self, other_pig):
        """
        Renvoie la distance inter-cochon pour une paire de cochon
        """
        # Calcul du centre du cochon déplacé de DX, DY
        centredx1 = self.x1 + self.DX + self.diametre/2
        centredy1 = self.y1 + self.DY + self.diametre/2

        # Calcul le centre du deuxième cochon
        centrex2 = other_pig.x1 + self.diametre/2
        centrey2 = other_pig.y1 + self.diametre/2

        # Calcul de la distance entre les deux cochons
        self.dist = math.sqrt((centredx1 - centrex2) ** 2 + (centredy1 - centrey2) ** 2) - self.diametre

    def __wall_bouncing(self):
        """
        Fait rebondir les cochons qui se heurtent à une parois du canva en inversant DX et DY
        """
        # rebond à droite et à gauche
        if self.x1 + self.piggy_size + self.DX > self.canva_size or self.x1 + self.DX < 0:
            self.DX = -self.DX

        # rebond en bas et en haut
        if self.y1 + self.piggy_size + self.DY > self.canva_size or self.y1 + self.DY < 0:
            self.DY = -self.DY

    def __spont_yawning(self):
        """
        Déclenche un bâillement spontanné (rend le cochon vert == bâillement) et ajoute un temps de récupération (recup)
        """
        if not self.age < 9 and random.random() < 0.0007 and self.recup == 0:
            self.can.itemconfig(self.visual, fill='Green2')
            self.recup = 6

    def __contag_yawning(self):
        """
        Fait bâiller le cochon selon sa proprabilité correspondante.
        concretement : rend le cochon vert (== bâillement) et ajoute un temps de recup
        """
        if random.random() < self.proba and self.recup == 0:
            self.can.itemconfig(self.visual, fill='Green2')
            self.recup = 6

    def __yawning_shield(self):
        """
        Protege un cochon d'un rebâillement pendant le temps de recup, le rend gris pour symboliser cette récupération
        et fait diminuer le temps de recup. Si recup == 0, rend le cochon rose à nouveau (prêt à bâiller)
        """
        if 9 <= self.age <= 22:
            if self.recup > 0:
                self.can.itemconfig(self.visual, fill='grey')  # Cochon protégé
                self.recup -= 1

            elif self.recup == 0:
                self.can.itemconfig(self.visual, fill='DeepPink2')  # Cochon déprotégé

    def __yawning_probability(self, other_pig):
        """
        Calcule la probabilité de bâiller et la renvoie dans self.proba
        """
        # Calcul de la probalilité de bâiller

        if self.can.itemcget(other_pig.visual, 'fill') == 'Green2' and other_pig.sexe == "male":
            if other_pig.sexe == "male":

                if self.dist < self.canva_size/50:
                    self.proba += 0.65 * 0.4
                elif self.dist < self.canva_size/5:
                    self.proba += 0.2 * 0.4
                else:
                    self.proba += 0.25 * 0.4

            else:  # proba si autre cochon == femelle
                if self.dist < self.canva_size/50:
                    self.proba += 0.65 * 0.28
                elif self.dist < self.canva_size/5:
                    self.proba += 0.2 * 0.28
                else:
                    self.proba += 0.25 * 0.28

    def __aging(self):
        """
        Fait vieillir le cochon d'un mois tout les 30 itération de la mainloop,
        renvoie l'age dans self.age et modifie le visuel en fonction de l'age
        """

        if self.jours == 30:
            self.jours = 0

            if self.age < 23:
                self.age += 1
                if self.age == 9:
                    self.piggy_size = self.diametre
            else:  # Le cochon renait de ses cendres après 22 mois, piste d'amélioration
                self.age = 1
                self.piggy_size = self.diametre/1.2
                self.can.itemconfig(self.visual, fill='LightPink1')
        else:
            self.jours += 1

    def mouvement(self):
        """
        Méthode de mouvement, s'interrompt si la simulation est en pause (stop == 1)

        """

        # Interrompt la boucle si pause activée
        if stop == 1:
            pass

        else:
            # initialisation du temps de recup à 0
            if not hasattr(self, 'recup'):
                self.recup = 0

            # Protection post bâillement
            self.__yawning_shield()

            # DX, DY précédentes sinon initialisation par la méthode direction
            if not hasattr(self, 'DX'):
                self.__direction()

            # remise des probas à 0
            self.proba = 0

            # levage du blocage du mouvement
            if self.DX == 0 or self.DY == 0:
                self.__direction()

            # Controle des parois, rebondit si prochain pas DX ou DY heurte la paroi du canva
            self.__wall_bouncing()

            # - calculer la distance inter-cochon
            # - contrôler la superposition
            # - si superposition, étourdir le cochon (relancer la direction aléatoire)
            # - calculer la probabilité de bâiller en fonction de la distance

            for PIG in Piggy_list:
                if PIG.x1 != self.x1 and PIG.y1 != self.y1:

                    self.__distance(PIG)

                    if self.dist <= 0:
                        self.DX, self.DY, proba = 0, 0, 0  # Étourdissement
                        break

                self.__yawning_probability(PIG)

            # Prise en compte de l'age du cochon dans
            self.proba = self.proba * self.dico_age[self.age]

            self.x1 += self.DX
            self.y1 += self.DY

            self.can.coords(self.visual, self.x1, self.y1, self.x1 + self.piggy_size, self.y1 + self.piggy_size)

            # bâillement contagieux
            self.__contag_yawning()

            # bâillement spontanné
            self.__spont_yawning()

            # Vieillissement
            self.__aging()

            # Mouvement de 75 ms
            self.fen.after(75, self.mouvement)


class Root(tk.Tk):

    """
    Affichage du GUI par tkinter
    """

    def __init__(self, canva_size=500):
        tk.Tk.__init__(self)
        self.label = tk.Label(self, text="", width=10)

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
                            "Petit cercle rose pâle : cochonnet de moins de 9 mois (ne bâillant pas)\n"
                            "Cercle rose : cochon prêt à bâiller\n"
                            "Cercle vert : cochon bâillant\n"
                            "Cercle gris : cochon ne pouvant plus bâiller", font="Arial 13 italic ").pack()

    def erase(self):
        """
        Efface les formes présentes dans le canvas
        """
        self.canvas.delete(tk.ALL)

    def generateur_de_cochon(self):
        """
        Génère les cochons, au nombre de nb_cochon récupéré dans la Doublevar(),
        les positionne dans le canvas, appelle le mouvement des cochons pour tout les cochons
        """
        global stop, Piggy_list

        stop = 1  # Met la simulation en pause
        Piggy_list = []
        posx, posy = 0, 0

        self.erase()

        nb_cochon = self.scale.get()

        # Calcul de la distance optimale entre les cochons lors de l'initialisation
        init_distance_inter_cochon = math.sqrt((self.canva_size ** 2 - self.diametre) / nb_cochon) - self.diametre

        # Génération des cochons sur le canvas
        while posy < self.canva_size - self.diametre:
            while posx < self.canva_size - self.diametre:
                if len(Piggy_list) == nb_cochon:
                    break
                pig_name = Pigs(posx, posy, can=self.canvas, fen=self, canva_size=self.canva_size)
                pig_name.piggy()
                Piggy_list.append(pig_name)
                posx += self.diametre + init_distance_inter_cochon

            if len(Piggy_list) == nb_cochon:
                break

            posy += self.diametre + init_distance_inter_cochon
            posx = 0  # retour à la ligne

        for PIG in Piggy_list:
            PIG.mouvement()


# ### Définition des fonctions :


def pause():
    """
    Renvoie la variable global stop après l'avoir inversé.
    Si stop == 0, appelle la méthode mouvement pour tous les cochons
    """

    global stop
    stop = 0 if stop == 1 else 1

    if stop == 0:
        for PIG in Piggy_list:
            PIG.mouvement()


def main():
    """
    Fonction principale du programme.
    Génère le GUI (pig_farm) et sa mainloop
    """
    pig_farm = Root()
    pig_farm.mainloop()


main()
