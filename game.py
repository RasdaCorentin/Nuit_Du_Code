import pyxel 
class Game: 
    def __init__(self):
        self.width = 256
        self.height = 256
        self.player = Player(50,50, self)
        self.list_bulle = [] 
        self.bulle1 = Bulle(50,75)
        self.bulle2 = Bulle(50,150)
        self.floor = Floor()
        self.list_bulle.append(self.bulle1)
        self.list_bulle.append(self.bulle2)
        self.collide = False
        self.on_ground = False
        pyxel.init(self.width, self.height, title="Un jeu")
        #load
        pyxel.load("1.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.move_player()
        self.check_collision()

    def draw(self):
        pyxel.cls(0)
        self.floor.draw_floor()
        self.player.draw_player()
        for bulle in self.list_bulle:
            bulle.draw_bulle()

    def check_collision(self):
        isCollision_wfloor = Collider(self.player, self.floor).collide()
        if isCollision_wfloor:
            self.on_ground = True
        else :
            self.on_ground = False
            
        for bulle in self.list_bulle:
            isCollision = Collider(self.player, bulle).collide()
            if isCollision:
                self.collide = True
                break
            else :
                self.collide = False
            
                

class Player:
    def __init__(self, x , y, game):
        self.width = 16
        self.height = 12
        self.x = x
        self. y = y
        self.gravity = 1
        self.game = game

    def draw_player(self):
        pyxel.blt(self.x,self.y,0,32,10,self.width,self.height)

    def move_player(self):
            if self.game.collide:
                self.y += (self.gravity - 0.5)
            if not self.game.on_ground and not self.game.collide:
                self.y += self.gravity
            if pyxel.btn(pyxel.KEY_LEFT):
                self.x += 1
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.x -= 1
class Floor:
    def __init__(self):
        self.width = 256
        self.height = 6
        self.x = 0
        self.y = 250

    def draw_floor(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 3)

class Bulle:
    def __init__(self, x, y):
        self.width = 8
        self.height = 8
        self.x = x
        self. y = y

    def draw_bulle(self):
        pyxel.blt(self.x,self.y,0,24,88,self.width,self.height)

class Collider:
    def __init__(self, obj1, obj2):
        self.obj1 = obj1
        self.obj2 = obj2

    def collide(self):
        return self.obj1.x + self.obj1.width > self.obj2.x and self.obj1.x < self.obj2.x + self.obj2.width and self.obj1.y + self.obj1.height > self.obj2.y and self.obj1.y < self.obj2.y + self.obj2.height
    
Game()
