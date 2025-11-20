from classes import *

pygame.init()
screen = pygame.display.set_mode((1600, 1200))
pygame.display.set_caption("The Siege of Walmartville")
pygame.display.set_icon(pygame.image.load("Resources/Temporary.png"))

background = pygame.image.load("Resources\\background.jpg")

waypoints = [(620,325),(620,150),(885,150),(885,610),(375,610),(375,895),(955,895),(955,1190)]


lives = 20
wave = 1
running = True
while running:
    if enemies.sprites() == [] and wave <= 11:
        done = False
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
    if wave <= 5 and not done:
        to_spawn = wave*5
        for i in range(to_spawn):
            enemies.add(Enemy((0,325),100,1,1))
        done = True
        wave += 1
    elif wave > 5 and wave < 11 and not done:
        to_spawn = (wave-5) * 5
        for i in range(to_spawn):
            enemies.add(Enemy((0,325),300,2,1))
        done = True
        wave += 1
    elif not done:
        enemies.add(Enemy((0,325),5000,1,1))
        done = True
        wave += 1

    for i in enemies:
        i.update(waypoints[i.next_waypoint_idx])
        if i.at_waypoint(waypoints[i.next_waypoint_idx]):
            if i.next_waypoint_idx > len(waypoints) - 1:
                i.kill()
                lives -= 1
    enemies.draw(screen)
    screen.blit(pygame.image.load("Resources\\sign.png"),(880,1075))
    pygame.display.flip()