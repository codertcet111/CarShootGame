import pygame
from pygame.locals import *
import math
import random

pygame.init()
width, height = 640, 480  # window's dimension
screen = pygame.display.set_mode((width, height))
keys = [False, False, False, False]  # all W-A-S-D keys for Car movement
playerpos = [100, 400]
trees = [[10, 0]]
acc = [0, 0]
arrows = []
badtimer = 100
badtimer1 = 0
badguys = [[640, 100]]
healthvalue = 194
pygame.mixer.init()

player = pygame.image.load("resources/images/Car.png")
tree = pygame.image.load("resources/images/Tree.png")
Blood= pygame.image.load("resources/images/Blood.png")
tree1 = tree
grass = pygame.image.load("resources/images/CarGrass.png")
castle = pygame.image.load("resources/images/castle.png")
road = pygame.image.load("resources/images/Road.png")
arrow = pygame.image.load("resources/images/missile11.png")
badguyimg = pygame.image.load("resources/images/badguy2.png")
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")
dhamaka = pygame.image.load("resources/images/dhamaka.png")

hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# keep looping through
running = 1
exitcode = 0
while running:
    badtimer -= 1
    # clear the screen before drawing it again
    screen.fill(0)
    # draw the Grass on the screen at X:100, Y:100
    screen.blit(grass, (0, 0))
    screen.blit(grass, (540, 0))
    # draw road
    screen.blit(road, (100, 0))
    # Set Car position
    screen.blit(player, playerpos)
    # Draw arrows

    for bullet in arrows:
        index = 0
        bullet[1] -= 40
        if bullet[1] <= 0:
            arrows.pop(index)
        index += 1
        screen.blit(arrow, (bullet[0], bullet[1]))

    # Draw badgers

    if badtimer == 0:
        badguys.append([random.randint(100, 480), 0])
        #badguys.append([random.randint(100, 480), 0])
        # add tree
        trees.append([random.randint(0, 20), 0])

        badtimer = 100 - (badtimer1 * 2)  # this is to increase rate of evils
        if badtimer1 >= 40:
            badtimer1 = 40
            #badguys.append([random.randint(100, 480), 0])
        else:
            badtimer1 += 20

    index = 0
    playerrect = pygame.Rect(player.get_rect())
    for badguy in badguys:
        if badguy[1] >= 480:
            badguys.pop(index)
        badguy[1] += 5
        # Attack-------------------------------#
        badrect = pygame.Rect(badguyimg.get_rect())
        badrect.top = badguy[1]
        badrect.left = badguy[0]
        if pygame.Rect(badrect.left,badrect.top,29,64).colliderect(playerpos[0],playerpos[1],50,100) == True:
            hit.play()
            healthvalue -= random.randint(5, 15)
            badguys.pop(index)
            screen.blit(Blood, (playerpos[0], playerpos[1]))
        # Check for collisions----------------------------------------------------------------
        index1 = 0
        for bullet in arrows:
            bullrect = pygame.Rect(arrow.get_rect())
            bullrect.left = bullet[0]
            bullrect.top = bullet[1]
            if badrect.colliderect(bullrect):
                enemy.play()
                acc[0] += 1
                badguys.pop(index)
                arrows.pop(index1)
                screen.blit(dhamaka, (bullet[0], bullet[1]))
            index1 += 1
        # Next bad guy
        index += 1
    for badguy in badguys:
        screen.blit(badguyimg, badguy)

    indexTree = 0
    index = 0
    # add trees
    for tree2 in trees:
        screen.blit(tree, (tree2[0], tree2[1]))
        screen.blit(tree, (tree2[0]+540, tree2[1]))
        if tree2[1] >= 480:
            trees.pop(indexTree)
    for tree2 in trees:
        tree2[1] += 7
    # Draw clock
    font = pygame.font.Font(None, 24)
    survivedtext = font.render(
        str((90000 - pygame.time.get_ticks()) / 60000) + ":" + str((90000 - pygame.time.get_ticks()) / 1000 % 60).zfill(
            2), True, (0, 0, 0))
    textRect = survivedtext.get_rect()
    textRect.topright = [635, 5]
    screen.blit(survivedtext, textRect)
    #  Draw health bar
    screen.blit(healthbar, (5, 5))
    for health1 in range(healthvalue):
        screen.blit(health, (health1 + 8, 8))
    # update the screen
    pygame.display.flip()
    # loop through the events
    for event in pygame.event.get():
        # check if the event is the X button
        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_a:
                keys[1] = False
            elif event.key == pygame.K_s:
                keys[2] = False
            elif event.key == pygame.K_d:
                keys[3] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot.play()
            acc[1] += 1
            arrows.append([playerpos[0] + 20, playerpos[1] + 32])
    # Move player
    if keys[0] and playerpos[1] >= 5:
        playerpos[1] -= 10
    elif keys[2] and playerpos[1] <= 400:
        playerpos[1] += 10
    if keys[1] and playerpos[0] >= 100:
        playerpos[0] -= 10
    elif keys[3] and playerpos[0] <= 490:
        playerpos[0] += 10

    # Win/Lose check
    if pygame.time.get_ticks() >= 90000:
        running = 0
        exitcode = 1
    if healthvalue <= 0:
        running = 0
        exitcode = 0
    if acc[1] != 0:
        accuracy = acc[0] * 0.99 / acc[1] * 100
    else:
        accuracy = 0
# Win/lose display
if exitcode == 0:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: "+str(accuracy)+"%", True, (255,0,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(gameover, (0,0))
    screen.blit(text, textRect)
else:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: "+str(accuracy)+"%", True, (0,255,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(youwin, (0,0))
    screen.blit(text, textRect)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
