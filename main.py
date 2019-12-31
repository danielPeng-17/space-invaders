"""
   Author: daniel peng
   date: March 2018
   description: space invaders game built with the pygame library.
"""
# import and init
import pygame, pySprites, random 
pygame.init()

def game(screen):
    """
    This is the main game. it sets up all of the aliens and wall and player objects. 
    """
    # display 
    background = pygame.image.load("./background stuff/honeycomb wall2.jpg")
    background.convert()
    screen.blit(background, (0, 0))  

    # entities   
    points = 0 
    barriers = []
    invadersList = []
    image_num = [1,1,2,2,3]
    image_num2 = [1,1,1,2,2,3]
    image_num3 = [1,1,1,2,2,2,3]
    boss_active = False 
    level_2 = False
    level_3 = False

    # makes barriers
    barrier_y = 630
    for barrierNum in range(4):
        for barrierRow in range(7):
            for barrierCol in range(13):
                barriers.append(pySprites.Barrier((barrierNum *250) + (barrierCol * 10) + 100, barrier_y))
            barrier_y -= 10
        barrier_y = 630

    # makes the first wave of invaders 
    invader_y = 280
    for row in range(5):
        for column in range(11):
            image = image_num[row]
            invadersList.append(pySprites.Invader(((column + 1)*37), invader_y, screen.get_width()-(((9) - column)*37) , (column*37), (row+1)*10 , 5,7, image))
        invader_y -= 30
    
    player_shoot = pygame.mixer.Sound("./sounds/shoot.wav")
    player_shoot.set_volume(0.3)
    
    alien_shoot = pygame.mixer.Sound("./sounds/shoot2.wav")
    alien_shoot.set_volume(0.3)
    
    invader_death = pygame.mixer.Sound("./sounds/invaderkilled.wav")
    invader_death.set_volume(0.3)
    
    player_death = pygame.mixer.Sound("./sounds/playerkilled.wav")
    player_death.set_volume(0.3)
    
    player = pySprites.Player(screen)
    barriers = pygame.sprite.OrderedUpdates(barriers)
    bullets = pygame.sprite.OrderedUpdates()
    enemyBullets = pygame.sprite.OrderedUpdates()
    invaders = pygame.sprite.OrderedUpdates(invadersList)
    bullet = pySprites.Bullet(player.rect.centerx , player.rect.top + 9, -25, True)
    boss_health = pySprites.Boss_health()
    zone = pySprites.Zone(80)
    # test
    test_bullet = pygame.sprite.OrderedUpdates()
    
    life = pySprites.Life()
    score = pySprites.Score(points)
    allSprites = pygame.sprite.OrderedUpdates(zone, score, life, bullet, barriers, invaders, player)    
        
    # alter / assign
    keepGoing = True 
    clock = pygame.time.Clock()

    # loop
    while keepGoing:
        # time
        clock.tick(30)
        # events
        key = pygame.key.get_pressed()
        
        # checks for keys pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, score.get_score(), life.get_life()
            
        if key[pygame.K_SPACE] and not bullet.get_control():
            bullet.set_control(True)
            bullet.reset(player.rect.centerx , player.rect.centery - 5)
            player_shoot.play()
            
        if key[pygame.K_LEFT]:
            player.go_left()
            if not bullet.get_control():
                bullet.go_left()
                
        if key[pygame.K_RIGHT]:
            player.go_right()
            if not bullet.get_control():
                bullet.go_right()
        
        if key[pygame.K_ESCAPE]:
            return False, score.get_score(), life.get_life()

        # test 
        if key[pygame.K_z]:
            test = pySprites.Bullet(player.rect.centerx, player.rect.centery, - 15 , True)
            test.set_control(True)
            test_bullet.add(test)
            allSprites.add(test_bullet)
                
        for op in invaders:
            if random.randrange(1500) == 9:
                bullet1 = pySprites.Bullet(op.rect.centerx, op.rect.centery, 15, False)
                bullet1.set_control(True)
                enemyBullets.add(bullet1)
                allSprites.add(enemyBullets)
                alien_shoot.play()
 
        # enemy bullet to player collition
        playerHit = pygame.sprite.spritecollide(player, enemyBullets, False)
        if playerHit:
            for x in playerHit:
                player_death.play()
                bullet.force_set((640, -10))
                bullet.set_control(True)
                player.set_value(True)
                x.kill()
            life.set_life()
            bullet.set_control(False)

        if life.get_life() <= 0 and not player.get_value():
            return True ,score.get_score(), life.get_life()        
    
        # player bullet to invader collition
        invaderHit = pygame.sprite.spritecollide(bullet, invaders, False)
        if invaderHit:
            for x in invaderHit:
                invader_death.play()
                bullet.reset(player.rect.centerx , player.rect.centery - 5)
                bullet.set_control(False)
                point = x.get_point()
                score.set_score(point)
                x.kill()
    
        #test
        for a in test_bullet:
            for b in invaders:
                if a.rect.colliderect(b.rect):
                    a.kill()
                    b.kill()
            
        # barrier to invader collition        
        for barrier in barriers:
            for invader in invaders:
                if barrier.rect.colliderect(invader.rect):
                    barrier.kill()
                
        # enemy bullet to barrier collition
        for enemybullet in enemyBullets:
            for barrier in barriers:
                if enemybullet.rect.colliderect(barrier.rect):
                    enemybullet.kill()
                    barrier.kill()
        
        # invader to player collition
        for invade in invaders:
            if player.rect.colliderect(invade.rect):
                life.instance_lose()
                return True, score.get_score(), life.get_life()
                    
        # player bullet to barrier collition
        for barrier in barriers:
            if bullet.rect.colliderect(barrier.rect):
                barrier.kill()
                bullet.reset(player.rect.centerx , player.rect.centery - 5)
                bullet.set_control(False)
            
        if bullet.rect.colliderect(zone.rect):
            bullet.set_control(False)
            bullet.reset(player.rect.centerx, player.rect.centery -5)
            
        # makes the second wave of invaders
        if len(invaders) == 0 and not boss_active and not level_2 and not level_3:
            invadersList = []
            y = 290
            for row in range(6):
                for column in range(13):
                    image = image_num2[row]
                    invadersList.append(pySprites.Invader(((column + 1)*37), y, screen.get_width()-(((11) - column)*37) , (column*37), (row+1)*10 , 6,8, image))
                y -= 30 
            invaders.add(invadersList)
            allSprites.add(invaders)
            level_2 = True
        
        # makes the thrid wave of invadeders
        if len(invaders) == 0 and not boss_active and level_2 and not level_3:
            invadersList = []
            y = 300
            for row in range(7):
                for column in range(15):
                    image = image_num3[row]
                    invadersList.append(pySprites.Invader(((column + 1)*37), y, screen.get_width()-(((13) - column)*37) , (column*37), (row+1)*10 , 7,9, image))
                y -= 30 
            invaders.add(invadersList)
            allSprites.add(invaders)
            level_3 = True        
        
        # makes the boss 
        if len(invaders) == 0 and not boss_active and level_2 and level_3:
            boss = pySprites.Invader(screen.get_width() /2, 180, screen.get_width(), 0, 500, 8,13, 10)
            allSprites.add(boss, boss_health)
            boss_active = True
            
        if boss_active and len(invaders) == 0:
            # makes the boss shoot 
            if random.randrange(30) == 9:
                bullet1 = pySprites.Bullet(boss.rect.centerx, boss.rect.centery, 15, False)
                bullet1.set_control(True)
                bullet2 = pySprites.Bullet(boss.rect.left, boss.rect.centery, 15, False)
                bullet2.set_control(True)
                bullet3 = pySprites.Bullet(boss.rect.right, boss.rect.centery, 15, False)
                bullet3.set_control(True)
                enemyBullets.add(bullet1, bullet2, bullet3)
                allSprites.add(enemyBullets)
        
            # boss collition
            if boss.rect.colliderect(bullet.rect):
                bullet.reset(player.rect.centerx, player.rect.centery -5)
                bullet.set_control(False)
                boss_health.resize()
                boss_health.set_health()
            
            # checks boss health
            if boss_health.get_health() < 0:
                invader_death.play()
                points = boss.get_point()
                score.set_score(points)
                boss.kill()
                boss_active = False
                
            if len(invaders) == 0 and not boss_active and level_2 and level_3:
                return True, score.get_score(), life.get_life()

        # refresh
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)   
        pygame.display.flip()

def game_menu(screen):
    """
    This is the game menu function
    """

    # display
    background = pygame.image.load("./background stuff/start and end wall.png")
    background.convert()
    screen.blit(background, (0, 0))
    
    # entities
    sign = pySprites.Game_menu_sign()
    play_button = pySprites.Game_menu_button((280, 650), (62, 112, 230), (62, 160, 230))
    quit_button = pySprites.Game_menu_button((800, 650), (154, 62, 230), (213, 62, 230))
    
    button_text1 = pySprites.General_text("PLAY", (280, 650), (255, 255,255), 50)
    button_text2 = pySprites.General_text("QUIT", (800, 650), (255, 255 ,255), 50)
    
    instruction_text = pySprites.General_text("MOVE LEFT => [ LEFT ARROW KEY ]" , (540, 390), (255, 255, 255), 35)
    instruction_text2 = pySprites.General_text("MOVE RIGHT => [ RIGHT ARROW KEY ]" , (540, 430), (255, 255, 255), 35)
    instruction_text3 = pySprites.General_text("SHOOT => [ SPACEBAR ]" , (540, 470), (255, 255, 255), 35)
    instruction_text4 = pySprites.General_text("QUIT => [ ESC ]" , (540, 510), (255, 255, 255), 35)
        
    allSprites = pygame.sprite.OrderedUpdates(sign, play_button, quit_button, button_text1, button_text2, instruction_text, instruction_text2,instruction_text3, instruction_text4)
    
    keepGoing = True 
    clock = pygame.time.Clock()

    # loop
    while keepGoing:
        # time
        clock.tick(30)    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_RETURN:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
            elif event.type == pygame.MOUSEBUTTONUP:
                if play_button.rect.collidepoint(pygame.mouse.get_pos()):
                    return True
                if quit_button.rect.collidepoint(pygame.mouse.get_pos()):
                    return False              

        # check rect between mouse and buttons
        if play_button.rect.collidepoint(pygame.mouse.get_pos()):
            play_button.set_value(True)
        else:
            play_button.set_value(False)
        
        if quit_button.rect.collidepoint(pygame.mouse.get_pos()):
            quit_button.set_value(True)
        else:
            quit_button.set_value(False)        
        
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)   
        pygame.display.flip()  

def end_screen(screen, score, life):
    """
    This is the end menu function 
    """
    # display
    background = pygame.image.load("./background stuff/start and end wall.png")
    background.convert()
    screen.blit(background, (0, 0)) 
    
    # entities
    if life <= 0:
        text = pySprites.General_text("YOU LOSE", (540, 150), (255,255,255), 150)
    else:
        text = pySprites.General_text("YOU WIN!", (540, 150), (255,255,255), 150) 
    
    score_text = pySprites.General_text("SCORE = %d"%score, (540, 390), (255,255,255), 100)
    replay_button = pySprites.Game_menu_button((280, 650), (62, 112, 230), (62, 160, 230))
    quit_button = pySprites.Game_menu_button((800, 650), (154, 62, 230), (213, 62, 230))
    button_text1 = pySprites.General_text("REPLAY", (280, 650), (255, 255,255), 45)
    button_text2 = pySprites.General_text("QUIT", (800, 650), (255, 255 ,255), 50)
    allSprites = pygame.sprite.OrderedUpdates(replay_button, quit_button, text, button_text1, button_text2, score_text)
    
    keepGoing = True 
    clock = pygame.time.Clock()

    # loop
    while keepGoing:
        # time
        clock.tick(30)    
        
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONUP:
                if replay_button.rect.collidepoint(pygame.mouse.get_pos()):
                    return True
                if quit_button.rect.collidepoint(pygame.mouse.get_pos()):
                    return False
                
        if key[pygame.K_RETURN]:
            return True
        
        # checks rect between mouse and buttons
        if quit_button.rect.collidepoint(pygame.mouse.get_pos()):
            quit_button.set_value(True)
        else:
            quit_button.set_value(False)
        
        if replay_button.rect.collidepoint(pygame.mouse.get_pos()):
            replay_button.set_value(True)
        else:
            replay_button.set_value(False)
        
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)   
        pygame.display.flip() 
                              
def main(): 
    #display
    screen = pygame.display.set_mode((1080, 750))
    pygame.display.set_caption("SPACE INVADERS")
    
    # entities 
    skip = False
    level = False
    
    pygame.mixer.music.load("./sounds/Warsongs - The Glory (James Egbert Remix).mp3")
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)
    
    keepGoing = True
    # loop
    while keepGoing:
        if not skip and keepGoing:
            keepGoing = game_menu(screen)
        if keepGoing:
            keepGoing, score, life = game(screen)
            level = True
        if keepGoing and  level:
            keepGoing = end_screen(screen, score, life)
            skip = True
            
    if not keepGoing:
        pygame.mixer.music.fadeout(750)
    
    pygame.time.delay(1000)
    pygame.quit()
    
main()