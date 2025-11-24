from classes import *

pygame.init()
screen = pygame.display.set_mode((1600, 1200))
pygame.display.set_caption("The Siege of Walmartville")
pygame.display.set_icon(pygame.image.load("Resources/Temporary.png"))

background = pygame.image.load("Resources\\background.jpg")

selectedtext = pygame.font.Font("Resources\\Times New Roman Regular.ttf",14)
wavetext = pygame.font.Font("Resources\\Times New Roman Regular.ttf",64)
waypoints = [(620,325),(620,150),(885,150),(885,610),(375,610),(375,895),(955,895),(955,1190)]

beellista_icon = Button((1267,365),"Resources/Temporary.png",1)
beehive_icon = Button((1387,365),"Resources/Temporary.png",1)
honeycannon_icon = Button((1507,365),"Resources/Temporary.png",1)


selected = ""
lives = 20
wave = 0
honey_supply = 0
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    if enemies.sprites() == [] and wave <= 11:
        done = False
        wave += 1
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_pos[0] < 1200:
            if not selected:
                pass
            elif selected == "Beellista":
                towers.add(Beellista((mouse_pos[0]-32,mouse_pos[1]-32),1,2,500))
            elif selected == "Beehive":
                towers.add(Beehive((mouse_pos[0]-32,mouse_pos[1]-32),1,0.5,500))
            elif selected == "Honeycannon":
                towers.add(Honeycannon((mouse_pos[0]-32,mouse_pos[1]-32),1,2,500))
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
    
    #Ensures that the button wasn't pressed too recently.
    if time.time() - beellista_icon.start_time > 0.25:
        if beellista_icon.draw(screen): 
            if selected == "Beellista":
                selected = ""
            else:
                selected = "Beellista"
    if time.time() - beehive_icon.start_time > 0.25:
        if beehive_icon.draw(screen): 
            if selected == "Beehive":
                selected = ""
            else:
                selected = "Beehive"
    if time.time() - honeycannon_icon.start_time > 0.25:
        if honeycannon_icon.draw(screen): 
            if selected == "Honeycannon":
                selected = ""
            else:
                selected = "Honeycannon"
    wave_display = wavetext.render(f"Wave: {wave}",True,(255,255,255))
    selected_display = selectedtext.render(selected,True,(0,0,0))
    enemies.draw(screen)
    towers.draw(screen)
    projectiles.draw(screen)
    screen.blit(pygame.image.load("Resources\\sign.png"),(880,1075))
    screen.blit(wave_display, (1300,1100))
    screen.blit(beellista_icon.img, (beellista_icon.x, beellista_icon.y))
    screen.blit(beehive_icon.img, (beehive_icon.x, beehive_icon.y))
    screen.blit(honeycannon_icon.img, (honeycannon_icon.x, honeycannon_icon.y))
    screen.blit(selected_display,(mouse_pos[0]+10,mouse_pos[1]-5))
    pygame.display.flip()