# -*- coding: utf-8 -*-
import math
import random
import os
import time
import pygame
from pygame import mixer
import sys

current_path = os.path.dirname(__file__) # Where .py file is located

#scoreboard
scoreboard = []
attempts = 1

while True:
  # Initialize the pygame
  pygame.init()

  clock = pygame.time.Clock()
  fps = 60

  # create the screen
  screen = pygame.display.set_mode((800, 600))

  # Background
  background = pygame.image.load(os.path.join(current_path, 'lab.png'))
  background = pygame.transform.scale(background,(800,600))  
  background2 = pygame.image.load(os.path.join(current_path, 'hospital.jpg'))
  background2 = pygame.transform.scale(background2,(800,600)) 
  background3 = pygame.image.load(os.path.join(current_path, 'garden.jpg'))
  background3 = pygame.transform.scale(background3,(800,600)) 

  # Player (設定chen的初始化位置)(陳時中目前可以左右動))
  playerImg = pygame.transform.scale(pygame.image.load(os.path.join(current_path, 'chen.png')),(150,180))
  playerX = 300  
  playerY = 435  
  playerX_change = 0
  playerY_change = 0

  # 設定Bats
  enemyImg = []
  enemyX = []
  enemyY = []
  enemyX_change = []
  enemyY_change = []
  num_of_enemies = 6
  for i in range(num_of_enemies):
    enemyImg.append(pygame.transform.scale(pygame.image.load(os.path.join(current_path, 'bat.png')),(200,150)))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(-300, 100))
    left_right = random.randint(1, 2)
    if left_right == 2:
      enemyX_change.append(4)
    else:
      enemyX_change.append(-4)
    enemyY_change.append(100)
  def bat_reset():
        global enemyImg
        global enemyX
        global enemyY
        global enemyX_change
        global enemyY_change
        global num_of_enemies
        enemyImg = []
        enemyX = []
        enemyY = []
        enemyX_change = []
        enemyY_change = []
        num_of_enemies = 6
        for i in range(num_of_enemies):
          enemyImg.append(pygame.transform.scale(pygame.image.load(os.path.join(current_path, 'bat.png')),(200,150)))
          enemyX.append(random.randint(0, 736))     #(0, 736)
          enemyY.append(random.randint(-50, 90))
          left_right = random.randint(1, 2)
          if left_right == 2:
            enemyX_change.append(4)
          else:
            enemyX_change.append(-4)
          enemyY_change.append(100)
      
  #mini_virus(第二關蝙蝠吐出病毒)
  def mini_virus_reset():
      global mini_virusImg
      global mini_virusX
      global mini_virusY
      global mini_virusX_change
      global mini_virusY_change
      mini_virusImg = []
      mini_virusX = []
      mini_virusY = []
      mini_virusX_change = []
      mini_virusY_change = []
  mini_virus_reset()
  def mini_virus_for_bats():
      global mini_virusImg
      global mini_virusX
      global mini_virusY
      global mini_virusX_change
      global mini_virusY_change
      for i in range(num_of_enemies):
          mini_virusImg.append(pygame.transform.scale(pygame.image.load(os.path.join(current_path, 'virus.png')),(100,100)))
          mini_virusX.append(0)   
          mini_virusY.append(2000)
          mini_virusX_change.append(0)
          mini_virusY_change.append(4)
  mini_virus_for_bats()

  #Virus(第三關敵人)
  num_of_viruses = 0
  def virus_reset():
    global virusImg
    global virusX
    global virusY
    global virusX_change
    global virusY_change
    virusImg = []
    virusX = []
    virusY = []
    virusX_change = []
    virusY_change = []  
    for i in range(num_of_viruses):
          virusImg.append(pygame.transform.scale(pygame.image.load(os.path.join(current_path, 'virus.png')),(175,175)))
          virusX.append(random.randint(0, 736))  
          virusY.append(random.randint(-150, 50))
          virusX_change.append(random.randint(-8, 8))
          virusY_change.append(random.randint(4, 8))

  #Virus Boss
  virus_bossImg = pygame.transform.scale(pygame.image.load(os.path.join(current_path, 'virus.png')),(600,600))
  virus_bossX = 280
  virus_bossY = 600


  #Final Boss
  final_bossImg = pygame.transform.scale(pygame.image.load(os.path.join(current_path, 'winnie.png')),(200,200))
  final_bossX = 0
  final_bossY = 0
  final_bossX_change = 0
  final_bossY_change = 0

  # Bullet口罩
  # Ready - You can't see the bullet on the screen
  # Fire - The bullet is currently moving
  bulletImg = pygame.transform.scale(pygame.image.load(os.path.join(current_path, 'mask.png')),(100,87))
  bulletX = 300
  bulletY = 500
  bulletX_change = 0
  bulletY_change = 30
  bullet_state = "ready"

  #Bullet2 藥丸
  bullet2Img = pygame.transform.scale(pygame.image.load(os.path.join(current_path, 'pill.png')),(60,50))
  bullet2X = 300
  bullet2Y = 500
  bullet2X_change = 0
  bullet2Y_change = 30
  bullet2_state = "ready"

  # Score
  score_value = 0
  font = pygame.font.Font(os.path.join(current_path,'GROBOLD.ttf'), 32)
  textX = 10
  testY = 10

  # Lives 
  life_count = 3
  textlX = 10
  testlY = 42


  # level顯示
  level_font = pygame.font.Font(os.path.join(current_path,'Night Shift - Demo.ttf'), 48)
  level_start_font = pygame.font.Font(os.path.join(current_path,'Night Shift - Demo.ttf'), 80)
  display_level = True
  level_ticks = 0
  def next_level():
    global level
    level += 1
    global level_ticks
    level_ticks = 0
    global display_level
    display_level = True
    global life_count
    life_count += 1

  #final boss movement
  timer_ticks = 0

  # Game Over
  over_font = pygame.font.Font(os.path.join(current_path,'The Poster King.ttf'), 90)

  scoreboard_font = pygame.font.Font(os.path.join(current_path,'GROBOLD.ttf'), 40)

  credits_font = pygame.font.Font(os.path.join(current_path,'GenJyuuGothic-Monospace-Bold.ttf'), 36)

  def show_score(x, y):
      score = font.render("Score : " + str(score_value), True, (255, 255, 255))
      screen.blit(score, (x, y))

  def show_lives(x, y):
      score = font.render("Lives : " + str(life_count), True, (255, 255, 255))
      screen.blit(score, (x, y))

  def show_scoreboard(item,x,y):
      score = scoreboard_font.render(item, True, (255, 255, 255))
      screen.blit(score, (x, y))

  def credits(name,x,y):
      line = credits_font.render(name, True, (255, 255, 255))
      screen.blit(line, (x, y))

  #設定關卡字樣
  def level_text(n):
    level_text = level_font.render("Level"+str(n),True, (255, 255, 255))
    screen.blit(level_text, (660, 20))

  def level_start(n):
    level_text = level_start_font.render("Level"+str(n),True, (255, 255, 255))
    screen.blit(level_text, (250, 250))

  def game_over_text():
      over_text = over_font.render("GAME OVER", True, (255, 255, 255))
      screen.blit(over_text, (200, 288))
      level_ticks = 0

  def game_win_text():
      over_text = over_font.render("YOU WIN", True, (0, 255, 255))
      screen.blit(over_text, (300, 250))

  def player(x, y):
      screen.blit(playerImg, (x, y))

  def enemy(x, y, i):
      screen.blit(enemyImg[i], (x, y))

  def mini_virus(x, y, i):
      screen.blit(mini_virusImg[i], (x, y))

  def virus(x, y, i):
      screen.blit(virusImg[i], (x, y))

  def virus_boss(x, y):
      screen.blit(virus_bossImg, (x, y))

  def final_boss(x, y):
      screen.blit(final_bossImg, (x, y))


  def fire_bullet(x, y):
      global bullet_state
      bullet_state = "fire"
      screen.blit(bulletImg, (x + 16, y + 10))

  #第二關攻擊武器
  def fire_bullet2(x, y):
      global bullet2_state
      bullet2_state = "fire"
      screen.blit(bullet2Img, (x + 16, y + 10))


  #子彈打到敵軍
  def isCollision(enemyX, enemyY, bulletX, bulletY):
      distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
      if distance < 60:
          return True
      else:
          return False

  def gameover():
    global level_ticks
    level_ticks = 0
    global scoreboard
    scoreboard.append('attempt '+str(attempts)+' : '+str(score_value))
    global running
    running = False
    global playerX_change
    playerX_change = 0
    global playerY_change
    playerY_change = 0

  def winnielaugh():
    screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(current_path, 'winnie.png')),(888,888)), (0, -88))
    final_score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(final_score, (330, 400))

  #蝙蝠發射病毒

  #chooses level
  level = 1

  #checks if boss fight is happening
  in_boss_fight = False


  # Game Loop
  running = True
  while running:
      # RGB = Red, Green, Blue
      screen.fill((0, 0, 0))
      
      # Background Image
      if level == 3 or level == 4 :
        screen.blit(background2, (0, 0))
      elif level == 5:
        screen.blit(background3, (0, 0))
      else:
        screen.blit(background, (0, 0))
      # Show Chen
      player(playerX, playerY)
      for event in pygame.event.get():
          # if keystroke is pressed check whether its right or left
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_SPACE:
                if level == 1:
                  if bullet_state == "ready":
                      # Get the current x cordinate of Chen
                      bulletX = playerX
                      bulletY = playerY
                      fire_bullet(bulletX, bulletY)
                elif level == 2 or level == 3 or level == 4 or level == 5:
                  if bullet2_state == "ready":
                      # Get the current x-coordinate of Chen
                      bullet2X = playerX
                      bullet2Y = playerY
                      fire_bullet2(bullet2X, bullet2Y)
          
          keys = pygame.key.get_pressed()
          if keys[pygame.K_LEFT] == True and keys[pygame.K_RIGHT] == False:
            playerX_change = -5
          elif keys[pygame.K_LEFT] == False and keys[pygame.K_RIGHT] == True:
            playerX_change = 5
          else:
            playerX_change = 0

          if keys[pygame.K_UP] == True and keys[pygame.K_DOWN] == False:
            playerY_change = -5
          elif keys[pygame.K_UP] == False and keys[pygame.K_DOWN] == True:
            playerY_change = 5
          else:
            playerY_change = 0
        
          #backdoor
          if keys[pygame.K_q] and keys[pygame.K_w] and keys[pygame.K_e] and level == 1: # 276
            score_value = 10
          if keys[pygame.K_w] and keys[pygame.K_e] and keys[pygame.K_r] and level == 2: # 276
            score_value = 30
          if keys[pygame.K_t] and keys[pygame.K_e] and keys[pygame.K_r] and level == 3 and in_boss_fight == False: # 276
            score_value = 50
          if keys[pygame.K_t] and keys[pygame.K_y] and keys[pygame.K_r] and level == 3 and in_boss_fight == True: # 276
            score_value = 80
          if keys[pygame.K_t] and keys[pygame.K_y] and keys[pygame.K_u] and level == 4: # 276
            score_value = 110
          if keys[pygame.K_i] and keys[pygame.K_y] and keys[pygame.K_u] and level == 5: # 276
            score_value = 150

      playerX += playerX_change
      if playerX <= -20:
          playerX = -20
      elif playerX >= 686:
          playerX = 686
      if playerY <= -80:
          playerY = -80
      elif playerY >= 435:
          playerY = 435
      playerY += playerY_change

      # Enemy Movement (level 1,2)
      if level == 1 or level == 2 or level == 4:
        for i in range(num_of_enemies):
          # Game Over
          #碰到蝙蝠死亡
          death = isCollision(enemyX[i], enemyY[i], playerX, playerY)
          #碰到病毒死亡
          death2 = isCollision(mini_virusX[i], mini_virusY[i], playerX, playerY+18)
          if death or death2:  #若death，則命-1
            life_count -= 1
            if life_count == 0:
              gameover()
            (playerX,playerY) = (300,435)
            enemyY[i] = 0
            if level != 1:
              mini_virusY[i] = enemyY[i]+50
              mini_virusX[i] = enemyX[i]

          if level==1 or level ==2 or level ==4:
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
              enemyX_change[i] = 4
              enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
              enemyX_change[i] = -4
              enemyY[i] += enemyY_change[i]
            if enemyY[i] >= 488:
              enemyY[i] = -enemyY_change[i]
          #發射小病毒
          if level == 2 or level ==4:
            mini_virusY[i] += mini_virusY_change[i]
            mini_virusX[i] == (mini_virusX[i]+playerX)//2
            if mini_virusY[i] >= 540 and enemyY[i] >= 0 and random.randint(1, 8)==8:
              mini_virusX[i] = enemyX[i]
              mini_virusY[i] = enemyY[i]+50

         
          # Collision
          #蝙蝠被口罩打到
          collision = isCollision(enemyX[i], enemyY[i], bulletX-100, bulletY)
          #蝙蝠被藥丸打到
          collision2 = isCollision(enemyX[i], enemyY[i], bullet2X-100, bullet2Y)
          #-100 so that masks hit bats in the center
          if collision or collision2:

              score_value += 1
              enemyX[i] = random.randint(0, 736)
              enemyY[i] = random.randint(-150, -50)
              if collision:
                bulletY = 480
                bullet_state = "ready"
              if collision2:
                bullet2Y = 480
                bullet2_state = "ready"       
          if level == 1 or level == 2 or level ==4:
            enemy(enemyX[i], enemyY[i], i)
            mini_virus(mini_virusX[i], mini_virusY[i], i)

      #level 3 enemies
      if in_boss_fight == False:
        for i in range(num_of_viruses):
          collision_virus = isCollision(virusX[i], virusY[i], bullet2X-100, bullet2Y)
          if collision_virus:

              score_value += 1
              virusX[i] = random.randint(0, 736)
              virusY[i] = random.randint(-150, -50)
              if collision_virus:
                bullet2Y = 480
                bullet2_state = "ready"  
          death_virus = isCollision(virusX[i], virusY[i], playerX-20, playerY-10)
          death_virus_2 = isCollision(virusX[i], virusY[i], playerX, playerY+10)
          if death_virus or death_virus_2:  #若death，則命-1
            life_count -= 1
            virusY[i] = 0
            if life_count == 0:
              gameover()
            (playerX,playerY) = (300,435) 
            virusY[i] = 0
          if level==3 or level ==4:
            virusX[i] += virusX_change[i]
            virusY[i] += virusY_change[i]
            if virusX[i] <= -20:
              virusX_change[i] = 4
            elif virusX[i] >= 736:
              virusX_change[i] = -4
            if virusY[i] <= 0:
              virusY_change[i] = 2
            elif virusY[i] >= 480:
              virusY[i] = 0
            virus(virusX[i],virusY[i],i)

      #level 3 boss fight
      if level == 3 and in_boss_fight == True:
        if (math.sqrt(math.pow(virus_bossX+270 - bullet2X, 2) + (math.pow(virus_bossY+240 - bullet2Y, 2))))< 120:
              score_value += 1
              bullet2Y = 480
              bullet2_state = "ready"  
        if (math.sqrt(math.pow(virus_bossX+270 - playerX, 2) + (math.pow(virus_bossY+240 - playerY, 2))))< 120:
              life_count -= 1
              if life_count == 0:
                gameover()
              playerY = playerY+100
        for i in range(num_of_enemies):
          #移動迷你病毒
          mini_virusX[i] += mini_virusX_change[i]
          mini_virusY[i] += mini_virusY_change[i]
          if mini_virusX[i] <= -50:
              mini_virusX_change[i] = random.randint(0, 11)
              mini_virusY_change[i] = 4
          elif mini_virusX[i] >= 736:
              mini_virusX_change[i] = random.randint(-11, 0)
              mini_virusY_change[i] = 4
          if mini_virusY[i] >= 540:
              mini_virusX_change[i] = random.randint(-10, 10)
              mini_virusY_change[i] = 0
              mini_virusX[i] = virus_bossX+170
              mini_virusY[i] = virus_bossY+240
          mini_virus(mini_virusX[i], mini_virusY[i], i)
        virus_boss(virus_bossX, virus_bossY)
        #小病毒命中陳時中
        for i in range(num_of_enemies):
          death2 = isCollision(mini_virusX[i], mini_virusY[i], playerX, playerY+18)
          if death2:  #若death，則命-1
            life_count -= 1
            if life_count == 0:
              gameover()
            mini_virusX[i] = virus_bossX+130
            mini_virusY[i] = virus_bossY+240

      #level 5 final boss
      if level == 5 and in_boss_fight == True:
        #子彈打中魔王
        timer_ticks += 1
        if (math.sqrt(math.pow(final_bossX+50 - bullet2X, 2) + (math.pow(final_bossY - bullet2Y, 2))))< 120:
              score_value += 1
              bullet2Y = 480
              bullet2_state = "ready"
              final_bossX_change = random.randint(-8,8)
              boss_move_time = random.randint(28,88)
              timer_ticks = 0
        if final_bossX > 600 or final_bossX < 0:
          final_bossX_change = -final_bossX_change
        if timer_ticks > boss_move_time:
          final_bossX_change = 0
        final_bossX += final_bossX_change
        #mini_viruses
        for i in range(num_of_enemies):
          mini_virusX[i] += mini_virusX_change[i]
          mini_virusY[i] += mini_virusY_change[i]
          if mini_virusY[i] >= 540:
              mini_virusX_change[i] = random.randint(-8,8)
              mini_virusY_change[i] = 4
              mini_virusX[i] = final_bossX+66
              mini_virusY[i] = final_bossY+100
          mini_virus(mini_virusX[i], mini_virusY[i], i)
        #小病毒命中陳時中
          death2 = isCollision(mini_virusX[i], mini_virusY[i], playerX, playerY+18)
          if death2:  #若death，則命-1
            life_count -= 1
            if life_count == 0:
              gameover()
            mini_virusX[i] = final_bossX+100
            mini_virusY[i] = final_bossY+100
        #畫boss
        final_boss(final_bossX, final_bossY)

      # Bullet Movement
      if bulletY <= -88:
          bulletY = 480
          bullet_state = "ready"

      if bullet_state == "fire":
          fire_bullet(bulletX, bulletY)
          bulletY -= bulletY_change

      # Bullet 2 Movement
      if bullet2Y <= -88:
          bullet2Y = 480
          bullet2_state = "ready"

      if bullet2_state == "fire":
          fire_bullet2(bullet2X, bullet2Y)
          bullet2Y -= bullet2Y_change
      #####show HUD
      show_score(textX, testY)
      show_lives(textlX, testlY)
      #顯示現在是第幾關
      if display_level == True:
        level_start(level)
      else:
        level_text(level)
      if level_ticks > 135 and display_level == True:
        display_level = False
      pygame.display.update()
      level_ticks += 1
      clock.tick(fps)
      #levels
      #enter level 2
      if score_value == 10 and level == 1:
        next_level()
        bat_reset()

      #enter level 3(virus level)
      if score_value == 30 and level == 2:
        next_level()
        for i in range(num_of_enemies):
          mini_virusY[i] = 600
          enemyY[i] = 600
          enemy(enemyX[i], enemyY[i], i)
          mini_virus(mini_virusX[i], mini_virusY[i], i)
        num_of_viruses = 12
        virus_reset()

      #level 3 boss fight
      if score_value == 50 and level == 3 and in_boss_fight == False:
        in_boss_fight = True
        for i in range(num_of_viruses):
          virusY[i] = 600
          virus(virusX[i],virusY[i],i)
        virus_bossX = 100
        virus_bossY = -127
        num_of_enemies = 15
        #activate boss attack
        mini_virus_reset()
        for i in range(num_of_enemies):
          mini_virusImg.append(pygame.transform.scale(pygame.image.load(os.path.join(current_path, 'virus.png')),(100,100)))
          mini_virusX.append(virus_bossX+170)   
          mini_virusY.append(virus_bossY+240)
          mini_virusX_change.append(random.randint(-10, 10))
          mini_virusY_change.append(0)

      #enter level 4
      if score_value == 80 and level == 3:
        next_level()
        in_boss_fight = False
        bat_reset()
        mini_virus_reset()
        mini_virus_for_bats()
        virus_reset()
      
      #enter level 5
      if score_value == 110 and level == 4 and in_boss_fight == False:
          next_level()
          in_boss_fight = True
          #show boss
          final_bossX = 300
          boss_move_time = 100
          #activate boss attack
          num_of_enemies = 18
          mini_virus_reset()
          for i in range(num_of_enemies):
            mini_virusImg.append(pygame.transform.scale(pygame.image.load(os.path.join(current_path, 'virus.png')),(100,100)))
            mini_virusX.append(final_bossX+66)   
            mini_virusY.append(final_bossY+100)
            mini_virusX_change.append(random.randint(-8,8))
            mini_virusY_change.append(random.randint(3,6))
        
      if level == 5 and score_value == 150  :
          break
  while running == False:
        # RGB = Red, Green, Blue
        #background
        screen.fill((0, 0, 0))
        if level == 3 or level == 4 :
          screen.blit(background2, (0, 0))
        elif level == 5:
          screen.blit(background3, (0, 0))
        else:
          screen.blit(background, (0, 0))
        #winnie laughs at your incompetence
        winnielaugh()
        game_over_text()
        Ycoordinate = 0
        for i in scoreboard:
            show_scoreboard(i,0,Ycoordinate)
            Ycoordinate += 50
        countdown = 3-level_ticks//60
        if level_ticks//60>3:
            running == True
            break
        retry = font.render("Restart in ... "+str(countdown), True, (255, 255, 255))
        screen.blit(retry, (320, 438))
        pygame.display.update()
        level_ticks += 1
        clock.tick(fps)
            
  attempts += 1

  if life_count > 0:
    #結束煙火
    # Setup pygame/window 
    mainClock = pygame.time.Clock()
    from pygame.locals import *
    pygame.init()
    pygame.display.set_caption('game base')
    screen = pygame.display.set_mode((1376, 900),0,32)
    TILE_SIZE = 20

    # [loc, velocity, timer]
    particles = []
    tile_map = {}

    clicking = False
    pygame.mouse.set_visible(False)
    # Loop 
    def mouse_simulator():
        if random.random() < .05:
            clicking = True
        else:
            clicking = False
        mx = random.randrange(0, 800)
        my = random.randrange(0, 800)
        return clicking, mx, my

    while True:
        
        # Background 
        screen.fill((0,0,0))
        clicking, mx, my = mouse_simulator()
        # mx, my = pygame.mouse.get_pos()
        # Particles 
        if clicking:
            for i in range(10):
                particles.append([[mx, my], [random.randint(0, 42) / 6 - 3.5, random.randint(0, 42) / 6 - 3.5], random.randint(4, 6)])

        for particle in particles:
            particle[0][0] += particle[1][0]
            loc_str = str(int(particle[0][0] / TILE_SIZE)) + ';' + str(int(particle[0][1] / TILE_SIZE))
            if loc_str in tile_map:
                particle[1][0] = -0.7 * particle[1][0]
                particle[1][1] *= 0.95
                particle[0][0] += particle[1][0] * 2
            particle[0][1] += particle[1][1]
            loc_str = str(int(particle[0][0] / TILE_SIZE)) + ';' + str(int(particle[0][1] / TILE_SIZE))
            if loc_str in tile_map:
                particle[1][1] = -0.7 * particle[1][1]
                particle[1][0] *= 0.95
                particle[0][1] += particle[1][1] * 2
            particle[2] -= 0.035
            particle[1][1] += 0.15
            xc1 = random.randrange(0,255)
            xc2 = random.randrange(0,255)
            xc3 = random.randrange(0,255)
            pygame.draw.circle(screen, (xc1, xc2, xc3), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                particles.remove(particle)
    # Render Tiles 
        for tile in tile_map:
            pygame.draw.rect(screen, tile_map[tile][2], pygame.Rect(tile_map[tile][0] * TILE_SIZE, tile_map[tile][1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    # Update 成員列表
        game_win_text()
        credits('遊戲設計：',0,0)
        credits('台大生傳系 林廣琦',0,38)
        credits('台大生傳系 洪文萱',0,76)
        credits('台大園藝系 劉芷岑',0,114)
        credits('台大財金系 張元彥',0,152)
        pygame.display.update()

