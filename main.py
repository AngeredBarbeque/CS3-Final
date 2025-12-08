from classes import *

pygame.init()
screen = pygame.display.set_mode((1600, 1200))
pygame.display.set_caption("The Siege of Walmartville")
pygame.display.set_icon(pygame.image.load("Resources//Honey.png"))

background = pygame.image.load("Resources\\background.jpg")

selectedtext = pygame.font.Font("Resources\\Times New Roman Regular.ttf",14)
wavetext = pygame.font.Font("Resources\\Times New Roman Regular.ttf",64)
honeytext = pygame.font.Font("Resources\\Times New Roman Regular.ttf",64)
flavortext = pygame.font.Font("Resources\\Times New Roman Regular.ttf",20)

waypoints = [(620,325),(620,150),(885,150),(885,610),(375,610),(375,895),(955,895),(955,1190)]

beellista_icon = Button((1267,365),"Resources/Beellista.png",1)
beehive_icon = Button((1387,365),"Resources//Hive.png",1)
honeycannon_icon = Button((1507,365),"Resources/Honeycannon.png",1)


#Defines collision rectangles for the track segments
track_1 = pygame.Rect(0,285,740,130)
track_2 = pygame.Rect(565,105,160,215)
track_3 = pygame.Rect(580,105,400,140)
track_4 = pygame.Rect(860,105,120,605)
track_5 = pygame.Rect(350,575,630,130)
track_6 = pygame.Rect(350,575,110,420)
track_7 = pygame.Rect(350,860,710,115)
track_8 = pygame.Rect(930,860,110,340)

#Creates a list of said collision rectangles
track_collision = [track_1,track_2,track_3,track_4,track_5,track_6,track_7,track_8]

beellista_cost = 3
honeycannon_cost = 2
beehive_cost = 1
to_spawn = 0
last_spawn = 0
flavor_text = ""
selected = ""
lives = 20
wave = 0
honey_supply = 10
running = True
while running:
    flavor_text = ""
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
            else:
                on_track = False
                for i in track_collision:
                    if pygame.Rect.collidepoint(i,mouse_pos[0],mouse_pos[1]):
                        on_track = True
                    else:
                        for i in towers:
                            if pygame.Rect.collidepoint(i.rect,mouse_pos[0],mouse_pos[1]):
                                on_track = True
                if selected == "Beellista" and not on_track and honey_supply >= beellista_cost:
                    towers.add(Beellista((mouse_pos[0]-32,mouse_pos[1]-32),2,2,600))
                    honey_supply -= beellista_cost
                elif selected == "Beehive" and not on_track and honey_supply >= beehive_cost:
                    towers.add(Beehive((mouse_pos[0]-32,mouse_pos[1]-32),1,0.5,600))
                    honey_supply -= beehive_cost
                elif selected == "Honeycannon" and not on_track and honey_supply >= honeycannon_cost:
                    towers.add(Honeycannon((mouse_pos[0]-32,mouse_pos[1]-32),1.5,1.5,600))
                    honey_supply -= honeycannon_cost
    
    if wave <= 5 and not done:
        if to_spawn == 0:
            to_spawn = wave*5
        #If the last spawn was a least a second ago, spawn another
        present = time.time()
        if last_spawn - present < -1 and to_spawn > 0:
            enemies.add(Enemy((0,325),100,1,1,pygame.image.load("Resources\\walmart.png")))
            to_spawn -= 1
            last_spawn = time.time()
        if to_spawn == 0:
            done = True
    elif wave > 5 and wave < 11 and not done:
        if to_spawn == 0:
            to_spawn = (wave-5)*5
        #If the last spawn was a least a second ago, spawn another
        present = time.time()
        if last_spawn - present < -1 and to_spawn > 0:
            enemies.add(Enemy((0,325),300,2,0.04,pygame.image.load("Resources\\noigelist.png")))
            to_spawn -= 1
            last_spawn = time.time()
        if to_spawn == 0:
            done = True
    elif not done:
        if to_spawn == 0:
            to_spawn = (wave-5)*5
        #If the last spawn was a least a second ago, spawn another
        present = time.time()
        if last_spawn - present < -1 and to_spawn > 0:
            enemies.add(Enemy((0,325),5000,1,1,pygame.image.load("Resources\\Intezarr.png")))
            to_spawn -= 1
            last_spawn = time.time()
        if to_spawn == 0:
            done = True

    for i in enemies:
        i.update(waypoints[i.next_waypoint_idx])
        if i.at_waypoint(waypoints[i.next_waypoint_idx],2):
            if i.next_waypoint_idx > len(waypoints) - 1:
                i.kill()
                lives -= 1
        if i.health <= 0:
            i.kill()
            honey_supply += 1
    for i in towers:
        if  time.time() - i.last_shot > i.fire_rate:
            i.fire()
    for i in projectiles:
        if i.type == "Bee":
            i.target = i.find_target(waypoints)
        i.move(i.target)
        i.has_hit()
    
    #Ensures that the button wasn't pressed too recently.
    if time.time() - beellista_icon.start_time > 0.25:
        if beellista_icon.draw(): 
            if selected == "Beellista":
                selected = ""
            else:
                selected = "Beellista"
    if time.time() - beehive_icon.start_time > 0.25:
        if beehive_icon.draw(): 
            if selected == "Beehive":
                selected = ""
            else:
                selected = "Beehive"
    if time.time() - honeycannon_icon.start_time > 0.25:
        if honeycannon_icon.draw(): 
            if selected == "Honeycannon":
                selected = ""
            else:
                selected = "Honeycannon"

    if selected == "":
        mouse_rect = pygame.Rect(mouse_pos[0],mouse_pos[1],5,5)
        if pygame.Rect.colliderect(mouse_rect,beellista_icon):
            flavor_text = "The Beellista\n[FLAVOR TEXT HERE]"
        elif pygame.Rect.colliderect(mouse_rect,beehive_icon):
            flavor_text = "The Beehive\n[FLAVOR TEXT HERE]"
        elif pygame.Rect.colliderect(mouse_rect,honeycannon_icon):
            flavor_text = "The Honeycannon\n[FLAVOR TEXT HERE]"
    wave_display = wavetext.render(f"Wave: {wave}",True,(255,255,255))
    selected_display = selectedtext.render(selected,True,(0,0,0))
    honey_display = honeytext.render(f"Honey: {honey_supply}",True,(0,0,0))
    enemies.draw(screen)
    towers.draw(screen)
    projectiles.draw(screen)
    screen.blit(pygame.image.load("Resources\\sign.png"),(880,1075))
    screen.blit(wave_display, (1300,1100))
    screen.blit(beellista_icon.img, (beellista_icon.x, beellista_icon.y))
    screen.blit(beehive_icon.img, (beehive_icon.x, beehive_icon.y))
    screen.blit(honeycannon_icon.img, (honeycannon_icon.x, honeycannon_icon.y))
    screen.blit(honey_display,(1300,440))
    
    flavor_list = flavor_text.splitlines()
    lines = 0
    for i in flavor_list:
        lines += 1
        flavor_display = flavortext.render(i,True,(0,0,0))
        screen.blit(flavor_display,(1250,280 +(lines * 20)))


    screen.blit(selected_display,(mouse_pos[0]+10,mouse_pos[1]-5))
    pygame.display.flip()