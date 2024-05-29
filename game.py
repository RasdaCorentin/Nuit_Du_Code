import pyxel

#constantes

START_MENU = 0
GAME = 1
GAME_OVER = 3
WIN = 2



class Game: 
    def __init__(self):
        self.width = 256
        self.height = 256
        self.game_mode = START_MENU
        self.defeat = False
        
        pyxel.init(self.width, self.height, title="Le trésor de la Buse", fps=60)
        self.reset()
        pyxel.load("ressources.pyxres")
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.player = Player(self.width // 2, 50, self)
        self.list_bulle = [] 
        self.bulle1 = Bulle(50,275)
        self.bulle2 = Bulle(75,350)
        self.floor = Floor()
        self.chest = Chest(self)
        self.bar = Barre(self)
        self.collide = False
        self.on_ground = False
        self.on_chest = False
        self.musique = True
        self.defeat = False



    def start_menu(self):
        pyxel.cls(6)
        pyxel.text(85,100,"LE TRESOR DE LA BUSE", 0)
        pyxel.text(100,200,"PRESS SPACE", 0)
        if pyxel.btnr(pyxel.KEY_SPACE):
            self.game_mode = GAME

    def game_over(self):
        pyxel.stop()
        pyxel.cls(6)
        pyxel.text(100,100,"GAME OVER", 0)
        pyxel.text(90,200,"PRESS R TO RESTART", 0)
        if pyxel.btnr(pyxel.KEY_R):
            self.game_mode = GAME
            self.reset()

    def win(self):
        pyxel.cls(6)
        pyxel.text(100,100,"YOU WON", 0)
        pyxel.text(90,200,"PRESS R TO RESTART", 0)
        if pyxel.btnr(pyxel.KEY_R):
            self.game_mode = GAME
            self.reset()
    

    def update(self):
        if not self.defeat:
            self.music()
            self.player.move_player()
            self.check_collision()
            if self.floor.y > 250:
                self.move(self.floor)
                self.move(self.chest)
            for bulle in self.list_bulle:
                self.move(bulle)
            self.bar.update_event()
            self.creation_bulle()
        if self.game_mode == GAME_OVER and pyxel.btn(pyxel.KEY_R):
            self.reset()
            self.musique = True

        if self.game_mode == WIN:
            self.win()
            self.musique = True
        


    def draw(self):
        if not self.defeat :
            pyxel.cls(5)
            self.bar.draw_barre()
            self.bar.draw_barre_event()
            self.floor.draw_floor()
            self.player.draw_player()
            if not self.on_chest:
                self.chest.draw_chest_close()
            else :
                self.chest.draw_chest_open()
                if pyxel.frame_count % 50 == 0:
                    self.game_mode = WIN

            for bulle in self.list_bulle:
                bulle.draw_bulle()
        if self.game_mode == START_MENU:
            self.start_menu()
            self.reset()
            pyxel.stop()
        if self.defeat:
            self.game_mode = GAME_OVER
            self.game_over()
            self.reset()
            pyxel.stop()
        if self.game_mode == WIN:
            self.reset()
            self.win() 

    def creation_bulle(self):
        self.bulle_x = pyxel.rndf(0,256)
        if pyxel.frame_count % 40 == 0:
            self.list_bulle.append(Bulle(self.bulle_x, 230))

    def move(self, elem):
        elem.y -= 1

    def check_collision(self):
        isCollision_wchest = Collider(self.player, self.chest).collide()
        if isCollision_wchest:
            self.on_chest = True
        else :
            self.on_chest = False
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
            if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q):
                self.x -= 1
            if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
                self.x += 1

class Chest:
    def __init__(self, game):
        self.game = game
        self.width = 256
        self.height = 6
        self.x = pyxel.rndi(5,250)
        self.y = self.game.floor.y - 6
    
    def draw_chest_close(self):
        pyxel.blt(self.x, self.y, 0 ,8, 80,8,8)

    def draw_chest_open(self):
        pyxel.blt(self.x, self.y, 0 ,16, 80,8,8)

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
        else : 
            self.game.defeat = True

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