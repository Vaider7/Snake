import pygame as pg
import random        
pg.init()
pg.mixer.init()
Sounds={'eat':'sounds\Eatting.ogg','die':'sounds\Dying.ogg'}
#'music\RetroWave.mp3''music\Kda_-_Popstars.mp3''music\Savlonic-The Rider.mp3'
Music = ['music\RetroWave.mp3',"""'music\Kda_-_Popstars.mp3','music\Savlonic-The Rider.mp3'"""]
playedMus=[]
Snake_head = [pg.image.load('sprites\Snake_head_w.png'),pg.image.load('sprites\Snake_head_d.png'),
              pg.image.load('sprites\Snake_head_s.png'),pg.image.load('sprites\Snake_head_a.png')]
Snake_body = [pg.image.load('sprites\Snake_body_v.png'),pg.image.load('sprites\Snake_body_h.png'),
              pg.image.load('sprites\Snake_body_v.png'),pg.image.load('sprites\Snake_body_h.png'),
              pg.image.load('sprites\Snake_body_t_wd.png'),pg.image.load('sprites\Snake_body_t_wa.png'),
              pg.image.load('sprites\Snake_body_t_sd.png'),pg.image.load('sprites\Snake_body_t_sa.png')]

Snake_tail = [pg.image.load('sprites\Snake_tail_w.png'),pg.image.load('sprites\Snake_tail_d.png'),
              pg.image.load('sprites\Snake_tail_s.png'),pg.image.load('sprites\Snake_tail_a.png')]

Fruits=[pg.image.load('sprites\Fruit.png'),pg.image.load('sprites\GFruit.png')]

def playmusic(q,vol):
    #chan=pg.mixer.Channel(0)
    global playedMus,Music,TimesPlayed
    if TimesPlayed==len(Music):
        playedMus=[]
        random.shuffle(Music)
        q=1
        TimesPlayed=0
        return
    name=Music[q]
    playedMus.append(name)
    TimesPlayed+=1
    pg.mixer.music.load(name)
    pg.mixer.music.set_volume(vol)
    pg.mixer.music.play(0)
    
def testMusic(i):
    if pg.mixer.music.get_busy()==0:
        playmusic(i,1)
    #sound=pg.mixer.Sound(name)
    #chan.set_volume(vol)
    #chan.play(sound,i)
def playsound(name,i,vol):
    chan=pg.mixer.Channel(1)
    sound=pg.mixer.Sound(name)
    chan.set_volume(vol)
    chan.play(sound,i)
def text_objects(text, font,i):
    global sur
    textSurface = font.render(text, True,(i,i,i))
    return textSurface, textSurface.get_rect()

def button(msg,sur,x,y,w,h,ic,ac,i,act=None):
    global mouse, click
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pg.draw.rect(sur, ac,(x,y,w,h))
        if click[0] == 1 and act != None:
            act()
    else:
        pg.draw.rect(sur, ic,(x,y,w,h))
          
    smallText = pg.font.Font("ConnectionSerif.otf",30)
    textSurf, textRect = text_objects(msg, smallText,i)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    sur.blit(textSurf, textRect)

def polzinormalno():
    global dirmove, tailmove, Slen
    for i in range(0,Slen-2):
        if ((tailmove[i+1]==0) and (tailmove[i]==1)) or ((tailmove[i+1]==3) and (tailmove[i]==2)): 
            dirmove[i]=4
        if ((tailmove[i+1]==0) and (tailmove[i]==3)) or ((tailmove[i+1]==1) and (tailmove[i]==2)): 
            dirmove[i]=5
        if ((tailmove[i+1]==2) and (tailmove[i]==1))or((tailmove[i+1]==3)and(tailmove[i]==0)): 
            dirmove[i]=6
        if ((tailmove[i+1]==2) and (tailmove[i]==3))or((tailmove[i+1]==1)and(tailmove[i]==0)):
            dirmove[i]=7


def drawsur():
    global sur,size, Fruit, GFruit, GFExis, move, dirmove, Slen, Snakehead, Snake, Snake_head, Snake_body
    sur.fill((0,0,0))
    dir=0
    #Drawing Fruits
    if GFExis:
        sur.blit(Fruits[1],(GFruit[0],GFruit[1]))

    sur.blit(Fruits[0],(Fruit[0],Fruit[1]))

    #Drawing Snake
    if move=='w':
        dir=0
    if move=='d':
        dir=1
    if move=='s':
        dir=2
    if move=='a':
        dir=3
    sur.blit(Snake_head[dir],(Snakehead[0],Snakehead[1]))

    for i in range(0,Slen-2):
        sur.blit(Snake_body[dirmove[i]],(Snake[i][0],Snake[i][1]))

    sur.blit(Snake_tail[tailmove[Slen-2]],(Snake[Slen-2][0],Snake[Slen-2][1]))
    
    pg.display.update()
    


def initFruit(W,H,size,Fruit,Snake,Snakehead,Slen):
    ex=True
    while ex:
      fx=random.randint(10,(W/size-1))*size
      fy=random.randint(10,(H/size-1))*size
      Fruit=[fx,fy]
      if Fruit in Snake:
          ex = True
      else:
          ex=False
    return Fruit
      
def quit():
    global menu, work
    menu=False
    work=False


def playsnake():
    global play, menu
    play=True
    menu=False



    
    
work=True
play=False
menu=True
intro=True

TimesPlayed=0

event=pg.event.get()
mouse=pg.mouse.get_pos()
click=pg.mouse.get_pressed()
#random.shuffle(Music)
testMusic(TimesPlayed)
while work :
    W=800
    H=600
    pg.init()
    sur=pg.display.set_mode(size=(W,H),flags=pg.FULLSCREEN)
    while intro:
        for i in range(0,256):
            largeText = pg.font.SysFont('times new roman', 40)
            TextSurf, TextRect=text_objects('The Game by Aytomik and Vaider',largeText,i)
            TextRect.center = ((400),(300))
            sur.blit(TextSurf, TextRect)
            pg.display.update()
            sur.fill((0,0,0))
            pg.time.delay(15)
            if i == 225:
                menu=True
                intro=False
            event=pg.event.get()
            keys=pg.key.get_pressed()
            if keys[pg.K_SPACE]:
                menu=True
                intro=False
                break
    while menu:
        pg.time.delay(60)
        for event in pg.event.get():
                keys=pg.key.get_pressed()
                mouse=pg.mouse.get_pos()
                click=pg.mouse.get_pressed()
                if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                    play = False
                    pg.quit()
                    break
        n=255
        button('Play',sur,W/2-35,H/2-20,125,32,(0,50,0),(100,200,100),n,playsnake)
        button('Quit',sur,W/2-35,H/2+20,125,32,(50,0,0),(200,100,100),n,quit)
        
        pg.display.update()
        sur.fill((0,0,0))
        if pg.mixer.music.get_busy()==0:
            testMusic(TimesPlayed)
    if play==True:
        size=10
        speed=1*size
        FPS = 10
        Snakehead=[None,None]
        Snake=[]
        dirmove=[]
        tailmove=[]
        Slen=10
        mult=3
        Counter2=Slen-2
        x = random.randint(Slen,int(W/size))*size
        y = random.randint(0,int(H/size))*size
        sur=pg.display.set_mode(size=(W,H),flags = pg.FULLSCREEN)
        pg.display.set_caption('Snake')
        play=True
        xm = 0
        ym = 0
        move='d'
        if move=='w':
            ym=-speed
        if move=='s':
            ym=speed
        if move=='a':
            xm=-speed
        if move=='d':
            xm=speed

        for i in range(0,Slen-1):
            Snake.append([None]*2)
            dirmove.append(1)
            tailmove.append(1)
        for i in range(0,Slen-1):
            Snake[i]=[(x-(1+i)*size),y]
        Fruit=[None,None]
        GFruit=[None,None]
        GFExis=False
        bool=True
        counter=0
        index=0
        Fruit=initFruit(W,H,size,Fruit,Snake,Snakehead,Slen)
        GFruit=initFruit(W,H,size,Fruit,Snake,Snakehead,Slen)
        while play:
            pressed=False
            pg.time.delay(60)
            for event in pg.event.get():
                keys=pg.key.get_pressed()

                if event.type == pg.QUIT or keys[pg.K_ESCAPE] :
                    play = False
                    pg.quit()
                    break
            Snakehead=[x,y]
            
            
            if counter>=5:
                GFExis=True                                                
                if index>100:
                    counter=0
                    index=0
                    GFExis=False
                    GFruit=initFruit(W,H,size,Fruit,Snake,Snakehead,Slen)
                index+=1
                if Snakehead==GFruit:
                    GFruit=initFruit(W,H,size,Fruit,Snake,Snakehead,Slen)
                    for i in range(0,3*mult):
                            dirmove.append(int(dirmove[Slen-2])) 
                            tailmove.append(int(tailmove[Slen-2])) 
                            Snake.append([Snake[Slen-2][0],Snake[Slen-2][1]])
                    Slen+=3*mult
                    counter=0
                    index=0
                    GFExis=False


        
            if Snakehead in Snake:
                playsound(Sounds['die'],0,0.7)
                pg.time.delay(1000)
                menu=True
                play = False
                break

            if Snakehead==Fruit:
                playsound(Sounds['eat'],0,1)
                Fruit=initFruit(W,H,size,Fruit,Snake,Snakehead,Slen)
                for i in range(0,mult):
                    Snake.append([Snake[Slen-2][0],Snake[Slen-2][1]]) 
                    dirmove.append(int(dirmove[Slen-2])) 
                    tailmove.append(int(tailmove[Slen-2]))   #Snake.append([Snake[Slen-3][0],Snake[Slen-3][1]])
                Slen+=mult
                counter+=1

            if not pressed:
                if keys[pg.K_w] and (not(move == 's')):
                    move = 'w'
                    ym=-speed
                    xm=0
                    pressed=True
                elif keys[pg.K_s] and (not(move == 'w')):
                    move = 's'
                    ym=speed
                    xm=0
                    pressed=True
                elif keys[pg.K_a] and (not(move == 'd')):
                    move = 'a'
                    xm=-speed
                    ym=0
                    pressed=True
                elif keys[pg.K_d] and (not(move == 'a')):
                    move = 'd'
                    xm=speed
                    ym=0
                    pressed=True
    
            x+=xm
            y+=ym
            if x<size:
                x=W-size
            if x>(W-size):
                x=size
            if y<size:
                y=H-size
            if y>(H-size):
                y=size
            drawsur()

           
            for i in range((Slen-2),(-1),-1):
                Snake[i]=[(Snake[i-1][0]),(Snake[i-1][1])]
            Snake[0]=[Snakehead[0],Snakehead[1]]
            for i in range((Slen-2),(-1),-1):
                dirmove[i]=int(dirmove[i-1])
            if move=='w':
                dirmove[0]=0
            if move=='d':
                dirmove[0]=1
            if move=='s':
                dirmove[0]=2
            if move=='a':
                dirmove[0]=3

            for i in range((Slen-2),(-1),-1):
                tailmove[i]=int(tailmove[i-1])
            if move=='w':
                tailmove[0]=0
            if move=='d':
                tailmove[0]=1
            if move=='s':
                tailmove[0]=2
            if move=='a':
                tailmove[0]=3


            polzinormalno() 
            if pg.mixer.music.get_busy()==0:
                testMusic(TimesPlayed)