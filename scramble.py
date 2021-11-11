import pygame, random, math #Importation

pygame.init()


#Variables

#Création de la fenêtre
fen_width = 1920
fen_height = 1033
fen_size = (fen_width, fen_height)
fen = pygame.display.set_mode(fen_size)
fen_surface = pygame.display.get_surface() #On fait de la fenêtre

#Varibale pour les boucles
run = True
run_menu = True

background_menu = pygame.image.load("background.png").convert_alpha()

full_screen = False

Vitesse = 2

fenetre = 0 #Permet de savoir dans quelle fenêtre du menu on se trouve

List_sol = []
List_plafond = []

fps = 60 #On défini le nombre d'image par secondes

clock = pygame.time.Clock()


with open("save.txt", "r") as f:
    b = f.read()
    f.close()
Meilleur_score = int(b)

pygame.mixer.music.load('BlueNavi-Starcade.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.7)

#importations de sprites
sprite_vaisseau = [pygame.image.load('starship1.png').convert_alpha(), pygame.image.load('starship2.png').convert_alpha(), pygame.image.load('starship3.png').convert_alpha(), pygame.image.load('starship4.png').convert_alpha(), pygame.image.load('starship5.png').convert_alpha()]
sprite_bombe = pygame.image.load('bombe.png').convert_alpha()

#importations de sons
son_missile = pygame.mixer.Sound('missile.wav')
son_explosion = pygame.mixer.Sound('explosion.wav')






#Classes
class Vaisseau(object):
    """La classe qui défini notre vaisseau !"""

    def __init__(self):
        """Créations de notre vaisseau. Il des attributs x, y définissant sa position, width et height définissant sa hitbox, vel déterminant sa vélocité,
        mort et mort2 permenant de savoir s'il est mort (False si vivant), coldown1 et coldown2 pour permettre un délai dans le ses tirs, score pour le score, max pour sa quantité d'essence max,
        essence pour sa quantité d'essence, bougex et bougey pour savoir s'il bouge, walkcount pour animé son sprite."""
        self.x = 50
        self.y = 200
        self.width = 50
        self.height = 25
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.vel = 8
        self.mort = False
        self.mort2 = False
        self.coldown1 = 0
        self.coldown2 = 0
        self.score = 1
        self.max = 1000
        self.essence = 1000
        self.accelerate = 0
        self.bougey = False
        self.bougex = False
        self.walkcount= 0


    def draw(self, fen, fen_width):
        """Méthode permetant d'afficher le vaisseau. Prends la surface d'affichage en paramètre"""
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.essence > 0:
            fen.blit(sprite_vaisseau[self.walkcount // 5], (self.x, self.y))
            self.walkcount += 1
            if self.walkcount > 15:
                self.walkcount = 0
        else:
            fen.blit(sprite_vaisseau[4], (self.x, self.y))

        pygame.draw.rect(fen, (0, 150, 0), (fen_width//2-self.max//2, 10, self.max, 30)) #On dessine la barre d'essence max
        pygame.draw.rect(fen, (0, 250, 0), (fen_width//2-self.max//2, 10, self.essence, 30)) #On dessine la barre d'essence

        font = pygame.font.SysFont("comicsans", 50)
        text = font.render("Fuel", 1, (255, 255, 255))
        fen.blit(text, (fen_width // 2 + self.max // 2 + 10, 10))


    def move(self, key):
        """Méthode s'occupant du mouvement du vaisseau. Prends pygame.key.get_pressed() en paramètre"""
        if key[pygame.K_w] and self.y >= (50 + self.vel) and self.essence > 0: #Si on appuie sur la touche Z
            if self.accelerate < 5: #On avance un peu
                self.y -= self.vel
            elif self.accelerate < 15: #On avance un peu plus
                self.y -= self.vel * 2
            elif self.accelerate < 20:
                self.y -= self.vel * 3 #On avance encore un peu plus
            else:
                self.y -= self.vel * 4 #On au max, ça permet de faire une accélération
                self.essence -= 0.1 #On en profite pour retirer l'essence consumée

        elif key[pygame.K_s] and self.y <= (fen_height - self.height - self.vel): #Idem pour S
            if self.accelerate < 5:
                self.y += self.vel
            elif self.accelerate < 15:
                self.y += self.vel * 2
            elif self.accelerate < 20:
                self.y += self.vel * 3
            else:
                self.y += self.vel * 4
                self.essence -= 0.1

        if key[pygame.K_d] and self.x <= (fen_width - self.width - self.vel): #Idem pour D
            if self.accelerate < 5:
                self.x += self.vel
            elif self.accelerate < 15:
                self.x += self.vel * 2
            elif self.accelerate < 20:
                self.x += self.vel * 3
            else:
                self.x += self.vel * 4
                self.essence -= 0.1

        elif key[pygame.K_a] and self.x >= (0 + self.vel): #Idem pour Q
            if self.accelerate < 5:
                self.x -= self.vel
            elif self.accelerate < 15:
                self.x -= self.vel * 2
            elif self.accelerate < 20:
                self.x -= self.vel * 3
            else:
                self.x -= self.vel * 4
                self.essence -= 0.1


    def fire(self, key):
        """Méthode s'occupant des projectiles du vaisseau. Prends pygame.key.get_pressed() en paramètre"""
        key2 = pygame.mouse.get_pressed()
        if key2[0] == 1 and self.coldown1 == 0: #Si on appuie sur clic gauche de la sourie
            son_missile.play() #On joue le son du missile
            missile = Missile((self.x + self.width), (self.y + self.height // 2 + 4)) #On créer un missile
            Missile_list.append(missile) #On le met dans une liste pour pouvoir l'afficher
            self.coldown1 = 1

        if key[pygame.K_SPACE] and self.coldown2 == 0: #Pareil pour espace
            self.essence -= 5
            bombe = Bombe((self.x + self.width // 2), (self.y + self.height))
            Bombe_list.append(bombe)
            self.coldown2 = 1

        if self.coldown1 > 0 and self.coldown1 < 10: #Permet de faire le délai du tire de missile
            self.coldown1 +=1
        else:
            self.coldown1 = 0

        if self.coldown2 > 0 and self.coldown2 < 10: #Et celui des bombes
            self.coldown2 += 1
        else:
            self.coldown2 = 0



vaisseau = Vaisseau()




class Ennemy(object):
    """Classe des ennemis à abattre !"""

    def __init__(self, x, y, id):
        """Prends en argument x, y et son id. Il y a 4 types d'ennemy, et donc 4 id, allant de 1 à 4."""
        self.x = x
        self.y = y
        self.id = id
        if self.id == 1:
            self.width = 40
            self.height = 40
            self.sprite = pygame.image.load("Ennemy_1.png").convert_alpha()
        elif self.id == 2:
            self.width = 20
            self.height = 40
            self.sprite = pygame.image.load("Ennemy_2.png").convert_alpha()
        elif self.id == 3:
            self.width = 40
            self.height = 20
            self.sprite = pygame.image.load("Ennemy_3.png").convert_alpha()
        elif self.id == 4:
            self.width = 50
            self.height = 25
            self.sprite = pygame.image.load("Ennemy_4.png").convert_alpha()
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.detect1 = pygame.Rect(self.x, self.y - 400, self.width, 1080)
        if self.id == 2:
            self.vel = random.randint(5, 15)
        elif self.id == 3:
            self.vel = random.randint(2, 7)
        elif self.id == 4:
            self.vel = random.randint(1, 4)
        self.go = False
        self.routine = 0



    def draw(self, fen):
        """Méthode qui affiche l'ennemie, prends en paramètre la surface d'affichage"""
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.id == 1:
##            pygame.draw.rect(fen, (0, 0, 150), self.hitbox)
            fen.blit(self.sprite, (self.x, self.y))
        elif self.id == 2:
            self.detect1 = pygame.Rect(self.x, self.y - 600, self.width, 600)
##            pygame.draw.rect(fen, (0, 150, 255), self.hitbox)
            fen.blit(self.sprite, (self.x, self.y))
        elif self.id == 3:
##            pygame.draw.rect(fen, (255, 0, 0), self.hitbox)
            fen.blit(self.sprite, (self.x, self.y))
        elif self.id == 4:
##            pygame.draw.rect(fen, (150, 0, 255), self.hitbox)
            fen.blit(self.sprite, (self.x, self.y))


    def move(self, vitesse, fen_width):
        """Méthode qui défini son déplacement. Prends en paramètre la vitesse du jeu """
        global Projectiles_list
        if self.id == 1:
            self.x -= vitesse

        elif self.id == 2:
            self.x -= vitesse
            if self.detect1.colliderect(vaisseau.hitbox):
                self.go = True
            if self.go:
                self.y -= self.vel

        elif self.id == 3:
            self.x -= vitesse
            if self.routine < 10:
                self.routine += 1
                self.x -= self.vel
                self.y -= self.vel
            elif self.routine < 20:
                self.routine += 1
                self.x -= self.vel
                self.y += self.vel
            elif self.routine < 30:
                self.routine += 1
                self.x += self.vel
                self.y += self.vel
            elif self.routine < 40:
                self.routine += 1
                self.x += self.vel
                self.y -= self.vel
            else:
                self.routine = 0

        elif self.id == 4:
            if self.x < fen_width - 50:
                if self.routine < 10:
                    self.x -= self.vel
                elif self.routine < 20:
                    self.x -= self.vel * 2
                elif self.routine < 30:
                    self.x -= self.vel * 3
                else:
                    self.x -= self.routine
                self.routine += 1
            else:
                self.x -= vitesse


    def occuper(self):
        l = []
        for i in range(self.width//10):
            l.append(self.x+10*i)
        return l


    def mort(self):
        """Méthode définissant son comportement à sa mort"""
        if self.id == 1:
            vaisseau.score += 5
            vaisseau.essence += 50
            if vaisseau.essence > vaisseau.max: #Permet d'éviter de dépasser la limite max d'essence
                vaisseau.essence = vaisseau.max
        elif self.id == 2:
            vaisseau.score += 10
        elif self.id == 3:
            vaisseau.score += 15
        else:
            vaisseau.score += 20


Ennemy_list = []




class Paysage():
    """La classe qui créra notre paysage"""

    def __init__(self, x, y):
        """Prends ses positions x et y en paramètre"""
        self.x = x
        self.y = y
        self.width = 10
        self.height = 20
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.sprite = pygame.image.load("sol.png").convert_alpha()

    def draw(self, fen):
        """Méthode affichant notre paysage. Prends la surface en paramètre."""
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        if (self.y < 599):
            fen.blit(self.sprite, (self.x, 0), (0, 0, 10, self.y+20))
        else:
            fen.blit(self.sprite, (self.x, self.y), (0, 0, 10, 20))
##        pygame.draw.rect(fen, (0, 0, 0), self.hitbox) (0, 0, 10, 1080-self.y)


List_sol = []



class Missile(object):
    """La classe des missile de notre vaisseau"""

    def __init__(self, x, y):
        """Prends ses positions initiales x et y en paramètre"""
        self.x = x
        self.y = y
        self.width = 10
        self.height = 4
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.vel = 8
        self.mov = 0
        self.sprite = pygame.image.load("fire.png").convert_alpha()


    def draw(self, fen):
        """Méthode affichant notre paysage. Prends la surface en paramètre."""
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
##        pygame.draw.rect(fen, (255, 0, 0), self.hitbox)
        fen.blit(self.sprite, (self.x, self.y))


    def move(self):
        """Méthode permetant le mouvement du missile. Prends la vitesse du jeu en paramètre"""
        if self.mov < 15:
            self.x += self.vel
        elif self.mov < 30:
            self.x += self.vel * 2
        else:
            self.x += self.vel * 3

        self.mov += 1



Missile_list = []






class Bombe(object):
    """La classe des bombes de notre vaisseau"""

    def __init__(self, x, y):
        """Prends ses positions initiales x et y en paramètre"""
        self.x = x
        self.y = y
        self.width = 15
        self.height = 25
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.vel = 5
        self.mov = 0


    def draw(self, fen):
        """Méthode affichant notre paysage. Prends la surface en paramètre."""
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        fen.blit(sprite_bombe, (self.x, self.y))


    def move(self, vitesse):
        """Méthode permetant le mouvement de la bombe. Prends la vitesse du jeu en paramètre"""
        if self.mov < 15:
            self.y += self.vel
        elif self.mov < 30:
            self.y +=self.vel * 2
        else:
            self.y += self.vel * 3

        self.mov += 1



Bombe_list = []





class button():
    """Classe créant les boutons"""

    def __init__(self, color, x, y ,width, height, text=''):
        """Prends en paramètre sa couleur initial, x, y, sa largeur (width), sa hauteur (height) et le texte que tu souhaite"""
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.etat = 0


    def draw(self,win,size,outline=None):
        """Méthode permettant d'afficher nos boutons. Prends en paramètre la surface (win), la taille de la police (size) et la bordure(outline). Pour la bordure, ne rien mettre pour ne pas en avoir,
        sinon mettre un int pour sa taille."""
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)

        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', size)
            text = font.render(self.text, 1, (255,255,255))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))


    def isOver(self, pos):
        """Permet de savoir si la sourie est sur un bouton. Prends en paramètre les coordonées de la sourie dans un tuple (x, y) (pos)"""
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


    def action(self, pos, col1, col2):
        """Permet de définir l'action du clique sur un bouton. Prends en paramètre les coordonées de la sourie dans un tuple (x, y) (pos), col1 et col2 qui sont des couleurs.
        col1 est la couleur de base, et col2 est la couleur quand la sourie est sur le bouton"""
        global run_menu, run, List_planfond, List_sol, Ennemy_list, vaisseau
        if self.isOver(pos):
            key2 = pygame.mouse.get_pressed() #Permet de détecter le clique de la sourie
            if key2[0] == 1:
                if self.text == 'Jouer': #On détermine l'action du bouton par rapport à son nom
                    run_menu = False
                    run = True
                    List_sol = []
                    List_sol = creation_paysage()
                    List_plafond = []
                    List_plafond = creation_plafond(fen_width)
                    Ennemy_list = []
                    Ennemy_list = Pop_ennemy(fen_width)
                    Vitesse = 2
                    vaisseau.x = 50
                    vaisseau.y = 250
                    vaisseau.score = 0
                    Avancement_niveau = 0

                elif self.text == 'Rejouer':
                    vaisseau.score = 0
                    Vitesse = 2
                    List_sol = []
                    List_sol = creation_paysage()
                    List_plafond = []
                    List_plafond = creation_plafond(fen_width)
                    Ennemy_list = []
                    Ennemy_list = Pop_ennemy(fen_width)
                    vaisseau.mort = False
                    vaisseau.mort2 = False
                    vaisseau.x = 50
                    vaisseau.y = 400
                    vaisseau.essence = vaisseau.max

                elif self.text == 'Quitter':
                    run_menu = False
                    run = False
                    RUN = False


            self.color = col2

        else:
            self.color = col1


But1 = button((0, 200, 0), fen_width//2-100, 370, 200, 40, 'Jouer')
But2 = button((0, 200, 0), fen_width//2-100, 370, 200, 40, 'Rejouer')
But3 = button((0, 200, 0), fen_width//2-100, 430, 200, 40, 'Quitter')



class Background:
    """La classe qui permet d'afficher le fonds en arrière plan et de le faire bouger"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = pygame.image.load("background2.png").convert_alpha()

    def move(self, Vitesse):
        self.x -= Vitesse
        if self.x < -3200:
            self.x = 3198

    def draw(self, fen):
        if self.x <= 1920:
            fen.blit(self.sprite, (self.x, self.y))


bckgrnd1 = Background(0, 0)
bckgrnd2 = Background(3198, 0)
listBckgrnd = [bckgrnd1, bckgrnd2]


#Fonctions
def creation_paysage():
    """Fonction créant le sol à intervalle régulier afin d'avoir un niveau infini"""
    if len(List_sol) == 0: #On vérifie si la list est vide
        x = 0
        y = 0
    elif len(List_sol) <= 200: #On vérifie si la list contient moins de 200 éléments. Si oui, on en créer 1000 de plus pour avoir un sol continu
        sol = List_sol[len(List_sol) - 1]
        x = sol.x
        y = sol.y

    if len(List_sol) <= 200:
        change = 0
        longeur = 1000
        while longeur >0:
            x += 10

            change = random.randint(0, 10)
            if change in (0, 4):
                y += 0
            elif change in (5, 7):
                y += 20
            elif change in (8, 10):
                y -= 20

            if y < 600:
                y = 600
            elif y > 1050:
                y = 1050

            sol = Paysage(x, y)
            List_sol.append(sol)

            longeur -= 1

    return List_sol




def creation_plafond(fen_width):
    """Fonction créant le plafond à intervalle régulier afin d'avoir un niveau de difficulté accrue"""
    if vaisseau.score % 2000 == 0 and len(List_plafond) < 200 and vaisseau.score > 1000:
        longeur = random.randint(500, 1500)
        x = fen_width + 100
        y = 50
        change = 0
        while longeur >0:
            sol = Paysage(x, y)
            List_plafond.append(sol)
            x += 10

            change = random.randint(0, 10)
            if change in (0, 4):
                y += 0
            elif change in (5, 7):
                y += 20
            elif change in (8, 10):
                y -= 20

            if y < 50:
                y = 50
            elif y > 300:
                y = 300
            longeur -= 1
        while y > 0:
            y -= 20
            x += 10
            sol = Paysage(x, y)
            List_plafond.append(sol)


    return List_plafond




def Pop_ennemy(fen_width):
    """Fonction faisant apparaitre nos ennemis à intervalle régulier"""
    if len(Ennemy_list) <= 10: #S'il reste moins de 10 ennemies, on en rajoute
        lg = len(List_sol)
        avance = 3
        y1 = 0
        y2 = 0
        y3 = 0
        y4 = 0
        longeur = 1000

        pris = set()
        for ennemy in Ennemy_list:
            l = ennemy.occuper()
            for nb in l:
                pris.add(nb)

        while longeur > 0 and lg > avance:
            sol = List_sol[avance]
            y1 = sol.y
            sol = List_sol[avance - 1]
            y2 = sol.y
            sol = List_sol[avance - 2]
            y3 = sol.y
            sol = List_sol[avance - 3]
            y4 = sol.y

            if y1 == y2 and y2 == y3 and y3 == y4:
                x = (avance * 10 - 30)
                y = y1
                if avance > fen_width//10 and longeur > fen_width//10:
                    pop = random.randint(0, 30)
                    if pop < 10 and vaisseau.score >= 20 and not (x in pris):
                        ennemy = Ennemy(x, y - 40, 1)
                        l = ennemy.occuper()
                        for nb in l:
                            pris.add(nb)
                        Ennemy_list.append(ennemy)
                        avance += 10
                    elif pop >= 10 and pop < 15 and vaisseau.score >= 500 and not (x in pris):
                        ennemy = Ennemy(x, y - 40, 2)
                        l = ennemy.occuper()
                        for nb in l:
                            pris.add(nb)
                        Ennemy_list.append(ennemy)
                        avance += 10
                    elif pop >=15 and pop < 20 and vaisseau.score >= 1200 and not (x in pris):
                        ennemy = Ennemy(x, 400 - random.randint(-50, 50), 3)
                        l = ennemy.occuper()
                        for nb in l:
                            pris.add(nb)
                        Ennemy_list.append(ennemy)
                        avance += 10
                    elif pop >= 20 and pop < 25 and vaisseau.score >= 1700 and not (x in pris):
                        ennemy = Ennemy(x, 400 - random.randint(-100, 100), 4)
                        l = ennemy.occuper()
                        for nb in l:
                            pris.add(nb)
                        Ennemy_list.append(ennemy)
                        avance += 10
            longeur -= 1
            avance += 1


    return Ennemy_list




def update_vitesse(vaisseau):
    """Fonction permettant de mettre à jour notre vitesse"""
    if vaisseau.score < 1000:
        Vitesse = 2
    elif vaisseau.score < 2000:
        Vitesse = 3
    elif vaisseau.score < 3000:
        Vitesse = 4
    elif vaisseau.score < 4000:
        Vitesse = 5
    elif vaisseau.score < 5000:
        Vitesse = 6
    else:
        Vitesse = 1

    return Vitesse




def update_projectiles(fen_width):
    """Fonction permettant d'afficher nos projectiles"""
    for missile in Missile_list:
        missile.move()
        missile.draw(fen)
        if missile.x > fen_width:
            Missile_list.remove(missile)

    for bombe in Bombe_list:
        bombe.move(Vitesse)
        bombe.draw(fen)

    return Missile_list, Bombe_list





def update_ennemy(fen_width):
    """Fonction permettant de faire les changements sur ennemis"""
    for ennemy in Ennemy_list:
        ennemy.move(Vitesse, fen_width)
        if ennemy.x <= fen_width:
            ennemy.draw(fen)
        if ennemy.x < 0 - ennemy.width:
            Ennemy_list.remove(ennemy)
        if ennemy.y < 50 - ennemy.height:
            Ennemy_list.remove(ennemy)
        if len(Missile_list) > 0:
            for missile in Missile_list:
                if missile.hitbox.colliderect(ennemy.hitbox):
                    ennemy.mort()
                    Ennemy_list.remove(ennemy)
                    Missile_list.remove(missile)
        if len(Bombe_list) > 0:
            for bombe in Bombe_list:
                if bombe.hitbox.colliderect(ennemy.hitbox):
                    son_explosion.play()
                    ennemy.mort()
                    Ennemy_list.remove(ennemy)
                    Bombe_list.remove(bombe)
        if vaisseau.hitbox.colliderect(ennemy.hitbox):
            vaisseau.mort = True

    return Vaisseau, Ennemy_list, Missile_list, Bombe_list




def update_terrain(fen_width):
    """Fonction permettant d'afficher et de gérer les actions du sol et du plafond"""
    for sol in List_sol:
        if sol.x < fen_width:
            sol.draw(fen)
        if sol.x < (-20 - sol.width):
            List_sol.remove(sol)
            vaisseau.score += 1
        if sol.hitbox.colliderect(vaisseau.hitbox):
            vaisseau.mort = True
        if len(Missile_list) > 0:
            for missile in Missile_list:
                if missile.hitbox.colliderect(sol.hitbox):
                    Missile_list.remove(missile)
        if len(Bombe_list) > 0:
            for bombe in Bombe_list:
                if bombe.hitbox.colliderect(sol.hitbox):
                    son_explosion.play()
                    Bombe_list.remove(bombe)
        sol.x -= Vitesse

    for sol in List_plafond:
        if sol.x < fen_width:
            sol.draw(fen)
        if sol.x < (0 - sol.width):
            List_plafond.remove(sol)
        if sol.hitbox.colliderect(vaisseau.hitbox):
            vaisseau.mort = True
        if len(Missile_list) > 0:
            for missile in Missile_list:
                if missile.hitbox.colliderect(sol.hitbox):
                    Missile_list.remove(missile)
        if len(Bombe_list) > 0:
            for bombe in Bombe_list:
                if bombe.hitbox.colliderect(sol.hitbox):
                    Bombe_list.remove(bombe)
        sol.x -= Vitesse

    return vaisseau, List_sol, List_plafond, Missile_list, Bombe_list




def raffraichissement(fen, key, vaisseau, fen_width, listBckgrnd, Vitesse):
    """Fonction permettant de raffraichir notre jeu"""
    fen.fill((255, 255, 255))
    for back in listBckgrnd:
        back.move(Vitesse)
        back.draw(fen)

    pygame.draw.rect(fen, (0, 0, 0), (0, 0, fen_width, 50))

    List_sol = creation_paysage()
    List_plafond = creation_plafond(fen_width)
    Ennemy_list = Pop_ennemy(fen_width)

    Vitesse = update_vitesse(vaisseau)

    Missile_list, Bombe_list = update_projectiles(fen_width)

    Vaisseau, Ennemy_list, Missile_list, Bombe_list = update_ennemy(fen_width)

    vaisseau, List_sol, List_plafond, Missile_list, Bombe_list = update_terrain(fen_width)


    if vaisseau.essence <= 0:
        vaisseau.essence = 0
        vaisseau.y += 2

    if not vaisseau.mort:
        vaisseau.essence -= 0.3
        vaisseau.move(key)
        vaisseau.fire(key)
        vaisseau.draw(fen, fen_width)

    score = 'Score : ' + str(vaisseau.score)
    font2 = pygame.font.SysFont("comicsans", 60)
    text2 = font2.render(score, 1, (255, 255, 255))
    fen.blit(text2, (0, 10))

    pygame.display.update()

    return vaisseau, List_sol, List_plafond, Ennemy_list, Missile_list, Bombe_list, Vitesse, listBckgrnd




def raf_menu(fen):
##    fen.fill((255, 255, 255))
    fen.blit(background_menu, (0, 0))

    string = "Appuyez sur F4 pour passer en pleins écran ou en mode fenêtré !"
    font1 = pygame.font.SysFont("comicsans", 30)
    text1 = font1.render(string, 1, (255, 255, 255))
    fen.blit(text1, (10, 10))

    But1.action(pos, (0, 150, 0), (0, 200, 0))
    But3.action(pos, (0, 150, 0), (0, 200, 0))
    But1.draw(fen, 30)
    But3.draw(fen, 30)

    pygame.display.update()




def mort(fen, Meilleur_score, fen_width):
    """Fonction permettant de gérer les actions liés à la mort"""
    score = 'Score : ' + str(vaisseau.score)
    font2 = pygame.font.SysFont("comicsans", 40)
    text2 = font2.render(score, 1, (255, 255, 255))
    fen.blit(text2, (fen_width//2 - (text2.get_width()/2), 310))

    if not vaisseau.mort2:

        if vaisseau.score > Meilleur_score:
            Meilleur_score = vaisseau.score
            score2 = 'Vous avez battu le meilleur score !'
        else:
            score2 = 'Meilleur score : ' + str(Meilleur_score)
        vaisseau.mort2 = True

        font2 = pygame.font.SysFont("comicsans", 40)
        text2 = font2.render(score2, 1, (255, 255, 255))
        fen.blit(text2, (fen_width//2 - (text2.get_width()/2), 340))

    But2.action(pos, (0, 150, 0), (0, 200, 0))
    But3.action(pos, (0, 150, 0), (0, 200, 0))
    But2.draw(fen, 30)
    But3.draw(fen, 30)
    pygame.display.update()

    return Meilleur_score, vaisseau






#Boucles
while run_menu:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            run_menu = False
            run = False

    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        run_menu = False
        run = False

    if key[pygame.K_F4]:
        if full_screen:
            fen_width = 1920
            fen_height = 1033
            fen_size = (fen_width, fen_height)
            fen = pygame.display.set_mode(fen_size)
            full_screen = False
        else:
            fen_width = 1920
            fen_height = 1080
            fen_size = (fen_width, fen_height)
            fen = pygame.display.set_mode(fen_size, pygame.FULLSCREEN)
            full_screen = True

    raf_menu(fen)



while run:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            run = False

    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        run = False



    if key[pygame.K_F4]:
        if full_screen:
            fen_width = 1920
            fen_height = 1033
            fen_size = (fen_width, fen_height)
            fen = pygame.display.set_mode(fen_size)
            full_screen = False
        else:
            fen_width = 1920
            fen_height = 1080
            fen_size = (fen_width, fen_height)
            fen = pygame.display.set_mode(fen_size, pygame.FULLSCREEN)
            full_screen = True

    if vaisseau.mort:
        pygame.mouse.set_visible(True)
        Meilleur_score, vaisseau = mort(fen, Meilleur_score, fen_width)

    else:
        pygame.mouse.set_visible(False)
        vaisseau, List_sol, List_plafond, Ennemy_list, Missile_list, Bombe_list, Vitesse, listBckgrnd = raffraichissement(fen, key, vaisseau, fen_width, listBckgrnd, Vitesse)

    clock.tick(fps) #fps


with open("save.txt", "w") as f: # gère close() automatiquement
    f.write(str(Meilleur_score))

pygame.quit()
quit()
