"""
   Author: daniel peng
   date: March 2018
   description: space invaders sprites and logic for varies different game components such as players and invaders.
"""
import pygame 

class Invader(pygame.sprite.Sprite):
    """
    This is the invader class. It takes 8 parameter. (x,y, end right, end left, point value, dx speed, dy speed, image number)
    """
    def __init__(self, x, y, end_right, end_left, point, dx, dy, image_num):
        pygame.sprite.Sprite.__init__(self)
        
        if 1 <= image_num <= 3:
            self.sprite_name = "./alien stuff/alien_"+str(image_num)+".png"
            self.animation_name = "./alien stuff/alien_"+str(image_num)+"_animation.png"
        if image_num == 10:
            self.sprite_name = "./alien stuff/boss.png"
            self.animation_name = "./alien stuff/boss.png"
            
        self.sprite1 = pygame.image.load(self.sprite_name)
        self.sprite2 = pygame.image.load(self.animation_name)
        
        self.image = self.sprite1
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = x 
        self.rect.centery = y
        self.end_right = end_right - 25
        self.end_left = end_left
        self.counter = 0
        self.point = point
        self.__dy = dy
        self.__dx = dx  
               
    def get_point(self):
        """
        This returns the points of each invader
        """
        return self.point
    
    def update(self):
        """
        This is the update of invader class 
        """
        self.counter += 1
            
        if self.counter == 20: 
            if self.image == self.sprite1:
                self.image = self.sprite2 
            else:
                self.image = self.sprite1
            self.counter = 0

        if self.rect.right >= self.end_right:
            self.rect.centery += self.__dy
            self.__dx = -self.__dx
        if self.rect.left <= self.end_left:
            self.rect.centery += self.__dy
            self.__dx = -self.__dx

        self.rect.centerx += self.__dx
            
class Boss_health(pygame.sprite.Sprite):
    """
    This is the boss health class
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.x = 1080
        self.y = 25
        self.image = self.image = pygame.Surface((self.x, self.y)) 
        self.image.fill((48, 232, 23))
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.left = 0
        self.health = 40
    
    def set_health(self):
        """
        This sets the boss health
        """
        self.health -= 1 
    
    def get_health(self):
        """
        This returns boss health
        """
        return self.health
    
    def resize(self):
        """
        This resizes the boss health bar
        """
        self.x -= 27
        if self.x > 0:
            self.image = pygame.Surface((self.x, self.y))
            if 13 <= self.health <= 25:
                self.image.fill((232, 225, 23))
            if self.health <= 12:
                self.image.fill((232, 23, 23))
            if 26 <= self.health:
                self.image.fill((48, 232, 23))

            
class Player(pygame.sprite.Sprite):
    """
    This is the player class
    """
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        
        self.normal = pygame.image.load("./player stuff/player.png").convert_alpha()
        self.blow_up = pygame.image.load("./player stuff/player_death_1.png").convert_alpha()
        self.blow_up_2 = pygame.image.load("./player stuff/player_death_2.png").convert_alpha()
        self.image = self.normal
        self.rect = self.image.get_rect()
        
        self.screen = screen
        self.rect.centery = self.screen.get_height() - 55
        self.rect.centerx = self.screen.get_width() / 2
        self.control = False 
        self.__dx = 9
        self.counter = 0
        self.value = False

    def set_value(self, value):
        """
        This sets the bool value of the animation variable
        """
        self.value = value 
    
    def get_value(self):
        """
        This returns the bool value 
        """
        return self.value
    
    def go_right(self):
        """
        This allows the player move right
        """
        self.rect.centerx += self.__dx
        
    def go_left(self):
        """
        This allows the player move left
        """
        self.rect.centerx -= self.__dx
        
    def update(self):
        """
        This is the update of player class
        """
        if self.value:
            self.counter += 1
            self.__dx = 0 
            if self.counter == 5:
                self.image = self.blow_up
            if self.counter == 15:
                self.image = self.blow_up_2
            if self.counter == 25:
                self.value = False
                self.image = self.normal
                self.counter = 0 
                self.__dx = 9 
                self.rect.centerx = 540
                
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.screen.get_width():
            self.rect.right = self.screen.get_width()
        
class Barrier(pygame.sprite.Sprite):
    """
    This is the barrier class
    """
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((10, 10))
        self.image.fill((255,255,255))
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = x 
        self.rect.centery = y
         
class Bullet(pygame.sprite.Sprite):
    """
    This is the bullet class 
    """
    def __init__(self,  x, y, speed, image_value):
        pygame.sprite.Sprite.__init__(self)

        if image_value:
            self.image = pygame.Surface((5, 15))
            self.image.fill((255,255,255))
            self.image.convert()  
        else:
            self.image = pygame.image.load("./alien stuff/alien_bullet.png")
            
        self.rect = self.image.get_rect()
        self.rect.centerx = x 
        self.rect.centery = y 
        self.y = y 

        self.__dy = speed
        self.control = False
    
    def go_left(self):
        """
        This allows the bullet to move left
        """
        self.rect.centerx -= 9
    
    def go_right(self):
        """
        This allows the bullet to move right
        """
        self.rect.centerx += 9
    
    def set_control(self, value):
        """
        This sets the control variable
        """
        self.control = value
        
    def get_control(self):
        """
        This returns control value
        """
        return self.control
    
    def force_set(self, pos):
        """
        This sets the position of the bullet
        """
        self.rect.center = pos
 
    def reset(self, playerx, playery):
        """
        This resets the bullet position
        """
        self.rect.center = (playerx, playery)

    def update(self):
        """
        This is the update of bullet class
        """
        if self.control:
            self.rect.centery += self.__dy 
            
        if self.rect.right > 1060:
            self.rect.right = 1060
        if self.rect.left < 20:
            self.rect.left = 20
            
        if self.rect.centery > 750:
            self.kill()
             
class Life(pygame.sprite.Sprite):
    """
    This is the life class
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.life = 3 
        self.__font = pygame.font.Font("./assests/fonts/Kermesse.ttf", 30)
        
    def set_life(self):
        """
        This sets the life value 
        """
        self.life -= 1 

    def get_life(self):
        """
        This returns the life value
        """
        return self.life
    
    def instance_lose(self):
        """
        This sets life = 0
        """
        self.life = 0

    def update(self):
        """
        This is the update of life class
        """
        message = "LIFE = %d" % self.life
        self.image = self.__font.render(message, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = 750
        self.rect.centery = 50 

class Score(pygame.sprite.Sprite):
    """
    This is the score class
    """
    def __init__(self, points):
        pygame.sprite.Sprite.__init__(self)
        
        self.score = 0
        self.__font = pygame.font.Font("./assests/fonts/Kermesse.ttf", 30)

    def set_score(self, points):
        """
        This changes the score
        """
        self.score += points
    
    def get_score(self):
        """
        This returns the score value 
        """
        return self.score
        
    def update(self):
        """
        This displays the score
        """
        message = "SCORE =  %d" % self.score
        self.image = self.__font.render(message, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = 240
        self.rect.centery = 50    

class Zone(pygame.sprite.Sprite):
    """
    This is the zone class
    """
    def __init__(self, y):
        """
        This is the init of the zone class, it positions the zone
        """
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((1081, 17))
        self.image = self.image.convert()
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = -1  
            
class Game_menu_sign(pygame.sprite.Sprite):
    """
    This is the game manu sign
    """
    def __init__(self):
        """
        This is the init of the game menu class. It loads in an image and positions it at (540, 200)
        """
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("./background stuff/space invader sign thing.png")
        self.rect = self.image.get_rect()
        self.rect.center = (540, 200)

class Game_menu_button(pygame.sprite.Sprite):
    """
    This is the class that creates buttons for the game menu, takes 3 parameter ( (x,y), colour1, colour2)
    """
    def __init__(self, position, colour_1, colour_2):
        pygame.sprite.Sprite.__init__(self)
        

        self.rect1 = pygame.Surface((175, 100))
        self.rect1.fill(colour_1)
        self.rect2 = pygame.Surface((175, 100))
        self.rect2.fill(colour_2)

        self.image = self.rect1
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.value = False
        
    def set_value(self, value):
        """
        This changes the bool value of the animation variable
        """
        self.value = value
        
    def update(self):
        """
        This is the update of game menu class, it changes animations
        """
        if self.value:
            self.image = self.rect2 
        else:
            self.image = self.rect1

class General_text(pygame.sprite.Sprite):
    """
    This is the general text class, it takes 4 parameter (message, (x,y), colour, size)
    """
    def __init__(self, message, position, colour, size):
        pygame.sprite.Sprite.__init__(self)
        self.colour = colour
        self.message = message
        self.position = position
        self.__font = pygame.font.Font("./assests/fonts/Kermesse.ttf", size)
    
    def update(self):
        """
        This is the update of General_text class
        """
        self.image = self.__font.render( self.message, 1, self.colour)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        
    
        


