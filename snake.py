import pygame
import sys
import random

pygame.font.init()

#Variabeln definieren
WIDTH = 500
HEIGHT = 500
FPS = 12
font_name = pygame.font.match_font('arial')
score = 0

#Das Fenster auf welchem gespielt wird, wird gemacht.
window = pygame.display.set_mode((WIDTH,HEIGHT))

#Der Titel des Fensters wird zu Snake geändert.
pygame.display.set_caption("Snake")

#Die Variabel fps wird definiert, um sicher zu gehen das, dass Spiel auf allen Computern gleich schnell läuft.
fps = pygame.time.Clock()

#Class mit allen Funktionen welche mit der Schlange zu tun haben.
class Snake():

    #Funktion welche die grundlegenden Variablen für die Schlange initiiert.
    def __init__(self):
        self.position = [100,50]
        self.body = [[100,50],[100,40],[100,30]]
        self.direction = "DOWN"
        self.changeDirectionTo = self.direction

    #Funktion welche die Richtung, in welche die Schlange geht, wechselt und kontrolliert ob die Richtung der Schlange sich überhaupt zu dieser Richtung wechseln darf.
    def changeDirTo(self,dir):
        if dir=="RIGHT" and not self.direction=="LEFT":
            self.direction = "RIGHT"
        if dir=="LEFT" and not self.direction=="RIGHT":
            self.direction = "LEFT"
        if dir=="UP" and not self.direction=="DOWN":
            self.direction = "UP"
        if dir=="DOWN" and not self.direction=="UP":
            self.direction = "DOWN"

    #Funktion welche die Schlange vorwärts bewegt.
    def move(self,foodPos):
        if self.direction == "RIGHT":
            self.position[0] += 10
        if self.direction == "LEFT":
            self.position[0] -= 10
        if self.direction == "UP":
            self.position[1] -= 10
        if self.direction == "DOWN":
            self.position[1] += 10
        self.body.insert(0,self.position[:])
        if self.position == foodPos:
            return 1
        else:
            self.body.pop()
            return 0

    #Funktion welche überprüft ob die Schlange mit der Wand oder mit sich selber kollidiert ist.
    def checkCollision(self):
        if self .position[0] > WIDTH-1 or self.position[0] < 0:
            return 1
        elif self.position[1] > HEIGHT-1 or self.position[1] < 0:
            return 1
        for part in self.body[1:]:
                if self.position == part:
                    return 1
        else:
            return 0
    #Funktion welche die die Anfangswerte wiederherstellt, wenn das Spiel neu gestartet wird.
    def reset(self):
        self.position = [100,50]
        self.body = [[100,50],[100,40],[100,30]]
        self.direction = "DOWN"
        self.changeDirectionTo = self.direction

    #Funktion welche die Positionen der Körperteile ausgibt.
    def getBody(self):
        return self.body

class FoodSpawner():

    #Funktion welche grundlegende Variabeln für den Apfel initiiert.
    def __init__(self):
        self.position = [random.randrange(1,WIDTH/10)*10, random.randrange(1,HEIGHT/10)*10]
        self.isFoodOnScreen = True

    #Funktion welche einen neuen Apfel platziert, wenn der vorherige gegessen wurde.
    def spawnFood(self):
        if self.isFoodOnScreen == False:
            self.position = [random.randrange(1,50)*10, random.randrange(1,50)*10]
            self.isFoodOnScreen = True
        return self.position

    #Funktion welche die obige funktion aktiviert, wenn der Apfel gegessen wurde.
    def setFoodOnScreen(self,b):
        self.isFoodOnScreen = b

#Es werden die Funktion Snake() mit snake und die Funktion FoodSpawner() mit foodSpawner gleich gesetzt, um das weitere arbeiten zu erleichtern.
snake =  Snake()
foodSpawner = FoodSpawner()

#Es wird eine Funktion definiert, mit welcher auf dem GameOver-Screen der Text geschrieben werden kann.
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (173, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#Funktion welche den GameOver-Screen macht und im Falle
def gameOver():
    window.fill(pygame.Color(73, 73, 73))
    draw_text(window, "GAME OVER", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(window, "press any button to restart", 40, WIDTH / 2, (HEIGHT / 4)+60)
    draw_text(window, "Score: "+ str(score), 64, WIDTH / 2, HEIGHT / 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        fps.tick(24)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                snake.reset()
                waiting = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver();
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.changeDirTo('RIGHT')
            if event.key == pygame.K_LEFT:
                snake.changeDirTo('LEFT')
            if event.key == pygame.K_UP:
                snake.changeDirTo('UP')
            if event.key == pygame.K_DOWN:
                snake.changeDirTo('DOWN')
    foodPos = foodSpawner.spawnFood()
    if(snake.move(foodPos)==1):
        score += 1
        foodSpawner.setFoodOnScreen(False)

    window.fill(pygame.Color(73, 73, 73))
    for pos in snake.getBody():
        pygame.draw.rect(window,pygame.Color(0,225,0),pygame.Rect(pos[0],pos[1],10,10))
    pygame.draw.rect(window,pygame.Color(225,0,0),pygame.Rect(foodPos[0],foodPos[1],10,10))
    if(snake.checkCollision()==1):
        gameOver()
        score = 0
    pygame.display.set_caption("Snake | Score: "+ str(score))
    pygame.display.flip()
    fps.tick(FPS)
