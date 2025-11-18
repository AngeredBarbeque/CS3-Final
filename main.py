from classes import *

pygame.init()
screen = pygame.display.set_mode((1600, 1200))
pygame.display.set_caption("The Siege of Walmartville")
pygame.display.set_icon(pygame.image.load("Resources/Temporary.png"))

background = pygame.image.load("Resources\\background.jpg")

waypoints = [Pos(310,325),Pos(310,290),Pos(360,290)]

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
            enemies.add(Enemy(Pos(0,325),100,0.5,1))
        done = True
        wave += 1
    elif wave > 5 and wave < 11 and not done:
        to_spawn = (wave-5) * 5
        for i in range(to_spawn):
            enemies.add(Enemy(Pos(0,0),300,20,1))
        done = True
        wave += 1
    elif not done:
        enemies.add(Enemy(Pos(0,0),5000,15,1))
        done = True
        wave += 1

    for i in enemies:
        i.update(waypoints[i.next_waypoint_idx])
        if i.at_waypoint(waypoints[i.next_waypoint_idx], 2):
            if i.next_waypoint_idx > len(waypoints) - 1:
                i.kill()
                lives -= 1
    enemies.draw(screen)
    pygame.display.flip()