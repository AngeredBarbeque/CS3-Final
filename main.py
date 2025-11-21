from classes import *

pygame.init()
screen = pygame.display.set_mode((1600, 1200))
pygame.display.set_caption("The Siege of Walmartville")
pygame.display.set_icon(pygame.image.load("Resources/Temporary.png"))

background = pygame.image.load("Resources\\background.jpg")

wavetext = pygame.font.Font("Resources\\Times New Roman Regular.ttf",64)
waypoints = [(620,325),(620,150),(885,150),(885,610),(375,610),(375,895),(955,895),(955,1190)]

#                                                                                                                           Finish button stuff!
beelista_icon = Button((0,0),"Resources/Temporary.png",1)

lives = 20
wave = 0
running = True
while running:
    if enemies.sprites() == [] and wave <= 11:
        done = False
        wave += 1
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
    if wave <= 5 and not done:
        to_spawn = wave*5
        for i in range(to_spawn):
            enemies.add(Enemy((0,325),100,1,1,pygame.image.load("Resources\\walmart.png")))
        done = True
    elif wave > 5 and wave < 11 and not done:
        to_spawn = (wave-5) * 5
        for i in range(to_spawn):
            enemies.add(Enemy((0,325),300,2,0.04,pygame.image.load("Resources\\noigelist.png")))
        done = True
    elif not done:
        enemies.add(Enemy((0,325),5000,1,1))
        done = True

    for i in enemies:
        i.update(waypoints[i.next_waypoint_idx])
        if i.at_waypoint(waypoints[i.next_waypoint_idx],2):
            if i.next_waypoint_idx > len(waypoints) - 1:
                i.kill()
                lives -= 1
        if i.health <= 0:
            i.kill()
    beelista_icon.draw(screen)
    wave_display = wavetext.render(f"Wave: {wave}",True,(255,255,255))
    enemies.draw(screen)
    screen.blit(pygame.image.load("Resources\\sign.png"),(880,1075))
    screen.blit(wave_display, (1300,1100))
    pygame.display.flip()