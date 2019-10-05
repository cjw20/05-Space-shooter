import sys, logging, open_color, arcade, random

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 1980
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Space Shooter"
STARTING_LOCATION = (990,100)
MARGIN = 20

BULLET_DAMAGE = 10
ENEMY_HP = 30
HIT_SCORE = 10
KILL_SCORE = 100
ENEMY_START = 9



class Window(arcade.Window):

    def __init__(self, width, height, title):

        # Call the parent class's init function
        super().__init__(width, height, title)

        # Make the mouse disappear when it is over the window.
        # So we just see our object, not the pointer.
        self.set_mouse_visible(False)
        arcade.set_background_color(open_color.black)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        
        self.player = Player()
        self.score = 0
       
    
    def setup(self):
        for i in range(ENEMY_START):
            x = 198 * (i+1) 
            y = random.randint(500,1000)  #spawns inital meteors
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy) 
                     
          
    def update(self, delta_time):
        
        self.bullet_list.update()

        for e in self.enemy_list:
            hit = arcade.check_for_collision_with_list(e,self.bullet_list)
            for f in hit:
                e.hp = e.hp - BULLET_DAMAGE
                f.kill()

                if e.hp <= 0:
                    e.kill()
                    self.score = self.score + KILL_SCORE

                    x = random.randint(198,1880)        #spawns new meteors at top of screen when one is destroyed
                    y = 1080
                    enemy = Enemy((x,y)) 
                    self.enemy_list.append(enemy)    
                    x = random.randint(198,1880)        
                    y = 1080
                    enemy = Enemy((x,y)) 
                    self.enemy_list.append(enemy)    
                    
                else:
                    self.score = self.score + HIT_SCORE
                   
            impact = arcade.check_for_collision(e,self.player)            
            if impact == True:
                print('Your Score Was:', self.score)   #ends game and prints score when player runs into a meteor
                sys.exit("THANKS FOR PLAYING")

        self.enemy_list.update()   #updates enemy position
                  

    def on_draw(self):

        
        arcade.start_render()
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 100, open_color.white, 50)
        self.player.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()


  

    def on_mouse_motion(self, x, y, dx, dy):
       
        self.player.center_x = x
        self.player.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
       
        
        if button == arcade.MOUSE_BUTTON_LEFT:
            x = self.player.center_x
            y = self.player.center_y + 15
            bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
            self.bullet_list.append(bullet)
           
  

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
      
       
        super().__init__("assets/R_laser.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
      
        self.center_x += self.dx
        self.center_y += self.dy



class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/player.png", 0.6)
        (self.center_x, self.center_y) = STARTING_LOCATION

    

class Enemy(arcade.Sprite):
    def __init__(self, position):
       
        
        super().__init__("assets/meteor1.png", 0.6)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position
        self.dx = random.randint(-2,2)
        self.dy = random.randint(-2,2)
    
    def update(self):
        self.center_x += self.dx
        self.center_y += self.dy

        if self.center_x <= MARGIN:    #makes enemies switch directions when they reach the end of the window
            self.center_x = MARGIN
            self.dx = abs(self.dx)
        if self.center_x >= SCREEN_WIDTH - MARGIN:
            self.center_x = SCREEN_WIDTH - MARGIN
            self.dx = abs(self.dx)*-1
        if self.center_x <= MARGIN:
            self.center_x = MARGIN
            self.dx = abs(self.dx)
        if self.center_y <= MARGIN:
            self.center_y = MARGIN
            self.dy = abs(self.dy)
        if self.center_y >= SCREEN_HEIGHT - MARGIN:
            self.center_y = SCREEN_HEIGHT - MARGIN
            self.dy = abs(self.dy)*-1



def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
  

if __name__ == "__main__":
    main()
