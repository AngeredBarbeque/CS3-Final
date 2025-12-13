from classes import *

def multiline(font,text="Default",color=(0,0,0),x=0,y=0,spacing=64):
    lines = 0
    for i in text.splitlines():
        lines += 1
        text = font.render(i,True,color)
        screen.blit(text,(x,y +(lines * spacing)))




pygame.init()
screen = pygame.display.set_mode((1600, 1200))
pygame.display.set_caption("The Siege of Walmartville")
pygame.display.set_icon(pygame.image.load("Resources//Honey.png"))

background = pygame.image.load("Resources\\background.jpg")

selectedtext = pygame.font.Font("Resources\\Times New Roman Regular.ttf",14)
wavetext = pygame.font.Font("Resources\\Times New Roman Regular.ttf",64)
honeytext = pygame.font.Font("Resources\\Times New Roman Regular.ttf",64)
lifetext = pygame.font.Font("Resources\\Times New Roman Regular.ttf",32)
flavortext = pygame.font.Font("Resources\\Times New Roman Regular.ttf",30)
basictext = pygame.font.Font("Resources\\Times New Roman Regular.ttf",64)

waypoints = [(620,325),(620,150),(885,150),(885,610),(375,610),(375,895),(955,895),(955,1190)]

wewart = pygame.image.load("Resources\\closed_wewart.png")
wewart_talk = pygame.image.load("Resources\\open_wewart.png")
wewart = pygame.transform.flip(wewart,True,False)
wewart_talk = pygame.transform.flip(wewart_talk,True,False)
wewart = pygame.transform.scale(wewart,(int(wewart.get_width() * 1.3),int(wewart.get_height() * 1.3)))
wewart_talk = pygame.transform.scale(wewart_talk,(int(wewart_talk.get_width() * 1.3),int(wewart_talk.get_height() * 1.3)))
wewart_rect = pygame.rect.Rect(1330,50,wewart.get_width(),wewart.get_height())
honey_icon = pygame.image.load("Resources\\Honey.png")
honey_icon = pygame.transform.scale(honey_icon,(int(honey_icon.get_width()*1.5),int(honey_icon.get_height()*1.5)))
honey_rect = pygame.rect.Rect(1370,520,honey_icon.get_width(),honey_icon.get_height())
lives_icon = pygame.image.load("Resources\\lives.png")
lives_icon = pygame.transform.scale(lives_icon,(lives_icon.get_width()*2,lives_icon.get_height()*2))
lives_rect = pygame.rect.Rect(1250,10,lives_icon.get_width(),lives_icon.get_height())
tree_rect = pygame.rect.Rect(40,824,68,96)
sign_rect = pygame.rect.Rect(880,1075,206,133)

beellista_icon = Button((1267,365),"Resources/Beellista.png",1)
beehive_icon = Button((1387,365),"Resources//Hive.png",1)
honeycannon_icon = Button((1507,365),"Resources/Honeycannon.png",1)
start = Button((1287,1000),"Resources//start.png",5)

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

beellista_cost = 6
honeycannon_cost = 3
beehive_cost = 2
to_spawn = 0
last_spawn = 0
last_swap = 0
flavor_text = ""
selected = ""
lives = 20
wave = 0
honey_supply = 10
running = True
tutorial = True
start_time = time.time()
win_text = "Congratulations, comrade!\nFor your bravery and skill,\nyou have been promoted to\nWewart's personal military advisor,\nand you have recieved a $5 gift\ncard for Beemart!"
death_text = "You have disappointed Wewart, comrade.\nYou will be stripped of your title, and live\nthe remainder of your life in the honey\nmines. Be grateful for Wewart's mercy,\ncomrade."
tutorial_text = "You are one of Walmartville's outer\ndefenders. A force of angry Walmart\nemployees is approaching the city.\nOn its own, this is not unusal.\nHowever, there are rumours\nthat something more sinister brews\non the horizon... For this reason,\nthe Glorious Wewart has agreed to\nacompany you today. You\nhave a short preperation\nperiod beforce they arrive."
pygame.mixer.music.load("Resources\\main_theme.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)
end_music = False
talking = False
while running: 
    since_start = time.time() - start_time
    if honey_supply > 99:
        honey_supply = 99
    flavor_text = ""
    mouse_pos = pygame.mouse.get_pos()
    if enemies.sprites() == [] and wave <= 11 and not tutorial and lives > 0:
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
                    towers.add(Beellista((mouse_pos[0]-64,mouse_pos[1]-64),2,2,300))
                    honey_supply -= beellista_cost
                elif selected == "Beehive" and not on_track and honey_supply >= beehive_cost:
                    towers.add(Beehive((mouse_pos[0]-32,mouse_pos[1]-32),1,0.5,200))
                    honey_supply -= beehive_cost
                elif selected == "Honeycannon" and not on_track and honey_supply >= honeycannon_cost:
                    towers.add(Honeycannon((mouse_pos[0]-48,mouse_pos[1]-48),1.5,1.5,300))
                    honey_supply -= honeycannon_cost
    if not tutorial and lives > 0:
        if wave <= 5 and not done:
            if to_spawn == 0:
                to_spawn = wave*5
            #If the last spawn was a least a second ago, spawn another
            present = time.time()
            if last_spawn - present < -1 and to_spawn > 0:
                enemies.add(Enemy((0,325),100,1,1,pygame.image.load("Resources\\walmart.png"),"Walmart"))
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
                enemies.add(Enemy((0,325),300,2,0.04,pygame.image.load("Resources\\noigelist.png"),"Fish"))
                to_spawn -= 1
                last_spawn = time.time()
            if to_spawn == 0:
                done = True
        elif wave == 11 and not done:
            to_spawn = 1
            #If the last spawn was a least a second ago, spawn another
            if to_spawn > 0:
                enemies.add(Enemy((0,325),5000,1,1,pygame.image.load("Resources\\Intezarr.png"),"Intezarr"))
                to_spawn -= 1
            if to_spawn == 0:
                done = True
    if lives > 0:
        for i in enemies:
            i.update(waypoints[i.next_waypoint_idx])
            if i.at_waypoint(waypoints[i.next_waypoint_idx],2):
                if i.next_waypoint_idx > len(waypoints) - 1:
                    i.kill()
                    if i.type == "Walmart":
                        lives -= 1
                    elif i.type == "Fish":
                        lives -= 2
                    elif i.type == "Intezarr":
                        lives = 0
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
    if lives <= 0:
        if start.draw():
            enemies.empty()
            projectiles.empty()
            towers.empty()
            lives = 20
            wave = 0
            honey_supply = 10
            to_spawn = 0
            last_spawn = 0
            start_time = time.time()
            pygame.mixer.music.fadeout(2000)
            pygame.mixer.music.load("Resources\\main_theme.mp3")
            pygame.mixer.music.play(-1)
            end_music = False
    elif tutorial:
        if start.draw():
            tutorial = False

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

    if selected == "" and lives > 0:
        if wave != 11:
            mouse_rect = pygame.Rect(mouse_pos[0],mouse_pos[1],5,5)
            if pygame.Rect.colliderect(mouse_rect,beellista_icon):
                flavor_text = "The Beellista\nThe beellista is my personal\nfavorite machine of war. It\nlaunches a deadly bolt,\nwhich then splits into a\nsmall amount of bees.\nCost: 6 Honey."
            elif pygame.Rect.colliderect(mouse_rect,beehive_icon):
                flavor_text = "The Beehive\nThe humble beehive releases\na consistent amount of bees\nto swarm your enemies.\nCost: 2 Honey."
            elif pygame.Rect.colliderect(mouse_rect,honeycannon_icon):
                flavor_text = "The Honeycannon\nThe honeycannon is a\nmarvel of engineering. After\nsplattering an opponent with\nenough honey, you will\nbreak their spirits and they\nwill be unable to continue.\nCost: 3 Honey."
            elif pygame.Rect.colliderect(mouse_rect,wewart_rect):
                flavor_text = "Get out of my face!"
            elif pygame.Rect.colliderect(mouse_rect,honey_rect):
                flavor_text = "That's your honey.\nYou can use your honey to\npurchase defenses."
            elif pygame.Rect.colliderect(mouse_rect,tree_rect):
                flavor_text = "That's my favorite tree.\nDon't mess with it."
            elif pygame.Rect.colliderect(mouse_rect,sign_rect):
                flavor_text = "That's the entrance to \nWalmartville. It's\nthe most wonderful\nplace to live on earth.\nProtect it with your life."
            elif pygame.Rect.colliderect(mouse_rect,lives_rect):
                flavor_text = "That's your life count.\nIf you let too many enemies\nthrough, you'll be punished."
            elif tutorial:
                flavor_text = "Hover your mouse over\nsomething without a tower\nselected, and I'll tell you\nabout it!\n(Click a tower icon again to\nunselect it.)\nPress the Start button to\nbegin."
            else:
                flavor_text = "Hover your mouse over\nsomething without a tower\nselected, and I'll tell you\nabout it!\n(Click a tower icon again to\nunselect it.)"
    elif wave == 11 and lives > 0:
        flavor_text = "Intezarr!?\nStand your ground, comrade.\nThe stakes are higher than we thought!"
    elif tutorial and lives > 0:
        flavor_text = "Hover your mouse over\nsomething without a tower\nselected, and I'll tell you\nabout it!\n(Click a tower icon again to\nunselect it.)\nPress the Start button to\nbegin."
    elif lives > 0:
        flavor_text = "Hover your mouse over\nsomething without a tower\nselected, and I'll tell you\nabout it!\n(Click a tower icon again to\nunselect it.)"
    wave_display = wavetext.render(f"Wave: {wave}",True,(255,255,255))
    selected_display = selectedtext.render(selected,True,(0,0,0))
    honey_display = honeytext.render(f"{honey_supply}",True,(0,0,0))
    lives_display = lifetext.render(f"{lives}",True,(0,0,0))
    enemies.draw(screen)
    towers.draw(screen)
    projectiles.draw(screen)
    if tutorial and since_start < 17:
        multiline(basictext,tutorial_text,(255,255,255),150,180,64)
    if lives <= 0:
        multiline(basictext,death_text,(255,255,255),150,180,64)
        start.x = 600
        start.y = 600
        start.rect.x = 600
        start.rect.y = 600
        if not end_music:
            pygame.mixer.music.fadeout(2000)
            pygame.mixer.music.load("Resources\\intezarr.mp3")
            pygame.mixer.music.play(-1)
            end_music = True
    if wave > 11:
        multiline(basictext,win_text,(255,255,255),150,180,64)
    screen.blit(pygame.image.load("Resources\\sign.png"),(880,1075))
    screen.blit(wave_display, (1300,1100))
    screen.blit(beellista_icon.img, (beellista_icon.x, beellista_icon.y))
    screen.blit(beehive_icon.img, (beehive_icon.x, beehive_icon.y))
    screen.blit(honeycannon_icon.img, (honeycannon_icon.x, honeycannon_icon.y))
    if tutorial or end_music:
        screen.blit(start.img, (start.x, start.y))
    if talking and time.time() - last_swap > 0.1 and flavor_text !="Hover your mouse over\nsomething without a tower\nselected, and I'll tell you\nabout it!\n(Click a tower icon again to\nunselect it.)\nPress the Start button to\nbegin." and flavor_text != "Hover your mouse over\nsomething without a tower\nselected, and I'll tell you\nabout it!\n(Click a tower icon again to\nunselect it.)" and flavor_text != "Intezarr!?\nStand your ground, comrade.\nThe stakes are higher than we thought!":
        screen.blit(wewart,(1300,20))
        talking = False
        last_swap = time.time()
    elif not talking and time.time() - last_swap > 0.1 and flavor_text !="Hover your mouse over\nsomething without a tower\nselected, and I'll tell you\nabout it!\n(Click a tower icon again to\nunselect it.)\nPress the Start button to\nbegin." and flavor_text != "Hover your mouse over\nsomething without a tower\nselected, and I'll tell you\nabout it!\n(Click a tower icon again to\nunselect it.)" and flavor_text != "Intezarr!?\nStand your ground, comrade.\nThe stakes are higher than we thought!":
        screen.blit(wewart_talk,(1300,20))
        talking = True
        last_swap = time.time()
    elif flavor_text == "Hover your mouse over\nsomething without a tower\nselected, and I'll tell you\nabout it!\n(Click a tower icon again to\nunselect it.)\nPress the Start button to\nbegin." or flavor_text == "Hover your mouse over\nsomething without a tower\nselected, and I'll tell you\nabout it!\n(Click a tower icon again to\nunselect it.)" or flavor_text == "Intezarr!?\nStand your ground, comrade.\nThe stakes are higher than we thought!" or flavor_text == "":
        screen.blit(wewart,(1300,20))
    elif not talking:
        screen.blit(wewart,(1300,20))
    elif talking:
        screen.blit(wewart_talk,(1300,20))
    screen.blit(honey_display,(1385,600))
    screen.blit(honey_icon,(1370,520))
    screen.blit(lives_icon,(1250,10))
    screen.blit(lives_display,(1300,22))
    
    multiline(flavortext,flavor_text,(0,0,0),1250,680,30)

    screen.blit(selected_display,(mouse_pos[0]+10,mouse_pos[1]-5))
    pygame.display.flip()