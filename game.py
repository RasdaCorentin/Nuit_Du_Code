import pyxel 
class Game: 
    def __init__(self):
        self.width = 256
        self.height = 256
        self.player = Player(self.width // 2, 50, self)
        self.list_bulle = [] 
        self.bulle1 = Bulle(50,275)
        self.bulle2 = Bulle(75,350)
        self.floor = Floor()
        self.bar = Barre(self)
        self.collide = False
        self.on_ground = False
        self.musique = True
        pyxel.init(self.width, self.height, title="Un jeu", fps=60)
        pyxel.load("1.pyxres")
        pyxel.run(self.update, self.draw)
        
    def update(self):
        self.player.move_player()
        self.check_collision()
        if self.floor.y > 250:
            self.move(self.floor)
        for bulle in self.list_bulle:
            self.move(bulle)
        self.bar.update_event()
        self.creation_bulle()

    def draw(self):
        pyxel.cls(0)
        self.bar.draw_barre()
        self.bar.draw_barre_event()
        self.floor.draw_floor()
        self.player.draw_player_explosion()
        for bulle in self.list_bulle:
            bulle.draw_bulle()

    def creation_bulle(self):
        self.bulle_x = pyxel.rndf(0,256)
        if pyxel.frame_count % 60 == 0:
            self.list_bulle.append(Bulle(self.bulle_x, 200))

    def move(self, elem):
        elem.y -= 1

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

    def music(self):
        if self.musique :
            pyxel.playm(0, tick = None, loop = True)
            self.musique = False

class Player:
    def __init__(self, x , y, game):
        self.width = 16
        self.height = 12
        self.x = x
        self. y = y
        self.pression = 0.15
        self.game = game

    def draw_player(self):
        pyxel.blt(self.x,self.y,0,32,10,self.width,self.height)

    def draw_player_explosion(self):
        self.count = pyxel.frame_count
        if self.count < 10:
            pyxel.blt(self.x, self.y, 0,16,96,8,8)
        elif self.count < 20 :
            pyxel.blt(self.x, self.y, 0,32,88,8,8)
        elif self.count < 30 :
            pyxel.blt(self.x, self.y, 0,18,107,12,11)
        elif self.count < 40 : 
            pyxel.blt(self.x, self.y, 0,34,107,12,11)
        


    def move_player(self):
            if self.game.collide:
                self.game.bar.height_event -= 1
            if self.game.floor.y < 252:
                if not self.game.on_ground:
                    self.y += 0.5
            if pyxel.btn(pyxel.KEY_LEFT):
                self.x -= 1
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.x += 1
class Barre:
    def __init__(self, game):
        self.x = 249
        self.y = 0
        self.width = 7
        self.height = 50
        self.height_event = 0
        self.height_event_max = 50
        self.game = game

    def draw_barre(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 7)

    def draw_barre_event(self):
        pyxel.rect(self.x, self.y, self.width, self.height_event, 3)
    
    def update_event(self):
        if self.height_event < self.height_event_max:
            self.height_event += self.game.player.pression

class Floor:
    def __init__(self):
        self.width = 256
        self.height = 6
        self.x = 0
        self.y = 600

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
